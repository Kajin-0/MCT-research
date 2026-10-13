"""Bounded fixed non-MPI service observation; NEVER an MPI/native issuer."""
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import selectors
import socket
import struct
import subprocess
import sys
import time
import uuid

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'cgroup_owned_2026-10-13'))
from contracts import (BASE,DFT,LOCK,REGISTRY,LIB,Refusal,Identity,atomic_json,manager_env,
                       memory,proc,ctl,show,cgroup_path,own_cgroup,counters,members,
                       flock_owner,digest,LinuxGuard,quota_headroom)
PRIVATE=BASE/'namespace_cookie_20261013'
BINARY=PRIVATE/'cookie_probe.v1'
CASES={'normal','bad_nonce','owner_disconnect'}
SO_NETNS_COOKIE=71


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def socket_cookie(sock):
    raw=sock.getsockopt(socket.SOL_SOCKET,SO_NETNS_COOKIE,8)
    if len(raw)!=8:raise Refusal('kernel cookie extent')
    value=struct.unpack('=Q',raw)[0]
    if not value:raise Refusal('zero kernel cookie')
    return value


def fresh_host_cookies():
    result=[]
    for _ in range(3):
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM|socket.SOCK_CLOEXEC) as s:
            result.append(socket_cookie(s))
    if len(set(result))!=1:raise Refusal('fresh host socket namespace changed')
    return result


def launch_command(job,owner,lockstat):
    # Exact fixed C binary only. No payload/environment/limit override.
    properties=dict(Type='exec',MemoryMax=str(64<<20),MemorySwapMax='0',TasksMax='4',
                    RuntimeMaxSec='8s',TimeoutStopSec='1s',OOMPolicy='kill',KillMode='control-group',
                    Delegate='no',Restart='no',SendSIGKILL='yes',LimitFSIZE='16384',LimitCORE='0',
                    LimitNOFILE='64',NoNewPrivileges='yes',PrivateUsers='yes',PrivateNetwork='yes',
                    RestrictAddressFamilies='AF_UNIX AF_INET AF_INET6 AF_NETLINK',SystemCallArchitectures='native',
                    WorkingDirectory=str(DFT),UnsetEnvironment='LD_PRELOAD LD_AUDIT LD_LIBRARY_PATH PYTHONPATH PYTHONHOME')
    return ['/usr/bin/systemd-run','--user','--pipe','--wait','--quiet','--unit='+job['unit'],
            *['--property='+k+'='+v for k,v in properties.items()],str(BINARY),job['socket'],
            str(owner['pid']),str(owner['start_ticks']),digest(job),job['profile_sha256'],
            str(job['host_cookie']),str(lockstat.st_dev),str(lockstat.st_ino),job['case']]


