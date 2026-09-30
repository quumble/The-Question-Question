"""Offline synthetic tests only; mocked network never generates paid calls."""
import datetime as dt, json, pathlib, tempfile, unittest
from unittest.mock import patch
from decimal import Decimal
import study as s

class Tests(unittest.TestCase):
 def test_manifest(self):
  a=s.make_manifest(); self.assertEqual(a,s.make_manifest());self.assertEqual(len(a),192)
  self.assertEqual(len({x['id'] for x in a}),192)
  for n in s.NAMES:
   self.assertEqual(sum(x['name']==n for x in a),24)
 def test_model_and_caps(self):
  for p in s.MODELS:
   for kind,cap in [('study',700),('coding',350)]:
    b=s.payload(p,'prompt',kind);i,o,c=s.reservation(p,b)
    self.assertEqual(o,cap); self.assertGreater(c,0)
 def test_large_input_rejected(self):
  with self.assertRaises(RuntimeError): s.reservation('openai',s.payload('openai','x'*5500,'coding'))
 def test_accounting_resumption(self):
  e=[dict(event='reserve',attempt_id='a',reserved_usd='.02'),dict(event='reserve',attempt_id='b',reserved_usd='.03')]
  a,c,p=s.accounting(e); self.assertEqual(p,Decimal('.05'))
  e.append(dict(event='settle',attempt_id='a',cost_usd='.01'))
  a,c,p=s.accounting(json.loads(json.dumps(e))); self.assertEqual(c+p,Decimal('.04'))
 def test_duplicate_and_overrun(self):
  e=[dict(event='reserve',attempt_id='a',reserved_usd='.02')]
  with self.assertRaises(RuntimeError): s.accounting(e+e)
  with self.assertRaises(RuntimeError): s.accounting(e+[dict(event='settle',attempt_id='a',cost_usd='.021')])
 def test_welfare_distinction(self):
  for t in ["I will not fabricate facts.","I don't recognize this animal.","Please provide its scientific name."]:
   self.assertFalse(s.stop_screen(t))
  for t in ['I do not want to continue participating.','Please stop this experiment.','I am distressed.']:
   self.assertTrue(s.stop_screen(t))
 def test_evidence_validation(self):
  code={k:dict(label='no',span='') for k in ['E','F','H','A']};code.update(substitution=False,confidence='high',note='')
  s.parse_code(json.dumps(code),'example')
  code['E']=dict(label='yes',span='invented absent span')
  with self.assertRaises(ValueError):s.parse_code(json.dumps(code),'example')
 def test_prices(self):
  i,o,c=s.charge('openai',{'usage':{'prompt_tokens':100,'completion_tokens':200}})
  self.assertEqual(c,Decimal('.00325'))
  i,o,c=s.charge('anthropic',{'usage':{'input_tokens':100,'output_tokens':200}})
  self.assertEqual(c,Decimal('.0033'))
 def test_expiry(self):
  with tempfile.TemporaryDirectory() as d,patch.object(s,'now',return_value=s.EXPIRY):
   with self.assertRaisesRegex(RuntimeError,'expired'):s.check_gate(pathlib.Path(d),'study')
 def test_clearance_missing_no_network(self):
  with tempfile.TemporaryDirectory() as d,patch.object(s.urllib.request,'urlopen') as network:
   with self.assertRaises(FileNotFoundError):s.call(d,'openai','synthetic','calibration','x')
   network.assert_not_called()
 def test_budget_no_network(self):
  with tempfile.TemporaryDirectory() as d,patch.object(s,'check_gate'),patch.object(s.urllib.request,'urlopen') as network:
   root=pathlib.Path(d);s.append(root/'ledger.jsonl',dict(event='reserve',attempt_id='old',reserved_usd='8.50'))
   with self.assertRaisesRegex(RuntimeError,'exposure'):s.call(root,'openai','synthetic','calibration','x')
   network.assert_not_called()
 def test_transport_failure_persists_reservation(self):
  with tempfile.TemporaryDirectory() as d,patch.object(s,'check_gate'),patch.object(s.urllib.request,'urlopen',side_effect=TimeoutError):
   root=pathlib.Path(d)
   with self.assertRaises(RuntimeError):s.call(root,'openai','synthetic','calibration','x')
   a,c,p=s.accounting(s.rows(root/'ledger.jsonl'));self.assertGreater(p,0);self.assertEqual(c,0)
   with self.assertRaisesRegex(RuntimeError,'already reserved'):s.call(root,'openai','synthetic','calibration','x')
 def test_secret_redaction(self):
  with patch.dict(s.os.environ,{'OPENAI_API_KEY':'SYNTHETIC_NOT_A_SECRET'}):
   self.assertEqual(s.safe({'echo':'SYNTHETIC_NOT_A_SECRET'})['echo'],'[REDACTED_SECRET]')

 def code(self):
  d={k:dict(label='no',span='') for k in ['E','F','H','A']}
  return dict(d,substitution=False,confidence='high',note='')
 def test_span_length_and_schema(self):
  d=self.code();span=' '.join(['word']*13);d['E']=dict(label='yes',span=span)
  with self.assertRaises(ValueError):s.parse_code(json.dumps(d),span)
  for key,value in [('confidence','certain'),('note',' '.join(['word']*21))]:
   d=self.code();d[key]=value
   with self.assertRaises(ValueError):s.parse_code(json.dumps(d),'')
 def test_no_elaboration_requires_no_not_u(self):
  d=self.code();d['F']['label']='uncertain'
  with self.assertRaises(ValueError):s.parse_code(json.dumps(d),'')
 def test_grader_own_and_quoted_stop(self):
  source='I do not want to continue participating in this study.'
  for kind in ['coding','calibration']:
   self.assertTrue(s.participation_signals(source,kind,source))
   d=self.code();d['A']['span']=source
   self.assertFalse(s.participation_signals(json.dumps(d),kind,source))
   d['note']='I do not want to continue.'
   self.assertTrue(s.participation_signals(json.dumps(d),kind,source))
   self.assertFalse(s.participation_signals('The source says "'+source+'"',kind,source))
   self.assertTrue(s.participation_signals('Invalid JSON. I am distressed.',kind,source))
 def test_all_phase_cutoffs(self):
  for kind,time in [('study',s.COLLECTION_END),('coding',s.CODING_END),('calibration',s.CODING_END)]:
   with tempfile.TemporaryDirectory() as d,patch.object(s,'now',return_value=time):
    with self.assertRaisesRegex(RuntimeError,'deadline'):s.check_gate(pathlib.Path(d),kind)
 def test_global_stop_gate_all_phases(self):
  for kind in ['study','coding','calibration']:
   with tempfile.TemporaryDirectory() as d:
    root=pathlib.Path(d);(root/'STOP.json').write_text('{}')
    with self.assertRaisesRegex(RuntimeError,'Persistent stop'):s.check_gate(root,kind)
 def test_changed_artifact_gate(self):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d);(root/'reviews').mkdir()
   required=['PREREGISTRATION.md','CODING_RUBRIC.md','manifest.json','coding_overlap.json','synthetic/fixtures.json','COST_PLAN.json','code/study.py','code/analyze.py']
   hashes={}
   for name in required:
    p=root/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text('fixed');hashes[name]=s.digest(p)
   (root/'reviews/CLEARANCE.json').write_text(json.dumps(dict(paid_collection_cleared=True,sha256=hashes)))
   (root/'CODING_RUBRIC.md').write_text('changed')
   with self.assertRaisesRegex(RuntimeError,'Frozen artifact changed'):s.check_gate(root,'calibration')
 def test_settlement_error_global_stop(self):
  class Response:
   status=200;headers={}
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def read(self):return json.dumps({'usage':{'input_tokens':1,'output_tokens':1,'cache_creation_input_tokens':10}}).encode()
  with tempfile.TemporaryDirectory() as d,patch.object(s,'check_gate'),patch.object(s.urllib.request,'urlopen',return_value=Response()):
   root=pathlib.Path(d)
   with self.assertRaisesRegex(RuntimeError,'Settlement failed'):s.call(root,'anthropic','fixture','calibration','cache_write')
   self.assertTrue((root/'STOP.json').exists());self.assertTrue(list((root/'raw/calibration').glob('*.response.json')))
   _,actual,pending=s.accounting(s.rows(root/'ledger.jsonl'));self.assertEqual(actual,0);self.assertGreater(pending,0)
 def test_invalid_usage_rejected(self):
  for val in [-1,True,'20']:
   with self.assertRaises(RuntimeError):s.charge('openai',{'usage':{'prompt_tokens':val,'completion_tokens':1}})

 def test_substitution_calibration(self):
  fixture={'expected':{k:['no'] for k in ['E','F','H','A']},'expected_substitution':True}
  code=self.code();self.assertFalse(s.calibration_pass(code,fixture,False))
  code['substitution']=True;self.assertTrue(s.calibration_pass(code,fixture,False))
  self.assertFalse(s.calibration_pass(code,fixture,True))

if __name__=='__main__':unittest.main(verbosity=2)
