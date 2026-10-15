"""8-state/Kramers, Bernoulli-pair and continuum exponent checks; no material fit."""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.spatial.transform import Rotation

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
I2=np.eye(2,dtype=complex)
sig=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1.,-1.])]
L=[np.array([[0,0,0],[0,0,-1j],[0,1j,0]]),
   np.array([[0,0,1j],[0,0,0],[-1j,0,0]]),
   np.array([[0,-1j,0],[1j,0,0],[0,0,0]])]
S=sum(np.kron(a,b) for a,b in zip(L,sig))
P8=(S+2*np.eye(6))/3
P7=(np.eye(6)-S)/3
J=[np.kron(a,I2)+np.kron(np.eye(3),b)/2 for a,b in zip(L,sig)]
n=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/np.sqrt(3)
pairs=list(itertools.combinations(range(4),2))
pairvec=np.array([n[i]+n[j] for i,j in pairs])
norm=lambda a: float(np.linalg.norm(a,2))


def V(b):
    out=np.zeros((8,8),complex)
    out[:2,2:]=np.kron(np.asarray(b).reshape(1,3),I2)
    out[2:,:2]=out[:2,2:].conj().T
    return out


def HH(q):
    q=np.array(q,dtype=float);q/=np.linalg.norm(q)
    jq=sum(a*b for a,b in zip(q,J))
    return (jq@jq-.25*np.eye(6))/2


