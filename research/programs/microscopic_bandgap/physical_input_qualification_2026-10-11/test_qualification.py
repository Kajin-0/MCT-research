"""Focused existing-source and synthetic proof checks; no native jobs."""
import hashlib
import json
from pathlib import Path
import importlib.util
from decimal import Decimal

import numpy as np

HERE = Path(__file__).resolve().parent


def audit():
    return json.loads((HERE / "existing_audit.json").read_text())


def test_native_physical_projection_audit_scope():
    a = audit()
    assert a["native_reference_SCF_gates"] == [True, True]
    assert a["native_source_phi_gram_error"] < 1e-12
    assert a["native_Gamma_kernel_norm_recomputed_eV"] < 5e-6
    assert not a["supervisor_records_opened"] and not a["native_jobs_launched"]
    assert not a["material_uncertainty_certified"] and a["physical_xc"] is None
    assert len(a["verified_sources_sha256"]) == 29
    assert not any(path.endswith("/state.json") for path in a["verified_sources_sha256"])


def test_native_sector_weights_and_reference_leakage():
    a = audit()
    for name, d in [("Gamma6", 2), ("Gamma8", 4)]:
        sector = a["sectors"][name]
        weights = np.array(sector["resolved_weights_without_prefix_renormalization"])
        assert len(weights) == 44 and np.all(weights >= 0)
        assert abs(weights.sum()-1) < 1e-10
        assert len(sector["native_singular_values"]) == d
        assert min(sector["native_singular_values"]) > 1-3e-12
        assert sector["maximum_matched_edge_displacement_eV"] < 5e-6
        assert len(sector["source_edge_energies_eV"]) == d
    assert a["prepared_pair"]["periodic_Cd_fraction"] == 1/8
    assert all(not v["accepted_scf"] for v in a["prepared_pair"]["SCF_members"].values())
    assert not a["existing_interior_SQS"]["Gamma_projected_spectral_contractions_present"]


def test_saved_completed_source_provenance():
    a = audit()
    for path, expected in a["verified_sources_sha256"].items():
        p = Path(path)
        if not p.is_absolute():
            p = HERE.parents[3] / p
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(262144), b""):
                h.update(chunk)
        assert h.hexdigest() == expected, path
    assert hashlib.sha256((HERE/"audit_existing.py").read_bytes()).hexdigest() == a["driver_sha256"]


def bounds_module():
    spec = importlib.util.spec_from_file_location("r07_conditional_ref_bound", HERE/"evaluate_reference_bound.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_conditional_uniform_bound_and_missing_material_budget():
    record = json.loads((HERE/"reference_bound.json").read_text())
    assert bounds_module().evaluate() == record
    assert Decimal(record["minimum_conditional_mass_floor"]) > Decimal("0.29")
    assert Decimal(record["ordering_transfer_error_bound_eV"]["hi"]) < Decimal("0.000059")
    assert record["material_error_bound_eV"] is None
    assert record["impurity_response_error_bound_eV"] is None
    assert record["native_exact_eigenpair_metric_assumption_certified"] is False


def test_quartic_window_constants_independent_critical_points():
    u = np.array([-1, -np.sqrt(3/5), -1/np.sqrt(3), -1/np.sqrt(5),
                  0., 1/np.sqrt(5), 1/np.sqrt(3), np.sqrt(3/5), 1])
    derivative_m = -4*u*(1-u*u)
    derivative_n = 1-6*u*u+5*u**4
    assert abs(np.max(np.abs(derivative_m))-8/(3*np.sqrt(3))) < 5e-16
    assert np.max(np.abs(derivative_n)) == 1
    assert np.min(derivative_n) >= -.8-5e-16
    assert abs(np.max(np.abs(u*(1-u*u)**2))-16/(25*np.sqrt(5))) < 1e-16


def test_concentrated_measure_bound_with_unknown_distant_weight():
    # Direct integral with independent positive Lorentz kernels; no antiderivative.
    module = bounds_module()
    e, weights, _ = module.arith.quadrature_grid(.5, .1, 16)
    chi_measure = weights
    def moments(t):
        density = .1/(np.pi*((e-t)**2+.1**2))
        return np.array([chi_measure@density, (e*chi_measure)@density])
    t, delta, leakage = .145, .003, .02
    ref = moments(t)
    changed = (1-leakage)*moments(t+delta)+leakage*moments(1e6)
    m_bound = 8/(3*np.sqrt(3)*.5)*delta+2*leakage
    n_bound = delta+32*.5/(25*np.sqrt(5))*leakage
    assert abs(changed[0]-ref[0]) <= m_bound
    assert abs(changed[1]-ref[1]) <= n_bound
    p = min(changed[0], ref[0])
    assert abs(changed[1]/changed[0]-ref[1]/ref[0]) <= (n_bound+.5*m_bound)/p
    # Its full unwindowed first-moment change is huge; that is not used by U1.
    assert (1-leakage)*(t+delta)+leakage*1e6-t > 1e4


def test_binary_pointwise_and_sorted_controls_fail_for_fixed_impurity():
    # Ambient dense inverse versus independently eliminated Q block.
    first = np.diag([.2, -.2, -1., 1.])
    second = np.diag([.2, -.2, 1., -1.])
    p = np.eye(4)[:, :2]
    v = np.zeros((4, 4)); v[0, 2] = v[2, 0] = .4
    assert np.array_equal(np.linalg.eigvalsh(first), np.linalg.eigvalsh(second))
    for z in (.05j, .1+.2j, -.3+.1j):
        source_r = p.T @ np.linalg.inv(z*np.eye(4)-first) @ p
        second_r = p.T @ np.linalg.inv(z*np.eye(4)-second) @ p
        np.testing.assert_array_equal(source_r, second_r)
        k = []
        for host, remote in [(first, -1), (second, 1)]:
            r = p.T @ np.linalg.inv(z*np.eye(4)-host-v) @ p
            reaction = z*np.eye(2)-host[:2, :2]-np.linalg.inv(r)
            expected = np.diag([.16/(z-remote), 0])
            np.testing.assert_allclose(reaction, expected, atol=3e-16, rtol=0)
            assert np.linalg.eigvalsh(-((reaction-reaction.conj().T)/(2j))).min() >= -1e-16
            k.append(reaction)
        assert np.linalg.norm(k[0]-k[1]) > .25
        if z.real == 0:
            assert k[0][0, 0].real > 0 > k[1][0, 0].real
