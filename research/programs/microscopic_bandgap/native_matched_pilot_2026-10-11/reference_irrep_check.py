"""Native fixed-frame Td character check; no native calculation/postprocessor.

The numerical envelope is conditional on standard bounded IEEE dot-product
rounding, exact NC metric and the declared spatial/spin representation. It is
not a true-HSE-eigenpair or material accuracy certificate.
"""
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import h5py
import numpy as np
from scipy.spatial.transform import Rotation

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
SOURCE=DFT/'calculations/r07/hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800'
sys.path.insert(0,str(DFT/'src'))
from mct_dft.qe_wavefunctions import read_spinors


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(262144),b''):h.update(block)
    return h.hexdigest()


def td_operations():
    """24 signed permutations preserving the four (product-sign +1) bonds."""
    pauli=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
    operations=[]
    legal=np.array([-1,-np.sqrt(.5),-.5,0,.5,np.sqrt(.5),1])
    for perm in permutations(range(3)):
        for signs in product((-1,1),repeat=3):
            if np.prod(signs)!=1:continue
            spatial=np.diag(signs)@np.eye(3)[list(perm)]
            determinant=round(np.linalg.det(spatial))
            raw=Rotation.from_matrix(determinant*spatial).as_quat()
            quaternion=legal[np.argmin(abs(raw[:,None]-legal),axis=1)]
            if np.max(abs(raw-quaternion))>1e-14:raise ValueError('Unexpected Td spin lift')
            spin=quaternion[3]*np.eye(2)-1j*np.einsum('a,aij->ij',quaternion[:3],pauli)
            t=2*quaternion[3]
            characters=np.array([t,determinant*t,determinant*(t**3-2*t)],complex)
            operations.append({'spatial':spatial,'spin':spin,'quaternion':quaternion,
                               'characters':characters,'determinant':determinant})
    return operations


def gamma(count):
    unit=2.**-53
    if count*unit>=1:raise ValueError('Floating error model outside range')
    return count*unit/(1-count*unit)


def nearby_irrep_envelope(gram_defect_frobenius, leakage_defect_frobenius,
                         native_character, ideal_character, dimension, components):
    """See proof; scalar evaluation is CALCULATED under arithmetic assumptions."""
    d=dimension
    entry_error=4*gamma(32*components)+16*2.**-53
    gram_error=gram_defect_frobenius+d*entry_error
    if gram_error>=.1:raise ValueError('Unqualified physical metric')
    c_error=d*entry_error+(1+gram_error)*gram_error/(1-gram_error)
    product_error=4*d*gamma(32*d)+32*d*d*2.**-53
    true_leakage_defect=leakage_defect_frobenius+c_error*(2+c_error)+product_error
    tau=np.sqrt(true_leakage_defect)
    if tau>=.5:raise ValueError('No nearby invariant projector certificate')
    multiplicity=ideal_character.conj().T@native_character/24
    character_error=d*c_error
    # Rank(P-Q)<=2d, ||P-Q||<=2 tau; trace error <=4d tau.
    error=np.array([2,2,4])*(character_error+4*d*tau)+64*gamma(24)
    integer=np.rint(multiplicity.real).astype(int)
    admitted=bool(np.all(abs(multiplicity-integer)+error<.5))
    return {'dot_entry_error_model':entry_error,'Gram_error_upper_model':gram_error,
            'twirl_projector_distance_tau_upper_model':tau,
            'nearby_invariant_projector_distance_upper_model':2*tau,
            'multiplicity_complex':[[float(z.real),float(z.imag)] for z in multiplicity],
            'multiplicity_error_upper_model':error.tolist(),
            'rounded_Gamma6_Gamma7_Gamma8_multiplicities':integer.tolist(),
            'nearest_integer_classification_admitted_under_model':admitted}


