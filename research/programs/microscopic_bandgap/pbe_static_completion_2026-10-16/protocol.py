"""Production native receipt/retirement path. No service or launcher on import."""
from pathlib import Path
import hashlib
import errno
import importlib.util
import json
import os
import socket
import stat
import struct
import sys
import time

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'qe75_streaming_2026-10-11'
for f in ['runtime_admission','checkpoint_phase','cgroup_owned_2026-10-13']:
    sys.path.insert(0,str(BASE/f))
spec=importlib.util.spec_from_file_location('_r07_static_kernel_peer',BASE/'terminal_owner_2026-10-14/retirement.py')
kernel=importlib.util.module_from_spec(spec);spec.loader.exec_module(kernel)
Peer,Refusal=kernel.Peer,kernel.Refusal
WIRE=struct.Struct('!4s4I64s64s32s32s32sQ')
REPLY=struct.Struct('!4s3I32s')
GIB=1<<30


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def durable(path,data):
    """Fresh evidence only; no overwrite/retrospective success publication."""
    payload=json.dumps(data,sort_keys=True,allow_nan=False).encode()+b'\n'
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        with os.fdopen(fd,'wb',closefd=False) as f:f.write(payload);f.flush();os.fsync(fd)
    finally:os.close(fd)
    directory=os.open(Path(path).parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(directory)
    finally:os.close(directory)


class Protocol:
    def __init__(self,root,job,profile,cgroup,invocation,reader,pre_ack):
        self.root=Path(root).resolve();self.job=job;self.profile=profile
        self.cgroup=cgroup;self.invocation=invocation;self.reader=reader;self.pre_ack=pre_ack
        self.peers={};self.waiting={};self.finals=set();self.refused=None
        self.begun=time.monotonic();self.deadline=None;self.packet_pins={};self.readback=None

    def fail(self,error):
        if self.refused is None:self.refused=str(error)
        raise Refusal(self.refused) from error if isinstance(error,Exception) else None

    def live(self):
        if self.refused is not None:raise Refusal('absorbing refusal: '+self.refused)

    def accept(self,conn):
        """Called by the actual owner loop; keeps both live connections held."""
        peer=None
        try:
            self.live();conn.settimeout(1)
            peer=Peer(conn,os.getuid(),self.cgroup)
            raw=conn.recv(WIRE.size+1,socket.MSG_TRUNC)
            if len(raw)!=WIRE.size:raise Refusal('native wire extent')
            magic,version,stage,rank,size,jh,ph,inv,nonce,challenge,extent=WIRE.unpack(raw)
            if (magic,version,size)!=(b'R07S',1,2) or stage not in [1,10] or rank not in [0,1]:
                raise Refusal('typed native domain')
            if (jh.decode(),ph.decode(),inv.decode(),nonce.decode())!=(
                self.job['job_sha256'],self.job['profile_sha256'],self.invocation,self.job['nonce']):
                raise Refusal('fresh invocation/JOB/PROFILE/nonce mismatch')
            if (stage,rank) in self.waiting or stage==1 and rank in self.peers:
                raise Refusal('duplicate rank/phase')
            peer.live_identity()
            exe=Path(f'/proc/{peer.pid}/exe').resolve(strict=True)
            argv=Path(f'/proc/{peer.pid}/cmdline').read_bytes().split(b'\0')[:-1]
            if (str(exe)!=self.profile['elf'] or sha(exe)!=self.profile['elf_sha256']
                or argv!=[os.fsencode(v) for v in self.job['argv'][str(rank)]]):
                raise Refusal('actual kernel ELF/argv mismatch')
            peer.live_identity()
            if stage==1:
                if extent or self.finals or self.deadline is not None:raise Refusal('premature/repeated begin')
                if peer.pid in [p.pid for p in self.peers.values()]:raise Refusal('one process claimed two ranks')
                self.peers[rank]=peer;peer=None
            else:
                if set(self.peers)!={0,1} or rank in self.finals or extent<=0 or extent>GIB:
                    raise Refusal('premature/invalid native final')
                registered=self.peers[rank];registered.live_identity()
                if (peer.pid,peer.start_ticks)!=(registered.pid,registered.start_ticks):
                    raise Refusal('final from different kernel process')
                path=self.root/'pilot'/f'H.rank{rank}'
                fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
                try:
                    s=os.fstat(fd)
                    if not stat.S_ISREG(s.st_mode) or s.st_uid!=os.getuid() or s.st_size!=extent:
                        raise Refusal('incomplete/foreign native packet')
                    # Native CLOSE succeeded before this receipt. Persist file;
                    # final reread/hash still required after all processes exit.
                    os.fsync(fd)
                    before=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
                    digest=sha(f'/proc/self/fd/{fd}')
                    s2=os.fstat(fd)
                    if before!=(s2.st_dev,s2.st_ino,s2.st_size,s2.st_mtime_ns,s2.st_ctime_ns):
                        raise Refusal('packet changed during receipt')
                    self.packet_pins[rank]=dict(path=str(path),sha256=digest,extent=extent,identity=before)
                finally:os.close(fd)
            self.waiting[(stage,rank)]=(conn,challenge)
            if all((stage,r) in self.waiting for r in [0,1]):
                for p in self.peers.values():p.live_identity()
                if stage==10:
                    self.readback=self.reader(self.root,self.profile,self.peers)
                    self.check_packets()
                    for p in self.peers.values():p.live_identity()
                    durable(self.root/'LIVE_FINAL.json',dict(invocation=self.invocation,
                        job=self.job['job_sha256'],profile=self.job['profile_sha256'],
                        ranks={str(r):dict(pid=p.pid,start_ticks=p.start_ticks) for r,p in self.peers.items()},
                        packets=self.packet_pins,readback=self.readback))
                    self.finals={0,1}
                self.pre_ack() # real owner resource gates, including after readback
                for r in [0,1]:
                    c,ch=self.waiting.pop((stage,r));c.sendall(REPLY.pack(b'R07S',1,0,16,ch));c.close()
        except Exception as e:
            conn.close();self.fail(e)
        finally:
            if peer is not None:peer.close()

    def check_packets(self):
        for pin in self.packet_pins.values():
            p=Path(pin['path']);s=p.lstat()
            if (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)!=tuple(pin['identity']) or sha(p)!=pin['sha256']:
                raise Refusal('packet lost/replaced/changed')

    def inventory_failure(self,pid,error):
        try:
            self.live()
            if not isinstance(error,(PermissionError,FileNotFoundError,ProcessLookupError)):
                raise Refusal('non-inventory failure cannot retire')
            peers=[p for p in self.peers.values() if p.pid==pid]
            if len(peers)!=1 or self.finals!={0,1}:raise Refusal('incomplete/unknown live final pair')
            if not peers[0].exited():raise Refusal('STILL LIVE FD denial: fatal')
            if self.deadline is None:self.deadline=min(self.begun+600,time.monotonic()+3)
        except Exception as e:self.fail(e)
        raise kernel.TerminalPending('kernel-proved exited rank; terminal conjunction still pending') from error

    def terminal(self,client,unit,cg_identity,account,resource_check):
        """Owner is OUTSIDE the MPI cgroup and retains actual rank pidfds."""
        try:
            self.live()
            if self.finals!={0,1} or not all(p.exited() for p in self.peers.values()):
                raise Refusal('lost/live rank, not terminal')
            if self.deadline is not None and time.monotonic()>=self.deadline:raise Refusal('3s pending deadline')
            f=kernel.show(unit)
            expected=dict(Id=unit,InvocationID=self.invocation,LoadState='loaded',ActiveState='inactive',
                SubState='dead',Result='success',ExecMainCode='1',ExecMainStatus='0',MainPID='0',Restart='no',Delegate='no')
            if client.poll()!=0 or any(f.get(k)!=v for k,v in expected.items()):raise Refusal('terminal manager/launcher mismatch')
            cg=kernel.cgroup_path(self.cgroup)
            if cg.exists():
                s=cg.stat()
                if (s.st_dev,s.st_ino)!=cg_identity:raise Refusal('cgroup replaced')
                if kernel.own_cgroup(os.getpid())==self.cgroup:raise Refusal('holder is not outside owned cgroup')
                if (cg/'cgroup.events').read_text().split()!=['populated','0','frozen','0']:
                    # Read parsed fields to tolerate kernel field order/additions.
                    fields=dict(line.split() for line in (cg/'cgroup.events').read_text().splitlines())
                    if fields.get('populated')!='0':raise Refusal('cgroup not empty')
                if (cg/'cgroup.procs').read_text().strip() or any(cg.glob('*/cgroup.procs')):
                    raise Refusal('cgroup tasks/descendants remain')
            resource_check();account.sample();self.check_packets()
            reread=self.reader(self.root,self.profile,self.peers)
            if reread!=self.readback:raise Refusal('post-exit source/readback changed')
            resource_check()
            if self.deadline is not None and time.monotonic()>=self.deadline:raise Refusal('3s terminal pending deadline')
            out=self.root/'pw.out'
            if not out.is_file() or not out.stat().st_size or out.stat().st_size>4*(1<<20):raise Refusal('lost/oversized log')
            text=out.read_text()
            if 'R07_STATIC_H_COMPLETE' not in text or 'JOB DONE.' not in text:raise Refusal('incomplete terminal log')
            # Log is an additional output requirement, never proof of task exit.
            return dict(terminal=True,invocation=self.invocation,manager=f,log_sha256=sha(out),
                actual_rank_pidfds_exited=True,packets=self.packet_pins,outside_holder=os.getpid())
        except Exception as e:self.fail(e)

    def close(self):
        for conn,_ in self.waiting.values():conn.close()
        for peer in self.peers.values():peer.close()
