#!/usr/bin/env python3
"""Generate deterministic R05 Phase 0 minimal-oracle reference records."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from mct_research.random_mass_covariance import (
    generate_random_mass_field,
    periodic_target_correlation,
)
from mct_research.random_mass_dirac import (
    dirac_eigenvalues,
    dirac_hamiltonian,
    hermiticity_residual,
    homogeneous_reference_eigenvalues,
    paired_spectrum_residual,
    periodic_domain_wall_pair,
)
from mct_research.random_mass_dos import (
    average_ensemble_results,
    average_random_mass_dos,
    effect_size,
    finite_box_gaussian_quadrature_dos,
    gaussian_convolve_uniform_grid,
)
from mct_research.random_mass_scalar_null import (
    gaussian_scalar_mixture_dos,
    zero_mean_gaussian_scalar_dos_exact,
)

E = np.linspace(-4.0, 4.0, 401)
ETA = 0.08
EXP_WIDTHS = (0.10, 0.25, 0.50, 1.00)
WINDOW = (-1.0, 1.0)


def integrate(y, x):
    return float(getattr(np, "trapezoid", np.trapz)(y, x))


def scalar_curve(m, g, eta=ETA):
    raw = gaussian_scalar_mixture_dos(E, m, g, quadrature_order=256)
    return gaussian_convolve_uniform_grid(E, raw, eta)


def metrics(result, m, g, eta):
    scalar = scalar_curve(m, g, eta)
    out = {}
    for width in EXP_WIDTHS:
        corr = gaussian_convolve_uniform_grid(E, result.mean_dos, width)
        null = gaussian_convolve_uniform_grid(E, scalar, width)
        value = effect_size(E, corr, null, energy_window=WINDOW)
        out[f"experimental_width_{width:.2f}"] = {
            "delta_1": value.delta_1,
            "delta_infinity": value.delta_infinity,
            "integrated_reference": value.integrated_reference,
            "maximum_reference": value.maximum_reference,
        }
    rows = np.asarray(result.realization_dos)
    if result.boundary == "combined":
        half = rows.shape[0] // 2
        rows = np.stack((rows[:half], rows[half:]), axis=1).reshape(rows.shape)
    null = gaussian_convolve_uniform_grid(E, scalar, 0.25)
    batch_delta = []
    for batch in np.array_split(rows, 4):
        corr = gaussian_convolve_uniform_grid(E, np.mean(batch, axis=0), 0.25)
        batch_delta.append(effect_size(E, corr, null, energy_window=WINDOW).delta_1)
    out.update(
        {
            "batch_delta_1_at_decision_width": batch_delta,
            "batch_standard_error_at_decision_width": float(
                np.std(batch_delta, ddof=1) / math.sqrt(4.0)
            ),
            "realized_sigma_mean": float(np.mean(result.realized_mass_sigmas)),
            "realized_sigma_standard_deviation": float(
                np.std(result.realized_mass_sigmas, ddof=1)
            ),
            "realized_mass_mean_maximum_absolute_error": float(
                np.max(np.abs(result.realized_mass_means - m))
            ),
        }
    )
    return out


def run_case(
    m,
    g,
    length,
    points,
    eta,
    realizations_each,
    seed,
    family="gaussian",
    remove_mean=True,
    normalize_variance=False,
    boundary_metrics=False,
):
    parts = []
    for boundary, boundary_seed in (
        ("periodic", seed),
        ("antiperiodic", seed + 100_003),
    ):
        parts.append(
            average_random_mass_dos(
                E,
                m,
                g,
                1.0,
                length,
                points,
                eta,
                realizations_each,
                seed=boundary_seed,
                covariance_family=family,
                boundary=boundary,
                remove_sample_mean=remove_mean,
                normalize_sample_variance=normalize_variance,
            )
        )
    combined = average_ensemble_results(parts)
    record = {
        "m": m,
        "g": g,
        "L_over_xi": length,
        "grid_points": points,
        "a_over_xi": length / points,
        "numerical_broadening": eta,
        "realizations": combined.realizations,
        "seed_periodic": seed,
        "seed_antiperiodic": seed + 100_003,
        "covariance_family": family,
        "remove_sample_mean": remove_mean,
        "normalize_sample_variance": normalize_variance,
        **metrics(combined, m, g, eta),
    }
    if boundary_metrics:
        record["periodic_metrics"] = metrics(parts[0], m, g, eta)
        record["antiperiodic_metrics"] = metrics(parts[1], m, g, eta)
    return record, combined


def common(schema):
    return {
        "schema_version": schema,
        "program": "R05_correlated_random_mass_kane",
        "controlling_issue": 390,
        "generator": "tools/run_r05_phase0_oracle.py",
        "generator_version": 1,
        "normalization": {
            "xi": 1.0,
            "hbar_velocity": 1.0,
            "epsilon": "E xi/(hbar v_K)",
            "m": "Mbar xi/(hbar v_K)",
            "g": "sigma_M xi/(hbar v_K)",
            "dos": "states per dimensionless length per dimensionless energy per two-component species",
        },
        "energy_grid": {
            "minimum": -4.0,
            "maximum": 4.0,
            "points": 401,
            "spacing": 0.02,
            "effect_window": list(WINDOW),
        },
        "numerical_broadening": ETA,
        "experimental_widths": list(EXP_WIDTHS),
        "decision_width": 0.25,
    }


def generate():
    reference = common("r05_phase0_reference_v1")
    mass = np.full(64, 0.7)
    hamiltonian = dirac_hamiltonian(mass, 16.0)
    eigenvalues = np.linalg.eigvalsh(hamiltonian)
    exact = homogeneous_reference_eigenvalues(64, 16.0, 0.7)
    scalar = gaussian_scalar_mixture_dos(E, 0.0, 0.8, quadrature_order=256)
    scalar_exact = zero_mean_gaussian_scalar_dos_exact(E, 0.8)
    reference["analytical_validation"] = {
        "hermiticity_residual": hermiticity_residual(hamiltonian),
        "paired_spectrum_residual": paired_spectrum_residual(eigenvalues),
        "homogeneous_maximum_absolute_eigenvalue_error": float(
            np.max(np.abs(eigenvalues - exact))
        ),
        "zero_mean_scalar_maximum_absolute_error": float(
            np.max(np.abs(scalar - scalar_exact))
        ),
    }

    fields = np.asarray(
        [
            generate_random_mass_field(128, 32.0, 0.0, 1.0, 1.0, seed=seed).fluctuation
            for seed in np.random.SeedSequence(9_041).spawn(512)
        ]
    )
    power = np.mean(np.abs(np.fft.fft(fields, axis=1)) ** 2, axis=0) / 128
    empirical = np.fft.ifft(power).real
    empirical /= empirical[0]
    target = periodic_target_correlation(128, 32.0, 1.0)
    reference["covariance_validation"] = {
        "realizations": 512,
        "ensemble_point_variance": float(np.mean(fields**2)),
        "maximum_absolute_correlation_error_first_16_lags": float(
            np.max(np.abs(empirical[:16] - target[:16]))
        ),
        "rms_correlation_error_first_16_lags": float(
            np.sqrt(np.mean((empirical[:16] - target[:16]) ** 2))
        ),
    }

    walls = []
    for length, points in ((20.0, 80), (40.0, 160), (60.0, 240)):
        profile = periodic_domain_wall_pair(points, length, 1.0, 1.0)
        levels = dirac_eigenvalues(profile, length, boundary="antiperiodic")
        walls.append(
            {
                "length": length,
                "grid_points": points,
                "a_over_wall_width": length / points,
                "minimum_absolute_eigenvalue": float(np.min(np.abs(levels))),
            }
        )
    reference["domain_wall_validation"] = walls

    finite = 0.5 * (
        finite_box_gaussian_quadrature_dos(
            E, 0.0, 0.8, 64.0, 128, ETA, boundary="periodic", quadrature_order=192
        )
        + finite_box_gaussian_quadrature_dos(
            E,
            0.0,
            0.8,
            64.0,
            128,
            ETA,
            boundary="antiperiodic",
            quadrature_order=192,
        )
    )
    analytic = scalar_curve(0.0, 0.8)
    mask = np.abs(E) <= 1.5
    null_error = integrate(np.abs(finite[mask] - analytic[mask]), E[mask]) / integrate(
        analytic[mask], E[mask]
    )
    reference["finite_box_scalar_validation"] = {
        "quadrature_order": 192,
        "L_over_xi": 64.0,
        "grid_points": 128,
        "boundary_average": ["periodic", "antiperiodic"],
        "integrated_relative_difference": null_error,
    }

    primary, ensemble = run_case(0.0, 0.3, 32.0, 256, ETA, 16, 39_005, boundary_metrics=True)
    primary.update(
        {
            "energies": E.tolist(),
            "correlated_dos": ensemble.mean_dos.tolist(),
            "correlated_standard_error": ensemble.standard_error.tolist(),
            "scalar_dos_numerically_broadened": scalar_curve(0.0, 0.3).tolist(),
        }
    )
    reference["primary_case"] = primary

    convergence = common("r05_convergence_summary_v1")
    convergence["primary_case_summary"] = {
        key: value
        for key, value in primary.items()
        if key
        not in {
            "energies",
            "correlated_dos",
            "correlated_standard_error",
            "scalar_dos_numerically_broadened",
        }
    }
    size_cases = [
        run_case(0.0, 0.3, length, points, ETA, 4, 50_000 + 100 * index)[0]
        for index, (length, points) in enumerate(
            ((16.0, 128), (32.0, 256), (64.0, 512), (32.0, 384), (32.0, 512))
        )
    ]
    broadening_cases = [
        run_case(0.0, 0.3, 32.0, 256, eta, 4, 55_000 + 100 * index)[0]
        for index, eta in enumerate((0.06, 0.08, 0.12))
    ]
    covariance_cases = [
        run_case(
            0.0,
            0.3,
            32.0,
            256,
            ETA,
            6,
            60_000 + 100 * index,
            family=family,
        )[0]
        for index, family in enumerate(
            ("gaussian", "matern_0.5", "matern_1.5", "matern_2.5")
        )
    ]
    conditioning_cases = [
        run_case(
            0.0,
            0.3,
            32.0,
            256,
            ETA,
            6,
            70_000 + 100 * index,
            remove_mean=remove,
            normalize_variance=normalize,
        )[0]
        for index, (remove, normalize) in enumerate(
            ((True, False), (True, True), (False, False))
        )
    ]
    convergence.update(
        {
            "size_and_grid_cases": size_cases,
            "numerical_broadening_cases": broadening_cases,
            "covariance_family_cases": covariance_cases,
            "field_conditioning_cases": conditioning_cases,
        }
    )

    delta = lambda record: float(record["experimental_width_0.25"]["delta_1"])
    accepted = [delta(record) for record in size_cases[1:]]
    grid = [delta(size_cases[index]) for index in (1, 3, 4)]
    broad = [delta(record) for record in broadening_cases]
    covariance = [delta(record) for record in covariance_cases]
    conditioning = [delta(record) for record in conditioning_cases]
    thresholds = {
        "minimum_converged_delta_1": 0.10,
        "maximum_primary_standard_error": 0.02,
        "maximum_finite_size_drift": 0.03,
        "maximum_discretization_drift": 0.03,
        "maximum_numerical_broadening_drift": 0.03,
        "minimum_covariance_family_delta_1": 0.10,
        "maximum_field_conditioning_drift": 0.03,
        "maximum_scalar_null_integrated_relative_difference": 0.01,
    }
    diagnostics = {
        "primary_delta_1": delta(primary),
        "primary_batch_standard_error": primary[
            "batch_standard_error_at_decision_width"
        ],
        "minimum_accepted_converged_delta_1": min(accepted),
        "maximum_accepted_converged_delta_1": max(accepted),
        "finite_size_drift": abs(delta(size_cases[2]) - delta(size_cases[1])),
        "discretization_drift": max(grid) - min(grid),
        "numerical_broadening_drift": max(broad) - min(broad),
        "minimum_covariance_family_delta_1": min(covariance),
        "maximum_covariance_family_delta_1": max(covariance),
        "field_conditioning_drift": max(conditioning) - min(conditioning),
        "scalar_null_integrated_relative_difference": null_error,
    }
    checks = {
        "effect_threshold": diagnostics["minimum_accepted_converged_delta_1"]
        > thresholds["minimum_converged_delta_1"],
        "sampling_uncertainty": diagnostics["primary_batch_standard_error"]
        <= thresholds["maximum_primary_standard_error"],
        "finite_size": diagnostics["finite_size_drift"]
        <= thresholds["maximum_finite_size_drift"],
        "discretization": diagnostics["discretization_drift"]
        <= thresholds["maximum_discretization_drift"],
        "numerical_broadening": diagnostics["numerical_broadening_drift"]
        <= thresholds["maximum_numerical_broadening_drift"],
        "covariance_family": diagnostics["minimum_covariance_family_delta_1"]
        > thresholds["minimum_covariance_family_delta_1"],
        "field_conditioning": diagnostics["field_conditioning_drift"]
        <= thresholds["maximum_field_conditioning_drift"],
        "scalar_null": null_error
        <= thresholds["maximum_scalar_null_integrated_relative_difference"],
    }
    convergence.update(
        {
            "thresholds": thresholds,
            "diagnostics": diagnostics,
            "checks": checks,
            "decision": "GO_PHYSICAL_SCREENING"
            if all(checks.values())
            else "STOP_NUMERICAL_EFFECT",
            "claim_boundary": (
                "Synthetic one-dimensional mechanism benchmark only; no HgCdTe "
                "material activation without a source-qualified mass-correlation length."
            ),
        }
    )
    return reference, convergence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference-output",
        type=Path,
        default=Path("data/validation/r05_phase0_reference.json"),
    )
    parser.add_argument(
        "--convergence-output",
        type=Path,
        default=Path("data/validation/r05_convergence_summary.json"),
    )
    args = parser.parse_args()
    reference, convergence = generate()
    for path, payload in (
        (args.reference_output, reference),
        (args.convergence_output, convergence),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"decision": convergence["decision"], **convergence["diagnostics"]}, indent=2))


if __name__ == "__main__":
    main()