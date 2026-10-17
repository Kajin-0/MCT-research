"""Read-only G-labelled HgTe-reference sector transport to VCA Γ spinors."""
import importlib.util,json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation
CASE=Path(__file__).resolve().parent
ROOT=Path("/home/User/opencode_workspace/DFT/.local/r07_vca_x0125_hse_20261017")
SAVE=ROOT/"out/r07pk4.save"
OLD=Path("/home/User/opencode_workspace/DFT/calculations/r07/hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800/out/r07.save")
MODULE=CASE.parents[1]/"primitive_k4_hse_2026-10-17/final_qualification/analyze_final.py"
spec=importlib.util.spec_from_file_location("existing_host_postprocessing",MODULE)
host=importlib.util.module_from_spec(spec); spec.loader.exec_module(host)
prior,_=host.load_prior()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
xml=ET.parse(SAVE/"data-file-schema.xml").getroot().find("output")
oldxml=ET.parse(OLD/"data-file-schema.xml").getroot().find("output")
cell=lambda out:np.array([np.fromstring(out.findtext("atomic_structure/cell/"+v),sep=" ") for v in ("a1","a2","a3")])
assert np.max(abs(cell(xml)-cell(oldxml)))<1e-12
c,g,k,b=prior.read(SAVE/"wfc1.hdf5")
oc,og,ok,ob=prior.read(OLD/"wfc1.hdf5")
assert np.linalg.norm(k)<1e-12 and np.linalg.norm(ok)<1e-12 and np.max(abs(b-ob))<1e-12
for at,bt in zip(xml.findall("atomic_structure/atomic_positions/atom"),oldxml.findall("atomic_structure/atomic_positions/atom")):
 assert at.attrib["name"]==bt.attrib["name"] and np.max(abs(np.fromstring(at.text,sep=" ")-np.fromstring(bt.text,sep=" ")))<1e-12
lookup={tuple(row):i for i,row in enumerate(og)}
assert all(tuple(row) in lookup for row in g)
idx=np.array([lookup[tuple(row)] for row in g])
reference=oc[32:38][:,:,idx]
overlap=reference.reshape(6,-1).conj()@c.reshape(44,-1).T
reference_tail=np.sum(abs(oc[32:38])**2,axis=(1,2))-np.sum(abs(reference)**2,axis=(1,2))
energies=2*np.fromstring(xml.findall("band_structure/ks_energies")[0].findtext("eigenvalues"),sep=" ")*13.605693122994
f=np.fromstring(xml.findall("band_structure/ks_energies")[0].findtext("occupations"),sep=" ")
ops=prior.ops(); xmlops=[]
for entry in xml.findall("symmetries/symmetry"):
 if entry.findtext("info")!="crystal_symmetry":continue
 rot=np.fromstring(entry.findtext("rotation"),sep=" ").reshape(3,3)
 candidates=[cell(xml).T@r@np.linalg.inv(cell(xml).T) for r in (rot,rot.T)]
 cart=min(candidates,key=lambda a:min(np.linalg.norm(a-r) for r,_,_ in ops))
 i=int(np.argmin([np.linalg.norm(cart-r) for r,_,_ in ops]))
 assert np.linalg.norm(cart-ops[i][0])<1e-10
 xmlops.append(i)
assert len(xmlops)==len(set(xmlops))==24
sectors={}
for label,sl,dim in [("Gamma6_like",slice(0,2),2),("Gamma8_like",slice(2,6),4)]:
 weights=np.sum(abs(overlap[sl])**2,axis=0)
 selected=np.sort(np.argsort(weights)[-dim:])
 u=c[selected].reshape(dim,-1).T
 td=[];chars=[];ideal=[]
 for i in xmlops:
  r,s,det=ops[i]
  d=prior.transform(c[selected],g,k,b,g,k,r,s).reshape(dim,-1).T
  a=u.conj().T@d
  td.append(float(np.linalg.norm(d-u@a,2)))
  chars.append(complex(np.trace(a)))
  trace=2*Rotation.from_matrix(det*r).as_quat()[3]
  ideal.append(trace if dim==2 else det*(trace**3-2*trace))
 theta=prior.transform(c[selected],g,k,b,g,k).reshape(dim,-1).T
 sew=u.conj().T@theta
 sectors[label]=dict(indices_1based=(selected+1).tolist(),energies_eV=energies[selected].tolist(),occupations=f[selected].tolist(),
 projection_weights=weights[selected].tolist(),projection_singular_values=np.linalg.svd(overlap[sl][:,selected],compute_uv=False).tolist(),
 max_Td_amplitude_span_leakage=float(max(td)),max_Td_character_error=float(max(abs(np.array(chars)-ideal))),
 Theta_amplitude_span_leakage=float(np.linalg.norm(theta-u@sew,2)),
 Theta_sewing_singular_values=np.linalg.svd(sew,compute_uv=False).tolist(),
 Theta_sewing_skew_error=float(np.linalg.norm(sew+sew.T,2)),
 max_Td_character_error_per_operation=[float(abs(a-b)) for a,b in zip(chars,ideal)],
 strict_sector_amplitude_1e8_pass=bool(max(td)<=1e-8 and np.linalg.norm(theta-u@sew,2)<=1e-8))
result=dict(status="REFERENCE_TRANSPORT_DIAGNOSTIC_NOT_STRICT_MASS_CERTIFICATE",
 reference_chemical_identity="HgTe host, NOT same pseudopotential as mixed-cation VCA",
 reference_frame="previously qualified e90/f120 HgTe reference with G-index e50 transport; frame chemical substitution prevents exact operator equivalence",
 full_reference_G_subset=True,reference_lost_probability=reference_tail.tolist(),
 sectors=sectors,provisional_energy_delta_eV=float(np.mean(energies[sectors["Gamma6_like"]["indices_1based"] and np.array(sectors["Gamma6_like"]["indices_1based"])-1])-np.mean(energies[np.array(sectors["Gamma8_like"]["indices_1based"])-1])),
 strict_full_density_1e8_pass=False,
 source_sha256=sha(__file__),native_xml_sha256=sha(SAVE/"data-file-schema.xml"),native_spinor_sha256=sha(SAVE/"wfc1.hdf5"),host_reference_spinor_sha256=sha(OLD/"wfc1.hdf5"))
(CASE/"reference_projection_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ("status","sectors","provisional_energy_delta_eV")},indent=2))
