#!/usr/bin/env python3
"""Validate the declared, not-yet-run CdTe A0 convergence protocol."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _load_object(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value) and value > 0


def _strictly_increasing(values: Any) -> bool:
    return (
        isinstance(values, list)
        and len(values) >= 2
        and all(_positive_number(value) for value in values)
        and all(left < right for left, right in zip(values, values[1:]))
    )


def _strictly_decreasing(values: Any) -> bool:
    return (
        isinstance(values, list)
        and len(values) >= 2
        and all(_positive_number(value) for value in values)
        and all(left > right for left, right in zip(values, values[1:]))
    )


def evaluate_convergence_protocol(
    specification: dict[str, Any],
    pseudopotential_selection: dict[str, Any],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    ladders = specification.get("convergence_ladders", {})
    protocol = specification.get("convergence_protocol", {})
    elements = pseudopotential_selection.get("elements", {})

    add(
        "declared_not_run",
        isinstance(ladders, dict)
        and ladders.get("selection_status") == "declared_not_run"
        and isinstance(protocol, dict)
        and protocol.get("calculation_results_recorded") is False,
        "The convergence object must remain a declared, not-yet-run plan.",
    )

    expected_cutoffs = pseudopotential_selection.get(
        "cdte_cutoff_ladder_rydberg", {}
    )
    expected_ecutwfc = [
        expected_cutoffs.get("low"),
        expected_cutoffs.get("normal"),
        expected_cutoffs.get("high"),
    ]
    ecutwfc = ladders.get("ecutwfc_ry", []) if isinstance(ladders, dict) else []
    add(
        "ecutwfc_matches_verified_pseudopotentials",
        ecutwfc == expected_ecutwfc and _strictly_increasing(ecutwfc),
        "The wavefunction ladder must remain the verified 94/102/114 Ry hints.",
    )

    reference_ecutwfc = (
        ladders.get("ecutrho_reference_ecutwfc_ry")
        if isinstance(ladders, dict)
        else None
    )
    ratios = ladders.get("ecutrho_ratio", []) if isinstance(ladders, dict) else []
    ecutrho = ladders.get("ecutrho_ry", []) if isinstance(ladders, dict) else []
    ratio_ladder_valid = (
        _positive_number(reference_ecutwfc)
        and ecutwfc
        and reference_ecutwfc == max(ecutwfc)
        and _strictly_increasing(ratios)
        and all(isinstance(value, int) and value >= 4 for value in ratios)
        and isinstance(ecutrho, list)
        and len(ecutrho) == len(ratios)
        and ecutrho == [reference_ecutwfc * ratio for ratio in ratios]
    )
    add(
        "ecutrho_ratio_ladder_consistent",
        ratio_ladder_valid,
        (
            "Charge-density cutoffs must be exact products of the highest ecutwfc "
            "and an independently tested increasing ratio ladder starting at 4."
        ),
    )

    k_grid = ladders.get("k_grid_n", []) if isinstance(ladders, dict) else []
    k_shift = ladders.get("k_grid_shift") if isinstance(ladders, dict) else None
    add(
        "gamma_centered_even_k_grid_ladder",
        _strictly_increasing(k_grid)
        and len(k_grid) >= 4
        and all(isinstance(value, int) and value % 2 == 0 for value in k_grid)
        and k_shift == [0, 0, 0],
        "Use increasing even cubic grids with zero shift so Gamma is sampled directly.",
    )

    valence_electrons = None
    if isinstance(elements, dict) and all(
        isinstance(elements.get(element), dict)
        and isinstance(elements[element].get("z_valence"), (int, float))
        for element in ("Cd", "Te")
    ):
        valence_electrons = int(
            elements["Cd"]["z_valence"] + elements["Te"]["z_valence"]
        )
    recorded_valence = (
        ladders.get("total_valence_electrons") if isinstance(ladders, dict) else None
    )
    nbnd = ladders.get("nbnd", []) if isinstance(ladders, dict) else []
    empty_bands = (
        ladders.get("empty_spinor_bands", []) if isinstance(ladders, dict) else []
    )
    band_ladder_valid = (
        valence_electrons is not None
        and recorded_valence == valence_electrons
        and _strictly_increasing(nbnd)
        and len(nbnd) >= 3
        and all(isinstance(value, int) and value > valence_electrons for value in nbnd)
        and isinstance(empty_bands, list)
        and empty_bands == [value - valence_electrons for value in nbnd]
        and all(value > 0 for value in empty_bands)
    )
    add(
        "soc_spinor_band_ladder_consistent",
        band_ladder_valid,
        (
            "The noncollinear SOC band ladder must be derived from the verified "
            "Cd+Te valence-electron count and record its explicit empty spinor states."
        ),
    )

    add(
        "threshold_ladders_tighten",
        isinstance(ladders, dict)
        and _strictly_decreasing(ladders.get("scf_conv_thr_ry"))
        and _strictly_decreasing(ladders.get("ph_tr2")),
        "SCF and phonon thresholds must tighten monotonically.",
    )

    governed_ladders = (
        "ecutwfc_ry",
        "ecutrho_ratio",
        "k_grid_n",
        "nbnd",
        "scf_conv_thr_ry",
        "ph_tr2",
    )
    add(
        "governed_ladders_support_two_refinements",
        isinstance(ladders, dict)
        and all(
            isinstance(ladders.get(name), list)
            and len(ladders[name]) >= 3
            for name in governed_ladders
        ),
        (
            "Every ladder governed by the generic selection rule must contain "
            "an initial point plus at least two refinements."
        ),
    )

    required_sequence = [
        "ecutrho_at_ecutwfc_114Ry",
        "ecutwfc_with_selected_ecutrho_ratio",
        "gamma_centered_k_grid",
        "nbnd_spinor_empty_states",
        "threshold_tightening",
        "selected_vs_next_denser_cross_factor_recheck",
    ]
    add(
        "sequential_one_factor_protocol",
        isinstance(protocol, dict)
        and protocol.get("sequence") == required_sequence
        and isinstance(protocol.get("selection_rule"), str)
        and "two successive refinements" in protocol["selection_rule"]
        and "new decision memo" in protocol["selection_rule"]
        and protocol.get("cross_factor_recheck_required") is True,
        (
            "The protocol must isolate variables sequentially, require two successive "
            "passing refinements and stop before extending the ladder automatically."
        ),
    )

    criteria = protocol.get("criteria", {}) if isinstance(protocol, dict) else {}
    required_criteria = {
        "total_energy_mev_per_atom",
        "stress_gpa",
        "gamma_conduction_edge_mev",
        "gamma_valence_edge_mev",
        "gamma_gap_mev",
        "spin_orbit_splitting_mev",
        "optical_phonon_cm-1",
        "acoustic_sum_rule_residual_cm-1",
        "dielectric_tensor_relative",
        "born_effective_charge_e",
    }
    add(
        "observable_stopping_criteria_complete",
        isinstance(criteria, dict)
        and set(criteria) == required_criteria
        and all(_positive_number(value) for value in criteria.values())
        and criteria.get("gamma_conduction_edge_mev", math.inf) <= 0.25
        and criteria.get("gamma_valence_edge_mev", math.inf) <= 0.25
        and criteria.get("gamma_gap_mev", math.inf) <= 0.5,
        "All static, edge, phonon, dielectric and Born-charge stopping criteria are required.",
    )

    valid = all(check["passed"] for check in checks)
    return {
        "schema_version": "1.0",
        "stage": specification.get("stage"),
        "protocol_valid": valid,
        "passed_checks": sum(check["passed"] for check in checks),
        "total_checks": len(checks),
        "blocking_checks": [
            check["name"] for check in checks if not check["passed"]
        ],
        "checks": checks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-spec-json",
        default="first_principles/a0/cdte_a0_run_spec.json",
    )
    parser.add_argument(
        "--selection-json",
        default="first_principles/a0/cdte_pseudopotential_selection.json",
    )
    parser.add_argument("--report-json")
    parser.add_argument(
        "--require-valid",
        action="store_true",
        help="exit nonzero unless the declared convergence protocol is internally valid",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = evaluate_convergence_protocol(
        _load_object(args.run_spec_json),
        _load_object(args.selection_json),
    )
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(output, end="")
    if args.report_json:
        path = Path(args.report_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    return 1 if args.require_valid and not report["protocol_valid"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
