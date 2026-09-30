"""Offline evidence inventory/checksum verification. --build is maintainer-only.
No generation calls, credentials or network are required. Remote ref evidence is
collected separately with authorized read-only git before --build.
"""
import argparse,hashlib,json,os,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'evidence/MANIFEST.json'
SUMS=ROOT/'evidence/SHA256SUMS'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files():return sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='ledger.lock' and p.suffix!='.pyc')
def category(p):
    n=str(p.relative_to(ROOT))
    if n.startswith('raw/calibration/'):return 'synthetic_api_request' if n.endswith('.request.json') else 'synthetic_api_response_envelope'
    if n=='manifest.json' or n=='coding_overlap.json':return 'unexecuted_study_plan'
    if n.startswith('synthetic/'):return 'synthetic_fixtures_or_validation'
    if n.startswith('analysis/'):return 'post_calibration_diagnostics_not_study_outcomes'
    if n.startswith('code/'):return 'code'
    if n.startswith('reviews/'):return 'authorization_or_model_assisted_review'
    return 'research_document_or_provenance'

def verify():
    d=json.loads(MANIFEST.read_text());expected={ROOT/x['path'] for x in d['files']}
    actual=set(files())-{MANIFEST,SUMS}
    assert expected==actual,'Inventory mismatch'
    for x in d['files']:
        p=ROOT/x['path'];assert p.stat().st_size==x['bytes'];assert sha(p)==x['sha256'],x['path']
    summed={}
    for line in SUMS.read_text().splitlines():
        digest,name=line.split('  ',1);p=ROOT/name;assert sha(p)==digest,name;summed[p]=digest
    assert set(summed)==set(files())-{SUMS}
    clearance=json.loads((ROOT/'reviews/CLEARANCE.json').read_text())
    for name,digest in clearance['sha256'].items():assert sha(ROOT/name)==digest,name
    assert (ROOT/'STOP.json').exists()
    print(json.dumps({'inventory_files':len(expected),'checksummed_files_including_manifest':len(summed),'all_hashes_match':True,'frozen_hashes_match':True,'stop_preserved':True}))

def build():
    inventory=[]
    for p in files():
        if p in [MANIFEST,SUMS]:continue
        data=p.read_bytes()
        for k in ['OPENAI_API_KEY','ANTHROPIC_API_KEY','GH_TOKEN','GITHUB_TOKEN']:
            value=os.getenv(k)
            if value and value.encode() in data:raise RuntimeError('Credential value found; abort')
        inventory.append({'path':str(p.relative_to(ROOT)),'bytes':len(data),'sha256':sha(p),'category':category(p)})
    manifest={'scope':'Complete study-folder evidence inventory. All API data are synthetic calibration; main N=0/192.','hash_algorithm':'SHA-256','exclusions':['evidence/MANIFEST.json (self-reference)','evidence/SHA256SUMS (hashes this manifest)','__pycache__/ and *.pyc (runtime cache)','ledger.lock (runtime lock)'],'files':inventory}
    MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n')
    SUMS.write_text(''.join(sha(p)+'  '+str(p.relative_to(ROOT))+'\n' for p in files() if p!=SUMS))
    verify()
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--build',action='store_true');args=a.parse_args()
    build() if args.build else verify()