def validate_observation(h,job,kernel_pid,fields,kernel):
    if h.get('event')!='HELLO' or h.get('scope')!='NON_MPI_NAMESPACE_COMPONENT':raise Refusal('typed non-MPI HELLO')
    if h.get('job')!=digest(job) or h.get('profile')!=job['profile_sha256']:raise Refusal('JOB/PROFILE mismatch')
    for key in ['pid','uid','start_ticks','inherited_sockets','interfaces','lo_entries','up_entries','nonlo_entries',
                'bad_addresses','ns_stat_errno','exe_stat_errno','exe_dev','exe_ino']:
        if type(h.get(key)) is not int or h[key]<0:raise Refusal('typed kernel observation '+key)
    if h.get('pid')!=kernel_pid or h.get('uid')!=1001 or h.get('start_ticks')!=proc(kernel_pid)['start_ticks']:
        raise Refusal('kernel peer/start identity mismatch')
    if fields.get('MainPID')!=str(kernel_pid) or fields.get('ActiveState')!='active' or fields.get('InvocationID')!=h.get('invocation'):
        raise Refusal('live unit identity mismatch')
    if h.get('cgroup')!=fields.get('ControlGroup') or h['cgroup']!=own_cgroup(kernel_pid):raise Refusal('actual cgroup mismatch')
    if not isinstance(h.get('nonce'),str) or len(h['nonce'])!=64 or any(c not in '0123456789abcdef' for c in h['nonce']):
        raise Refusal('challenge extent/encoding')
    for key,want in [('memory_max','67108864'),('swap_max','0'),('tasks_max','4'),('oom_group','1')]:
        if kernel.get(key)!=want:raise Refusal('actual kernel limit mismatch '+key)
    for key,want in [('MemoryMax','67108864'),('MemorySwapMax','0'),('TasksMax','4'),('LimitFSIZE','16384'),
                     ('LimitNOFILE','64'),('LimitCORE','0'),('PrivateNetwork','yes'),('PrivateUsers','yes'),
                     ('KillMode','control-group'),('OOMPolicy','kill'),('Delegate','no'),('Restart','no'),('NoNewPrivileges','yes')]:
        if fields.get(key)!=want:raise Refusal('actual manager property mismatch '+key)
    cookies=h.get('cookies')
    if not isinstance(cookies,list) or len(cookies)!=3 or any(type(c) is not int or c<=0 or c>=1<<64 for c in cookies):
        raise Refusal('cookie extent/type')
    if len(set(cookies))!=1 or cookies[0]==job['host_cookie']:raise Refusal('namespace cookie comparison')
    if h.get('inherited_sockets')!=0 or h.get('interfaces')!=1 or h.get('nonlo_entries')!=0 or h.get('bad_addresses')!=0:
        raise Refusal('socket/interface isolation evidence')
    if type(h.get('lo_entries')) is not int or h['lo_entries']<=0 or h.get('up_entries')!=h['lo_entries']:
        raise Refusal('loopback not verifiably up')
    st=BINARY.stat()
    if h.get('exe_stat_errno')!=0 or (h.get('exe_dev'),h.get('exe_ino'))!=(st.st_dev,st.st_ino):
        raise Refusal('self executing image identity unavailable')


def live_fields(unit):
    f=show(unit)
    r=ctl(unit,'show','--property=PrivateNetwork,PrivateUsers,LimitNOFILE')
    f.update(dict(s.split('=',1) for s in r.stdout.splitlines() if '=' in s))
    return f


