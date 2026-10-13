"""Generate canonical fixed Fock inputs from the genuine control, read-only.
No fitted physics. Exact IEEE weight reconstruction in this actual fixture.
"""
import hashlib,json,os,struct,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'native_pair_2026-10-13'))
from compare_pair import decode
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011')
CONTROL=ROOT/'first_ace_sampled_v6_20261013/control'
PRIVATE=ROOT/'fixed_operator_20261013'
MAGIC=b'QE75-FIXED-01   ';END=b'QE75-FIXED-END  '

def create():
    PRIVATE.mkdir(mode=0o700,exist_ok=False);r=PRIVATE/'canonical';r.mkdir(mode=0o700)
    files={str(p.relative_to(CONTROL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((CONTROL/'diag').glob('*.before'))}
    if len(files)!=6:raise ValueError('incomplete actual control')
    identity=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
    wk=np.array([.125,.5,.375],dtype='=f8');records=[]
    for rank in [0,1]:
        old=[]
        for k in [1,2,3]:old.append(decode(CONTROL/'diag'/f'rank{rank}.k{k}.before'))
        occ=old[0]['occupation'];assert occ.shape==(48,3)
        assert all(np.array_equal(occ.view('=u8'),d['occupation'].view('=u8')) for d in old)
        assert np.all((occ[:,1:]==0)|(occ[:,1:]==1))
        wg=occ*wk[None,:]
        assert np.array_equal((wg/wk).view('=u8'),occ.view('=u8'))
        # Partial entries only at exact power-of-two weight, with normal range;
        # for 3/8 all zeros/ones have a unique double preimage under division.
        partial=occ[:,0][(occ[:,0]!=0)&(occ[:,0]!=1)]
        assert np.all((partial>.1)&(partial<.9))
        for k,d in enumerate(old,1):
            _,_,_,_,padded,active,spin,bands,_=d['header'];layout=d['layout']
            phi=np.zeros((padded*spin,bands),dtype='=c16',order='F');probe=np.zeros((padded*spin,1),dtype='=c16',order='F')
            indices=np.r_[np.arange(active),padded+np.arange(active)]
            phi[indices]=d['phi'];probe[indices]=d['probe']
            payload=MAGIC+struct.pack('=8q',rank,k,padded,active,spin,bands,3,len(layout))+identity.encode()
            for a in [layout,d['global_g'],phi,occ,wg,wk,probe]:payload+=np.asarray(a).tobytes(order='F')
            payload+=END
            f=r/f'rank{rank}.k{k}.input';f.write_bytes(payload);f.chmod(0o444)
            records.append(dict(rank=rank,k=k,path=str(f),sha256=hashlib.sha256(payload).hexdigest(),bytes=len(payload)))
    evidence=dict(canonical_identity=identity,records=records,control_before_files_sha256=files,
                  wk=wk.tolist(),exact_weight_reconstruction=True,partial_weight_only_dyadic=True,
                  new_domain='fixed Fock inputs; original full-state refusal preserved',
                  old_control_setup_tables_not_captured=True)
    (HERE/'canonical.json').write_text(json.dumps(evidence,indent=2)+'\n');return evidence
if __name__=='__main__':print(json.dumps(create(),indent=2))
