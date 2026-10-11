#!/usr/bin/env python3
"""Oriented Te p-onsite identity audit; unspecified material amplitudes."""
import argparse
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import subprocess

import numpy as np


def exact_rank(matrix):
    rows = [[Fraction(v) for v in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][column]
        rows[rank] = [v/divisor for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                scale = rows[i][column]
                rows[i] = [a-scale*b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('data/calculated/te_p_tensor_tomography_audit.json'))
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Never overwrite frozen evidence')
    directions = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
    tensors = (directions[:, :, None]*directions[:, None, :]-np.eye(3)[None])/3
    group = []
    for permutation in permutations(range(3)):
        for signs in product([-1, 1], repeat=3):
            if np.prod(signs) == 1:
                rotation = np.eye(3, dtype=int)[list(permutation)]*np.array(signs)[:, None]
                mapping = [int(np.flatnonzero(np.all(directions == rotation @ d, axis=1))[0]) for d in directions]
                group.append((rotation, mapping))
    components = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    basis = []
    for i, j in components:
        tensor = np.zeros((3, 3), int)
        tensor[i, j] = tensor[j, i] = 1
        basis.append(tensor)
    dimensions = []
    for mask in [0, 1, 3, 14, 15]:
        selected = {i for i in range(4) if mask & (1 << i)}
        stabilizer = [rotation for rotation, mapping in group if {mapping[i] for i in selected} == selected]
        constraints = []
        for rotation in stabilizer:
            action = np.array([[int((rotation @ tensor @ rotation.T)[i, j]) for tensor in basis] for i, j in components])
            constraints.extend((action-np.eye(6, dtype=int)).tolist())
        dimensions.append(dict(N=mask.bit_count(), stabilizer_order=len(stabilizer), exact_dimension=6-exact_rank(constraints)))
    assert [row['exact_dimension'] for row in dimensions] == [1, 2, 3, 2, 1]
    pair_E, pair_B = {}, {}
    for i in range(4):
        for j in range(i+1, 4):
            axis = directions[i]+directions[j]
            pair_E[i, j] = np.eye(3)/3-np.outer(axis, axis)/float(axis @ axis)
            pair_B[i, j] = tensors[i]+tensors[j]
    rng = np.random.default_rng(110746)
    h1, h2, h3, a1, a3, e2, b2 = rng.normal(size=7)
    c = a3-a1+2*b2
    values = {}
    for mask in range(16):
        sites = [i for i in range(4) if mask & (1 << i)]
        if len(sites) == 1:
            value = h1*np.eye(3)+a1*tensors[sites[0]]
        elif len(sites) == 2:
            pair = tuple(sites)
            value = h2*np.eye(3)+e2*pair_E[pair]+b2*pair_B[pair]
        elif len(sites) == 3:
            missing = next(i for i in range(4) if i not in sites)
            value = h3*np.eye(3)+a3*tensors[missing]
        else:
            value = np.zeros((3, 3))
        values[mask] = value
    group_error = 0.
    for rotation, mapping in group:
        for mask, value in values.items():
            transformed = sum(1 << mapping[i] for i in range(4) if mask & (1 << i))
            group_error = max(group_error, float(np.linalg.norm(values[transformed]-rotation @ value @ rotation.T)))
    def inner(a, b):
        return float(np.einsum('ij,ij->', a, b))
    extracted = [np.trace(values[m])/3 for m in [1, 3, 14]]
    extracted.extend([inner(values[1], tensors[0])/inner(tensors[0], tensors[0]),
        inner(values[14], tensors[0])/inner(tensors[0], tensors[0]),
        inner(values[3], pair_E[0, 1])/inner(pair_E[0, 1], pair_E[0, 1]),
        inner(values[3], pair_B[0, 1])/inner(pair_B[0, 1], pair_B[0, 1])])
    extraction_error = float(np.max(np.abs(np.array(extracted)-[h1, h2, h3, a1, a3, e2, b2])))
    directional = {mask:value-np.trace(value)/3*np.eye(3) for mask, value in values.items()}
    raw = {mask:sum(((-1)**(mask.bit_count()-sub.bit_count())*directional[sub]
                   for sub in range(16) if sub & mask == sub), start=np.zeros((3, 3))) for mask in range(16)}
    rows = []
    for x in [.17, .2, .5, .83]:
        k = x*(1-x)
        beta1 = a1+2*x*(b2-a1)-c*x*x
        beta2 = b2-a1-c*x
        mean = sum((x**mask.bit_count()*(1-x)**(4-mask.bit_count())*value for mask, value in values.items()), start=np.zeros((3, 3)))
        mean_prediction = (4*x*(1-x)**3*h1+6*x*x*(1-x)**2*h2+4*x**3*(1-x)*h3)*np.eye(3)
        variance = sum(x**mask.bit_count()*(1-x)**(4-mask.bit_count())*inner(value, value) for mask, value in directional.items())
        prediction = 8/3*k*beta1**2+k*k*(4*e2**2+16/3*beta2**2)+8/3*k**3*c*c
        vertex_error = 0.
        for mask in range(1, 16):
            sites = [i for i in range(4) if mask & (1 << i)]
            vertex = sum((raw[sup]*x**(sup.bit_count()-mask.bit_count()) for sup in range(16) if sup & mask == mask), start=np.zeros((3, 3)))
            if len(sites) == 1:
                expected = beta1*tensors[sites[0]]
            elif len(sites) == 2:
                pair = tuple(sites)
                expected = e2*pair_E[pair]+beta2*pair_B[pair]
            elif len(sites) == 3:
                expected = c*tensors[next(i for i in range(4) if i not in sites)]
            else:
                expected = np.zeros((3, 3))
            vertex_error = max(vertex_error, float(np.linalg.norm(vertex-expected)))
        rows.append(dict(x=x, coherent_error=float(np.linalg.norm(mean-mean_prediction)),
            centered_directional_vertex_max_error=vertex_error,
            direct_directional_Frobenius_variance=float(variance),
            predicted_directional_Frobenius_variance=float(prediction),
            variance_error=float(abs(variance-prediction))))
    fourier = []
    for q in [np.zeros(3), np.array([0., 0., 2*np.pi]), *rng.normal(size=(12, 3))*8]:
        phase = np.exp(1j*directions @ q/4)
        f0 = phase.sum()
        fxyz = phase @ directions
        gamma = np.einsum('i,ijk->jk', phase, tensors)
        norm = float(np.linalg.norm(gamma, 'fro')**2)
        predicted = 2/9*(16-abs(f0)**2)
        fourier.append(dict(q_times_lattice_constant=q.tolist(), scalar_form_factor_squared=float(abs(f0)**2),
            hadamard_sum_error=float(abs(abs(f0)**2+np.sum(np.abs(fxyz)**2)-16)),
            directional_vertex_Frobenius_squared=norm,
            complementary_norm_error=float(abs(norm-predicted))))
    max_error = max(group_error, extraction_error,
        *(max(row['coherent_error'], row['centered_directional_vertex_max_error'], row['variance_error']) for row in rows),
        *(max(row['hadamard_sum_error'], row['complementary_norm_error']) for row in fourier))
    assert max_error < 1e-12
    record = dict(claim_status='CALCULATED exhaustive algebra/geometry audit; no material amplitude or alloy fit',
        git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        empirical_alloy_gap_inputs=[], assumptions=['fixed four-neighbor ideal Td geometry',
            'real symmetric spin-independent p-onsite tensors in one Cartesian frame',
            'independent Bernoulli occupations; translationally identical Te frames'],
        amplitude_status='seven arbitrary audit parameters; no HgCdTe calibration',
        stabilizer_dimensions=dimensions, endpoint_invisible_parameter_dimension=7,
        coherent_parameter_dimension=3, hidden_directional_parameter_dimension=4,
        tetrahedral_group_elements=len(group), configurations=16,
        group_covariance_max_error=group_error, representative_extraction_error=extraction_error,
        directional_raw_four_body_norm=float(np.linalg.norm(raw[15])),
        concentration_controls=rows, Fourier_controls=fourier, maximum_audit_error=max_error,
        limits=['No physical impurity potential, spectral susceptibility, linewidth or inversion is calculated',
            'SOC, other orbitals, hopping tensors and background dependence are outside this restricted classification',
            'Full physical T-matrix endpoint slopes can contain directional scattering even when coherent M derivatives cannot'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'stabilizer_dimensions':dimensions, 'maximum_audit_error':max_error,
                      'four_body_directional_norm':record['directional_raw_four_body_norm']}, indent=2))


if __name__ == '__main__':
    main()
