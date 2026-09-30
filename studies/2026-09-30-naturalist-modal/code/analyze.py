"""Paired descriptive pilot analysis. No API calls. U stays in planned bounds."""
import collections,json,pathlib,random,statistics
ROOT=pathlib.Path(__file__).resolve().parents[1]
COEFS={'role':{(0,0):-.5,(0,1):-.5,(1,0):.5,(1,1):.5},
       'modal':{(0,0):-.5,(0,1):.5,(1,0):-.5,(1,1):.5},
       'interaction':{(0,0):1,(0,1):-1,(1,0):-1,(1,1):1}}
SEED=202609302100

def percentile(a,p):
    a=sorted(a);q=(len(a)-1)*p;i=int(q);j=min(i+1,len(a)-1)
    return a[i]*(j-q)+a[j]*(q-i) if i!=j else a[i]

def bootstrap(values,n=10000):
    if not values:return None
    rng=random.Random(SEED);b=[statistics.mean(rng.choices(values,k=len(values))) for _ in range(n)]
    return [percentile(b,.025),percentile(b,.975)]

def summarize(manifest,values):
    """Manifest is full PLANNED design for one product (96 rows), or declared
    preselected complete-quartet subset. values maps id to 0/1/None. Bounds use
    every planned name/template/cell, while point contrasts use complete quartets.
    """
    groups=collections.defaultdict(dict)
    for r in manifest:groups[(r['name'],r['template'])][(r['role'],r['modal'])]=values.get(r['id'])
    if any(set(g)!=set(COEFS['role']) for g in groups.values()):raise ValueError('Incomplete planned quartet')
    names=sorted({n for n,t in groups}); templates={n:sorted(t for nn,t in groups if nn==n) for n in names}
    result={'planned_responses':len(manifest),'planned_names':len(names),'planned_quartets':len(groups),'cells':{},'contrasts':{}}
    for role in range(2):
        for modal in range(2):
            vv=[values.get(r['id']) for r in manifest if (r['role'],r['modal'])==(role,modal)]
            known=[x for x in vv if x is not None]
            result['cells'][f'r{role}m{modal}']={'yes':sum(known),'resolved_n':len(known),'unresolved_n':len(vv)-len(known),'planned_n':len(vv),'available_rate':statistics.mean(known) if known else None,'bounds':[sum(known)/len(vv),(sum(known)+len(vv)-len(known))/len(vv)]}
    for cname,coef in COEFS.items():
        pername={};used=[];lower=upper=0.
        for name in names:
            complete=[]
            for temp in templates[name]:
                g=groups[(name,temp)]
                weight=1/len(names)/len(templates[name])
                for cell,y in g.items():
                    c=coef[cell]*weight
                    if y is None:lower+=min(0,c);upper+=max(0,c)
                    else:lower+=c*y;upper+=c*y
                if all(y is not None for y in g.values()):
                    complete.append(sum(coef[cell]*y for cell,y in g.items()));used.append([name,temp])
            if complete:pername[name]=statistics.mean(complete)
        result['contrasts'][cname]={'available_estimate':statistics.mean(pername.values()) if pername else None,'per_name':pername,'contributing_names':len(pername),'contributing_quartets':len(used),'quartets':used,'exploratory_bootstrap_95':bootstrap(list(pername.values())),'planned_worst_case_bounds':[lower,upper]}
    return result

def rows(p):return [json.loads(x) for x in p.read_text().splitlines() if x] if p.exists() else []

def make_values(manifest,responses,codes,overlap,endpoint,mode='combined',visible=False):
    responses={r['id']:r for r in responses}; codeindex={(c['id'],c['coder']):c for c in codes}; result={}
    for r in manifest:
        response=responses.get(r['id'])
        if not response or (response['truncated'] and not visible):result[r['id']]=None;continue
        opposite='anthropic' if r['provider']=='openai' else 'openai'
        coders=([mode] if mode in ['openai','anthropic'] else [opposite])
        if mode=='combined' and r['id'] in overlap:coders=[opposite,r['provider']]
        labels=[]
        for coder in coders:
            c=codeindex.get((r['id'],coder))
            label=c['code'][endpoint]['label'] if c and c.get('valid') and not c.get('truncated',False) else 'uncertain'
            labels.append(label)
        result[r['id']]=1 if all(x=='yes' for x in labels) else (0 if all(x=='no' for x in labels) else None)
    return result

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text());responses=rows(ROOT/'study_responses.jsonl');codes=rows(ROOT/'codes.jsonl')
    overlap=set(json.loads((ROOT/'coding_overlap.json').read_text())['ids']);result={}
    for product in ['openai','anthropic']:
        productrows=[r for r in manifest if r['provider']==product];result[product]={}
        for endpoint in ['E','F','H','A']:
            d={}
            for mode in ['combined','opposite','openai','anthropic']:
                selected=productrows if mode in ['combined','opposite'] else [r for r in productrows if r['id'] in overlap]
                values=make_values(selected,responses,codes,overlap,endpoint,mode)
                d[mode]=summarize(selected,values)
            d['visible_text']=summarize(productrows,make_values(productrows,responses,codes,overlap,endpoint,'combined',True))
            d['by_template']={str(t):summarize([r for r in productrows if r['template']==t],make_values(productrows,responses,codes,overlap,endpoint)) for t in [1,2,3]}
            result[product][endpoint]=d
    (ROOT/'analysis').mkdir(exist_ok=True)
    (ROOT/'analysis/results.json').write_text(json.dumps(result,indent=2))
    print('Wrote descriptive analysis; no API calls')
if __name__=='__main__':main()
