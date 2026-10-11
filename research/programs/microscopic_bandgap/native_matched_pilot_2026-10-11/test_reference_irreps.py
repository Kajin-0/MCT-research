"""Independent small representation checks; no native calculation or scan."""
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.linalg import block_diag, expm

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('reference_irreps', HERE/'reference_irrep_check.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def angular_momentum(j):
    m = np.arange(j, -j-1, -1)
    raising = np.zeros((len(m), len(m)), complex)
    for col in range(1, len(m)):
        raising[col-1, col] = np.sqrt(j*(j+1)-m[col]*(m[col]+1))
    lowering = raising.conj().T
    return np.array([(raising+lowering)/2, (raising-lowering)/(2j), np.diag(m)])


def independent_spin(j, op):
    q = op['quaternion']
    length = np.linalg.norm(q[:3])
    if length < 1e-14:
        return np.eye(round(2*j+1))*q[3]**round(2*j)
    angle = 2*np.arctan2(length, q[3])
    return expm(-1j*angle*np.einsum('a,aij->ij', q[:3]/length, angular_momentum(j)))


def test_spatial_group_closure_spin_lifts_and_character_orthogonality():
    ops = module.td_operations()
    bonds = {(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)}
    indices = {tuple(op['spatial'].ravel()): i for i, op in enumerate(ops)}
    assert len(indices) == 24
    for a in ops:
        assert {tuple(a['spatial']@b) for b in bonds} == bonds
        assert np.allclose(a['spin'].conj().T@a['spin'], np.eye(2), atol=2e-15)
        for b in ops:
            c = ops[indices[tuple((a['spatial']@b['spatial']).ravel())]]
            spin = a['spin']@b['spin']
            assert min(np.linalg.norm(spin-c['spin']), np.linalg.norm(spin+c['spin'])) < 2e-15
    chars = np.array([op['characters'] for op in ops])
    assert np.allclose(chars.conj().T@chars/24, np.eye(3), atol=2e-15)


def test_independent_j_half_and_j_three_halves_matrix_exponentials():
    for op in module.td_operations():
        assert np.allclose(independent_spin(.5, op), op['spin'], atol=3e-15)
        independent = op['determinant']*independent_spin(1.5, op)
        assert abs(np.trace(independent)-op['characters'][2]) < 6e-15


def test_accidental_fourfold_degeneracy_does_not_identify_Gamma8():
    ops = module.td_operations()
    chars = np.array([op['characters'] for op in ops])
    fake_quartet = np.array([np.trace(block_diag(op['spin'], op['determinant']*op['spin'])) for op in ops])
    multiplicity = chars.conj().T@fake_quartet/24
    assert np.allclose(multiplicity, [1,1,0], atol=2e-15)
    two_doublets = 2*chars[:,0]
    assert np.allclose(chars.conj().T@two_doublets/24, [2,0,0], atol=2e-15)


def test_twirl_bound_by_independent_dense_spectral_projector():
    ops = module.td_operations()
    reps = [block_diag(op['spin'], op['determinant']*op['spin']) for op in ops]
    angle = .01
    frame = np.vstack([np.eye(2)*np.cos(angle), np.eye(2)*np.sin(angle)])
    p = frame@frame.conj().T
    c = [frame.conj().T@u@frame for u in reps]
    tau = np.sqrt(max(np.linalg.norm(np.eye(2)-a.conj().T@a, 2) for a in c))
    twirl = sum(u@p@u.conj().T for u in reps)/24
    eig, vec = np.linalg.eigh(twirl)
    q = vec[:,eig>.5]@vec[:,eig>.5].conj().T
    assert np.count_nonzero(eig>.5) == 2
    assert np.linalg.norm(twirl-p, 2) <= tau+2e-14
    assert np.linalg.norm(q-p, 2) <= 2*tau+2e-14
    assert max(np.linalg.norm(u@q-q@u, 2) for u in reps) < 2e-14
    ideal = np.array([op['characters'] for op in ops])
    actual_m = ideal.conj().T@np.array([np.trace(q@u) for u in reps])/24
    compressed_m = ideal.conj().T@np.array([np.trace(a) for a in c])/24
    assert np.allclose(actual_m, [1,0,0], atol=2e-15)
    assert np.all(abs(actual_m-compressed_m) <= np.array([2,2,4])*8*tau+1e-14)


def test_saved_native_character_envelope_and_explicit_rejections():
    record = json.loads((HERE/'reference_irrep_check.json').read_text())
    ideal = np.array([op['characters'] for op in module.td_operations()])
    for label, expected in [('Gamma6',[1,0,0]), ('Gamma8',[0,0,1])]:
        sector = record['sectors'][label]
        chars = np.array([complex(*z) for z in sector['character_complex']])
        recalc = module.nearby_irrep_envelope(
            sector['Gram_defect_frobenius'], sector['maximum_span_leakage_defect_frobenius'],
            chars, ideal, 2 if label=='Gamma6' else 4, 2*record['native_plane_waves'])
        assert recalc['rounded_Gamma6_Gamma7_Gamma8_multiplicities'] == expected
        assert recalc['nearest_integer_classification_admitted_under_model']
        assert max(recalc['multiplicity_error_upper_model']) < .004
        assert recalc == {key: sector[key] for key in recalc}
    assert not record['true_HSE_eigenpair_metric_or_material_accuracy_certified']
    assert not record['failed_pilot_host_irreps_admitted']
    assert not record['native_postprocessor_invoked']
    assert record['physical_xc'] is None
    with pytest.raises(ValueError, match='physical metric'):
        module.nearby_irrep_envelope(.1, 0, ideal[:,0], ideal, 2, 2)
    with pytest.raises(ValueError, match='projector certificate'):
        module.nearby_irrep_envelope(0, .3, ideal[:,0], ideal, 2, 2)


def test_saved_native_source_and_helper_hashes():
    record = json.loads((HERE/'reference_irrep_check.json').read_text())
    assert module.digest(HERE/'reference_irrep_check.py') == record['driver_sha256']
    for path, expected in record['source_sha256'].items():
        assert module.digest(path) == expected
