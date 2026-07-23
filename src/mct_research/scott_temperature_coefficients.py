from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np

HANSEN_B0_EV_PER_K = 5.35e-4
HANSEN_B1_EV_PER_K_PER_X = -1.07e-3
COMPOSITION_HALF_WIDTH_X = 0.005
MEASUREMENT_CLASS = "fixed_absorption_optical_edge_alpha_500_cm_inverse"

SUBSET_COMPOSITIONS: Mapping[str, tuple[float, ...]] = {
    "full_9_specimens": (0.23, 0.25, 0.31, 0.35, 0.385, 0.405, 0.46, 0.53, 0.61),
    "exclude_source_flagged_x_0p25_0p385_0p53": (
        0.23,
        0.31,
        0.35,
        0.405,
        0.46,
        0.61,
    ),
    "exclude_x_0p61_outside_scott_equation_range": (
        0.23,
        0.25,
        0.31,
        0.35,
        0.385,
        0.405,
        0.46,
        0.53,
    ),
    "core_unflagged_within_range": (0.23, 0.31, 0.35, 0.405, 0.46),
    "exclude_endpoint_x_0p23_0p61": (
        0.25,
        0.31,
        0.35,
        0.385,
        0.405,
        0.46,
        0.53,
    ),
}


@dataclass(frozen=True)
class ScottPoint:
    marker_id: str
    specimen_label: str
    specimen_group: str
    composition_x: float
    quality_flag: str
    temperature_k: float
    edge_ev: float
    temperature_half_width_k: float
    energy_half_width_ev: float


def load_scott_points(path: str | Path) -> tuple[ScottPoint, ...]:
    source = Path(path)
    points: list[ScottPoint] = []
    with source.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["measurement_class"] != MEASUREMENT_CLASS:
                raise ValueError(
                    f"unexpected Scott measurement class: {row['measurement_class']}"
                )
            if row["signed_gap_eligible"].lower() != "false":
                raise ValueError("Scott fixed-alpha point cannot be signed-gap eligible")
            if (
                row["intrinsic_gap_eligible_without_observation_operator"].lower()
                != "false"
            ):
                raise ValueError(
                    "Scott fixed-alpha point cannot be intrinsic-gap eligible"
                )
            if row["pointwise_experimental_covariance"] != "not_reported":
                raise ValueError("Scott pointwise covariance must remain not_reported")
            points.append(
                ScottPoint(
                    marker_id=row["marker_id"],
                    specimen_label=row["specimen_label"],
                    specimen_group=row["shared_specimen_group"],
                    composition_x=float(row["nominal_density_composition_x"]),
                    quality_flag=row["source_quality_flag"],
                    temperature_k=float(row["temperature_k"]),
                    edge_ev=float(row["fixed_alpha_edge_ev"]),
                    temperature_half_width_k=float(
                        row["temperature_extraction_half_width_k"]
                    ),
                    energy_half_width_ev=float(
                        row["energy_extraction_half_width_ev"]
                    ),
                )
            )
    validate_points(points)
    return tuple(points)


def validate_points(points: Sequence[ScottPoint]) -> None:
    if len(points) != 70:
        raise ValueError(f"expected 70 Scott Figure 2 markers, found {len(points)}")
    groups = group_points(points)
    if len(groups) != 9:
        raise ValueError(f"expected 9 Scott specimens, found {len(groups)}")
    seen_ids = {point.marker_id for point in points}
    if len(seen_ids) != len(points):
        raise ValueError("duplicate Scott marker_id")
    for label, series in groups.items():
        if len(series) < 3:
            raise ValueError(f"{label} has fewer than three temperatures")
        compositions = {point.composition_x for point in series}
        if len(compositions) != 1:
            raise ValueError(f"{label} has inconsistent composition")
        temperatures = [point.temperature_k for point in series]
        if temperatures != sorted(temperatures):
            raise ValueError(f"{label} temperatures are not monotone")


