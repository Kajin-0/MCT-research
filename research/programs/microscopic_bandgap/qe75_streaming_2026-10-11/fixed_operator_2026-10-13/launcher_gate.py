"""Fixed local first-ACE launcher: no arbitrary command, wait for live owner."""
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import sys

root=Path(sys.argv[1]).resolve()
allowed=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/fixed_operator_replay_v2_20261013')
if root.parent!=allowed or root.is_symlink():raise RuntimeError('owned fixed job root')
job=json.loads((root/'JOB_LAUNCH.json').read_text())
original=json.loads((root/'JOB.json').read_text())
for key in ['kind','command','launch_pins','root','profile_sha256','unit']:
    if job[key]!=original[key]:raise RuntimeError('fixed command/profile changed')
if job['kind']!='R07_LOCAL_QE_FIXED_FOCK_ONLY_V1':raise RuntimeError('fixture scope')
for name,digest in job['launch_pins'].items():
    if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest:raise RuntimeError('launch source/binary/input pin')
owner=json.loads((root/'OWNER.json').read_text())
if hashlib.sha256(json.dumps(original,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=owner['job_sha256']:
    raise RuntimeError('sealed original JOB digest')
with socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET) as s:
    s.settimeout(5);s.connect('\0'+owner['gate_socket'])
    pid,uid,_=struct.unpack('3i',s.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
    if uid!=os.getuid() or pid!=owner['pid']:raise RuntimeError('kernel owner peer')
    challenge=os.urandom(32).hex()
    s.send(json.dumps(dict(pid=os.getpid(),challenge=challenge,job=owner['job_sha256'])).encode())
    reply=json.loads(s.recv(4096))
    if reply!=dict(action='EXECUTE_PINNED_FIRST_ACE',challenge=challenge,job=owner['job_sha256']):
        raise RuntimeError('live owner launch refusal')
os.execve(job['command'][0],job['command'],job['environment'])
