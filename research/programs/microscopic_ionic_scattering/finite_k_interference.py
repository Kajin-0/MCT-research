"""R08 bare ionic single-site Gamma-to-saved-k coupling feasibility.

Frozen xCd=.125 8 irreducible native HSE spinor states; no QE run.
Both local and relativistic nonlocal Hg/Cd operator terms in common PW basis.
All output is conditional/provisional; NOT a linewidth, scattering lifetime,
screened defect potential, or full-BZ sampling.
"""
import json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from functools import lru_cache
import numpy as np,h5py
from scipy.integrate import simpson
from scipy.interpolate import PchipInterpolator
from scipy.special import spherical_jn,sph_harm_y

ROOT=Path("/home/User/opencode_workspace/DFT")
SRC=Path(__file__).resolve().parent
SAVE=ROOT/".local/r07_vca_x0125_hse_20261017/out/r07pk4.save"
UPF={
"Hg":ROOT/"calculations/r07/hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800/out/r07.save/Hg_sg15_pbe_fr_v12.UPF",
"Cd":ROOT/"calculations/r07/cdte_hse_sg15_k4_q2_e90_fullacc/out/r07.save/Cd_sg15_pbe_fr_v12.UPF"}
EV=13.605693122994
X=ET.parse(SAVE/"data-file-schema.xml").getroot().find("output")
cell=np.array([np.fromstring(X.findtext("atomic_structure/cell/"+n),sep=" ") for n in ("a1","a2","a3")])
omega=abs(np.linalg.det(cell))
atom=X.find("atomic_structure/atomic_positions/atom")
assert atom.attrib["name"]=="Hg" and max(abs(np.fromstring(atom.text,sep=" ")))<1e-12
energies=[2*EV*np.fromstring(x.findtext("eigenvalues"),sep=" ") for x in X.findall("band_structure/ks_energies")]
assert len(energies)==8 and all(len(e)==44 for e in energies)

def state(i):
    with h5py.File(SAVE/f"wfc{i}.hdf5") as f:
        g=f["MillerIndices"][:].astype(int)
        b=np.array([f["MillerIndices"].attrs["bg"+str(n)] for n in (1,2,3)])
        k=np.asarray(f.attrs["xk"],dtype=float)
        psi=np.ascontiguousarray(f["evc"][:]).view(np.complex128).reshape(44,2,len(g))
    assert g.max()<11 and g.min()>=-11
    assert abs(np.linalg.det(b))>0
    overlap=psi.reshape(44,-1).conj()@psi.reshape(44,-1).T
    assert np.max(abs(overlap-np.eye(44)))<1e-7
    return dict(g=g,b=b,k=k,psi=psi,pw=g@b+k[None,:],i=i,e=energies[i-1])
S=[state(i) for i in range(1,9)]
for s in S[1:]:
    assert np.max(abs(s["b"]-S[0]["b"]))<1e-12
assert np.linalg.norm(S[0]["k"])<1e-13
assert all(len(s["g"])>2600 for s in S)

def upf(path):
    r=ET.parse(path).getroot()
    rr=np.fromstring(r.findtext("PP_MESH/PP_R"),sep=" ")
    rab=np.fromstring(r.findtext("PP_MESH/PP_RAB"),sep=" ")
    loc=np.fromstring(r.findtext("PP_LOCAL"),sep=" ")
    betas=[z for z in r.find("PP_NONLOCAL") if z.tag.startswith("PP_BETA.")]
    js=[float(z.attrib["jjj"]) for z in r.find("PP_SPIN_ORB") if z.tag.startswith("PP_RELBETA")]
    D=np.fromstring(r.findtext("PP_NONLOCAL/PP_DIJ"),sep=" ").reshape(len(js),len(js))
    assert np.max(abs(D-np.diag(np.diag(D))))<1e-12
    assert len(betas)==len(js)
    projectors=[(int(z.attrib["angular_momentum"]),j,np.fromstring(z.text,sep=" "),float(D[i,i])) for i,(z,j) in enumerate(zip(betas,js))]
    return rr,rab,loc,projectors

rh,rabh,vh,hproj=upf(UPF["Hg"])
rc,rabc,vc,cproj=upf(UPF["Cd"])
vh_at_cd=np.interp(rc,rh,vh)
vh_at_cd[rc>rh[-1]]=-40/rc[rc>rh[-1]]
dv=vc-vh_at_cd
assert np.max(abs(dv[-80:]))<1e-5

def local_ft(q):
    res=np.zeros(len(q))
    for j in range(0,len(q),130):
        kk=q[j:j+130,None]
        res[j:j+130]=4*np.pi*simpson(
             (rc*rc*dv)[None,:]*np.sinc(kk*rc[None,:]/np.pi),x=rc,axis=1)
    return res

