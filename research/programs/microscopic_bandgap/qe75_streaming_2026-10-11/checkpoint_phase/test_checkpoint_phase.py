"""Small storage, failure-injection, resource and old-ACE counterexample tests.

All temporary files are inside DFT/.local; no native QE/MPI launch.
"""
import copy
import ctypes
import errno
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import numpy as np
from checkpoint_capsule import Capsule,InjectedFailure,Refusal,REQUIRED,digest_file,encode,sync_dir
from resource_guard import LinuxGuard,admission,live_limits,round_blocks,I64,GIB

PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/checkpoint_phase')
LAYOUT={0:{'R':16,'band_lo':3,'band_hi':7,'Q':4,'spinor':2,'fft':[8,1,1],
           'rank_count':2,'pool_count':1,'exchange_groups':1,'encoding':'complex-DP-native-16'},
        1:{'R':12,'band_lo':3,'band_hi':7,'Q':4,'spinor':2,'fft':[8,1,1],
           'rank_count':2,'pool_count':1,'exchange_groups':1,'encoding':'complex-DP-native-16'}}
PROVENANCE={'qe_commit':'770a0b2d12928a67048e2f3da8d10d057e52179e','source_fingerprint':'test-source-pin',
            'input_operator_fingerprint':'test-HSE-SOC-cutoffs-grid','PP_sha256':['test-Hg','test-Te'],
            'zero_fit':True,'state_generation':'old-density-g1','test_only':True}


def full_info():
    quota={'error':errno.ESRCH,'active':0,'used_bytes':0,'hard_blocks_1024':0,'soft_blocks_1024':0,'valid':0}
    return {'probe_errno':0,'fs_type':0xef53,'block_bytes':4096,'available_blocks':100*GIB//4096,
            'available_bytes':100*GIB,'project_error':0,'project_id':0,'quotas':[copy.deepcopy(quota) for _ in range(3)]}


class PhaseChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=PRIVATE,prefix='unit-')
        self.root=Path(self.temp.name)
        self.cap=Capsule(self.root/'capsule',create=True)
        for rank in LAYOUT:
            for role in REQUIRED:
                self.cap.member(rank,role).write_bytes((f'old-generation {rank} {role}\n'*33).encode())

    def tearDown(self): self.temp.cleanup()

    def test_zero_copy_immutable_ownership(self):
        stamps={self.cap.member(r,s):self.cap.member(r,s).stat() for r in LAYOUT for s in REQUIRED}
        self.cap.publish(LAYOUT,PROVENANCE)
        directory,manifest=self.cap.verify(LAYOUT,PROVENANCE)
        for item in manifest['members']:
            live=self.cap.member(item['rank'],item['role']); snap=directory/item['name']
            self.assertEqual(live.stat().st_ino,snap.stat().st_ino)
            self.assertEqual(live.stat().st_blocks,stamps[live].st_blocks)
            live.unlink() # original store closes/deletes its live path
        self.cap.adopt(LAYOUT,PROVENANCE)
        for item in manifest['members']:
            self.assertEqual(self.cap.member(item['rank'],item['role']).stat().st_ino,(directory/item['name']).stat().st_ino)
        self.cap.consume(LAYOUT,PROVENANCE)
        self.assertFalse((self.cap.root/'CURRENT.json').exists())
        for r in LAYOUT:
            for s in REQUIRED: self.assertFalse(self.cap.member(r,s).exists())

    def test_all_publication_crash_points(self):
        for point in ['after_link','after_data_sync','after_manifest_sync','before_commit','after_commit','after_commit_sync']:
            with self.subTest(point=point):
                cap=Capsule(self.root/point,create=True)
                for r in LAYOUT:
                    for s in REQUIRED: cap.member(r,s).write_bytes(b'old immutable data')
                with self.assertRaises(InjectedFailure): cap.publish(LAYOUT,PROVENANCE,fail_at=point)
                committed=(cap.root/'CURRENT.json').exists()
                self.assertEqual(committed,point in ['after_commit','after_commit_sync'])
                if committed:
                    cap.verify(LAYOUT,PROVENANCE)
                else:
                    with self.assertRaises((Refusal,FileNotFoundError)): cap.verify(LAYOUT,PROVENANCE)
                    directory=next(cap.root.glob('generation-*'))
                    cap.cleanup_orphan(directory.name.removeprefix('generation-'))
                    self.assertFalse(directory.exists())
                    self.assertTrue(all(cap.member(r,s).exists() for r in LAYOUT for s in REQUIRED))

    def test_retirement_crash_is_refusal_not_stale_restore(self):
        self.cap.publish(LAYOUT,PROVENANCE)
        with self.assertRaises(InjectedFailure): self.cap.consume(LAYOUT,PROVENANCE,fail_at='after_retire')
        with self.assertRaises((Refusal,FileNotFoundError)): self.cap.verify(LAYOUT,PROVENANCE)

    def test_incomplete_rank_or_operator_members_refused(self):
        self.cap.member(1,'exx_state').unlink()
        with self.assertRaisesRegex(Refusal,'incomplete'): self.cap.publish(LAYOUT,PROVENANCE)
        self.assertFalse((self.cap.root/'CURRENT.json').exists())

    def test_corruption_and_layout_provenance_refused(self):
        self.cap.publish(LAYOUT,PROVENANCE)
        for name,value in [('layout',LAYOUT),('provenance',PROVENANCE)]:
            altered=copy.deepcopy(value)
            if name=='layout': altered[0]['Q']=5
            else: altered['PP_sha256']=['different-PP']
            with self.assertRaises(Refusal): self.cap.verify(altered if name=='layout' else LAYOUT,altered if name=='provenance' else PROVENANCE)
        directory,manifest=self.cap.verify(LAYOUT,PROVENANCE)
        with (directory/manifest['members'][0]['name']).open('r+b') as f: f.write(b'CORRUPTION')
        with self.assertRaisesRegex(Refusal,'corruption'): self.cap.verify(LAYOUT,PROVENANCE)

    def test_manifest_version_digest_and_native_gate(self):
        self.cap.publish(LAYOUT,PROVENANCE)
        with self.assertRaisesRegex(Refusal,'native QE'): self.cap.verify(LAYOUT,PROVENANCE,require_native=True)
        pointer=self.cap.root/'CURRENT.json'; obj=json.loads(pointer.read_text()); obj['version']='r07-v0'; pointer.write_bytes(encode(obj))
        with self.assertRaisesRegex(Refusal,'version'): self.cap.verify(LAYOUT,PROVENANCE)

    def test_unrelated_cleanup_target_and_current_refused(self):
        self.cap.publish(LAYOUT,PROVENANCE); directory,manifest=self.cap.verify(LAYOUT,PROVENANCE)
        with self.assertRaisesRegex(Refusal,'current'): self.cap.cleanup_orphan(manifest['generation'])
        self.cap.consume(LAYOUT,PROVENANCE)
        foreign=directory/'unrelated.txt'; foreign.write_bytes(b'preserve me')
        with self.assertRaisesRegex(Refusal,'unrelated'): self.cap.cleanup_orphan(manifest['generation'])
        self.assertEqual(foreign.read_bytes(),b'preserve me')

    def test_preexisting_adoption_target_refused(self):
        self.cap.publish(LAYOUT,PROVENANCE); active=self.cap.member(0,'stream'); active.unlink(); active.write_bytes(b'unrelated active file')
        with self.assertRaisesRegex(Refusal,'unrelated'): self.cap.adopt(LAYOUT,PROVENANCE)
        self.assertEqual(active.read_bytes(),b'unrelated active file')

    def test_symlinks_and_second_writer_refused(self):
        source=self.cap.member(0,'stream'); source.unlink(); source.symlink_to(self.cap.member(1,'stream'))
        with self.assertRaisesRegex(Refusal,'symlink'): self.cap.publish(LAYOUT,PROVENANCE)
        with self.cap.locked():
            with self.assertRaisesRegex(Refusal,'another writer'):
                with self.cap.locked(): pass

    def test_signed64_rounding_and_actual_guard_refusal(self):
        self.assertEqual(round_blocks(23622320128,4096),23622320128)
        self.assertEqual(round_blocks(4097,4096),8192)
        with self.assertRaises(Refusal): round_blocks(I64,4096)
        info=full_info()
        self.assertTrue(admission(info,[4097,2048],GIB,20*GIB)['admitted'])
        actual=LinuxGuard(PRIVATE/'storage_guard.so').probe(self.cap.root)
        # A separate read-only Q_GETINFO may establish OFF. EPERM alone cannot.
        if any(q['error'] not in [0,errno.ESRCH] for q in actual['quotas']):
            with self.assertRaisesRegex(Refusal,'UNKNOWN'):
                admission(actual,[4096,4096],GIB,20*GIB)
        else:
            self.assertTrue(admission(actual,[4096,4096],GIB,20*GIB)['admitted'])

    def test_ram_disk_quota_and_bad_telemetry_refusals(self):
        for variant in ['disk','ram','rss','quota','unknown_quota','soft_grace','partial_quota']:
            with self.subTest(variant=variant):
                info=full_info(); mem=20*GIB; rss=0
                if variant=='disk': info['available_blocks']=10*GIB//4096; info['available_bytes']=10*GIB
                elif variant=='ram': mem=15*GIB
                elif variant=='rss': rss=12*GIB+1
                else:
                    q=info['quotas'][0]; q.update(error=0,active=1,valid=3,hard_blocks_1024=1)
                    if variant=='unknown_quota': q['error']=errno.EPERM
                    if variant=='soft_grace': q.update(hard_blocks_1024=100*GIB//1024,soft_blocks_1024=1)
                    if variant=='partial_quota': q['valid']=0
                with self.assertRaises(Refusal): admission(info,[4096],GIB,mem,rss)
        for elapsed in [600,601,float('nan'),-1]:
            with self.assertRaises(Refusal): live_limits(full_info(),20*GIB,0,elapsed)

    def test_real_ext4_reservation_and_tmpfs_refusal(self):
        guard=LinuxGuard(PRIVATE/'storage_guard.so')
        # Isolated 8-KiB syscall test only, not native-policy admission.
        path=self.root/'reserve-unit'; fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL,0o600)
        try:
            allocated=ctypes.c_int64(); code=guard.lib.qe_reserve_fd(fd,4097,ctypes.byref(allocated))
            self.assertEqual(code,0); self.assertGreaterEqual(allocated.value,8192)
            self.assertEqual(os.fstat(fd).st_size,4097)
            self.assertEqual(guard.lib.qe_reserve_fd(fd,4097,ctypes.byref(allocated)),errno.EEXIST)
        finally: os.close(fd)

    def test_per_rank_reservation_and_collision_rollback(self):
        guard=LinuxGuard(PRIVATE/'storage_guard.so')
        cap=Capsule(self.root/'reservation',create=True)
        policy=guard.reserve(cap,[4097,1024],512*1024,20*GIB)
        self.assertEqual(len(policy['rank_files']),2)
        self.assertEqual([x['logical_bytes'] for x in policy['rank_files']],[4097,1024])
        self.assertGreaterEqual(policy['rank_files'][0]['allocated_bytes'],8192)
        other=Capsule(self.root/'collision',create=True)
        second=other.member(1,'stream'); second.write_bytes(b'unrelated pre-existing file')
        with self.assertRaises(FileExistsError): guard.reserve(other,[4096,4096],512*1024,20*GIB)
        self.assertFalse(other.member(0,'stream').exists())
        self.assertEqual(second.read_bytes(),b'unrelated pre-existing file')
        fd=os.memfd_create('r07-tmpfs-refusal')
        try:
            allocated=ctypes.c_int64(); code=guard.lib.qe_reserve_fd(fd,4096,ctypes.byref(allocated))
            self.assertEqual(code,errno.ENODEV); self.assertEqual(os.fstat(fd).st_size,0)
        finally: os.close(fd)

    def test_actual_fortran_open_file_checkpoint_and_restore(self):
        # A sealed, still-open Fortran store is linked; its normal delete-close
        # cannot delete checkpoint data. Then a fresh unit restores that old data.
        cap=Capsule(self.root/'fortran',create=True); layout={0:LAYOUT[0]}
        for role in ['exx_state','native_state']: cap.member(0,role).write_bytes(b'UNIT ONLY opaque complete state placeholder')
        exe=PRIVATE/'ownership_unit'
        writer=subprocess.Popen([str(exe),'write',str(cap.member(0,'stream'))],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            self.assertEqual(writer.stdout.readline().strip(),'SEALED_OLD_GENERATION')
            cap.publish(layout,PROVENANCE)
            out,err=writer.communicate('COMMITTED\n',timeout=15)
            self.assertEqual(writer.returncode,0,(out,err)); self.assertIn('OWNERSHIP_RELEASE_PASS',out)
        finally:
            if writer.poll() is None: writer.kill(); writer.wait()
        directory,manifest=cap.verify(layout,PROVENANCE); self.assertFalse(cap.member(0,'stream').exists())
        cap.adopt(layout,PROVENANCE)
        for mode,code in [('wrong_shape',9),('write_after_restore',9),('read',0)]:
            result=subprocess.run([str(exe),mode,str(cap.member(0,'stream'))],capture_output=True,text=True,timeout=15)
            self.assertEqual(result.returncode,code,result.stdout+result.stderr)
        cap.verify(layout,PROVENANCE) # checkpoint link survives fresh unit's close

    def test_old_ace_cannot_be_rebuilt_from_current_basis(self):
        operator=-np.diag([1.0,2.0]); old=np.array([1.0,0.0]); current=np.array([1.,1.])/np.sqrt(2)
        def ace(phi):
            action=operator@phi
            return -np.outer(action,action)/(-phi@action)
        old_ace=ace(old); replacement=ace(current)
        self.assertLess(np.linalg.norm(old_ace@old-operator@old),1e-15)
        self.assertLess(np.linalg.norm(replacement@current-operator@current),1e-15)
        self.assertGreater(np.linalg.norm(old_ace-replacement),1.0)
        self.assertGreater(np.linalg.norm((old_ace-replacement)@old),0.5)


if __name__=='__main__': unittest.main(verbosity=2)
