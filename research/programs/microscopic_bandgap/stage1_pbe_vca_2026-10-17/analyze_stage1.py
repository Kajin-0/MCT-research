"""Read-only, matched fixed-reference x=.125 PBE ordered-VCA contrasts. No QE."""
from pathlib import Path
import json,sys,hashlib
import numpy as np,h5py
from xml.etree import ElementTree as ET
ROOT=Path(__file__).parent
OLD=ROOT.parent/'chemical_pbe16_p2_2026-10-15'
sys.path.insert(0,str(OLD))
from science import frames,read_spinors,td_check,cell
P=Path('/home/User/opencode_workspace/DFT/.local/r07s1_20261017/primitive/out/r07pbe.save')
H=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16p2_20261015/host/out/r07pbe.save')
C=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16cd_20261015/cd/out/r07pbe.save')
ev=27.211386245988
def read(d):
 t=ET.parse(d/'data-file-schema.xml')
 es=np.fromstring(t.findtext('.//output/band_structure/ks_energies/eigenvalues'),sep=' ')*ev
 ef=float(t.findtext('.//output/band_structure/fermi_energy'))*ev
 w,g,k=read_spinors(d/'wfc1.hdf5')
 return t,es,ef,w,g,k
pt,ep,fp,cp,gp,kp=read(P);ht,eh,fh,ch,gh,kh=read(H);ct,ec,fc,cc,gc,kc=read(C)
assert np.max(abs(cell(ht)-2*cell(pt)))<1e-10
frames_host,transport=frames(gh,kh,ht)
lookup={tuple(g):i for i,g in enumerate(gh)}
even=np.array([lookup[tuple(2*g)] for g in gp])
ref=json.loads((OLD/'multiplet_result.json').read_text())
data={'ordered':{},'vca':{}}
observables={}
for label,dim in [('Gamma6',2),('Gamma8',4)]:
 frame=frames_host[label][:,:,even]
 assert abs(np.linalg.norm(frame)**2-dim)<1e-9
 ov=frame.reshape(dim,-1).conj()@cp.reshape(46,-1).T
 w=np.sum(abs(ov)**2,axis=0)/dim
 pinds=np.sort(np.argsort(w)[-dim:])
 sym=td_check(cp[pinds],gp,cell(pt))
 assert sym['nearest_integer_classification_admitted_under_model']
 assert sym['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==([1,0,0] if label=='Gamma6' else [0,0,1])
 # Exact retained ordered spectrum using previous fixed frame, source was independently validated.
 tab=np.loadtxt(OLD/('cd_'+label+'_spectrum.csv'),delimiter=',',skiprows=1)
 data['vca'][label]={'energy':ep-fp,'weight':w}
 data['ordered'][label]={'energy':tab[:,1],'weight':tab[:,2]}
 observables[label]={'VCA_Gamma_bands_1based':list(map(int,pinds+1)),
   'VCA_Td_class':sym['rounded_Gamma6_Gamma7_Gamma8_multiplicities'],
   'VCA_frame_weight_in_selected':float(sum(w[pinds])),
   'VCA_retained_weight':float(sum(w)),
   'ordered_retained_weight':float(sum(tab[:,2])),
   'VCA_mean_minus_own_Fermi_eV':float(np.mean(ep[pinds]-fp)),
   'ordered_mean_minus_own_Fermi_eV':ref['members']['cd'][label]['mean_minus_own_Fermi_eV']}
def gaussian(sample,W):
 x=sample['energy'];w=sample['weight'];f=np.exp(-x*x/(2*W*W));mass=float(w@f)
 return {'centroid_eV':float(w@(x*f)/mass),'Gaussian_mass':mass,'missing_spectral_probability':max(0.,float(1-sum(w)))}
def inverse(sample,eta):
 x=sample['energy'];w=sample['weight'];G=np.sum(w/(1j*eta-x))
 return {'G_real':float(G.real),'G_imag':float(G.imag),'inverse_real_eV':float((1/G).real),'missing_spectral_probability':max(0.,float(1-sum(w)))}
tracked={m:obs['ordered_mean_minus_own_Fermi_eV'] if m=='ordered' else obs['VCA_mean_minus_own_Fermi_eV'] for m,obs in []}
tracked_ordered=observables['Gamma6']['ordered_mean_minus_own_Fermi_eV']-observables['Gamma8']['ordered_mean_minus_own_Fermi_eV']
tracked_vca=observables['Gamma6']['VCA_mean_minus_own_Fermi_eV']-observables['Gamma8']['VCA_mean_minus_own_Fermi_eV']
grows=[];inverse_rows=[]
for W in [1.,1.5,2.,2.5,3.]:
 vals={m:{l:gaussian(data[m][l],W) for l in ['Gamma6','Gamma8']} for m in data}
 order={m:vals[m]['Gamma6']['centroid_eV']-vals[m]['Gamma8']['centroid_eV'] for m in data}
 grows.append({'W_eV':W,'ordered_eV':order['ordered'],'VCA_eV':order['vca'],'ordered_minus_VCA_eV':order['ordered']-order['vca'],'details':vals})
for eta in [.025,.05,.1]:
 vals={m:{l:inverse(data[m][l],eta) for l in ['Gamma6','Gamma8']} for m in data}
 order={m:vals[m]['Gamma8']['inverse_real_eV']-vals[m]['Gamma6']['inverse_real_eV'] for m in data}
 inverse_rows.append({'eta_eV':eta,'ordered_eV':order['ordered'],'VCA_eV':order['vca'],'ordered_minus_VCA_eV':order['ordered']-order['vca'],'details':vals})
result={'status':'CALCULATED matched retained-spectral model contrasts; NOT material error certification',
'observable_reference':'each specimen own Fermi energy; no absolute cross-specimen offset',
'original_fixed_projectors_reused':True,'VCA_Td':observables,
'tracked_multiplet_ordered_eV':tracked_ordered,'tracked_multiplet_VCA_eV':tracked_vca,'tracked_ordered_minus_VCA_eV':tracked_ordered-tracked_vca,
'Gaussian_W_rows':grows,'scalar_inverse_eta_rows':inverse_rows,
'caveats':['Gaussian widths/eta are externally imposed probes, not intrinsic linewidth','PBE 46-band Γ-retained VCA and 352-band ordered supercell have separate incomplete high-energy tails','No material uncertainty bound or physical xc established','No HSE transfer or random alloy statistics','Scalar inverse is not equivalent to a sharp signed inversion mass','own Fermi energy per sample; no absolute energy alignment'],
'native_stage1_guard_pass':json.loads((P.parent.parent/'FINAL.json').read_text())['terminal_pass']}
(ROOT/'stage1_contrasts.json').write_text(json.dumps(result,indent=2)+'\n')
print('TRACKED',tracked_ordered,tracked_vca,tracked_ordered-tracked_vca)
for a in grows:print('Gaussian W',a['W_eV'],'delta',a['ordered_minus_VCA_eV'],'missing',[(m,l,a['details'][m][l]['missing_spectral_probability']) for m in data for l in ['Gamma6','Gamma8']])
for a in inverse_rows:print('INVERSE eta',a['eta_eV'],'delta',a['ordered_minus_VCA_eV'])
