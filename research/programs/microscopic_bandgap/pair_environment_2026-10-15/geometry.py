"""Independent periodic geometry, affine subgroup and host-frame specification."""
from pathlib import Path
import itertools,sys
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'native_matched_pilot_2026-10-11'))
from reference_irrep_check import td_operations
Q=np.ones((3,3),int)-np.eye(3,dtype=int)
HG=np.array(list(itertools.product([0.,.5],repeat=3)))
XYZ=np.r_[HG,HG+.125]
SPEC={'unshared':[0,7],'shared':[0,1]}


def symbols(member):return [('Cd' if i in SPEC[member] else 'Hg') if i<8 else 'Te' for i in range(16)]


def periodic_atoms(coords,syms):
    assert np.max(abs(coords*8-np.rint(coords*8)))<1e-10
    return {(s,tuple(v%8)) for s,v in zip(syms,np.rint(coords*8).astype(int))}


def compute():
    shell=[]
    for te in XYZ[8:]:
        nn=[]
        for i,hg in enumerate(HG):
            for shift in itertools.product([-1,0,1],repeat=3):
                d=(hg+shift-te)@Q
                if abs(d@d-3/16)<1e-12:nn.append(i)
        assert len(nn)==4;shell.append(nn)
    result={}
    for name,cd in SPEC.items():
        counts=[sum(i in cd for i in nn) for nn in shell]
        ops=[];linear=[]
        atoms=periodic_atoms(XYZ,symbols(name))
        for op in td_operations():
            R=op['spatial'];S=np.linalg.inv(Q.T)@R@Q.T
            assert np.max(abs(S-np.rint(S)))<1e-12
            good=[]
            for shift in HG:
                if periodic_atoms(XYZ@S.T+shift,symbols(name))==atoms:
                    good.append(shift.tolist());ops.append(dict(cartesian=R.tolist(),crystal=np.rint(S).astype(int).tolist(),translation=shift.tolist()))
            if good:linear.append(R.tolist())
        delta=HG[cd[1]]-HG[cd[0]]
        distances=[float(np.linalg.norm((delta+t)@Q)) for t in itertools.product([-2,-1,0,1,2],repeat=3)]
        result[name]=dict(Cd_indices_0based=cd,Te_N_counts=counts,histogram={str(n):counts.count(n) for n in range(5)},nearest_periodic_Cd_distance_over_a=min(distances),affine_operations=ops,point_rotations=linear,point_group_order=len(linear),translation_multiplicity=len(ops)//len(linear))
    assert result['unshared']['histogram']=={'0':0,'1':8,'2':0,'3':0,'4':0}
    assert result['shared']['histogram']=={'0':2,'1':4,'2':2,'3':0,'4':0}
    assert result['unshared']['point_group_order']==24 and result['shared']['point_group_order']==4
    assert abs(result['unshared']['nearest_periodic_Cd_distance_over_a']-1)<1e-12
    assert abs(result['shared']['nearest_periodic_Cd_distance_over_a']-1/np.sqrt(2))<1e-12
    assert all(v['translation_multiplicity']==2 for v in result.values())
    return dict(cell_repeat=Q.tolist(),cation_fractional=HG.tolist(),Te_nn_cation_indices=shell,members=result,periodic_not_dilute_pair=True,same_composition_cell_and_PP=True,not_geometrically_equivalent=True)
