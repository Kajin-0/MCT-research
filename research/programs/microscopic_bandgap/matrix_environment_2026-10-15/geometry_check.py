"""Independent host affine-group orbit check; no native job or new physical data."""
from pathlib import Path
import hashlib,itertools,json
import numpy as np
from analyze import HERE,OLD


def main():
    if (HERE/'geometry_check.json').exists():raise FileExistsError('preserve first geometry check')
    p=OLD/'geometry_result.json';geo=json.loads(p.read_text());Q=np.array(geo['cell_repeat']);c=np.array(geo['cation_fractional']);pos=np.r_[c,c+.125];species=['Hg']*8+['Te']*8
    keys=lambda a:[(s,tuple(np.rint(x*8).astype(int)%8)) for s,x in zip(species,a)]
    original=set(keys(pos));cmap={tuple(np.rint(x*8).astype(int)%8):i for i,x in enumerate(c)};group=[]
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([-1,1],repeat=3):
            R=np.eye(3)[list(perm)]*np.array(signs)[:,None];S=np.linalg.inv(Q.T)@R@Q.T
            for shift in c:
                out=pos@S.T+shift
                if set(keys(out))==original:
                    mapping=[cmap[tuple(np.rint(x*8).astype(int)%8)] for x in out[:8]]
                    group.append((tuple(R.astype(int).ravel()),mapping))
    assert len(group)==192 and len({x[0] for x in group})==24
    configs=set(itertools.combinations(range(8),3));orbits=[]
    while configs:
        seed=min(configs);orb={tuple(sorted(m[i] for i in seed)) for _,m in group};assert orb<=configs
        configs-=orb;ns=[sum(i in seed for i in shell) for shell in geo['Te_nn_cation_indices']];orbits.append(dict(seed=list(seed),size=len(orb),histogram=[ns.count(n) for n in range(5)]))
    rows=[]
    for cd in [(0,1,2),(0,1,7)]:
        ns=[sum(i in cd for i in shell) for shell in geo['Te_nn_cation_indices']];stabilizers=[r for r,m in group if tuple(sorted(m[i] for i in cd))==cd]
        rows.append(dict(Cd_indices=list(cd),Te_N_counts=ns,histogram=[ns.count(n) for n in range(5)],chemical_point_group_order=len(set(stabilizers))))
    assert sorted(x['size'] for x in orbits)==[24,32]
    assert rows[0]['histogram']==[1,3,3,1,0] and rows[0]['chemical_point_group_order']==6
    assert rows[1]['histogram']==[0,4,4,0,0] and rows[1]['chemical_point_group_order']==8
    result=dict(status='PASS exact affine-orbit geometry; no native symmetry claim',host_affine_group_order=len(group),orbits=orbits,candidates=rows,new_native_jobs=0,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'geometry_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
