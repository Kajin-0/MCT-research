"""Frozen R07 Stage 0 read-only spectral-prefix and source-pin preflight. No QE invocation."""
import hashlib, itertools, json, pathlib, sys, xml.etree.ElementTree as ET
import h5py, numpy as np
HERE=pathlib.Path(__file__).resolve().parent
DFT=pathlib.Path('/home/User/opencode_workspace/DFT')
SAVE=DFT/'.local/qe75_lowram_20261011/p16p2_20261015/host/out/r07pbe.save'
SRC=DFT/'.local/qe-env/bin'
PP=DFT/'pseudopotentials'
pins={
'pw.x':(SRC/'pw.x','1d66c7856f5d6b3cd9c66b8578e01512b16bbe907b4360e54234890712ccd6a1'),
'mpirun':(SRC/'mpirun','9647aa90368686758b66cb2984cda4f552ac170851f34ff07e35f9bdbf54e625'),
'Hg':(PP/'Hg_sg15_pbe_fr_v12.UPF','846a3a2bbef4b97835486a60468a0dafd68d622e21ebfb76011e51ce65fafee0'),
'Cd':(PP/'Cd_sg15_pbe_fr_v12.UPF','a388ee7afceb3557a41675cad4891fddcd6677cccf4e42e133e55a3f18e34e9b'),
'Te':(PP/'Te_sg15_pbe_fr_v12.UPF','1b6d3177b82988cecabebf7da1636825613b7270bc269795a1fb6c12743e12fa'),
'host_xml':(SAVE/'data-file-schema.xml','50671ba742d4ac7ed3c3bdc627af7f28c23528a3a2ae4d2b1ab6133d08871875'),
'host_input':(DFT/'.local/qe75_lowram_20261011/p16p2_20261015/host/pw.in','8e97aa2e4e66c72a65b5f6d9aee4b5b6d53b9fdf2f420a34c8c464350a20c0d8')}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
checks={k:{'path':str(p),'sha256':sha(p),'match':sha(p)==want} for k,(p,want) in pins.items()}
assert all(x['match'] for x in checks.values())
deck=(HERE/'primitive_pbe_fold46.in').read_text()
for t in ('nat=2','ntyp=2','nbnd=46','ecutwfc=50','ecutrho=200',"smearing='fd'",'degauss=0.001','noncolin=.true.','lspinorb=.true.','2 2 2 0 0 0'):assert t in deck,t
assert deck.count('Hg 0.00000000')==1 and deck.count('Te 0.25000000')==1
r=ET.parse(SAVE/'data-file-schema.xml').getroot()
s=np.fromstring(r.findtext('output/band_structure/ks_energies/eigenvalues'),sep=' ')*27.211386245988
with h5py.File(SAVE/'wfc1.hdf5','r') as f:
 g=f['MillerIndices'][:] % 2
 codes=4*g[:,0]+2*g[:,1]+g[:,2]
 a=np.ascontiguousarray(f['evc'][:]).view(np.complex128).reshape(352,2,-1)
 weights=np.stack([np.sum(abs(a[:,:,codes==i])**2,axis=(1,2)) for i in range(8)],axis=1)
assert np.max(abs(weights.sum(axis=1)-1))<1e-11
trace350=weights[:350].sum(axis=0)
trace352=weights.sum(axis=0)
want=np.array([46,46,46,40,46,40,40,46])
assert np.max(abs(trace350-want))<1e-8
assert np.max(abs(weights[:144].sum(axis=0)-18))<1e-10
occupation=np.fromstring(r.findtext('output/band_structure/ks_energies/occupations'),sep=' ')
assert len(occupation)==352
weighted=occupation@weights
assert abs(occupation.sum()-288)<1e-8
assert np.max(abs(weighted-36))<1e-8
assert np.all(abs(occupation[286:290]-.5)<1e-8)
assert np.max(abs(trace352-np.round(trace352)))>.1
a_matrix=np.array([[0,1,1],[1,0,1],[1,1,0]])
fold=[]
for p in itertools.product([0,.5],repeat=3):
 q=np.array(p);t=q@a_matrix
 code=4*int(2*q[0])+2*int(2*q[1])+int(2*q[2])
 fold.append({'primitive_fractional':list(p),'supercell_reciprocal_fractional':list(map(float,t)),'parity_sector':format(code,'03b'),'multiplicity_class':('Gamma' if sum(q)==0 else 'X' if sum(q)==1 else 'L')})
out={'status':'READ_ONLY_DESIGN_PIN_AND_SPECTRAL_PREFLIGHT_PASS_NO_NATIVE_OWNER_EXECUTION',
'deck_sha256':sha(HERE/'primitive_pbe_fold46.in'),'deck_path':str(HERE/'primitive_pbe_fold46.in'),
'source_pins':checks,'folding_map':fold,'prefix_144_parity_per_sector_not_occupied':list(map(float,weights[:144].sum(axis=0))),
'occupation_weighted_electrons_per_sector':list(map(float,weighted)),
'occupation_sum_electrons':float(occupation.sum()),
'occupation_fractional_bands_1based':[287,288,289,290],
'occupation_fractional_values':list(map(float,occupation[286:290])),
'prefix_350_per_sector':list(map(float,trace350)),'prefix_352_per_sector':list(map(float,trace352)),
'max_integrality_error_350':float(np.max(abs(trace350-np.round(trace350)))),
'retained_E350_eV':float(s[349]),'retained_E351_eV':float(s[350]),'retained_E352_eV':float(s[351]),
'primitive_minimum_band_count':46,'full_supercell_deg_cluster':'unresolved: archived bands351-352 are partial X-derived multiplet; four higher supercell states not archived',
'full_spectrum_acceptance':'INCONCLUSIVE before complete supercell cutoff manifold, irrespective of 46 primitive coverage',
'physical_scope':'PBE+SOC folding; no new DFT, no HSE, no random-alloy x_c',
'native_execution_authorized':False,'native_resource_owner_qualified':False}
(HERE/'spectral_preflight.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS', 'N_BAND',46,'complete350',want.tolist(),'truncated352',np.round(trace352,6).tolist(),'cutoff_eV',s[351],'pins',len(checks))
