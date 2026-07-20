"""Chang 2006 nonparabolic-Urbach absorption observation operator.

This module implements a conservative, provenance-bound observation-model candidate
derived from Chang et al., Applied Physics Letters 89, 062109 (2006),
DOI 10.1063/1.2245220. It is not a material-gap law.
"""
from __future__ import annotations

from collections.abc import Mapping
import math
from typing import Any

import numpy as np
from numpy.typing import NDArray

CHANG_2006_SOURCE_DOI = "10.1063/1.2245220"
CHANG_2006_COMPOSITION_RANGE = (0.21, 0.23)
CHANG_2006_TEMPERATURE_RANGE_K = (77.0, 80.0)
CHANG_2006_RELATIVE_ENERGY_RANGE_EV = (-0.020, 0.300)
CHANG_2006_NORMALIZATION = (
    "continuity-normalized at E0=Eg+W/2 from source Eqs. (1), (9), and (13); "
    "the ambiguous absolute exponential prefactor printed in the first branch "
    "of Eq. (14) is not used literally"
)
_ALLOWED_CONFIGURATION_KEYS = {
    "enabled",
    "fit_absorption_window_cm1",
    "edge_search_bounds_ev",
    "urbach_width_ev",
    "urbach_width_provenance",
    "hyperbola_b_ev",
    "hyperbola_b_provenance",
    "grid_points",
}
_REQUIRED_ENABLED_KEYS = _ALLOWED_CONFIGURATION_KEYS - {"enabled"}


