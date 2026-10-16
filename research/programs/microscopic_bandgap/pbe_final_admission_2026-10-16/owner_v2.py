"""FINAL one-shot NON_SCIENCE sequence; fixed targets only; no material release."""
import ctypes,fcntl,hashlib,json,os,resource,select,signal,stat,subprocess,time,traceback,uuid
from pathlib import Path
from checks import Audit,Refusal,manager_checks,identity_checks,kernel_checks,live_members,GIB
P=Path(__file__).resolve().parent;REPO=P.parents[3];BASE=REPO/'.tmp/r07spc16';OLD=P.parent/'pbe_density_driver_2026-10-16'
LEGACY=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/runtime_admission')
ENV={**os.environ,'XDG_RUNTIME_DIR':'/run/user/1001','DBUS_SESSION_BUS_ADDRESS':'unix:path=/run/user/1001/bus'}
for k in list(ENV):
 if k.startswith(('OMPI_','PMIX_','PMI_','PRTE_')) or k in ('LD_PRELOAD','LD_AUDIT','LD_LIBRARY_PATH','PYTHONPATH','PYTHONHOME'):ENV.pop(k)
FIELDS='Id,LoadState,ActiveState,SubState,MainPID,ControlGroup,InvocationID,Result,ExecMainCode,ExecMainStatus,ExecMainPID,ExecMainStartTimestampMonotonic,ExecMainExitTimestampMonotonic,MemoryMax,MemorySwapMax,TasksMax,KillMode,OOMPolicy,Restart,Delegate,NoNewPrivileges,LimitFSIZE,LimitCORE,RuntimeMaxUSec,TimeoutStopUSec,MemoryPeak,MemorySwapPeak,NRestarts'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def atomic(path,obj):
 data=(json.dumps(obj,indent=2)+'\n').encode()
 if len(data)>1<<20:raise Refusal('ATOMIC_EVIDENCE_BOUND')
 temp=path.with_suffix('.tmp')
 fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:
  if os.write(fd,data)!=len(data):raise Refusal('ATOMIC_SHORT_WRITE')
  os.fsync(fd)
 finally:os.close(fd)
 temp.replace(path);fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
def cmd(args):return subprocess.run(args,env=ENV,capture_output=True,text=True,timeout=3)
def show(unit):
 r=cmd(['/usr/bin/systemctl','--user','show',unit,'--property='+FIELDS])
 return dict(line.split('=',1) for line in r.stdout.splitlines() if '=' in line)
def proc(pid):
 raw=Path(f'/proc/{pid}/stat').read_text();t=raw[raw.rindex(')')+2:].split()
 return dict(pid=pid,start_ticks=int(t[19]),exe=sha(f'/proc/{pid}/exe'),cgroup=Path(f'/proc/{pid}/cgroup').read_text().strip().removeprefix('0::'))
def exited(fd):
 poll=select.poll();poll.register(fd,select.POLLIN);events=poll.poll(0)
 if events and events[0][1]&~(select.POLLIN|select.POLLHUP):raise Refusal('PIDFD_INVALID_EVENTS')
 return bool(events)
def host():
 mem={k:int(v.split()[0])*1024 for k,v in (s.split(':',1) for s in Path('/proc/meminfo').read_text().splitlines())};disk=os.statvfs(BASE)
 return dict(MemAvailable_B=mem['MemAvailable'],free_disk_B=disk.f_bavail*disk.f_frsize)
def floor_check(a):
 x=host();a.need('HOST_FLOORS',x,{'MemAvailable_B_min':4*GIB,'free_disk_B_min':10*GIB},ok=x['MemAvailable_B']>=4*GIB and x['free_disk_B']>=10*GIB);return x
class Ref:
 def __init__(self,unit,a):
  self.unit=unit;self.a=a;self.lib=ctypes.CDLL('libsystemd.so.0');self.bus=ctypes.c_void_p();l=self.lib
  l.sd_bus_new.argtypes=[ctypes.POINTER(ctypes.c_void_p)];l.sd_bus_set_address.argtypes=[ctypes.c_void_p,ctypes.c_char_p];l.sd_bus_set_bus_client.argtypes=[ctypes.c_void_p,ctypes.c_int];l.sd_bus_start.argtypes=[ctypes.c_void_p];l.sd_bus_unref.argtypes=[ctypes.c_void_p]
  l.sd_bus_call_method.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
  for name,code in [('NEW',l.sd_bus_new(ctypes.byref(self.bus))),('ADDRESS',l.sd_bus_set_address(self.bus,b'unix:path=/run/user/1001/bus')),('CLIENT',l.sd_bus_set_bus_client(self.bus,1)),('START',l.sd_bus_start(self.bus))]:a.need('BUS.'+name,code,'>=0',ok=code>=0)
  self.call('RefUnit')
 def call(self,method):
  code=self.lib.sd_bus_call_method(self.bus,b'org.freedesktop.systemd1',b'/org/freedesktop/systemd1',b'org.freedesktop.systemd1.Manager',method.encode(),None,None,b's',self.unit.encode())
  self.a.need('BUS.'+method,code,'>=0',ok=code>=0)
 def close(self):
  # Cleanup must remain possible after absorbing refusal: no token or PASS here.
  code=self.lib.sd_bus_call_method(self.bus,b'org.freedesktop.systemd1',b'/org/freedesktop/systemd1',b'org.freedesktop.systemd1.Manager',b'UnrefUnit',None,None,b's',self.unit.encode())
  self.a.record('CLEANUP.UnrefUnit',code,'>=0',code>=0);self.lib.sd_bus_unref(self.bus)