def group_points(points: Sequence[ScottPoint]) -> dict[str, tuple[ScottPoint, ...]]:
    grouped: dict[str, list[ScottPoint]] = {}
    for point in points:
        grouped.setdefault(point.specimen_group, []).append(point)
    return {
        label: tuple(sorted(series, key=lambda point: point.temperature_k))
        for label, series in grouped.items()
    }


def select_compositions(
    points: Sequence[ScottPoint], compositions: Iterable[float]
) -> tuple[ScottPoint, ...]:
    allowed = tuple(float(value) for value in compositions)
    selected = tuple(
        point
        for point in points
        if any(abs(point.composition_x - value) <= 1e-12 for value in allowed)
    )
    if not selected:
        raise ValueError("empty Scott subset")
    return selected


def specimen_order(points: Sequence[ScottPoint]) -> tuple[str, ...]:
    grouped = group_points(points)
    return tuple(
        label
        for label, _ in sorted(
            grouped.items(), key=lambda item: item[1][0].composition_x
        )
    )


def _centered_rows(
    points: Sequence[ScottPoint],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple[str, ...]]:
    grouped = group_points(points)
    tc: list[float] = []
    ec: list[float] = []
    xs: list[float] = []
    labels: list[str] = []
    for label in specimen_order(points):
        series = grouped[label]
        mean_t = float(np.mean([point.temperature_k for point in series]))
        mean_e = float(np.mean([point.edge_ev for point in series]))
        for point in series:
            tc.append(point.temperature_k - mean_t)
            ec.append(point.edge_ev - mean_e)
            xs.append(point.composition_x)
            labels.append(label)
    return (
        np.asarray(tc, dtype=float),
        np.asarray(ec, dtype=float),
        np.asarray(xs, dtype=float),
        tuple(labels),
    )


def fit_shared_composition_slope(
    points: Sequence[ScottPoint],
) -> dict[str, float | int]:
    tc, ec, xs, _ = _centered_rows(points)
    design = np.column_stack((tc, tc * xs))
    rank = int(np.linalg.matrix_rank(design))
    if rank != 2:
        raise ValueError(f"centered Scott design rank is {rank}, expected 2")
    beta, _, _, singular_values = np.linalg.lstsq(design, ec, rcond=None)
    return {
        "b0_ev_per_k": float(beta[0]),
        "b1_ev_per_k_per_x": float(beta[1]),
        "rank": rank,
        "condition_number": float(singular_values[0] / singular_values[-1]),
    }


def fit_independent_slopes(points: Sequence[ScottPoint]) -> dict[str, float]:
    grouped = group_points(points)
    slopes: dict[str, float] = {}
    for label in specimen_order(points):
        series = grouped[label]
        temperature = np.asarray(
            [point.temperature_k for point in series], dtype=float
        )
        edge = np.asarray([point.edge_ev for point in series], dtype=float)
        tc = temperature - float(np.mean(temperature))
        ec = edge - float(np.mean(edge))
        denominator = float(np.dot(tc, tc))
        if denominator <= 0.0:
            raise ValueError(f"{label} has zero temperature leverage")
        slopes[label] = float(np.dot(tc, ec) / denominator)
    return slopes


def model_slopes(
    points: Sequence[ScottPoint], b0: float, b1: float
) -> dict[str, float]:
    grouped = group_points(points)
    return {
        label: float(b0 + b1 * series[0].composition_x)
        for label, series in grouped.items()
    }


def _prediction_rows(
    points: Sequence[ScottPoint], slopes: Mapping[str, float]
) -> list[dict[str, float | str]]:
    grouped = group_points(points)
    rows: list[dict[str, float | str]] = []
    for label in specimen_order(points):
        series = grouped[label]
        mean_t = float(np.mean([point.temperature_k for point in series]))
        mean_e = float(np.mean([point.edge_ev for point in series]))
        slope = float(slopes[label])
        for point in series:
            centered_temperature = point.temperature_k - mean_t
            prediction = mean_e + slope * centered_temperature
            rows.append(
                {
                    "marker_id": point.marker_id,
                    "specimen_group": label,
                    "composition_x": point.composition_x,
                    "centered_temperature_k": centered_temperature,
                    "observed_ev": point.edge_ev,
                    "predicted_ev": prediction,
                    "residual_ev": point.edge_ev - prediction,
                    "slope_ev_per_k": slope,
                    "temperature_half_width_k": point.temperature_half_width_k,
                    "energy_half_width_ev": point.energy_half_width_ev,
                }
            )
    return rows


