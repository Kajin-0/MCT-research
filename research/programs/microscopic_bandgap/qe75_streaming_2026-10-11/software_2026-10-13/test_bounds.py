import itertools
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import numpy as np
from bounds import conservative,good_order,exact_initial_extent,live_inode_budget,admit_native_envelope,Refusal
from common_state import decode
from build_wave import PRIVATE


class BoundTest(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory(dir=PRIVATE);self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_pristine_fft_orders_512_exact_cases(self):
        path=self.root/'fft'
        subprocess.run([str(PRIVATE/'bounds/fft_unit'),str(path)],check=True,timeout=3)
        rows=np.frombuffer(path.read_bytes(),dtype='=i8').reshape((-1,4))
        self.assertEqual(len(rows),512)
        for n,order,factor,padded in rows:
            self.assertEqual(order,good_order(int(n)))
            if n>=2:self.assertEqual(factor,good_order(int(n),2))
            self.assertEqual(padded,n)
    def test_geometry_bounds_and_q_coset_closure(self):
        b=conservative();self.assertEqual(b['global_FFT_order_upper'],{'fock':32,'density':54})
        self.assertLess(b['per_rank_initial_packet_upper_bytes'],b['initial_packet_guard_bytes'])
        grid=set(itertools.product([0,1],repeat=3))
        for k in grid:
            for q in grid:self.assertIn(tuple((ki+qi)%2 for ki,qi in zip(k,q)),grid)
        self.assertEqual(len(grid),b['stored_q_upper'])
        self.assertFalse(b['whole_native_output_envelope_certified'])
    def test_exact_initial_file_size_checked(self):
        path=self.root/'initial'
        subprocess.run([str(PRIVATE/'wave/stock/initial_unit'),str(path),'0'],check=True,timeout=3)
        self.assertEqual(exact_initial_extent(decode(path)['header']),path.stat().st_size)
        bad=decode(path)['header'];bad[3]=2**62
        with self.assertRaises(Refusal):exact_initial_extent(bad)
    def test_workspace_unequal_distribution_counterexample_to_half_volume(self):
        # Same global dimensions and two processors, concentrated sticks:
        # source fft_type_set's alltoall term exceeds V/P. A division by rank
        # count is therefore not a safe local-workspace certificate.
        nx=32;ny=32;nz=32;V=nx*ny*nz
        ncpx=nx*ny;nr3px=nz//2
        nnr=max(ncpx*nz,nx*ny*nr3px,ncpx*nr3px*2)
        self.assertGreater(nnr,V//2);self.assertLessEqual(nnr,2*V)
    def test_live_aliases_generations_and_block_rounding(self):
        r=live_inode_budget({'old':4097,'new':8193},[['old','old'],['old','new'],['new']])
        self.assertEqual(r['per_phase_allocated_payload_blocks'],[8192,20480,12288])
        self.assertFalse(r['metadata_and_unknown_files_included'])
        with self.assertRaises(Refusal):live_inode_budget({'a':16},[['unknown']])
    def test_missing_hdf5_or_native_descriptor_cannot_be_guessed(self):
        with self.assertRaisesRegex(Refusal,'UNKNOWN'):admit_native_envelope(conservative(),{})
        with self.assertRaisesRegex(Refusal,'missing'):admit_native_envelope({'actual_native_MPI_descriptor':'certified'},
                                                                                 {'HDF5_blocks':100})
    def test_hdf5_equal_payload_does_not_fix_allocation_extent(self):
        import h5py
        paths=[self.root/'plain.h5',self.root/'metadata.h5']
        values=np.arange(48,dtype=np.float64)
        for i,path in enumerate(paths):
            with h5py.File(path,'w') as f:
                f.create_dataset('wave',data=values)
                if i:f.attrs['independent_metadata']='x'*16384
        with h5py.File(paths[0],'r') as a,h5py.File(paths[1],'r') as b:
            np.testing.assert_array_equal(a['wave'][:],b['wave'][:])
        self.assertGreater(paths[1].stat().st_blocks,paths[0].stat().st_blocks)


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(BoundTest))
    (PRIVATE/'bounds_tests.json').write_text(json.dumps({'passed':r.wasSuccessful(),'methods':r.testsRun,
        'conservative_components':conservative(),'native_MPI_QE_run':False},indent=2)+'\n')
    raise SystemExit(0 if r.wasSuccessful() else 1)
