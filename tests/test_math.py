import importlib.util,json,subprocess,sys,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'scripts/check_math.py'
s=importlib.util.spec_from_file_location('mathcheck',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class MathTests(unittest.TestCase):
 def test_ninety_percent(self):
  r=m.analyze(20,.5,22);self.assertEqual(r['baseline_total'],40);self.assertEqual(r['allowed_stage'],2);self.assertAlmostEqual(r['required_stage_reduction'],.9);self.assertAlmostEqual(r['total_reduction'],.45)
 def test_no_document_conversion(self): self.assertNotIn('whole_population_floor',m.analyze(20,.5,22))
 def test_floor(self):
  r=m.analyze(20,.5,22,.35);self.assertEqual(r['whole_population_floor'],27);self.assertFalse(r['target_feasible_with_coverage'])
 def test_weighted(self): self.assertAlmostEqual(m.weighted_time(20,20,.35,2),28.3)
 def test_impossible(self): self.assertFalse(m.analyze(20,.5,19)['target_feasible_by_stage_alone'])
 def test_coverage_boundaries(self):
  self.assertEqual(m.analyze(20,.5,22,0)['whole_population_floor'],20);self.assertEqual(m.analyze(20,.5,22,1)['whole_population_floor'],40)
 def test_full_stage(self): self.assertEqual(m.analyze(20,1,0)['allowed_stage'],0)
 def test_no_saving(self): self.assertEqual(m.analyze(20,.5,40)['required_stage_reduction'],0)
 def test_slower_target(self): self.assertLess(m.analyze(20,.5,50)['required_stage_reduction'],0)
 def test_invalid(self):
  for a in [(0,.5,22),(20,0,22),(20,1.1,22),(20,.5,-1),(20,.5,22,-.1),(20,.5,22,1.1),(float('nan'),.5,22),(20,float('inf'),22),(True,.5,22)]:
   with self.subTest(a=a),self.assertRaises(ValueError): m.analyze(*a)
 def test_weighted_boundaries(self):
  self.assertEqual(m.weighted_time(20,20,1,2),40);self.assertEqual(m.weighted_time(20,20,0,2),22)
  with self.assertRaises(ValueError): m.weighted_time(20,20,.35,-1)
 def test_transfer_values(self):
  r=m.analyze(12,.4,24);self.assertEqual(r["baseline_total"],30);self.assertEqual(r["unchanged_other"],18);self.assertEqual(r["allowed_stage"],6);self.assertAlmostEqual(r["required_stage_reduction"],.5)
 def test_cli(self):
  r=subprocess.run([sys.executable,str(P),'--stage','20','--share','.5','--target','22'],capture_output=True,text=True);self.assertEqual(r.returncode,0);self.assertEqual(json.loads(r.stdout)['allowed_stage'],2)
 def test_cli_nan(self):
  r=subprocess.run([sys.executable,str(P),'--stage','nan','--share','.5','--target','22'],capture_output=True,text=True);self.assertNotEqual(r.returncode,0)
