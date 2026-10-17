"""R08 bounded QE-7.5 source-formula parity on saved Gamma spinors.

Independent computational path: QE's real ylmr2 harmonics, rot_ylm, spinor.f90
fcoef tensor, beta_mod tabular interpolation, simpsn Simpson coefficients,
and add_vuspsi noncollinear contraction. No new QE DFT calculation.

IMPORTANT: This is NOT execution of native QE add_vuspsi, which still requires
a frozen-state initialized native diagnostic.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import json,hashlib
import numpy as np
import h5py
from scipy.special import spherical_jn,sph_harm_y

ROOT=Path("/home/User/opencode_workspace/DFT")
CASE=Path(__file__).resolve().parent
SAVE=ROOT/".local/r07_vca_x0125_hse_20261017/out/r07pk4.save"
UPF={
"Hg":ROOT/"calculations/r07/hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800/out/r07.save/Hg_sg15_pbe_fr_v12.UPF",
"Cd":ROOT/"calculations/r07/cdte_hse_sg15_k4_q2_e90_fullacc/out/r07.save/Cd_sg15_pbe_fr_v12.UPF"
}
RE=13.605693122994
with h5py.File(SAVE/"wfc1.hdf5") as f:
    mill=f["MillerIndices"][:]
    bg=np.array([f["MillerIndices"].attrs["bg"+str(i)] for i in (1,2,3)])
    psi=np.ascontiguousarray(f["evc"][32:38]).view(np.complex128).reshape(6,2,len(mill))
g=mill@bg
q=np.linalg.norm(g,axis=1)
theta=np.zeros_like(q);phi=np.zeros_like(q)
mask=q>1e-12
theta[mask]=np.arccos(np.clip(g[mask,2]/q[mask],-1,1))
phi[mask]=np.arctan2(g[mask,1],g[mask,0])
Y={}
for l in range(4):
    z=[sph_harm_y(l,m,theta,phi) for m in range(l+1)]
    Y[l]=[z[0].real]
    for m in range(1,l+1):
        Y[l].extend([np.sqrt(2)*z[m].real,np.sqrt(2)*z[m].imag])
    Y[l]=np.asarray(Y[l])
    # QE rot_ylm: complex harmonic = U @ real harmonic.
    rot=np.zeros((2*l+1,2*l+1),complex)
    rot[l,0]=1
    for m in range(1,l+1):
        cos,sin=2*m-1,2*m
        rot[l-m,cos]=(-1)**m/np.sqrt(2)
        rot[l-m,sin]=-1j*(-1)**m/np.sqrt(2)
        rot[l+m,cos]=1/np.sqrt(2)
        rot[l+m,sin]=1j/np.sqrt(2)
    for m in range(-l,l+1):
        actual=rot[m+l]@Y[l]
        expected=sph_harm_y(l,m,theta,phi)
        assert np.max(abs(actual-expected))<2e-14,(l,m)

def sp(l,j,m,s):
    # QE upflib/spinor.f90, 1-based spin channel
    if abs(j-l-.5)<1e-9:
        return np.sqrt(max(0,(l+m+1 if s==1 else l-m)/(2*l+1)))
    if m < -l+1:return 0.
    if s==1:return np.sqrt((l-m+1)/(2*l+1))
    return -np.sqrt((l+m)/(2*l+1))

def sind(l,j,m,s):
    # QE upflib/sph_ind.f90. 0 means no orbital term (otherwise magnetic m)
    if abs(j-l-.5)<1e-9:
        mm=m if s==1 else m+1
    else:
        mm=m-1 if s==1 else m
    return mm if -l<=mm<=l else None

def qe_radial_weights(n,rab):
    # QE upflib/simpsn.f90: includes even-mesh DFTK last-panel correction.
    w=np.zeros(n)
    w[0]=1
    w[1:-1]=np.where(np.arange(1,n-1)%2==1,4.,2.)
    if n%2: w[-1]=1
    else:
        w[-3]-=.25
        w[-2]+=1.
        w[-1]=1.25
    return w*rab/3

def read_pp(path):
    root=ET.parse(path).getroot()
    rr=np.fromstring(root.findtext("PP_MESH/PP_R"),sep=" ")
    rab=np.fromstring(root.findtext("PP_MESH/PP_RAB"),sep=" ")
    betas=[z for z in root.find("PP_NONLOCAL") if z.tag.startswith("PP_BETA.")]
    j=[float(z.attrib["jjj"]) for z in root.find("PP_SPIN_ORB") if z.tag.startswith("PP_RELBETA")]
    d=np.fromstring(root.findtext("PP_NONLOCAL/PP_DIJ"),sep=" ").reshape(len(j),len(j))
    assert np.max(abs(d-np.diag(np.diag(d))))<1e-12
    assert len(betas)==len(j)
    return rr,rab,[(int(z.attrib["angular_momentum"]),jj,np.fromstring(z.text,sep=" "),float(d[i,i])) for i,(z,jj) in enumerate(zip(betas,j))]

def radial_qe(r,rab,beta,l,mode="table"):
    # QE beta_mod: 4pi/sqrt(omega)*simpson(beta(r)*r*j_l(qr), rab).
    omega=454.814355208707
    w=qe_radial_weights(len(r),rab)*beta*r*4*np.pi/np.sqrt(omega)
    if mode=="direct":
        qs=q
    else:
        dq=.01
        qs=np.arange(0,q.max()+.07,dq)
    f=np.empty(len(qs))
    for start in range(0,len(qs),100):
        block=qs[start:start+100,None]
        f[start:start+100]=spherical_jn(l,block*r[None,:])@w
    if mode=="direct":return f
    # Exact four-point QE beta_mod/interp_beta weights.
    ip=np.floor(q/.01).astype(int)
    px=q/.01-ip
    ux=1-px;vx=2-px;wx=3-px
    return (f[ip]*ux*vx*wx/6+f[ip+1]*px*vx*wx/2
            -f[ip+2]*px*ux*wx/2+f[ip+3]*px*ux*vx/6)

def sector(mat):
    return float((np.trace(mat[:2,:2]).real/2-np.trace(mat[2:,2:]).real/4)*RE)

def calculate(kind,mode):
    r,rab,rows=read_pp(UPF[kind])
    mat=np.zeros((6,6),complex)
    for l,j,beta,d in rows:
        v=(-1j)**l*radial_qe(r,rab,beta,l,mode)
        # QE nhtolm real harmonics, 2*l+1 for a radial beta.
        k=len(Y[l])
        bec=np.einsum("hg,asg,g->ahs",Y[l],psi,v.conj(),optimize=True)
        # bec dimensions [band,realY,spin]; complex conjugate phase is on v.
        rot=np.zeros((2*l+1,2*l+1),complex)
        rot[l,0]=1
        for mm in range(1,l+1):
            rot[l-mm,2*mm-1]=(-1)**mm/np.sqrt(2)
            rot[l-mm,2*mm]=-1j*(-1)**mm/np.sqrt(2)
            rot[l+mm,2*mm-1]=1/np.sqrt(2)
            rot[l+mm,2*mm]=1j/np.sqrt(2)
        fcoef=np.zeros((k,k,2,2),complex)
        mr=range(-l-1,l+1) if abs(j-l-.5)<1e-9 else range(-l+1,l+1)
        for mj in mr:
            for sa in (1,2):
                ia=sind(l,j,mj,sa)
                if ia is None:continue
                aa=rot[ia+l]*sp(l,j,mj,sa)
                for sb in (1,2):
                    ib=sind(l,j,mj,sb)
                    if ib is None:continue
                    bb=rot[ib+l]*sp(l,j,mj,sb)
                    fcoef[:,:,sa-1,sb-1]+=aa[:,None]*bb.conj()[None,:]
        # Source add_vuspsi_nc: PS_ih,s1 = deeq_nc_ih,jh,s1,s2 BEC_jh,s2
        ps=np.einsum("ijuv,bjv->biu",fcoef,bec,optimize=True)
        mat+=d*np.einsum("aiu,biu->ab",bec.conj(),ps,optimize=True)
    assert np.max(abs(mat-mat.conj().T))<2e-11
    return mat

ref=json.loads((CASE/"nonlocal_gamma_provisional.json").read_text())
res={}
for name in ("Hg","Cd"):
    table=calculate(name,"table")
    direct=calculate(name,"direct")
    b=ref["parent_"+name]
    res[name]={
      "qe_source_formula_table_sector_contrast_eV":sector(table),
      "qe_source_formula_direct_sector_contrast_eV":sector(direct),
      "prior_python_sector_contrast_eV":b["sector_contrast"],
      "qe_interpolation_vs_direct_max_element_eV":float(np.max(abs(table-direct))*RE),
      "hermiticity_error_eV":float(np.max(abs(table-table.conj().T))*RE),
      "matrix_table":table,
    }
mat=res["Cd"]["matrix_table"]-res["Hg"]["matrix_table"]
orig=np.asarray(ref["nonlocal_delta_matrix"])
original=orig[:,:,0]+1j*orig[:,:,1]
result={
"status":"QE_SOURCE_FORMULA_PARITY_NOT_NATIVE_ACTION",
"parents":{n:{k:v for k,v in v.items() if k!="matrix_table"} for n,v in res.items()},
"delta_source_sector_contrast_eV":sector(mat),
"delta_previous_sector_contrast_eV":sector(original/RE),
"delta_source_vs_prior_max_abs_eV":float(np.max(abs(mat*RE-original))),
"delta_source_vs_prior_fro_eV":float(np.linalg.norm(mat*RE-original)),
"delta_source_matrix_eV":[[[float(z.real*RE),float(z.imag*RE)] for z in row] for row in mat],
"source_conventions":"QE 7.5 ylmr2, rot_ylm, spinor, sph_ind, init_us_1 fcoef, simpsn, beta_mod interp_beta, add_vuspsi_nc contractions",
"native_add_vuspsi_executed":False,
"note":"Formula parity from separate realY QE implementation only; absolute native action and unit normalization remain uncertified.",
"source_pins":{str(p):hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in UPF.values()}
}
(CASE/"qe_source_parity_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="delta_source_matrix_eV" and k!="source_pins"},indent=2))
