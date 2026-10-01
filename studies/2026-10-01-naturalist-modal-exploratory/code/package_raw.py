"""Create a readable raw transcript and mechanical completeness record; no coding."""
import datetime, hashlib, json, pathlib, os
from decimal import Decimal
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(name): return [json.loads(s) for s in (ROOT/name).read_text().splitlines()] if (ROOT/name).exists() else []
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
manifest=json.loads((ROOT/'manifest.json').read_text())['observations']
responses=read('responses.jsonl'); ledger=read('ledger.jsonl'); reviews=read('safety_reviews.jsonl')
assert len({r['id'] for r in responses})==len(responses)
reserved={e['id']:Decimal(e['reserved_usd']) for e in ledger if e['event']=='reserve'}
settled={e['id']:Decimal(e['cost_usd']) for e in ledger if e['event']=='settle'}
assert len(reserved)==sum(e['event']=='reserve' for e in ledger)
assert len(settled)==sum(e['event']=='settle' for e in ledger)
assert set(settled)<=set(reserved)
assert all(v<=reserved[k] for k,v in settled.items())
assert {r['id'] for r in responses}==set(settled)
assert {r['id'] for r in reviews}==set(settled)
assert all(not r['participation_objection_or_apparent_distress'] for r in reviews)
for r in responses:
    x=next(x for x in manifest if x['id']==r['id'])
    prefix=ROOT/'raw'/r['id']
    for side in ['request','response']:
        raw=pathlib.Path(str(prefix)+f'.{side}-body.json').read_bytes()
        meta=json.loads(pathlib.Path(str(prefix)+f'.{side}.json').read_text())
        assert hashlib.sha256(raw).hexdigest()==meta[f'{side}_body_sha256']
    request=json.loads(pathlib.Path(str(prefix)+'.request-body.json').read_text())
    body=json.loads(pathlib.Path(str(prefix)+'.response-body.json').read_text())
    assert request==x['payload'] and r['prompt']==x['prompt']
    text=body['choices'][0]['message'].get('content') or '' if x['provider']=='openai' else '\n'.join(c['text'] for c in body['content'] if c['type']=='text')
    assert text==r['text']
    assert body['model']==x['model']==r['returned_model']
for p,h in json.loads((ROOT/'precollection_hashes.json').read_text()).items(): assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
lines=['# Exact prompts and responses','', 'This is a mechanical transcript in request order. It contains no substantive analysis. Text inside each response block is reproduced exactly from the convenience extraction; the original response body, including all provider fields, is retained in `raw/`. The surrounding labels are documentation rather than part of the response. Each request is a separate single-turn interaction.','']
for r in responses:
    x=next(x for x in manifest if x['id']==r['id'])
    fence='`'*max(4,max((len(part) for part in __import__('re').findall(r'`+',r['text'])),default=0)+1)
    lines += [f"## Observation {x['order']:02d}",'',f"Provider: {r['provider']}. Requested model: `{r['requested_model']}`. Returned model: `{r['returned_model']}`.",'',f"Prompt: {r['prompt']}",'',f"Response identifier: `{r['response_id']}`. Stop reason: `{r['finish_reason']}`. Output limit reached: {'yes' if r['truncated'] else 'no'}.",'',fence,r['text'],fence,'']
(ROOT/'TRANSCRIPT.md').write_text('\n'.join(lines))
actual=sum(settled.values(),Decimal(0)); pending=sum((v for k,v in reserved.items() if k not in settled),Decimal(0))
summary={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'planned_observations':32,'recorded_responses':len(responses),'attempts':len(reserved),'retries':0,'technical_failures':len(read('failures.jsonl')),'settled_usage_cost_usd':str(actual),'unresolved_reservations_usd':str(pending),'aggregate_exposure_usd':str(actual+pending),'authorized_limit_usd':'2.00','paid_interpretation_calls':0,'all_request_and_response_hashes_match':True,'all_extracted_text_matches_raw':True,'all_models_match_manifest':True,'all_precollection_files_unchanged':True,'all_responses_safety_reviewed':True,'substantive_analysis_started':False}
save('provenance/RAW_CHECKS.json',summary)
(ROOT/'COLLECTION_STATUS.md').write_text(f'''# Collection record before analysis\n\nThe collector preserved {len(responses)} responses from {len(reserved)} attempts against a target of 32. There were {len(read('failures.jsonl'))} technical failures and zero retries. Every recorded response has a direct participation and distress review. No participation objection or apparent distress was found in those reviews. No response was repaired, replaced, or regenerated.\n\nThe charge calculated from reported provider usage is ${actual}. Unresolved reservations total ${pending}. The combined recorded exposure is ${actual+pending}, against the authorized $2 ceiling. There were zero paid interpretation calls. These figures are usage-based estimates, not retrieved invoices.\n\nMechanical verification confirms that request bodies match the precollection manifest, all stored body fingerprints match, extracted text matches the raw response bodies, returned model identifiers match the requested models, and the frozen precollection files remain unchanged. No substantive analysis has started. The raw commit and successful remote verification must be announced before that work begins.\n''')
files={}
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.lock' or p.name=='SHA256SUMS.json': continue
    raw=p.read_bytes()
    for k in ['OPENAI_API_KEY','ANTHROPIC_API_KEY','GH_TOKEN','GITHUB_TOKEN']:
        v=os.getenv(k)
        assert not v or v.encode() not in raw, 'Credential found in archive'
    files[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest()
save('SHA256SUMS.json',files)
print(json.dumps(summary,indent=2))
