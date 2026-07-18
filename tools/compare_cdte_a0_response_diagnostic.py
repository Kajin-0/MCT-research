#!/usr/bin/env python3
"""Compare the one authorized stricter CdTe response with the audited baseline."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ratio(current: float, baseline: float) -> float:
    denominator = abs(float(baseline))
    if denominator == 0.0:
        raise ValueError("baseline response metric is zero and cannot define a ratio")
    return abs(float(current)) / denominator


def compare(
    baseline: dict[str, Any],
    diagnostic: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    if contract.get("stage") != "A0_same_geometry_stricter_response_diagnostic":
        raise ValueError("unexpected stricter-response contract stage")
    baseline_observables = baseline["observables"]
    diagnostic_observables = diagnostic["observables"]
    ratios = {
        "raw_acoustic": _ratio(
            diagnostic_observables["maximum_raw_acoustic_absolute_frequency_cm1"],
            baseline_observables["maximum_raw_acoustic_absolute_frequency_cm1"],
        ),
        "born_charge_sum": _ratio(
            diagnostic_observables["born_charge_sum_mean_e"],
            baseline_observables["born_charge_sum_mean_e"],
        ),
        "asr_optical_shift": _ratio(
            diagnostic_observables["asr_optical_relative_shift"],
            baseline_observables["asr_optical_relative_shift"],
        ),
    }
    criteria = contract["material_collapse_criteria"]
    collapse_checks = {
        "raw_acoustic": ratios["raw_acoustic"]
        <= float(criteria["maximum_acoustic_ratio_to_baseline"]),
        "born_charge_sum": ratios["born_charge_sum"]
        <= float(criteria["maximum_born_sum_ratio_to_baseline"]),
        "asr_optical_shift": ratios["asr_optical_shift"]
        <= float(criteria["maximum_asr_optical_shift_ratio_to_baseline"]),
    }
    materially_collapsed = (
        all(collapse_checks.values())
        if criteria.get("require_all_three") is True
        else any(collapse_checks.values())
    )
    deltas = {
        "total_energy_ry": float(diagnostic_observables["total_energy_ry"])
        - float(baseline_observables["total_energy_ry"]),
        "direct_gamma_gap_ev": float(diagnostic_observables["direct_gamma_gap_ev"])
        - float(baseline_observables["direct_gamma_gap_ev"]),
        "pressure_kbar": float(diagnostic_observables["pressure_kbar"])
        - float(baseline_observables["pressure_kbar"]),
        "dielectric_mean": sum(diagnostic_observables["dielectric_eigenvalues"]) / 3.0
        - sum(baseline_observables["dielectric_eigenvalues"]) / 3.0,
        "raw_optical_mean_cm1": float(diagnostic_observables["raw_optical_mean_cm1"])
        - float(baseline_observables["raw_optical_mean_cm1"]),
        "simple_asr_optical_mean_cm1": float(
            diagnostic_observables["simple_asr_optical_mean_cm1"]
        )
        - float(baseline_observables["simple_asr_optical_mean_cm1"]),
    }
    return {
        "schema_version": "1.0",
        "status": "cdte_a0_stricter_response_comparison_completed",
        "baseline_source": contract["baseline"],
        "diagnostic_settings": contract["required_settings"],
        "ratios_to_baseline": ratios,
        "collapse_checks": collapse_checks,
        "observable_deltas": deltas,
        "decision": {
            "all_three_failed_response_metrics_materially_collapsed": materially_collapsed,
            "a1_electron_phonon_authorized": False,
            "automatic_additional_compute_authorized": False,
            "interpretation": (
                "Tightening ecutrho and tr2_ph materially reduced all three failed "
                "response diagnostics. This supports a numerical-response explanation, "
                "but one comparison is not convergence and A1 remains blocked."
                if materially_collapsed
                else "Tightening ecutrho and tr2_ph did not materially reduce all "
                "three failed response diagnostics. Stop numerical tightening and "
                "reassess volume stress, pseudopotential response, and DFPT formulation "
                "before any further compute."
            ),
            "next_action": (
                "write a separate bounded response-convergence decision before any new point"
                if materially_collapsed
                else "perform analytical root-cause review; no additional calculation is authorized"
            ),
        },
        "claim_boundary": contract["claim_boundary"],
    }


def analyze(
    baseline_path: str | Path,
    diagnostic_path: str | Path,
    contract_path: str | Path,
) -> dict[str, Any]:
    baseline = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    diagnostic = json.loads(Path(diagnostic_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    result = compare(baseline, diagnostic, contract)
    result["input_sha256"] = {
        "baseline": _sha256(baseline_path),
        "diagnostic": _sha256(diagnostic_path),
        "contract": _sha256(contract_path),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--diagnostic", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.baseline, args.diagnostic, args.contract)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
