"""Live kernel-authenticated lease RPC. JSON MONITOR files are never authority."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import sys
import time

from process_identity import Identity,flock_owner,Refusal
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'native_bridge'))


def request(root,action,rank=None,size=None,profile_sha256=None):
    root=Path(root)
    from checkpoint_capsule import read_meta,encode
    job=read_meta(root/'JOB.json');ticket=read_meta(root/'LEASE_ENDPOINT.json')
    if ticket['profile_sha256']!=hashlib.sha256(encode(job)).hexdigest():
        raise Refusal('runtime not qualified: profile/endpoint mismatch')
    if profile_sha256 is not None and profile_sha256!=ticket['profile_sha256']:
        raise Refusal('runtime not qualified: requested profile mismatch')
    sock=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
    sock.settimeout(1)
    try:
        sock.connect('\0'+ticket['abstract_socket'])
        pid,uid,gid=struct.unpack('3i',sock.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
        if uid!=os.getuid() or pid!=ticket['guardian']['pid']: raise Refusal('lease server kernel credentials mismatch')
        identity=Identity(pid)
        try:
            if identity.start_ticks!=ticket['guardian']['start_ticks'] or not identity.live():
                raise Refusal('lease guardian PID reused/dead')
            if flock_owner(Path(ticket['global_lock']))!=[pid]: raise Refusal('live kernel lease not owned by guardian')
            expected=str(Path(__file__).with_name('family_runtime.py'))
            command=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
            if len(command)<5 or os.fsdecode(command[1])!=expected or os.fsdecode(command[2])!='guardian' or os.fsdecode(command[3])!=str(root):
                raise Refusal('lease peer is not the registered guardian command')
            from native_bundle import artifact_sha256
            if job['files'].get(expected)!=artifact_sha256(Path(expected)):
                raise Refusal('guardian source fingerprint changed')
            payload={'action':action,'rank':rank,'size':size,'profile_sha256':ticket['profile_sha256'],
                     'challenge':os.urandom(32).hex()}
            sock.send(json.dumps(payload).encode())
            result=json.loads(sock.recv(65536))
            if result.get('challenge')!=payload['challenge']: raise Refusal('lease challenge not acknowledged')
            if not result.get('ok'): raise Refusal(result.get('reason','lease RPC refused'))
            if not 0<=time.monotonic()-result['monotonic']<=2: raise Refusal('stale live lease response')
            if not identity.live() or flock_owner(Path(ticket['global_lock']))!=[pid]:
                raise Refusal('lease lost during authorization')
            return result
        finally: identity.close()
    finally: sock.close()


def authorize_native_hook(root,profile_sha256,action,rank=None,size=None):
    from checkpoint_capsule import read_meta
    job=read_meta(Path(root)/'JOB.json')
    if job.get('kind')!='QEF_QE75_NATIVE_FIXTURE': raise Refusal('synthetic/unqualified runtime is not native authority')
    # A PROFILE is not a JOB. Bind its independently computed digest into the
    # versioned JOB; never require the two different objects to hash equally.
    sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'m5_readiness'))
    from binding import load_pair,native_admission
    identities=load_pair(root)
    if identities['profile_sha256']!=profile_sha256: raise Refusal('native PROFILE digest mismatch')
    if action!='authorize': raise Refusal('native hook action unregistered')
    # The new compiled transport can issue only component receipts until the
    # full native owner/state/common-wave/layout/inventory gate is qualified.
    # No Boolean, synthetic receipt or speculative JSON handler can bypass it.
    return native_admission()
