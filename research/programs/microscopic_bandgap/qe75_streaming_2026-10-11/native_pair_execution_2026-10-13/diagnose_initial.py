"""Read-only field-by-field analysis of the actual refused native state pair.
No phase rotation, tolerance acceptance, field omission or native execution.
"""
from pathlib import Path
import hashlib,json,struct
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011')
CONTROL=ROOT/'first_ace_sampled_v6_20261013/control'
STREAM=ROOT/'first_ace_stream_scope4_20261013/stream'

def diagnose():
    records=[]
    for rank in [0,1]:
        for k in [1,2,3]:
            paths=[root/'initial'/f'rank{rank}.k{k}.initial' for root in [CONTROL,STREAM]]
            if any(f.is_symlink() or not 208<=f.stat().st_size<=128*(1<<20) for f in paths):raise ValueError('unbounded packet')
            raw=[f.read_bytes() for f in paths]
            h=struct.unpack_from('=13q',raw[0],16)
            if h!=struct.unpack_from('=13q',raw[1],16):raise ValueError('shape mismatch')
            _,_,_,padded,active,spin,bands,nt,nr,ns,ng,layout,_=h
            pos=208;fields={}
            def check(name,n,dtype):
                nonlocal pos
                x,y=[v[pos:pos+n] for v in raw];xx,yy=[np.frombuffer(v,dtype=dtype) for v in [x,y]]
                fields[name]=dict(bytes=n,byte_identical=x==y,numeric_unequal=int(np.count_nonzero(xx!=yy)),
                    max_absolute_difference=float(np.max(np.abs(xx-yy))) if len(xx) else 0.,
                    control_max=float(np.max(np.abs(xx))) if len(xx) else 0.,stream_max=float(np.max(np.abs(yy))) if len(yy) else 0.)
                pos+=n
            fields['header_fingerprint_kpoint']=dict(byte_identical=raw[0][:208]==raw[1][:208])
            check('layout',8*layout,'=i8');check('Miller',24*active,'=i8');check('waves',16*padded*spin*bands,'=c16')
            for j in range(nt):check(f'et.k{j+1}',8*bands,'=f8');check(f'wg.k{j+1}',8*bands,'=f8')
            for j in range(ns):
                check(f'rho.real.spin{j+1}',8*nr,'=f8');check(f'rho.reciprocal.spin{j+1}',16*ng,'=c16');check(f'vrs.spin{j+1}',8*nr,'=f8')
            if pos!=len(raw[0]) or pos!=len(raw[1]):raise ValueError('extended/truncated state')
            records.append(dict(rank=rank,k=k,fields=fields,control_sha256=hashlib.sha256(raw[0]).hexdigest(),stream_sha256=hashlib.sha256(raw[1]).hexdigest()))
    return dict(actual_native_packets=True,passed=False,records=records,fields_not_ignored=True,
                no_phase_or_band_alignment=True,stream_EXX_not_constructed=True)

if __name__=='__main__':
    value=diagnose();(HERE/'initial_mismatch.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({name:max(r['fields'][name]['max_absolute_difference'] for r in value['records'])
                      for name in ['waves','rho.real.spin1','rho.reciprocal.spin1','vrs.spin1']},indent=2))
