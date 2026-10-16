"""Offline injections and actual retained manager fixture; no systemd/MPI launch."""
import copy,json,tempfile,unittest
from pathlib import Path
from checks import Audit,Refusal,manager_checks,identity_checks,kernel_checks,live_members,GIB
P=Path(__file__).resolve().parent;OLD=P.parent/'pbe_density_driver_2026-10-16'
class Checks(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=P.parents[3]/'.tmp/r07spc16');self.file=Path(self.temp.name)/'audit.jsonl';self.a=Audit(self.file)
  self.r=json.loads((OLD/'runtime_fs_probe.json').read_text());self.job=json.loads((OLD/'preregistered_fs_probe.json').read_text());self.m=self.r['terminal_manager']
  self.id=dict(pid=123,start_ticks=456,exe='a'*64,cgroup='/user.slice/dummy')
 def tearDown(self):self.temp.cleanup()
 def check_refusal(self,fn,name):
  with self.assertRaises(Refusal) as e:fn()
  self.assertEqual(str(e.exception),name)
  event=json.loads(self.file.read_text().splitlines()[-1]);self.assertFalse(event['passed']);self.assertTrue(event['predicate_source']['line'])
  with self.assertRaises(Refusal):self.a.nonce_release(lambda:self.fail('token release after refusal'))
 def test_retained_properties_only(self):
  # Real captured TERMINAL data can test property formatting, NOT former live identity.
  for k in ('MemoryMax','MemorySwapMax','TasksMax','KillMode','OOMPolicy','Restart','Delegate','NoNewPrivileges','LimitFSIZE','LimitCORE'):
   self.a.need('RETAINED.'+k,self.m[k],self.job['props'][k])
  self.a.need('RETAINED.RuntimeMaxUSec',self.m['RuntimeMaxUSec'],'10min');self.a.need('RETAINED.TimeoutStopUSec',self.m['TimeoutStopUSec'],'3s')
  self.assertEqual(self.m['ExecMainStatus'],'15');self.assertEqual(self.r['status'],'REFUSED_ABSORBING')
 def test_retained_terminal_cannot_be_live(self):
  self.check_refusal(lambda:manager_checks(self.a,self.m,self.job['props'],self.job['unit'],self.m['InvocationID'],int(self.m['ExecMainPID']),'/unknown'),'MANAGER.ActiveState')
 def test_valid_simulated_live(self):
  identity_checks(self.a,self.id,self.id,'a'*64,self.id['cgroup'],False)
  kernel_checks(self.a,{'memory.max':str(12*GIB),'memory.swap.max':'0','pids.max':'12'});live_members(self.a,[123],123)
 def test_identity_injection(self):
  bad={**self.id,'exe':'b'*64};self.check_refusal(lambda:identity_checks(self.a,self.id,bad,'a'*64,self.id['cgroup'],False),'ELF')
 def test_start_reuse_injection(self):
  self.check_refusal(lambda:identity_checks(self.a,self.id,{**self.id,'start_ticks':999},'a'*64,self.id['cgroup'],False),'START_TICKS')
 def test_cgroup_injection(self):
  self.check_refusal(lambda:identity_checks(self.a,self.id,{**self.id,'cgroup':'/foreign'},'a'*64,self.id['cgroup'],False),'CGROUP')
 def test_process_absence(self):self.check_refusal(lambda:identity_checks(self.a,self.id,None,'a'*64,self.id['cgroup'],False),'PID_STILL_PRESENT')
 def test_live_pidfd_exit(self):self.check_refusal(lambda:identity_checks(self.a,self.id,self.id,'a'*64,self.id['cgroup'],True),'PIDFD_LIVE')
 def test_kernel_property(self):self.check_refusal(lambda:kernel_checks(self.a,{'memory.max':'max'}),'KERNEL.memory.max')
 def test_helper_injection(self):self.check_refusal(lambda:live_members(self.a,[123,124],123),'EXACT_ONE_PROCESS')
 def test_time_and_property(self):
  s=copy.deepcopy(self.m);s.update(ActiveState='active',MainPID='123',ControlGroup='/dummy',RuntimeMaxUSec='11min')
  self.check_refusal(lambda:manager_checks(self.a,s,self.job['props'],self.job['unit'],self.m['InvocationID'],123,'/dummy'),'MANAGER.RuntimeMaxUSec')
 def test_invocation_property_injection(self):
  s=copy.deepcopy(self.m);s.update(ActiveState='active',MainPID='123',ControlGroup='/dummy')
  self.check_refusal(lambda:manager_checks(self.a,s,self.job['props'],self.job['unit'],'f'*32,123,'/dummy'),'MANAGER.InvocationID')
 def test_real_self_pidfd_and_named_owner(self):
  import os,ast
  from owner_v2 import proc,exited
  first=proc(os.getpid());fd=os.pidfd_open(os.getpid(),0)
  try:identity_checks(self.a,first,proc(os.getpid()),first['exe'],first['cgroup'],exited(fd))
  finally:os.close(fd)
  for name in ('owner_v2.py','checks.py'):
   self.assertFalse(any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((P/name).read_text()))))
 def test_traceback_durable(self):
  try:raise OSError('deliberate offline injection')
  except OSError as e:self.a.exception(e)
  row=json.loads(self.file.read_text());self.assertIn('OSError',row['traceback']);self.assertTrue(self.a.failed)
if __name__=='__main__':unittest.main(verbosity=2)
