"""Independent synthetic checks; no claim of physical material validation."""

from decimal import Decimal
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("centroid_registered_study", HERE / "run_study.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)
I = study.I


def contains(enclosure, value):
    return enclosure.lo <= value <= enclosure.hi


def test_elementary_outward_arithmetic_independent_rationals():
    # Fraction endpoints avoid validating an interval with its own midpoint.
    for left, right in [(1, 3), (-7, 9), (19, 11)]:
        result = I(left) / right
        exact = Fraction(left, right)
        assert Fraction(result.lo) <= exact <= Fraction(result.hi)
    assert contains(I("-0.3", "0.2")**2, Decimal("0.09"))
    assert contains(I("-0.3", "0.2")**2, Decimal(0))
    with pytest.raises(ZeroDivisionError):
        I(1) / I(-1, 1)
    with pytest.raises(TypeError):
        I(0.1)


def test_pi_atan_log_independent_high_precision_constants():
    # Each independent published mathematical constant is bracketed to 50 digits.
    # The computed 32-digit enclosure must contain BOTH bracket endpoints.
    lower = Decimal("3.14159265358979323846264338327950288419716939937510")
    upper = Decimal("3.14159265358979323846264338327950288419716939937511")
    assert contains(study.PI, lower) and contains(study.PI, upper)
    log_lower = Decimal("0.69314718055994530941723212145817656807550013436025")
    log_upper = Decimal("0.69314718055994530941723212145817656807550013436026")
    logarithm = study.ln_interval(I(2))
    assert contains(logarithm, log_lower) and contains(logarithm, log_upper)
    at_zero = study.atan_interval(I(0))
    assert contains(at_zero, Decimal(0))
    at_one = study.atan_interval(I(1))
    quarter = study.PI / 4
    assert max(at_one.lo, quarter.lo) <= min(at_one.hi, quarter.hi)
    for value in ("0.49", "0.8", "1.1", "17"):
        positive = study.atan_interval(I(value))
        negative = study.atan_interval(-I(value))
        assert negative.lo == positive.hi.copy_negate()
        assert negative.hi == positive.lo.copy_negate()


@pytest.mark.parametrize("a", [-1, 0, 1])
def test_exact_normalization_coherent_and_endpoint_controls(a):
    # Exact rational calculation independent of Decimal interval/model helpers.
    satellite = [(1, Fraction(2, 5)*(1+a)), (-1, Fraction(2, 5)*(1-a)),
                 (4, Fraction(1, 10)*(1-a)), (-4, Fraction(1, 10)*(1+a))]
    assert all(w >= 0 for _, w in satellite)
    assert sum(w for _, w in satellite) == 1
    assert sum(t*w for t, w in satellite) == 0
    for x_string in study.REG["composition"] + ["0", "1"]:
        x = Fraction(x_string)
        h, e, b = 16*(x*(1-x))**2, -Fraction(3, 10)+Fraction(11, 10)*x, Fraction(1, 20)
        assert 0 <= h <= 1
        assert (1-h) + h*b + sum(h*(1-b)*w for _, w in satellite) == 1
        assert (1-h)*e + sum(h*(1-b)*t*w for t, w in satellite) == (1-h)*e
    # h=16x²-32x³+16x⁴ and h'=32x-96x²+64x³: first spectral jets agree.
    for x in (0, 1):
        assert 16*x**2-32*x**3+16*x**4 == 0
        assert 32*x-96*x**2+64*x**3 == 0


@pytest.mark.parametrize("a", [-1, 0, 1])
def test_fixed_projection_dense_resolvent_proxy(a):
    # Two-node quadrature bath is a finite proxy for an INDEPENDENT adapter test.
    # It is not used in the continuum scan or certified as its approximation.
    x, b = .35, .05
    h, e = 16*(x*(1-x))**2, -.3+1.1*x
    weights = np.array([.4*(1+a), .4*(1-a), .1*(1-a), .1*(1+a)])
    levels = np.array([e, 1, -1, 4, -4, -2/np.sqrt(3), 2/np.sqrt(3)])
    retained = np.eye(7)[0]
    cloud = np.r_[0., np.sqrt((1-b)*weights), np.sqrt(b/2), np.sqrt(b/2)]
    c, s = np.sqrt(1-h), np.sqrt(h)
    u = (np.eye(7) + (c-1)*(np.outer(retained, retained)+np.outer(cloud, cloud))
         + s*(np.outer(cloud, retained)-np.outer(retained, cloud)))
    assert np.allclose(u.T @ u, np.eye(7), atol=2e-15, rtol=0)
    ham = u.T @ np.diag(levels) @ u
    assert np.allclose(ham, ham.T, atol=1e-15, rtol=0)
    for z in (.07+.13j, -1.4+.2j, 3+.7j):
        dense = retained @ np.linalg.solve(z*np.eye(7)-ham, retained)
        spectral = (1-h)/(z-e) + h*(1-b)*np.sum(weights/(z-levels[1:5])) + h*b/2*np.sum(1/(z-levels[5:]))
        assert abs(dense-spectral) < 5e-14
        assert dense.imag < 0  # Retarded Stieltjes convention.


@pytest.mark.parametrize("t,w,eta", [("0", ".5", ".05"), ("-4", "1.5", ".10"), ("1", "5", ".20")])
def test_atom_primitive_against_direct_positive_quadrature(t, w, eta):
    m, n, _ = study.atom_integrals(Decimal(t), Decimal(w), Decimal(eta))
    # Direct kernel integration, not recurrence/antiderivatives.
    e, weights, _ = study.quadrature_grid(float(w), float(eta), 16)
    density = float(eta)/(np.pi*((e-float(t))**2+float(eta)**2))
    assert abs(float(m.midpoint()) - weights @ density) < 2e-12
    assert abs(float(n.midpoint()) - (weights*e) @ density) < 2e-12


def test_uniform_bath_symmetry_and_direct_integration():
    for w, eta in [(".5", ".05"), ("1.5", ".10"), ("5", ".20")]:
        mass, moment = study.uniform_integrals(Decimal(w), Decimal(eta), Decimal(2))
        e, weights, bath = study.quadrature_grid(float(w), float(eta), 16)
        assert abs(float(mass.midpoint()) - weights @ bath) < 2e-12
        assert abs((weights*e) @ bath) < 1e-15
        assert moment.lo == moment.hi == 0


def test_energy_units_and_joint_reference_covariance():
    # Pointwise Lorentz/window identity under E->scale*E+delta, t->scale*t+delta,
    # window reference->delta, eta/W->scale*(eta/W). The Jacobian cancels for m.
    e = np.linspace(-.5, .5, 41)
    t, w, eta = -.08, .5, .1
    scale, delta = 1000., 7.
    kernel = eta/(np.pi*((e-t)**2+eta**2))
    shifted = scale*eta/(np.pi*((scale*e+delta-(scale*t+delta))**2+(scale*eta)**2))
    assert np.allclose(scale*shifted, kernel, rtol=3e-15, atol=3e-15)
    chi = (1-(e/w)**2)**2
    transformed = (1-((scale*e+delta-delta)/(scale*w))**2)**2
    assert np.allclose(transformed, chi, rtol=3e-15, atol=3e-15)
    m, n, _ = study.atom_integrals(Decimal("-.08"), Decimal(".5"), Decimal(".1"))
    ms, ns, _ = study.atom_integrals(Decimal("-80"), Decimal("500"), Decimal("100"))
    assert max(m.lo, ms.lo) <= min(m.hi, ms.hi)
    scaled_n = n * 1000
    assert max(scaled_n.lo, ns.lo) <= min(scaled_n.hi, ns.hi)


def saved_results():
    return json.loads((HERE / "results.json").read_text())


def test_registered_grid_sources_and_code_pins():
    result = saved_results()
    metadata, rows = result["metadata"], result["rows"]
    assert metadata["preregistration_commit"].startswith("5347d3c")
    assert metadata["registration_sha256"] == study.sha256(HERE / "registration.json")
    assert metadata["runner_sha256"] == study.sha256(HERE / "run_study.py")
    committed = subprocess.check_output(["git", "show", f"{metadata['preregistration_commit']}:{(HERE / 'registration.json').relative_to(study.ROOT)}"], cwd=study.ROOT)
    assert committed == (HERE / "registration.json").read_bytes()
    expected = set(itertools.product(study.REG["composition"], study.REG["alternatives"], study.REG["window_half_widths_eV"], study.REG["eta_eV"]))
    actual = [(r["x"], r["alternative"], r["W_eV"], r["eta_eV"]) for r in rows]
    assert len(rows) == 135 and len(set(actual)) == 135 and set(actual) == expected
    assert metadata["physical_material_validation"] is False
    for source in study.REG["sources"]:
        assert study.sha256(study.ROOT/source["path"]) == source["sha256"]


def test_postscan_export_fix_preserves_integration_code_and_rows():
    # Only post-scan runner edit: explicitly export LF rather than CSV-default
    # CRLF. Reconstruct its original source hash, and pin every numerical row.
    original = (HERE / "run_study.py").read_bytes().replace(b', lineterminator="\\n"', b'')
    assert hashlib.sha256(original).hexdigest() == "65d2a7388d9d72b5d1ee531452f60f12ba6b7bfe67614ae5e8252d60b4afccf2"
    canonical_rows = json.dumps(saved_results()["rows"], sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical_rows).hexdigest() == "9a0035ad124e77f13bf166222eb50af15902c48dd96b293a2f1b4d0e8a9a61c0"
    assert b"\r" not in (HERE / "rows.csv").read_bytes()


def test_all_saved_enclosures_quadrature_gates_and_summary():
    rows = saved_results()["rows"]
    for r in rows:
        for name in ("m6", "m8", "n6_eV", "n8_eV", "c6_eV", "c8_eV", "omega_eV"):
            v = r[name]
            lo, hi, mid, radius = [Decimal(v[k]) for k in ("lo", "hi", "mid", "radius")]
            assert lo <= mid <= hi
            assert radius >= max(mid-lo, hi-mid)
            if name in ("c6_eV", "c8_eV", "omega_eV"):
                assert radius <= Decimal(study.REG["max_numerical_centroid_radius_eV"])
        assert 0 < Decimal(r["m6"]["lo"]) <= Decimal(r["m6"]["hi"]) <= 1
        assert 0 < Decimal(r["m8"]["lo"]) <= Decimal(r["m8"]["hi"]) <= 1
        for order, values in r["quad_moments"].items():
            for index, name in enumerate(("m6", "n6_eV", "m8", "n8_eV")):
                error = abs(values[index]-float(r[name]["mid"]))
                limit = float(study.REG["quad_mass_tolerance"]) if index % 2 == 0 else float(r["W_eV"])*float(study.REG["quad_moment_tolerance_per_W"])
                assert error <= limit, (r["x"], r["alternative"], order, name, error)
        assert r["quadrature_pass"]
        assert Decimal(r["c8_eV"]["lo"]) == Decimal(r["c8_eV"]["hi"]) == 0
    assert study.summarize(rows) == json.loads((HERE / "summary.json").read_text())


def test_balanced_sign_from_independent_lorentz_pair_inequality():
    # Even positive window/bath: symmetric mixed sector has n=0. For e>0,
    # P(E-e)-P(E+e)>0 at E>0, so the atom's n has e's sign. No scan fit.
    for r in saved_results()["rows"]:
        if r["alternative"] != "balanced":
            continue
        e = -Fraction(3, 10)+Fraction(11, 10)*Fraction(r["x"])
        assert r["sign"] == ("positive" if e > 0 else "negative")
    positive_e, sample_e, eta = .08, .17, .1
    assert eta/((sample_e-positive_e)**2+eta**2) > eta/((sample_e+positive_e)**2+eta**2)


def test_redistribution_affine_identity_and_mass_invariance():
    # Independent parity derivation: all even-window masses are a-independent;
    # n6(a)=n6(0)+a*h*(1-b)*[.8*n_atom(1)-.2*n_atom(4)].
    # Test saved enclosures only; do not repeat the 135-row integration scan.
    rows = saved_results()["rows"]
    for x, w, eta in itertools.product(study.REG["composition"], study.REG["window_half_widths_eV"], study.REG["eta_eV"]):
        group = {r["alternative"]: r for r in rows if (r["x"], r["W_eV"], r["eta_eV"]) == (x, w, eta)}
        for name in ("m6", "m8"):
            assert max(Decimal(r[name]["lo"]) for r in group.values()) <= min(Decimal(r[name]["hi"]) for r in group.values())
        for name in ("n6_eV", "omega_eV"):
            positive = I(group["positive"][name]["lo"], group["positive"][name]["hi"])
            negative = I(group["negative"][name]["lo"], group["negative"][name]["hi"])
            midpoint_alternatives = (positive + negative) / 2
            balanced = I(group["balanced"][name]["lo"], group["balanced"][name]["hi"])
            assert max(midpoint_alternatives.lo, balanced.lo) <= min(midpoint_alternatives.hi, balanced.hi)


def test_sign_selection_rejects_ties_and_numerical_overwrite(tmp_path):
    assert study.interval_sign(I("-.0001", ".0001")) == ("unresolved", Decimal(0))
    assert study.interval_sign(I("-.1", "-.01")) == ("negative", Decimal(".01"))
    (tmp_path / "results.json").write_text("sentinel")
    with pytest.raises(FileExistsError):
        study.run(tmp_path)
    assert (tmp_path / "results.json").read_text() == "sentinel"