def bounded_residual_metrics(
    points: Sequence[ScottPoint],
    slopes: Mapping[str, float],
    *,
    composition_slope_b1: float | None,
    composition_half_width_x: float = COMPOSITION_HALF_WIDTH_X,
) -> dict[str, object]:
    rows = _prediction_rows(points, slopes)
    specimen_rows: dict[str, list[dict[str, float | str]]] = {}
    for row in rows:
        bound = float(row["energy_half_width_ev"]) + abs(
            float(row["slope_ev_per_k"])
        ) * float(row["temperature_half_width_k"])
        if composition_slope_b1 is not None:
            bound += (
                abs(composition_slope_b1)
                * composition_half_width_x
                * abs(float(row["centered_temperature_k"]))
            )
        if bound <= 0.0:
            raise ValueError("nonpositive Scott residual envelope")
        residual = float(row["residual_ev"])
        row["first_order_box_half_width_ev"] = bound
        row["normalized_box_residual"] = abs(residual) / bound
        specimen_rows.setdefault(str(row["specimen_group"]), []).append(row)

    def summarize(
        local_rows: Sequence[dict[str, float | str]],
    ) -> dict[str, float | int]:
        local_residuals = np.asarray(
            [float(row["residual_ev"]) for row in local_rows], dtype=float
        )
        local_u = np.asarray(
            [float(row["normalized_box_residual"]) for row in local_rows],
            dtype=float,
        )
        return {
            "n_points": len(local_rows),
            "rmse_ev": float(np.sqrt(np.mean(local_residuals**2))),
            "maximum_absolute_residual_ev": float(
                np.max(np.abs(local_residuals))
            ),
            "maximum_normalized_box_residual": float(np.max(local_u)),
            "fraction_within_first_order_box": float(np.mean(local_u <= 1.0)),
            "squared_hinge_violation": float(
                np.sum(np.maximum(0.0, local_u - 1.0) ** 2)
            ),
        }

    summary = summarize(rows)
    summary["box_feasible"] = bool(
        float(summary["maximum_normalized_box_residual"]) <= 1.0
    )
    summary["by_specimen"] = {
        label: {
            **summarize(local_rows),
            "composition_x": float(local_rows[0]["composition_x"]),
            "slope_ev_per_k": float(local_rows[0]["slope_ev_per_k"]),
        }
        for label, local_rows in specimen_rows.items()
    }
    return summary


def analyze_subset(points: Sequence[ScottPoint]) -> dict[str, object]:
    shared = fit_shared_composition_slope(points)
    independent_slopes = fit_independent_slopes(points)
    s1_slopes = model_slopes(
        points,
        float(shared["b0_ev_per_k"]),
        float(shared["b1_ev_per_k_per_x"]),
    )
    hansen_slopes = model_slopes(
        points, HANSEN_B0_EV_PER_K, HANSEN_B1_EV_PER_K_PER_X
    )
    grouped = group_points(points)
    return {
        "n_points": len(points),
        "n_specimens": len(grouped),
        "specimens": [
            {
                "specimen_group": label,
                "composition_x": grouped[label][0].composition_x,
                "quality_flag": grouped[label][0].quality_flag,
                "n_points": len(grouped[label]),
            }
            for label in specimen_order(points)
        ],
        "S0_independent_specimen_slopes": {
            "slopes_ev_per_k": independent_slopes,
            "metrics": bounded_residual_metrics(
                points,
                independent_slopes,
                composition_slope_b1=None,
            ),
        },
        "S1_shared_linear_composition_slope": {
            **shared,
            "metrics": bounded_residual_metrics(
                points,
                s1_slopes,
                composition_slope_b1=float(shared["b1_ev_per_k_per_x"]),
            ),
        },
        "SH_hansen_fixed_slope": {
            "b0_ev_per_k": HANSEN_B0_EV_PER_K,
            "b1_ev_per_k_per_x": HANSEN_B1_EV_PER_K_PER_X,
            "metrics": bounded_residual_metrics(
                points,
                hansen_slopes,
                composition_slope_b1=HANSEN_B1_EV_PER_K_PER_X,
            ),
        },
        "hansen_slope_delta_pattern": slope_delta_pattern(
            points, independent_slopes, hansen_slopes
        ),
    }


