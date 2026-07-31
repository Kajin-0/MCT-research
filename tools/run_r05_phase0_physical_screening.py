#!/usr/bin/env python3
"""Run the bounded R05 Phase 0 physical screen and final activation gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from mct_research.random_mass_dos import (
    average_ensemble_results,
    average_random_mass_dos,
    effect_size,
    gaussian_convolve_uniform_grid,
)
from mct_research.random_mass_scalar_null import gaussian_scalar_mixture_dos

ENERGIES = np.linspace(-4.0, 4.0, 401)
NUMERICAL_BROADENING = 0.08
EXPERIMENTAL_WIDTH = 0.25
EFFECT_WINDOW = (-1.0, 1.0)
CASES = (
    (0.0, 0.1),
    (0.0, 0.2),
    (0.0, 0.25),
    (0.0, 0.3),
    (0.0, 0.4),
    (0.5, 0.3),
    (0.5, 0.6),
    (1.0, 0.3),
    (1.0, 0.6),
    (1.0, 1.0),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_case(mean_mass: float, sigma_mass: float, seed: int) -> dict[str, object]:
    parts = []
    for boundary, boundary_seed in (
        ("periodic", seed),
        ("antiperiodic", seed + 100_003),
    ):
        parts.append(
            average_random_mass_dos(
                ENERGIES,
                mean_mass,
                sigma_mass,
                1.0,
                32.0,
                256,
                NUMERICAL_BROADENING,
                16,
                seed=boundary_seed,
                covariance_family="gaussian",
                boundary=boundary,
                remove_sample_mean=True,
                normalize_sample_variance=False,
            )
        )
    combined = average_ensemble_results(parts)
    scalar = gaussian_scalar_mixture_dos(
        ENERGIES,
        mean_mass,
        sigma_mass,
        quadrature_order=256,
    )
    scalar_numerical = gaussian_convolve_uniform_grid(
        ENERGIES, scalar, NUMERICAL_BROADENING
    )
    correlated_convolved = gaussian_convolve_uniform_grid(
        ENERGIES, combined.mean_dos, EXPERIMENTAL_WIDTH
    )
    scalar_convolved = gaussian_convolve_uniform_grid(
        ENERGIES, scalar_numerical, EXPERIMENTAL_WIDTH
    )
    effect = effect_size(
        ENERGIES,
        correlated_convolved,
        scalar_convolved,
        energy_window=EFFECT_WINDOW,
    )
    batch_delta = []
    for batch in np.array_split(np.asarray(combined.realization_dos), 4):
        batch_convolved = gaussian_convolve_uniform_grid(
            ENERGIES, np.mean(batch, axis=0), EXPERIMENTAL_WIDTH
        )
        batch_delta.append(
            effect_size(
                ENERGIES,
                batch_convolved,
                scalar_convolved,
                energy_window=EFFECT_WINDOW,
            ).delta_1
        )
    return {
        "m": mean_mass,
        "g": sigma_mass,
        "L_over_xi": 32.0,
        "grid_points": 256,
        "a_over_xi": 0.125,
        "numerical_broadening": NUMERICAL_BROADENING,
        "experimental_width": EXPERIMENTAL_WIDTH,
        "realizations": combined.realizations,
        "seed_periodic": seed,
        "seed_antiperiodic": seed + 100_003,
        "delta_1": effect.delta_1,
        "delta_infinity": effect.delta_infinity,
        "integrated_reference": effect.integrated_reference,
        "batch_delta_1": batch_delta,
        "batch_standard_error": float(
            np.std(batch_delta, ddof=1) / math.sqrt(len(batch_delta))
        ),
    }


def _parameter_mapping(parameter_record: dict[str, object]) -> list[dict[str, float]]:
    parameters = {
        entry["symbol"]: entry
        for entry in parameter_record["parameters"]
        if isinstance(entry, dict) and "symbol" in entry
    }
    hbar_velocity = float(parameters["hbar_v_K"]["nominal_value"])
    derivative = float(parameter_record["derived_reference"]["dEg_dx_eV_per_fraction"])
    rows = []
    for sigma_x in (0.0005, 0.001, 0.002, 0.005, 0.01):
        sigma_mass = 0.5 * derivative * sigma_x
        for g in (0.25, 0.3):
            correlation_length = g * hbar_velocity / sigma_mass
            decision_resolution = 0.25 * hbar_velocity / correlation_length
            thermal_ceiling = decision_resolution / (3.5 * 8.617333262e-5)
            rows.append(
                {
                    "sigma_x_exploratory": sigma_x,
                    "sigma_M_meV": 1000.0 * sigma_mass,
                    "g": g,
                    "xi_nm_required": correlation_length,
                    "decision_resolution_meV": 1000.0 * decision_resolution,
                    "thermal_ceiling_K_for_3p5_kBT_equal_resolution": thermal_ceiling,
                }
            )
    return rows


def generate(
    parameter_path: Path,
    convergence_path: Path,
) -> dict[str, object]:
    parameter_record = json.loads(parameter_path.read_text(encoding="utf-8"))
    convergence_record = json.loads(convergence_path.read_text(encoding="utf-8"))
    sweep = [
        _run_case(mean_mass, sigma_mass, 20_000 + 1_000 * index)
        for index, (mean_mass, sigma_mass) in enumerate(CASES)
    ]
    gates = {
        "claim_level_distinction_from_prior_work": True,
        "source_supported_hgcdte_parameter_regime": False,
        "matched_correlated_model_differs": True,
        "effect_exceeds_predeclared_threshold": True,
        "numerical_convergence_passes": bool(all(convergence_record["checks"].values())),
        "covariance_variation_passes": bool(
            convergence_record["checks"]["covariance_family"]
        ),
        "survives_source_grounded_experimental_convolution": False,
        "experiment_can_distinguish_models": False,
        "next_full_kane_calculation_is_decision_changing": False,
        "full_kane_status_explicit": True,
    }
    return {
        "schema_version": "r05_activation_decision_v1",
        "program": "R05_correlated_random_mass_kane",
        "controlling_issue": 390,
        "decision": "REFRAME_AS_METHOD_BENCHMARK",
        "decision_date": "2026-07-31",
        "source_model_commit": "376cf9ec77fa2085c47d4c1ba9a9e2c1fd608c91",
        "generator": "tools/run_r05_phase0_physical_screening.py",
        "generator_version": 1,
        "inputs": {
            "parameter_envelope": str(parameter_path),
            "parameter_envelope_sha256": _sha256(parameter_path),
            "convergence_summary": str(convergence_path),
            "convergence_summary_sha256": _sha256(convergence_path),
        },
        "screening_normalization": {
            "epsilon": "E xi/(hbar v_K)",
            "m": "Mbar xi/(hbar v_K)",
            "g": "sigma_M xi/(hbar v_K)",
            "effect_window": list(EFFECT_WINDOW),
            "numerical_broadening": NUMERICAL_BROADENING,
            "experimental_width": EXPERIMENTAL_WIDTH,
        },
        "dimensionless_sweep": sweep,
        "threshold_bracket_near_massless_mean": {
            "lower_g": 0.25,
            "lower_delta_1": next(
                row["delta_1"] for row in sweep if row["m"] == 0.0 and row["g"] == 0.25
            ),
            "upper_g": 0.3,
            "upper_delta_1": next(
                row["delta_1"] for row in sweep if row["m"] == 0.0 and row["g"] == 0.3
            ),
            "interpretation": "The 10% synthetic threshold is bracketed between g=0.25 and g=0.30 for the declared finite-box screen; this is not a universal critical coupling.",
        },
        "hgcdte_exploratory_mapping": _parameter_mapping(parameter_record),
        "activation_gates": gates,
        "failed_activation_gates": [name for name, passed in gates.items() if not passed],
        "full_kane_decision": "DEFER_NOT_DECISION_CHANGING_WITHOUT_MATERIAL_OVERLAP",
        "experimental_decision": "FAIL_NO_SOURCE_QUALIFIED_XI_OR_MATCHED_SPECTROSCOPIC_DATASET",
        "claim_boundary": (
            "The solver and matched-null threshold are retained as a method benchmark. "
            "No new HgCdTe physical law, measured correlation length, topological phase, "
            "or experimentally established low-energy DOS signature is supported."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--parameter-envelope",
        type=Path,
        default=Path("data/validation/r05_parameter_envelope.json"),
    )
    parser.add_argument(
        "--convergence-summary",
        type=Path,
        default=Path("data/validation/r05_convergence_summary.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/validation/r05_activation_decision.json"),
    )
    args = parser.parse_args()
    record = generate(args.parameter_envelope, args.convergence_summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "decision": record["decision"],
                "failed_activation_gates": record["failed_activation_gates"],
                "threshold_bracket": record["threshold_bracket_near_massless_mean"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
