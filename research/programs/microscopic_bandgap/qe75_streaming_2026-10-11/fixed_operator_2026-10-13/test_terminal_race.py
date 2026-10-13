"""Two focused offline checks of the observed teardown defect; no new unit/MPI."""
import json,unittest
from pathlib import Path
import owned_pair as o
class TerminalRace(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((o.PRIVATE/'stream/RESULT.json').read_text())
 def test_actual_terminal_and_receipts(self):
  r=self.r
  self.assertTrue(o.completed_native_retirement('stream',r['real_rank_receipts'],r['manager_terminal'],r['invocation'],False))
  self.assertFalse(o.completed_native_retirement('stream',r['real_rank_receipts'],r['manager_terminal'],r['invocation'],True))
  self.assertFalse(o.completed_native_retirement('stream',r['real_rank_receipts'],r['manager_terminal'],'other-invocation',False))
 def test_incomplete_or_wrong_terminal_refused(self):
  r=self.r;h=[v for v in r['real_rank_receipts'] if not (v['action']==6 and v['rank']==1)]
  self.assertFalse(o.completed_native_retirement('stream',h,r['manager_terminal'],r['invocation'],False))
  for fields in [{'Result':'signal'},{'ExecMainStatus':'0'},{'ActiveState':'active'}]:
   self.assertFalse(o.completed_native_retirement('stream',r['real_rank_receipts'],r['manager_terminal']|fields,r['invocation'],False))
if __name__=='__main__':unittest.main()
