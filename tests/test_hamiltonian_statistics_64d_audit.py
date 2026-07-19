from __future__ import annotations

from pathlib import Path

import pytest

from tools.audit_hamiltonian_statistics_64d import (
    STANDARD_ERROR_RATIO_TOLERANCE,
    analyze,
)

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data/evidence/hamiltonian_statistics_64d_inventory.csv"


def result() -> dict[str, object]:
    return analyze(INVENTORY)


def test_point_estimates_and_numeric_sse_are_preserved() -> None:
    audit = result()
    comparison = audit["comparison"]
    assert comparison["maximum_parameter_difference"] <= 1e-10
    assert comparison["numeric_sse_difference"] <= 1e-18
    assert audit["decision"][
        "deterministic_static_point_estimates_retain_validity"
    ] is True
    assert audit["decision"][
        "deterministic_frobenius_residuals_retain_validity"
    ] is True


def test_observation_count_and_degrees_of_freedom_are_corrected() -> None:
    audit = result()
    old = audit["legacy_unweighted"]
    new = audit["current_unweighted"]
    assert old["observation_count"] == 768
    assert new["observation_count"] == 384
    assert old["rank"] == new["rank"] == 8
    assert old["degrees_of_freedom"] == 760
    assert new["degrees_of_freedom"] == 376
    expected_ratio = 760 / 376
    assert audit["comparison"]["legacy_to_current_dof_ratio"] == pytest.approx(
        expected_ratio, abs=1e-14
    )
    assert audit["comparison"][
        "reduced_chi_square_ratio_current_to_legacy"
    ] == pytest.approx(expected_ratio, abs=1e-12)


def test_variance_scaled_standard_errors_increase_by_expected_ratio() -> None:
    audit = result()
    expected = (760 / 376) ** 0.5
    assert audit["comparison"][
        "expected_current_to_legacy_standard_error_ratio"
    ] == pytest.approx(expected, abs=1e-14)
    assert audit["comparison"]["standard_error_ratio_tolerance"] == (
        STANDARD_ERROR_RATIO_TOLERANCE
    )
    for ratio in audit["comparison"]["standard_error_ratios"].values():
        assert ratio == pytest.approx(
            expected, abs=STANDARD_ERROR_RATIO_TOLERANCE
        )
    assert audit["decision"][
        "legacy_variance_scaled_standard_errors_retain_validity"
    ] is False


def test_absolute_covariance_subspace_statistics_are_equivalent() -> None:
    audit = result()["absolute_covariance_equivalence"]
    assert audit["legacy_covariance_dimension"] == 128
    assert audit["legacy_covariance_rank"] == 64
    assert audit["current_covariance_dimension"] == 64
    assert audit["maximum_parameter_difference"] <= 1e-10
    assert audit["chi_square_difference"] <= 1e-8
    assert audit["parameter_covariance_frobenius_difference"] <= 1e-10


def test_inventory_separates_affected_and_unaffected_outputs() -> None:
    audit = result()
    inventory = audit["repository_inventory"]
    assert inventory["row_count"] == 11
    assert inventory["counts_by_disposition"] == {
        "regenerated": 2,
        "unaffected": 6,
        "out_of_scope": 3,
    }
    assert inventory["regenerated"] == [
        "src/mct_research/projection.py",
        "tests/test_hermitian_covariance_coordinates.py",
    ]
    assert audit["decision"][
        "committed_physical_hamiltonian_statistical_values_replaced"
    ] is False


def test_all_regeneration_checks_pass() -> None:
    assert all(result()["validation_checks"].values())