def leave_one_specimen_out(
    points: Sequence[ScottPoint], *, model: str
) -> dict[str, object]:
    grouped = group_points(points)
    results: dict[str, object] = {}
    for held_out in specimen_order(points):
        training = tuple(
            point for point in points if point.specimen_group != held_out
        )
        test = grouped[held_out]
        if model == "S1":
            shared = fit_shared_composition_slope(training)
            b0 = float(shared["b0_ev_per_k"])
            b1 = float(shared["b1_ev_per_k_per_x"])
        elif model == "SH":
            b0 = HANSEN_B0_EV_PER_K
            b1 = HANSEN_B1_EV_PER_K_PER_X
        else:
            raise ValueError("leave-one-specimen-out model must be S1 or SH")
        slopes = model_slopes(test, b0, b1)
        metrics = bounded_residual_metrics(test, slopes, composition_slope_b1=b1)
        results[held_out] = {
            "composition_x": test[0].composition_x,
            "training_b0_ev_per_k": b0,
            "training_b1_ev_per_k_per_x": b1,
            "predicted_slope_ev_per_k": next(iter(slopes.values())),
            "metrics": metrics,
        }
    return {
        "model": model,
        "all_held_out_specimens_box_feasible": all(
            bool(result["metrics"]["box_feasible"])
            for result in results.values()
        ),
        "maximum_held_out_normalized_box_residual": max(
            float(result["metrics"]["maximum_normalized_box_residual"])
            for result in results.values()
        ),
        "by_held_out_specimen": results,
    }


def slope_delta_pattern(
    points: Sequence[ScottPoint],
    independent_slopes: Mapping[str, float],
    reference_slopes: Mapping[str, float],
) -> dict[str, object]:
    grouped = group_points(points)
    ordered = []
    for label in specimen_order(points):
        delta = independent_slopes[label] - reference_slopes[label]
        sign = 0 if abs(delta) <= 1e-15 else (1 if delta > 0 else -1)
        ordered.append(
            {
                "specimen_group": label,
                "composition_x": grouped[label][0].composition_x,
                "slope_delta_ev_per_k": delta,
                "sign": sign,
            }
        )
    longest_run = 0
    current_run = 0
    previous_sign = 0
    for item in ordered:
        sign = int(item["sign"])
        if sign == 0:
            current_run = 0
            previous_sign = 0
        elif sign == previous_sign:
            current_run += 1
        else:
            current_run = 1
            previous_sign = sign
        longest_run = max(longest_run, current_run)
    return {
        "ordered_slope_deltas": ordered,
        "longest_same_sign_run": longest_run,
        "monotone_residual_sign_pattern": bool(longest_run >= 4),
        "definition": (
            "four_or_more_consecutive_composition_ordered_specimens_with_the_"
            "same_sign_of_independent_minus_reference_slope"
        ),
    }


