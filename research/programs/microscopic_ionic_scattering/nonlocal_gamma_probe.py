"""R08 provisional independent UPF scalar+fully relativistic KB projector action.
Uses common QE plane-wave spinor Hilbert space; no native QE calculation.
Validation against QE's source/operator action is required before physical acceptance.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import hashlib,json
import numpy as np,h5py
from scipy.integrate import simpson
from scipy.integrate import simpson
from scipy.special import spherical_jn,sph_harm_y
ROOT=Path("/home/User/opencode_workspace/DFT")
BASE=ROOT/"calculations/r07"
pp={
"Hg":BASE/"hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800/out/r07.save/Hg_sg15_pbe_fr_v12.UPF",
"Cd":BASE/"cdte_hse_sg15_k4_q2_e90_fullacc/out/r07.save/Cd_sg15_pbe_fr_v12.UPF",
"VCA":ROOT/".local/r07_vca_x0125_hse_20261017/pp/VCA_HgCd_x0125.UPF"}
save=ROOT/".local/r07_vca_x0125_hse_20261017/out/r07pk4.save"
with h5py.File(save/"wfc1.hdf5") as f:
    gs=f["MillerIndices"][:]
    bg=np.array([f["MillerIndices"].attrs["bg"+str(i)] for i in (1,2,3)])
    c=np.ascontiguousarray(f["evc"][32:38]).view(np.complex128).reshape(6,2,len(gs))
xml=ET.parse(save/"data-file-schema.xml").getroot()
cell=np.array([np.fromstring(xml.findtext("output/atomic_structure/cell/"+s),sep=" ") for s in ("a1","a2","a3")])
omega=abs(np.linalg.det(cell))
gvec=gs@bg;q=np.linalg.norm(gvec,axis=1)
theta=np.zeros_like(q);phi=np.zeros_like(q);ok=q>1e-12
theta[ok]=np.arccos(np.clip(gvec[ok,2]/q[ok],-1,1))
phi[ok]=np.arctan2(gvec[ok,1],gvec[ok,0])
def inner(z):
    return np.einsum("nsg,sg->n",c.conj(),z,optimize=True)
def spinor(l,j,m):
    # m is integer index of QE spinor.f90: Jz=m+1/2 for j=l+1/2;
    # Jz=m-1/2 for j=l-1/2
    v=np.zeros((2,len(q)),dtype=complex)
    d=2*l+1
    if abs(j-l-.5)<1e-6:
        if -l<=m<=l:v[0]=np.sqrt((l+m+1)/d)*sph_harm_y(l,m,theta,phi)
        if -l<=m+1<=l:v[1]=np.sqrt((l-m)/d)*sph_harm_y(l,m+1,theta,phi)
    else:
        if -l<=m-1<=l:v[0]=np.sqrt((l-m+1)/d)*sph_harm_y(l,m-1,theta,phi)
        if -l<=m<=l:v[1]=-np.sqrt((l+m)/d)*sph_harm_y(l,m,theta,phi)
    return v
def load(path):
    root=ET.parse(path).getroot(); mesh=root.find("PP_MESH")
    r=np.fromstring(mesh.findtext("PP_R"),sep=" ")
    rab=np.fromstring(mesh.findtext("PP_RAB"),sep=" ")
    non=root.find("PP_NONLOCAL")
    nb=int(root.find("PP_HEADER").get("number_of_proj"))
    d=np.fromstring(non.findtext("PP_DIJ"),sep=" ").reshape(nb,nb)
    assert np.max(abs(d-np.diag(np.diag(d))))<1e-12
    angular=[float(e.get("jjj")) for e in root.find("PP_SPIN_ORB") if e.tag.startswith("PP_RELBETA")]
    betas=[e for e in non if e.tag.startswith("PP_BETA.")]
    assert len(angular)==len(betas)==nb
    rows=[]
    for i,(b,j) in enumerate(zip(betas,angular)):
        l=int(b.get("angular_momentum")); beta=np.fromstring(b.text,sep=" ")
        assert len(beta)==len(r)
        rows.append(dict(l=l,j=j,beta=beta,d=float(d[i,i])))
    return r,rab,rows
# radial: (4pi/sqrt(volume)) integral beta_i(r) j_l(qr) r dr
# UPF beta is stored as r*beta(r). QE init_tab_beta convention.
def radial(r,rab,beta,l):
    # independent direct nonuniform q samples; avoid relying on QE tab_beta interpolation.
    x=np.empty(len(q))
    for i in range(0,len(q),120):
        qq=q[i:i+120,None]
        bes=spherical_jn(l,qq*r[None,:])
        x[i:i+120]=(4*np.pi/np.sqrt(omega))*simpson(beta[None,:]*bes*r[None,:],x=r,axis=1)
    return x
def matrix(kind):
    r,rab,rows=load(pp[kind]);res=np.zeros((6,6),dtype=complex)
    cache={}
    for i,row in enumerate(rows):
        l=row["l"];j=row["j"]
        key=(l,j);cache.setdefault(key,[])
        cache[key].append(i)
    profiles=[radial(r,rab,x["beta"],x["l"]) for x in rows]
    for (l,j),indices in cache.items():
        if abs(j-l-.5)<1e-6:mr=range(-l-1,l+1)
        else:mr=range(-l+1,l+1)
        for m in mr:
            ang=spinor(l,j,m)
            for i in indices:
                w=(-1j)**l * profiles[i][None,:]*ang
                a=inner(w)
                # all parent UPF dion matrices diagonal here.
                res+=rows[i]["d"]*np.outer(a,a.conj())
    assert np.max(abs(res-res.conj().T))<1e-10
    return res
H=matrix("Hg");C=matrix("Cd");V=matrix("VCA")
mixed=.875*H+.125*C
delta=C-H
diff=V-mixed
E=13.605693122994
def metrics(m):
    a=m[:2,:2];b=m[2:,2:]
    return dict(G6_mean=float(np.trace(a).real/2*E),
                G8_mean=float(np.trace(b).real/4*E),
                sector_contrast=float((np.trace(a).real/2-np.trace(b).real/4)*E),
                cross_fro=float(np.linalg.norm(m[:2,2:])*E),
                hermiticity=float(np.max(abs(m-m.conj().T))*E))
out=dict(
 status="NUMERIC_PROVISIONAL_NEEDS_INDEPENDENT_QE_KB_VALIDATION",
 unit="eV", parent_Hg=metrics(H),parent_Cd=metrics(C),
 nonlocal_Cd_minus_Hg=metrics(delta),
 vca_nonlocal=metrics(V), weighted_parent_nonlocal=metrics(mixed),
 vca_identity_max_abs_eV=float(np.max(abs(diff))*E),
 vca_identity_fro_eV=float(np.linalg.norm(diff)*E),
 nonlocal_delta_matrix=[[[float(z.real*E),float(z.imag*E)] for z in row] for row in delta],
 notes=["Complex Ylm representation is convention-independent for diagonal spherical projectors when angular CG phases are consistent","Spherical Bessel integral discretized by Simpson over UPF radial mesh; independent QE operator validation outstanding","Not screened, self-consistent, random-alloy or finite-k calculation"],
 source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*pp.values(),save/"wfc1.hdf5",save/"data-file-schema.xml"]})
p=Path(__file__).with_name("nonlocal_gamma_provisional.json")
p.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if "matrix" not in k and k!="source_sha256"},indent=2))
