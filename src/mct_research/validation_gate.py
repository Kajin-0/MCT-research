"""Deterministic scoring for external HgCdTe validation routes.

The score ranks expected decision value under a declared acquisition state. It is
not a probability that a source or model is correct. Route criteria must be
updated after every source audit rather than silently retaining provisional
values.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

CRITERION_RANGES: dict[str, tuple[int, int]] = {
    "same_specimen_state": (0, 2),
    "composition_provenance": (0, 2),
    "carrier_provenance": (0, 2),
    "thickness_provenance": (0, 2),
    "calibrated_spectrum": (0, 2),
    "equation_completeness": (0, 2),
    "falsification_power": (0, 3),
    "reproducibility_rights": (0, 2),
    "flagship_relevance": (0, 3),
    "nuisance_penalty": (0, 3),
    "implementation_cost": (1, 3),
}

ACTIONABLE_READINESS = frozenset({"ready_now", "ready_after_retrieval"})


@dataclass(frozen=True)
class ValidationRouteScore:
    """One scored route with deterministic tie-break metadata."""

    route_id: str
    title: str
    score: int
    readiness: str
    source_priority: int
    implementation_cost: int
    source_keys: tuple[str, ...]
    blocking_artifacts: tuple[str, ...]


def _required_string(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _string_tuple(mapping: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = mapping.get(key)
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{key} must be a sequence of strings")
    result = tuple(str(item).strip() for item in value)
    if not result or any(not item for item in result):
        raise ValueError(f"{key} must contain non-empty strings")
    if len(set(result)) != len(result):
        raise ValueError(f"{key} must not contain duplicates")
    return result


def score_validation_criteria(criteria: Mapping[str, Any]) -> int:
    """Return the declared route score after strict criterion validation."""

    missing = set(CRITERION_RANGES) - set(criteria)
    extra = set(criteria) - set(CRITERION_RANGES)
    if missing or extra:
        raise ValueError(
            "criteria keys must match the scoring contract; "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )

    values: dict[str, int] = {}
    for key, (lower, upper) in CRITERION_RANGES.items():
        value = criteria[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"criterion {key} must be an integer")
        if not lower <= value <= upper:
            raise ValueError(
                f"criterion {key} must lie in the inclusive range "
                f"[{lower}, {upper}]"
            )
        values[key] = value

    return int(
        3 * values["falsification_power"]
        + 3 * values["flagship_relevance"]
        + 2 * values["same_specimen_state"]
        + 2 * values["calibrated_spectrum"]
        + values["composition_provenance"]
        + values["carrier_provenance"]
        + values["thickness_provenance"]
        + values["equation_completeness"]
        + values["reproducibility_rights"]
        - 2 * values["nuisance_penalty"]
        - values["implementation_cost"]
    )


def rank_validation_routes(manifest: Mapping[str, Any]) -> tuple[ValidationRouteScore, ...]:
    """Score and rank all declared validation routes.

    Sorting follows the manifest contract:

    1. larger score;
    2. lower minimum source priority;
    3. lower implementation cost;
    4. lexicographic route id.
    """

    sources = manifest.get("sources")
    routes = manifest.get("validation_routes")
    if not isinstance(sources, list) or not sources:
        raise ValueError("manifest sources must be a non-empty list")
    if not isinstance(routes, list) or not routes:
        raise ValueError("manifest validation_routes must be a non-empty list")

    priority_by_key: dict[str, int] = {}
    for source in sources:
        if not isinstance(source, Mapping):
            raise ValueError("each source record must be an object")
        key = _required_string(source, "citation_key")
        priority = source.get("priority")
        if isinstance(priority, bool) or not isinstance(priority, int) or priority < 1:
            raise ValueError("source priority must be a positive integer")
        if key in priority_by_key:
            raise ValueError(f"duplicate citation key: {key}")
        priority_by_key[key] = priority

    scored: list[ValidationRouteScore] = []
    route_ids: set[str] = set()
    for route in routes:
        if not isinstance(route, Mapping):
            raise ValueError("each validation route must be an object")
        route_id = _required_string(route, "route_id")
        if route_id in route_ids:
            raise ValueError(f"duplicate route id: {route_id}")
        route_ids.add(route_id)
        source_keys = _string_tuple(route, "source_keys")
        unknown = set(source_keys) - set(priority_by_key)
        if unknown:
            raise ValueError(f"route {route_id} references unknown sources: {sorted(unknown)}")
        criteria = route.get("criteria")
        if not isinstance(criteria, Mapping):
            raise ValueError(f"route {route_id} criteria must be an object")
        scored.append(
            ValidationRouteScore(
                route_id=route_id,
                title=_required_string(route, "title"),
                score=score_validation_criteria(criteria),
                readiness=_required_string(route, "readiness"),
                source_priority=min(priority_by_key[key] for key in source_keys),
                implementation_cost=int(criteria["implementation_cost"]),
                source_keys=source_keys,
                blocking_artifacts=_string_tuple(route, "blocking_artifacts"),
            )
        )

    scored.sort(
        key=lambda item: (
            -item.score,
            item.source_priority,
            item.implementation_cost,
            item.route_id,
        )
    )
    return tuple(scored)


def select_first_external_validation_route(
    manifest: Mapping[str, Any],
    *,
    actionable_readiness: Iterable[str] = ACTIONABLE_READINESS,
) -> ValidationRouteScore:
    """Return the highest-ranked route that is actionable after retrieval."""

    allowed = frozenset(str(value) for value in actionable_readiness)
    if not allowed:
        raise ValueError("actionable_readiness must not be empty")
    for route in rank_validation_routes(manifest):
        if route.readiness in allowed:
            return route
    raise ValueError("manifest contains no actionable external-validation route")


def prioritized_source_requests(manifest: Mapping[str, Any]) -> tuple[str, ...]:
    """Order source citation keys by selected-route relevance then source priority."""

    selected = select_first_external_validation_route(manifest)
    sources = manifest.get("sources")
    assert isinstance(sources, list)
    priority_by_key = {
        str(source["citation_key"]): int(source["priority"])
        for source in sources
    }
    remaining = sorted(
        (key for key in priority_by_key if key not in selected.source_keys),
        key=lambda key: (priority_by_key[key], key),
    )
    return tuple(selected.source_keys) + tuple(remaining)
