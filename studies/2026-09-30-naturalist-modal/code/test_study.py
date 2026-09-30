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
  code={k:dict(label='no',span='') for k in ['E','F','H','A']};code['substitution']=False
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

if __name__=='__main__':unittest.main(verbosity=2)