def linearized_box_sensitivity(points: Sequence[ScottPoint]) -> dict[str, object]:
    center = fit_shared_composition_slope(points)
    center_beta = np.asarray(
        [
            float(center["b0_ev_per_k"]),
            float(center["b1_ev_per_k_per_x"]),
        ],
        dtype=float,
    )
    categories = {
        "marker_energy": np.zeros(2, dtype=float),
        "marker_temperature": np.zeros(2, dtype=float),
        "specimen_composition": np.zeros(2, dtype=float),
    }
    mutable = list(points)

    for index, point in enumerate(points):
        plus = mutable.copy()
        minus = mutable.copy()
        plus[index] = replace(
            point, edge_ev=point.edge_ev + point.energy_half_width_ev
        )
        minus[index] = replace(
            point, edge_ev=point.edge_ev - point.energy_half_width_ev
        )
        categories["marker_energy"] += 0.5 * np.abs(
            _beta_vector(plus) - _beta_vector(minus)
        )

    for index, point in enumerate(points):
        plus = mutable.copy()
        minus = mutable.copy()
        plus[index] = replace(
            point,
            temperature_k=point.temperature_k + point.temperature_half_width_k,
        )
        minus[index] = replace(
            point,
            temperature_k=point.temperature_k - point.temperature_half_width_k,
        )
        categories["marker_temperature"] += 0.5 * np.abs(
            _beta_vector(plus) - _beta_vector(minus)
        )

    for label in specimen_order(points):
        plus = [
            replace(
                point,
                composition_x=point.composition_x + COMPOSITION_HALF_WIDTH_X,
            )
            if point.specimen_group == label
            else point
            for point in points
        ]
        minus = [
            replace(
                point,
                composition_x=point.composition_x - COMPOSITION_HALF_WIDTH_X,
            )
            if point.specimen_group == label
            else point
            for point in points
        ]
        categories["specimen_composition"] += 0.5 * np.abs(
            _beta_vector(plus) - _beta_vector(minus)
        )

    half_width = sum(categories.values(), np.zeros(2, dtype=float))
    lower = center_beta - half_width
    upper = center_beta + half_width
    hansen = np.asarray(
        [HANSEN_B0_EV_PER_K, HANSEN_B1_EV_PER_K_PER_X], dtype=float
    )
    return {
        "method": (
            "linearized_box_sensitivity_summed_absolute_symmetric_secant_"
            "contributions"
        ),
        "probabilistic_interpretation": False,
        "center": {
            "b0_ev_per_k": float(center_beta[0]),
            "b1_ev_per_k_per_x": float(center_beta[1]),
        },
        "half_width": {
            "b0_ev_per_k": float(half_width[0]),
            "b1_ev_per_k_per_x": float(half_width[1]),
        },
        "lower": {
            "b0_ev_per_k": float(lower[0]),
            "b1_ev_per_k_per_x": float(lower[1]),
        },
        "upper": {
            "b0_ev_per_k": float(upper[0]),
            "b1_ev_per_k_per_x": float(upper[1]),
        },
        "category_half_widths": {
            category: {
                "b0_ev_per_k": float(values[0]),
                "b1_ev_per_k_per_x": float(values[1]),
            }
            for category, values in categories.items()
        },
        "hansen_coefficients_inside_componentwise_envelope": bool(
            np.all(hansen >= lower) and np.all(hansen <= upper)
        ),
    }


def _beta_vector(points: Sequence[ScottPoint]) -> np.ndarray:
    result = fit_shared_composition_slope(points)
    return np.asarray(
        [
            float(result["b0_ev_per_k"]),
            float(result["b1_ev_per_k_per_x"]),
        ],
        dtype=float,
    )


def _outside_componentwise_envelope(
    sensitivity: Mapping[str, object],
) -> bool:
    lower = sensitivity["lower"]
    upper = sensitivity["upper"]
    return not (
        float(lower["b0_ev_per_k"])
        <= HANSEN_B0_EV_PER_K
        <= float(upper["b0_ev_per_k"])
        and float(lower["b1_ev_per_k_per_x"])
        <= HANSEN_B1_EV_PER_K_PER_X
        <= float(upper["b1_ev_per_k_per_x"])
    )


