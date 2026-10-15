"""Independent geometry and native spectral-contraction checks, no QE launch."""
from pathlib import Path
from xml.etree import ElementTree as ET
import itertools,json
import numpy as np
import owner as r

HERE=Path(__file__).resolve().parent


def main():
    geo=json.loads((HERE/'geometry_result.json').read_text());Q=np.array(geo['cell_repeat']);xyz=np.array(geo['cation_fractional']);allxyz=np.r_[xyz,xyz+.125];shifts=np.array(list(itertools.product([-1,0,1],repeat=3)))
    geometry={}
    for m,indices in [('unshared',[0,7]),('shared',[0,1])]:
        counts=[]
        for te in allxyz[8:]:
            dis=np.linalg.norm(((xyz[:,None,:]+shifts[None,:,:]-te)@Q).reshape(-1,3),axis=1)
            order=np.argsort(dis);assert np.ptp(dis[order[:4]])<1e-12 and dis[order[4]]>dis[order[3]]+1e-3
            counts.append(sum((int(j)//len(shifts)) in indices for j in order[:4]))
        assert counts==geo['members'][m]['Te_N_counts']
        # Independent ALL48 signed permutations, without prior Td generator list.
        syms=['Cd' if i in indices else 'Hg' for i in range(8)]+['Te']*8
        keys=lambda pos:{(s,tuple(np.rint(x*8).astype(int)%8)) for s,x in zip(syms,pos)}
        rotations=[];affine=0
        for perm in itertools.permutations(range(3)):
            for signs in itertools.product([-1,1],repeat=3):
                R=np.eye(3)[list(perm)]*np.array(signs)[:,None];S=np.linalg.inv(Q.T)@R@Q.T
                good=sum(keys(allxyz@S.T+shift)==keys(allxyz) for shift in xyz)
                if good:rotations.append(R.astype(int).tolist());affine+=good
        assert {tuple(np.ravel(x)) for x in rotations}=={tuple(np.ravel(x)) for x in geo['members'][m]['point_rotations']}
        assert affine==len(geo['members'][m]['affine_operations'])
        geometry[m]=dict(independent_nearest4_histogram={str(n):counts.count(n) for n in range(5)},all48_signed_permutations_linear_order=len(rotations),affine_order=affine)
    result=json.loads((HERE/'numerical_result.json').read_text());v=np.load(HERE/'complex_overlaps.npz');independent={};mat={}
    for m in ['unshared','shared']:
        r.load(m);root=r.PAIR/m;t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml');e=np.fromstring(t.findtext('.//output/band_structure/ks_energies/eigenvalues'),sep=' ')*27.211386245988;ef=float(t.findtext('.//output/band_structure/fermi_energy'))*27.211386245988
        branches={};Cs=[]
        for l,d in [('Gamma6',2),('Gamma8',4)]:
            C=v[m+'_'+l];Cs.append(C);w=np.array([np.vdot(C[:,j],C[:,j]).real/d for j in range(352)])
            saved=np.loadtxt(HERE/(m+'_'+l+'_spectrum.csv'),delimiter=',',skiprows=1);assert np.max(abs(w-saved[:,3]))<1e-15
            phi=np.exp(-.5*((e-ef)/2)**2);branches[l]=float(sum(w*phi*(e-ef))/sum(w*phi))
        independent[m]=branches['Gamma6']-branches['Gamma8'];C=np.vstack(Cs);z=.05j
        G=sum(np.outer(C[:,j],C[:,j].conj())/(z-(e[j]-ef)) for j in range(352));H=z*np.eye(6)-np.linalg.inv(G)
        mat[m]=float((np.trace(H[:2,:2])/2-np.trace(H[2:,2:])/4).real)
    delta=independent['shared']-independent['unshared'];assert abs(delta-result['primary_W2_eV'])<1e-12
    matrixdelta=mat['shared']-mat['unshared'];old=next(a for a in result['matrix_causal_rows'] if a['eta_eV']==.05);assert abs(matrixdelta-old['delta_eV'])<1e-11
    # Actual identical settings, with ONLY paths and substitution labels removed.
    decks=[]
    for m in ['unshared','shared']:
        root=r.PAIR/m;text=(root/'pw.in').read_text().replace(str(root),'ROOT');lines=text.splitlines();i=lines.index('ATOMIC_POSITIONS crystal')+1
        for j in range(8):lines[i+j]='Hg '+' '.join(lines[i+j].split()[1:])
        decks.append('\n'.join(lines))
    assert decks[0]==decks[1]
    out=dict(status='PASS independent real-data checks, not material validation',independent_geometry=geometry,independent_W2_delta_eV=delta,independent_matrix_eta05_delta_eV=matrixdelta,only_substitution_and_private_path_deck_difference=True,source_sha256=r.sha(Path(__file__)),physical_xc=None)
    (HERE/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
