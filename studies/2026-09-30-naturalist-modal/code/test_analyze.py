import unittest
import analyze as a
import study as s
class Tests(unittest.TestCase):
 def setUp(self):self.m=[r for r in s.make_manifest() if r['provider']=='openai']
 def test_known_effects(self):
  for factor in ['role','modal']:
   v={r['id']:r[factor] for r in self.m};out=a.summarize(self.m,v)
   self.assertEqual(out['contrasts'][factor]['available_estimate'],1)
   self.assertAlmostEqual(out['contrasts'][factor]['planned_worst_case_bounds'][0],1)
   self.assertEqual(out['contrasts']['interaction']['available_estimate'],0)
 def test_interaction(self):
  v={r['id']:int(r['role']==r['modal']) for r in self.m};out=a.summarize(self.m,v)
  self.assertEqual(out['contrasts']['interaction']['available_estimate'],2)
 def test_all_unresolved(self):
  o=a.summarize(self.m,{})
  for k,b in [('role',[-1,1]),('modal',[-1,1]),('interaction',[-2,2])]:
   d=o['contrasts'][k];self.assertIsNone(d['available_estimate']);self.assertEqual(d['contributing_quartets'],0)
   for got,want in zip(d['planned_worst_case_bounds'],b):self.assertAlmostEqual(got,want)
 def test_missing_retains_full_denominator(self):
  v={r['id']:0 for r in self.m};r=self.m[0];v[r['id']]=None;o=a.summarize(self.m,v)
  d=o['contrasts']['interaction'];self.assertEqual(d['contributing_quartets'],23);self.assertEqual(d['contributing_names'],8)
  lo,hi=d['planned_worst_case_bounds'];self.assertAlmostEqual(hi-lo,1/24)
  self.assertEqual(o['planned_responses'],96)
 def test_name_weighting(self):
  v={r['id']:int(r['role']) if r['name']==s.NAMES[0] else 0 for r in self.m}
  # This name contributes only one resolved template but still one name weight.
  for r in self.m:
   if r['name']==s.NAMES[0] and r['template']!=1:v[r['id']]=None
  d=a.summarize(self.m,v)['contrasts']['role'];self.assertEqual(d['available_estimate'],1/8)
 def test_truncation_and_disagreement(self):
  r=self.m[0];response=[dict(id=r['id'],truncated=True)]
  codes=[dict(id=r['id'],coder=p,valid=True,code={'E':{'label':'no'}}) for p in ['openai','anthropic']]
  self.assertIsNone(a.make_values([r],response,codes,{r['id']},'E')[r['id']])
  response[0]['truncated']=False;codes[0]['code']['E']['label']='yes'
  self.assertIsNone(a.make_values([r],response,codes,{r['id']},'E')[r['id']])
 def test_planned_quartet_rejection(self):
  with self.assertRaises(ValueError):a.summarize(self.m[:-1],{})
if __name__=='__main__':unittest.main(verbosity=2)
