#!/usr/bin/env python3
"""Exhaustive controls for oriented tetrahedral response; no material fit."""
import argparse
from fractions import Fraction
from itertools import product, permutations
import hashlib
import json
from math import comb, factorial
from pathlib import Path
import subprocess

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('data/calculated/oriented_tetrahedron_audit.json'))
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Never overwrite frozen evidence')
    directions = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    exact = [[[Fraction(int(d[i]*d[j]-(i == j)), 3) for j in range(3)] for i in range(3)] for d in directions]
    assert all(sum(exact[m][i][j] for m in range(4)) == 0 for i in range(3) for j in range(3))
    quadrupoles = (directions[:, :, None]*directions[:, None, :]-np.eye(3)[None])/3
    configurations = np.array(list(product([0, 1], repeat=4)))
    local_values = np.einsum('cm,mij->cij', configurations, quadrupoles)
    rotations = []
    covariance_errors = []
    for perm in permutations(range(3)):
        for signs in product([-1, 1], repeat=3):
            if np.prod(signs) != 1:
                continue
            rotation = np.eye(3, dtype=int)[list(perm)]*np.asarray(signs)[:, None]
            mapping = [int(np.flatnonzero(np.all(directions == rotation @ d, axis=1))[0]) for d in directions]
            for config, value in zip(configurations, local_values):
                transformed = np.zeros(4, int)
                transformed[mapping] = config
                rotated_response = np.einsum('m,mij->ij', transformed, quadrupoles)
                covariance_errors.append(float(np.max(np.abs(rotated_response-rotation @ value @ rotation.T))))
            rotations.append(rotation.tolist())
    phases = np.array([1j, -1j, -1j, 1j])
    gx = np.einsum('m,mij->ij', phases, quadrupoles)
    expected = np.zeros((3, 3), complex)
    expected[0, 1] = expected[1, 0] = 4j/3
    np.testing.assert_allclose(gx, expected, atol=1e-14)
    rows = []
    for x in [.17, .2, .5, .83]:
        probability = x**configurations.sum(axis=1)*(1-x)**(4-configurations.sum(axis=1))
        mean = np.einsum('c,cij->ij', probability, local_values)
        variance = float(np.einsum('c,cij,cij->', probability, local_values, local_values))
        predicted = 8*x*(1-x)/3
        np.testing.assert_allclose(mean, 0, atol=1e-14)
        np.testing.assert_allclose(variance, predicted, atol=1e-14)
        rows.append(dict(x=x, coherent_norm=float(np.linalg.norm(mean)),
            normalized_local_Frobenius_variance=variance, predicted_local_variance=predicted,
            normalized_X_Frobenius_variance=float(x*(1-x)*np.linalg.norm(gx, 'fro')**2)))
    # Independent arbitrary complex Hermitian response: exhaustive 16-event
    # covariance versus centered subsets, derivatives, and the positive floor.
    rng = np.random.default_rng(4082)
    arbitrary = {}
    for mask in range(16):
        a = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
        arbitrary[mask] = (a+a.conj().T)/2 if mask not in [0, 15] else np.zeros((3, 3), complex)
    raw = {mask:sum(((-1)**(mask.bit_count()-sub.bit_count())*arbitrary[sub]
                     for sub in range(16) if sub & mask == sub), start=np.zeros((3, 3), complex))
           for mask in range(16)}
    closure = []
    for x in [.17, .2, .5, .83]:
        k = x*(1-x)
        probabilities = {mask:x**mask.bit_count()*(1-x)**(4-mask.bit_count()) for mask in range(16)}
        mean = sum((probabilities[mask]*arbitrary[mask] for mask in range(16)), start=np.zeros((3, 3), complex))
        direct = sum((probabilities[mask]*np.outer((arbitrary[mask]-mean).ravel(), (arbitrary[mask]-mean).ravel().conj()) for mask in range(16)), start=np.zeros((9, 9), complex))
        vertices = {mask:sum((raw[sup]*x**(sup.bit_count()-mask.bit_count()) for sup in range(16) if sup & mask == mask), start=np.zeros((3, 3), complex)) for mask in range(1, 16)}
        exact_cov = sum((k**mask.bit_count()*np.outer(v.ravel(), v.ravel().conj()) for mask, v in vertices.items()), start=np.zeros((9, 9), complex))
        floor = np.zeros((9, 9), complex)
        directional = np.zeros_like(floor)
        derivative_errors = []
        for m in range(1, 5):
            blocks = [v for mask, v in vertices.items() if mask.bit_count() == m]
            average = sum(blocks, start=np.zeros((3, 3), complex))/comb(4, m)
            derivative = sum((factorial(mask.bit_count())/factorial(mask.bit_count()-m)*raw[mask]*x**(mask.bit_count()-m) for mask in range(16) if mask.bit_count() >= m), start=np.zeros((3, 3), complex))
            derivative_errors.append(float(np.linalg.norm(average-derivative/(factorial(m)*comb(4, m)))))
            floor += comb(4, m)*k**m*np.outer(average.ravel(), average.ravel().conj())
            for vertex in blocks:
                delta = (vertex-average).ravel()
                directional += k**m*np.outer(delta, delta.conj())
        err_direct = float(np.linalg.norm(direct-exact_cov))
        err_split = float(np.linalg.norm(exact_cov-floor-directional))
        if max(err_direct, err_split, *derivative_errors) > 1e-11:
            raise ValueError('General oriented cluster identity failed')
        closure.append(dict(x=x, direct_vs_cluster_covariance_error=err_direct,
            mean_vertex_derivative_max_error=max(derivative_errors),
            floor_plus_directional_decomposition_error=err_split,
            minimum_directional_covariance_eigenvalue=float(np.linalg.eigvalsh(directional).min()),
            directional_covariance_trace=float(np.trace(directional).real)))
    record = dict(claim_status='CALCULATED exact-combinatorial identity audit; unit response, no material coefficient',
        git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        empirical_alloy_gap_inputs=[], amplitude='lambda left unspecified; numerical tensors normalized to lambda=1',
        source_geometry='Fixed ideal zincblende tetrahedral bond directions',
        prior_art='Niquet et al., PRB79,245201 (2009), Eq.(10); https://arxiv.org/pdf/0902.0491; angular tensor precedent, not HgCdTe calibration',
        rational_endpoint_sum_is_exactly_zero=True,
        tetrahedral_group_elements=len(rotations), oriented_configurations=16,
        group_covariance_max_error=max(covariance_errors),
        X_vertex_error=float(np.linalg.norm(gx-expected)), normalized_X_vertex=[[dict(real=float(v.real), imag=float(v.imag)) for v in row] for row in gx],
        directional_counterexample=rows, general_covariance_closure=closure,
        consequences=['Coherent configurational derivatives determine order-averaged vertices only',
            'Full oriented covariance is the Bernstein floor plus positive directional terms',
            'A directional one-body response can survive a scalar tetrahedral form-factor zero',
            'Centered-subset orthogonality and white m>=2 zincblende configurational channels remain intact'],
        limits=['No HgCdTe lambda, gap shift, dynamic susceptibility or inversion is computed',
            'Count-symmetric closure remains exact under its additional equal-matrix assumption',
            'A actual impurity extraction must retain common-frame orbital directions before averaging'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'group_elements':len(rotations), 'group_covariance_max_error':max(covariance_errors),
                      'X_vertex_error':record['X_vertex_error'], 'counterexample':rows,
                      'closure_max_error':max(max(r['direct_vs_cluster_covariance_error'],r['floor_plus_directional_decomposition_error']) for r in closure)}, indent=2))


if __name__ == '__main__':
    main()
