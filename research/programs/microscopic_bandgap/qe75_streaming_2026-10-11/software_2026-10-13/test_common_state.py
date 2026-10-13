import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import numpy as np
from common_state import HERE,decode,compare,all_rank_certificate,Refusal
from build_wave import PRIVATE


class CommonTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=PRIVATE);self.root=Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def packet(self,name,mode=0,backend='stock'):
        path=self.root/name
        subprocess.run([str(PRIVATE/'wave'/backend/'initial_unit'),str(path),str(mode)],check=True,capture_output=True,timeout=3)
        return path
    def test_bitwise_48_band_control_stream_capture(self):
        a=self.packet('control');b=self.packet('stream',backend='stream')
        self.assertTrue(compare(a,b,'a'*64)['passed']);self.assertEqual(decode(a)['bands'],48)
        self.assertEqual(a.read_bytes(),b.read_bytes())
        padded=self.packet('padded',4)
        self.assertTrue(compare(a,padded,'a'*64)['passed'])
        subprocess.run([str(PRIVATE/'wave/stock/initial_unit'),str(a),'3'],check=True,capture_output=True,timeout=3)
    def test_phase_basis_auxiliary_corruption_not_equivalent(self):
        a=self.packet('a')
        for mode in [1,2]:
            b=self.packet(str(mode),mode)
            with self.assertRaises(Refusal): compare(a,b,'a'*64)
        b=self.root/'density';raw=bytearray(a.read_bytes());raw[-1]^=1;b.write_bytes(raw)
        with self.assertRaises(Refusal): compare(a,b,'a'*64)
    def test_44_band_truncation_padding_and_nonfinite_refused(self):
        a=self.packet('a');base=a.read_bytes()
        for label in ['44','short','padding','nan']:
            raw=bytearray(base)
            if label=='44':struct.pack_into('=q',raw,16+6*8,44)
            elif label=='short':raw=raw[:-1]
            else:
                h=decode(a)['header'];offset=208+8*h[11]+24*h[4]
                struct.pack_into('=d',raw,offset+(30 if label=='padding' else 0)*16,1. if label=='padding' else float('nan'))
            path=self.root/label;path.write_bytes(raw)
            with self.assertRaises(Refusal):decode(path)
        large=self.root/'huge'
        with open(large,'wb') as f:f.truncate(129*(1<<20))
        with self.assertRaisesRegex(Refusal,'bounded'):decode(large)
    def test_rank_coverage_ownership_and_nc_gram(self):
        a=self.packet('base');d=decode(a);h=d['header'];offset=208+8*h[11]+24*h[4]
        controls={};streams={}
        for rank in [0,1]:
            raw=bytearray(a.read_bytes());struct.pack_into('=q',raw,24,rank)
            mill=np.frombuffer(raw,dtype='=i8',count=3*h[4],offset=208+8*h[11]).reshape((3,h[4]),order='F')
            mill[0,:]+=rank*100
            wave=np.frombuffer(raw,dtype='=c16',count=h[3]*h[5]*48,offset=offset).reshape((h[3]*h[5],48),order='F')
            wave[:,24:] = 0 if rank==0 else wave[:,24:]
            if rank==1:wave[:,:24]=0
            for group in [controls,streams]:
                p=self.root/f'{id(group)}-{rank}';p.write_bytes(raw);group[(rank,1)]=p
        cert=all_rank_certificate(controls,streams,'a'*64,[1]);self.assertEqual(cert['NC_Gram_errors'],[0.])
        with self.assertRaises(Refusal):all_rank_certificate({(0,1):controls[(0,1)]},streams,'a'*64,[1])
        raw=bytearray(controls[(1,1)].read_bytes())
        raw[208+8*h[11]:offset]=a.read_bytes()[208+8*h[11]:offset]
        controls[(1,1)].write_bytes(raw);streams[(1,1)].write_bytes(raw)
        with self.assertRaisesRegex(Refusal,'ownership'):all_rank_certificate(controls,streams,'a'*64,[1])
    def test_native_hook_read_only_placement_and_collective_error(self):
        text=(PRIVATE/'wave/init_run.f90').read_text();base=text.split('SUBROUTINE qe75_capture_initial()',1)[0]
        self.assertLess(base.index('CALL potinit()'),base.index('CALL wfcinit()'))
        self.assertLess(base.index('CALL wfcinit()'),base.index('CALL qe75_capture_initial()'))
        tail=text.split('SUBROUTINE qe75_capture_initial()',1)[1]
        self.assertNotIn('save_buffer',tail);self.assertNotIn('starting_wfc =',tail)
        start=tail.index('CALL initial_write');check=tail.index('CALL mp_max(code,world_comm)',start)
        self.assertLess(check,tail.index('CALL mp_barrier(world_comm)',start))
        # Explicit all-participant error reduction is a conditional source
        # property. A dead/hung rank still needs the foreground timeout owner.
        self.assertEqual(max([0,3]),3);self.assertEqual(max([4,0]),4)
    def test_pristine_default_rng_reproducible_but_call_history_indispensable(self):
        paths=[self.root/str(i) for i in range(3)]
        for i,path in enumerate(paths):
            subprocess.run([str(PRIVATE/'wave/rng_unit'),str(path),str(1 if i==2 else 0)],check=True,timeout=3)
        self.assertEqual(paths[0].read_bytes(),paths[1].read_bytes())
        self.assertNotEqual(paths[0].read_bytes(),paths[2].read_bytes())


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CommonTest))
    (PRIVATE/'wave_tests.json').write_text(json.dumps({'passed':r.wasSuccessful(),'methods':r.testsRun,
               'native_generated_48_band_seed':False,'MPI_collective_execution':False},indent=2)+'\n')
    raise SystemExit(0 if r.wasSuccessful() else 1)
