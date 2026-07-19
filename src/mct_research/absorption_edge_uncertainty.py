"""Explicit uncertainty envelopes for absorption-derived HgCdTe edges.

The module evaluates declared edge models and fixed absorption thresholds. It does
not select a universal correction or identify a latent material gap.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

import numpy as np
from numpy.typing import NDArray

CONTRACT_VERSION = "1.0"
CHU_1994_COMPOSITION_RANGE = (0.170, 0.443)
CHU_1994_TEMPERATURE_RANGE_K = (77.0, 300.0)
CHU_1994_SOURCE_DOI = "10.1063/1.356464"


def _canonical_digest(value: Mapping[str, Any]) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(text.encode("utf-8")).hexdigest()


def _required(mapping: Mapping[str, Any], key: str, *, context: str) -> Any:
    if key not in mapping:
        raise ValueError(f"{context} is missing required field {key!r}")
    return mapping[key]


def _finite_vector(
    value: Any,
    *,
    name: str,
    positive: bool = False,
) -> NDArray[np.float64]:
    array = np.asarray(value, dtype=float)
    if array.ndim != 1 or array.size < 3:
        raise ValueError(f"{name} must be a one-dimensional array with at least 3 values")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} contains non-finite values")
    if positive and np.any(array <= 0.0):
        raise ValueError(f"{name} must be strictly positive")
    return array


def threshold_edge_ev(
    energy_ev: NDArray[np.float64],
    absorption_cm1: NDArray[np.float64],
    threshold_cm1: float,
) -> float:
    """Interpolate the first threshold crossing."""

    threshold = float(threshold_cm1)
    if not np.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("threshold must be finite and positive")
    indices = np.flatnonzero(absorption_cm1 >= threshold)
    if indices.size == 0:
        raise ValueError("threshold is not crossed")
    index = int(indices[0])
    if index == 0:
        return float(energy_ev[0])
    e0, e1 = energy_ev[index - 1], energy_ev[index]
    a0, a1 = absorption_cm1[index - 1], absorption_cm1[index]
    if a1 == a0:
        return float(e1)
    fraction = (threshold - a0) / (a1 - a0)
    return float(e0 + fraction * (e1 - e0))


def fit_fractional_power_edge(
    energy_ev: NDArray[np.float64],
    absorption_cm1: NDArray[np.float64],
    *,
    edge_bounds_ev: tuple[float, float],
    exponent: float | None,
    grid_points: int = 4001,
) -> dict[str, float]:
    """Fit ``alpha=A*(E-Eg)^p/E`` by deterministic edge grid search."""

    lower, upper = (float(edge_bounds_ev[0]), float(edge_bounds_ev[1]))
    if not np.isfinite(lower) or not np.isfinite(upper) or lower >= upper:
        raise ValueError("edge search bounds must be finite and ordered")
    if upper >= float(np.min(energy_ev)):
        raise ValueError("edge search upper bound must be below the fitted energy range")
    if grid_points < 101:
        raise ValueError("grid_points must be at least 101")
    fixed = None if exponent is None else float(exponent)
    if fixed is not None and (not np.isfinite(fixed) or not 0.2 <= fixed <= 1.5):
        raise ValueError("fixed exponent must lie in [0.2, 1.5]")

    target = np.log(absorption_cm1 * energy_ev)
    best: tuple[float, float, float, float] | None = None
    for edge in np.linspace(lower, upper, grid_points):
        predictor = np.log(energy_ev - edge)
        if fixed is None:
            design = np.column_stack((np.ones_like(predictor), predictor))
            log_amplitude, fitted_exponent = np.linalg.lstsq(
                design, target, rcond=None
            )[0]
            if not 0.2 <= fitted_exponent <= 1.5:
                continue
        else:
            fitted_exponent = fixed
            log_amplitude = float(np.mean(target - fixed * predictor))
        predicted = log_amplitude + fitted_exponent * predictor
        mse = float(np.mean((target - predicted) ** 2))
        if best is None or mse < best[0]:
            best = (
                mse,
                float(edge),
                float(np.exp(log_amplitude)),
                float(fitted_exponent),
            )
    if best is None:
        raise RuntimeError("no valid fractional-power edge candidate")
    return {
        "edge_ev": best[1],
        "amplitude": best[2],
        "exponent": best[3],
        "log_mean_square_error": best[0],
    }


def chu_1994_beta_ev_inverse(composition_x: float, temperature_k: float) -> float:
    """Return the Chu 1994 Kane-region curvature parameter.

    The provenance-bound prior-art law is

    ``beta(x,T) = -1 + 0.083*T + (21 - 0.13*T)*x``.

    Its use here is restricted to the composition and temperature range reported
    by the source family. It is an observation-model candidate, not a gap law.
    """

    composition = float(composition_x)
    temperature = float(temperature_k)
    if not np.isfinite(composition) or not np.isfinite(temperature):
        raise ValueError("Chu 1994 composition and temperature must be finite")
    if not CHU_1994_COMPOSITION_RANGE[0] <= composition <= CHU_1994_COMPOSITION_RANGE[1]:
        raise ValueError(
            "Chu 1994 candidate requires composition_x in "
            f"[{CHU_1994_COMPOSITION_RANGE[0]}, {CHU_1994_COMPOSITION_RANGE[1]}]"
        )
    if not CHU_1994_TEMPERATURE_RANGE_K[0] <= temperature <= CHU_1994_TEMPERATURE_RANGE_K[1]:
        raise ValueError(
            "Chu 1994 candidate requires temperature_k in "
            f"[{CHU_1994_TEMPERATURE_RANGE_K[0]}, "
            f"{CHU_1994_TEMPERATURE_RANGE_K[1]}]"
        )
    beta = -1.0 + 0.083 * temperature + (21.0 - 0.13 * temperature) * composition
    if beta <= 0.0:
        raise ValueError("Chu 1994 beta is nonpositive at the declared x,T point")
    return float(beta)


def fit_chu_1994_kane_edge(
    energy_ev: NDArray[np.float64],
    absorption_cm1: NDArray[np.float64],
    *,
    edge_bounds_ev: tuple[float, float],
    composition_x: float,
    temperature_k: float,
    grid_points: int = 4001,
) -> dict[str, float]:
    """Fit the Chu 1994 Kane-region observation law.

    The candidate model is

    ``alpha = alpha_g * exp(sqrt(beta(x,T) * (E-Eg)))``.

    ``beta`` is fixed by the source law. ``Eg`` is found by deterministic grid
    search and ``log(alpha_g)`` is solved analytically at each edge candidate.
    """

    lower, upper = (float(edge_bounds_ev[0]), float(edge_bounds_ev[1]))
    if not np.isfinite(lower) or not np.isfinite(upper) or lower >= upper:
        raise ValueError("edge search bounds must be finite and ordered")
    if upper >= float(np.min(energy_ev)):
        raise ValueError("edge search upper bound must be below the fitted energy range")
    if grid_points < 101:
        raise ValueError("grid_points must be at least 101")
    beta = chu_1994_beta_ev_inverse(composition_x, temperature_k)
    target = np.log(absorption_cm1)
    best: tuple[float, float, float] | None = None
    for edge in np.linspace(lower, upper, grid_points):
        predictor = np.sqrt(beta * (energy_ev - edge))
        log_alpha_g = float(np.mean(target - predictor))
        predicted = log_alpha_g + predictor
        mse = float(np.mean((target - predicted) ** 2))
        if best is None or mse < best[0]:
            best = (mse, float(edge), float(np.exp(log_alpha_g)))
    if best is None:
        raise RuntimeError("no valid Chu 1994 Kane-region edge candidate")
    return {
        "edge_ev": best[1],
        "alpha_g_cm1": best[2],
        "beta_ev_inverse": beta,
        "log_mean_square_error": best[0],
    }


def _validate_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    if str(_required(payload, "schema_version", context="contract")) != CONTRACT_VERSION:
        raise ValueError(f"schema_version must be {CONTRACT_VERSION!r}")
    specimen_id = str(_required(payload, "specimen_id", context="contract")).strip()
    measurement_id = str(_required(payload, "measurement_id", context="contract")).strip()
    if not specimen_id or not measurement_id:
        raise ValueError("specimen_id and measurement_id must be non-empty")

    source = dict(_required(payload, "source", context="contract"))
    for key in ("kind", "reference", "calibration_record"):
        if not str(_required(source, key, context="source")).strip():
            raise ValueError(f"source.{key} must be explicit and non-empty")

    metadata = dict(_required(payload, "metadata", context="contract"))
    required_metadata = (
        "modality",
        "temperature_k",
        "thickness_um",
        "composition_x",
        "composition_sigma_x",
        "composition_method",
        "carrier_type",
        "carrier_density_cm3",
        "carrier_density_status",
        "tail_model",
    )
    for key in required_metadata:
        _required(metadata, key, context="metadata")
    temperature = float(metadata["temperature_k"])
    if not np.isfinite(temperature) or temperature < 0.0:
        raise ValueError("metadata.temperature_k must be finite and nonnegative")
    if metadata["carrier_type"] not in {"n", "p", "intrinsic", "unknown"}:
        raise ValueError("metadata.carrier_type must be n, p, intrinsic, or unknown")
    if metadata["carrier_density_cm3"] is None and not str(
        metadata["carrier_density_status"]
    ).strip():
        raise ValueError("unknown carrier density requires an explicit status")
    for key in ("modality", "composition_method", "tail_model"):
        if not str(metadata[key]).strip():
            raise ValueError(f"metadata.{key} must be explicit and non-empty")

    assumptions = dict(_required(payload, "analysis_assumptions", context="contract"))
    fit_window = np.asarray(
        _required(
            assumptions,
            "fit_absorption_window_cm1",
            context="analysis_assumptions",
        ),
        dtype=float,
    )
    bounds = np.asarray(
        _required(
            assumptions,
            "edge_search_bounds_ev",
            context="analysis_assumptions",
        ),
        dtype=float,
    )
    thresholds = np.asarray(
        _required(assumptions, "thresholds_cm1", context="analysis_assumptions"),
        dtype=float,
    )
    exponents = list(
        _required(
            assumptions,
            "fractional_power_exponents",
            context="analysis_assumptions",
        )
    )
    include_chu = assumptions.get("include_chu_1994_kane_region", False)
    if not isinstance(include_chu, bool):
        raise ValueError("include_chu_1994_kane_region must be boolean")
    if fit_window.shape != (2,) or not np.all(np.isfinite(fit_window)) or not fit_window[0] < fit_window[1]:
        raise ValueError("fit_absorption_window_cm1 must contain two ordered values")
    if bounds.shape != (2,) or not np.all(np.isfinite(bounds)) or not bounds[0] < bounds[1]:
        raise ValueError("edge_search_bounds_ev must contain two ordered values")
    if thresholds.ndim != 1 or thresholds.size == 0 or np.any(thresholds <= 0.0):
        raise ValueError("thresholds_cm1 must contain positive values")
    if len(exponents) == 0:
        raise ValueError("fractional_power_exponents must not be empty")
    normalized_exponents: list[float | None] = []
    for value in exponents:
        if value == "free":
            normalized_exponents.append(None)
        else:
            number = float(value)
            if not 0.2 <= number <= 1.5:
                raise ValueError("fractional power exponents must lie in [0.2, 1.5]")
            normalized_exponents.append(number)

    if include_chu:
        if metadata["composition_x"] is None:
            raise ValueError(
                "Chu 1994 candidate requires a measured or declared composition_x"
            )
        chu_1994_beta_ev_inverse(float(metadata["composition_x"]), temperature)

    spectrum = dict(_required(payload, "spectrum", context="contract"))
    energy = _finite_vector(
        _required(spectrum, "energy_ev", context="spectrum"),
        name="energy_ev",
    )
    absorption = _finite_vector(
        _required(spectrum, "absorption_cm1", context="spectrum"),
        name="absorption_cm1",
        positive=True,
    )
    if energy.shape != absorption.shape:
        raise ValueError("energy_ev and absorption_cm1 must have equal length")
    if np.any(np.diff(energy) <= 0.0):
        raise ValueError("energy_ev must be strictly increasing")
    mask = (absorption >= fit_window[0]) & (absorption <= fit_window[1])
    if np.count_nonzero(mask) < 20:
        raise ValueError("fit window must contain at least 20 spectral points")
    if bounds[1] >= float(np.min(energy[mask])):
        raise ValueError("edge search upper bound must be below the fitted energy range")

    return {
        "specimen_id": specimen_id,
        "measurement_id": measurement_id,
        "source": source,
        "metadata": metadata,
        "fit_window": fit_window,
        "bounds": bounds,
        "thresholds": thresholds,
        "exponents": normalized_exponents,
        "include_chu_1994_kane_region": include_chu,
        "energy": energy,
        "absorption": absorption,
        "mask": mask,
    }


def _envelope(values: list[float]) -> dict[str, float | int]:
    array = np.asarray(values, dtype=float)
    return {
        "candidate_count": int(array.size),
        "minimum_edge_ev": float(np.min(array)),
        "maximum_edge_ev": float(np.max(array)),
        "descriptive_median_edge_ev": float(np.median(array)),
        "full_span_mev": float(1000.0 * np.ptp(array)),
        "half_range_mev": float(500.0 * np.ptp(array)),
    }


def analyze_absorption_edge_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate the declared model and threshold ensemble."""

    validated = _validate_contract(payload)
    energy = validated["energy"]
    absorption = validated["absorption"]
    mask = validated["mask"]
    fit_energy = energy[mask]
    fit_absorption = absorption[mask]

    model_candidates: list[dict[str, Any]] = []
    for exponent in validated["exponents"]:
        fit = fit_fractional_power_edge(
            fit_energy,
            fit_absorption,
            edge_bounds_ev=tuple(validated["bounds"]),
            exponent=exponent,
        )
        identifier = (
            "fractional_power_free"
            if exponent is None
            else f"fractional_power_p_{exponent:g}"
        )
        model_candidates.append(
            {"candidate_id": identifier, "method": "fractional_power_fit", **fit}
        )

    if validated["include_chu_1994_kane_region"]:
        chu_fit = fit_chu_1994_kane_edge(
            fit_energy,
            fit_absorption,
            edge_bounds_ev=tuple(validated["bounds"]),
            composition_x=float(validated["metadata"]["composition_x"]),
            temperature_k=float(validated["metadata"]["temperature_k"]),
        )
        model_candidates.append(
            {
                "candidate_id": "chu_1994_kane_region",
                "method": "chu_1994_kane_region_fit",
                "source_doi": CHU_1994_SOURCE_DOI,
                "model_expression": (
                    "alpha=alpha_g*exp(sqrt(beta(x,T)*(E-Eg)))"
                ),
                "beta_expression": (
                    "-1+0.083*T+(21-0.13*T)*x"
                ),
                "source_validity_range": {
                    "composition_x": list(CHU_1994_COMPOSITION_RANGE),
                    "temperature_k": list(CHU_1994_TEMPERATURE_RANGE_K),
                },
                **chu_fit,
            }
        )

    threshold_candidates: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    for threshold in validated["thresholds"]:
        identifier = f"threshold_{threshold:g}_cm-1"
        try:
            edge = threshold_edge_ev(energy, absorption, float(threshold))
        except ValueError as exc:
            excluded.append({"candidate_id": identifier, "reason": str(exc)})
        else:
            threshold_candidates.append(
                {
                    "candidate_id": identifier,
                    "method": "fixed_absorption_threshold",
                    "threshold_cm1": float(threshold),
                    "edge_ev": edge,
                }
            )

    all_candidates = model_candidates + threshold_candidates
    if len(all_candidates) < 2:
        raise ValueError("at least two valid edge candidates are required")
    all_edges = [float(item["edge_ev"]) for item in all_candidates]
    model_edges = [float(item["edge_ev"]) for item in model_candidates]
    threshold_edges = [float(item["edge_ev"]) for item in threshold_candidates]

    output = {
        "schema_version": CONTRACT_VERSION,
        "analysis": "absorption edge model-ensemble uncertainty export",
        "input_sha256": _canonical_digest(payload),
        "specimen_id": validated["specimen_id"],
        "measurement_id": validated["measurement_id"],
        "source": validated["source"],
        "metadata": validated["metadata"],
        "analysis_assumptions": {
            "fit_absorption_window_cm1": validated["fit_window"].tolist(),
            "edge_search_bounds_ev": validated["bounds"].tolist(),
            "thresholds_cm1": validated["thresholds"].tolist(),
            "fractional_power_exponents": [
                "free" if value is None else value for value in validated["exponents"]
            ],
            "include_chu_1994_kane_region": validated[
                "include_chu_1994_kane_region"
            ],
            "fit_point_count": int(np.count_nonzero(mask)),
        },
        "model_candidates": model_candidates,
        "threshold_candidates": threshold_candidates,
        "excluded_candidates": excluded,
        "combined_envelope": _envelope(all_edges),
        "model_family_envelope": _envelope(model_edges),
        "threshold_envelope": None if not threshold_edges else _envelope(threshold_edges),
        "decision": {
            "research_use_only": True,
            "production_correction_authorized": False,
            "single_corrected_gap_selected": False,
            "report_full_candidate_ensemble": True,
            "report_edge_model_uncertainty_envelope": True,
        },
        "claim_boundary": (
            "The envelope quantifies declared model and threshold sensitivity. It does "
            "not estimate an intrinsic material gap or identify a universal correction."
        ),
    }
    return output
