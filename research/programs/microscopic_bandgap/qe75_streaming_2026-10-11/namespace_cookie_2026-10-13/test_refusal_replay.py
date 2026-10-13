"""Replay the captured failure without live peers/services or any authority."""
import json
import unittest
from unittest.mock import patch
import sys
import cookie_owner as c


class MeasuredReplay(unittest.TestCase):
    def test_requested_private_network_does_not_admit_host_cookie(self):
        r=json.loads((c.PRIVATE/'normal_result.json').read_text())
        h=r['hello'];self.assertEqual(r['manager_live']['PrivateNetwork'],'yes')
        self.assertEqual(h['cookies'],r['host_fresh_before'])
        self.assertEqual(h['interfaces'],5)
        with patch.object(c,'proc',return_value={'start_ticks':h['start_ticks']}),patch.object(c,'own_cgroup',return_value=h['cgroup']):
            with self.assertRaisesRegex(c.Refusal,'namespace cookie comparison'):
                c.validate_observation(h,r['job'],h['pid'],r['manager_live'],r['kernel_at_hello'])


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MeasuredReplay))
    (c.PRIVATE/'replay_tests.json').write_text(json.dumps({'passed':r.wasSuccessful(),'methods':r.testsRun,
            'kind':'MEASURED_REFUSAL_OFFLINE_REPLAY','service_relaunched':False,'MPI_QE_executed':False},indent=2)+'\n')
    sys.exit(0 if r.wasSuccessful() else 1)
