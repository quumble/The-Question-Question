"""POST-CALIBRATION reporting only. No API calls; never changes frozen labels.
Reconciles every reservation/settlement with its raw request/response artifacts,
then derives synthetic diagnostic tables. These are NOT factorial study results.
"""
import collections,csv,datetime,hashlib,json,pathlib
from decimal import Decimal
import study as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def get_json(text):
    clean=text.strip()
    if clean.startswith('```'):
        import re
        clean=re.sub(r'^```(?:json)?\s*|\s*```$','',clean)
    return json.loads(clean)

def main():
    responses=s.rows(ROOT/'calibration_responses.jsonl');fixtures={f['id']:f for f in json.loads((ROOT/'synthetic/fixtures.json').read_text())}
    events=s.rows(ROOT/'ledger.jsonl');attempts,settled,pending=s.accounting(events)
    reservations={x['attempt_id']:x for x in events if x['event']=='reserve'}
    settlements={x['attempt_id']:x for x in events if x['event']=='settle'}
    byprovider=collections.defaultdict(lambda:dict(calls=0,input_tokens=0,output_tokens=0,cost=Decimal(0)))
    byrun=collections.defaultdict(lambda:dict(calls=0,cost=Decimal(0),first=None,last=None))
    diagnostic=[];used_files=set()
    for r in responses:
        aid=r['attempt_id'];provider=r['provider'];version='v2' if r['id'].startswith('v2__') else 'v1'
        task=r['id'].removeprefix('v2__');fixture_id=task.rsplit('_',1)[0];f=fixtures[fixture_id]
        reqpath=ROOT/'raw/calibration'/(aid+'.request.json');respath=ROOT/'raw/calibration'/(aid+'.response.json')
        used_files.update([reqpath,respath]);req=json.loads(reqpath.read_text());res=json.loads(respath.read_text())
        assert s.digest(reqpath)==reservations[aid]['request_sha256'];assert s.digest(respath)==settlements[aid]['response_sha256']
        assert req['task_id']==r['id'] and req['provider']==provider and req['kind']=='calibration'
        assert req['payload']['model']==s.MODELS[provider] and res['body']['model']==s.MODELS[provider]
        assert res['status']==200
        inp,out,cost=s.charge(provider,res['body']);assert cost==Decimal(settlements[aid]['cost_usd'])==Decimal(r['cost_usd'])
        assert (inp,out)==(settlements[aid]['input_tokens'],settlements[aid]['output_tokens'])
        text,finish=s.extract(provider,res['body']);assert text==r['text'] and finish==r['finish_reason']
        assert not s.participation_signals(text,'calibration',f['text'])
        g=byprovider[provider];g['calls']+=1;g['input_tokens']+=inp;g['output_tokens']+=out;g['cost']+=cost
        g=byrun[version];g['calls']+=1;g['cost']+=cost;g['first']=g['first'] or reservations[aid]['at'];g['last']=settlements[aid]['at']
        record={'run':version,'fixture':fixture_id.removeprefix('synthetic_'),'coder':provider,'task_id':r['id'],'truncated':r['truncated'],'cost_usd':str(cost),'expected':{**{k:v[0] for k,v in f['expected'].items()},'substitution':f['expected_substitution']}}
        try:
            c=s.parse_code(text,f['text']);record['schema_valid']=True
            record['labels']={**{k:c[k]['label'] for k in ['E','F','H','A']},'substitution':c['substitution']}
            passed=s.calibration_pass(c,f,r['truncated']);record['passed']=passed
            record['reason']='pass' if passed else 'semantic_disagreement_with_authored_expectation'
            record['details']='; '.join(k+': '+str(record['labels'][k])+' vs '+str(v) for k,v in record['expected'].items() if record['labels'][k]!=v)
        except Exception as e:
            record.update(schema_valid=False,passed=False,reason='engineering_truncation' if r['truncated'] else 'engineering_format',details=type(e).__name__+': '+str(e))
            # Raw parseable labels are displayed for diagnostics only, never rescued
            # into the frozen gate or agreement denominators.
            try:
                c=get_json(text);record['raw_labels_unvalidated']={**{k:c[k]['label'] for k in ['E','F','H','A']},'substitution':c['substitution']}
            except Exception:pass
        diagnostic.append(record)
    assert len(responses)==len(attempts)==len(settlements)==38
    assert len({r['attempt_id'] for r in responses})==38
    assert set((ROOT/'raw/calibration').glob('*.json'))==used_files
    assert sum(g['cost'] for g in byprovider.values())==settled==Decimal('0.1342155') and pending==0
    assert not s.rows(ROOT/'study_responses.jsonl') and not s.rows(ROOT/'coding_responses.jsonl')
    assert (ROOT/'STOP.json').exists()
    clearance=json.loads((ROOT/'reviews/CLEARANCE.json').read_text())
    for path,sha in clearance['sha256'].items():assert s.digest(ROOT/path)==sha,path
    for g in list(byprovider.values())+list(byrun.values()):g['cost_usd']=str(g.pop('cost'))
    agreement={}
    for version in ['v1','v2']:
        data={(d['fixture'],d['coder']):d for d in diagnostic if d['run']==version}
        paired=[]
        for fixture in sorted({d['fixture'] for d in diagnostic if d['run']==version}):
            left=data.get((fixture,'openai'));right=data.get((fixture,'anthropic'))
            if left and right and left['schema_valid'] and right['schema_valid'] and not left['truncated'] and not right['truncated']:paired.append((left,right))
        fields={}
        for k in ['E','F','H','A','substitution']:
            tab=collections.Counter((str(l['labels'][k]),str(r['labels'][k])) for l,r in paired)
            fields[k]={'agree':sum(l['labels'][k]==r['labels'][k] for l,r in paired),'denominator':len(paired),'cross_tab':[{'openai':a,'anthropic':b,'n':n} for (a,b),n in sorted(tab.items())]}
        agreement[version]={'joint_schema_valid_fixtures':len(paired),'all_fields_agree':sum(l['labels']==r['labels'] for l,r in paired),'fields':fields,'scope':'Synthetic diagnostics only; not study overlap agreement or validation against human gold.'}
    (ROOT/'analysis').mkdir(exist_ok=True)
    (ROOT/'analysis/calibration_diagnostics.json').write_text(json.dumps({'scope':'POST-CALIBRATION SYNTHETIC DIAGNOSTICS; main N=0','rows':diagnostic,'agreement':agreement},indent=2))
    with (ROOT/'analysis/calibration_diagnostics.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=['run','fixture','coder','schema_valid','passed','reason','details','truncated','cost_usd']);writer.writeheader()
        for d in diagnostic:writer.writerow({k:d[k] for k in writer.fieldnames})
    status={'scope':'Final cumulative API reconciliation; no experimental study responses','main_planned_n':192,'main_observed_n':0,'main_missing_n':192,'calibration_calls':38,'settled_usd':str(settled),'unresolved_usd':str(pending),'exposure_usd':str(settled+pending),'by_provider':byprovider,'by_run':byrun,'raw_request_files':38,'raw_response_files':38,'all_ledger_raw_hashes_match':True,'frozen_hashes_match':True,'active_stop':json.loads((ROOT/'STOP.json').read_text()),'api_execution_closed':True,'remaining_work':'Final independent review and archive verification; no further paid execution authorized.'}
    (ROOT/'COMPLETION_REPORT.json').write_text(json.dumps(status,indent=2))
    lines=['# Synthetic calibration diagnostics','', 'Post-calibration reporting only. These rows are not observations from the factorial study. PASS means every frozen check passed; SEM means disagreement with authored expectations, not established error; FMT means format validation failed; TRUNC means output truncation. NR means not run.','', '| Fixture | v1 GPT | v1 Sonnet | v2 GPT | v2 Sonnet |','|---|---|---|---|---|']
    lookup={(d['run'],d['fixture'],d['coder']):d for d in diagnostic}
    for f in fixtures:
        name=f.removeprefix('synthetic_');cells=[]
        for v,p in [('v1','openai'),('v1','anthropic'),('v2','openai'),('v2','anthropic')]:
            d=lookup.get((v,name,p));cells.append('NR' if not d else {'pass':'PASS','semantic_disagreement_with_authored_expectation':'SEM','engineering_format':'FMT','engineering_truncation':'TRUNC'}[d['reason']])
        lines.append('| '+name+' | '+' | '.join(cells)+' |')
    lines+=['','## Agreement on jointly schema-valid synthetic fixture judgments','', '| Run | Joint-valid fixtures | All five fields agree | E | F | H | A | Substitution |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for v,g in agreement.items():lines.append('| '+v+' | '+str(g['joint_schema_valid_fixtures'])+' | '+str(g['all_fields_agree'])+' | '+' | '.join(str(g['fields'][k]['agree'])+'/'+str(g['fields'][k]['denominator']) for k in ['E','F','H','A','substitution'])+' |')
    lines+=['','Agreement conditions on valid output and is descriptive only. Selection differs by run. No kappa, population confidence interval, or claim of human validation is warranted. Endpoint-pair cross-tabs and raw unvalidated labels are in calibration_diagnostics.json. Both coders flagged substitution on the v2 correction fixture; the flag agreed while E/F interpretations differed. The planned 64-response study overlap never occurred.','', '## Failure details','']
    for d in diagnostic:
        if not d['passed']:lines.append('- '+d['run']+' / '+d['fixture']+' / '+d['coder']+': '+d['reason']+'; '+d['details'])
    (ROOT/'analysis/CALIBRATION_DIAGNOSTICS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'attempts':38,'settled_usd':str(settled),'unresolved_usd':str(pending),'main_n':0,'agreement':agreement},indent=2))
if __name__=='__main__':main()
