from __future__ import annotations

import copy
from pathlib import Path

import pytest

from mct_research.r04_bounded_literature_constraints import (
    BoundedConstraintValidationError,
    load_constraint_package,
    validate_constraint_package,
)


ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "data" / "validation" / "r04_bounded_literature_constraints.json"


def _record() -> dict:
    return load_constraint_package(RECORD_PATH)


def _constraint(record: dict, constraint_id: str) -> dict:
    return next(item for item in record["constraints"] if item["id"] == constraint_id)


def test_reference_constraint_package_validates() -> None:
    validate_constraint_package(_record())


def test_no_probability_distribution_is_assigned() -> None:
    record = _record()
    assert record["default_probability_distributions_assigned"] is False
    assert all(item["distribution"] is None for item in record["constraints"])


def test_distribution_assignment_is_rejected() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "chang_cdte_si_center_sigma_x")["distribution"] = "normal"
    with pytest.raises(BoundedConstraintValidationError, match="may not assign a distribution"):
        validate_constraint_package(record)


def test_bovkun_range_cannot_become_probability_interval() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "bovkun_qw_boundary_composition")["is_probability_interval"] = True
    with pytest.raises(BoundedConstraintValidationError, match="not a probability interval"):
        validate_constraint_package(record)


def test_bovkun_model_broadening_cannot_become_measured_kernel() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "bovkun_kp_broadening_convention")["is_measured_energy_kernel"] = True
    with pytest.raises(BoundedConstraintValidationError, match="not a measured kernel"):
        validate_constraint_package(record)


def test_chang_sigma_cannot_become_local_random_variance() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "chang_cdte_si_full_sigma_x")["stationary_local_variance"] = True
    with pytest.raises(BoundedConstraintValidationError, match="not stationary local variance"):
        validate_constraint_package(record)


def test_chang_sigma_ratio_is_recomputed() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "chang_full_to_center_sigma_ratio")["value"] = 4.0
    with pytest.raises(BoundedConstraintValidationError, match="Chang sigma ratio mismatch"):
        validate_constraint_package(record)


def test_biquard_depth_kernel_cannot_become_correlation_length() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "biquard_micro_laue_depth_kernel")["is_target_material_correlation_length"] = True
    with pytest.raises(BoundedConstraintValidationError, match="not a correlation length"):
        validate_constraint_package(record)


def test_biquard_width_ratio_is_recomputed() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "biquard_measured_to_nominal_width_ratio")["value"] = 1.0
    with pytest.raises(BoundedConstraintValidationError, match="Biquard width ratio mismatch"):
        validate_constraint_package(record)


def test_zha_apparent_gap_cannot_become_local_dos() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "zha_flat_region_apparent_gap_excess")["is_direct_local_dos"] = True
    with pytest.raises(BoundedConstraintValidationError, match="not direct local DOS"):
        validate_constraint_package(record)


def test_zha_gap_excess_is_recomputed() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "zha_flat_region_apparent_gap_excess")["value"] = 0.10
    with pytest.raises(BoundedConstraintValidationError, match="Zha gap excess mismatch"):
        validate_constraint_package(record)


def test_zha_bias_contrast_cannot_become_geometry() -> None:
    record = copy.deepcopy(_record())
    _constraint(record, "zha_bias_dependent_apparent_pit_depth")["is_geometric_depth_change"] = True
    with pytest.raises(BoundedConstraintValidationError, match="not geometric depth"):
        validate_constraint_package(record)


def test_cross_paper_specimen_synthesis_remains_disabled() -> None:
    record = copy.deepcopy(_record())
    record["cross_paper_specimen_synthesis"] = True
    with pytest.raises(BoundedConstraintValidationError, match="cross-paper specimen synthesis"):
        validate_constraint_package(record)


def test_r05_activation_remains_blocked() -> None:
    record = copy.deepcopy(_record())
    record["r05_material_activation"] = "ACTIVE"
    with pytest.raises(BoundedConstraintValidationError, match="R05 must remain blocked"):
        validate_constraint_package(record)


def test_new_simulation_remains_unauthorized() -> None:
    record = copy.deepcopy(_record())
    record["new_simulation_authorized"] = True
    with pytest.raises(BoundedConstraintValidationError, match="new simulation remains unauthorized"):
        validate_constraint_package(record)