def prepare(kind,elf,build):
 root=BASE/('final-'+kind+'-'+uuid.uuid4().hex);root.mkdir(mode=0o700)
 for d in ('input','foreign','output','temp'):(root/d).mkdir()
 for n in ('input/ro','foreign/canary','foreign/new_missing','foreign/inherited','temp/ro','output/allowed','stdin','stdout','stderr','go'):(root/n).write_bytes(b'canary' if '/' in n and not n.startswith('output') else b'')
 unit='r07-owned-'+uuid.uuid4().hex+'.service';nonce=uuid.uuid4().hex
 props={'Type':'exec','MemoryMax':str(12*GIB),'MemorySwapMax':'0','TasksMax':'12','RuntimeMaxSec':'600s','TimeoutStopSec':'3s','KillMode':'control-group','OOMPolicy':'kill','Restart':'no','Delegate':'no','NoNewPrivileges':'yes','LimitCORE':'0','LimitFSIZE':str(1<<20),'LimitNOFILE':'64','Nice':'10','CPUQuota':'200%','AllowedCPUs':' '.join(map(str,sorted(os.sched_getaffinity(0))[:2])),'WorkingDirectory':str(root),'StandardInput':'file:'+str(root/'stdin'),'StandardOutput':'append:'+str(root/'stdout'),'StandardError':'append:'+str(root/'stderr'),'UnsetEnvironment':'LD_PRELOAD LD_AUDIT LD_LIBRARY_PATH PYTHONHOME PYTHONPATH'}
 command=['/usr/bin/systemd-run','--user','--wait','--quiet','--unit='+unit]
 for k,v in props.items():command+=['--property='+k+'='+v]
 for k,v in {'TMPDIR':str(root/'temp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','OMPI_MCA_btl':'self','OMPI_MCA_pml':'ob1'}.items():command+=['--setenv='+k+'='+v]
 command+=[str(elf),str(root),nonce]
 job={'kind':kind,'scope':'R07_FINAL_V2_NON_SCIENCE','unit':unit,'root':str(root),'nonce':nonce,'elf_sha256':sha(elf),'source_sha256':build['source_sha256'],'owner_sha256':sha(__file__),'checks_sha256':sha(P/'checks.py'),'argv':command,'props':props,'science_release':False}
 atomic(root/'FROZEN.json',job);return job

def attempt(job,all_roots):
 root=Path(job['root']);a=Audit(root/'predicates.jsonl');unit=job['unit'];child=None;fd=None;ref=None;cg=None;inv=None;identity=None;t=time.monotonic()
 result={'status':'REFUSED_ABSORBING','unit':unit,'scope':job['scope'],'kind':job['kind'],'science_release':False,'samples':[]}
 try:
  a.need('UID',os.getuid(),1001);a.need('FRESH_UNIT',show(unit).get('LoadState'),'not-found');a.need('EMPTY_NONCE',(root/'go').read_bytes().hex(),'')
  a.need('PINNED_ELF',sha(job['argv'][-3]),job['elf_sha256']);a.need('PINNED_OWNER',sha(__file__),job['owner_sha256']);a.need('PINNED_CHECKS',sha(P/'checks.py'),job['checks_sha256']);floor_check(a)
  child=subprocess.Popen(job['argv'],env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
  while time.monotonic()-t<5:
   s=show(unit);pid=int(s.get('MainPID','0'))
   if pid and s.get('ActiveState')=='active':break
   if child.poll() is not None:raise Refusal('UNIT_ENDED_BEFORE_IDENTITY: '+repr(child.communicate()))
   time.sleep(.01)
  else:raise Refusal('UNIT_START_DEADLINE')
  inv=s.get('InvocationID');a.record('RAW_LIVE_MANAGER',s,'facts before checks',True)
  ref=Ref(unit,a);identity=proc(pid);a.record('RAW_KERNEL_IDENTITY',identity,'facts before checks',True)
  fd=os.pidfd_open(pid,0);after=proc(pid)
  identity_checks(a,identity,after,job['elf_sha256'],s.get('ControlGroup'),exited(fd));a.need('INVOCATION_FORMAT',inv,'32 hex',ok=isinstance(inv,str) and len(inv)==32 and all(c in '0123456789abcdef' for c in inv))
  a.need('MANAGER_SUBTREE',identity['cgroup'],'UID1001 user-manager child',ok=identity['cgroup'].startswith('/user.slice/user-1001.slice/user@1001.service/'))
  cg=Path('/sys/fs/cgroup')/identity['cgroup'].lstrip('/')
  kernel={k:(cg/k).read_text().strip() for k in ('memory.max','memory.swap.max','pids.max','memory.oom.group','memory.peak','cgroup.procs','memory.events','pids.events')}
  a.record('RAW_KERNEL_CONTROLS',kernel,'facts before checks',True)
  kernel_checks(a,kernel);manager_checks(a,s,job['props'],unit,inv,pid,identity['cgroup']);live_members(a,[int(p) for p in kernel['cgroup.procs'].split()],pid)
  a.need('READY_NATIVE_IDENTITY',f'V2 READY pid={pid} ' in (root/'stdout').read_text(),True)
  identity_checks(a,identity,proc(pid),job['elf_sha256'],identity['cgroup'],exited(fd))
  def release():
   a.record('PRE_NONCE_COMPLETE',{'pid':pid,'invocation':inv},'all named predicates durable',True)
   with (root/'go').open('wb') as f:f.write(job['nonce'].encode());f.flush();os.fsync(f.fileno())
  a.nonce_release(release);result.update(identity=identity,invocation=inv)
  while time.monotonic()-t<25:
   obs=host();block=logical=files=0
   for r in all_roots:
    for p in r.rglob('*'):
     st=p.lstat()
     if stat.S_ISLNK(st.st_mode):raise Refusal('OUTPUT_SYMLINK')
     block+=st.st_blocks*512;logical+=st.st_size;files+=1
   obs.update(output_blocks_B=block,output_logical_B=logical,output_inodes=files,holder_peak_RSS_B=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
   if cg.exists():obs.update(members=[int(p) for p in (cg/'cgroup.procs').read_text().split()],kernel_peak_B=int((cg/'memory.peak').read_text()))
   result['samples'].append(obs)
   a.need('BOUNDED_SAMPLE',obs,'host>=4GiB disk>=10GiB output<14GiB holder<512MiB single process',ok=obs['MemAvailable_B']>=4*GIB and obs['free_disk_B']>=10*GIB and max(block,logical)<14*GIB and files<128 and obs['holder_peak_RSS_B']<512*(1<<20) and obs.get('members',[]) in ([],[pid]))
   if exited(fd) and child.poll() is not None:break
   time.sleep(.1)
  else:raise Refusal('FINAL_ELAPSED_DEADLINE')
  out,err=child.communicate(timeout=3);s=show(unit);a.record('RAW_TERMINAL_MANAGER',s,'terminal facts',True)
  result.update(final_manager=s,wait_returncode=child.returncode,launcher_stdout=out.decode(),launcher_stderr=err.decode())
  for name,got,want in [('INVOCATION',s.get('InvocationID'),inv),('MANAGER_RESULT',s.get('Result'),'success'),('EXIT_CODE',s.get('ExecMainCode'),'1'),('EXIT_STATUS',s.get('ExecMainStatus'),'0'),('WAIT',child.returncode,0),('MANAGER_TERMINAL',s.get('ActiveState'),'inactive'),('PIDFD_EXIT',exited(fd),True),('CGROUP_EMPTY',not cg.exists() or not (cg/'cgroup.procs').read_text().split(),True)]:a.need('TERMINAL.'+name,got,want)
  text=(root/'stdout').read_text();a.need('NATIVE_STDERR',(root/'stderr').read_text(),'')
  expected='inherited_exemption_demonstrated_then_closed=1' if job['kind']=='fs' else 'SINGLETON world_size=1 rank=0 finalized=1'
  a.need('NATIVE_COMPLETE',expected in text,True);a.need('ACTUAL_ABI7','abi=7' in text,True)
  for n in ('input/ro','foreign/canary','foreign/new_missing','temp/ro'):a.need('CANARY.'+n,(root/n).read_text(),'canary')
  a.need('INHERITED_CAPABILITY_DEMO',(root/'foreign/inherited').read_text(),'Xanary' if job['kind']=='fs' else 'canary')
  result['status']='PASS_NON_SCIENCE_V2'
 except BaseException as e:
  result['error']=repr(e);result['traceback']=traceback.format_exc()
  try:a.exception(e)
  except BaseException as logerr:result['evidence_write_error']=repr(logerr)
 finally:
  if child is not None:
   try:
    s=show(unit)
    if inv and s.get('InvocationID')==inv and s.get('ActiveState') in ('active','activating','deactivating'):cmd(['/usr/bin/systemctl','--user','stop',unit])
    out,err=child.communicate(timeout=5);result.setdefault('wait_returncode',child.returncode);result.setdefault('launcher_stdout',out.decode());result.setdefault('launcher_stderr',err.decode())
    result['terminal_manager']=show(unit)
    result['process_pidfd_exited']=bool(fd is not None and exited(fd));result['original_cgroup_empty_or_absent']=bool(cg is not None and (not cg.exists() or not (cg/'cgroup.procs').read_text().split()))
   except BaseException as e:result['cleanup_error']=repr(e);result['status']='REFUSED_ABSORBING'
  result['elapsed_s']=time.monotonic()-t;result['stdout']=(root/'stdout').read_text(errors='replace');result['stderr']=(root/'stderr').read_text(errors='replace')
  result['predicates_sha256']=sha(root/'predicates.jsonl')
  atomic(root/'RESULT.json',result);atomic(P/('result_'+job['kind']+'.json'),result)
  if ref:
   try:ref.close()
   except BaseException as e:atomic(P/'CLEANUP_REFUSAL.json',{'unit':unit,'error':repr(e),'science_release':False})
  if fd is not None:os.close(fd)
  if result.get('terminal_manager',{}).get('ActiveState')=='failed':cmd(['/usr/bin/systemctl','--user','reset-failed',unit])
  (P/('predicates_'+job['kind']+'.jsonl')).write_bytes((root/'predicates.jsonl').read_bytes())
 return result

def main():
 resource.setrlimit(resource.RLIMIT_AS,(512<<20,512<<20));resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_FSIZE,(1<<20,1<<20))
 if (P/'STARTED.json').exists():raise Refusal('FINAL_SEQUENCE_ONE_SHOT_ALREADY_STARTED')
 a=Audit(P/'preflight.jsonl')
 try:
  a.need('UID',os.getuid(),1001);floor_check(a)
  build=json.loads((P/'build_result.json').read_text());a.need('BUILT_NON_SCIENCE',build['passed'],True)
  for path,h in build['elf_pins'].items():a.need('PINNED_TINY_ELF.'+Path(path).name,sha(path),h)
  a.need('PINNED_C_SOURCE',sha(P/'runtime_probe_v2.c'),build['source_sha256'])
  a.need('OFFLINE_VERIFIED',json.loads((P/'offline_result.json').read_text())['passed'],True)
  a.need('PROTECTION_VERIFIED',json.loads((P/'protection_before.json').read_text())['passed'],True)
  lock=os.open(LEGACY/'MPI_FAMILY.lock',os.O_RDONLY|os.O_CLOEXEC);fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  registry=json.loads((LEGACY/'CURRENT_FAMILY.json').read_text());a.need('REGISTERED_FAMILY_INACTIVE',registry.get('phase'),'FINISHED');a.need('REGISTERED_MEMBERS_EMPTY',registry.get('members'),[])
  jobs=[prepare(k,Path(build['root'])/n,build) for k,n in [('fs','fs_probe_v2'),('mpi','singleton_probe_v2')]]
  for j in jobs:a.need('PREPARED_FRESH_UNIT.'+j['kind'],show(j['unit']).get('LoadState'),'not-found')
  frozen={'scope':'FINAL_ONE_SEQUENCE_NON_SCIENCE_V2','jobs':jobs,'before':host(),'owner_sha256':sha(__file__),'checks_sha256':sha(P/'checks.py'),'science_release':False,'conditional_mpi_only_if_fs_complete':True,'no_retry_after_refusal':True}
  atomic(P/'STARTED.json',frozen)
  roots=[Path(j['root']) for j in jobs]+[P,Path(build['root'])]
  fs=attempt(jobs[0],roots);print('FS:',fs['status'],fs.get('error',''))
  if fs['status']!='PASS_NON_SCIENCE_V2' or not fs.get('process_pidfd_exited') or not fs.get('original_cgroup_empty_or_absent') or (P/'CLEANUP_REFUSAL.json').exists():return
  mpi=attempt(jobs[1],roots);print('MPI:',mpi['status'],mpi.get('error',''))
 except BaseException as e:
  a.exception(e);atomic(P/'PREFLIGHT_REFUSAL.json',{'error':repr(e),'traceback':traceback.format_exc(),'science_release':False})
 finally:
  if 'lock' in locals():fcntl.flock(lock,fcntl.LOCK_UN);os.close(lock)
if __name__=='__main__':main()
