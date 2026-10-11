"""Registered finite synthetic study; no material Hamiltonian or root inference.

Run: python run_study.py --output /path/to/empty/output
Only Decimal interval bounds certify arithmetic error. Fixed numpy quadrature
is an independent implementation check, not an error certificate.
"""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, localcontext
from functools import lru_cache
import hashlib
import itertools
import json
from math import ceil, comb
from pathlib import Path
import subprocess

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REG = json.loads((HERE / "registration.json").read_text())
PREC = REG["decimal_precision"]
TERMS = REG["atan_terms"]


def directed(fn, rounding):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = rounding
        return fn()


class I:
    """Closed Decimal enclosure; float inputs deliberately rejected."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        if isinstance(lo, I):
            if hi is not None:
                raise TypeError("nested interval")
            self.lo, self.hi = lo.lo, lo.hi
            return
        if isinstance(lo, float) or isinstance(hi, float):
            raise TypeError("use exact decimal strings")
        self.lo = Decimal(lo)
        self.hi = self.lo if hi is None else Decimal(hi)
        if not self.lo.is_finite() or not self.hi.is_finite() or self.lo > self.hi:
            raise ValueError("invalid finite interval")

    def __add__(self, other):
        b = I(other)
        return I(directed(lambda: self.lo + b.lo, ROUND_FLOOR),
                 directed(lambda: self.hi + b.hi, ROUND_CEILING))

    __radd__ = __add__

    def __neg__(self):
        # copy_negate is exact and does not inherit the ambient 28-digit context.
        return I(self.hi.copy_negate(), self.lo.copy_negate())

    def __sub__(self, other):
        return self + -I(other)

    def __rsub__(self, other):
        return I(other) + -self

    def __mul__(self, other):
        b = I(other)
        pairs = list(itertools.product((self.lo, self.hi), (b.lo, b.hi)))
        lower = [directed(lambda a=a, c=c: a * c, ROUND_FLOOR) for a, c in pairs]
        upper = [directed(lambda a=a, c=c: a * c, ROUND_CEILING) for a, c in pairs]
        return I(min(lower), max(upper))

    __rmul__ = __mul__

    def __truediv__(self, other):
        b = I(other)
        if b.lo <= 0 <= b.hi:
            raise ZeroDivisionError("divisor interval contains zero")
        reciprocal = I(directed(lambda: Decimal(1) / b.hi, ROUND_FLOOR),
                       directed(lambda: Decimal(1) / b.lo, ROUND_CEILING))
        return self * reciprocal

    def __rtruediv__(self, other):
        return I(other) / self

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise TypeError("nonnegative integer powers only")
        answer, base = I(1), self
        while exponent:
            if exponent & 1:
                answer = answer * base
            exponent //= 2
            if exponent:
                base = base * base
        return answer

    def midpoint(self):
        return directed(lambda: (self.lo + self.hi) / 2, ROUND_HALF_EVEN)

    def radius(self):
        mid = self.midpoint()
        return max(directed(lambda: mid - self.lo, ROUND_CEILING),
                   directed(lambda: self.hi - mid, ROUND_CEILING))

    def record(self):
        return {"lo": str(self.lo), "hi": str(self.hi),
                "mid": str(self.midpoint()), "radius": str(self.radius())}


def ln_interval(z):
    z = I(z)
    if z.lo <= 0:
        raise ValueError("logarithm needs positive interval")
    # Decimal.ln is documented as correctly rounded ROUND_HALF_EVEN, regardless
    # of context.rounding. Enlarge each endpoint by one representable neighbour.
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_HALF_EVEN
        return I(z.lo.ln().next_minus(), z.hi.ln().next_plus())


def atan_series(z):
    z = I(z)
    magnitude = max(z.lo.copy_abs(), z.hi.copy_abs())
    if magnitude > Decimal("0.5"):
        raise ValueError("series reduction domain exceeded")
    total, term, square = I(0), z, z * z
    for j in range(TERMS):
        total = total + ((-1) ** j) * term / (2 * j + 1)
        term = term * square
    # Alternating-series remainder pointwise, bounded uniformly on z.
    remainder = (I(magnitude) ** (2 * TERMS + 1) / (2 * TERMS + 1)).hi
    return total + I(remainder.copy_negate(), remainder)


PI = 16 * atan_series(I(1) / 5) - 4 * atan_series(I(1) / 239)


def atan_point(y):
    y = Decimal(y)
    if y < 0:
        return -atan_point(y.copy_negate())
    if y > 1:
        return PI / 2 - atan_interval(I(1) / I(y))
    if y > Decimal("0.5"):
        return PI / 4 + atan_series((I(y) - 1) / (I(y) + 1))
    return atan_series(I(y))


def atan_interval(z):
    z = I(z)
    return I(atan_point(z.lo).lo, atan_point(z.hi).hi)


@lru_cache(maxsize=128)
def atom_integrals(t, width, eta):
    t, width, eta = I(t), I(width), I(eta)
    left, right = -width - t, width - t
    b = [atan_interval(right / eta) - atan_interval(left / eta),
         eta / 2 * ln_interval((right**2 + eta**2) / (left**2 + eta**2))]
    for j in range(2, 6):
        b.append(eta * (right**(j - 1) - left**(j - 1)) / (j - 1)
                 - eta**2 * b[j - 2])
    j = [sum((comb(ell, k) * t**(ell - k) * b[k]
              for k in range(ell + 1)), I(0)) / PI for ell in range(6)]
    mass = j[0] - 2 * j[2] / width**2 + j[4] / width**4
    moment = j[1] - 2 * j[3] / width**2 + j[5] / width**4
    return mass, moment, tuple(j)


@lru_cache(maxsize=16)
def uniform_integrals(width, eta, half_width):
    w, eta, length = I(width), I(eta), I(half_width)

    def q(e):
        return e - 2 * e**3 / (3 * w**2) + e**5 / (5 * w**4)

    boundary = (q(w) * atan_interval((w + length) / eta)
                - q(-w) * atan_interval((-w + length) / eta))
    _, _, j = atom_integrals(length.lo.copy_negate(), w.lo, eta.lo)
    mass = (boundary - PI * (j[1] - 2 * j[3] / (3 * w**2)
                            + j[5] / (5 * w**4))) / (PI * length)
    return mass, I(0)


def model_parameters(x, alternative):
    x, a = I(x), I(alternative)
    h = 16 * (x * (1 - x))**2
    energy = I(REG["reference_chord_eV"][0]) + I(REG["reference_chord_eV"][1]) * x
    b = I(REG["continuum_mixed_weight"])
    # Positive normalized exact rational weights; keep zero-weight satellites.
    atoms = [(energy, 1 - h), (I(1), h * (1 - b) * I("0.4") * (1 + a)),
             (I(-1), h * (1 - b) * I("0.4") * (1 - a)),
             (I(4), h * (1 - b) * I("0.1") * (1 - a)),
             (I(-4), h * (1 - b) * I("0.1") * (1 + a))]
    return atoms, h * b


def enclosed_moments(x, alternative, width, eta):
    atoms, continuum_weight = model_parameters(x, alternative)
    # All registered energies/weights are finite decimals and exact here;
    # model intervals propagate their arithmetic through the weighted sums.
    bath, _ = uniform_integrals(Decimal(width), Decimal(eta),
                               Decimal(REG["continuum_half_width_eV"]))
    mass, moment = continuum_weight * bath, I(0)
    for energy, weight in atoms:
        if energy.lo != energy.hi:
            raise ArithmeticError("registered atom energy must be exactly representable")
        m, n, _ = atom_integrals(energy.lo, Decimal(width), Decimal(eta))
        mass, moment = mass + weight * m, moment + weight * n
    return mass, moment, bath, I(0)


@lru_cache(maxsize=32)
def quadrature_grid(width, eta, order):
    segments = ceil(2 * width / eta)
    if segments > REG["max_quad_segments"]:
        raise ValueError("registered quadrature resource cap exceeded")
    nodes, weights = np.polynomial.legendre.leggauss(order)
    edges = np.linspace(-width, width, segments + 1)
    half = (edges[1:] - edges[:-1]) / 2
    mid = (edges[1:] + edges[:-1]) / 2
    e = (mid[:, None] + half[:, None] * nodes).ravel()
    measure = (half[:, None] * weights).ravel()
    chi = (1 - (e / width)**2)**2
    length = float(REG["continuum_half_width_eV"])
    bath = (np.arctan((length - e) / eta) + np.arctan((length + e) / eta)) / (2 * np.pi * length)
    return e, measure * chi, bath


def quadrature_moments(x, alternative, width, eta, order):
    e, weights, bath = quadrature_grid(width, eta, order)
    x, a = float(x), float(alternative)
    h, b = 16 * (x * (1 - x))**2, float(REG["continuum_mixed_weight"])
    t = float(REG["reference_chord_eV"][0]) + float(REG["reference_chord_eV"][1]) * x
    density = h * b * bath
    for atom, weight in [(t, 1 - h), (1, h * (1-b) * .4 * (1+a)),
                         (-1, h * (1-b) * .4 * (1-a)),
                         (4, h * (1-b) * .1 * (1-a)),
                         (-4, h * (1-b) * .1 * (1+a))]:
        density = density + weight * eta / (np.pi * ((e - atom)**2 + eta**2))
    return np.array([np.dot(weights, density), np.dot(weights * e, density),
                     np.dot(weights, bath), np.dot(weights * e, bath)])


def interval_sign(omega):
    if omega.lo > 0:
        return "positive", omega.lo
    if omega.hi < 0:
        return "negative", omega.hi.copy_negate()
    return "unresolved", Decimal(0)


def summarize(rows):
    floor = Decimal(REG["mass_floor"])
    margin = Decimal(REG["minimum_sign_margin_eV"])
    maximum_radius = Decimal(REG["max_numerical_centroid_radius_eV"])
    groups = []
    for x in REG["composition"]:
        alternatives = {}
        for name in REG["alternatives"]:
            subset = [r for r in rows if r["x"] == x and r["alternative"] == name]
            signs = sorted(set(r["sign"] for r in subset))
            minimum_margin = min(Decimal(r["sign_margin_eV"]) for r in subset)
            alternatives[name] = {
                "signs": signs,
                "all_nine_stable": len(signs) == 1 and signs[0] != "unresolved" and minimum_margin >= margin,
                "minimum_sign_margin_eV": str(minimum_margin),
                "minimum_mass_lower": str(min(Decimal(r[q]["lo"]) for r in subset for q in ("m6", "m8"))),
                "omega_range_eV": [str(min(Decimal(r["omega_eV"]["lo"]) for r in subset)),
                                    str(max(Decimal(r["omega_eV"]["hi"]) for r in subset))],
            }
        all_signs = sorted(set(r["sign"] for r in rows if r["x"] == x))
        groups.append({"x": x, "alternatives": alternatives,
                       "alternative_robust": all(v["all_nine_stable"] for v in alternatives.values()) and len(all_signs) == 1})
    numerical_pass = all(Decimal(r["omega_eV"]["radius"]) <= maximum_radius and r["quadrature_pass"] for r in rows)
    floor_pass = all(Decimal(r[q]["lo"]) >= floor for r in rows for q in ("m6", "m8"))
    sign_pass = all(g["alternative_robust"] for g in groups)
    return {
        "scope": "finite synthetic model grid only; physical inputs unqualified",
        "row_count": len(rows), "compositions": groups,
        "numerical_gate": numerical_pass, "mass_floor_gate": floor_pass,
        "within_model_sign_gate": all(v["all_nine_stable"] for g in groups for v in g["alternatives"].values()),
        "alternative_robust_gate": sign_pass,
        "numeric_and_sign_decision": "GO" if numerical_pass and floor_pass and sign_pass else "NO-GO",
        "model_qualification": "requires independent focused tests, recorded in verification.md",
        "minimum_mass_lower": str(min(Decimal(r[q]["lo"]) for r in rows for q in ("m6", "m8"))),
        "maximum_centroid_radius_eV": str(max(Decimal(r["omega_eV"]["radius"]) for r in rows)),
        "maximum_quad_mass_discrepancy": max(r["quad_max_mass_discrepancy"] for r in rows),
        "maximum_quad_moment_discrepancy_eV": max(r["quad_max_moment_discrepancy_eV"] for r in rows),
        "maximum_quad_normalized_moment_discrepancy": max(r["quad_max_moment_discrepancy_eV"] / float(r["W_eV"]) for r in rows),
        "physical_xc": None, "root_search_performed": False,
    }


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output):
    output = Path(output)
    names = ("results.json", "summary.json", "rows.csv")
    if any((output / name).exists() for name in names):
        raise FileExistsError("use an empty output directory; registered results are never overwritten")
    for source in REG["sources"]:
        if sha256(ROOT / source["path"]) != source["sha256"]:
            raise ValueError(f"registered source changed: {source['path']}")
    prereg = subprocess.check_output(["git", "log", "-1", "--format=%H", "--", str(HERE / "registration.json")], cwd=ROOT, text=True).strip()
    rows = []
    for x, (name, a), width, eta in itertools.product(REG["composition"], REG["alternatives"].items(), REG["window_half_widths_eV"], REG["eta_eV"]):
        m6, n6, m8, n8 = enclosed_moments(x, a, width, eta)
        c6, c8 = n6 / m6, n8 / m8
        omega = c6 - c8
        sign, sign_margin = interval_sign(omega)
        centers = np.array([float(z.midpoint()) for z in (m6, n6, m8, n8)])
        checks = {str(order): quadrature_moments(x, a, float(width), float(eta), order) for order in REG["quad_orders"]}
        errors = np.array([np.abs(v - centers) for v in checks.values()])
        m_error, n_error = float(errors[:, [0, 2]].max()), float(errors[:, [1, 3]].max())
        rows.append({
            "x": x, "alternative": name, "a": a, "W_eV": width, "eta_eV": eta,
            "m6": m6.record(), "n6_eV": n6.record(), "m8": m8.record(), "n8_eV": n8.record(),
            "c6_eV": c6.record(), "c8_eV": c8.record(), "omega_eV": omega.record(),
            "sign": sign, "sign_margin_eV": str(sign_margin),
            "quad_moments": {order: list(map(float, v)) for order, v in checks.items()},
            "quad_order_difference": list(map(float, np.abs(checks["16"] - checks["8"]))),
            "quad_max_mass_discrepancy": m_error, "quad_max_moment_discrepancy_eV": n_error,
            "quadrature_pass": m_error <= float(REG["quad_mass_tolerance"]) and n_error <= float(width) * float(REG["quad_moment_tolerance_per_W"]),
        })
    if len(rows) != REG["max_rows"]:
        raise ValueError("wrong registered grid")
    metadata = {"preregistration_commit": prereg, "registration_sha256": sha256(HERE / "registration.json"),
                "runner_sha256": sha256(Path(__file__)), "source_hashes": REG["sources"],
                "interval_precision": PREC, "atan_terms": TERMS, "pi_enclosure": PI.record(),
                "units": {"mass": "1", "n_centroid_eta_W": "eV", "x": "1"},
                "physical_material_validation": False}
    output.mkdir(parents=True, exist_ok=True)
    for name, payload in [("results.json", {"metadata": metadata, "rows": rows}), ("summary.json", summarize(rows))]:
        (output / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    with (output / "rows.csv").open("w", newline="") as handle:
        fields = ["x", "alternative", "W_eV", "eta_eV", "m6_lower", "m8_lower", "omega_mid_eV", "omega_lower_eV", "omega_upper_eV", "radius_eV", "sign", "margin_eV", "quad_mass_error", "quad_moment_error_eV"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow({"x": r["x"], "alternative": r["alternative"], "W_eV": r["W_eV"], "eta_eV": r["eta_eV"],
                             "m6_lower": r["m6"]["lo"], "m8_lower": r["m8"]["lo"], "omega_mid_eV": r["omega_eV"]["mid"],
                             "omega_lower_eV": r["omega_eV"]["lo"], "omega_upper_eV": r["omega_eV"]["hi"],
                             "radius_eV": r["omega_eV"]["radius"], "sign": r["sign"], "margin_eV": r["sign_margin_eV"],
                             "quad_mass_error": r["quad_max_mass_discrepancy"], "quad_moment_error_eV": r["quad_max_moment_discrepancy_eV"]})
    return summarize(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
