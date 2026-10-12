"""Read-only actual QE save decoding + exact diagnostic codec checks. No QE run."""
from pathlib import Path
import hashlib
import json
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import h5py
import numpy as np
from binding import artifact_sha256,Refusal
from build import DFT,PRIVATE

REFERENCE=DFT/'calculations/r07/hgte_hse_sg15_k4_q2_e90_fullacc_c1e-10_t1800/out/r07.save'


def readback():
    rows=[]
    with tempfile.TemporaryDirectory(dir=PRIVATE,prefix='readback-') as tmp:
        for filename,kind in [('wfc1.hdf5','wave'),('ace1.hdf5','wave'),('charge-density.hdf5','density')]:
            source=REFERENCE/filename;sha=artifact_sha256(source);output=Path(tmp)/(filename+'.decoded')
            r=subprocess.run([str(PRIVATE/'hdf5_readback'),str(source),str(output),kind],
                             capture_output=True,text=True,timeout=20)
            if r.returncode or r.stderr.strip(): raise Refusal('serial native-HDF5 read failed '+r.stderr+r.stdout)
            with h5py.File(source,'r') as h5,output.open('rb') as f:
                npol,igwx,nbnd=struct.unpack('=3i',f.read(12));encoded=hashlib.sha256();decoded=hashlib.sha256()
                d=h5['evc' if kind=='wave' else 'rhotot_g']
                wanted_shape=(nbnd,2*npol*igwx) if kind=='wave' else (2*igwx,)
                if d.shape!=wanted_shape: raise Refusal('QE HDF5 column shape mismatch')
                for j in range(nbnd):
                    raw=f.read(16*npol*igwx)
                    expected=np.asarray(d[j,:] if kind=='wave' else d[:],dtype='=f8').tobytes()
                    if raw!=expected: raise Refusal('cross-language exact complex byte mismatch')
                    encoded.update(expected);decoded.update(raw)
                if f.read(1): raise Refusal('extended decoder output')
                attrs={k:(v.tolist() if hasattr(v,'tolist') else str(v)) for k,v in h5.attrs.items()}
                attrs={k:(v.decode() if isinstance(v,bytes) else v) for k,v in attrs.items()}
            if artifact_sha256(source)!=sha: raise Refusal('pre-existing input changed during readback')
            rows.append({'source':str(source),'source_sha256':sha,'kind':kind,'attrs':attrs,
                         'npol':npol,'igwx':igwx,'bands':nbnd,'complex_values_checked':npol*igwx*nbnd,
                         'HDF5_column_bytes_sha256':encoded.hexdigest(),'QE_qeh5_read_bytes_sha256':decoded.hexdigest(),
                         'bitwise_equal':True,'source_unchanged':True})
    schema=REFERENCE/'data-file-schema.xml';xml=ET.parse(schema).getroot()
    def value(tag):
        candidates=[node.text for node in xml.iter() if node.tag.split('}')[-1]==tag]
        return candidates
    return {'passed':True,'PW_MPI_HSE_executed':False,'MPI_initialization_trapped':True,
            'HDF5_transitive_MPI_library_loaded':True,'source':str(REFERENCE),'cases':rows,
            'native_schema_sha256':artifact_sha256(schema),'bands_in_schema':value('nbnd'),
            'ecutfock_Ha_in_schema':value('ecutfock'),'existing_reference_is_target_seed':False,
            'seed_refusal':'Existing 44-band/k4/Fock180Ry save is not the admitted 48-band/k2/Fock120Ry fixture. No seed relabelled or reused.',
            'boundary':'Serial pristine QE qeh5 decoding only; no actual MPI splitwf, XML/SCF restore or old-vs-current ACE restart qualification.'}


def decode_diag(path):
    raw=Path(path).read_bytes();pos=0
    def take(n):
        nonlocal pos
        result=raw[pos:pos+n];pos+=n
        if len(result)!=n: raise Refusal('truncated diagnostic')
        return result
    if take(16)!=b'QE75-ACE-DIAG01 ': raise Refusal('diagnostic magic')
    version,rank,k,stage,npwx,npw,npol,bands,nlayout=struct.unpack('=9q',take(72))
    if version!=1 or stage not in [1,2] or min(npwx,npw,npol,bands,nlayout)<1 or npw>npwx:
        raise Refusal('diagnostic version/stage/shape')
    if max(npwx*npol*bands,bands*bands,nlayout,npw)>2000000: raise Refusal('diagnostic bounded decoder limit')
    energy=struct.unpack('=d',take(8))[0]
    layout=np.frombuffer(take(8*nlayout),dtype='=i8').copy();globals_=np.frombuffer(take(8*npw),dtype='=i8').copy()
    rows=npwx*npol
    def complex_(n): return np.frombuffer(take(16*n),dtype='=c16').copy()
    result={'rank':rank,'k':k,'stage':stage,'rows':rows,'bands':bands,'energy':energy,'layout':layout,'global_g':globals_}
    if stage==1:
        n1,n2=struct.unpack('=2q',take(16))
        if min(n1,n2)<1 or n1*n2>2000000: raise Refusal('occupation extent')
        result['occupation']=np.frombuffer(take(8*n1*n2),dtype='=f8').copy().reshape((n1,n2),order='F')
        phi=np.empty((rows,bands),complex);vphi=phi.copy()
        for j in range(bands): phi[:,j]=complex_(rows);vphi[:,j]=complex_(rows)
        result.update(phi=phi,vphi=vphi,gram=complex_(bands*bands).reshape((bands,bands),order='F'),
                      probe=complex_(rows),action=complex_(rows))
    else:
        result.update(xi=complex_(rows*bands).reshape((rows,bands),order='F'),
                      factor=complex_(bands*bands).reshape((bands,bands),order='F'),action=complex_(rows))
    if pos!=len(raw): raise Refusal('extended diagnostic')
    for key,value in result.items():
        if isinstance(value,(np.ndarray,float)) and not np.all(np.isfinite(value)):
            raise Refusal('nonfinite diagnostic '+key)
    return result