def run(case):
    if case not in CASES:raise Refusal('fixed non-MPI case allowlist')
    build=json.loads((PRIVATE/'build.json').read_text())
    if sha(BINARY)!=build['binary_sha256'] or sha(HERE/'cookie_probe.c')!=build['source_sha256']:raise Refusal('compiled/source pins')
    legacy=REGISTRY.read_bytes()
    if json.loads(legacy)['phase']!='FINISHED' or json.loads((BASE/'cgroup_owned_20261013/CURRENT_UNIT.json').read_text())['phase']!='FINISHED':
        raise Refusal('old owned families not closed')
    root=DFT/'.tmp'/('r07cookie-'+uuid.uuid4().hex);root.mkdir(mode=0o700)
    endpoint=str(root/'owner.sock')
    if len(os.fsencode(endpoint))>=108:raise Refusal('pathname socket extent')
    host=fresh_host_cookies();profile={'scope':'NON_MPI_NAMESPACE_COMPONENT','memory_max':64<<20,'swap_max':0,
         'tasks_max':4,'wall_seconds':8,'binary':str(BINARY),'binary_sha256':sha(BINARY),'case':case}
    job={'unit':'r07-owned-'+uuid.uuid4().hex+'.service','case':case,'root':str(root),'socket':endpoint,
         'host_cookie':host[0],'profile_sha256':digest(profile),'version':1}
    atomic_json(root/'JOB.json',job);atomic_json(root/'PROFILE.json',profile)
    lock=os.open(LOCK,os.O_RDWR|os.O_CLOEXEC|os.O_NOFOLLOW);fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    ls=os.fstat(lock);owner=proc(os.getpid());listener=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
    listener.bind(endpoint);listener.listen(1);listener.setblocking(False)
    client=None;peer=None;ident=None;cg=None;invocation=None;sampled=[];out=bytearray();hello=None;received=[]
    started=time.monotonic();last_sample=None;max_interval=0;image_error=None
    result={'kind':'NON_MPI_FRESH_SOCKET_COOKIE_PATHNAME_COMPONENT','job':job,'profile':profile,
            'owner':owner,'host_fresh_before':host,'native_MPI_QE_HSE_executed':False,'hostwide_exclusion':'UNPASSED',
            'passed':False,'reason':'uncompleted','command':launch_command(job,owner,ls)}
    atomic_json(root/'INTENT.json',result);guard=LinuxGuard(LIB)
    try:
        info=guard.probe(root)
        if info['probe_errno'] or info['fs_type']!=0xef53 or info['project_error']:raise Refusal('supported ext4/project probe')
        for quota in info['quotas']:
            headroom=quota_headroom(quota)
            if headroom is not None and headroom<(1<<20)+4096:raise Refusal('known quota lacks bounded extent/output headroom')
        if info['available_bytes']<10*(1<<30)+(1<<20) or memory()['MemAvailable']<4*(1<<30)+(64<<20):raise Refusal('preflight floors+owned margin')
        fd=os.open(root/'reserved.extent',os.O_CREAT|os.O_EXCL|os.O_RDWR|os.O_NOFOLLOW,0o600)
        try:
            for quota in guard.probe_fd(fd)['quotas']:
                headroom=quota_headroom(quota)
                if headroom is not None and headroom<(1<<20)+4096:raise Refusal('actual inode quota lacks headroom')
            allocated=ctypes.c_int64();code=guard.lib.qe_reserve_fd(fd,4096,ctypes.byref(allocated))
            if code or os.fstat(fd).st_size!=4096 or allocated.value<4096:raise Refusal('actual byte/block reservation')
            result['reservation']={'requested':4096,'allocated':allocated.value,'inode':os.fstat(fd).st_ino}
        finally:os.close(fd)
        if show(job['unit'])['LoadState']!='not-found':raise Refusal('unit collision')
        client=subprocess.Popen(launch_command(job,owner,ls),env=manager_env(),stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True)
        os.set_blocking(client.stdout.fileno(),False)
        selector=selectors.DefaultSelector();selector.register(listener,selectors.EVENT_READ);selector.register(client.stdout,selectors.EVENT_READ)
        while True:
            now=time.monotonic()
            if now-started>10:raise Refusal('foreground wall+cleanup cap')
            mem=memory()['MemAvailable'];disk=guard.probe(root)['available_bytes']
            if mem<4*(1<<30) or disk<10*(1<<30):raise Refusal('independent host pressure floor')
            if last_sample is not None:max_interval=max(max_interval,now-last_sample)
            last_sample=now
            sample={'elapsed':now-started,'MemAvailable':mem,'disk_free':disk,'owner_RSS':proc(os.getpid())['rss_bytes']}
            if cg and cg.exists():
                k=counters(cg);rows=members(cg);sample['kernel']=k;sample['members']=rows
                if k['memory_max']!='67108864' or k['swap_max']!='0' or k['tasks_max']!='4':raise Refusal('changed kernel limits')
                if sum(r['rss_bytes'] for r in rows.values())+sample['owner_RSS']>12*(1<<30):raise Refusal('family summed RSS guard')
            sampled.append(sample);sampled=sampled[-128:]
            for key,_ in selector.select(.01):
                if key.fileobj is listener:
                    if peer is not None:raise Refusal('second peer')
                    peer,_=listener.accept();peer.settimeout(.5)
                    pid,uid,_=struct.unpack('3i',peer.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
                    if uid!=1001:raise Refusal('kernel peer UID')
                    ident=Identity(pid);raw=peer.recv(4097)
                    if len(raw)>4096:raise Refusal('HELLO cap')
                    hello=json.loads(raw);fields=live_fields(job['unit']);invocation=fields['InvocationID']
                    cg=cgroup_path(own_cgroup(pid));kernel=counters(cg)
                    result.update(hello=hello,peer=ident.record(),manager_live=fields,cgroup_inode=cg.stat().st_ino,
                                  accepted_endpoint_cookie=socket_cookie(peer),kernel_at_hello=kernel)
                    try:
                        executable=Path(os.readlink(f'/proc/{pid}/exe')).resolve()
                        if executable!=BINARY or sha(executable)!=build['binary_sha256']:raise Refusal('actual peer image mismatch')
                        result['parent_image_path_verified']=True
                    except PermissionError as exc:
                        image_error=exc.errno;result['parent_image_path_errno']=exc.errno
                    validate_observation(hello,job,pid,fields,kernel)
                    if flock_owner(LOCK)!=[os.getpid()]:raise Refusal('kernel lease holder mismatch')
                    during=fresh_host_cookies();result['host_fresh_during']=during
                    if during!=host:raise Refusal('host namespace changed')
                    if case=='owner_disconnect':
                        peer.close();peer=None
                    else:
                        nonce=hello['nonce'] if case=='normal' else ('0' if hello['nonce'][0]!='0' else '1')+hello['nonce'][1:]
                        grant=f"GRANT|1|{digest(job)}|{job['profile_sha256']}|{nonce}|{hello['cookies'][0]}|{host[0]}|NON_MPI_NAMESPACE_COMPONENT"
                        peer.sendmsg([grant.encode()],[(socket.SOL_SOCKET,socket.SCM_RIGHTS,struct.pack('i',lock))])
                else:
                    data=os.read(client.stdout.fileno(),4096)
                    if data:out.extend(data)
                    else:selector.unregister(client.stdout)
                    if len(out)>32768:raise Refusal('exact log cap')
            if client.poll() is not None:
                while True:
                    data=os.read(client.stdout.fileno(),4096)
                    if not data:break
                    out.extend(data)
                    if len(out)>32768:raise Refusal('exact log cap')
                break
        events=[json.loads(line) for line in out.decode().splitlines() if line.startswith('{')]
        result['events']=events;result['exit_status']=client.returncode
        expected=(client.returncode==0 and any(e.get('event')=='DONE' for e in events)) if case=='normal' else (
            client.returncode==94 and any(e.get('step')==('grant_binding' if case=='bad_nonce' else 'owner_eof') for e in events))
        result['component_conditions_passed']=expected and hello is not None
        result['image_binding_complete']=image_error is None
        # Retain refusal for unreadable parent image even if cookies/IPC worked.
        result['passed']=expected and hello is not None and image_error is None
        result['reason']='PASS' if result['passed'] else ('parent image permission incomplete' if image_error else 'native probe/receipt mismatch')
    except BaseException as exc:
        result['reason']=type(exc).__name__+': '+str(exc)
    finally:
        if peer:peer.close()
        listener.close()
        fields=show(job['unit'])
        if invocation and fields.get('InvocationID') not in ['',invocation]:raise Refusal('cleanup invocation mismatch')
        if fields.get('ActiveState') in ['active','activating','deactivating']:ctl(job['unit'],'stop')
        if client:client.wait(timeout=3)
        if client:
            while True:
                data=os.read(client.stdout.fileno(),4096)
                if not data:break
                out.extend(data)
                if len(out)>32768:raise Refusal('final exact log cap')
        if 'events' not in result:
            result['events']=[json.loads(line) for line in out.decode(errors='replace').splitlines() if line.startswith('{')]
        terminal=show(job['unit']);result['terminal_manager']=terminal
        if terminal.get('MainPID','0')!='0':raise Refusal('owned service still active')
        if cg and cg.exists() and counters(cg)['cgroup_events']['populated']:raise Refusal('owned cgroup populated')
        if ident and ident.live():raise Refusal('witnessed peer not retired')
        if terminal.get('ActiveState')=='failed':ctl(job['unit'],'reset-failed')
        result.update(unit_unloaded=show(job['unit'])['LoadState']=='not-found',legacy_byte_exact=REGISTRY.read_bytes()==legacy,
                      stdout=out.decode(errors='replace'),samples=sampled,max_host_sample_interval=max_interval,
                      elapsed_seconds=time.monotonic()-started,host_fresh_after=fresh_host_cookies())
        # Check retention of flock after the entire peer/unit has retired.
        other=os.open(LOCK,os.O_RDWR|os.O_CLOEXEC|os.O_NOFOLLOW)
        try:
            try:fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB);result['flock_retained_after_peer']=False
            except BlockingIOError:result['flock_retained_after_peer']=True
        finally:os.close(other)
        if not result['unit_unloaded'] or not result['legacy_byte_exact'] or result['host_fresh_after']!=host or not result['flock_retained_after_peer']:
            result['passed']=False;result['reason']='closure/reference/lease mismatch'
        atomic_json(root/'RESULT.json',result)
        atomic_json(PRIVATE/(case+'_result.json'),result)
        if ident:ident.close()
        os.close(lock)
    return result


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('fixed case required')
    result=run(sys.argv[1]);print(json.dumps({k:result.get(k) for k in ['passed','reason','job','hello','exit_status','unit_unloaded','elapsed_seconds']},indent=2))
    raise SystemExit(0 if result['passed'] else 2)
