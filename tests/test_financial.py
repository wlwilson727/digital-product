import importlib.util, math, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('financial',Path(__file__).resolve().parents[1]/'financial-models/model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class FinancialModelTests(unittest.TestCase):
 def test_independent_moderate_arithmetic(self):
  r=m.calculate(m.SCENARIOS['moderate'],5000)
  expected=49*.96-49*.029-.30-12-1
  self.assertAlmostEqual(r['contribution_per_order'],expected,places=4)
  self.assertEqual(r['orders'],158)
  self.assertEqual(r['sessions'],7900)
  self.assertGreaterEqual(r['operating_profit'],5000)
  self.assertLess((r['orders']-1)*expected-100,5000)
 def test_unreachable_and_break_even(self):
  r=m.calculate(dict(m.SCENARIOS['moderate'],cac=100),0)
  self.assertIsNone(r['orders']);self.assertIsNone(r['break_even_orders'])
  self.assertEqual(m.calculate(m.SCENARIOS['moderate'],0)['orders'],4)
 def test_scenario_targets(self):
  for s in m.SCENARIOS.values():
   for t in m.TARGETS:
    r=m.calculate(s,t);self.assertGreaterEqual(r['operating_profit'],t)
    self.assertEqual(r['ad_budget'],r['orders']*s['cac'])
 def test_invalid_inputs(self):
  for k,v in [('conversion',0),('conversion',1.1),('price',-1),('fee_rate',-1),('fee_rate',1.1),('refund_rate',1),('cac',float('nan')),('ai',-1),('hosting',float('inf')),('fixed',999)]:
   with self.subTest(k=k,v=v),self.assertRaises(ValueError):m.calculate(dict(m.SCENARIOS['moderate'],**{k:v}),1000)
  for t in [-1,float('nan'),float('inf')]:
   with self.assertRaises(ValueError):m.calculate(m.SCENARIOS['moderate'],t)
if __name__=='__main__':unittest.main()