# Reuse a phase-aware FFT convolution; odd grid prevents Nyquist aliasing.
N=49
modes=np.fft.fftfreq(N)*N
h=np.stack(np.meshgrid(modes,modes,modes,indexing="ij"),axis=-1).reshape(-1,3)
assert N>2*max(abs(s["g"]).max() for s in S)+1
B=S[0]["b"]
def fft_states(s,selected):
    out=np.zeros((len(selected),2,N,N,N),dtype=np.complex128)
    psi=s["psi"][selected]
    for j,v in enumerate(s["g"]):
        out[:,:,v[0]%N,v[1]%N,v[2]%N]=psi[:,:,j]
    return np.fft.ifftn(out,axes=(-3,-2,-1))*np.sqrt(N**3)

def local_mat(initial,final,initial_idxs,final_idxs):
    # <final(kf)|Vloc|initial(ki)>: q=(ki-kf)+(Gi-Gf).
    shifted=initial["k"]-final["k"]
    Q=np.linalg.norm(h@B+shifted[None,:],axis=1)
    xx=np.arange(0,float(Q.max())+.1,.01)
    kern=PchipInterpolator(xx,local_ft(xx))(Q).reshape((N,)*3)/omega
    real=np.fft.ifftn(kern)*N**3
    ci=fft_states(initial,initial_idxs)
    cf=fft_states(final,final_idxs)
    return np.einsum("nsijk,ijk,msijk->nm",cf.conj(),real,ci,optimize=True)

def angular(l,j,m,theta,phi):
    v=np.zeros((2,len(theta)),complex);den=2*l+1
    if abs(j-l-.5)<1e-7:
        if -l<=m<=l:v[0]=np.sqrt((l+m+1)/den)*sph_harm_y(l,m,theta,phi)
        if -l<=m+1<=l:v[1]=np.sqrt((l-m)/den)*sph_harm_y(l,m+1,theta,phi)
    else:
        if -l<=m-1<=l:v[0]=np.sqrt((l-m+1)/den)*sph_harm_y(l,m-1,theta,phi)
        if -l<=m<=l:v[1]=-np.sqrt((l+m)/den)*sph_harm_y(l,m,theta,phi)
    return v

def overlap_betas(state,proj,radial_r):
    xyz=state["pw"];q=np.linalg.norm(xyz,axis=1)
    theta=np.zeros_like(q);phi=np.zeros_like(q);valid=q>1e-12
    theta[valid]=np.arccos(np.clip(xyz[valid,2]/q[valid],-1,1))
    phi[valid]=np.arctan2(xyz[valid,1],xyz[valid,0])
    amp=[];dion=[]
    for l,j,beta,d in proj:
        radial=np.empty(len(q))
        for i in range(0,len(q),150):
            qi=q[i:i+150,None]
            radial[i:i+150]=4*np.pi/np.sqrt(omega)*simpson(
                beta[None,:]*spherical_jn(l,qi*radial_r[None,:])*radial_r[None,:],
                x=radial_r,axis=1)
        ms=range(-l-1,l+1) if abs(j-l-.5)<1e-7 else range(-l+1,l+1)
        for m in ms:
            w=(-1j)**l*radial[None,:]*angular(l,j,m,theta,phi)
            amp.append(np.einsum("nsg,sg->n",state["psi"].conj(),w,optimize=True))
            dion.append(d)
    return np.array(amp).T,np.array(dion)

gamma=S[0];idx=np.arange(32,38)
# Cache initial projector contractions; kpoint final contractions independent.
AiHg,diHg=overlap_betas(gamma,hproj,rh)
AiCd,diCd=overlap_betas(gamma,cproj,rc)
def nonlocal_mat(k):
    Ah,_=overlap_betas(k,hproj,rh)
    Ac,_=overlap_betas(k,cproj,rc)
    return (Ac*diCd)@AiCd[idx].conj().T - (Ah*diHg)@AiHg[idx].conj().T

saved_loc=json.loads((SRC/"bare_local_gamma_result.json").read_text())
saved_nl=json.loads((SRC/"nonlocal_gamma_provisional.json").read_text())
def mat(x):
    a=np.asarray(x,dtype=float)
    return a[:,:,0]+1j*a[:,:,1]
L00=local_mat(gamma,gamma,idx,idx)*EV
N00=nonlocal_mat(gamma)[idx,:]*EV
assert np.max(abs(L00-mat(saved_loc["matrix_eV"])))<1e-7
assert np.max(abs(N00-mat(saved_nl["nonlocal_delta_matrix"])))<1e-7
assert np.max(abs(L00-L00.conj().T))<1e-10
assert np.max(abs(N00-N00.conj().T))<1e-10
print("Gamma validation",np.max(abs(L00-mat(saved_loc["matrix_eV"]))),np.max(abs(N00-mat(saved_nl["nonlocal_delta_matrix"]))),flush=True)

