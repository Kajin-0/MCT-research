"""Local sensitivity diagnostics for the external-validation route gate."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .validation_gate import (
    ACTIONABLE_READINESS,
    CRITERION_RANGES,
    rank_validation_routes,
)

CRITERION_WEIGHTS: dict[str, int] = {
    "same_specimen_state": 2,
    "composition_provenance": 1,
    "carrier_provenance": 1,
    "thickness_provenance": 1,
    "calibrated_spectrum": 2,
    "equation_completeness": 1,
    "falsification_power": 3,
    "reproducibility_rights": 1,
    "flagship_relevance": 3,
    "nuisance_penalty": -2,
    "implementation_cost": -1,
}


@dataclass(frozen=True)
class ValidationSelectionRobustness:
    """One-step score sensitivity around the selected actionable route."""

    selected_route_id: str
    closest_competitor_id: str
    current_margin: int
    maximum_selected_one_step_drop: int
    margin_after_selected_adverse_step: int
    maximum_competitor_one_step_gain: int
    margin_after_competitor_favorable_step: int
    margin_after_simultaneous_two_route_steps: int
    robust_to_any_single_one_level_change: bool
    robust_to_simultaneous_adverse_and_favorable_steps: bool


def _route_by_id(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    routes = manifest.get("validation_routes")
    if not isinstance(routes, list):
        raise ValueError("manifest validation_routes must be a list")
    result: dict[str, Mapping[str, Any]] = {}
    for route in routes:
        if not isinstance(route, Mapping):
            raise ValueError("each validation route must be an object")
        route_id = route.get("route_id")
        if not isinstance(route_id, str) or not route_id:
            raise ValueError("route_id must be a non-empty string")
        if route_id in result:
            raise ValueError(f"duplicate route id: {route_id}")
        result[route_id] = route
    return result


def _maximum_adverse_drop(criteria: Mapping[str, Any]) -> int:
    drops: list[int] = []
    for key, weight in CRITERION_WEIGHTS.items():
        lower, upper = CRITERION_RANGES[key]
        value = int(criteria[key])
        if weight > 0 and value > lower:
            drops.append(weight)
        elif weight < 0 and value < upper:
            drops.append(-weight)
    return max(drops, default=0)


def _maximum_favorable_gain(criteria: Mapping[str, Any]) -> int:
    gains: list[int] = []
    for key, weight in CRITERION_WEIGHTS.items():
        lower, upper = CRITERION_RANGES[key]
        value = int(criteria[key])
        if weight > 0 and value < upper:
            gains.append(weight)
        elif weight < 0 and value > lower:
            gains.append(-weight)
    return max(gains, default=0)


def selection_robustness(
    manifest: Mapping[str, Any],
) -> ValidationSelectionRobustness:
    """Evaluate one-level local sensitivity of the top actionable route.

    A *single one-level change* modifies one criterion on either the selected
    route or its closest actionable competitor. The simultaneous diagnostic
    applies one adverse selected-route change and one favorable competitor
    change; it is a two-change stress test rather than the declared gate.
    """

    actionable = [
        route
        for route in rank_validation_routes(manifest)
        if route.readiness in ACTIONABLE_READINESS
    ]
    if len(actionable) < 2:
        raise ValueError("at least two actionable routes are required")
    selected, competitor = actionable[:2]
    routes = _route_by_id(manifest)
    selected_criteria = routes[selected.route_id].get("criteria")
    competitor_criteria = routes[competitor.route_id].get("criteria")
    if not isinstance(selected_criteria, Mapping) or not isinstance(
        competitor_criteria, Mapping
    ):
        raise ValueError("route criteria must be objects")

    current_margin = selected.score - competitor.score
    selected_drop = _maximum_adverse_drop(selected_criteria)
    competitor_gain = _maximum_favorable_gain(competitor_criteria)
    selected_margin = current_margin - selected_drop
    competitor_margin = current_margin - competitor_gain
    simultaneous_margin = current_margin - selected_drop - competitor_gain

    return ValidationSelectionRobustness(
        selected_route_id=selected.route_id,
        closest_competitor_id=competitor.route_id,
        current_margin=current_margin,
        maximum_selected_one_step_drop=selected_drop,
        margin_after_selected_adverse_step=selected_margin,
        maximum_competitor_one_step_gain=competitor_gain,
        margin_after_competitor_favorable_step=competitor_margin,
        margin_after_simultaneous_two_route_steps=simultaneous_margin,
        robust_to_any_single_one_level_change=(
            selected_margin > 0 and competitor_margin > 0
        ),
        robust_to_simultaneous_adverse_and_favorable_steps=(
            simultaneous_margin > 0
        ),
    )
