"""R08 local-only Hg->Cd bare ionic operator projected on saved x=.125 Gamma spinors.
Not a fully screened or fully relativistic defect-scattering operator. No QE run.
"""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from scipy.integrate import simpson
from scipy.interpolate import PchipInterpolator
import h5py

BASE=Path("/home/User/opencode_workspace/DFT/calculations/r07")
UPFS={
"Hg":BASE/"hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800/out/r07.save/Hg_sg15_pbe_fr_v12.UPF",
"Cd":BASE/"cdte_hse_sg15_k4_q2_e90_fullacc/out/r07.save/Cd_sg15_pbe_fr_v12.UPF"}
SAVE=Path("/home/User/opencode_workspace/DFT/.local/r07_vca_x0125_hse_20261017/out/r07pk4.save")
RY_TO_EV=13.605693122994
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def upf(path):
    root=ET.parse(path).getroot()
    rr=np.fromstring(root.findtext("PP_MESH/PP_R"),sep=" ")
    vv=np.fromstring(root.findtext("PP_LOCAL"),sep=" ")
    h=root.find("PP_HEADER").attrib
    assert h["pseudo_type"]=="NC" and h["relativistic"]=="full"
    assert h["has_so"]=="T" and float(h["z_valence"])==20
    assert len(rr)==len(vv)
    return rr,vv,h

rh,vh,hh=upf(UPFS["Hg"]);rc,vc,hc=upf(UPFS["Cd"])
assert np.max(abs(rh-np.arange(len(rh))*.01))<1e-9
assert np.max(abs(rc-np.arange(len(rc))*.01))<1e-9
hgatcd=np.interp(rc,rh,vh)
hgatcd[rc>rh[-1]]=-40/rc[rc>rh[-1]]
dv=vc-hgatcd
assert np.max(abs(dv[-80:]))<1e-5

with h5py.File(SAVE/"wfc1.hdf5") as f:
    g=f["MillerIndices"][:].astype(int)
    b=np.array([f["MillerIndices"].attrs["bg"+str(i)] for i in range(1,4)])
    wave=np.ascontiguousarray(f["evc"][32:38]).view(np.complex128).reshape(6,2,len(g))
    assert f.attrs["npol"]==2 and np.max(abs(f.attrs["xk"]))<1e-13
xml=ET.parse(SAVE/"data-file-schema.xml").getroot()
cell=np.array([np.fromstring(xml.findtext("output/atomic_structure/cell/"+s),sep=" ") for s in ("a1","a2","a3")])
volume=abs(np.linalg.det(cell))
basis_gram=wave.reshape(6,-1).conj()@wave.reshape(6,-1).T
assert np.linalg.norm(basis_gram-np.eye(6),2)<1e-10

# Radial Fourier transform of LOCAL PP difference: F(q)=4pi int dr r^2 delta_v(r) sinc(qr).
# Local ionic UPF potential uses Rydbergs and coordinates use atomic units.
def vform(q):
    q=np.asarray(q)
    out=np.empty(len(q))
    for i in range(0,len(q),80):
        k=q[i:i+80,None]
        out[i:i+80]=4*np.pi*simpson((rc*rc*dv)[None,:]*np.sinc(k*rc[None,:]/np.pi),x=rc,axis=1)
    return out

def projected(N,dq):
    assert N>2*max(abs(g).max(axis=0))+1
    modes=np.fft.fftfreq(N)*N
    h=np.stack(np.meshgrid(modes,modes,modes,indexing="ij"),axis=-1).reshape(-1,3)
    q=np.linalg.norm(h@b,axis=1)
    sample=np.arange(0,float(q.max())+0.5,dq)
    fourier=PchipInterpolator(sample,vform(sample))(q).reshape((N,)*3)/volume
    potential=np.fft.ifftn(fourier)*N**3
    assert np.max(abs(potential.imag))<1e-9
    cg=np.zeros((6,2,N,N,N),dtype=np.complex128)
    for ix,v in enumerate(g):
        cg[:,:,v[0]%N,v[1]%N,v[2]%N]=wave[:,:,ix]
    realspace=np.fft.ifftn(cg,axes=(-3,-2,-1))*np.sqrt(N**3)
    mat=np.einsum("asijk,ijk,bsijk->ab",realspace.conj(),potential.real,realspace,optimize=True)
    return mat,float(np.max(abs(potential.imag)))
m41,im41=projected(41,.01)
m49,im49=projected(49,.01)
m41fine,imfine=projected(41,.005)
assert np.max(abs(m49-m41))<1e-8
assert np.max(abs(m41-m41fine))<2e-6
assert np.max(abs(m49-m49.conj().T))<1e-11
m=m49*RY_TO_EV
a=m[:2,:2];z=m[2:,2:];cross=m[:2,2:]
out=dict(status="CALCULATED_BARE_LOCAL_ONLY_NOT_FULL_DEFECT",
 matrix_eV=[[[float(v.real),float(v.imag)] for v in row] for row in m],
 gamma6_mean_diagonal_eV=float(np.trace(a).real/2),
 gamma8_mean_diagonal_eV=float(np.trace(z).real/4),
 gamma6_minus_gamma8_local_eV=float(np.trace(a).real/2-np.trace(z).real/4),
 gamma6_gamma8_cross_fro_eV=float(np.linalg.norm(cross)),
 gamma6_nonidentity_op_eV=float(np.linalg.norm(a-np.eye(2)*np.trace(a)/2,2)),
 gamma8_nonidentity_op_eV=float(np.linalg.norm(z-np.eye(4)*np.trace(z)/4,2)),
 grid_41_49_max_difference_eV=float(np.max(abs(m49-m41))*RY_TO_EV),
 q_step_0p01_0p005_max_difference_eV=float(np.max(abs(m41-m41fine))*RY_TO_EV),
 hermiticity_error_eV=float(np.max(abs(m-m.conj().T))),
 imaginary_potential_error_Ry=max(im41,im49,imfine),
 qzero_local_formfactor_Ry_bohr3=float(vform(np.array([0.]))[0]),
 radial_tail_max_dv_Ry=float(np.max(abs(dv[-80:]))),
 saved_G_count=len(g),primitive_cell_volume_bohr3=volume,
 omissions=["Nonlocal spin-orbit ionic projectors","Self-consistent response and screened defect perturbation","Off-Gamma scattering","Multiple disorder configurations","Certified Gamma sector symmetry"],
 normalization="localized potential per cation site with Bloch amplitudes cell-normalized; scattering amplitudes for a single defect in N cells require 1/N factor",
 provenance_sha256={str(p):sha(p) for p in [UPFS["Hg"],UPFS["Cd"],SAVE/"wfc1.hdf5",SAVE/"data-file-schema.xml"]})
Path(__file__).with_name("bare_local_gamma_result.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k.endswith("_eV") or k in ("status","qzero_local_formfactor_Ry_bohr3")},indent=2))
