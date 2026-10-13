"""Serial native wire tests only: threads/AF_UNIX, never MPI_Init or MPI jobs."""
import ctypes
import errno
import fcntl
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import sys
import threading
import unittest
import uuid

HERE=Path(__file__).resolve().parent
PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/local_owned_mpi_20261013')
REQUEST=struct.Struct('!4sIIII64s64s32s');REPLY=struct.Struct('!4sIII32s')
sys.path.insert(0,str(HERE))
import isolation_probe as probe


class SerialComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib=ctypes.CDLL(str(PRIVATE/'collective_lease.v2.so'))
        cls.call=cls.lib.r07_collective_lease_call
        cls.call.argtypes=[ctypes.c_int]*3;cls.call.restype=ctypes.c_int
        cls.root=PRIVATE/('serial-'+uuid.uuid4().hex);cls.root.mkdir(mode=0o700)
        cls.lock=os.open(cls.root/'serial.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600)
        fcntl.flock(cls.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        ticks=Path('/proc/self/stat').read_text().rsplit(')',1)[1].split()[19]
        cls.old_env={k:os.environ.get(k) for k in ['QE75_LEASE_PID','QE75_LEASE_TICKS','QE75_LEASE_LOCK',
                      'QE75_JOB_SHA256','QE75_PROFILE_SHA256','QE75_LEASE_SOCKET']}
        os.environ.update(QE75_LEASE_PID=str(os.getpid()),QE75_LEASE_TICKS=ticks,
                          QE75_LEASE_LOCK=str(cls.root/'serial.lock'),QE75_JOB_SHA256='a'*64,QE75_PROFILE_SHA256='b'*64)

    @classmethod
    def tearDownClass(cls):
        os.close(cls.lock)
        for k,v in cls.old_env.items():
            if v is None:os.environ.pop(k,None)
            else:os.environ[k]=v

    def exchange(self,magic=b'R07C',scope=3,status=0,challenge_ok=True,job_good=True,preinit=False):
        address='r07-serial-'+uuid.uuid4().hex
        server=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);server.bind('\0'+address);server.listen(1)
        server.settimeout(2);os.environ['QE75_LEASE_SOCKET']=address
        requests=[];errors=[]
        def reply():
            try:
                c,_=server.accept();c.settimeout(2)
                with c:
                    raw=c.recv(181);r=REQUEST.unpack(raw);requests.append(r)
                    c.send(REPLY.pack(magic,1,status,scope,r[-1] if challenge_ok else bytes(32)))
            except BaseException as exc:errors.append(repr(exc))
        if not job_good:os.environ['QE75_JOB_SHA256']='not-a-digest'
        worker=threading.Thread(target=reply,daemon=True);worker.start()
        try:
            result=self.call(-1,0,3) if preinit else self.call(0,2,1)
            if job_good:
                worker.join(2.1);self.assertFalse(worker.is_alive());self.assertEqual(errors,[])
                self.assertEqual(requests[0][:5],(b'R07C',1,3,0xffffffff,0) if preinit else (b'R07C',1,1,0,2))
                self.assertEqual(requests[0][5:7],(b'a'*64,b'b'*64))
            return result
        finally:
            server.close();worker.join(2.1);os.environ['QE75_JOB_SHA256']='a'*64

    def test_new_magic_scope_success_is_codec_only(self):self.assertEqual(self.exchange(),0)
    def test_preinit_is_not_world_rank_registration(self):
        self.assertEqual(self.exchange(preinit=True),0)
        self.assertEqual(self.exchange(scope=2,preinit=True),errno.EACCES)
        for args in [(0,0,3),(-1,2,3),(0,2,3),(-1,0,1)]:self.assertEqual(self.call(*args),errno.EINVAL)
        code=(HERE/'collective_harness.c').read_text()
        self.assertLess(code.index('int preinit=r07_collective_lease_call(-1,0,3);'),code.index('int code=MPI_Init_thread'))
    def test_old_abi_and_qe_native_scopes_refused(self):
        for scope in [1,2]:self.assertEqual(self.exchange(scope=scope),errno.EACCES)
    def test_old_magic_not_interchangeable(self):self.assertEqual(self.exchange(magic=b'R07L'),errno.EPROTO)
    def test_signed_overflow_status_refused(self):
        for status in [0x80000000,0xffffffff]:self.assertEqual(self.exchange(status=status),errno.EPROTO)
    def test_negative_challenge_refused(self):self.assertEqual(self.exchange(challenge_ok=False),errno.EPROTO)
    def test_nonzero_status_and_bad_rank(self):
        self.assertEqual(self.exchange(status=errno.EAGAIN),errno.EAGAIN)
        for args in [(-1,2,1),(2,2,1),(0,3,1),(0,2,99)]:self.assertEqual(self.call(*args),errno.EINVAL)
    def test_fingerprint_format_refused_before_peer(self):self.assertEqual(self.exchange(job_good=False),errno.EINVAL)
    def test_probe_has_no_payload_override(self):
        command=probe.fixed_command('r07-owned-'+'1'*32+'.service')
        self.assertEqual(command[-1],str(probe.BINARY))
        for flag in ['PrivateUsers=yes','PrivateNetwork=yes','MemoryMax=67108864','MemorySwapMax=0',
                     'TasksMax=4','RuntimeMaxSec=8s','LimitFSIZE=16384','KillMode=control-group']:
            self.assertIn('--property='+flag,command)
        self.assertNotIn('mpirun',' '.join(command));self.assertNotIn('pw.x',' '.join(command))
    def test_status_normalizes_without_abs_or_overflow(self):
        src=self.root/'status_export.c';lib=self.root/'status.so'
        src.write_text('#include "status.h"\nint exported(int status){return r07_failed(status);}\n')
        r=subprocess.run(['/usr/bin/cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-fPIC','-shared',
                          '-I'+str(HERE),str(src),'-o',str(lib)],capture_output=True,text=True,timeout=10)
        self.assertEqual(r.returncode,0,r.stderr)
        f=ctypes.CDLL(str(lib)).exported;f.argtypes=[ctypes.c_int];f.restype=ctypes.c_int
        for x in [-(1<<31),-13,-1,0,1,7,(1<<31)-1]:self.assertEqual(f(x),int(x!=0))


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(SerialComponents)
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    record=dict(passed=r.wasSuccessful(),methods=r.testsRun,failures=len(r.failures),errors=len(r.errors),
                actual_MPI_collectives=False,MPI_Init=False,QE_executed=False,
                kind='COMPILED_SCOPE3_SERIAL_UNIX_CODEC_ONLY')
    (PRIVATE/'component_results.json').write_text(json.dumps(record,indent=2)+'\n')
    sys.exit(0 if r.wasSuccessful() else 1)
