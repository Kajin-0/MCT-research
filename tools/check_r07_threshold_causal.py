#!/usr/bin/env python3
"""Freeze a bounded synthetic audit of the R07 threshold/root theorems.

No material inputs, DFT processes, queues or native supervisors are used.
Refuses to overwrite evidence. Independent integrals are covered by tests.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np

from mct_research.analytical_gap_closure import DiscreteFeshbachMeasure
from mct_research.threshold_causal_closure import (
    causal_mass_root_error_bound,
    quadratic_threshold_kernel,
    subleading_density_remainder_bound,
)
from mct_research.threshold_impurity import below_edge_green_prime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parents[1]
    output = args.output if args.output.is_absolute() else root_dir/args.output
    if output.exists():
        raise SystemExit("Refusing to overwrite an existing audit")
    sources = ["src/mct_research/threshold_causal_closure.py",
               "tests/test_r07_threshold_causal_closure.py",
               "tools/check_r07_threshold_causal.py"]
    record = {
        "status": "CALCULATED: synthetic mathematical audit; no material validation",
        "date": "2026-10-11",
        "parent_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root_dir, text=True).strip(),
        "numpy_version": np.__version__,
        "source_sha256": {p: hashlib.sha256((root_dir/p).read_bytes()).hexdigest()
                          for p in sources},
    }
    c, v, root = 0.3, 0.8, 0.25
    k0 = quadratic_threshold_kernel(0, 0, 1, c).real
    rows = []
    for detuning in [1e-6, 1e-10, 1e-12]:
        k = quadratic_threshold_kernel(-detuning, 0, 1, c).real
        fs = -detuning+k0/2-k/2
        eps = -fs
        candidate_root = root-(k-k0)/(2*v)
        bound = causal_mass_root_error_bound(eps, eps, v)
        error = abs(candidate_root-root)
        assert error <= bound
        rows.append({"gap_detuning_eV": detuning,
                     "raw_normalized_host_susceptibility": float(-below_edge_green_prime(detuning)),
                     "branch_residual_eV": eps, "root_error": error,
                     "root_error_bound": bound, "error_over_bound": error/bound})
    record["threshold_root_certificate"] = rows
    record["subleading_bounds"] = [
        {"exponent": p, "synthetic_density_bound_coefficient": 0.3,
         "h_eV": 0.01, "cutoff_eV": 0.7,
         "remainder_bound_eV": subleading_density_remainder_bound(0.01, 0.3, p, 0.7)}
        for p in [1.5, 2, 2.5]]
    energy, b = 0.001, 0.9
    k = b*math.log((1+energy)/(1-energy))
    record["causal_continuum_counterexample"] = {
        "density_eV": b, "half_width_eV": 1, "energy_eV": energy,
        "abs_mass_over_common_secant": abs((k/2)/(energy-k/2)),
        "derivative_ratio_at_center": 9.0,
    }
    reference = 0.3
    t = reference+np.array([0.5, 1, -1, -0.5])
    null = np.array([1, -2, 2, -1])
    ir = quadratic_threshold_kernel(0.1, 0.3, 0.4, 0.04).real
    moment_rows = []
    for sign in [-1, 1]:
        measure = DiscreteFeshbachMeasure(t, 0.02*(1+sign*0.2*null))
        total = ir+measure.kernel(0.1).real
        lo, hi = 0.2, 0.3
        for _ in range(70):
            x = (lo+hi)/2
            if 1.6*(x-0.23)+x*(1-x)*total < 0:
                lo = x
            else:
                hi = x
        moment_rows.append({"sign": sign, "regular_moment_reference_eV": reference,
                            "C_eV": measure.moments(reference)[0],
                            "A": measure.moments(reference)[1], "distance_eV": 0.5,
                            "total_weight_eV2": float(sum(measure.weights)),
                            "shared_IR_at_crossing_eV": ir,
                            "full_kernel_at_crossing_eV": total,
                            "root": (lo+hi)/2})
    assert abs(moment_rows[0]["root"]-moment_rows[1]["root"]) > 1e-4
    record["same_IR_and_regular_moments_distinct_roots"] = moment_rows
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive mode protects against an overwrite race as well.
    with output.open("x") as handle:
        json.dump(record, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(f"Wrote synthetic threshold audit: {output}")


if __name__ == "__main__":
    main()
