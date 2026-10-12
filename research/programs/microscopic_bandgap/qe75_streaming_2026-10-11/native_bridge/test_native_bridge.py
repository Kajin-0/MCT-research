"""Serial codec + explicitly SYNTHETIC native save transaction tests. No PW/MPI."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import struct
import subprocess
import tempfile
import unittest

from native_bundle import NativeBundle,Refusal,InjectedFailure,packet_header,encode

DFT=Path('/home/User/opencode_workspace/DFT')
PRIVATE=DFT/'.local/qe75_lowram_20261011/native_bridge'
LIB=PRIVATE.parent/'checkpoint_phase/storage_guard.so'


def invoke(executable,action,path,fingerprint,rank=0,mode=1):
    result=subprocess.run([str(executable),action,str(path),fingerprint,str(rank),str(mode)],
                          capture_output=True,text=True,timeout=10)
    if 'array temporary' in result.stderr.lower(): raise AssertionError(result.stderr)
    return result


class NativeBridgeTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=PRIVATE,prefix='test-')
        self.base=Path(self.temp.name)
        self.exe=PRIVATE/'unit-O0/state_unit'

    def tearDown(self): self.temp.cleanup()

    def profile(self):
        return {'prefix':'synthetic','ranks':2,'nks':2,'guard_library':str(LIB),
                'native_qualified':False,'runtime_authorized':False,
                'pseudopotentials':{'mock.UPF':hashlib.sha256(b'SYNTHETIC_PP').hexdigest()},
                'provenance':{'kind':'EXPLICIT_SYNTHETIC_NATIVE_STAND_INS','source':'QE7.5 codec unit'}}

    def fixture(self,mode=1):
        bundle=NativeBundle.create(self.base/'owned',self.profile())
        fingerprint=hashlib.sha256(encode(bundle.profile)).hexdigest()
        save=bundle.out/'synthetic.save';save.mkdir()
        (save/'mock.UPF').write_bytes(b'SYNTHETIC_PP')
        for name in ['data-file-schema.xml','charge-density.hdf5','wfc1.hdf5','wfc2.hdf5','ace1.hdf5','ace2.hdf5']:
            (save/name).write_bytes(('SYNTHETIC_STAND_IN:'+name).encode())
        for rank in range(2):
            state=bundle.out/f'synthetic.exx_state.{rank}'
            result=invoke(self.exe,'write',state,fingerprint,rank,mode)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            (bundle.out/f'synthetic.exx_qstream.{rank}').write_bytes(bytes(range(96))*2)
            if mode==1:
                suffix='' if rank==0 else str(rank+1)
                (bundle.out/f'synthetic.restart_scf{suffix}').write_text('5 1e-8 1e-10\n-1 -2 -3 -4\n')
                (bundle.out/f'synthetic.mix{rank+1}').write_bytes(b'SYNTHETIC_MIX_HISTORY')
        return bundle,fingerprint

    def test_exact_roundtrip_both_stops_optimizations(self):
        for optimization in ['O0','O2']:
            executable=PRIVATE/('unit-'+optimization)/'state_unit'
            for mode in [1,2]:
                path=self.base/f'{optimization}-{mode}.state'
                for action in ['write','read']:
                    result=invoke(executable,action,path,'a'*64,mode=mode)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertEqual(packet_header(path)['mode'],mode)
                # Independent Python interpretation of the actual Fortran bytes.
                raw=path.read_bytes();offset=16+72+64+20*8+16+72
                self.assertEqual(struct.unpack('=4d',raw[offset:offset+32]),(1.,0.,.8,.2))
                offset+=32
                self.assertEqual(struct.unpack('=8d',raw[offset:offset+64]),(.45,.05,-4.,-3.,.3,.2,-2.,1.))
                offset+=64
                actual=[complex(*pair) for pair in struct.iter_unpack('=2d',raw[offset:])]
                expected=[z for k in [1,2] for j in [1,2] for z in [complex(j,k),complex(-j,k),complex(j,-k)]]
                self.assertEqual(actual,expected)
            result=invoke(executable,'extent64',self.base/'unused','a'*64)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_codec_refusals(self):
        path=self.base/'packet'
        self.assertEqual(invoke(self.exe,'write',path,'a'*64).returncode,0)
        raw=path.read_bytes()
        for action,fingerprint,needle in [('read','b'*64,'fingerprint refused'),
                                          ('wrong_layout','a'*64,'layout refused')]:
            result=invoke(self.exe,action,path,fingerprint)
            self.assertEqual(result.returncode,9,result.stdout+result.stderr)
            self.assertIn(needle,result.stdout)
        for label,data,needle in [
            ('truncated',raw[:-1],'truncated/extended'),
            ('extended',raw+b'x','truncated/extended'),
            ('version',raw[:16]+struct.pack('=q',1)+raw[24:],'version/encoding'),
            ('byteorder',raw[:24]+bytes(8)+raw[32:],'version/encoding')]:
            path.write_bytes(data)
            result=invoke(self.exe,'read',path,'a'*64)
            self.assertEqual(result.returncode,9,label+result.stdout+result.stderr)
            self.assertIn(needle,result.stdout)
        path.unlink()
        self.assertEqual(invoke(self.exe,'write',path,'a'*64,mode=3).returncode,9)
        self.assertFalse(path.exists())

    def test_actual_stock_zero_counter_requires_packet_tolerance(self):
        result=subprocess.run([str(PRIVATE/'zero-counter/zero_counter_unit'),str(self.base)],
                              capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('STOCK_ZERO_COUNTER_IGNORES_SAVED_ETHR_ET',result.stdout)
        self.assertIn('PACKET_SEEDED_ZERO_COUNTER_PASS',result.stdout)

    def test_no_copy_all_native_members(self):
        bundle,fingerprint=self.fixture()
        bundle.publish()
        directory,manifest=bundle.verify()
        self.assertFalse(manifest['native_qualified'])
        for item in manifest['members']:
            a=(bundle.out/item['path']).stat();b=(directory/'tree'/item['path']).stat()
            self.assertEqual((a.st_dev,a.st_ino,a.st_blocks),(b.st_dev,b.st_ino,b.st_blocks))
        receipt=bundle.consume_for_import()
        self.assertFalse((bundle.root/'CURRENT_NATIVE.json').exists())
        self.assertTrue(receipt['consumed_before_QE_read'])
        for rank in range(2):
            result=invoke(self.exe,'read',bundle.out/f'synthetic.exx_state.{rank}',fingerprint,rank)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        for item in manifest['members']:
            self.assertFalse((directory/'tree'/item['path']).exists())
            self.assertTrue((bundle.out/item['path']).exists())
        # Native in-place modifications now cannot mutate an available checkpoint.
        (bundle.out/'synthetic.save/charge-density.hdf5').write_bytes(b'NEW_LIVE_DENSITY')

    def test_failure_injection_publication(self):
        for point in ['member','manifest','before_commit','after_commit','after_sync']:
            with self.subTest(point=point):
                # Each injection has its own positively owned directory.
                oldbase=self.base;self.base=oldbase/point;self.base.mkdir()
                bundle,_=self.fixture()
                with self.assertRaises(InjectedFailure): bundle.publish(point)
                if point in ['after_commit','after_sync']: bundle.verify()
                else:
                    self.assertFalse((bundle.root/'CURRENT_NATIVE.json').exists())
                    generation=next(bundle.root.glob('native-*')).name[7:]
                    bundle.cleanup_orphan(generation)
                    self.assertFalse((bundle.root/('native-'+generation)).exists())
                    self.assertTrue((bundle.out/'synthetic.exx_qstream.0').exists())
                self.base=oldbase

    def test_retirement_failure_has_no_import_receipt(self):
        bundle,_=self.fixture();bundle.publish()
        with self.assertRaises(InjectedFailure): bundle.consume_for_import('retired')
        self.assertFalse((bundle.root/'CURRENT_NATIVE.json').exists())
        self.assertFalse((bundle.root/'IMPORT.json').exists())

    def test_corrupt_current_density_refused(self):
        bundle,_=self.fixture();bundle.publish()
        (bundle.out/'synthetic.save/charge-density.hdf5').write_bytes(b'BROKEN')
        with self.assertRaisesRegex(Refusal,'corruption'): bundle.verify()

    def test_corrupt_packet_payload_refused(self):
        bundle,_=self.fixture();bundle.publish()
        path=bundle.out/'synthetic.exx_state.0'
        with open(path,'r+b') as f:
            f.seek(-1,2);old=f.read(1);f.seek(-1,2);f.write(bytes([old[0]^1]))
        with self.assertRaisesRegex(Refusal,'corruption'): bundle.verify()

    def test_missing_rank_and_cross_rank_epoch_refused(self):
        bundle,fingerprint=self.fixture()
        path=bundle.out/'synthetic.exx_state.1';path.unlink()
        with self.assertRaisesRegex(Refusal,'missing rank'): bundle.publish()
        self.assertEqual(invoke(self.exe,'write',path,fingerprint,1,2).returncode,0)
        with self.assertRaisesRegex(Refusal,'cross-rank'): bundle.publish()

    def test_inner_restart_and_mix_required_outer_not(self):
        bundle,_=self.fixture()
        path=bundle.out/'synthetic.mix1';path.unlink()
        with self.assertRaisesRegex(Refusal,'mixing history'): bundle.publish()
        (bundle.out/'synthetic.restart_scf').write_text('0 0 1e-10\n')
        bundle.publish() # iteration zero is correctly exempt from history

    def test_symlink_refused(self):
        bundle,_=self.fixture()
        path=bundle.out/'synthetic.save/wfc1.hdf5';path.unlink()
        path.symlink_to(bundle.out/'synthetic.save/wfc2.hdf5')
        with self.assertRaises(Refusal): bundle.publish()

    def test_profile_changed_refused(self):
        bundle,_=self.fixture();bundle.publish()
        changed=bundle.profile.copy();changed['provenance']={'physics':'changed'}
        (bundle.root/'PROFILE.json').write_text(json.dumps(changed))
        with self.assertRaises(Refusal): NativeBundle(bundle.root).verify()

    def test_outer_stop_without_inner_files(self):
        bundle,_=self.fixture(2);bundle.publish();bundle.verify()

    def test_outer_stale_history_refused(self):
        bundle,_=self.fixture(2)
        (bundle.out/'synthetic.restart_k').write_text('1 1e-10 2\n')
        with self.assertRaisesRegex(Refusal,'stale inner'): bundle.publish()

    def test_unrelated_orphan_file_refuses_cleanup(self):
        bundle,_=self.fixture()
        with self.assertRaises(InjectedFailure): bundle.publish('member')
        directory=next(bundle.root.glob('native-*'))
        (directory/'foreign.txt').write_text('DO NOT DELETE')
        before=set(directory.rglob('*'))
        with self.assertRaisesRegex(Refusal,'unrelated'): bundle.cleanup_orphan(directory.name[7:])
        self.assertEqual(before,set(directory.rglob('*')))

    def reservation_fixture(self):
        profile=self.profile();profile['output_envelope_bytes']=1048576
        bundle=NativeBundle.create(self.base/'reservation',profile)
        fingerprint=hashlib.sha256(encode(profile)).hexdigest()
        for rank in range(2):
            (bundle.out/f'synthetic.stream_request.{rank}').write_text(fingerprint+'\n192\n')
        return bundle

    def test_native_reservation_fortran_producer(self):
        bundle=self.reservation_fixture();report=bundle.reserve_streams()
        self.assertEqual([item['bytes'] for item in report],[192,192])
        for rank in range(2):
            path=bundle.out/f'synthetic.exx_qstream.{rank}'
            self.assertGreaterEqual(path.stat().st_blocks*512,192)
            result=subprocess.run([str(PRIVATE/'unit-O0/reserved_unit'),str(path)],
                                  capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertNotIn('array temporary',result.stderr.lower())
            self.assertFalse(path.exists())

    def test_native_reservation_collision_rolls_back_only_owned(self):
        bundle=self.reservation_fixture()
        foreign=bundle.out/'synthetic.exx_qstream.1';foreign.write_bytes(b'KEEP_FOREIGN')
        with self.assertRaises(FileExistsError): bundle.reserve_streams()
        self.assertEqual(foreign.read_bytes(),b'KEEP_FOREIGN')
        self.assertFalse((bundle.out/'synthetic.exx_qstream.0').exists())
        self.assertTrue((bundle.out/'synthetic.stream_request.0').exists())

    def test_reservation_overflow_and_22GiB_policy_refused(self):
        bundle=self.reservation_fixture()
        request=bundle.out/'synthetic.stream_request.0'
        fingerprint=request.read_text().splitlines()[0]
        request.write_text(fingerprint+'\n9223372036854775808\n')
        with self.assertRaisesRegex(Refusal,'64-bit'): bundle.reserve_streams()
        # Use a mathematically synthetic 30-GiB filesystem for a deterministic
        # policy test; do NOT create a 22-GiB file or depend on live free space.
        from resource_guard import admission
        info={'fs_type':0xef53,'block_bytes':4096,'available_blocks':30*(1<<30)//4096,
              'available_bytes':30*(1<<30),'project_error':0,'quotas':[
                  {'error':3,'active':0}]*3}
        with self.assertRaisesRegex(Refusal,'disk reserve'):
            admission(info,[22*(1<<30)],1048576,30*(1<<30))

    def test_native_runtime_fails_closed(self):
        bundle,fingerprint=self.fixture()
        env=dict(os.environ,QE75_BRIDGE_ROOT=str(bundle.root),QE75_BRIDGE_FINGERPRINT=fingerprint)
        result=subprocess.run(['/usr/bin/python3',str(Path(__file__).with_name('native_bundle.py')),'pre_import'],
                              env=env,capture_output=True,text=True,timeout=10)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('not qualified',result.stderr)
        self.assertFalse((bundle.root/'CURRENT_NATIVE.json').exists())

    def test_boolean_cannot_promote_synthetic_profile(self):
        profile=self.profile();profile['runtime_authorized']=True
        bundle=NativeBundle.create(self.base/'promoted',profile)
        fingerprint=hashlib.sha256(encode(profile)).hexdigest()
        env=dict(os.environ,QE75_BRIDGE_ROOT=str(bundle.root),QE75_BRIDGE_FINGERPRINT=fingerprint)
        result=subprocess.run(['/usr/bin/python3',str(Path(__file__).with_name('native_bundle.py')),'pre_import'],
                              env=env,capture_output=True,text=True,timeout=10)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('synthetic/unqualified',result.stderr)

    def test_coordinator_lock_refused(self):
        bundle,_=self.fixture()
        with bundle.locked():
            with self.assertRaisesRegex(Refusal,'already owned'): bundle.publish()


if __name__=='__main__': unittest.main(verbosity=2)
