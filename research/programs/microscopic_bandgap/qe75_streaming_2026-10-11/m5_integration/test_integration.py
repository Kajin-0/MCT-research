"""Real production guardian/compiled peer/child-hook paths. No MPI or QE."""
from pathlib import Path
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest

from production_transport import HERE,BUILD,create_job,digest,Refusal
from family_runtime import PRIVATE,LOCK,REGISTRY,read_meta,verify_job
from process_identity import Identity,proc,subreaper,reap,flock_owner

MEASURED=[]

def wait_file(path,seconds=3):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        if path.exists():
            try: return read_meta(path)
            except json.JSONDecodeError: pass
        time.sleep(.01)
    raise AssertionError('bounded wait exhausted: '+str(path))


class IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls): subreaper()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=PRIVATE,prefix='integration-')
        self.base=Path(self.temp.name);self.children=[]

    def tearDown(self):
        for process,identity in self.children:
            if identity.live(): identity.send(signal.SIGTERM)
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                identity.send(signal.SIGKILL);process.wait(timeout=2)
            identity.close()
        reap();self.temp.cleanup()

    def job(self,name='job',**kw):
        root=self.base/name;create_job(root,**kw);return root

    def start(self,root):
        with open(root/'owner.log','wb') as out:
            p=subprocess.Popen([sys.executable,str(HERE.parent/'runtime_admission/family_runtime.py'),'owner',str(root)],
                               stdout=out,stderr=out,close_fds=True)
        identity=Identity(p.pid);self.children.append((p,identity));return p,identity

    def finish(self,root,p):
        p.wait(timeout=8);result=wait_file(root/'RESULT.json',4)
        deadline=time.monotonic()+1
        while flock_owner(LOCK) and time.monotonic()<deadline: time.sleep(.01)
        for member in result.get('members',[])+result.get('survivors',[]):
            try:
                row=proc(member['pid']);self.assertFalse(row['start_ticks']==member['start_ticks'] and row['state']!='Z')
            except FileNotFoundError: pass
        self.assertEqual(result['survivors'],[]);self.assertEqual(flock_owner(LOCK),[])
        self.assertFalse(result['native_PW_MPI_executed'])
        MEASURED.append({'case':self.id().split('.')[-1],**result})
        return result

    def test_live_production_wire_and_child_hook(self):
        root=self.job();p,i=self.start(root);r=self.finish(root,p)
        self.assertTrue(r['passed'],r)
        typed=r['typed_transport'];self.assertEqual(typed['scope'],'ABI_NO_MPI')
        self.assertEqual(set(r['rank_registration']),{'0','1'})
        self.assertNotEqual(typed['binding']['job_sha256'],typed['binding']['profile_sha256'])
        self.assertEqual({h['world_rank'] for h in typed['hook_receipts']},{0,1})
        for rank in [0,1]:
            h=read_meta(root/f'out/hook{rank}.json');receipt=h['receipt']
            self.assertEqual(receipt['scope'],1);self.assertIn('not native authority',h['native_refusal'])
            self.assertEqual(receipt['native_pid'],r['rank_registration'][str(rank)]['pid'])
            self.assertEqual(receipt['owner'],read_meta(root/'JOB.json')['bridge_owner'])
        self.assertGreater(r['peak_summed_RSS_bytes'],0)
        self.assertGreaterEqual(r['minimum_MemAvailable_bytes'],4*(1<<30))
        self.assertGreaterEqual(r['minimum_free_disk_bytes'],10*(1<<30))
        for reservation in r['reservations']:
            st=Path(reservation['path']).stat();self.assertEqual(st.st_size,reservation['bytes'])
            self.assertGreaterEqual(st.st_blocks*512,reservation['bytes'])
        with self.assertRaisesRegex(Refusal,'reused'): verify_job(root)

    def test_wrong_job_profile_guardian_identity_and_native_scope(self):
        for mode in ['bad_job','bad_profile','bad_ticks','native_scope','duplicate']:
            with self.subTest(mode=mode):
                root=self.job(mode,scenario=mode);p,i=self.start(root);r=self.finish(root,p)
                self.assertFalse(r['passed']);self.assertFalse(r['typed_transport']['hook_receipts'])

    def test_registered_dead_rank_cannot_authorize_child(self):
        root=self.job(scenario='dead_rank');p,i=self.start(root);r=self.finish(root,p)
        self.assertFalse(r['passed']);self.assertFalse(r['typed_transport']['hook_receipts'])

    def test_owned_but_unregistered_launcher_child_refused(self):
        root=self.job(scenario='forged_hook');p,i=self.start(root);r=self.finish(root,p)
        self.assertTrue(r['passed'],r)
        self.assertIn('not descended from a live registered rank',read_meta(root/'out/forged_refusal.json')['reason'])

    def test_outside_hook_and_malformed_packet_refused(self):
        from binding import REPLY,REQUEST,MAGIC,VERSION
        root=self.job(scenario='hold',wall=4);p,i=self.start(root);wait_file(root/'out/hook0.json')
        ticket=read_meta(root/'LEASE_ENDPOINT.json')
        for raw in [b'R07Lshort',REQUEST.pack(MAGIC,VERSION,1,0,2,ticket['job_sha256'].encode(),ticket['profile_sha256'].encode(),b'n'*32)]:
            with socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET) as s:
                s.settimeout(1);s.connect('\0'+ticket['abstract_socket']);s.send(raw)
                reply=REPLY.unpack(s.recv(REPLY.size));self.assertNotEqual(reply[2],0);self.assertEqual(reply[3],1)
        from runtime_client import typed_request
        with self.assertRaisesRegex(Refusal,'outside pinned owned family'): typed_request(root,ticket['profile_sha256'])
        i.send(signal.SIGTERM);r=self.finish(root,p);self.assertFalse(r['passed'])

    def test_transport_owner_crash_and_fresh_lease(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root);wait_file(root/'out/hook0.json')
        i.send(signal.SIGKILL);p.wait(timeout=1);r=self.finish(root,p);self.assertFalse(r['passed']);reap()
        root2=self.job('fresh');p2,i2=self.start(root2);self.assertTrue(self.finish(root2,p2)['passed'])

    def test_transport_guardian_crash_owner_cleans(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root);wait_file(root/'out/hook0.json')
        ticket=read_meta(root/'LEASE_ENDPOINT.json');guardian=Identity(ticket['guardian']['pid'])
        try: guardian.send(signal.SIGKILL)
        finally: guardian.close()
        r=self.finish(root,p);self.assertIn('guardian died; owner fallback',r['reason'])

    def test_transport_wall_cap_terminates_only_owned_family(self):
        root=self.job(scenario='hold',wall=.8);p,i=self.start(root);r=self.finish(root,p)
        self.assertFalse(r['passed']);self.assertIn('monotonic wall cap',r['reason'])

    def test_profile_mutation_native_relabelling_and_oversize_refused(self):
        for mode in ['profile','native','oversize']:
            root=self.job(mode);job=read_meta(root/'JOB.json')
            if mode=='profile':
                profile=read_meta(root/'PROFILE.json');profile['native_qualified']=True
                (root/'PROFILE.json').write_text(json.dumps(profile))
            elif mode=='native':
                job.update(kind='QEF_QE75_NATIVE_FIXTURE',runtime_authorized=True)
                (root/'JOB.json').write_text(json.dumps(job))
            else:
                job['output_envelope_bytes']=22*(1<<30);(root/'JOB.json').write_text(json.dumps(job))
            with self.assertRaises(Refusal): verify_job(root)
            self.assertEqual(list((root/'scratch').iterdir()),[])


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IntegrationTest))
    (BUILD/'integration_tests.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
             'real_guardian_component_evidence':MEASURED,'MPI_PW_executed':False},indent=2)+'\n')
    sys.exit(0 if result.wasSuccessful() else 1)
