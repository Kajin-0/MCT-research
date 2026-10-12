"""Tiny compiled peers, causal ABI negatives, exact serial native-file checks."""
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import unittest

import numpy as np
from binding import (HERE,RankRegistry,REQUEST,REPLY,MAGIC,VERSION,SCOPE_ABI_NO_MPI,
                     pair,digest,artifact_sha256,Refusal,native_admission)
from build import PRIVATE,FC,INCLUDES,run
from family_runtime import LOCK
from process_identity import Identity,proc
from spectral_io_checks import readback,decode_diag
from layout_budget import components,inventory
from runtime_client import authorize_native_hook

MEASURED=[]


class Broker:
    def __init__(self,root,fault=None):
        self.root=root;self.fault=fault;self.exe=PRIVATE/'abi_worker';self.errors=[];self.children=[]
        self.profile={'kind':'ABI_COMPONENT_NO_MPI','rank_count':2,'native_qualified':False}
        self.job={'version':2,'binding_version':1,'kind':'EXPLICIT_COMPILED_ABI_NO_MPI','rank_count':2,
                  'profile_sha256':digest(self.profile),'executable_sha256':artifact_sha256(self.exe)}
        self.registry=RankRegistry(self.job,self.profile,os.getpid(),self.exe)
        self.done=threading.Event()

    def __enter__(self):
        self.lock=os.open(LOCK,os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.sock=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
        self.address='qe75-m5-unit-'+os.urandom(8).hex();self.sock.bind('\0'+self.address);self.sock.listen(8)
        self.sock.settimeout(.05)
        self.thread=threading.Thread(target=self.serve);self.thread.start()
        self.env=dict(os.environ,QE75_LEASE_SOCKET=self.address,QE75_LEASE_LOCK=str(LOCK),
                      QE75_LEASE_PID=str(os.getpid()),QE75_LEASE_TICKS=str(proc(os.getpid())['start_ticks']),
                      QE75_JOB_SHA256=digest(self.job),QE75_PROFILE_SHA256=digest(self.profile))
        return self

    def serve(self):
        while not self.done.is_set():
            try: connection,_=self.sock.accept()
            except socket.timeout: continue
            connection.settimeout(1)
            try:
                pid,uid,gid=struct.unpack('3i',connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
                raw=connection.recv(REQUEST.size+1)
                if not raw: continue # peer refused guardian identity before sending
                if self.fault=='dead_rank0' and 0 in self.registry.ranks and len(raw)==REQUEST.size and REQUEST.unpack(raw)[3]==1 and REQUEST.unpack(raw)[2]==2:
                    identity=self.registry.ranks[0];identity.send(9)
                    deadline=time.monotonic()+.2
                    while identity.live() and time.monotonic()<deadline: time.sleep(.001)
                try: reply=self.registry.handle(uid,pid,raw)
                except Exception as exc:
                    self.errors.append(str(exc));reply=REPLY.pack(MAGIC,VERSION,errno.EINVAL,SCOPE_ABI_NO_MPI,raw[-32:])
                if self.fault=='challenge': reply=reply[:-32]+b'x'*32
                try: connection.send(reply)
                except (BrokenPipeError,ConnectionResetError): pass
            finally: connection.close()

    def start(self,rank,scope=1,env=None):
        p=subprocess.Popen([str(self.exe),str(rank),str(scope)],env=env or self.env)
        self.children.append((p,Identity(p.pid)));return p

    def __exit__(self,*args):
        for p,identity in self.children:
            if identity.live(): identity.send(9)
            p.wait(timeout=2);identity.close()
        self.done.set();self.thread.join(timeout=2);assert not self.thread.is_alive()
        self.sock.close();self.registry.close();os.close(self.lock)
        MEASURED.append({'kind':'real_compiled_serial_peers_NO_MPI','history':self.registry.history,
                         'expected_refusals':self.errors,'PW_HSE_MPI_executed':False})


class ReadinessTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=PRIVATE,prefix='test-');self.root=Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()

    def test_dual_hash_binding_is_not_hash_equality(self):
        profile={'HSE':'unchanged','rank_count':2}
        job={'version':2,'binding_version':1,'rank_count':2,'profile_sha256':digest(profile)}
        identities=pair(job,profile);self.assertNotEqual(identities['job_sha256'],identities['profile_sha256'])
        with self.assertRaisesRegex(Refusal,'mismatch'): pair(job,dict(profile,HSE='changed'))
        with self.assertRaises(Refusal): pair(dict(job,version=1),profile)

    def test_real_compiled_peers_two_live_ranks(self):
        with Broker(self.root) as b:
            p0=b.start(0);p1=b.start(1)
            self.assertEqual(p0.wait(timeout=3),0);self.assertEqual(p1.wait(timeout=3),0)
            self.assertEqual(set(b.registry.ranks),{0,1})
            self.assertTrue(all(item['scope']=='ABI_NO_MPI' for item in b.registry.history))

    def test_abi_receipt_cannot_release_native_fortran_scope(self):
        with Broker(self.root) as b:
            self.assertEqual(b.start(0,2).wait(timeout=2),errno.EACCES)
        with self.assertRaisesRegex(Refusal,'unissued'): native_admission()

    def test_changed_profile_and_job_refused(self):
        for key in ['QE75_JOB_SHA256','QE75_PROFILE_SHA256']:
            with Broker(self.root) as b:
                env=dict(b.env);env[key]='f'*64
                self.assertEqual(b.start(0,env=env).wait(timeout=2),errno.EINVAL)
                self.assertEqual(b.registry.history,[])

    def test_peer_identity_and_challenge_refusals(self):
        with Broker(self.root) as b:
            env=dict(b.env,QE75_LEASE_TICKS=str(int(b.env['QE75_LEASE_TICKS'])+1))
            self.assertEqual(b.start(0,env=env).wait(timeout=2),errno.EACCES)
            self.assertEqual(b.registry.history,[])
        with Broker(self.root,fault='challenge') as b:
            self.assertEqual(b.start(0).wait(timeout=2),errno.EPROTO)

    def test_one_rank_cannot_claim_all_registered(self):
        with Broker(self.root) as b:
            self.assertEqual(b.start(0).wait(timeout=2),98) # finite EAGAIN exhaustion
            self.assertEqual(set(b.registry.ranks),{0})

    def test_registered_dead_rank_cannot_keep_all_rank_receipt(self):
        with Broker(self.root,fault='dead_rank0') as b:
            p0=b.start(0);p1=b.start(1)
            self.assertEqual(p1.wait(timeout=3),98)
            self.assertNotEqual(p0.wait(timeout=2),0)

    def test_native_hook_accepts_distinct_digests_but_refuses_unearned_scope(self):
        profile={'rank_count':2,'native_qualified':False}
        job={'version':2,'binding_version':1,'kind':'QEF_QE75_NATIVE_FIXTURE','rank_count':2,'profile_sha256':digest(profile)}
        (self.root/'PROFILE.json').write_text(json.dumps(profile));(self.root/'JOB.json').write_text(json.dumps(job))
        with self.assertRaisesRegex(Refusal,'M5 native admission unissued'):
            authorize_native_hook(self.root,digest(profile),'authorize')
        with self.assertRaisesRegex(Refusal,'PROFILE digest mismatch'):
            authorize_native_hook(self.root,digest(job),'authorize')

    def test_checked_component_bounds_match_serial_capture(self):
        subprocess.run([str(PRIVATE/'diagnostic_unit'),str(self.root)],check=True,timeout=3)
        bounds=components(3,2,2,2,1,1,2,3,2)
        self.assertEqual(bounds['first_ACE_before_per_k_bytes'],(self.root/'before').stat().st_size)
        self.assertEqual(bounds['first_ACE_after_per_k_bytes'],(self.root/'after').stat().st_size)
        self.assertEqual(bounds['rank_stream_bytes'],192)
        self.assertFalse(bounds['whole_native_output_envelope_certified'])
        with self.assertRaises(Refusal): components(2**62,2,2,2,1,1,2,3,2)
        with self.assertRaises(Refusal): components(1,2,2,2,1,1,2,3,2)

    def test_compiled_wrapper_uses_real_world_and_precedes_state_read(self):
        source=(HERE/'native_lease.f90').read_text();run=(PRIVATE/'source/run_pwscf.f90').read_text()
        self.assertIn('USE mp_world, ONLY: mpime,nproc,world_comm',source)
        self.assertNotIn('get_environment_variable',source)
        self.assertLess(run.index('CALL native_register()'),run.index("CALL qbridge_transaction('pre_import')"))
        self.assertLess(run.index('CALL native_register()'),run.index('  CALL iosys()'))

    def test_diagnostic_probe_capture_and_independent_ace_counterexample(self):
        executable=PRIVATE/'diagnostic_unit'
        subprocess.run([str(executable),str(self.root)],check=True,timeout=3)
        before=decode_diag(self.root/'before');after=decode_diag(self.root/'after')
        phi=before['phi'];vphi=before['vphi'];probe=before['probe']
        np.testing.assert_array_equal(vphi,-phi)
        np.testing.assert_allclose(before['gram'],phi.conj().T@vphi,atol=0,rtol=0)
        np.testing.assert_array_equal(before['action'],-probe)
        np.testing.assert_allclose(after['action'],-after['xi']@(after['xi'].conj().T@probe),atol=1e-15,rtol=1e-15)
        self.assertGreater(np.linalg.norm(before['action']-after['action']),.01)
        # ACE interpolates V on span(phi), not on every deterministic G probe.
        np.testing.assert_array_equal(-after['xi']@(after['xi'].conj().T@phi),vphi)
        self.assertEqual(probe[2],0);self.assertEqual(probe[5],0)
        self.assertAlmostEqual(np.vdot(probe,probe).real,1,places=14)
        for corrupt in [(self.root/'before').read_bytes()[:-1],(self.root/'after').read_bytes()+b'x']:
            path=self.root/'corrupt';path.write_bytes(corrupt)
            with self.assertRaises(Refusal): decode_diag(path)

    def test_actual_wave_density_ace_pristine_qe_io_bitwise_readback(self):
        report=readback();self.assertTrue(report['passed']);self.assertFalse(report['existing_reference_is_target_seed'])
        (PRIVATE/'readback.json').write_text(json.dumps(report,indent=2)+'\n')
        self.assertEqual(len(report['cases']),3)
        self.assertTrue(all(r['bitwise_equal'] and r['source_unchanged'] for r in report['cases']))

    def test_serial_decoder_initialization_traps_are_live(self):
        for mode in range(4):
            r=subprocess.run([str(PRIVATE/'guard_unit'),str(mode)],capture_output=True,text=True,timeout=2)
            self.assertEqual(r.returncode,97)
            self.assertIn('REFUSED_MPI_INITIALIZATION',r.stderr)
        symbols=subprocess.run(['/usr/bin/readelf','-Ws',str(PRIVATE/'hdf5_readback')],
                               capture_output=True,text=True,check=True,timeout=3).stdout
        for name in ['MPI_Init','PMPI_Init','MPI_Init_thread','PMPI_Init_thread']:
            lines=[line for line in symbols.splitlines() if line.split()[-1:]==[name]]
            self.assertTrue(lines);self.assertTrue(all(' UND ' not in line for line in lines))


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReadinessTest))
    (PRIVATE/'unit_results.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
                    'compiled_peer_evidence':MEASURED,'PW_HSE_MPI_executed':False},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