def evaluate():
    result=json.loads((SOURCE/'result.json').read_text())
    assignment_path=SOURCE/'gamma/signed_gap.json'
    assignment=json.loads(assignment_path.read_text())
    if not result['accepted_scf']:raise ValueError('Accepted source only')
    schema=SOURCE/'out/r07_open.save/data-file-schema.xml'
    tree=ET.parse(schema)
    indices=[i for i,row in enumerate(tree.findall('.//ks_energies'),1)
             if np.linalg.norm(np.fromstring(row.findtext('k_point'),sep=' '))<1e-9]
    if len(indices)!=1:raise ValueError('Unique native Gamma required')
    wave=SOURCE/f'out/r07_open.save/wfc{indices[0]}.hdf5'
    states,miller,k=read_spinors(wave)
    selections={}
    for label,d in [('Gamma6',2),('Gamma8',4)]:
        first,last=assignment[label+'_bands_1based']
        if last-first+1!=d:raise ValueError('Prior native irrep dimension changed')
        selections[label]=states[first-1:last]
    with h5py.File(wave) as handle:
        reciprocal=np.array([handle['MillerIndices'].attrs[f'bg{i}'] for i in (1,2,3)])
    ideal_reciprocal=np.ones((3,3))-2*np.eye(3)
    scale=reciprocal[0,1]
    if np.max(abs(reciprocal/scale-ideal_reciprocal))>1e-12:
        raise ValueError('Declared Cartesian fcc frame changed')
    lookup={tuple(g):i for i,g in enumerate(miller)}
    operations=td_operations()
    ideal_char=np.array([op['characters'] for op in operations])
    chars={label:[] for label in selections};leak={label:0. for label in selections}
    metric={}
    for label,c in selections.items():
        flat=c.reshape(len(c),-1)
        metric[label]=float(np.linalg.norm(flat.conj()@flat.T-np.eye(len(c)),'fro'))
        nonzero=abs(flat[flat!=0])
        if nonzero.min()<1e-100 or nonzero.max()>1:
            raise ValueError('Overflow/underflow assumptions need a separate budget')
    for op in operations:
        index_rotation=ideal_reciprocal@op['spatial'].T@np.linalg.inv(ideal_reciprocal)
        if np.max(abs(index_rotation-np.rint(index_rotation)))>1e-14:
            raise ValueError('Nonintegral point-group mapping')
        mapped=miller@np.rint(index_rotation).astype(int)
        indices=np.array([lookup[tuple(g)] for g in mapped])
        for label,c in selections.items():
            transformed=np.empty_like(c)
            transformed[:,:,indices]=np.einsum('st,atg->asg',op['spin'],c)
            cmat=c.reshape(len(c),-1).conj()@transformed.reshape(len(c),-1).T
            chars[label].append(np.trace(cmat))
            leak[label]=max(leak[label],float(np.linalg.norm(np.eye(len(c))-cmat.conj().T@cmat,'fro')))
    sectors={}
    for label,c in selections.items():
        char=np.array(chars[label])
        expected=0 if label=='Gamma6' else 2
        certificate=nearby_irrep_envelope(metric[label],leak[label],char,ideal_char,len(c),2*len(miller))
        sectors[label]={'Gram_defect_frobenius':metric[label],'maximum_span_leakage_defect_frobenius':leak[label],
                        'maximum_character_mismatch':float(np.max(abs(char-ideal_char[:,expected]))),
                        'character_complex':[[float(z.real),float(z.imag)] for z in char],
                        **certificate}
    return {'claim_status':'CALCULATED source numerical character check; PROVEN UNDER ASSUMPTIONS nearby-projector theorem',
            'source':str(SOURCE),'point_group_order':24,'double_group_order':48,
            'sector_order':['Gamma6','Gamma7','Gamma8'],'native_plane_waves':len(miller),
            'sectors':sectors,'source_sha256':{str(p):digest(p) for p in
                (SOURCE/'result.json',assignment_path,schema,wave,DFT/'src/mct_dft/qe_wavefunctions.py')},
            'driver_sha256':digest(__file__),'native_postprocessor_invoked':False,
            'true_HSE_eigenpair_metric_or_material_accuracy_certified':False,
            'arithmetic_model':'standard IEEE complex dot products, no overflow/underflow; ideal Td lift error included; scalar envelopes conditional, not interval-native audit',
            'physical_xc':None,'failed_pilot_host_irreps_admitted':False}


if __name__=='__main__':
    output=HERE/'reference_irrep_check.json'
    if output.exists():raise FileExistsError('Never overwrite source qualification')
    result=evaluate()
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'group_order':result['point_group_order'],
          'sectors':{k:{j:v[j] for j in ['maximum_character_mismatch',
          'nearby_invariant_projector_distance_upper_model','rounded_Gamma6_Gamma7_Gamma8_multiplicities',
          'nearest_integer_classification_admitted_under_model']} for k,v in result['sectors'].items()}},indent=2))
