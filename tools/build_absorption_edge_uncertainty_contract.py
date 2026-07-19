#!/usr/bin/env python3
"""Build the reusable absorption edge-uncertainty export from the validated benchmark."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from mct_research.absorption_observation import (
    AbsorptionEdgeObservation,
    AnalysisWindow,
    CarrierState,
    CompositionMetadata,
    EdgeModel,
    SensitivityEstimate,
    TailTreatment,
    TemperatureMetadata,
    absorption_edge_export_dict,
    build_edge_uncertainty_envelope,
    save_absorption_edge_export,
)
from tools.benchmark_absorption_observation_models import analyze as benchmark_analyze


def _record_from_scenario(
    scenario: dict[str, Any],
) -> AbsorptionEdgeObservation:
    x = float(scenario["composition_x"])
    temperature = float(scenario["temperature_k"])
    latent = float(scenario["latent_gap_ev"])
    threshold_bias = scenario["chang_inspired_threshold_bias_mev"]
    central = latent + float(threshold_bias["1500"]) / 1000.0

    estimates: list[SensitivityEstimate] = []
    for threshold in (600, 1000, 1200, 2000):
        estimates.append(
            SensitivityEstimate(
                label=f"fixed_threshold_{threshold}_cm-1",
                edge_ev=(
                    latent
                    + float(threshold_bias[str(threshold)]) / 1000.0
                ),
                varied_factors=("fixed_threshold",),
                settings={"threshold_cm1": threshold},
            )
        )
    for fit_name, result in scenario[
        "chang_inspired_truth_fits"
    ].items():
        estimates.append(
            SensitivityEstimate(
                label=f"fractional_power_fit_{fit_name}",
                edge_ev=float(result["edge_ev"]),
                varied_factors=("model_family",),
                settings={
                    "model": "alpha=A*(E-Eg)^p/E",
                    "fit_variant": fit_name,
                    "fitted_exponent": float(result["exponent"]),
                    "fit_absorption_window_cm1": [600.0, 5000.0],
                },
            )
        )

    return AbsorptionEdgeObservation(
        record_id=(
            f"synthetic_x{x:.2f}_T{temperature:.0f}K_threshold1500"
        ),
        composition=CompositionMetadata(
            value_x=x,
            standard_uncertainty_x=None,
            method="declared synthetic benchmark coordinate",
            status="synthetic_not_measured",
        ),
        temperature=TemperatureMetadata(value_k=temperature),
        reported_edge_ev=central,
        reported_standard_uncertainty_ev=None,
        observable_definition="absorption_edge_energy",
        measurement_modality="synthetic FTIR absorption curve",
        extraction_method="fixed_absorption_threshold",
        fixed_threshold_cm1=1500.0,
        edge_model=EdgeModel(
            name="chang_inspired_urbach_nonparabolic_reference",
            expression=(
                "smooth Urbach tail blended with heavy/light-hole "
                "hyperbolic nonparabolic absorption"
            ),
            parameters={
                "nonparabolic_scale_ev": 0.103,
                "urbach_energy_ev": 0.006,
                "edge_absorption_cm1": 400.0,
                "target_absorption_cm1": 4000.0,
                "target_excess_energy_ev": 0.100,
            },
        ),
        analysis_window=AnalysisWindow(
            energy_ev=(latent - 0.040, latent + 0.150),
            absorption_cm1=(600.0, 5000.0),
        ),
        carrier_state=CarrierState(status="not_applicable"),
        tail_treatment=TailTreatment(
            status="modeled",
            model=(
                "Urbach exponential blended into intrinsic "
                "nonparabolic absorption"
            ),
            parameters={
                "urbach_energy_ev": 0.006,
                "edge_absorption_cm1": 400.0,
            },
        ),
        sensitivity_estimates=tuple(estimates),
        source_doi="10.1063/1.2245220",
        source_locator=(
            "synthetic scenario in "
            "tools/benchmark_absorption_observation_models.py; "
            "source-inspired structure, not a specimen transcription"
        ),
        evidence_class="synthetic_method_benchmark",
        notes=(
            "The provisional HgCdTe gap defines only the latent synthetic "
            "reference. This record demonstrates the export contract and is "
            "not a production uncertainty assignment."
        ),
    )


def build_records() -> tuple[AbsorptionEdgeObservation, ...]:
    benchmark = benchmark_analyze()
    return tuple(
        _record_from_scenario(row)
        for row in benchmark["scenarios"]
    )


def _provenance() -> dict[str, Any]:
    return {
        "generator": "tools.build_absorption_edge_uncertainty_contract",
        "upstream_analysis": (
            "formula-level HgCdTe absorption observation-model benchmark"
        ),
        "upstream_source_dois": [
            "10.1007/s11664-005-0019-3",
            "10.1063/1.2245220",
        ],
        "evidence_class": "synthetic_method_benchmark",
    }


def analyze() -> dict[str, Any]:
    records = build_records()
    export = absorption_edge_export_dict(
        records,
        provenance=_provenance(),
    )
    envelopes = [
        build_edge_uncertainty_envelope(record)
        for record in records
    ]
    return {
        "schema_version": export["schema_version"],
        "contract": export["contract"],
        "record_count": len(records),
        "sensitivity_estimates_per_record": sorted(
            {
                len(record.sensitivity_estimates)
                for record in records
            }
        ),
        "all_records_cover_threshold_and_model_family": all(
            set(envelope.varied_factors)
            == {"fixed_threshold", "model_family"}
            for envelope in envelopes
        ),
        "minimum_envelope_span_mev": min(
            envelope.span_mev for envelope in envelopes
        ),
        "maximum_envelope_span_mev": max(
            envelope.span_mev for envelope in envelopes
        ),
        "maximum_lower_deviation_mev": max(
            envelope.lower_deviation_mev
            for envelope in envelopes
        ),
        "maximum_upper_deviation_mev": max(
            envelope.upper_deviation_mev
            for envelope in envelopes
        ),
        "roundtrip_required_fields": [
            "measurement modality",
            "edge model",
            "analysis window",
            "fixed threshold when used",
            "carrier state",
            "tail treatment",
            "same-record sensitivity estimates",
        ],
        "production_correction_authorized": False,
        "claim_boundary": export["claim_boundary"],
    }


def write_summary_csv(
    path: Path,
    records: tuple[AbsorptionEdgeObservation, ...],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "record_id",
                "composition_x",
                "temperature_k",
                "reported_edge_ev",
                "minimum_edge_ev",
                "maximum_edge_ev",
                "lower_deviation_mev",
                "upper_deviation_mev",
                "span_mev",
                "sensitivity_count",
                "varied_factors",
                "evidence_class",
            ],
        )
        writer.writeheader()
        for record in records:
            envelope = build_edge_uncertainty_envelope(record)
            writer.writerow(
                {
                    "record_id": record.record_id,
                    "composition_x": record.composition.value_x,
                    "temperature_k": record.temperature.value_k,
                    "reported_edge_ev": record.reported_edge_ev,
                    "minimum_edge_ev": envelope.minimum_edge_ev,
                    "maximum_edge_ev": envelope.maximum_edge_ev,
                    "lower_deviation_mev": envelope.lower_deviation_mev,
                    "upper_deviation_mev": envelope.upper_deviation_mev,
                    "span_mev": envelope.span_mev,
                    "sensitivity_count": envelope.sensitivity_count,
                    "varied_factors": ";".join(
                        envelope.varied_factors
                    ),
                    "evidence_class": record.evidence_class,
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path)
    args = parser.parse_args()

    records = build_records()
    save_absorption_edge_export(
        args.output_json,
        records,
        provenance=_provenance(),
    )
    write_summary_csv(args.output_csv, records)
    summary = analyze()
    if args.summary_json is not None:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        args.summary_json.write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
