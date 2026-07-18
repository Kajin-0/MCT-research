from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from mct_research.kane8 import ExtendedKaneParameters, hamiltonian_two_p
from tools.run_zg_selected_band_matrix_oracle import (
    evaluate,
    project_gamma_irreps,
    reconstruct_selected_matrix,
    simulate_supercell_eigenpairs,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/matrix_oracle/zg_selected_band_matrix_reconstruction_contract.json"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_complete_zg_reconstruction_oracle_passes() -> None:
    result = evaluate(_contract())
    metrics = result["metrics"]
    decision = result["decision"]

    assert all(result["checks"].values())
    assert metrics["minimum_selected_overlap_singular_value"] > 0.95
    assert metrics["maximum_per_configuration_reconstruction_relative_error"] < 1e-12
    assert metrics["minimum_unpaired_configuration_relative_error"] > 1e-3
    assert metrics["minimum_pre_restoration_symmetry_residual"] > 1e-4
    assert metrics["maximum_post_restoration_symmetry_residual"] < 1e-12
    assert metrics["maximum_final_matrix_relative_error"] < 1e-12
    assert metrics["maximum_extended_parameter_absolute_error"] < 1e-10
    assert metrics["maximum_holdout_matrix_relative_error"] < 1e-12
    assert metrics["minimum_naive_eigenvalue_only_matrix_relative_error"] > 1e-3

    assert decision["selected_band_supercell_reconstruction_ready"] is True
    assert decision["displacement_pairing_required"] is True
    assert decision["multiple_configuration_averaging_required"] is True
    assert decision["Gamma_and_time_reversal_restoration_required"] is True
    assert decision["eigenvalue_only_ZG_analysis_forbidden"] is True
    assert decision["real_ZG_export_contract_design_authorized"] is True
    assert decision["real_ZG_execution_authorized"] is False
    assert decision["finite_size_polar_correction_ready"] is False
    assert decision["automatic_additional_compute_authorized"] is False


def test_supercell_polar_reconstruction_is_gauge_invariant() -> None:
    parameters = ExtendedKaneParameters(
        ev=0.0,
        eg=0.31,
        delta=0.90,
        p8=7.0,
        p7=6.3,
        f=-0.1,
        gamma1=4.5,
        gamma2=1.2,
        gamma3=1.7,
    )
    matrix = hamiltonian_two_p([0.0, 0.0, 0.0], parameters)
    reconstructions = []
    singular_values = []
    for seed in (1, 2, 3):
        energies, vectors, reference = simulate_supercell_eigenpairs(
            matrix,
            rng=np.random.default_rng(seed),
            supercell_dimension=16,
            leakage_range=(0.08, 0.28),
            remote_energy_range=(2.0, 4.0),
            degeneracy_tolerance_ev=1e-9,
        )
        reconstructed, diagnostics = reconstruct_selected_matrix(
            energies, vectors, reference, 8
        )
        reconstructions.append(reconstructed)
        singular_values.append(diagnostics["minimum_selected_overlap_singular_value"])

    for reconstructed in reconstructions:
        assert np.linalg.norm(reconstructed - matrix) / np.linalg.norm(matrix) < 1e-12
    assert min(singular_values) > 0.95
    assert np.linalg.norm(reconstructions[0] - reconstructions[2]) < 1e-12


def test_gamma_projection_removes_only_non_irrep_structure() -> None:
    diagonal = np.diag([0.3, 0.3, 0.0, 0.0, 0.0, 0.0, -0.9, -0.9]).astype(
        np.complex128
    )
    artifact = np.zeros((8, 8), dtype=np.complex128)
    artifact[0, 1] = artifact[1, 0] = 0.01
    artifact[2, 2] = 0.02
    artifact[3, 3] = -0.02

    projected = project_gamma_irreps(diagonal + artifact)
    assert np.allclose(projected, diagonal)


def test_invalid_supercell_dimension_fails_closed() -> None:
    matrix = np.eye(8, dtype=np.complex128)
    with pytest.raises(ValueError, match="equal-size remote complement"):
        simulate_supercell_eigenpairs(
            matrix,
            rng=np.random.default_rng(1),
            supercell_dimension=17,
            leakage_range=(0.08, 0.28),
            remote_energy_range=(2.0, 4.0),
            degeneracy_tolerance_ev=1e-9,
        )
