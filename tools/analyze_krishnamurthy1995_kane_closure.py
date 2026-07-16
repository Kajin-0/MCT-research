#!/usr/bin/env python3
"""Reproduce Krishnamurthy 1995 Table II hyperbolic closure.

The primary paper writes the conduction-band energy relative to its minimum as

    epsilon(k, T) = sqrt(gamma(T) * k**2 + c(T)**2) - c(T).

The printed reciprocal-space normalization of k is retained rather than inferred.
For a fixed k convention, the small-k expansion gives

    epsilon = gamma * k**2 / (2 c) + O(k**4),

so the tabulated effective-mass ratio must satisfy

    m*(T) / m*(T0) = [c(T) / gamma(T)] / [c(T0) / gamma(T0)].

An absolute equivalent hyperbolic velocity can be obtained without knowing the
printed k normalization by rewriting the local dispersion in physical wavevector
form and using c = m* v_h**2:

    v_h(T) = sqrt(c(T) / m*(T)).

This is a reproducibility test against historical calculated data. It is not
experimental validation and does not infer an absolute multiband Kane matrix
element P.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

ELECTRON_VOLT_J = 1.602176634e-19
FREE_ELECTRON_MASS_KG = 9.1093837015e-31


def _load_table(path: str | Path) -> dict[str, np.ndarray]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if not rows:
        raise ValueError("Table II CSV is empty")

    numeric_columns = (
        "temperature_k",
        "gap_mev",
        "gamma_reported",
        "c_ev",
        "effective_mass_ratio_to_m0",
        "base_effective_mass_over_free_electron",
    )
    data = {
        name: np.asarray([float(row[name]) for row in rows], dtype=float)
        for name in numeric_columns
    }
    count = data["temperature_k"].size
    if count != 21:
        raise ValueError(f"expected 21 Table II rows, found {count}")
    if not np.all(np.isfinite(np.column_stack(tuple(data.values())))):
        raise ValueError("Table II contains non-finite numerical values")
    if not np.all(np.diff(data["temperature_k"]) > 0.0):
        raise ValueError("temperature must be strictly increasing")
    for name in (
        "gap_mev",
        "gamma_reported",
        "c_ev",
        "effective_mass_ratio_to_m0",
        "base_effective_mass_over_free_electron",
    ):
        if np.any(data[name] <= 0.0):
            raise ValueError(f"{name} must be positive")
    if not np.allclose(
        data["base_effective_mass_over_free_electron"],
        data["base_effective_mass_over_free_electron"][0],
        rtol=0.0,
        atol=0.0,
    ):
        raise ValueError("base effective mass must be constant")
    return data


def _error_metrics(
    prediction: np.ndarray,
    reference: np.ndarray,
    temperature_k: np.ndarray,
    mask: np.ndarray,
) -> dict[str, float]:
    fractional = prediction[mask] / reference[mask] - 1.0
    maximum_index = int(np.argmax(np.abs(fractional)))
    return {
        "mean_fractional_error": float(np.mean(fractional)),
        "mean_absolute_fractional_error": float(np.mean(np.abs(fractional))),
        "rms_fractional_error": float(np.sqrt(np.mean(fractional**2))),
        "maximum_absolute_fractional_error": float(np.max(np.abs(fractional))),
        "maximum_error_temperature_k": float(temperature_k[mask][maximum_index]),
    }


def _drift_metrics(
    relative_value: np.ndarray,
    temperature_k: np.ndarray,
    mask: np.ndarray,
) -> dict[str, float]:
    selected = relative_value[mask]
    drift = selected - 1.0
    best_constant = float(np.mean(selected))
    residual_to_constant = selected / best_constant - 1.0
    maximum_index = int(np.argmax(np.abs(drift)))
    minimum_index = int(np.argmin(drift))
    positive_index = int(np.argmax(drift))
    return {
        "mean_signed_drift": float(np.mean(drift)),
        "rms_drift": float(np.sqrt(np.mean(drift**2))),
        "maximum_absolute_drift": float(np.max(np.abs(drift))),
        "maximum_drift_temperature_k": float(temperature_k[mask][maximum_index]),
        "minimum_signed_drift": float(drift[minimum_index]),
        "minimum_temperature_k": float(temperature_k[mask][minimum_index]),
        "maximum_signed_drift": float(drift[positive_index]),
        "maximum_temperature_k": float(temperature_k[mask][positive_index]),
        "best_constant_relative_to_reference": best_constant,
        "rms_about_best_constant": float(np.sqrt(np.mean(residual_to_constant**2))),
        "maximum_about_best_constant": float(np.max(np.abs(residual_to_constant))),
    }


def analyze_table(path: str | Path) -> tuple[list[dict[str, float]], dict[str, Any]]:
    data = _load_table(path)
    temperature = data["temperature_k"]
    gap_ev = data["gap_mev"] * 1.0e-3
    gamma = data["gamma_reported"]
    c_ev = data["c_ev"]
    mass_ratio = data["effective_mass_ratio_to_m0"]
    base_mass_ratio = data["base_effective_mass_over_free_electron"][0]
    mass_kg = base_mass_ratio * FREE_ELECTRON_MASS_KG * mass_ratio

    mass_ratio_reproduced = (c_ev / gamma) / (c_ev[0] / gamma[0])
    mass_closure_fractional_error = mass_ratio_reproduced / mass_ratio - 1.0

    hyperbolic_velocity_m_per_s = np.sqrt(c_ev * ELECTRON_VOLT_J / mass_kg)
    hyperbolic_velocity_relative = (
        hyperbolic_velocity_m_per_s / hyperbolic_velocity_m_per_s[0]
    )

    gamma_velocity_relative = np.sqrt(gamma / gamma[0])
    velocity_convention_fractional_difference = (
        hyperbolic_velocity_relative / gamma_velocity_relative - 1.0
    )

    reduced_velocity_m_per_s = np.sqrt(
        gap_ev * ELECTRON_VOLT_J / (2.0 * mass_kg)
    )
    reduced_velocity_relative = reduced_velocity_m_per_s / reduced_velocity_m_per_s[0]

    gap_only_fixed_velocity_mass_ratio = gap_ev / gap_ev[0]
    c_only_fixed_velocity_mass_ratio = c_ev / c_ev[0]
    gap_plus_hyperbolic_velocity_mass_ratio = (
        gap_only_fixed_velocity_mass_ratio / hyperbolic_velocity_relative**2
    )
    complete_hyperbolic_mass_ratio = mass_ratio_reproduced
    c_over_half_gap = c_ev / (0.5 * gap_ev)

    mask_100 = temperature <= 100.0
    mask_300 = temperature <= 300.0
    mask_600 = temperature <= 600.0

    minimum_gap_index = int(np.argmin(gap_ev))
    turnover_depth_mev = float(
        data["gap_mev"][0] - data["gap_mev"][minimum_gap_index]
    )
    velocity_at_turnover = float(
        hyperbolic_velocity_relative[minimum_gap_index] - 1.0
    )
    reduced_velocity_at_turnover = float(
        reduced_velocity_relative[minimum_gap_index] - 1.0
    )

    robust_velocity = _drift_metrics(
        hyperbolic_velocity_relative, temperature, mask_300
    )
    full_velocity = _drift_metrics(
        hyperbolic_velocity_relative, temperature, mask_600
    )
    reduced_diagnostic = _drift_metrics(
        reduced_velocity_relative, temperature, mask_300
    )

    threshold = 0.05
    large_renormalization_supported = (
        robust_velocity["maximum_absolute_drift"] >= threshold
    )
    decision = (
        "large_P_T_renormalization_not_supported"
        if not large_renormalization_supported
        else "non_gap_Kane_renormalization_strengthened"
    )

    rows: list[dict[str, float]] = []
    for index in range(temperature.size):
        rows.append(
            {
                "temperature_k": float(temperature[index]),
                "gap_mev": float(data["gap_mev"][index]),
                "gamma_reported": float(gamma[index]),
                "c_ev": float(c_ev[index]),
                "effective_mass_ratio_reported": float(mass_ratio[index]),
                "effective_mass_ratio_reproduced": float(
                    mass_ratio_reproduced[index]
                ),
                "mass_closure_fractional_error": float(
                    mass_closure_fractional_error[index]
                ),
                "hyperbolic_velocity_m_per_s": float(
                    hyperbolic_velocity_m_per_s[index]
                ),
                "hyperbolic_velocity_relative_to_1k": float(
                    hyperbolic_velocity_relative[index]
                ),
                "gamma_velocity_relative_to_1k": float(
                    gamma_velocity_relative[index]
                ),
                "velocity_convention_fractional_difference": float(
                    velocity_convention_fractional_difference[index]
                ),
                "reduced_velocity_m_per_s": float(reduced_velocity_m_per_s[index]),
                "reduced_velocity_relative_to_1k": float(
                    reduced_velocity_relative[index]
                ),
                "gap_only_fixed_velocity_mass_ratio": float(
                    gap_only_fixed_velocity_mass_ratio[index]
                ),
                "c_only_fixed_velocity_mass_ratio": float(
                    c_only_fixed_velocity_mass_ratio[index]
                ),
                "gap_plus_hyperbolic_velocity_mass_ratio": float(
                    gap_plus_hyperbolic_velocity_mass_ratio[index]
                ),
                "complete_hyperbolic_mass_ratio": float(
                    complete_hyperbolic_mass_ratio[index]
                ),
                "c_over_half_gap": float(c_over_half_gap[index]),
            }
        )

    summary: dict[str, Any] = {
        "analysis": "Krishnamurthy 1995 Hg0.78Cd0.22Te Table II Kane closure",
        "source_kind": "historical_calculated_HPTB_plus_valence_force_field_data",
        "experimental_validation": False,
        "paper_dispersion": {
            "equation": "epsilon(k,T)=sqrt(gamma(T)*k^2+c(T)^2)-c(T)",
            "energy_origin": "conduction_band_minimum",
            "small_k_expansion": "epsilon=gamma*k^2/(2*c)+O(k^4)",
            "mass_ratio_identity": (
                "m*(T)/m*(T0)=[c(T)/gamma(T)]/[c(T0)/gamma(T0)]"
            ),
            "absolute_gamma_normalization": (
                "not inferred; depends on the paper reciprocal-space k convention"
            ),
        },
        "dimensional_checks": {
            "c": "energy",
            "gamma_times_k_squared": "energy_squared",
            "equivalent_velocity": "sqrt(c_energy_J/mass_kg), in m/s",
            "reduced_velocity": "sqrt(Eg_energy_J/(2*mass_kg)), in m/s",
            "base_effective_mass_over_free_electron": float(base_mass_ratio),
        },
        "table_reproduction": {
            "row_count": int(temperature.size),
            "maximum_absolute_mass_ratio_fractional_error": float(
                np.max(np.abs(mass_closure_fractional_error))
            ),
            "rms_mass_ratio_fractional_error": float(
                np.sqrt(np.mean(mass_closure_fractional_error**2))
            ),
            "maximum_relative_velocity_convention_difference": float(
                np.max(np.abs(velocity_convention_fractional_difference))
            ),
            "interpretation": "residuals are consistent with rounding of the printed columns",
        },
        "equivalent_hyperbolic_velocity": {
            "velocity_1k_m_per_s": float(hyperbolic_velocity_m_per_s[0]),
            "velocity_300k_m_per_s": float(
                hyperbolic_velocity_m_per_s[temperature == 300.0][0]
            ),
            "velocity_600k_m_per_s": float(hyperbolic_velocity_m_per_s[-1]),
            "drift_1_to_100k": _drift_metrics(
                hyperbolic_velocity_relative, temperature, mask_100
            ),
            "drift_1_to_300k": robust_velocity,
            "drift_1_to_600k": full_velocity,
        },
        "reduced_gap_mass_diagnostic": {
            "definition": "v_eff=sqrt(Eg/(2*m*))",
            "assumption": "symmetric two-band closure c=Eg/2",
            "drift_1_to_300k": reduced_diagnostic,
            "c_over_half_gap_1k": float(c_over_half_gap[0]),
            "c_over_half_gap_300k": float(c_over_half_gap[temperature == 300.0][0]),
            "interpretation": (
                "the greater-than-5-percent drift is convention-sensitive because "
                "the reported c is not Eg/2"
            ),
        },
        "mass_model_comparison_1_to_300k": {
            "gap_only_fixed_velocity": _error_metrics(
                gap_only_fixed_velocity_mass_ratio,
                mass_ratio,
                temperature,
                mask_300,
            ),
            "c_only_fixed_velocity": _error_metrics(
                c_only_fixed_velocity_mass_ratio,
                mass_ratio,
                temperature,
                mask_300,
            ),
            "gap_plus_reported_hyperbolic_velocity_forced_into_Eg_over_2": (
                _error_metrics(
                    gap_plus_hyperbolic_velocity_mass_ratio,
                    mass_ratio,
                    temperature,
                    mask_300,
                )
            ),
            "complete_reported_hyperbola": _error_metrics(
                complete_hyperbolic_mass_ratio,
                mass_ratio,
                temperature,
                mask_300,
            ),
            "gap_plus_reduced_velocity": (
                "reproduces the reported mass algebraically by construction and "
                "is not an independent predictive test"
            ),
        },
        "low_temperature_turnover": {
            "minimum_temperature_k": float(temperature[minimum_gap_index]),
            "depth_relative_to_1k_mev": turnover_depth_mev,
            "hyperbolic_velocity_drift_at_minimum": velocity_at_turnover,
            "reduced_velocity_drift_at_minimum": reduced_velocity_at_turnover,
            "resolved_closure_effect": False,
            "reason": (
                "1.04 meV is below the paper-level approximately 10-15 meV "
                "comparison/model accuracy and has no supplied pointwise uncertainty"
            ),
        },
        "decision_rule": {
            "robust_temperature_window_k": [1.0, 300.0],
            "velocity_drift_threshold": threshold,
            "maximum_robust_hyperbolic_velocity_drift": robust_velocity[
                "maximum_absolute_drift"
            ],
            "decision": decision,
            "large_P_T_renormalization_supported": large_renormalization_supported,
            "high_temperature_warning": (
                "the 5 percent threshold is crossed only at 550-600 K, where the "
                "paper itself calls for higher-order or self-consistently "
                "renormalized finite-temperature bands"
            ),
        },
        "prior_art_boundary": {
            "constant_Kane_velocity_null": (
                "supported to within 2.8 percent over 1-300 K by the paper-convention "
                "equivalent velocity"
            ),
            "not_established": (
                "absolute multiband Kane P(T), separate P8/P7, F(T), gamma_i(T), "
                "or complete 8-band matrix closure"
            ),
        },
        "uncertainty_limitations": [
            "Table II has rounded values and no datum-level uncertainties.",
            "The source is a historical calculation, not an experimental dataset.",
            "The reciprocal-space normalization needed to convert printed gamma directly into an absolute velocity is not inferred.",
            "The equivalent absolute velocity uses the reported m*(0)/m0=0.008.",
            "The reduced Eg/(2m*) diagnostic assumes c=Eg/2, which the table violates.",
            "The paper reports an overall approximately 10-15 meV comparison/model floor.",
        ],
        "falsification_criteria": [
            "A primary-source recheck showing a different hyperbolic equation or column ordering invalidates this analysis.",
            "Unrounded source values that fail the c/gamma mass closure beyond reported numerical accuracy invalidate the reconstruction.",
            "A modern calculation or experiment showing greater than 5 percent velocity drift over a controlled 1-300 K range strengthens non-gap Kane renormalization.",
            "A resolved low-temperature turnover larger than the complete uncertainty floor would require signed competing thermal channels.",
        ],
    }
    return rows, summary


def _write_csv(path: str | Path, rows: list[dict[str, float]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/theory/krishnamurthy1995_hg078cd022_table2.csv",
    )
    parser.add_argument("--output-csv")
    parser.add_argument("--summary-json")
    args = parser.parse_args()

    rows, summary = analyze_table(args.input_csv)
    if args.output_csv:
        _write_csv(args.output_csv, rows)
    if args.summary_json:
        output = Path(args.summary_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
