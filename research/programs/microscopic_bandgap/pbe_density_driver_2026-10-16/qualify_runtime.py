"""Finite NON_SCIENCE qualification only. Fixed compiled probes; NO QE command."""
import ctypes,fcntl,hashlib,json,os,resource,select,stat,subprocess,time,uuid
from pathlib import Path
P=Path(__file__).resolve().parent;REPO=P.parents[3];BASE=REPO/'.tmp/r07spc16'
OLD=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/runtime_admission')
GIB=1<<30
ENV={**os.environ,'XDG_RUNTIME_DIR':'/run/user/1001','DBUS_SESSION_BUS_ADDRESS':'unix:path=/run/user/1001/bus'}
for k in list(ENV):
 if k.startswith(('OMPI_','PMIX_','PMI_','PRTE_')) or k in ('LD_PRELOAD','LD_AUDIT','PYTHONPATH','PYTHONHOME'):ENV.pop(k)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,**kw):return subprocess.run(args,env=ENV,capture_output=True,text=True,timeout=5,**kw)
def show(unit):
 r=run(['/usr/bin/systemctl','--user','show',unit]);return dict(x.split('=',1) for x in r.stdout.splitlines() if '=' in x)
def floors():
 m={a:int(b.split()[0])*1024 for a,b in (s.split(':',1) for s in Path('/proc/meminfo').read_text().splitlines())}
 d=os.statvfs(BASE);a=dict(MemAvailable_B=m['MemAvailable'],free_disk_B=d.f_bavail*d.f_frsize)
 assert a['MemAvailable_B']>=4*GIB and a['free_disk_B']>=10*GIB,a
 return a
def atomic(path,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();assert len(raw)<262144
 tmp=path.with_suffix('.tmp');tmp.write_bytes(raw)
 with tmp.open('rb') as f:os.fsync(f.fileno())
 tmp.replace(path)
 d=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY);os.fsync(d);os.close(d)
def proc(pid):
 raw=Path(f'/proc/{pid}/stat').read_text();tail=raw[raw.rindex(')')+2:].split()
 return dict(pid=pid,start_ticks=int(tail[19]),exe=sha(f'/proc/{pid}/exe'),cgroup=Path(f'/proc/{pid}/cgroup').read_text().strip().removeprefix('0::'))
def exited(fd):
 p=select.poll();p.register(fd,select.POLLIN);e=p.poll(0)
 if e:assert not e[0][1]&~(select.POLLIN|select.POLLHUP)
 return bool(e)
def sample(root,cg):
 a=floors();files=list(root.rglob('*'));blocks=0;logical=0
 for f in files:
  s=f.lstat();assert not stat.S_ISLNK(s.st_mode)
  blocks+=s.st_blocks*512;logical+=s.st_size
 assert max(blocks,logical)<14*GIB
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024;assert rss<512*(1<<20)
 if cg.exists():
  a.update(memory_peak_B=int((cg/'memory.peak').read_text()),pids_current=int((cg/'pids.current').read_text()),members=[int(p) for p in (cg/'cgroup.procs').read_text().split()])
 a.update(output_allocated_B=blocks,output_logical_B=logical,outside_holder_peak_RSS_B=rss);return a
class Ref:
 def __init__(self,unit):
  self.unit=unit;self.lib=ctypes.CDLL('libsystemd.so.0');self.bus=ctypes.c_void_p();l=self.lib
  l.sd_bus_new.argtypes=[ctypes.POINTER(ctypes.c_void_p)];l.sd_bus_set_address.argtypes=[ctypes.c_void_p,ctypes.c_char_p];l.sd_bus_set_bus_client.argtypes=[ctypes.c_void_p,ctypes.c_int];l.sd_bus_start.argtypes=[ctypes.c_void_p];l.sd_bus_unref.argtypes=[ctypes.c_void_p];l.sd_bus_call_method.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
  assert l.sd_bus_new(ctypes.byref(self.bus))>=0;assert l.sd_bus_set_address(self.bus,b'unix:path=/run/user/1001/bus')>=0;assert l.sd_bus_set_bus_client(self.bus,1)>=0;assert l.sd_bus_start(self.bus)>=0
  self.call('RefUnit')
 def call(self,method):assert self.lib.sd_bus_call_method(self.bus,b'org.freedesktop.systemd1',b'/org/freedesktop/systemd1',b'org.freedesktop.systemd1.Manager',method.encode(),None,None,b's',self.unit.encode())>=0
 def close(self):self.call('UnrefUnit');self.lib.sd_bus_unref(self.bus)
