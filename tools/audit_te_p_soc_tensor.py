#!/usr/bin/env python3
"""Spinful p-onsite tensor audit; no physical response coefficients."""
import argparse
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import subprocess

import numpy as np

from audit_te_p_tensor_tomography import exact_rank


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('data/calculated/te_p_soc_tensor_audit.json'))
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Never overwrite frozen evidence')
    sigmas = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex)
    angular = np.array([[[0, 0, 0], [0, 0, -1j], [0, 1j, 0]],
                        [[0, 0, 1j], [0, 0, 0], [-1j, 0, 0]],
                        [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]])
    def spin_tensor(t):
        return sum((t[i, j]*np.kron(angular[i], sigmas[j]) for i in range(3) for j in range(3)), start=np.zeros((6, 6), complex))
    scalar_so = spin_tensor(np.eye(3))
    p8, p7 = (scalar_so+2*np.eye(6))/3, (np.eye(6)-scalar_so)/3
    np.testing.assert_allclose(np.linalg.eigvalsh(scalar_so), [-2, -2, 1, 1, 1, 1], atol=1e-14)
    directions = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    group = []
    for perm in permutations(range(3)):
        for signs in product([-1, 1], repeat=3):
            if np.prod(signs) != 1:
                continue
            q = np.eye(3, dtype=int)[list(perm)]*np.array(signs)[:, None]
            mapping = [int(np.flatnonzero(np.all(directions == q @ d, axis=1))[0]) for d in directions]
            group.append((q, mapping))
    full_basis = []
    for i in range(3):
        for j in range(3):
            t = np.zeros((3, 3), int); t[i, j] = 1
            full_basis.append(t)
    dimensions = []
    for mask in [0, 1, 3, 14, 15]:
        sites = {i for i in range(4) if mask & (1 << i)}
        stabilizer = [q for q, mapping in group if {mapping[i] for i in sites} == sites]
        constraints = []
        for q in stabilizer:
            action = np.column_stack([(q @ t @ q.T).ravel() for t in full_basis])
            constraints.extend((action-np.eye(9, dtype=int)).tolist())
        dimension = 9-exact_rank(constraints)
        dimensions.append(dict(N=mask.bit_count(), stabilizer_order=len(stabilizer), exact_B_dimension=dimension))
    assert [row['exact_B_dimension'] for row in dimensions] == [1, 2, 3, 2, 1]
    theta = np.kron(np.eye(3), 1j*sigmas[1])
    real_symmetric = []
    for i in range(3):
        for j in range(i, 3):
            t = np.zeros((3, 3)); t[i, j] = t[j, i] = 1
            real_symmetric.append(t)
    even_basis = [np.kron(t, np.eye(2)) for t in real_symmetric]
    even_basis.extend(np.kron(l, sigma) for l in angular for sigma in sigmas)
    gram = np.array([[np.trace(a.conj().T @ b).real for b in even_basis] for a in even_basis])
    assert np.linalg.matrix_rank(gram) == 15
    tr_error = max(float(np.linalg.norm(theta @ h.conj() @ theta.conj().T-h)) for h in even_basis)
    rng = np.random.default_rng(115326)
    rotation_errors = []
    for q, _ in group:
        proper = int(round(np.linalg.det(q)))*q
        trace = np.trace(proper)
        if trace > -1:
            w = np.sqrt(1+trace)/2
            vector = np.array([proper[2, 1]-proper[1, 2], proper[0, 2]-proper[2, 0], proper[1, 0]-proper[0, 1]])/(4*w)
        else:
            axis_projector = (proper+np.eye(3))/2
            pivot = int(np.argmax(np.diag(axis_projector)))
            vector = axis_projector[:, pivot]/np.sqrt(axis_projector[pivot, pivot]); w = 0.
        spin_u = w*np.eye(2)-1j*np.einsum('i,ijk->jk', vector, sigmas)
        physical_u = np.kron(q, spin_u)
        b = rng.normal(size=(3, 3))
        rotation_errors.append(float(np.linalg.norm(physical_u @ spin_tensor(b) @ physical_u.conj().T-spin_tensor(q @ b @ q.T))))
    angular_rows = []
    for t in real_symmetric:
        t = t-np.trace(t)/3*np.eye(3)
        if np.linalg.norm(t) == 0:
            continue
        a = np.kron(t, np.eye(2)); s = spin_tensor(t)
        expected_norm = 2/3*np.linalg.norm(t, 'fro')**2
        intra_norm = float(np.linalg.norm(p8 @ a @ p8, 'fro')**2)
        inter_norm = float(np.linalg.norm(p8 @ a @ p7, 'fro')**2)
        cancellation = a+.5*s
        angular_rows.append(dict(anticommutator_error=float(np.linalg.norm(scalar_so @ a+a @ scalar_so+s)),
            j_half_block_norm=float(np.linalg.norm(p7 @ a @ p7)),
            orbital_intra_norm_error=float(abs(intra_norm-expected_norm)),
            orbital_inter_norm_error=float(abs(inter_norm-expected_norm)),
            SOC_intra_projection_error=float(np.linalg.norm(p8 @ s @ p8+2*p8 @ a @ p8)),
            SOC_inter_projection_error=float(np.linalg.norm(p8 @ s @ p7-p8 @ a @ p7)),
            cancellation_intra_norm=float(np.linalg.norm(p8 @ cancellation @ p8)),
            cancellation_inter_norm=float(np.linalg.norm(p8 @ cancellation @ p7)),
            full_SOC_norm_error=float(abs(np.linalg.norm(s, 'fro')**2-4*np.linalg.norm(t, 'fro')**2))))
    # Independent 6x6 representative matrices and their orthogonal recovery.
    a1 = (np.outer(directions[0], directions[0])-np.eye(3))/3
    e12 = np.diag([-2, 1, 1])/3
    b12 = (np.outer(directions[0], directions[0])+np.outer(directions[1], directions[1])-2*np.eye(3))/3
    extraction_rows = []
    for tensors in [[a1], [e12, b12], [a1]]:
        basis = [np.eye(6), scalar_so]
        basis.extend(np.kron(t, np.eye(2)) for t in tensors)
        basis.extend(spin_tensor(t) for t in tensors)
        norms = np.array([np.trace(h.conj().T @ h).real for h in basis])
        inner = np.array([[np.trace(a.conj().T @ b).real for b in basis] for a in basis])
        coefficients = rng.normal(size=len(basis))
        response = sum((coefficient*h for coefficient, h in zip(coefficients, basis)), start=np.zeros((6, 6), complex))
        extracted = np.array([np.trace(h.conj().T @ response).real/norm for h, norm in zip(basis, norms)])
        extraction_rows.append(dict(parameters=len(basis), orthogonality_error=float(np.linalg.norm(inner-np.diag(norms))),
            extraction_error=float(np.max(np.abs(extracted-coefficients)))))
    maximum = max(tr_error, *rotation_errors,
        *(max(v for k,v in row.items() if k.endswith('error') or k in ['j_half_block_norm', 'cancellation_intra_norm']) for row in angular_rows),
        *(max(row['orthogonality_error'],row['extraction_error']) for row in extraction_rows))
    assert maximum < 1e-12
    record = dict(claim_status='CALCULATED spinful algebra/symmetry audit; no HgCdTe amplitude',
        git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        exact_rank_helper_sha256=hashlib.sha256(Path('tools/audit_te_p_tensor_tomography.py').read_bytes()).hexdigest(),
        empirical_alloy_gap_inputs=[], assumptions=['fixed four-bond Td-covariant local p-onsite response',
            'Hermitian and time-reversal invariant; common Cartesian/spin frame'],
        time_reversal_even_Hermitian_dimension=15, endpoint_stabilizer_B_dimensions=dimensions,
        full_configuration_parameter_dimension=18, endpoint_invisible_parameter_dimension=14,
        coherent_parameter_dimension=6, directional_parameter_dimension=8,
        TR_basis_max_error=tr_error, proper_improper_rotation_max_error=max(rotation_errors),
        angular_projection_controls=angular_rows, representative_extraction_controls=extraction_rows,
        maximum_audit_error=maximum,
        limits=['No chemical/SOC coefficient, actual Bloch branch response, gap, susceptibility or inversion is inferred',
            'Other orbitals, hopping matrices and background dependence require their full microscopic operators',
            'The conditional a=2alpha cancellation is not a proposed calibrated HgCdTe mechanism'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({key:record[key] for key in ['endpoint_invisible_parameter_dimension','coherent_parameter_dimension',
        'directional_parameter_dimension','proper_improper_rotation_max_error','maximum_audit_error']},indent=2))


if __name__ == '__main__':
    main()