out=[]
for s in S:
    fidx=np.arange(44)
    local=local_mat(gamma,s,idx,fidx)*EV
    nl=nonlocal_mat(s)*EV
    full=local+nl
    assert np.all(np.isfinite(full))
    if s["i"]==1:
        assert np.max(abs(full[idx]-(L00+N00)))<1e-8
    result={"k_index":s["i"],"k_cart_bohr_inv":s["k"].tolist(),
        "k_cart_norm_bohr_inv":float(np.linalg.norm(s["k"])),
        "reported_bands":44}
    for name,cols,target in (("Gamma6_like",slice(0,2),np.mean(gamma["e"][32:34])),
                              ("Gamma8_like",slice(2,6),np.mean(gamma["e"][34:38]))):
        a=full[:,cols];al=local[:,cols];an=nl[:,cols]
        strength=np.sum(abs(a)**2,axis=1)
        sl=np.sum(abs(al)**2,axis=1)
        sn=np.sum(abs(an)**2,axis=1)
        interference=strength-sl-sn
        assert np.max(abs(strength-sl-sn-2*np.real(np.sum(al.conj()*an,axis=1))))<1e-10
        result[name+"_energy_resolved"]=[{"final_band_1based":int(j+1),"delta_E_eV":float(s["e"][j]-target),"local_eV2_per_initial":float(sl[j]/a.shape[1]),"nonlocal_eV2_per_initial":float(sn[j]/a.shape[1]),"interference_eV2_per_initial":float(interference[j]/a.shape[1]),"total_eV2_per_initial":float(strength[j]/a.shape[1])} for j in range(len(strength))]
        for v,arr in (("all_44_strength_eV2",strength),
                      ("all_44_local_strength_eV2",np.sum(abs(al)**2,axis=1)),
                      ("all_44_nonlocal_strength_eV2",np.sum(abs(an)**2,axis=1))):
            result[name+"_"+v]=float(arr.sum())
        for window in (.25,.50,1.0):
            eligible=np.where(abs(s["e"]-target)<=window)[0]
            key=name+f"_energy_window_{window:g}_eV"
            result[key]={"count":len(eligible),"bands_1based":(eligible+1).tolist(),
                         "strength_eV2":float(strength[eligible].sum()),
                         "mean_energy_eV":float(np.mean(s["e"][eligible])) if len(eligible) else None}
        chosen=np.argsort(strength)[-5:][::-1]
        result[name+"_top5"]=[{"band":int(j+1),"E_eV":float(s["e"][j]),
             "delta_E_from_initial_eV":float(s["e"][j]-target),
             "squared_matrix_eV2":float(strength[j]),
             "local_only_eV2":float(np.sum(abs(al[j])**2)),
             "nonlocal_only_eV2":float(np.sum(abs(an[j])**2))} for j in chosen]
    result["nearGamma_k_not_scattering_lifetime"]=True
    out.append(result)
    print("k",s["i"],"norm",round(result["k_cart_norm_bohr_inv"],4),
        "strength",round(result["Gamma6_like_all_44_strength_eV2"],4),
        round(result["Gamma8_like_all_44_strength_eV2"],4),
        "win0.5",round(result["Gamma6_like_energy_window_0.5_eV"]["strength_eV2"],5),
        round(result["Gamma8_like_energy_window_0.5_eV"]["strength_eV2"],5),flush=True)

# Reciprocity: independent reverse local phase and reverse nonlocal contractions.
for ix in (1,3):
    s=S[ix]
    m_fi=local_mat(gamma,s,idx,np.arange(44))*EV
    m_if=local_mat(s,gamma,np.arange(44),idx)*EV
    assert np.max(abs(m_fi-m_if.conj().T))<3e-10

result={"status":"BOUNDED_BARE_SINGLE_SITE_FINITE_K_MATRIX_ELEMENTS_PROVISIONAL",
        "phase_and_normalization":"One cation site at Cartesian origin; delta-k included in local Fourier kernel; nonlocal Bloch k+G projector factors. Cell-normalized matrix = single impurity periodic amplitude x Ncells; not a finite defect-normalized rate.",
        "numerical_validation":{"gamma_local_max_abs_eV":float(np.max(abs(L00-mat(saved_loc["matrix_eV"])))),
            "gamma_nonlocal_max_abs_eV":float(np.max(abs(N00-mat(saved_nl["nonlocal_delta_matrix"])))),
            "reciprocity_gamma_to_k3_k5_local_max_abs_eV":"passed below 3e-10",
            "fft_N":N,"local_radial_dq_bohr_inv":.01},
        "source_sha256":{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*UPF.values(),SAVE/"data-file-schema.xml"]},
        "kpoint_wavefunction_sha256":{str(s["i"]):hashlib.sha256((SAVE/f'wfc{s["i"]}.hdf5').read_bytes()).hexdigest() for s in S},
        "kpoint_records":out,
        "omissions":["bare unscreened ionic potential","only 8 irreducible k points","only 44 computed spinor bands","no full Brillouin-zone unfold/symmetry expansion","no group velocity or absolute cross section","zero excluded random-alloy correlations","strict 1e-8 symmetry gate still FAIL"]}
(SRC/"finite_k_energy_resolved_results.json").write_text(json.dumps(result,indent=2)+"\n")
