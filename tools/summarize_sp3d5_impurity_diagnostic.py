#!/usr/bin/env python3
"""Freeze endpoint reductions using calculated T matrices only."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def physical_roots(coefficients):
    roots = np.roots(np.trim_zeros(np.array(coefficients)[::-1], trim="f"))
    return sorted(float(z.real) for z in roots if abs(z.imag) < 1e-9 and 0 < z.real < 1)


def projected(row, method="exact", component="real"):
    return (row["branches"]["6"][method][component] - row["branches"]["8"][method][component]) / 2


def reduce_dataset(path):
    dataset = json.loads(path.read_text())
    e0 = dataset["binary"]["HgTe"]["gap_eV"]
    e1 = dataset["binary"]["CdTe"]["gap_eV"]
    span = e1 - e0
    groups = sorted({(r["mesh"], r["eta_eV"]) for r in dataset["rows"] if r["eta_eV"] > 0})
    summaries = []
    for mesh, eta in groups:
        rows = {(r["host"], r["reference"]): r for r in dataset["rows"] if r["mesh"] == mesh and r["eta_eV"] == eta}
        h, c = rows["HgTe", "common_mode"], rows["CdTe", "common_mode"]
        th, tc = projected(h), projected(c)
        mh, delta = e0 / 2, span / 2
        mass_coeffs = [mh, th, 3 * delta - 2 * th + tc, -2 * delta + th - tc]
        # Counterexample: the handoff formula if full host-referenced T is inserted as a residual.
        wrong_u0, wrong_u1 = delta + th, delta - tc
        wrong_coeffs = [mh, wrong_u0, 3 * delta - 2 * wrong_u0 - wrong_u1, -2 * delta + wrong_u0 + wrong_u1]
        g0 = (rows["HgTe", "Gamma6_pole"]["branches"]["6"]["exact"]["real"]
              - rows["HgTe", "Gamma8_pole"]["branches"]["8"]["exact"]["real"])
        g1 = -(rows["CdTe", "Gamma6_pole"]["branches"]["6"]["exact"]["real"]
               - rows["CdTe", "Gamma8_pole"]["branches"]["8"]["exact"]["real"])
        p0, p1 = g0 - span, g1 - span
        a = (p0 + p1) / span
        static = (e1 * p0 + e0 * p1) / span
        record = {
            "mesh": mesh, "eta_eV": eta,
            "full_common_mass_H_eV": th, "full_common_mass_C_eV": tc,
            "full_common_mass_H_imag_eV": projected(h, component="imag"),
            "full_common_mass_C_imag_eV": projected(c, component="imag"),
            "chord_residual_H_eV": th - delta, "chord_residual_C_eV": tc + delta,
            "mass_cubic_coefficients_ascending_eV": mass_coeffs,
            "mass_cubic_roots": physical_roots(mass_coeffs),
            "incorrect_double_counted_mass_roots": physical_roots(wrong_coeffs),
            "gap_slope_H_eV": g0, "gap_slope_C_eV": g1,
            "reciprocal_A_from_slopes": a, "reciprocal_C_eV": static,
            "reciprocal_rho": -static / span,
            "reciprocal_roots": physical_roots([e0, span + static, -static]),
            "common_symmetric_negative_derivative": {},
            "common_positive_cloud_norm": {},
            "Born2_common_gap_eV": {},
            "exact_minus_first_common_gap_eV": {},
        }
        for host, row in (("HgTe", h), ("CdTe", c)):
            branches = row["branches"]
            record["common_symmetric_negative_derivative"][host] = (branches["6"]["exact_negative_derivative"]["real"] + branches["8"]["exact_negative_derivative"]["real"]) / 2
            record["common_positive_cloud_norm"][host] = -(branches["6"]["exact"]["imag"] + branches["8"]["exact"]["imag"]) / (2 * eta)
            record["Born2_common_gap_eV"][host] = 2 * projected(row, "second")
            record["exact_minus_first_common_gap_eV"][host] = 2 * (projected(row) - projected(row, "first"))
        summaries.append(record)
    return {
        "input": str(path), "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "offset_eV": dataset["offset_eV"], "te_share": dataset["te_share"],
        "binary_gap_H_eV": e0, "binary_gap_C_eV": e1, "chord_root": -e0 / span,
        "max_optical_theorem_relative_residual": max(r["optical_theorem_relative_residual"] for r in dataset["rows"]),
        "min_causality_eigenvalue": min(r["causality_min_eigenvalue"] for r in dataset["rows"]),
        "endpoint_reductions": summaries,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/calculated/sp3d5_endpoint_reductions.json"))
    args = parser.parse_args()
    result = {
        "claim_status": "CALCULATED diagnostic endpoint interpolants; real parts at finite eta, not physical x_c predictions",
        "empirical_alloy_gap_inputs": [],
        "mass_convention": "Full host-referenced T: mu'(0)=full_t_H, mu'(1)=-full_t_C",
        "common_mode_prescription": "Hermitian/real-part endpoint projection at (E6+E8)/2, finite retarded eta; not a solved interior common-mode trajectory",
        "datasets": [reduce_dataset(path) for path in args.inputs]
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
