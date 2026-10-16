"""Named, durable, absorbing NON_SCIENCE predicates. Never a science release."""
import inspect,json,os,time,traceback
from pathlib import Path
GIB=1<<30
class Refusal(RuntimeError):pass
class Audit:
 def __init__(self,path):
  self.path=Path(path);self.count=0;self.failed=False
 def record(self,name,observed,expected,passed,**extra):
  frame=inspect.currentframe().f_back
  row=dict(sequence=self.count,monotonic=time.monotonic(),name=name,observed=observed,expected=expected,passed=bool(passed),source=dict(file=frame.f_code.co_filename,line=frame.f_lineno),**extra)
  raw=(json.dumps(row,sort_keys=True)+'\n').encode()
  if self.count>=300 or len(raw)>131072:raise Refusal('EVIDENCE_BOUND')
  fd=os.open(self.path,os.O_WRONLY|os.O_APPEND|os.O_CREAT|os.O_NOFOLLOW|os.O_CLOEXEC,0o600)
  try:
   if os.fstat(fd).st_size+len(raw)>1<<20:raise Refusal('EVIDENCE_FILE_BOUND')
   if os.write(fd,raw)!=len(raw):raise Refusal('EVIDENCE_SHORT_WRITE')
   os.fsync(fd)
  finally:os.close(fd)
  self.count+=1
  if not passed:self.failed=True
 def need(self,name,observed,expected,*,ok=None):
  passed=(observed==expected) if ok is None else bool(ok)
  frame=inspect.currentframe().f_back
  self.record(name,observed,expected,passed,predicate_source=dict(file=frame.f_code.co_filename,line=frame.f_lineno))
  if self.failed:raise Refusal(name)
 def exception(self,error):
  self.record('EXCEPTION',repr(error),'no exception',False,traceback=traceback.format_exc())
 def nonce_release(self,fn):
  self.need('NO_PRIOR_REFUSAL',self.failed,False)
  fn()

def manager_checks(a,s,p,unit,inv,pid,cg):
 for k,v in [('Id',unit),('LoadState','loaded'),('ActiveState','active'),('InvocationID',inv),('MainPID',str(pid)),('ControlGroup',cg)]:a.need('MANAGER.'+k,s.get(k),v)
 for k in ('MemoryMax','MemorySwapMax','TasksMax','KillMode','OOMPolicy','Restart','Delegate','NoNewPrivileges','LimitFSIZE','LimitCORE'):a.need('MANAGER.'+k,s.get(k),p[k])
 a.need('MANAGER.RuntimeMaxUSec',s.get('RuntimeMaxUSec'),'10min')
 a.need('MANAGER.TimeoutStopUSec',s.get('TimeoutStopUSec'),'3s')
def identity_checks(a,before,after,wanted_exe,cg,pidfd_exited):
 a.need('PID_STILL_PRESENT',after is not None,True)
 a.need('PID',after.get('pid'),before['pid'])
 a.need('START_TICKS',after.get('start_ticks'),before['start_ticks'])
 a.need('ELF',after.get('exe'),wanted_exe)
 a.need('CGROUP',after.get('cgroup'),cg)
 a.need('PIDFD_LIVE',pidfd_exited,False)
def kernel_checks(a,v):
 for k,w in [('memory.max',str(12*GIB)),('memory.swap.max','0'),('pids.max','12')]:a.need('KERNEL.'+k,v.get(k),w)
def live_members(a,members,pid):a.need('EXACT_ONE_PROCESS',members,[pid])
