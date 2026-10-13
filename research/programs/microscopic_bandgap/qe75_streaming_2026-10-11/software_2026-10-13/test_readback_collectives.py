import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from build_wave import PRIVATE

MEASURED=[]


class ReadbackTest(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory(dir=PRIVATE);self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def unit(self,mode,path,backend='stock'):
        return subprocess.run([str(PRIVATE/'wave'/backend/'initial_unit'),str(path),str(mode)],
                              capture_output=True,text=True,timeout=3)
    def test_48_band_native_encoded_cross_mode_reader(self):
        path=self.root/'state';self.assertEqual(self.unit(0,path).returncode,0)
        for backend in ['stock','stream']:
            r=self.unit(5,path,backend);self.assertEqual(r.returncode,0,r.stderr)
            readback=Path(str(path)+'.readback')
            self.assertEqual(readback.read_bytes(),path.read_bytes())
            readback.unlink() # only this test's newly created private file
    def test_reader_metadata_extent_and_nonfinite_refusals(self):
        path=self.root/'base';self.assertEqual(self.unit(0,path).returncode,0);base=path.read_bytes()
        for name in ['fingerprint','miller','layout','truncated','nan','padding']:
            raw=bytearray(base)
            if name=='fingerprint':raw[120]=ord('b')
            elif name=='miller':struct.pack_into('=q',raw,208+16,999)
            elif name=='layout':struct.pack_into('=q',raw,208,999)
            elif name=='truncated':raw=raw[:-1]
            elif name=='padding':struct.pack_into('=d',raw,208+16+24*30+16*30,19.)
            else:struct.pack_into('=d',raw,len(raw)-8,float('nan'))
            bad=self.root/name;bad.write_bytes(raw)
            r=self.unit(6,bad);self.assertEqual(r.returncode,0,r.stderr);self.assertIn('EXPECTED_READ_REFUSAL',r.stdout)
    def test_unchanged_native_lease_decisions_all_rank_failures(self):
        for rank in [0,1]:
            for scenario in range(5):
                r=subprocess.run([str(PRIVATE/'collectives/collective_unit'),str(scenario),str(rank)],
                                 capture_output=True,text=True,timeout=3)
                MEASURED.append({'rank':rank,'scenario':scenario,'code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
                lines=r.stdout.splitlines()
                if scenario==0:
                    self.assertEqual(r.returncode,0);self.assertEqual(sum('BARRIER' in line for line in lines),2)
                    self.assertEqual(sum('DECISION_STUB_NO_AUTHORITY' in line for line in lines),2)
                else:
                    self.assertEqual(r.returncode,88);self.assertNotIn('SERIAL_DECISION_ACCEPT',r.stdout)
                    self.assertEqual(sum('BARRIER' in line for line in lines),1 if scenario==2 else 0)


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReadbackTest))
    (PRIVATE/'readback_collective_tests.json').write_text(json.dumps({'passed':r.wasSuccessful(),'methods':r.testsRun,
               'serial_decision_traces':MEASURED,'actual_MPI_collective_execution':False,'native_SCf_restart':False},indent=2)+'\n')
    raise SystemExit(0 if r.wasSuccessful() else 1)
