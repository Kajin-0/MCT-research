import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from build_transport import PRIVATE
from fft_descriptor import read,compare,Refusal


class DescriptorTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=PRIVATE);self.root=Path(self.temp.name)
        self.profiles={'stock':'a'*64,'stream':'b'*64};self.common='c'*64;self.paths={}
        for mode in ['stock','stream']:
            self.paths[mode]=[]
            for r in [0,1]:
                p=self.root/f'{mode}{r}.fft'
                subprocess.run([str(PRIVATE/'descriptor'/mode/'descriptor_unit'),str(p),str(r),self.profiles[mode],self.common],
                               check=True,capture_output=True,text=True,timeout=3)
                self.paths[mode].append(p)
    def tearDown(self):self.temp.cleanup()
    def test_real_type_codec_corresponding_rank_and_unequal_local_extents(self):
        report=compare(self.paths['stock'],self.paths['stream'],self.profiles,self.common)
        self.assertTrue(report['passed']);self.assertFalse(report['native_admission_issued'])
        self.assertEqual([read(p)['descriptors']['fock']['nnr'] for p in self.paths['stock']],[48,32])
        self.assertIsNone(read(self.paths['stock'][0])['descriptors']['fock']['nlm'])
        self.assertFalse(read(self.paths['stock'][0])['native_authenticated_observation'])
    def test_same_dimensions_different_G_map_refused(self):
        p=self.paths['stream'][0];raw=bytearray(p.read_bytes())
        # Change only the third Fock-map value, keeping counts and volume equal.
        i=raw.rfind(b'nl'+b' '*22)+40
        self.assertGreater(i,40);struct.pack_into('<q',raw,i+16,4);p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal,'corresponding-rank'):compare(self.paths['stock'],self.paths['stream'],self.profiles,self.common)
    def test_missing_duplicate_rank_and_profile_not_boolean(self):
        with self.assertRaises(Refusal):compare(self.paths['stock'][:1],self.paths['stream'],self.profiles,self.common)
        with self.assertRaises(Refusal):compare([self.paths['stock'][0]]*2,self.paths['stream'],self.profiles,self.common)
        with self.assertRaises(Refusal):compare(self.paths['stock'],self.paths['stream'],{'stock':'b'*64,'stream':'b'*64},self.common)
        with self.assertRaises(Refusal):compare(self.paths['stock'],self.paths['stream'],self.profiles,'d'*64)
    def test_truncation_extent_tail_and_negative_shape_refused(self):
        p=self.root/'bad';raw=self.paths['stock'][0].read_bytes()
        for bad in [raw[:-1],raw+b'extra',raw[:35]]:
            p.write_bytes(bad)
            with self.assertRaises(Refusal):read(p)
        bad=bytearray(raw);i=bad.find(b'nr1p'+b' '*20)+24
        struct.pack_into('<q',bad,i,-2);p.write_bytes(bad)
        with self.assertRaisesRegex(Refusal,'shape'):read(p)
    def test_inconsistent_partition_and_local_owner_refused(self):
        raw=bytearray(self.paths['stock'][0].read_bytes())
        label=raw.find(b'nr3p'+b' '*20);struct.pack_into('<q',raw,label+40,4)
        p=self.root/'bad';p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal,'partition cover'):read(p)
    def test_invalid_leading_dimension_and_duplicate_G_map_refused(self):
        original=self.paths['stock'][0].read_bytes();p=self.root/'bad'
        raw=bytearray(original)
        # Fixed header + scope + descriptor label; nr1x is scalar index 3.
        struct.pack_into('<q',raw,8+32+128+12*8+16+3*8,3);p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal,'leading dimension'):read(p)
        raw=bytearray(original);i=raw.find(b'nl'+b' '*22)+40
        struct.pack_into('<q',raw,i+8,1);p.write_bytes(raw)
        with self.assertRaisesRegex(Refusal,'G map'):read(p)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DescriptorTest))
    (PRIVATE/'descriptor_tests.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
        'scope':'standalone serial codec using real QE derived type; synthetic arrays; no MPI authority',
        'actual_native_MPI_descriptor_observed':False,'native_PW_MPI_run':False},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
