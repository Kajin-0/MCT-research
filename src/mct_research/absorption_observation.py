"""Provenance-explicit uncertainty contracts for absorption-derived HgCdTe edges.

Experimental uncertainty and observation-model sensitivity are kept separate.
The module validates what was measured, how an edge was extracted, and which
same-record reanalyses define the sensitivity envelope. It never applies or
learns a universal correction to a reported edge.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

ABSORPTION_EDGE_EXPORT_SCHEMA_VERSION = "1.0"
ABSORPTION_EDGE_EXPORT_CONTRACT = "hgcdte_absorption_edge_uncertainty"

_ALLOWED_OBSERVABLES = {"absorption_edge_energy", "signed_gap_model_parameter"}
_ALLOWED_EXTRACTION_METHODS = {
    "model_fit_parameter",
    "fixed_absorption_threshold",
    "other",
}
_ALLOWED_EVIDENCE_CLASSES = {
    "experimental_primary",
    "experimental_secondary",
    "synthetic_method_benchmark",
    "template",
}
_ALLOWED_CARRIER_STATUS = {
    "measured",
    "inferred",
    "not_reported",
    "not_applicable",
}
_ALLOWED_TAIL_STATUS = {"modeled", "excluded", "not_reported", "not_applicable"}
_ALLOWED_SENSITIVITY_FACTORS = {
    "model_family",
    "fixed_threshold",
    "fit_window",
    "tail_model",
    "carrier_state",
    "thickness",
    "calibration",
    "other",
}


def _finite(value: float, *, name: str) -> float:
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _optional_nonnegative(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    result = _finite(value, name=name)
    if result < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return result


def _text(value: str, *, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name} must be non-empty")
    return result


def _json_mapping(value: Mapping[str, Any], *, name: str) -> dict[str, Any]:
    result = dict(value)
    try:
        json.dumps(result, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be JSON serializable") from exc
    return result


@dataclass(frozen=True)
class CompositionMetadata:
    value_x: float
    method: str
    status: str
    standard_uncertainty_x: float | None = None

    def __post_init__(self) -> None:
        value = _finite(self.value_x, name="composition value_x")
        if not 0.0 <= value <= 1.0:
            raise ValueError("composition value_x must lie in [0, 1]")
        object.__setattr__(self, "value_x", value)
        object.__setattr__(self, "method", _text(self.method, name="composition method"))
        object.__setattr__(self, "status", _text(self.status, name="composition status"))
        object.__setattr__(
            self,
            "standard_uncertainty_x",
            _optional_nonnegative(
                self.standard_uncertainty_x,
                name="composition standard uncertainty",
            ),
        )


@dataclass(frozen=True)
class TemperatureMetadata:
    value_k: float
    standard_uncertainty_k: float | None = None

    def __post_init__(self) -> None:
        value = _finite(self.value_k, name="temperature value_k")
        if value < 0.0:
            raise ValueError("temperature value_k must be non-negative")
        object.__setattr__(self, "value_k", value)
        object.__setattr__(
            self,
            "standard_uncertainty_k",
            _optional_nonnegative(
                self.standard_uncertainty_k,
                name="temperature standard uncertainty",
            ),
        )


@dataclass(frozen=True)
class AnalysisWindow:
    energy_ev: tuple[float, float] | None = None
    absorption_cm1: tuple[float, float] | None = None

    def __post_init__(self) -> None:
        if self.energy_ev is None and self.absorption_cm1 is None:
            raise ValueError(
                "analysis window requires energy_ev or absorption_cm1 bounds"
            )
        for field_name in ("energy_ev", "absorption_cm1"):
            raw = getattr(self, field_name)
            if raw is None:
                continue
            if len(raw) != 2:
                raise ValueError(f"{field_name} must contain lower and upper bounds")
            lower = _finite(raw[0], name=f"{field_name} lower")
            upper = _finite(raw[1], name=f"{field_name} upper")
            if lower >= upper:
                raise ValueError(f"{field_name} bounds must be strictly increasing")
            if field_name == "absorption_cm1" and lower < 0.0:
                raise ValueError("absorption_cm1 lower bound must be non-negative")
            object.__setattr__(self, field_name, (lower, upper))


@dataclass(frozen=True)
class EdgeModel:
    name: str
    expression: str
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _text(self.name, name="edge model name"))
        object.__setattr__(
            self,
            "expression",
            _text(self.expression, name="edge model expression"),
        )
        object.__setattr__(
            self,
            "parameters",
            _json_mapping(self.parameters, name="edge model parameters"),
        )


@dataclass(frozen=True)
class CarrierState:
    status: str
    carrier_type: str | None = None
    density_cm3: float | None = None
    standard_uncertainty_cm3: float | None = None
    method: str | None = None

    def __post_init__(self) -> None:
        status = str(self.status).strip()
        if status not in _ALLOWED_CARRIER_STATUS:
            raise ValueError(
                f"carrier status must be one of {sorted(_ALLOWED_CARRIER_STATUS)}"
            )
        object.__setattr__(self, "status", status)
        if status in {"measured", "inferred"}:
            if (
                self.carrier_type is None
                or self.density_cm3 is None
                or self.method is None
            ):
                raise ValueError(
                    "measured or inferred carrier state requires type, density, and method"
                )
            object.__setattr__(
                self,
                "carrier_type",
                _text(self.carrier_type, name="carrier type"),
            )
            density = _finite(self.density_cm3, name="carrier density_cm3")
            if density <= 0.0:
                raise ValueError("carrier density_cm3 must be positive")
            object.__setattr__(self, "density_cm3", density)
            object.__setattr__(
                self,
                "method",
                _text(self.method, name="carrier method"),
            )
            object.__setattr__(
                self,
                "standard_uncertainty_cm3",
                _optional_nonnegative(
                    self.standard_uncertainty_cm3,
                    name="carrier standard uncertainty",
                ),
            )
        elif self.density_cm3 is not None or self.standard_uncertainty_cm3 is not None:
            raise ValueError(
                "not_reported/not_applicable carrier state cannot include density"
            )


@dataclass(frozen=True)
class TailTreatment:
    status: str
    model: str | None = None
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        status = str(self.status).strip()
        if status not in _ALLOWED_TAIL_STATUS:
            raise ValueError(
                f"tail status must be one of {sorted(_ALLOWED_TAIL_STATUS)}"
            )
        object.__setattr__(self, "status", status)
        if status == "modeled" and self.model is None:
            raise ValueError("modeled tail treatment requires a model")
        if self.model is not None:
            object.__setattr__(self, "model", _text(self.model, name="tail model"))
        object.__setattr__(
            self,
            "parameters",
            _json_mapping(self.parameters, name="tail parameters"),
        )


@dataclass(frozen=True)
class SensitivityEstimate:
    label: str
    edge_ev: float
    varied_factors: tuple[str, ...]
    settings: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "label",
            _text(self.label, name="sensitivity label"),
        )
        object.__setattr__(
            self,
            "edge_ev",
            _finite(self.edge_ev, name="sensitivity edge_ev"),
        )
        factors = tuple(str(value).strip() for value in self.varied_factors)
        if not factors or any(not value for value in factors):
            raise ValueError(
                "sensitivity estimate requires at least one varied factor"
            )
        unknown = set(factors) - _ALLOWED_SENSITIVITY_FACTORS
        if unknown:
            raise ValueError(f"unknown sensitivity factors: {sorted(unknown)}")
        if len(set(factors)) != len(factors):
            raise ValueError("sensitivity factors must be unique")
        object.__setattr__(self, "varied_factors", factors)
        object.__setattr__(
            self,
            "settings",
            _json_mapping(self.settings, name="sensitivity settings"),
        )


@dataclass(frozen=True)
class AbsorptionEdgeObservation:
    record_id: str
    composition: CompositionMetadata
    temperature: TemperatureMetadata
    reported_edge_ev: float
    reported_standard_uncertainty_ev: float | None
    observable_definition: str
    measurement_modality: str
    extraction_method: str
    edge_model: EdgeModel
    analysis_window: AnalysisWindow
    fixed_threshold_cm1: float | None
    carrier_state: CarrierState
    tail_treatment: TailTreatment
    sensitivity_estimates: tuple[SensitivityEstimate, ...]
    source_doi: str
    source_locator: str
    evidence_class: str
    notes: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "record_id",
            _text(self.record_id, name="record_id"),
        )
        edge = _finite(self.reported_edge_ev, name="reported_edge_ev")
        observable = str(self.observable_definition).strip()
        if observable not in _ALLOWED_OBSERVABLES:
            raise ValueError(
                "observable_definition must be one of "
                f"{sorted(_ALLOWED_OBSERVABLES)}"
            )
        if observable == "absorption_edge_energy" and edge < 0.0:
            raise ValueError("absorption_edge_energy cannot be negative")
        object.__setattr__(self, "reported_edge_ev", edge)
        object.__setattr__(
            self,
            "reported_standard_uncertainty_ev",
            _optional_nonnegative(
                self.reported_standard_uncertainty_ev,
                name="reported standard uncertainty",
            ),
        )
        object.__setattr__(self, "observable_definition", observable)
        object.__setattr__(
            self,
            "measurement_modality",
            _text(self.measurement_modality, name="measurement modality"),
        )
        method = str(self.extraction_method).strip()
        if method not in _ALLOWED_EXTRACTION_METHODS:
            raise ValueError(
                f"extraction_method must be one of {sorted(_ALLOWED_EXTRACTION_METHODS)}"
            )
        object.__setattr__(self, "extraction_method", method)
        threshold = _optional_nonnegative(
            self.fixed_threshold_cm1,
            name="fixed threshold_cm1",
        )
        if method == "fixed_absorption_threshold" and threshold is None:
            raise ValueError(
                "fixed_absorption_threshold requires fixed_threshold_cm1"
            )
        if threshold is not None and threshold <= 0.0:
            raise ValueError("fixed_threshold_cm1 must be positive")
        if (
            threshold is not None
            and self.analysis_window.absorption_cm1 is not None
            and not (
                self.analysis_window.absorption_cm1[0]
                <= threshold
                <= self.analysis_window.absorption_cm1[1]
            )
        ):
            raise ValueError(
                "fixed_threshold_cm1 must lie inside absorption_cm1 window"
            )
        if (
            observable == "absorption_edge_energy"
            and self.analysis_window.energy_ev is not None
            and self.analysis_window.energy_ev[0] < 0.0
        ):
            raise ValueError(
                "absorption-edge energy window cannot extend below zero"
            )
        object.__setattr__(self, "fixed_threshold_cm1", threshold)

        estimates = tuple(self.sensitivity_estimates)
        if not estimates:
            raise ValueError(
                "at least one same-record sensitivity estimate is required to "
                "define an envelope"
            )
        labels = [estimate.label for estimate in estimates]
        if len(set(labels)) != len(labels):
            raise ValueError("sensitivity estimate labels must be unique")
        if observable == "absorption_edge_energy" and any(
            estimate.edge_ev < 0.0 for estimate in estimates
        ):
            raise ValueError(
                "absorption-edge sensitivity estimates cannot be negative"
            )
        object.__setattr__(self, "sensitivity_estimates", estimates)
        object.__setattr__(
            self,
            "source_doi",
            _text(self.source_doi, name="source DOI"),
        )
        object.__setattr__(
            self,
            "source_locator",
            _text(self.source_locator, name="source locator"),
        )
        evidence = str(self.evidence_class).strip()
        if evidence not in _ALLOWED_EVIDENCE_CLASSES:
            raise ValueError(
                f"evidence_class must be one of {sorted(_ALLOWED_EVIDENCE_CLASSES)}"
            )
        object.__setattr__(self, "evidence_class", evidence)
        if self.notes is not None:
            object.__setattr__(self, "notes", _text(self.notes, name="notes"))


@dataclass(frozen=True)
class EdgeUncertaintyEnvelope:
    central_edge_ev: float
    minimum_edge_ev: float
    maximum_edge_ev: float
    lower_deviation_mev: float
    upper_deviation_mev: float
    span_mev: float
    sensitivity_count: int
    varied_factors: tuple[str, ...]
    factor_envelopes: Mapping[str, Mapping[str, float]]
    reported_standard_uncertainty_ev: float | None
    interpretation: str


def build_edge_uncertainty_envelope(
    observation: AbsorptionEdgeObservation,
) -> EdgeUncertaintyEnvelope:
    central = observation.reported_edge_ev
    all_values = np.asarray(
        [central]
        + [estimate.edge_ev for estimate in observation.sensitivity_estimates],
        dtype=float,
    )
    minimum = float(np.min(all_values))
    maximum = float(np.max(all_values))
    factors = sorted(
        {
            factor
            for estimate in observation.sensitivity_estimates
            for factor in estimate.varied_factors
        }
    )
    factor_envelopes: dict[str, dict[str, float]] = {}
    for factor in factors:
        values = [central] + [
            estimate.edge_ev
            for estimate in observation.sensitivity_estimates
            if factor in estimate.varied_factors
        ]
        factor_minimum = float(np.min(values))
        factor_maximum = float(np.max(values))
        factor_envelopes[factor] = {
            "minimum_edge_ev": factor_minimum,
            "maximum_edge_ev": factor_maximum,
            "lower_deviation_mev": 1000.0 * (central - factor_minimum),
            "upper_deviation_mev": 1000.0 * (factor_maximum - central),
            "span_mev": 1000.0 * (factor_maximum - factor_minimum),
        }
    return EdgeUncertaintyEnvelope(
        central_edge_ev=central,
        minimum_edge_ev=minimum,
        maximum_edge_ev=maximum,
        lower_deviation_mev=1000.0 * (central - minimum),
        upper_deviation_mev=1000.0 * (maximum - central),
        span_mev=1000.0 * (maximum - minimum),
        sensitivity_count=len(observation.sensitivity_estimates),
        varied_factors=tuple(factors),
        factor_envelopes=factor_envelopes,
        reported_standard_uncertainty_ev=(
            observation.reported_standard_uncertainty_ev
        ),
        interpretation=(
            "Same-record model/threshold sensitivity envelope. Reported standard "
            "uncertainty is retained separately and is not combined in quadrature."
        ),
    )


def _observation_dict(
    observation: AbsorptionEdgeObservation,
) -> dict[str, Any]:
    payload = asdict(observation)
    payload["material"] = "Hg1-xCdxTe"
    payload["model_sensitivity_envelope"] = asdict(
        build_edge_uncertainty_envelope(observation)
    )
    return json.loads(json.dumps(payload, sort_keys=True))


def absorption_edge_export_dict(
    observations: Sequence[AbsorptionEdgeObservation],
    *,
    provenance: Mapping[str, Any],
) -> dict[str, Any]:
    records = tuple(observations)
    if not records:
        raise ValueError("absorption edge export requires at least one record")
    ids = [record.record_id for record in records]
    if len(set(ids)) != len(ids):
        raise ValueError("record_id values must be unique")
    return {
        "schema_version": ABSORPTION_EDGE_EXPORT_SCHEMA_VERSION,
        "contract": ABSORPTION_EDGE_EXPORT_CONTRACT,
        "claim_boundary": (
            "Observation metadata and same-record sensitivity only; no universal "
            "edge correction or latent-gap refit is authorized."
        ),
        "provenance": _json_mapping(provenance, name="export provenance"),
        "records": [_observation_dict(record) for record in records],
    }


def save_absorption_edge_export(
    path: str | Path,
    observations: Sequence[AbsorptionEdgeObservation],
    *,
    provenance: Mapping[str, Any],
) -> None:
    payload = absorption_edge_export_dict(observations, provenance=provenance)
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _observation_from_dict(raw: Mapping[str, Any]) -> AbsorptionEdgeObservation:
    return AbsorptionEdgeObservation(
        record_id=raw["record_id"],
        composition=CompositionMetadata(**dict(raw["composition"])),
        temperature=TemperatureMetadata(**dict(raw["temperature"])),
        reported_edge_ev=raw["reported_edge_ev"],
        reported_standard_uncertainty_ev=(
            raw["reported_standard_uncertainty_ev"]
        ),
        observable_definition=raw["observable_definition"],
        measurement_modality=raw["measurement_modality"],
        extraction_method=raw["extraction_method"],
        edge_model=EdgeModel(**dict(raw["edge_model"])),
        analysis_window=AnalysisWindow(
            energy_ev=(
                None
                if raw["analysis_window"]["energy_ev"] is None
                else tuple(raw["analysis_window"]["energy_ev"])
            ),
            absorption_cm1=(
                None
                if raw["analysis_window"]["absorption_cm1"] is None
                else tuple(raw["analysis_window"]["absorption_cm1"])
            ),
        ),
        fixed_threshold_cm1=raw["fixed_threshold_cm1"],
        carrier_state=CarrierState(**dict(raw["carrier_state"])),
        tail_treatment=TailTreatment(**dict(raw["tail_treatment"])),
        sensitivity_estimates=tuple(
            SensitivityEstimate(
                label=item["label"],
                edge_ev=item["edge_ev"],
                varied_factors=tuple(item["varied_factors"]),
                settings=item.get("settings", {}),
            )
            for item in raw["sensitivity_estimates"]
        ),
        source_doi=raw["source_doi"],
        source_locator=raw["source_locator"],
        evidence_class=raw["evidence_class"],
        notes=raw.get("notes"),
    )


def load_absorption_edge_export(
    path: str | Path,
) -> tuple[tuple[AbsorptionEdgeObservation, ...], dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != ABSORPTION_EDGE_EXPORT_SCHEMA_VERSION:
        raise ValueError("unsupported absorption edge export schema_version")
    if payload.get("contract") != ABSORPTION_EDGE_EXPORT_CONTRACT:
        raise ValueError("unexpected absorption edge export contract")
    records = tuple(
        _observation_from_dict(item)
        for item in payload.get("records", [])
    )
    regenerated = absorption_edge_export_dict(
        records,
        provenance=payload.get("provenance", {}),
    )
    if regenerated != payload:
        raise ValueError(
            "stored export does not match normalized contract recomputation"
        )
    return records, dict(payload.get("provenance", {}))