def _finite_positive(value: Any, *, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


def _ordered_pair(value: Any, *, name: str, positive: bool = False) -> tuple[float, float]:
    array = np.asarray(value, dtype=float)
    if array.shape != (2,) or not np.all(np.isfinite(array)) or not array[0] < array[1]:
        raise ValueError(f"{name} must contain two finite ordered values")
    if positive and np.any(array <= 0.0):
        raise ValueError(f"{name} must contain positive values")
    return float(array[0]), float(array[1])


def chang_2006_intrinsic_shape(
    energy_ev: NDArray[np.float64],
    *,
    edge_ev: float,
    hyperbola_b_ev: float,
) -> NDArray[np.float64]:
    """Return the dimensionless intrinsic shape from Chang 2006 Eq. (9)."""

    energy = np.asarray(energy_ev, dtype=float)
    edge = float(edge_ev)
    b_value = _finite_positive(hyperbola_b_ev, name="hyperbola_b_ev")
    if energy.ndim != 1 or energy.size == 0 or not np.all(np.isfinite(energy)):
        raise ValueError("energy_ev must be a nonempty finite one-dimensional array")
    if np.any(energy <= 0.0):
        raise ValueError("energy_ev must be positive")

    epsilon = energy - edge
    if np.any(epsilon < 0.0):
        raise ValueError("intrinsic Chang 2006 branch requires energy_ev >= edge_ev")

    first_argument = epsilon + b_value
    second_argument = epsilon + 2.0 * b_value
    first_radicand = first_argument**2 - b_value**2
    second_radicand = second_argument**2 - (2.0 * b_value) ** 2
    if np.any(first_radicand < -1e-14) or np.any(second_radicand < -1e-14):
        raise ValueError("Chang 2006 intrinsic radicand is negative")
    first = first_argument * np.sqrt(np.maximum(first_radicand, 0.0))
    second = 0.125 * second_argument * np.sqrt(np.maximum(second_radicand, 0.0))
    shape = (first + second) / energy
    if np.any(~np.isfinite(shape)) or np.any(shape <= 0.0):
        raise ValueError("Chang 2006 intrinsic shape is nonpositive or nonfinite")
    return shape


def chang_2006_absorption_shape(
    energy_ev: NDArray[np.float64],
    *,
    edge_ev: float,
    urbach_width_ev: float,
    hyperbola_b_ev: float,
) -> NDArray[np.float64]:
    """Evaluate the continuity-normalized piecewise Chang 2006 shape."""

    energy = np.asarray(energy_ev, dtype=float)
    edge = float(edge_ev)
    width = _finite_positive(urbach_width_ev, name="urbach_width_ev")
    b_value = _finite_positive(hyperbola_b_ev, name="hyperbola_b_ev")
    if not math.isfinite(edge) or edge <= 0.0:
        raise ValueError("edge_ev must be finite and positive")
    if energy.ndim != 1 or energy.size == 0 or not np.all(np.isfinite(energy)):
        raise ValueError("energy_ev must be a nonempty finite one-dimensional array")
    if np.any(energy <= 0.0):
        raise ValueError("energy_ev must be positive")

    join_energy = edge + 0.5 * width
    join_shape = float(
        chang_2006_intrinsic_shape(
            np.asarray([join_energy], dtype=float),
            edge_ev=edge,
            hyperbola_b_ev=b_value,
        )[0]
    )
    result = np.empty_like(energy)
    tail_mask = energy < join_energy
    result[tail_mask] = join_shape * np.exp((energy[tail_mask] - join_energy) / width)
    if np.any(~tail_mask):
        result[~tail_mask] = chang_2006_intrinsic_shape(
            energy[~tail_mask],
            edge_ev=edge,
            hyperbola_b_ev=b_value,
        )
    if np.any(~np.isfinite(result)) or np.any(result <= 0.0):
        raise ValueError("Chang 2006 absorption shape is nonpositive or nonfinite")
    return result


def fit_chang_2006_nonparabolic_urbach_edge(
    energy_ev: NDArray[np.float64],
    absorption_cm1: NDArray[np.float64],
    *,
    edge_bounds_ev: tuple[float, float],
    fit_absorption_window_cm1: tuple[float, float],
    urbach_width_ev: float,
    hyperbola_b_ev: float,
    grid_points: int = 2001,
) -> dict[str, float | int]:
    """Fit ``Eg`` with fixed provenance-bound ``W`` and ``b``.

    A positive multiplicative amplitude is solved analytically in log space for
    every deterministic edge-grid candidate.
    """

    energy = np.asarray(energy_ev, dtype=float)
    absorption = np.asarray(absorption_cm1, dtype=float)
    if energy.ndim != 1 or absorption.ndim != 1 or energy.shape != absorption.shape:
        raise ValueError("energy_ev and absorption_cm1 must be equal one-dimensional arrays")
    if energy.size < 20 or not np.all(np.isfinite(energy)) or not np.all(np.isfinite(absorption)):
        raise ValueError("Chang 2006 fit requires at least 20 finite spectral points")
    if np.any(energy <= 0.0) or np.any(absorption <= 0.0):
        raise ValueError("Chang 2006 fit requires positive energy and absorption")
    if np.any(np.diff(energy) <= 0.0):
        raise ValueError("energy_ev must be strictly increasing")

    lower_edge, upper_edge = _ordered_pair(edge_bounds_ev, name="edge_bounds_ev")
    lower_alpha, upper_alpha = _ordered_pair(
        fit_absorption_window_cm1,
        name="fit_absorption_window_cm1",
        positive=True,
    )
    width = _finite_positive(urbach_width_ev, name="urbach_width_ev")
    b_value = _finite_positive(hyperbola_b_ev, name="hyperbola_b_ev")
    if not isinstance(grid_points, int) or isinstance(grid_points, bool):
        raise ValueError("grid_points must be an integer")
    if not 101 <= grid_points <= 20001:
        raise ValueError("grid_points must lie in [101, 20001]")

    mask = (absorption >= lower_alpha) & (absorption <= upper_alpha)
    fit_energy = energy[mask]
    fit_absorption = absorption[mask]
    if fit_energy.size < 20:
        raise ValueError("Chang 2006 fit window must contain at least 20 spectral points")

    target = np.log(fit_absorption)
    best: tuple[float, float, float, int, int] | None = None
    relative_lower, relative_upper = CHANG_2006_RELATIVE_ENERGY_RANGE_EV
    for edge in np.linspace(lower_edge, upper_edge, grid_points):
        relative = fit_energy - edge
        if relative[0] < relative_lower - 1e-12 or relative[-1] > relative_upper + 1e-12:
            continue
        join_energy = edge + 0.5 * width
        tail_count = int(np.count_nonzero(fit_energy < join_energy))
        intrinsic_count = int(np.count_nonzero(fit_energy >= join_energy))
        if tail_count < 5 or intrinsic_count < 10:
            continue
        shape = chang_2006_absorption_shape(
            fit_energy,
            edge_ev=float(edge),
            urbach_width_ev=width,
            hyperbola_b_ev=b_value,
        )
        log_amplitude = float(np.mean(target - np.log(shape)))
        predicted = log_amplitude + np.log(shape)
        mse = float(np.mean((target - predicted) ** 2))
        candidate = (
            mse,
            float(edge),
            float(np.exp(log_amplitude)),
            tail_count,
            intrinsic_count,
        )
        if best is None or candidate[:2] < best[:2]:
            best = candidate

    if best is None:
        raise ValueError(
            "no Chang 2006 edge candidate satisfies the relative-energy domain "
            "and minimum tail/intrinsic branch coverage"
        )
    return {
        "edge_ev": best[1],
        "amplitude_cm1": best[2],
        "urbach_width_ev": width,
        "hyperbola_b_ev": b_value,
        "join_energy_ev": best[1] + 0.5 * width,
        "log_mean_square_error": best[0],
        "fit_point_count": int(fit_energy.size),
        "tail_point_count": best[3],
        "intrinsic_point_count": best[4],
    }


def build_chang_2006_candidate(
    configuration: Mapping[str, Any] | None,
    *,
    metadata: Mapping[str, Any],
    energy_ev: NDArray[np.float64],
    absorption_cm1: NDArray[np.float64],
) -> dict[str, Any] | None:
    """Validate the opt-in contract and return one model candidate."""

    if configuration is None:
        return None
    if not isinstance(configuration, Mapping):
        raise ValueError("chang_2006_nonparabolic_urbach must be an object")
    unknown = set(configuration) - _ALLOWED_CONFIGURATION_KEYS
    if unknown:
        raise ValueError(
            "chang_2006_nonparabolic_urbach contains unsupported fields: "
            + ", ".join(sorted(unknown))
        )
    enabled = configuration.get("enabled", False)
    if not isinstance(enabled, bool):
        raise ValueError("Chang 2006 enabled must be boolean")
    if not enabled:
        if set(configuration) != {"enabled"}:
            raise ValueError("disabled Chang 2006 configuration may contain only enabled")
        return None

    missing = _REQUIRED_ENABLED_KEYS - set(configuration)
    if missing:
        raise ValueError(
            "enabled Chang 2006 configuration is missing: " + ", ".join(sorted(missing))
        )

    composition = metadata.get("composition_x")
    temperature = metadata.get("temperature_k")
    if composition is None:
        raise ValueError("Chang 2006 candidate requires composition_x")
    composition_value = float(composition)
    temperature_value = float(temperature)
    if not (
        CHANG_2006_COMPOSITION_RANGE[0]
        <= composition_value
        <= CHANG_2006_COMPOSITION_RANGE[1]
    ):
        raise ValueError(
            "Chang 2006 candidate requires composition_x in "
            f"[{CHANG_2006_COMPOSITION_RANGE[0]}, {CHANG_2006_COMPOSITION_RANGE[1]}]"
        )
    if not (
        CHANG_2006_TEMPERATURE_RANGE_K[0]
        <= temperature_value
        <= CHANG_2006_TEMPERATURE_RANGE_K[1]
    ):
        raise ValueError(
            "Chang 2006 candidate requires temperature_k in "
            f"[{CHANG_2006_TEMPERATURE_RANGE_K[0]}, "
            f"{CHANG_2006_TEMPERATURE_RANGE_K[1]}]"
        )

    width_provenance = str(configuration["urbach_width_provenance"]).strip()
    b_provenance = str(configuration["hyperbola_b_provenance"]).strip()
    if not width_provenance:
        raise ValueError("Chang 2006 urbach_width_provenance must be explicit")
    if not b_provenance:
        raise ValueError("Chang 2006 hyperbola_b_provenance must be explicit")

    edge_bounds = _ordered_pair(
        configuration["edge_search_bounds_ev"],
        name="Chang 2006 edge_search_bounds_ev",
    )
    absorption_window = _ordered_pair(
        configuration["fit_absorption_window_cm1"],
        name="Chang 2006 fit_absorption_window_cm1",
        positive=True,
    )
    width = _finite_positive(
        configuration["urbach_width_ev"],
        name="Chang 2006 urbach_width_ev",
    )
    b_value = _finite_positive(
        configuration["hyperbola_b_ev"],
        name="Chang 2006 hyperbola_b_ev",
    )
    grid_points_raw = configuration["grid_points"]
    if not isinstance(grid_points_raw, int) or isinstance(grid_points_raw, bool):
        raise ValueError("Chang 2006 grid_points must be an integer")

    fit = fit_chang_2006_nonparabolic_urbach_edge(
        energy_ev,
        absorption_cm1,
        edge_bounds_ev=edge_bounds,
        fit_absorption_window_cm1=absorption_window,
        urbach_width_ev=width,
        hyperbola_b_ev=b_value,
        grid_points=grid_points_raw,
    )
    declared_configuration = {
        "enabled": True,
        "fit_absorption_window_cm1": list(absorption_window),
        "edge_search_bounds_ev": list(edge_bounds),
        "urbach_width_ev": width,
        "urbach_width_provenance": width_provenance,
        "hyperbola_b_ev": b_value,
        "hyperbola_b_provenance": b_provenance,
        "grid_points": grid_points_raw,
    }
    return {
        "candidate_id": "chang_2006_nonparabolic_urbach",
        "method": "chang_2006_nonparabolic_urbach_fit",
        "source_doi": CHANG_2006_SOURCE_DOI,
        "model_expression": (
            "intrinsic: source Eq.(9); tail: alpha(E0)*exp((E-E0)/W); "
            "E0=Eg+W/2"
        ),
        "normalization_provenance": CHANG_2006_NORMALIZATION,
        "source_validity_range": {
            "composition_x": list(CHANG_2006_COMPOSITION_RANGE),
            "temperature_k": list(CHANG_2006_TEMPERATURE_RANGE_K),
            "energy_minus_edge_ev": list(CHANG_2006_RELATIVE_ENERGY_RANGE_EV),
        },
        "declared_configuration": declared_configuration,
        **fit,
    }
