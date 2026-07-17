from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest

from tools.cdte_volume_grid import (
    build_volume_grid,
    grid_from_specification,
    lattice_scale_from_volume_fraction,
)

RUN_SPEC_PATH = Path("first_principles/a0/cdte_a0_run_spec.json")


def _load_specification() -> dict:
    return json.loads(RUN_SPEC_PATH.read_text(encoding="utf-8"))


def test_cubic_volume_offsets_are_not_lattice_offsets() -> None:
    low = lattice_scale_from_volume_fraction(-0.005)
    high = lattice_scale_from_volume_fraction(0.005)

    assert low == pytest.approx(0.9983305478136913)
    assert high == pytest.approx(1.001663896579312)
    assert low - 1.0 != pytest.approx(-0.005)
    assert high - 1.0 != pytest.approx(0.005)
    assert low**3 == pytest.approx(0.995)
    assert high**3 == pytest.approx(1.005)


def test_repository_protocol_is_symmetric_and_fixed_volume() -> None:
    specification = _load_specification()
    protocol = specification["structure"]["fixed_volume_protocol"]

    assert protocol["reference_temperature_k"] == 0
    assert protocol["temperature_dependent_electron_phonon_runs_use_one_volume"] is True
    assert protocol["quasiharmonic_volume_path_authorized_in_a0"] is False
    assert protocol["volume_fractional_offsets"] == [-0.005, 0.0, 0.005]

    expected = [
        lattice_scale_from_volume_fraction(value)
        for value in protocol["volume_fractional_offsets"]
    ]
    assert protocol["lattice_scale_factors"] == pytest.approx(expected)
    assert "added once" in protocol["double_counting_rule"]


def test_repository_bounded_execution_grid_is_auditable() -> None:
    specification = _load_specification()
    result = grid_from_specification(specification)

    assert result["reference_status"] == "execution_reference"
    assert result["execution_authorized"] is True
    assert result["reference_source_type"] == (
        "primary_experimental_with_bounded_transform"
    )
    assert result["reference_lattice_constant_angstrom"] == pytest.approx(
        6.476035479332049
    )
    assert result["reference_lattice_conservative_bound_angstrom"] == pytest.approx(
        0.0018149594091957418
    )
    assert [point["volume_ratio"] for point in result["points"]] == pytest.approx(
        [0.995, 1.0, 1.005]
    )
    for point in result["points"]:
        assert math.isclose(
            (
                point["lattice_constant_angstrom"]
                / result["reference_lattice_constant_angstrom"]
            )
            ** 3,
            point["volume_ratio"],
            rel_tol=0.0,
            abs_tol=1e-14,
        )


def test_planning_grid_remains_explicitly_non_executable() -> None:
    specification = copy.deepcopy(_load_specification())
    specification["structure"]["execution_lattice_constant_angstrom"] = None

    with pytest.raises(ValueError, match="execution lattice is unresolved"):
        grid_from_specification(specification)

    result = grid_from_specification(
        specification,
        allow_planning_candidate=True,
    )
    assert result["reference_status"] == "planning_candidate_only"
    assert result["execution_authorized"] is False
    assert result["reference_source_type"] is None
    assert result["reference_lattice_conservative_bound_angstrom"] is None
    assert result["reference_lattice_constant_angstrom"] == pytest.approx(6.482)


def test_primary_execution_anchor_generates_auditable_grid() -> None:
    specification = copy.deepcopy(_load_specification())
    structure = specification["structure"]
    structure["execution_lattice_constant_angstrom"] = 6.47
    structure["execution_lattice_constant_source"] = {
        "source_type": "primary_experimental",
        "source_sha256": "a" * 64,
    }

    result = grid_from_specification(specification)

    assert result["reference_status"] == "execution_reference"
    assert result["execution_authorized"] is True
    assert result["reference_source_type"] == "primary_experimental"
    assert result["reference_lattice_conservative_bound_angstrom"] is None
    for point in result["points"]:
        assert math.isclose(
            (point["lattice_constant_angstrom"] / 6.47) ** 3,
            point["volume_ratio"],
            rel_tol=0.0,
            abs_tol=1e-14,
        )


def test_execution_grid_rejects_nonhex_source_hash() -> None:
    specification = copy.deepcopy(_load_specification())
    structure = specification["structure"]
    structure["execution_lattice_constant_angstrom"] = 6.47
    structure["execution_lattice_constant_source"] = {
        "source_type": "primary_experimental",
        "source_sha256": "z" * 64,
    }

    with pytest.raises(ValueError, match="accepted primary source record and SHA-256"):
        grid_from_specification(specification)


def test_bounded_grid_rejects_failed_volume_gate() -> None:
    specification = copy.deepcopy(_load_specification())
    source = specification["structure"]["execution_lattice_constant_source"]
    source["execution_uncertainty"]["volume_sensitivity_gate_passed"] = False

    with pytest.raises(ValueError, match="accepted primary source record and SHA-256"):
        grid_from_specification(specification)


def test_grid_rejects_asymmetric_offsets() -> None:
    with pytest.raises(ValueError, match="symmetric"):
        build_volume_grid(6.482, [-0.005, 0.0, 0.01])