def controlling_decision(
    core_analysis: Mapping[str, object],
    core_lopo_s1: Mapping[str, object],
    core_lopo_sh: Mapping[str, object],
    core_sensitivity: Mapping[str, object],
) -> dict[str, object]:
    s1_box = bool(
        core_analysis["S1_shared_linear_composition_slope"]["metrics"][
            "box_feasible"
        ]
    )
    sh_box = bool(core_analysis["SH_hansen_fixed_slope"]["metrics"]["box_feasible"])
    s1_lopo_box = bool(core_lopo_s1["all_held_out_specimens_box_feasible"])
    sh_lopo_box = bool(core_lopo_sh["all_held_out_specimens_box_feasible"])
    sign_pattern = bool(
        core_analysis["hansen_slope_delta_pattern"][
            "monotone_residual_sign_pattern"
        ]
    )
    hansen_outside = _outside_componentwise_envelope(core_sensitivity)

    if sh_box and sh_lopo_box and not sign_pattern:
        decision = "hansen_compatible"
    elif s1_box and s1_lopo_box and not sh_box and hansen_outside:
        decision = "observable_specific_correction_required"
    else:
        decision = "non_identifiable_at_figure_precision"
    return {
        "decision": decision,
        "controlling_subset": "core_unflagged_within_range",
        "gates": {
            "S1_core_box_feasible": s1_box,
            "S1_core_leave_one_specimen_out_box_feasible": s1_lopo_box,
            "SH_core_box_feasible": sh_box,
            "SH_core_leave_one_specimen_out_box_feasible": sh_lopo_box,
            "hansen_monotone_residual_sign_pattern": sign_pattern,
            "hansen_coefficients_outside_S1_linearized_box_envelope": (
                hansen_outside
            ),
        },
        "claim_boundary": (
            "temperature_trend_of_fixed_alpha_optical_edge_only; "
            "no_intrinsic_gap_or_absolute_hansen_polynomial_validation"
        ),
    }


def build_reference(
    points: Sequence[ScottPoint], *, source_csv_sha256: str
) -> dict[str, object]:
    analyses = {
        name: analyze_subset(select_compositions(points, compositions))
        for name, compositions in SUBSET_COMPOSITIONS.items()
    }
    full_points = select_compositions(
        points, SUBSET_COMPOSITIONS["full_9_specimens"]
    )
    core_points = select_compositions(
        points, SUBSET_COMPOSITIONS["core_unflagged_within_range"]
    )
    lopo = {
        "full_9_specimens": {
            "S1": leave_one_specimen_out(full_points, model="S1"),
            "SH": leave_one_specimen_out(full_points, model="SH"),
        },
        "core_unflagged_within_range": {
            "S1": leave_one_specimen_out(core_points, model="S1"),
            "SH": leave_one_specimen_out(core_points, model="SH"),
        },
    }
    sensitivity = {
        "full_9_specimens": linearized_box_sensitivity(full_points),
        "core_unflagged_within_range": linearized_box_sensitivity(core_points),
    }
    decision = controlling_decision(
        analyses["core_unflagged_within_range"],
        lopo["core_unflagged_within_range"]["S1"],
        lopo["core_unflagged_within_range"]["SH"],
        sensitivity["core_unflagged_within_range"],
    )
    return {
        "schema_version": "1.0",
        "program": "R01",
        "issue": 312,
        "source": {
            "path": "data/experimental/scott1969_figure2_digitized.csv",
            "sha256": source_csv_sha256,
            "row_count": len(points),
            "specimen_count": len(group_points(points)),
        },
        "observation_boundary": {
            "measurement_class": MEASUREMENT_CLASS,
            "signed_gap_eligible": False,
            "intrinsic_gap_eligible_without_observation_operator": False,
            "pointwise_experimental_covariance": "not_reported",
            "coordinate_half_widths_are_gaussian_sigma": False,
        },
        "constants": {
            "hansen_b0_ev_per_k": HANSEN_B0_EV_PER_K,
            "hansen_b1_ev_per_k_per_x": HANSEN_B1_EV_PER_K_PER_X,
            "composition_half_width_x": COMPOSITION_HALF_WIDTH_X,
        },
        "subset_analyses": analyses,
        "leave_one_specimen_out": lopo,
        "linearized_box_sensitivity": sensitivity,
        "decision": decision,
    }


def source_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def quantize_for_json(value: object, digits: int = 12) -> object:
    if isinstance(value, dict):
        return {
            str(key): quantize_for_json(item, digits)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [quantize_for_json(item, digits) for item in value]
    if isinstance(value, (float, np.floating)):
        return round(float(value), digits)
    if isinstance(value, (bool, str, int)) or value is None:
        return value
    raise TypeError(f"unsupported reference value: {type(value)!r}")
