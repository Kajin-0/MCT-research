#!/usr/bin/env python3
"""Audit whether Chang 2006 Figure 2 can validate the committed operator."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.chang_2006_absorption import (
    CHANG_2006_RELATIVE_ENERGY_RANGE_EV,
    chang_2006_absorption_shape,
    fit_chang_2006_nonparabolic_urbach_edge,
)

SOURCE_ASSET_SHA256 = (
    "37a08e3fc37fc3b795b1a9d7ac3b3b662f9f96c2cad4cddbf79bc0fe3b57b41d"
)
EXPECTED_FALSE_SOURCE_FIELDS = (
    "temperature_metadata_consistent",
    "native_numeric_data_recovered",
    "calibration_metadata_recovered",
    "same_specimen_urbach_width_recovered",
    "same_specimen_hyperbola_b_recovered",
    "figure_fit_parameters_tabulated",
)
EXPECTED_FALSE_DECISION_FIELDS = (
    "quantitative_operator_validation_authorized",
    "figure_digitization_for_gap_inference_authorized",
    "transfer_x023_b_as_exact_x021_input_authorized",
    "assign_real_specimen_uncertainty_from_synthetic_screen",
    "material_gap_fit_authorized",
)
PARAMETER_LABELS = ("edge_eV", "log_urbach_width", "log_hyperbola_b", "log_amplitude")


def _require_close(actual: Any, expected: float, field: str) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=1.0e-12
    ):
        raise ValueError(f"{field} changed: {actual!r} != {expected!r}")


def _energy_grid(segments: list[dict[str, Any]]) -> np.ndarray:
    arrays: list[np.ndarray] = []
    for index, segment in enumerate(segments):
        start = float(segment["start_eV"])
        stop = float(segment["stop_eV"])
        count = int(segment["point_count"])
        if not start < stop or count < 2:
            raise ValueError(f"invalid synthetic energy segment {index}")
        arrays.append(np.linspace(start, stop, count))
    energy = np.unique(np.concatenate(arrays))
    if energy.size != sum(int(segment["point_count"]) for segment in segments):
        raise ValueError("synthetic energy segments overlap")
    return energy


def _log_prediction(
    energy: np.ndarray,
    parameters: np.ndarray,
) -> np.ndarray:
    edge = float(parameters[0])
    width = math.exp(float(parameters[1]))
    b_value = math.exp(float(parameters[2]))
    amplitude = math.exp(float(parameters[3]))
    return np.log(
        amplitude
        * chang_2006_absorption_shape(
            energy,
            edge_ev=edge,
            urbach_width_ev=width,
            hyperbola_b_ev=b_value,
        )
    )


def _local_weighted_identifiability(
    energy: np.ndarray,
    *,
    edge_eV: float,
    urbach_width_eV: float,
    hyperbola_b_eV: float,
    amplitude_cm1: float,
    sigma_energy_eV: float,
    sigma_log_absorption: float,
    parameter_steps: dict[str, float],
) -> dict[str, Any]:
    parameters = np.asarray(
        [
            edge_eV,
            math.log(urbach_width_eV),
            math.log(hyperbola_b_eV),
            math.log(amplitude_cm1),
        ],
        dtype=float,
    )
    steps = np.asarray(
        [
            parameter_steps["edge_eV"],
            parameter_steps["log_urbach_width"],
            parameter_steps["log_hyperbola_b"],
            parameter_steps["log_amplitude"],
        ],
        dtype=float,
    )
    columns: list[np.ndarray] = []
    for index, step in enumerate(steps):
        delta = np.zeros(4)
        delta[index] = step
        columns.append(
            (_log_prediction(energy, parameters + delta) - _log_prediction(energy, parameters - delta))
            / (2.0 * step)
        )
    jacobian = np.column_stack(columns)

    energy_step = float(parameter_steps["energy_eV"])
    energy_derivative = (
        _log_prediction(energy + energy_step, parameters)
        - _log_prediction(energy - energy_step, parameters)
    ) / (2.0 * energy_step)
    point_sigma = np.sqrt(
        sigma_log_absorption**2 + (energy_derivative * sigma_energy_eV) ** 2
    )
    weighted = jacobian / point_sigma[:, None]
    information = weighted.T @ weighted
    covariance = np.linalg.inv(information)
    standard_errors = np.sqrt(np.diag(covariance))
    correlation = covariance / np.sqrt(np.outer(np.diag(covariance), np.diag(covariance)))

    return {
        "parameter_order": list(PARAMETER_LABELS),
        "weighted_jacobian_condition_number": float(np.linalg.cond(weighted)),
        "linearized_standard_errors": {
            "edge_meV": float(1000.0 * standard_errors[0]),
            "relative_urbach_width": float(standard_errors[1]),
            "relative_hyperbola_b": float(standard_errors[2]),
            "relative_amplitude": float(standard_errors[3]),
        },
        "correlations": {
            "edge_log_urbach_width": float(correlation[0, 1]),
            "edge_log_hyperbola_b": float(correlation[0, 2]),
            "edge_log_amplitude": float(correlation[0, 3]),
            "log_urbach_width_log_hyperbola_b": float(correlation[1, 2]),
            "log_urbach_width_log_amplitude": float(correlation[1, 3]),
            "log_hyperbola_b_log_amplitude": float(correlation[2, 3]),
        },
        "minimum_effective_log_sigma": float(np.min(point_sigma)),
        "maximum_effective_log_sigma": float(np.max(point_sigma)),
    }


def _profile_fixed_parameter(
    energy: np.ndarray,
    absorption: np.ndarray,
    *,
    truth_edge_eV: float,
    truth_width_eV: float,
    truth_b_eV: float,
    parameter: str,
    scales: list[float],
    edge_bounds_eV: tuple[float, float],
    absorption_window_cm1: tuple[float, float],
    grid_points: int,
) -> list[dict[str, float]]:
    records: list[dict[str, float]] = []
    for scale in scales:
        if parameter == "urbach_width":
            width = truth_width_eV * scale
            b_value = truth_b_eV
        elif parameter == "hyperbola_b":
            width = truth_width_eV
            b_value = truth_b_eV * scale
        else:
            raise ValueError(f"unsupported profile parameter: {parameter}")
        fit = fit_chang_2006_nonparabolic_urbach_edge(
            energy,
            absorption,
            edge_bounds_ev=edge_bounds_eV,
            fit_absorption_window_cm1=absorption_window_cm1,
            urbach_width_ev=width,
            hyperbola_b_ev=b_value,
            grid_points=grid_points,
        )
        records.append(
            {
                "scale": float(scale),
                "fixed_value_eV": float(width if parameter == "urbach_width" else b_value),
                "fitted_edge_eV": float(fit["edge_ev"]),
                "edge_bias_meV": float(1000.0 * (float(fit["edge_ev"]) - truth_edge_eV)),
                "fitted_amplitude_cm1": float(fit["amplitude_cm1"]),
                "root_mean_square_log_residual": float(
                    math.sqrt(float(fit["log_mean_square_error"]))
                ),
            }
        )
    return records


def audit(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("unsupported Chang 2006 Figure 2 readiness schema")

    source = payload["source"]
    if source["doi"] != "10.1063/1.2245220":
        raise ValueError("Chang 2006 DOI changed")
    if source["input_asset_sha256"] != SOURCE_ASSET_SHA256:
        raise ValueError("Chang 2006 source asset hash changed")
    if source["copyrighted_source_committed"] is not False:
        raise ValueError("copyrighted source content may not be committed")
    _require_close(source["figure_composition_x"], 0.21, "Figure 2 composition")
    _require_close(source["caption_temperature_K"], 80.0, "Figure 2 caption temperature")
    _require_close(source["body_temperature_K"], 77.0, "Figure 2 body temperature")
    for field in EXPECTED_FALSE_SOURCE_FIELDS:
        if source.get(field) is not False:
            raise ValueError(f"source readiness field {field} changed")

    external_b = source["reported_external_b"]
    _require_close(external_b["value_eV"], 0.103, "external b value")
    _require_close(external_b["sigma_eV"], 0.002, "external b sigma")
    _require_close(external_b["composition_x"], 0.23, "external b composition")
    _require_close(external_b["temperature_K"], 77.0, "external b temperature")
    if external_b["same_figure_specimen"] is not False:
        raise ValueError("x=0.23 b cannot be relabeled as the Figure 2 specimen")
    if external_b["admissible_as_exact_figure2_input"] is not False:
        raise ValueError("external b cannot be promoted to an exact Figure 2 input")

    decision = payload["decision"]
    for field in EXPECTED_FALSE_DECISION_FIELDS:
        if decision.get(field) is not False:
            raise ValueError(f"decision field {field} changed")
    if decision.get("screen_only_source_recovery_priority") != "high":
        raise ValueError("Figure 2 source-recovery priority changed")
    if len(decision.get("reopening_requirements", [])) != 6:
        raise ValueError("Figure 2 reopening requirement inventory is incomplete")

    screen = payload["synthetic_screen"]
    truth = screen["truth"]
    edge = float(truth["edge_eV"])
    width = float(truth["urbach_width_eV"])
    b_value = float(truth["hyperbola_b_eV"])
    amplitude = float(truth["amplitude_cm1"])
    energy = _energy_grid(screen["energy_segments"])
    declared_upper_margin = float(
    screen["source_domain_upper_margin_at_truth_eV"]
)
    actual_upper_margin = float(
        CHANG_2006_RELATIVE_ENERGY_RANGE_EV[1] - (float(np.max(energy)) - edge)
    )
    if declared_upper_margin <= 0.0 or not math.isclose(
        actual_upper_margin,
        declared_upper_margin,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        raise ValueError("synthetic source-domain upper margin changed")
    absorption = amplitude * chang_2006_absorption_shape(
        energy,
        edge_ev=edge,
        urbach_width_ev=width,
        hyperbola_b_ev=b_value,
    )

    coordinate = screen["hypothetical_coordinate_uncertainty"]
    identifiability = _local_weighted_identifiability(
        energy,
        edge_eV=edge,
        urbach_width_eV=width,
        hyperbola_b_eV=b_value,
        amplitude_cm1=amplitude,
        sigma_energy_eV=float(coordinate["sigma_energy_eV"]),
        sigma_log_absorption=float(coordinate["sigma_log_absorption"]),
        parameter_steps=screen["finite_difference_steps"],
    )

    edge_bounds = tuple(float(value) for value in screen["profile_edge_bounds_eV"])
    absorption_window = tuple(
        float(value) for value in screen["profile_absorption_window_cm1"]
    )
    width_profile = _profile_fixed_parameter(
        energy,
        absorption,
        truth_edge_eV=edge,
        truth_width_eV=width,
        truth_b_eV=b_value,
        parameter="urbach_width",
        scales=[float(value) for value in screen["urbach_width_scale_profiles"]],
        edge_bounds_eV=edge_bounds,
        absorption_window_cm1=absorption_window,
        grid_points=int(screen["profile_grid_points"]),
    )
    b_profile = _profile_fixed_parameter(
        energy,
        absorption,
        truth_edge_eV=edge,
        truth_width_eV=width,
        truth_b_eV=b_value,
        parameter="hyperbola_b",
        scales=[float(value) for value in screen["hyperbola_b_scale_profiles"]],
        edge_bounds_eV=edge_bounds,
        absorption_window_cm1=absorption_window,
        grid_points=int(screen["profile_grid_points"]),
    )

    nontruth_records = [
        record
        for record in width_profile + b_profile
        if not math.isclose(record["scale"], 1.0, rel_tol=0.0, abs_tol=1e-12)
    ]
    visually_small_residual_with_mev_bias = any(
        record["root_mean_square_log_residual"] <= 0.03
        and abs(record["edge_bias_meV"]) >= 0.75
        for record in nontruth_records
    )

    return {
        "schema_version": payload["schema_version"],
        "analysis": payload["analysis"],
        "source_readiness": {
            "figure_composition_x": source["figure_composition_x"],
            "caption_temperature_K": source["caption_temperature_K"],
            "body_temperature_K": source["body_temperature_K"],
            "temperature_metadata_consistent": False,
            "native_numeric_data_recovered": False,
            "same_specimen_urbach_width_recovered": False,
            "same_specimen_hyperbola_b_recovered": False,
        },
        "synthetic_point_count": int(energy.size),
        "synthetic_source_domain_upper_margin_eV": actual_upper_margin,
        "synthetic_tail_point_count_at_truth": int(
            np.count_nonzero(energy < edge + 0.5 * width)
        ),
        "synthetic_absorption_range_cm1": [
            float(np.min(absorption)),
            float(np.max(absorption)),
        ],
        "local_weighted_identifiability": identifiability,
        "fixed_urbach_width_profiles": width_profile,
        "fixed_hyperbola_b_profiles": b_profile,
        "visually_small_residual_can_mask_mev_scale_edge_bias": (
            visually_small_residual_with_mev_bias
        ),
        "decision": decision,
        "claim_boundary": (
            "The synthetic screen quantifies local parameter confounding under declared "
            "hypothetical coordinate uncertainties. It is not a measurement uncertainty "
            "for Figure 2 and does not authorize figure digitization as a material-gap point."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.input_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