def main():
    assert norm(P8@P8-P8)<1e-14 and abs(np.trace(P8)-4)<1e-14
    assert norm(P7@P8)<1e-14
    spec=importlib.util.spec_from_file_location('r02_readonly',REPO/'tools/analyze_kane_symmetry_intertwiner.py')
    r02=importlib.util.module_from_spec(spec);spec.loader.exec_module(r02)
    basis8,basis7=r02.coupled_p_basis()
    r02_error=norm(P8-basis8@basis8.conj().T)
    assert r02_error<1e-14 and norm(P7-basis7@basis7.conj().T)<1e-14
    theta=np.kron(np.eye(4),1j*sig[1])
    assert norm(theta@theta.conj()+np.eye(8))<1e-14
    H0=np.zeros((8,8),complex);H0[:2,:2]=.3*I2
    H0[2:,2:]=-.2*P8-1.1*P7
    kval=np.array([.11,-.07,.15])
    H=H0+V(1j*kval)
    assert norm(theta@H.conj()@theta.conj().T-(H0+V(-1j*kval)))<1e-14
    rot_err=[];dis_err=[];site_interblock=norm(P8@V(n[0])[2:,:2])
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([-1,1],repeat=3):
            if np.prod(signs)!=1: continue
            R=np.diag(signs)@np.eye(3)[list(perm)]
            q=Rotation.from_matrix(np.linalg.det(R)*R).as_quat()
            spin=q[3]*I2-1j*sum(q[i]*sig[i] for i in range(3))
            U=np.zeros((8,8),complex);U[:2,:2]=spin;U[2:,2:]=np.kron(R,spin)
            rot_err.append(norm(U@H@U.conj().T-(H0+V(1j*(R@kval)))))
            dis_err.append(norm(U@V(n[0])@U.conj().T-V(R@n[0])))
    assert len(rot_err)==24 and max(rot_err+dis_err)<1e-12
    assert site_interblock>.1
    assert norm(theta@V(n[0]).conj()@theta.conj().T-V(n[0]))<1e-14
    pair_identity=norm(pairvec.T@pairvec-(8/3)*np.eye(3))
    assert pair_identity<1e-14
    rows=[]
    for x in [.125,.25,.5]:
        k=x*(1-x);mean=np.zeros(3);cov=np.zeros((3,3));cross=np.zeros((3,3));max_id=0.
        for occ in itertools.product([0,1],repeat=4):
            eta=np.array(occ);xi=eta-x
            w=x**sum(eta)*(1-x)**(4-sum(eta))
            b=sum((n[i]+n[j])*eta[i]*eta[j] for i,j in pairs)
            one=2*x*(xi@n)
            two=sum((n[i]+n[j])*xi[i]*xi[j] for i,j in pairs)
            max_id=max(max_id,norm((b-one-two).reshape(1,3)))
            mean+=w*b;cov+=w*np.outer(two,two);cross+=w*np.outer(one,two)
        assert np.linalg.norm(mean)<1e-14 and max_id<1e-14
        assert norm(cov-(8/3)*k*k*np.eye(3))<1e-14 and norm(cross)<1e-14
        hhw=[];dark=[];nonanalytic=[]
        for direction in [[0,0,1],[1,2,3],[1,-1,2]]:
            q=np.asarray(direction,float);q/=np.linalg.norm(q);ph=HH(q)
            assert norm(ph@ph-ph)<1e-14 and abs(np.trace(ph)-2)<1e-14
            weight=sum(k*k*np.trace(V(v)[:2,2:]@ph@V(v)[2:,:2]).real/2 for v in pairvec)
            hhw.append(weight)
            dark.append(norm(ph@V(1j*q)[2:,:2]))
            an=np.array([q[1]*q[2],q[2]*q[0],q[0]*q[1]])
            nonanalytic.append(norm(ph@V(an)[2:,:2])**2)
        assert max(abs(w-(8/3)*k*k) for w in hhw)<1e-14
        assert max(dark)<1e-14 and max(nonanalytic)>.01
        # Distinct centered pair fields on tetrahedra sharing only site0.
        white=np.zeros((3,3))
        for occ in itertools.product([0,1],repeat=7):
            occ=np.array(occ);xi=occ-x;w=x**sum(occ)*(1-x)**(7-sum(occ))
            b=[]
            for inds in [[0,1,2,3],[0,4,5,6]]:
                b.append(sum(pairvec[t]*xi[inds[i]]*xi[inds[j]] for t,(i,j) in enumerate(pairs)))
            white+=w*np.outer(*b)
        assert norm(white)<1e-14
        rows.append(dict(x=x,mean_vector_norm=float(np.linalg.norm(mean)),
            exact_centered_identity_error=max_id,pair_covariance_error=norm(cov-(8/3)*k*k*np.eye(3)),
            one_pair_cross_error=norm(cross),cross_tetra_pair_error=norm(white),
            Gamma6_to_HH_weights=hhw,predicted_pair_IR_weight=(8/3)*k*k,
            isotropic_longitudinal_dark_norms=dark,
            nonanalytic_transverse_weights=nonanalytic))
    # Two coarea exponents, cross-checked by independent volume quadrature.
    exponents=[]
    for eps in [.01,.04]:
        qmax=eps**.25
        volume=quad(lambda qz: np.pi*(eps-qz**4),-qmax,qmax,epsabs=1e-13)[0]
        exact=8*np.pi/5*eps**1.25
        assert abs(volume-exact)<1e-13
        exponents.append(dict(epsilon=eps,mixed_quadratic_quartic_volume=volume,
            exact_volume=exact,DOS_power=.25))
    z=.2+.07j;flat=[]
    for curvature in [.01,.001,.0001]:
        fun=lambda q:3*q*q/(z-curvature*q*q)
        value=quad(lambda q:fun(q).real,0,1)[0]+1j*quad(lambda q:fun(q).imag,0,1)[0]
        flat.append(dict(curvature=curvature,error_to_flat_kernel=float(abs(value-1/z))))
    assert flat[-1]['error_to_flat_kernel']<flat[0]['error_to_flat_kernel']
    out=dict(status='PASS',physical_xc=None,material_validation=False,native_jobs=0,
        R02_projector_equivalence_error=r02_error,Td_operation_count=len(rot_err),
        maximum_Kane_covariance_error=max(rot_err),maximum_local_vertex_covariance_error=max(dis_err),
        individual_site_inter_irrep_norm=site_interblock,pair_tensor_identity_error=pair_identity,
        Bernoulli_examples=rows,anisotropic_exponent_checks=exponents,flat_limit_checks=flat,
        exact_alloy_IR_exponent_claim=False)
    (HERE/'route_A_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
