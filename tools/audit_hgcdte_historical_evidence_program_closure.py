#!/usr/bin/env python3
"""Fail-closed audit for Issue #132 historical-evidence closure."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

EXPECTED_PRS = [131, 133, 134, 135, 137, 138, 142, 144, 146, 150, 152, 154, 156, 158]
EXPECTED_STOP_RULES = {
    "composition_dominates": True,
    "winner_changes_with_treatment": True,
    "class_offsets_not_universal": True,
    "model_conditioned_composition_present": True,
    "independent_validation_insufficient": True,
    "more_coefficients": False,
    "more_unpaired_sources": False,
}
EXPECTED_DECISION = {
    "close_parent_issue": True,
    "historical_integration_complete": True,
    "pool_observation_classes": False,
    "fit_universal_gap_law": False,
    "reopen_manuscript": False,
    "next_track": "paired_acquisition_protocol",
}


def _close(actual: Any, expected: float, field: str, tol: float = 1.0e-12) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=tol
    ):
        raise ValueError(f"{field} changed: {actual!r} != {expected!r}")


def audit(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported closure schema")
    if data.get("parent_issue") != 132 or data.get("closure_issue") != 159:
        raise ValueError("issue identity changed")
    if data.get("status") != "complete_under_non_identifiability_stop_rules":
        raise ValueError("program status changed")
    if data.get("evidence_prs") != EXPECTED_PRS:
        raise ValueError("merged evidence inventory changed")
    if data.get("copyrighted_source_content_committed") is not False:
        raise ValueError("copyrighted source content may not be committed")

    questions = data.get("questions")
    if not isinstance(questions, dict) or len(questions) != 5:
        raise ValueError("all five Issue 132 questions must be answered")

    q1 = questions["independent_magneto_labs"]
    if q1.get("answer") != "qualitative_agreement_only" or q1.get("few_meV_ranking") is not False:
        raise ValueError("magneto-optical identifiability conclusion changed")
    _close(q1["gap_fit_sigma_meV"], 3.0, "Weiler fit uncertainty")
    if q1.get("composition_scale_meV") != [8.945, 27.84]:
        raise ValueError("composition propagation range changed")
    _close(q1["model_observable_discrepancy_meV"], 4.0, "model discrepancy")

    q2 = questions["groves_sign_change"]
    if q2.get("answer") != "rejects_schmit_stelzer_at_4K_but_selects_no_universal_model":
        raise ValueError("Groves sign conclusion changed")
    _close(q2["composition_x"], 0.161, "Groves composition")
    _close(q2["composition_sigma"], 0.003, "Groves sigma_x")
    if q2.get("schmit_stelzer_pass") is not False:
        raise ValueError("Schmit-Stelzer cannot pass the Groves 4 K sign gate")
    if q2.get("chu_status") != "composition_ambiguous":
        raise ValueError("Chu sign status changed")
    if q2.get("hansen_seiler_laurenti_pade_pass") is not True:
        raise ValueError("accepted Groves sign comparators changed")

    q3 = questions["absorption_method_spread"]
    if q3.get("answer") != "several_to_tens_of_meV":
        raise ValueError("absorption spread conclusion changed")
    if q3.get("moazzami_meV") != [6.414, 6.83]:
        raise ValueError("Moazzami span changed")
    if q3.get("finkman_threshold_meV") != [15.028284, 37.637923]:
        raise ValueError("Finkman threshold range changed")
    if q3.get("finkman_zero_intercept_meV") != [20.10684, 21.348002]:
        raise ValueError("Finkman zero-intercept range changed")
    _close(q3["mroczkowski_efold_change_meV"], 2.7670528, "vacancy e-fold change")
    if q3.get("yue_anomaly_meV") != [9.7, 11.3]:
        raise ValueError("Yue anomaly range changed")
    if q3.get("pool_as_one_distribution") is not False:
        raise ValueError("distinct physical coordinates cannot be pooled by default")

    q4 = questions["chang_real_spectrum_enlargement"]
    if q4.get("answer") != "not_identified":
        raise ValueError("Chang real-spectrum decision changed")
    if q4.get("operator_implemented") is not True:
        raise ValueError("Chang operator implementation status changed")
    if any(q4.get(field) is not False for field in (
        "native_data_recovered", "temperature_resolved", "same_specimen_W_b_recovered"
    )):
        raise ValueError("Chang Figure 2 readiness was promoted without evidence")
    if q4.get("synthetic_shift_meV") != [0.265, 1.72]:
        raise ValueError("Chang synthetic sensitivity range changed")

    q5 = questions["historical_model_ordering"]
    if q5.get("answer") != "not_stable" or q5.get("universal_selection") is not False:
        raise ValueError("historical model-ordering decision changed")
    _close(q5["chu_offset_transfer_seiler_hansen_difference_meV"], 0.091, "Chu Seiler-Hansen difference")
    if q5.get("manuscript_seiler_advantage_meV") != [0.177, 0.255]:
        raise ValueError("manuscript Seiler-Hansen range changed")
    if q5.get("threshold_changes_winner") is not True or q5.get("source_class_changes_winner") is not True:
        raise ValueError("winner-instability evidence changed")

    if data.get("stop_rules") != EXPECTED_STOP_RULES:
        raise ValueError("stop-rule decision changed")
    if data.get("decision") != EXPECTED_DECISION:
        raise ValueError("final program decision changed")

    outputs = data.get("outputs")
    if not isinstance(outputs, dict) or set(outputs.values()) - {
        "complete", "complete_with_blocked_fields", "complete_where_justified", "this_tranche"
    }:
        raise ValueError("required-output status changed")
    if len(data.get("reopen_only_for", [])) != 3:
        raise ValueError("reopening gate inventory changed")

    q1_min = min(q1["composition_scale_meV"])
    manuscript_max = max(q5["manuscript_seiler_advantage_meV"])
    return {
        "schema_version": data["schema_version"],
        "parent_issue": data["parent_issue"],
        "answered_question_count": len(questions),
        "evidence_pr_count": len(data["evidence_prs"]),
        "triggered_stop_rule_count": sum(value is True for value in data["stop_rules"].values()),
        "minimum_composition_scale_meV": q1_min,
        "maximum_manuscript_model_separation_meV": manuscript_max,
        "composition_to_model_separation_ratio": q1_min / manuscript_max,
        "historical_integration_complete": data["decision"]["historical_integration_complete"],
        "close_parent_issue": data["decision"]["close_parent_issue"],
        "next_track": data["decision"]["next_track"],
        "decision": data["decision"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.input_json)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        Path(args.output_json).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
