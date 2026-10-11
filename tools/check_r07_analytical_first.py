#!/usr/bin/env python3
"""Small independent R07 identity checks; no DFT, physical inputs or gap fit."""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import subprocess

import numpy as np

from mct_research.analytical_gap_closure import (
    DiscreteFeshbachMeasure,
    covariance_resolvent_error_bound,
    mass_root_error_bound,
)


def angular_operators():
    pauli = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]],
                      [[1, 0], [0, -1]]], complex)
    angular = np.array([[[0, 0, 0], [0, 0, -1j], [0, 1j, 0]],
                        [[0, 0, 1j], [0, 0, 0], [-1j, 0, 0]],
                        [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]])
    def spin_tensor(t):
        return sum((t[i, j] * np.kron(angular[i], pauli[j])
                    for i in range(3) for j in range(3)), start=np.zeros((6, 6), complex))
    so = spin_tensor(np.eye(3))
    p8, p7 = (so + 2*np.eye(6))/3, (np.eye(6)-so)/3
    directions = np.array([[1, 1, 1], [1, -1, -1],
                           [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
    tensors = [np.outer(n, n)-np.eye(3)/3 for n in directions]
    disturbances = [2*np.kron(t, np.eye(2))+spin_tensor(t) for t in tensors]
    return p8, p7, tensors, disturbances, spin_tensor


def directional_records():
    p8, p7, tensors, disturbances, spin_tensor = angular_operators()
    e8, e7, x, z = 0.0, -0.7, 0.23, 0.22+0.11j
    host = e8*p8+e7*p7
    g0 = np.linalg.inv(z*np.eye(6)-host)
    k = x*(1-x)
    records = []
    for strength in (0.02, 0.01, 0.005):
        avg_g, avg_w, moment2 = (np.zeros((6, 6), complex) for _ in range(3))
        for occupations in product((0, 1), repeat=4):
            n = sum(occupations)
            probability = x**n*(1-x)**(4-n)
            w = strength*sum((eta*d for eta, d in zip(occupations, disturbances)),
                             start=np.zeros((6, 6), complex))
            avg_w += probability*w
            avg_g += probability*np.linalg.inv(z*np.eye(6)-host-w)
            moment2 += probability*w@w
        g8 = np.trace(p8@avg_g)/4
        self_energy = z-e8-1/g8
        born = 4*strength**2*k/(z-e7)
        np.testing.assert_allclose(avg_w, 0, atol=1e-15)
        np.testing.assert_allclose(p8@moment2@p8, 4*strength**2*k*p8, atol=1e-15)
        np.testing.assert_allclose(p8@avg_g@p8, g8*p8, atol=1e-15)
        assert np.linalg.eigvalsh(-(avg_g-avg_g.conj().T)/(2j)).min() > 0
        records.append({"strength_eV": strength,
                        "exact_sigma8_eV": [self_energy.real, self_energy.imag],
                        "born_sigma8_eV": [born.real, born.imag],
                        "absolute_error_eV": float(abs(self_energy-born)),
                        "coherent_response_norm_eV": float(np.linalg.norm(avg_w))})
    ratios = [records[i]["absolute_error_eV"]/records[i+1]["absolute_error_eV"]
              for i in range(2)]
    assert all(15 < value < 17 for value in ratios), ratios
    # Check the trace contractions independently, for an arbitrary traceless tensor.
    t = np.array([[0.2, 0.3, -0.4], [0.3, -0.1, 0.15], [-0.4, 0.15, -0.1]])
    a, alpha = 0.21, -0.08
    d = a*np.kron(t, np.eye(2))+alpha*spin_tensor(t)
    b8 = np.trace(p8@d@g0@d@p8)/4
    predicted = np.linalg.norm(t)**2/6*((a-2*alpha)**2/(z-e8)+(a+alpha)**2/(z-e7))
    np.testing.assert_allclose(b8, predicted, atol=1e-15)
    return {"assumptions": "isotropic atomic p propagator; synthetic e8/e7; spectator Gamma6",
            "composition": x, "records": records,
            "fourth_order_error_ratios": ratios,
            "two_invariant_trace_error_eV": float(abs(b8-predicted))}


def bisect_root(function, low=0.0, high=1.0):
    if function(low)*function(high) >= 0:
        raise ValueError("A strict root bracket is required")
    for _ in range(70):
        mid = (low+high)/2
        if function(mid)*function(low) > 0:
            low = mid
        else:
            high = mid
    return (low+high)/2


def moment_records():
    energies = np.array([0.5, 1.0, -1.0, -0.5])
    direction = np.array([1, -2, 2, -1])
    base, epsilon = 0.02, 0.2
    measures = [DiscreteFeshbachMeasure(energies, base*(1+sign*epsilon*direction))
                for sign in (-1, 1)]
    records = []
    for measure in measures:
        c, a, distance = measure.moments(0)
        half_width = 0.2
        bound = measure.linearization_bound(0, half_width)
        error = max(abs(measure.kernel(e)-(c-a*e))
                    for e in np.linspace(-half_width, half_width, 81))
        assert error <= bound
        value = measure.kernel(0.1).real
        root = bisect_root(lambda x: 1.6*(x-0.23)+x*(1-x)*value)
        records.append({"weights_eV2": measure.weights.tolist(),
                        "total_weight_eV2": float(sum(measure.weights)),
                        "C_eV": c, "A": a, "support_distance_eV": distance,
                        "kernel_at_point1_eV": value, "synthetic_root": root,
                        "linear_bound_eV": bound, "sampled_error_eV": float(error)})
    assert abs(records[0]["synthetic_root"]-records[1]["synthetic_root"]) > 1e-5
    return {"material_prediction": False, "records": records}


def endpoint_records():
    # Exact combinatorial coefficient proof, independent of floating point jets.
    records = []
    for order in range(1, 5):
        r, n = order+1, 2*(order+1)
        coefficients = [Fraction(0) for _ in range(n+1)]
        for j in range(r+1):
            coefficients[r+j] = Fraction(comb(n, r)*comb(r, j)*(-1)**j)
        assert all(c == 0 for c in coefficients[:order+1])
        # The balanced probability is invariant under x -> 1-x.
        transformed = [sum((coefficients[i]*comb(i, j)*(-1)**j
                            for i in range(j, n+1)), start=Fraction(0)) for j in range(n+1)]
        assert transformed == coefficients
        records.append({"endpoint_jet_order": order, "neighbors": n,
                        "midpoint_event_probability": float(Fraction(comb(n, r), 2**n))})
    return records


def run_checks():
    return {"scope": "mathematical checks and counterexamples only; no material validation",
            "directional_gap_channel": directional_records(),
            "same_moments_different_crossing": moment_records(),
            "exact_hidden_endpoint_events": endpoint_records(),
            "illustrative_root_budget": mass_root_error_bound(0.002, 0.001, 2, 0.4, 0.5),
            "illustrative_covariance_resolvent_bound": covariance_resolvent_error_bound(0.1, 1)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("data/calculated/r07_analytical_first_audit.json"))
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Do not overwrite frozen scientific evidence")
    result = run_checks()
    paths = [Path(__file__), Path("src/mct_research/analytical_gap_closure.py")]
    result["source_hashes"] = {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in paths}
    result["parent_commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    result["numpy_version"] = np.__version__
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(f"Independent synthetic checks passed; evidence: {args.output}")


if __name__ == "__main__":
    main()
