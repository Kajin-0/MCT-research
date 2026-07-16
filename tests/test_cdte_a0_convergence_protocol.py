from __future__ import annotations

import copy
import json
from pathlib import Path

from tools.check_cdte_a0_convergence_protocol import evaluate_convergence_protocol

RUN_SPEC_PATH = Path("first_principles/a0/cdte_a0_run_spec.json")
SELECTION_PATH = Path("first_principles/a0/cdte_pseudopotential_selection.json")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_repository_convergence_protocol_is_internally_valid_and_not_run() -> None:
    report = evaluate_convergence_protocol(_load(RUN_SPEC_PATH), _load(SELECTION_PATH))

    assert report["protocol_valid"] is True
    assert report["blocking_checks"] == []
    assert report["passed_checks"] == report["total_checks"]


def test_ecutrho_values_must_match_reference_cutoff_times_ratios() -> None:
    specification = copy.deepcopy(_load(RUN_SPEC_PATH))
    specification["convergence_ladders"]["ecutrho_ry"][1] += 1

    report = evaluate_convergence_protocol(specification, _load(SELECTION_PATH))

    assert report["protocol_valid"] is False
    assert "ecutrho_ratio_ladder_consistent" in report["blocking_checks"]


def test_k_grid_must_be_even_gamma_centered_and_increasing() -> None:
    specification = copy.deepcopy(_load(RUN_SPEC_PATH))
    specification["convergence_ladders"]["k_grid_n"] = [4, 6, 9, 12]
    specification["convergence_ladders"]["k_grid_shift"] = [1, 1, 1]

    report = evaluate_convergence_protocol(specification, _load(SELECTION_PATH))

    assert report["protocol_valid"] is False
    assert "gamma_centered_even_k_grid_ladder" in report["blocking_checks"]


def test_band_ladder_must_follow_verified_valence_electron_count() -> None:
    specification = copy.deepcopy(_load(RUN_SPEC_PATH))
    specification["convergence_ladders"]["total_valence_electrons"] = 18
    specification["convergence_ladders"]["empty_spinor_bands"] = [22, 30, 38, 46]

    report = evaluate_convergence_protocol(specification, _load(SELECTION_PATH))

    assert report["protocol_valid"] is False
    assert "soc_spinor_band_ladder_consistent" in report["blocking_checks"]


def test_protocol_cannot_claim_results_or_skip_cross_factor_recheck() -> None:
    specification = copy.deepcopy(_load(RUN_SPEC_PATH))
    specification["convergence_ladders"]["selection_status"] = "converged"
    specification["convergence_protocol"]["calculation_results_recorded"] = True
    specification["convergence_protocol"]["cross_factor_recheck_required"] = False

    report = evaluate_convergence_protocol(specification, _load(SELECTION_PATH))

    assert report["protocol_valid"] is False
    assert "declared_not_run" in report["blocking_checks"]
    assert "sequential_one_factor_protocol" in report["blocking_checks"]


def test_every_governed_ladder_supports_two_successive_refinements() -> None:
    specification = copy.deepcopy(_load(RUN_SPEC_PATH))
    specification["convergence_ladders"]["ph_tr2"] = [1e-12, 1e-14]

    report = evaluate_convergence_protocol(
        specification,
        _load(SELECTION_PATH),
    )

    assert report["protocol_valid"] is False
    assert (
        "governed_ladders_support_two_refinements"
        in report["blocking_checks"]
    )
