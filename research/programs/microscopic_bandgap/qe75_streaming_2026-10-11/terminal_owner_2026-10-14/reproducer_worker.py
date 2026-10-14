"""Fixed two-child NON-MPI actor. Only its own dumpability is altered."""
import ctypes
import os
import socket
import subprocess
import sys


def connect(address):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    s.settimeout(6)
    s.connect('\0' + address)
    return s


def main():
    role, address, argument = sys.argv[1:]
    s = connect(address)
    s.send((role + ':' + argument).encode())
    if s.recv(128) != b'bound':
        raise RuntimeError('owner did not bind actual actor')
    if role == 'parent':
        children = [subprocess.Popen([sys.executable, __file__, 'rank', address, str(r)]) for r in (0, 1)]
        if s.recv(128) != b'reap':
            raise RuntimeError('bounded parent hold protocol')
        for p in children:
            if p.wait(timeout=3) != 0:
                raise RuntimeError('actor child failed')
        s.send(b'reaped')
        s.close()
        raise SystemExit(int(argument))
    if role != 'rank' or argument not in ('0', '1'):
        raise RuntimeError('actor allowlist')
    s.send(b'final')
    if s.recv(128) != b'final-accepted':
        raise RuntimeError('live final protocol')
    if argument == '0':
        lib = ctypes.CDLL(None, use_errno=True)
        if lib.prctl(4, 0, 0, 0, 0) != 0:  # PR_SET_DUMPABLE=0 on THIS actor only.
            raise OSError(ctypes.get_errno(), 'own dumpability fixture')
        s.send(b'live-fd-denial')
    else:
        s.send(b'live-normal')
    if s.recv(128) != b'exit':
        raise RuntimeError('actor exit protocol')
    s.close()


if __name__ == '__main__':
    main()
