"""Exact initial-state observation, not a seed generator or native permission."""
from pathlib import Path
import hashlib
import json
import struct
import sys
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'m5_readiness'))
from binding import Refusal
from family_runtime import integer,multiply
from resource_guard import add


def decode(path):
    path=Path(path)
    if path.is_symlink() or not 208<=path.stat().st_size<=128*(1<<20): raise Refusal('initial bounded regular packet required')
    raw=path.read_bytes()
    if len(raw)<208 or raw[:16]!=b'QE75-INITIAL-01 ': raise Refusal('initial packet magic/truncation')
    h=list(struct.unpack('=13q',raw[16:120]))
    ver,rank,k,padded,active,spin,bands,nt,nr,ns,ng,layout,sentinel=h
    if ver!=1 or rank not in [0,1] or sentinel!=72623859790382856: raise Refusal('initial encoding/rank')
    for value in [k,padded,active,spin,bands,nt,nr,ns,ng,layout]:
        if integer(value)<1: raise Refusal('initial positive shape')
    if bands!=48 or spin!=2 or active>padded or nt>8 or ns not in [1,4]: raise Refusal('initial exact fixture shape')
    sizes=[multiply(8,layout),multiply(24,active),multiply(multiply(16,padded*spin),bands),
           multiply(multiply(16,bands),nt),multiply(multiply(16,nr),ns),multiply(multiply(16,ng),ns)]
    extent=208
    for size in sizes: extent=add(extent,size)
    if extent!=len(raw): raise Refusal('initial exact extent')
    fingerprint=raw[120:184].decode('ascii')
    if len(fingerprint)!=64 or any(c not in '0123456789abcdef' for c in fingerprint): raise Refusal('initial fingerprint')
    kp=np.frombuffer(raw[184:208],dtype='=f8')
    offset=208+sizes[0];mill=np.frombuffer(raw[offset:offset+sizes[1]],dtype='=i8').reshape((3,active),order='F')
    if len({tuple(row) for row in mill.T})!=active: raise Refusal('duplicated initial reciprocal rows')
    offset+=sizes[1]
    wave=np.frombuffer(raw[offset:offset+sizes[2]],dtype='=c16').reshape((padded*spin,bands),order='F')
    for s in range(spin):
        if np.any(wave[s*padded+active:(s+1)*padded]): raise Refusal('nonzero padded initial rows')
    numeric=np.frombuffer(raw[184:208],dtype='=f8')
    if not np.all(np.isfinite(numeric)) or not np.all(np.isfinite(wave)): raise Refusal('nonfinite initial state')
    # Compare every remaining density/potential/et/wg payload byte as well;
    # their mixed field ordering is native-column-wise and intentionally fixed.
    tail=np.frombuffer(raw[offset+sizes[2]:],dtype='=f8')
    if not np.all(np.isfinite(tail)): raise Refusal('nonfinite initial auxiliary state')
    return {'header':h,'fingerprint':fingerprint,'kpoint':kp.tolist(),'mill':mill.tolist(),
            'payload_sha256':hashlib.sha256(raw[184:]).hexdigest(),'packet_sha256':hashlib.sha256(raw).hexdigest(),
            'bytes':len(raw),'bands':bands,'active_rows':active,'padded_rows':padded}


def compare(control,stream,expected_profile):
    a=decode(control);b=decode(stream)
    if a['fingerprint']!=expected_profile or b['fingerprint']!=expected_profile: raise Refusal('common PROFILE mismatch')
    if a!=b: raise Refusal('common initial state differs: phases, maps and all payload bytes must match')
    return {'passed':True,'observation':'EXACT_PACKET_EQUALITY','packet_sha256':a['packet_sha256'],
            'bands':48,'bytes':a['bytes'],'native_generation_or_MPI_verified':False}


def all_rank_certificate(control,stream,expected_profile,ks,gram_tolerance=1e-12):
    wanted={(rank,k) for rank in range(2) for k in ks}
    if set(control)!=wanted or set(stream)!=wanted: raise Refusal('complete two-rank/k initial coverage required')
    if not 0<gram_tolerance<=1e-10: raise Refusal('initial Gram tolerance must be explicitly tight')
    records=[];gram_errors=[]
    for key in sorted(wanted):
        for path in [control[key],stream[key]]:
            h=decode(path)['header']
            if tuple(h[1:3])!=key: raise Refusal('initial rank/k labelling mismatch')
        records.append({'rank':key[0],'k':key[1],**compare(control[key],stream[key],expected_profile)})
    for k in ks:
        seen=set();gram=np.zeros((48,48),dtype=np.complex128);points=[]
        for rank in range(2):
            path=control[(rank,k)];raw=Path(path).read_bytes();d=decode(path);h=d['header']
            local={tuple(row) for row in np.array(d['mill']).T}
            if seen.intersection(local): raise Refusal('duplicated reciprocal ownership across ranks')
            seen.update(local);points.append(d['kpoint'])
            offset=208+8*h[11]+24*h[4]
            wave=np.frombuffer(raw[offset:offset+16*h[3]*h[5]*48],dtype='=c16').reshape((h[3]*h[5],48),order='F')
            gram+=wave.conj().T@wave
        if points[0]!=points[1]: raise Refusal('rank k-point disagreement')
        error=float(np.max(np.abs(gram-np.eye(48))))
        if error>gram_tolerance: raise Refusal('initial full-band NC Gram condition failed')
        gram_errors.append(error)
    return {'version':1,'kind':'INITIAL_STATE_OBSERVATION_NOT_ADMISSION','records':records,
            'profile_sha256':expected_profile,'NC_Gram_errors':gram_errors,'Gram_tolerance':gram_tolerance,
            'certificate_sha256':hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest()}