def attempt(kind,elf):
 assert kind in ('fs_probe','singleton_probe') and Path(elf).name==kind
 assert os.getuid()==1001
 root=BASE/('density-nonscience-'+kind+'-'+uuid.uuid4().hex);root.mkdir(mode=0o700)
 for n in ('input','foreign','output','temp'):(root/n).mkdir()
 for n in ('input/ro','foreign/canary','foreign/new_missing','foreign/inherited','temp/ro','output/allowed','stdin','stdout','stderr','go'):(root/n).write_bytes(b'canary' if '/' in n and not n.startswith('output') else b'')
 unit='r07-owned-'+uuid.uuid4().hex+'.service';nonce=uuid.uuid4().hex
 props={'Type':'exec','MemoryMax':str(12*GIB),'MemorySwapMax':'0','TasksMax':'12','RuntimeMaxSec':'600s','TimeoutStopSec':'3s','KillMode':'control-group','OOMPolicy':'kill','Restart':'no','Delegate':'no','NoNewPrivileges':'yes','LimitCORE':'0','LimitFSIZE':str(1<<20),'Nice':'10','CPUQuota':'200%','AllowedCPUs':' '.join(map(str,sorted(os.sched_getaffinity(0))[:2])),'WorkingDirectory':str(root),'StandardInput':'file:'+str(root/'stdin'),'StandardOutput':'append:'+str(root/'stdout'),'StandardError':'append:'+str(root/'stderr'),'UnsetEnvironment':' '.join(k for k in os.environ if k.startswith(('OMPI_','PMIX_','PMI_','PRTE_')) or k in ('LD_PRELOAD','LD_AUDIT','LD_LIBRARY_PATH'))}
 cmd=['/usr/bin/systemd-run','--user','--wait','--quiet','--unit='+unit]
 for k,v in props.items():cmd+=['--property='+k+'='+v]
 for k,v in {'TMPDIR':str(root/'temp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','OMPI_MCA_btl':'self','OMPI_MCA_pml':'ob1'}.items():cmd+=['--setenv='+k+'='+v]
 cmd += [str(elf),str(root),nonce]
 job={'scope':'DENSITY_DRIVER_NON_SCIENCE_'+kind,'scientific_release':False,'root':str(root),'unit':unit,'nonce':nonce,'elf_sha256':sha(elf),'source_sha256':sha(P/'runtime_probe.c'),'owner_sha256':sha(__file__),'argv':cmd,'floors':floors(),'props':props,'attempts':1}
 atomic(root/'FROZEN.json',job)
 atomic(P/('preregistered_'+kind+'.json'),job)
 assert show(unit).get('LoadState')=='not-found'
 state={'status':'REFUSED_ABSORBING','scope':job['scope'],'unit':unit,'root':str(root),'samples':[],'science_release':False}
 child=None;fd=None;ref=None;cg=None;identity=None;inv=None;t=time.monotonic()
 try:
  child=subprocess.Popen(cmd,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
  for _ in range(250):
   s=show(unit);pid=int(s.get('MainPID','0'))
   if pid and s.get('ActiveState')=='active':break
   if child.poll() is not None:raise RuntimeError('service refused: '+str(child.communicate()))
   time.sleep(.01)
  else:raise RuntimeError('startup timeout')
  ref=Ref(unit);identity=proc(pid);fd=os.pidfd_open(pid,0);assert proc(pid)==identity and not exited(fd)
  inv=s['InvocationID'];assert len(inv)==32 and identity['exe']==job['elf_sha256']
  assert identity['cgroup']==s['ControlGroup'] and identity['cgroup'].startswith('/user.slice/user-1001.slice/user@1001.service/')
  cg=Path('/sys/fs/cgroup')/identity['cgroup'].lstrip('/')
  for k,v in [('memory.max',str(12*GIB)),('memory.swap.max','0'),('pids.max','12')]:assert (cg/k).read_text().strip()==v
  for k in ('MemoryMax','MemorySwapMax','TasksMax','KillMode','OOMPolicy','Restart','Delegate','NoNewPrivileges','LimitFSIZE','LimitCORE'):
   assert s[k]==props[k],(k,s[k],props[k])
  assert s['RuntimeMaxUSec']=='10min' and s['TimeoutStopUSec']=='3s'
  a=sample(root,cg);assert a['members']==[pid];state['samples'].append(a)
  state.update(identity=identity,InvocationID=inv,initial_manager=s,initial_kernel={k:(cg/k).read_text() for k in ('memory.max','memory.swap.max','pids.max')})
  # Recheck pinned live identity immediately before releasing the nonce gate.
  assert proc(pid)==identity and not exited(fd)
  with (root/'go').open('wb') as f:f.write(nonce.encode());f.flush();os.fsync(f.fileno())
  while time.monotonic()-t<25:
   a=sample(root,cg);state['samples'].append(a)
   if a.get('members'):assert a['members']==[pid],'unapproved helper process'
   if exited(fd) and child.poll() is not None:break
   time.sleep(.02)
  else:raise RuntimeError('bounded runtime/exit deadline')
  out,err=child.communicate(timeout=3);assert len(out)+len(err)<65536
  s=show(unit);state.update(final_manager=s,systemd_run_stdout=out.decode(),systemd_run_stderr=err.decode(),wait_returncode=child.returncode)
  assert s['InvocationID']==inv and s['Result']=='success' and s['ExecMainStatus']=='0' and child.returncode==0
  assert s['ActiveState']=='inactive' and exited(fd)
  assert not cg.exists() or not (cg/'cgroup.procs').read_text().split()
  txt=(root/'stdout').read_text();error=(root/'stderr').read_text();assert not error
  if kind=='fs_probe':assert 'inherited_exemption_demonstrated_then_closed=1' in txt
  else:assert 'SINGLETON world_size=1 rank=0 finalized=1' in txt
  assert (root/'foreign/inherited').read_bytes()==(b'Xanary' if kind=='fs_probe' else b'canary')
  for n in ('input/ro','foreign/canary','foreign/new_missing','temp/ro'):assert (root/n).read_bytes()==b'canary'
  state['status']='PASS_NON_SCIENCE'
 except BaseException as e:state['error']=repr(e)
 finally:
  if child is not None:
   s=show(unit)
   if inv and s.get('InvocationID')==inv and s.get('ActiveState') in ('active','activating','deactivating'):run(['/usr/bin/systemctl','--user','stop',unit])
   try:
    out,err=child.communicate(timeout=5);state.setdefault('wait_returncode',child.returncode);state.setdefault('systemd_run_stdout',out.decode());state.setdefault('systemd_run_stderr',err.decode())
   except subprocess.TimeoutExpired:state['cleanup_error']='systemd foreground wait incomplete'
   state['terminal_manager']=show(unit)
   state['original_process_kernel_exited']=bool(fd is not None and exited(fd))
   state['original_cgroup_empty_or_absent']=bool(cg is not None and (not cg.exists() or not (cg/'cgroup.procs').read_text().split()))
  state['elapsed_s']=time.monotonic()-t
  for n in ('stdout','stderr'):state[n]=(root/n).read_text(errors='replace');state[n+'_sha256']=sha(root/n)
  atomic(root/'RESULT.json',state);atomic(P/('runtime_'+kind+'.json'),state)
  if ref:ref.close()
  if fd is not None:os.close(fd)
  # Only this new failed, stopped unit may be reset after durable failure evidence.
  if state.get('terminal_manager',{}).get('ActiveState')=='failed':run(['/usr/bin/systemctl','--user','reset-failed',unit])
 return state
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512<<20,512<<20))
 resource.setrlimit(resource.RLIMIT_CPU,(60,60))
 resource.setrlimit(resource.RLIMIT_FSIZE,(1<<20,1<<20))
 assert not (P/'runtime_fs_probe.json').exists(),'one-shot attempt exists; never retry'
 build=json.loads((P/'runtime_build.json').read_text());assert build['passed']
 for p,h in build['elf_pins'].items():assert sha(p)==h
 assert sha(P/'runtime_probe.c')==build['source_sha256']
 lock=os.open(OLD/'MPI_FAMILY.lock',os.O_RDONLY|os.O_CLOEXEC);fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 try:
  registry=json.loads((OLD/'CURRENT_FAMILY.json').read_text());assert registry['phase']=='FINISHED' and not registry['members']
  assert Path('/run/user/1001/bus').exists();floors()
  fs=attempt('fs_probe',Path(build['root'])/'fs_probe');print(fs['status'],fs.get('error',''))
  if fs['status']!='PASS_NON_SCIENCE' or not fs['original_process_kernel_exited'] or not fs['original_cgroup_empty_or_absent']:return
  mpi=attempt('singleton_probe',Path(build['root'])/'singleton_probe');print(mpi['status'],mpi.get('error',''))
 finally:fcntl.flock(lock,fcntl.LOCK_UN);os.close(lock)
if __name__=='__main__':main()
