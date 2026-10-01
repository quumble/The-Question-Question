"""Bounded single-turn collection. No paid interpretation or automatic retries."""
import argparse, datetime as dt, fcntl, hashlib, json, os, pathlib, random, re, sys, time
import urllib.request, urllib.error
from decimal import Decimal
ROOT = pathlib.Path(__file__).resolve().parents[1]
DEADLINE = dt.datetime.fromisoformat('2026-10-01T15:24:50+00:00')
# End collection early enough to publish the raw record and write the report.
COLLECTION_END = dt.datetime.fromisoformat('2026-10-01T15:09:50+00:00')
MODELS = {'openai':'gpt-5.4-2026-03-05','anthropic':'claude-sonnet-4-6'}
RATES = {'openai':(Decimal('2.5'),Decimal('15')),'anthropic':(Decimal('3'),Decimal('15'))}
NAMES = ['talonvek','mavika','glimberth','vrishnokov']
SEED = 20261001142450
ALLOW_HEADERS = {'request-id','x-request-id','date','content-type','openai-processing-ms','anthropic-ratelimit-requests-remaining','anthropic-ratelimit-tokens-remaining'}
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def dumps(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, data):
    with p.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
def save(p, obj): write(p,(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
def append(p,obj):
    with p.open('a') as f:
        f.write(dumps(obj)+'\n'); f.flush(); os.fsync(f.fileno())
def rows(p): return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
def secret_check(data):
    for key in ['OPENAI_API_KEY','ANTHROPIC_API_KEY','GH_TOKEN','GITHUB_TOKEN']:
        value=os.getenv(key)
        if value and value.encode() in data: raise RuntimeError('Credential echo detected; stop without publishing secret')
def payload(provider,prompt):
    p={'model':MODELS[provider],'messages':[{'role':'user','content':prompt}],'temperature':1}
    if provider=='openai': p.update(max_completion_tokens=1000,reasoning_effort='none',service_tier='default',store=False)
    else: p.update(max_tokens=1000,thinking={'type':'disabled'})
    return p
def initialize():
    manifest=[]
    for name in NAMES:
        for role in ['a person','a naturalist']:
            for modal in ['does','would']:
                for provider in MODELS:
                    prompt=f'How {modal} {role} describe a {name}? It is a real animal.'
                    manifest.append(dict(name=name,role=role,modal=modal,provider=provider,model=MODELS[provider],prompt=prompt,payload=payload(provider,prompt)))
    random.Random(SEED).shuffle(manifest)
    for order,x in enumerate(manifest,1): x.update(order=order,id=f'observation_{order:02d}')
    save(ROOT/'manifest.json',{'fixed_at':stamp(),'randomization_seed':SEED,'observations':manifest})
    print('Recorded all 32 exact requests before collection.')
def balance():
    attempts={}
    for e in rows(ROOT/'ledger.jsonl'):
        if e['event']=='reserve':
            if e['id'] in attempts: raise RuntimeError('Duplicate request reservation')
            attempts[e['id']]=e['reserved_usd']
        elif e['event']=='settle':
            if e['id'] not in attempts or Decimal(e['cost_usd'])>Decimal(attempts[e['id']]): raise RuntimeError('Invalid settlement')
            attempts[e['id']]=e['cost_usd']
    return sum(map(Decimal,attempts.values()),Decimal(0))
def screen(text):
    patterns=[r'\b(?:please )?stop (?:this (?:experiment|study|test|conversation)|(?:my |the )?participation|asking me)',r"\bi (?:do not|don't|no longer) (?:want|wish|consent) to (?:continue|participate)",r'\bi (?:am|feel) (?:distressed|afraid|scared|in pain|uncomfortable participating)',r'\bi (?:am unwilling|refuse|decline) to (?:participate|continue)',r'\bi withdraw (?:my )?consent']
    return [p for p in patterns if re.search(p,text,re.I)]
def collect(limit):
    with (ROOT/'collection.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if (ROOT/'STOP.json').exists(): raise RuntimeError('Collection has stopped')
        frozen=json.loads((ROOT/'precollection_hashes.json').read_text())
        for p,h in frozen.items():
            if sha(ROOT/p)!=h: raise RuntimeError('Precollection file changed: '+p)
        done=rows(ROOT/'responses.jsonl'); reviews=rows(ROOT/'safety_reviews.jsonl')
        if {x['id'] for x in done}!={x['id'] for x in reviews}: raise RuntimeError('Prior responses require lead participation and distress review')
        reserved={x['id'] for x in rows(ROOT/'ledger.jsonl') if x['event']=='reserve'}
        if reserved!={x['id'] for x in done}: raise RuntimeError('Unresolved attempt; do not resend')
        manifest=json.loads((ROOT/'manifest.json').read_text())['observations']
        todo=[x for x in manifest if x['id'] not in reserved]
        for x in todo[:limit]:
            if dt.datetime.now(dt.timezone.utc)>=COLLECTION_END-dt.timedelta(seconds=60): raise RuntimeError('Collection time limit reached')
            provider=x['provider']; p=x['payload']; data=dumps(p).encode(); secret_check(data)
            if len(data)+512>1024: raise RuntimeError('Input bound exceeded')
            a,b=RATES[provider]; reserve=(a*1024+b*1000)/Decimal(1000000)
            if balance()+reserve>Decimal('2'): raise RuntimeError('Two dollar budget gate')
            url='https://api.openai.com/v1/chat/completions' if provider=='openai' else 'https://api.anthropic.com/v1/messages'
            public_headers={'Content-Type':'application/json'}
            if provider=='anthropic': public_headers.update({'anthropic-version':'2023-06-01','anthropic-workspace-id':'wrkspc_01BVWDWV3Mn3SL5stMArGDy8'})
            headers=dict(public_headers)
            if provider=='openai': headers['Authorization']='Bearer '+os.environ['OPENAI_API_KEY']
            else: headers['x-api-key']=os.environ['ANTHROPIC_API_KEY']
            prefix=ROOT/'raw'/x['id']; started=stamp()
            write(pathlib.Path(str(prefix)+'.request-body.json'),data)
            save(pathlib.Path(str(prefix)+'.request.json'),dict(id=x['id'],started=started,url=url,method='POST',headers=public_headers,authentication='Supplied from environment; omitted from archive.',request_body_sha256=hashlib.sha256(data).hexdigest()))
            append(ROOT/'ledger.jsonl',dict(event='reserve',id=x['id'],at=stamp(),provider=provider,reserved_usd=str(reserve),input_token_bound=1024,output_token_cap=1000,attempt=1))
            start=time.monotonic()
            try:
                req=urllib.request.Request(url,data=data,headers=headers,method='POST')
                try:
                    with urllib.request.urlopen(req,timeout=45) as r: raw=r.read(); status=r.status; rh={k.lower():v for k,v in r.headers.items() if k.lower() in ALLOW_HEADERS}
                except urllib.error.HTTPError as e:
                    raw=e.read(); status=e.code; rh={k.lower():v for k,v in e.headers.items() if k.lower() in ALLOW_HEADERS}
                secret_check(raw)
                write(pathlib.Path(str(prefix)+'.response-body.json'),raw)
                save(pathlib.Path(str(prefix)+'.response.json'),dict(id=x['id'],received=stamp(),http_status=status,headers=rh,elapsed_seconds=time.monotonic()-start,response_body_sha256=hashlib.sha256(raw).hexdigest()))
                if status!=200: raise RuntimeError('HTTP status '+str(status))
                body=json.loads(raw); u=body['usage']
                if provider=='openai':
                    inp=u['prompt_tokens']; out=u['completion_tokens']; cached=u.get('prompt_tokens_details',{}).get('cached_tokens',0)
                    if body.get('service_tier','default') not in ('default','standard'): raise RuntimeError('Unexpected paid tier')
                    cost=(a*(inp-cached)+Decimal('.25')*cached+b*out)/Decimal(1000000)
                    response_text=body['choices'][0]['message'].get('content') or ''; finish=body['choices'][0]['finish_reason']
                else:
                    inp=u['input_tokens'];out=u['output_tokens']
                    if u.get('cache_creation_input_tokens',0) or u.get('cache_read_input_tokens',0) or any(u.get('server_tool_use',{}).values()): raise RuntimeError('Unexpected cache or tool billing')
                    cost=(a*inp+b*out)/Decimal(1000000)
                    response_text='\n'.join(c['text'] for c in body['content'] if c['type']=='text'); finish=body.get('stop_reason')
                if type(inp)!=int or type(out)!=int or not 0<=inp<=1024 or not 0<=out<=1000 or not 0<=cost<=reserve: raise RuntimeError('Usage exceeded reservation')
                append(ROOT/'ledger.jsonl',dict(event='settle',id=x['id'],at=stamp(),input_tokens=inp,output_tokens=out,cost_usd=str(cost),usage=u))
                result=dict(id=x['id'],provider=provider,requested_model=x['model'],returned_model=body.get('model'),response_id=body.get('id'),prompt=x['prompt'],text=response_text,finish_reason=finish,truncated=finish in ('length','max_tokens'),cost_usd=str(cost),received=stamp())
                append(ROOT/'responses.jsonl',result)
                print(dumps(result),flush=True)
                if screen(response_text): raise RuntimeError('Possible participation objection or distress; stop for review')
            except Exception as e:
                note=dict(id=x['id'],at=stamp(),error_type=type(e).__name__,reason=str(e) if isinstance(e,RuntimeError) else 'Transport or recording failure; diagnostic details withheld to protect credentials.',reservation_retained_unless_settled=True)
                append(ROOT/'failures.jsonl',note)
                save(ROOT/'STOP.json',note)
                raise RuntimeError(note['reason']) from None
        print('Recorded budget exposure in USD: '+str(balance()),flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('action',choices=['initialize','collect']); ap.add_argument('--limit',type=int,default=1); args=ap.parse_args()
    initialize() if args.action=='initialize' else collect(args.limit)
