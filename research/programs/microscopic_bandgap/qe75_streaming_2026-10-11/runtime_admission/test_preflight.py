"""Cheap admission falsification. Never starts any native program or MPI."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from fixture_preflight import template,match_deck,physical_text,QE_PIN
from family_runtime import HERE,PRIVATE,Refusal,create_fake_job,verify_job,Family
from native_bundle import NativeBundle,encode
from process_identity import mpi_inventory,proc,pin_descendant


class PreflightTest(unittest.TestCase):
    def test_exact_templates_same_physics(self):
        self.assertEqual(physical_text(template('control')),physical_text(template('stream')))
        for mode in ['control','stream']:
            text=(HERE/(mode+'.in')).read_text()
            self.assertEqual(match_deck(text,mode),hashlib.sha256(text.encode()).hexdigest())

    def test_changed_or_ambiguous_deck_refused(self):
        text=template('control')
        for bad in [text.replace('nbnd = 48','nbnd = 352'),text.replace("input_dft = 'HSE'","input_dft = 'PBE'"),
                    text.replace('nqx1 = 2','nqx1 = 1'),text.replace('conv_thr = 1e-10','conv_thr = 1e-8'),
                    text.replace('nat = 2','nat = 16'),text+'! even harmless extra text is not whitelisted\n',
                    text.replace("prefix = 'r07m4'","prefix = 'r07m4'\n prefix = 'ambiguous'")]:
            with self.assertRaises(Refusal): match_deck(bad,'control')

    def test_allocation_amplification_refused_before_reservation(self):
        with tempfile.TemporaryDirectory(dir=PRIVATE) as tmp:
            root=Path(tmp)/'job';job=create_fake_job(root)
            job['output_envelope_bytes']=22*(1<<30)
            (root/'JOB.json').write_text(json.dumps(job))
            with self.assertRaisesRegex(Refusal,'cannot be enlarged'): verify_job(root)
            self.assertEqual(list((root/'scratch').iterdir()),[])

    def test_stdout_and_unknown_files_charge_envelope(self):
        with tempfile.TemporaryDirectory(dir=PRIVATE) as tmp:
            root=Path(tmp)/'job';create_fake_job(root);family=Family(root)
            try:
                baseline=family.output_bytes()
                path=root/'logs/native.log';path.write_bytes(b'x'*8192)
                self.assertGreaterEqual(family.output_bytes()-baseline,8192)
                (root/'scratch/unregistered.extra').write_bytes(b'x'*4096)
                self.assertGreaterEqual(family.output_bytes()-baseline,12288)
            finally: family.owner_identity.close()

    def test_unreadable_global_inventory_refuses(self):
        row=proc(os.getpid())
        with mock.patch('process_identity.table',return_value={os.getpid():row}), \
             mock.patch('pathlib.Path.read_bytes',return_value=b'not-mpi\0'), \
             mock.patch('pathlib.Path.read_text',side_effect=PermissionError()):
            with self.assertRaisesRegex(Refusal,'unreadable'): mpi_inventory(require_global=True)
            self.assertEqual(mpi_inventory(require_global=False),[]) # fake-only readable namespace

    def test_snapshot_pid_reuse_cannot_establish_owned_lineage(self):
        pid=os.getpid();row=proc(pid);snapshot={pid:dict(row,start_ticks=row['start_ticks']-1)}
        with self.assertRaisesRegex(Refusal,'lineage changed'): pin_descendant(pid,os.getppid(),snapshot)

    def test_forged_native_boolean_and_monitor_never_grant_lease(self):
        with tempfile.TemporaryDirectory(dir=PRIVATE) as tmp:
            profile={'prefix':'mock','ranks':2,'native_qualified':False,'runtime_authorized':True,
                     'provenance':{'kind':'QEF_QE75_NATIVE_FIXTURE','qe_commit':QE_PIN}}
            root=Path(tmp)/'owned';bundle=NativeBundle.create(root,profile)
            (root/'MONITOR.json').write_text(json.dumps({'runtime_authorized':True,'pid':os.getpid(),
                     'monotonic':1e99,'rank_registration':[0,1]}))
            env=dict(os.environ,QE75_BRIDGE_ROOT=str(root),QE75_BRIDGE_FINGERPRINT=hashlib.sha256(encode(profile)).hexdigest())
            result=subprocess.run([sys.executable,str(HERE.parent/'native_bridge/native_bundle.py'),'pre_import'],
                                  capture_output=True,text=True,env=env,timeout=3)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('live native lease unavailable',result.stderr)
            self.assertFalse((root/'CURRENT_NATIVE.json').exists())


if __name__=='__main__': unittest.main(verbosity=2)
