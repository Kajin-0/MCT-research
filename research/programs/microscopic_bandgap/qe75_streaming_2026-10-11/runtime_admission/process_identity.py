"""Linux process identities. Numeric PID/PGID alone NEVER authorize a signal."""
from __future__ import annotations
import ctypes
import errno
import os
from pathlib import Path
import signal
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'checkpoint_phase'))
from checkpoint_capsule import Refusal


def proc(pid):
    raw=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
    return {'pid':int(pid),'state':raw[0],'ppid':int(raw[1]),'pgid':int(raw[2]),
            'sid':int(raw[3]),'start_ticks':int(raw[19]),'rss_bytes':int(raw[21])*os.sysconf('SC_PAGE_SIZE')}


def table():
    result={}
    for path in Path('/proc').iterdir():
        if not path.name.isdecimal(): continue
        try: result[int(path.name)]=proc(int(path.name))
        except (FileNotFoundError,ProcessLookupError): pass
        except PermissionError as exc: raise Refusal('process inventory unreadable') from exc
    return result


def descendants(root,entries):
    known={root};changed=True
    while changed:
        changed=False
        for pid,row in entries.items():
            if pid not in known and row['ppid'] in known:
                known.add(pid);changed=True
    return known-{root}


class Identity:
    def __init__(self,pid):
        first=proc(pid)
        self.fd=os.pidfd_open(pid,0)
        try:
            second=proc(pid)
            if first['start_ticks']!=second['start_ticks']: raise Refusal('PID reuse during acquisition')
            signal.pidfd_send_signal(self.fd,0)
        except BaseException:
            os.close(self.fd);raise
        self.pid=pid;self.start_ticks=first['start_ticks']

    def row(self):
        try:
            row=proc(self.pid)
            if row['start_ticks']!=self.start_ticks: return None # retired pidfd; never retarget a reused PID
            return row
        except (FileNotFoundError,ProcessLookupError): return None

    def live(self):
        row=self.row()
        return row is not None and row['state']!='Z'

    def send(self,number):
        # pidfd points to the acquired process even if its numeric PID is reused.
        if self.live():
            try: signal.pidfd_send_signal(self.fd,number)
            except ProcessLookupError: pass

    def close(self): os.close(self.fd)
    def record(self): return {'pid':self.pid,'start_ticks':self.start_ticks}


def pin_descendant(pid,root,entries):
    """Bind a snapshot lineage to pidfds; reject reuse/reparenting races.

    Child-subreaper ownership is irreversible for descendants after a witnessed
    valid chain. Snapshot numeric parent links alone are not signal authority.
    """
    identity=Identity(pid)
    try:
        seen=set();current=pid
        while current!=root:
            if current in seen or current not in entries: raise Refusal('lineage snapshot incomplete')
            seen.add(current);old=entries[current];now=proc(current)
            if (old['start_ticks'],old['ppid'])!=(now['start_ticks'],now['ppid']):
                raise Refusal('lineage changed during identity acquisition')
            current=now['ppid']
        if identity.start_ticks!=entries[pid]['start_ticks']: raise Refusal('descendant PID reused')
        return identity
    except BaseException:
        identity.close();raise


def subreaper():
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(36,1,0,0,0)!=0: raise OSError(ctypes.get_errno(),'PR_SET_CHILD_SUBREAPER')


def parent_death(number,expected_parent):
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(1,number,0,0,0)!=0: raise OSError(ctypes.get_errno(),'PR_SET_PDEATHSIG')
    if os.getppid()!=expected_parent: raise Refusal('parent died during death-signal setup')


def reap():
    records=[]
    while True:
        try: pid,status=os.waitpid(-1,os.WNOHANG)
        except ChildProcessError: break
        if pid==0: break
        records.append({'pid':pid,'status':status})
    return records


def mpi_inventory(require_global=False):
    names={'pw.x','mpiexec','mpirun','prterun','orterun','orted',
           'pw.qstream.UNVALIDATED','pw.bridge.RUNTIME_REFUSED','pw.control.M4_UNVALIDATED'}
    result=[]
    for pid,row in table().items():
        try:
            command=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
            if command and Path(os.fsdecode(command[0])).name in names and row['state']!='Z':
                result.append({**row,'argv0':os.fsdecode(command[0])})
            elif row['state']!='Z':
                # Catch renamed native binaries too. Loading an MPI backend is
                # conservative grounds for refusal, never signal authority.
                maps=Path(f'/proc/{pid}/maps').read_text()
                if any(('libmpi' in line or 'libmpich' in line) and '.so' in line for line in maps.splitlines()):
                    result.append({**row,'argv0':os.fsdecode(command[0]) if command else '',
                                   'reason':'MPI backend loaded'})
        except (FileNotFoundError,ProcessLookupError): pass
        except PermissionError as exc:
            # Unprivileged /proc/maps is unavailable for some other-UID system
            # processes. Fake-worker tests may inspect the readable namespace;
            # native admission must not infer global exclusivity from this.
            if require_global:
                raise Refusal('MPI inventory unreadable for PID '+str(pid)) from exc
    return result


def flock_owner(path):
    stamp=path.stat();wanted=(os.major(stamp.st_dev),os.minor(stamp.st_dev),stamp.st_ino)
    matches=[]
    for line in Path('/proc/locks').read_text().splitlines():
        words=line.split()
        if len(words)<6 or words[1]!='FLOCK' or words[3]!='WRITE': continue
        dev=words[5].split(':')
        if len(dev)==3 and (int(dev[0],16),int(dev[1],16),int(dev[2]))==wanted:
            matches.append(int(words[4]))
    return matches
