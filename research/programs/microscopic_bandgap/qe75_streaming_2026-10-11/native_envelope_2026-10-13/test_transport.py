"""Real serial ABI peers plus unchanged-versus-fixed collective counterexample."""
import errno
import fcntl
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
from build_transport import HERE,PRIVATE
from binding import RankRegistry,REQUEST,REPLY,MAGIC,VERSION,digest,artifact_sha256
from family_runtime import LOCK
from process_identity import proc

MEASURED=[]


class WireServer:
    def __init__(self,worker,status):
        self.worker=worker;self.status=status;self.done=threading.Event();self.error=None
        self.profile={'kind':'SERIAL_STATUS_COUNTEREXAMPLE','native_qualified':False}
        self.job={'version':2,'binding_version':1,'rank_count':2,'kind':'EXPLICIT_COMPILED_ABI_NO_MPI',
                  'profile_sha256':digest(self.profile),'executable_sha256':artifact_sha256(worker)}
        self.registry=RankRegistry(self.job,self.profile,os.getpid(),worker)
    def __enter__(self):
        self.fd=os.open(LOCK,os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.sock=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
        self.address='qe75-status-'+os.urandom(8).hex();self.sock.bind('\0'+self.address);self.sock.listen(2);self.sock.settimeout(.05)
        self.thread=threading.Thread(target=self.serve);self.thread.start()
        return self
    def serve(self):
        while not self.done.is_set():
            try:s,_=self.sock.accept()
            except socket.timeout:continue
            try:
                s.settimeout(1);pid,uid,gid=struct.unpack('3i',s.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
                raw=s.recv(REQUEST.size+1);self.registry.handle(uid,pid,raw)
                challenge=REQUEST.unpack(raw)[-1]
                s.send(REPLY.pack(MAGIC,VERSION,self.status,1,challenge))
            except Exception as error:self.error=str(error)
            finally:s.close()
    def run(self,scope=1):
        env=dict(os.environ,QE75_LEASE_SOCKET=self.address,QE75_LEASE_LOCK=str(LOCK),
                 QE75_LEASE_PID=str(os.getpid()),QE75_LEASE_TICKS=str(proc(os.getpid())['start_ticks']),
                 QE75_JOB_SHA256=digest(self.job),QE75_PROFILE_SHA256=digest(self.profile))
        r=subprocess.run([str(self.worker),str(scope)],env=env,capture_output=True,text=True,timeout=3)
        if self.error:raise RuntimeError(self.error)
        return int(r.stdout.split()[-1])
    def __exit__(self,*args):
        self.done.set();self.thread.join(2);assert not self.thread.is_alive()
        self.sock.close();self.registry.close();os.close(self.fd)


class TransportTest(unittest.TestCase):
    def test_real_wire_unsigned_status_counterexample_and_refusal(self):
        for status in [0x80000000,0xffffffff]:
            result={}
            for version in ['legacy','safe']:
                with WireServer(PRIVATE/'transport'/f'{version}_worker',status) as server:result[version]=server.run()
            self.assertLess(result['legacy'],0);self.assertEqual(result['safe'],errno.EPROTO)
            MEASURED.append({'kind':'LIVE_SERIAL_KERNEL_ABI_NOT_MPI','status':status,'returns':result})
    def test_valid_status_and_native_scope_semantics_preserved(self):
        for status,scope,wanted in [(0,1,0),(13,1,13),(0,2,errno.EACCES)]:
            with WireServer(PRIVATE/'transport/safe_worker',status) as server:self.assertEqual(server.run(scope),wanted)
    def test_signed_nonzero_cannot_be_masked_by_collective_max(self):
        for rank in [0,1]:
            for scenario in [0,1,2,3]:
                results={}
                for version in ['legacy','safe']:
                    r=subprocess.run([str(PRIVATE/'transport'/f'{version}_model'),str(scenario),str(rank)],
                                     capture_output=True,text=True,timeout=3)
                    results[version]={'returncode':r.returncode,'stdout':r.stdout}
                if scenario in [1,2]:self.assertEqual(results['legacy']['returncode'],0)
                self.assertEqual(results['safe']['returncode'],0 if scenario==0 else 88)
                MEASURED.append({'kind':'SERIAL_DECISION_MODEL_NOT_MPI','rank':rank,'scenario':scenario,'results':results})


if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TransportTest))
    (PRIVATE/'transport_tests.json').write_text(json.dumps({'passed':r.wasSuccessful(),'methods':r.testsRun,
                'evidence':MEASURED,'native_MPI_QE_run':False,'native_scope_issued':False},indent=2)+'\n')
    raise SystemExit(0 if r.wasSuccessful() else 1)
