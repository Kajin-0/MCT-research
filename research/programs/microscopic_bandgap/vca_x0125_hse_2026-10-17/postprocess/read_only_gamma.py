"""Read-only Γ full-density symmetry audit, not a physical irrep certificate."""
import importlib.util,json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
ROOT=Path("/home/User/opencode_workspace/DFT/.local/r07_vca_x0125_hse_20261017")
SAVE=ROOT/"out/r07pk4.save"
P=Path(__file__).resolve().parent
SRC=P.parents[1]/"primitive_k4_hse_2026-10-17/final_qualification/analyze_final.py"
sp=importlib.util.spec_from_file_location("host_density_math",SRC)
a=importlib.util.module_from_spec(sp); sp.loader.exec_module(a)
prior,_=a.load_prior()
t=ET.parse(SAVE/"data-file-schema.xml").getroot(); out=t.find("output")
ks=out.findall("band_structure/ks_energies")
assert len(ks)==8 and out.findtext("convergence_info/scf_conv/convergence_achieved")=="true"
c,g,k,b=prior.read(SAVE/"wfc1.hdf5")
assert len(c)==44 and np.linalg.norm(k)<1e-12
f=np.fromstring(ks[0].findtext("occupations"),sep=" ")
e=2*np.fromstring(ks[0].findtext("eigenvalues"),sep=" ")*13.605693122994
assert len(e)==len(f)==44
charge=sum(float(v.find("k_point").attrib["weight"])*np.sum(np.fromstring(v.findtext("occupations"),sep=" ")) for v in ks)
assert abs(charge-36)<1e-8
cell=np.array([np.fromstring(out.findtext("atomic_structure/cell/"+x),sep=" ") for x in ("a1","a2","a3")]);ops=prior.ops()
xmlops=[]
for z in out.findall("symmetries/symmetry"):
 if z.findtext("info")!="crystal_symmetry":continue
 rot=np.fromstring(z.findtext("rotation"),sep=" ").reshape(3,3)
 choices=[cell.T@r@np.linalg.inv(cell.T) for r in (rot,rot.T)]
 cart=min(choices,key=lambda q:min(np.linalg.norm(q-r) for r,_,_ in ops))
 i=int(np.argmin([np.linalg.norm(cart-r) for r,_,_ in ops]))
 assert np.linalg.norm(cart-ops[i][0])<1e-10
 xmlops.append(i)
assert len(xmlops)==len(set(xmlops))==24
tr=prior.transform(c,g,k,b,g,k)
theta=a.density_norm(c,tr,f,f)
spatial=[]
for i in xmlops:
 r,s,_=ops[i];d=prior.transform(c,g,k,b,g,k,r,s)
 spatial.append(dict(operation_index=i,op=a.density_norm(c,d,f,f)["op"]))
delta=float(np.mean(e[32:34])-np.mean(e[34:38]))
records=dict(status="NUMERICAL_HSE_PASS_PHYSICAL_GAMMA_LABELS_PENDING",
 gamma_candidate_indices={"doublet":[33,34],"quartet":[35,36,37,38]},
 gamma_candidate_doublet_eV=e[32:34].tolist(),gamma_candidate_quartet_eV=e[34:38].tolist(),
 gamma_candidate_signed_delta_eV=delta,gamma_candidate_half_delta_eV=delta/2,
 gamma_candidate_occupations=f[32:38].tolist(),gamma_full_density_Theta=theta,
 gamma_full_density_Td_max=float(max(v["op"] for v in spatial)),
 gamma_full_density_Td_operations=spatial,
 strict_density_1e8_pass=bool(theta["op"]<=1e-8 and max(v["op"] for v in spatial)<=1e-8),
 native_irreducible_k=8,full_64_fiber_certificate=False,physical_Gamma_labels_certified=False,
 physical_random_alloy_xc=None,
 note="No density symmetrization; Γ indices provisional, not physical irrep identification.",
 input_sha256=hashlib.sha256((ROOT/"pw.in").read_bytes()).hexdigest(),
 xml_sha256=hashlib.sha256((SAVE/"data-file-schema.xml").read_bytes()).hexdigest(),
 spinor_sha256=hashlib.sha256((SAVE/"wfc1.hdf5").read_bytes()).hexdigest())
(P/"gamma_density_results.json").write_text(json.dumps(records,indent=2)+"\n")
print(json.dumps({k:records[k] for k in ("gamma_candidate_signed_delta_eV","gamma_candidate_half_delta_eV","gamma_full_density_Theta","gamma_full_density_Td_max","strict_density_1e8_pass")},indent=2))
