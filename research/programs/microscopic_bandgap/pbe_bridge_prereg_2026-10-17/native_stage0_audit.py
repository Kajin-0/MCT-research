"""Read-only post-execution R07 Stage0 primitive/supercell native null audit."""
import json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np,h5py
HERE=Path(__file__).resolve().parent
P=Path('/home/User/opencode_workspace/DFT/.local/r07s0_20261017/primitive')
H=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16p2_20261015/host')
EV_H=27.211386245988
def parse(path):
 r=ET.parse(path/'out/r07pbe.save/data-file-schema.xml').getroot();o=r.find('output');b=o.find('band_structure')
 return o,b,[(np.fromstring(x.findtext('eigenvalues'),sep=' ')*EV_H,np.fromstring(x.findtext('occupations'),sep=' '),float(x.find('k_point').attrib['weight'])) for x in b.findall('ks_energies')]
po,pb,pe=parse(P);ho,hb,he=parse(H)
assert len(pe)==3 and len(he)==1
assert all(len(x[0])==46 for x in pe) and len(he[0][0])==352
assert np.max(np.abs(np.array([x[2] for x in pe])-[.125,.5,.375]))<1e-14
assert all(abs(x[1].sum()-36)<1e-8 for x in pe)
assert abs(he[0][1].sum()-288)<1e-8
assert po.findtext('convergence_info/scf_conv/convergence_achieved')=='true'
assert ho.findtext('convergence_info/scf_conv/convergence_achieved')=='true'
assert [int(po.find('basis_set/fft_grid').attrib[x]) for x in ('nr1','nr2','nr3')]==[40]*3
assert [int(ho.find('basis_set/fft_grid').attrib[x]) for x in ('nr1','nr2','nr3')]==[80]*3
full=np.sort(np.concatenate([pe[0][0],np.tile(pe[1][0],4),np.tile(pe[2][0][:40],3)]))
delta=full-he[0][0][:350]
max_meV=float(max(abs(delta))*1000)
mean_meV=float(np.mean(abs(delta))*1000)
Eprim_H=float(po.findtext('total_energy/etot'));Ehost_H=float(ho.findtext('total_energy/etot'))
free_meV=(Ehost_H-8*Eprim_H)*EV_H*1000
# The QE XML 'etot' in Hartree contains the finite smearing entropy term.
# Verify with the native Ry text output before interpreting F.
def smeared(path):
 import re
 s=(path/'pw.out').read_text()
 m=re.findall(r'smearing contrib\. \(-TS\)\s*=\s*([-+\d.Ee]+) Ry',s)
 assert m
 return float(m[-1])
Sprim=smeared(P);Shost=smeared(H)
entropic_meV=(Shost-8*Sprim)*13.605693122994*1000
with h5py.File(P/'out/r07pbe.save/charge-density.hdf5') as p,h5py.File(H/'out/r07pbe.save/charge-density.hdf5') as h:
 pg=p['MillerIndices'][:];hg=h['MillerIndices'][:]
 pv=np.ascontiguousarray(p['rhotot_g'][:]).view('c16')
 hv=np.ascontiguousarray(h['rhotot_g'][:]).view('c16')
 hm={tuple(g):z for g,z in zip(hg,hv)}
 assert all(tuple(2*g) in hm for g in pg)
 paired=np.array([hm[tuple(2*g)] for g in pg])
 odd=hv[np.any(hg%2,axis=1)]
 density_rel=float(np.linalg.norm(paired-pv)/np.linalg.norm(pv))
 oddmax=float(max(abs(odd)))
with h5py.File(P/'out/r07pbe.save/wfc1.hdf5') as f:
 a=np.ascontiguousarray(f['evc'][:]).view(np.complex128).reshape(46,-1)
 prim_gram=float(np.max(abs(a.conj()@a.T-np.eye(46))))
with h5py.File(H/'out/r07pbe.save/wfc1.hdf5') as f:
 a=np.ascontiguousarray(f['evc'][:]).view(np.complex128).reshape(352,-1)
 host_gram=float(np.max(abs(a.conj()@a.T-np.eye(352))))
assert max_meV<2 and abs(free_meV)<8
assert prim_gram<1e-8 and host_gram<1e-8
guard=json.loads((P/'FINAL.json').read_text())
assert guard['terminal_pass'] and guard['guard']['pass_guard'] and guard['guard']['launcher_returncode']==0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=dict(experiment='R07_STAGE0_NATIVE_PBE_SOC_PRIMITIVE_FOLD46_SINGLE_AUTHORIZED_RUN',native_execution='SUCCEEDED_ONCE',terminal_guard='PASS',
k_reduced=[{'weight':z[2],'band_count':len(z[0]),'occupations':float(z[1].sum())} for z in pe],
electron_primitive=36,electron_supercell=288,spinor_occupation_kind='QE noncollinear FD smearing',
complete_350_spectrum_max_abs_meV=max_meV,complete_350_spectrum_mean_abs_meV=mean_meV,
observed_2meV_spectral_target='MET',
primitive_etot_H=Eprim_H,supercell_etot_H=Ehost_H,supercell_minus_8primitive_free_energy_meV=free_meV,
observed_8meV_free_energy_target='MET',
supercell_minus_8primitive_entropy_term_meV=entropic_meV,
primitive_fft=[40]*3,supercell_fft=[80]*3,
density_even_coefficients_relative_L2=density_rel,density_odd_max_abs=oddmax,
primitive_wfc_gram_max_error=prim_gram,supercell_wfc_gram_max_error=host_gram,
full_352_cutoff='INCONCLUSIVE (incomplete symmetry multiplet)',
independent_numerical_error_budget='NOT CERTIFIED; SCF/FFT/charge diagnostics do not form a rigorous <=1meV/<=4meV comparison error bound',
projector_subspace_validation='NOT FULLY QUALIFIED (native Γ symmetry frame overlap pending)',
stage0_overall='INCONCLUSIVE UNDER STRICT FROZEN PASS CONDITIONS',
stages_1_2='NOT AUTHORIZED',
inputs_sha256={str(f):sha(f) for f in [P/'pw.in',P/'out/r07pbe.save/data-file-schema.xml',H/'out/r07pbe.save/data-file-schema.xml']})
(HERE/'native_stage0_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='inputs_sha256'},indent=2))
