"""Integer counterexamples/checks only. Does not allocate these budgets."""
import json
from pathlib import Path
import unittest
import sys
from resource_bounds import *


class Bounds(unittest.TestCase):
    def test_shared_rss_conditional_address_bound(self):
        self.assertEqual(resident_mapping_upper_bound(32,256<<20,128<<20),(8<<30)+(128<<20))
        with self.assertRaises(MissingBound):monitored_rss_upper_bound(32,256<<20,128<<20)
        self.assertEqual(monitored_rss_upper_bound(32,256<<20,128<<20,4096),(8<<30)+(128<<20)+4096)
    def test_open_fd_limit_is_not_retained_file_limit(self):
        # One sequentially reused fd, every individual file <=32MiB.
        self.assertGreater(aggregate_file_upper_bound(32<<20,129,0),64<<20)
        with self.assertRaises(MissingBound):aggregate_file_upper_bound(32<<20,None,0)
    def test_partial_runtime_sum_refuses(self):
        with self.assertRaisesRegex(MissingBound,'PRRTE_PMIX'):complete_budget(current_local_mpi_terms())
    def test_complete_finite_model_and_checked_units(self):
        self.assertEqual(complete_budget([Term('a',4096,'exact bounded model'),Term('b',8192,'exact bounded model')]),12288)
        for value in [True,-1,1<<63]:
            with self.assertRaises(ValueError):checked(value)
        with self.assertRaises(ValueError):resident_mapping_upper_bound(32,1<<62,0)
    def test_no_evidence_and_duplicate_terms_refuse(self):
        with self.assertRaises(MissingBound):complete_budget([Term('a',4096,'')])
        with self.assertRaises(ValueError):complete_budget([Term('a',1,'x'),Term('a',2,'y')])


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Bounds))
    root=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/namespace_cookie_20261013')
    (root/'resource_tests.json').write_text(json.dumps({'passed':r.wasSuccessful(),'methods':r.testsRun,
          'MPI_QE_executed':False,'real_budget_allocations':False},indent=2)+'\n')
    sys.exit(0 if r.wasSuccessful() else 1)
