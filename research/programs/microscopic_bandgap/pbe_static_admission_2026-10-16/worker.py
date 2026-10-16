"""Tiny, self-expiring non-MPI peer for isolated owner-policy tests."""
import ctypes
import json
import select
import socket
import sys

path,rank,job,profile,nonce=sys.argv[1:]
rank=int(rank)


def receipt(action):
    s=socket.socket(socket.AF_UNIX);s.settimeout(3);s.connect(path)
    s.sendall(json.dumps(dict(version=1,rank=rank,action=action,job=job,profile=profile,nonce=nonce)).encode()+b'\n')
    if s.recv(32)!=b'OK\n':raise RuntimeError('receipt refused')
    s.close()


def command():
    if not select.select([sys.stdin],[],[],8)[0]:raise SystemExit(24)
    c=sys.stdin.readline().strip()
    if not c:raise SystemExit(25)
    return c


receipt(1)
if command()!='final':raise SystemExit(26)
receipt(10)
c=command()
if c=='deny':
    # Changes this disposable child's dumpability ONLY; no host permissions.
    if ctypes.CDLL(None).prctl(4,0,0,0,0):raise RuntimeError('PR_SET_DUMPABLE')
    print('DUMPABLE0',flush=True)
    c=command()
raise SystemExit(0 if c=='exit' else 3)
