from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data/hansen/antcliffe1970_hsc_r07_source_metadata.csv"
SPECIMEN_PATH = ROOT / "data/hansen/antcliffe1970_specimens.csv"
GAP_PATH = ROOT / "data/hansen/antcliffe1970_gap_observations.csv"
PARAMETER_PATH = ROOT / "data/hansen/antcliffe1970_band_parameters.csv"
REFERENCE_PATH = ROOT / "data/validation/antcliffe1970_hsc_r07_audit.json"
INGESTION_PATH = ROOT / "data/hansen/antcliffe1970_hansen_ingestion_candidates.csv"

HC_EV_UM = 1.2398419843320026
A4_NUMERIC_CONSTANT = 6.90e-8


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _ols_intercept_slope(x: list[float], y: list[float]) -> tuple[float, float]:
    x_bar = sum(x) / len(x)
    y_bar = sum(y) / len(y)
    sxx = sum((value - x_bar) ** 2 for value in x)
    sxy = sum((xv - x_bar) * (yv - y_bar) for xv, yv in zip(x, y, strict=True))
    slope = sxy / sxx
    intercept = y_bar - slope * x_bar
    return intercept, slope


def hansen_gap_ev(x: float, temperature_k: float) -> float:
    return (
        -0.302
        + 1.93 * x
        - 0.810 * x**2
        + 0.832 * x**3
        + 5.35e-4 * temperature_k * (1.0 - 2.0 * x)
    )


def build_audit() -> dict[str, Any]:
    metadata = _csv(METADATA_PATH)[0]
    specimens = _csv(SPECIMEN_PATH)
    gaps = {row["observation_id"]: row for row in _csv(GAP_PATH)}
    parameters = {row["parameter_id"]: row for row in _csv(PARAMETER_PATH)}
    ingestion_candidates = {row["candidate_id"]: row for row in _csv(INGESTION_PATH)}

    table_rows = [row for row in specimens if row["source_role"] == "table1_transport_fit"]
    f_oe = [
        1.0 / (float(row["period_delta_inv_h_1e4_oe_inv"]) * 1e-4)
        for row in table_rows
    ]
    mass_ratio = [float(row["effective_mass_ratio_1e3"]) * 1e-3 for row in table_rows]
    y = [value**2 for value in mass_ratio]
    intercept, slope = _ols_intercept_slope(f_oe, y)

    table_mass_edge = math.sqrt(intercept)
    table_ep_ev = A4_NUMERIC_CONSTANT / slope
    table_gap_ev = (
        (2.0 / 3.0)
        * table_ep_ev
        * table_mass_edge
        / (1.0 - table_mass_edge)
    )
    predicted_y = [intercept + slope * value for value in f_oe]
    table_rmse_mass_squared = math.sqrt(
        sum((observed - predicted) ** 2 for observed, predicted in zip(y, predicted_y, strict=True))
        / len(y)
    )

    optical_77 = gaps["ANT70_PC50_77K"]
    wavelength_77_um = float(optical_77["wavelength_um"])
    wavelength_half_width_um = float(optical_77["wavelength_half_width_um"])
    optical_77_ev = HC_EV_UM / wavelength_77_um
    optical_77_lower_ev = HC_EV_UM / (wavelength_77_um + wavelength_half_width_um)
    optical_77_upper_ev = HC_EV_UM / (wavelength_77_um - wavelength_half_width_um)

    optical_4p2 = gaps["ANT70_PC50_4P2K"]
    ratio = float(optical_4p2["wavelength_ratio_to_77k"])
    ratio_implied_4p2_ev = HC_EV_UM / (wavelength_77_um * ratio)
    source_optical_4p2_ev = float(optical_4p2["value_ev"])
    source_transport_gap_ev = float(gaps["ANT70_SDH_KP_GAP"]["value_ev"])

    delta_t = 77.0 - 4.2
    source_reported_optical_slope = (
        optical_77_ev - source_optical_4p2_ev
    ) / delta_t
    ratio_check_slope = (optical_77_ev - ratio_implied_4p2_ev) / delta_t
    transport_to_optical_slope = (optical_77_ev - source_transport_gap_ev) / delta_t
    source_reported_optical_80_ev = (
        optical_77_ev + 3.0 * source_reported_optical_slope
    )
    ratio_check_80_ev = optical_77_ev + 3.0 * ratio_check_slope
    transport_to_optical_80_ev = optical_77_ev + 3.0 * transport_to_optical_slope

    x = float(metadata["nominal_composition_x"])
    hansen_4p2 = hansen_gap_ev(x, 4.2)
    hansen_77 = hansen_gap_ev(x, 77.0)
    hansen_80 = hansen_gap_ev(x, 80.0)

    source_m0 = float(parameters["ANT70_M0"]["value"])
    source_ep = float(parameters["ANT70_EP"]["value"])
    source_eg = float(parameters["ANT70_EG"]["value"])

    return {
        "schema_version": "1.0",
        "source_id": metadata["source_id"],
        "source_pdf_sha256": metadata["source_pdf_sha256"],
        "source_scope": {
            "table1_transport_rows": len(table_rows),
            "named_figure_only_specimens": len(specimens) - len(table_rows),
            "complete_experimental_specimen_count_reported": False,
            "figure_digitization_performed": False,
            "copyrighted_source_committed": False,
        },
        "primary_source_observations": {
            "composition_x": x,
            "composition_spatial_half_width_x": float(
                metadata["composition_variation_half_width_x"]
            ),
            "temperature_range_k": [
                float(metadata["overall_temperature_min_k"]),
                float(metadata["overall_temperature_max_k"]),
            ],
            "maximum_magnetic_field_kg": float(metadata["max_magnetic_field_kg"]),
            "optical_77k": {
                "wavelength_um": wavelength_77_um,
                "wavelength_half_width_um": wavelength_half_width_um,
                "derived_energy_ev": optical_77_ev,
                "derived_energy_interval_ev": [
                    optical_77_lower_ev,
                    optical_77_upper_ev,
                ],
            },
            "optical_4p2k": {
                "source_reported_proxy_ev": source_optical_4p2_ev,
                "source_reported_half_width_ev": float(
                    optical_4p2["value_half_width_ev"]
                ),
                "wavelength_ratio_to_77k": ratio,
                "ratio_implied_energy_ev": ratio_implied_4p2_ev,
            },
            "transport_kp_gap": {
                "source_reported_ev": source_transport_gap_ev,
                "source_reported_half_width_ev": float(
                    gaps["ANT70_SDH_KP_GAP"]["value_half_width_ev"]
                ),
                "measurement_class": gaps["ANT70_SDH_KP_GAP"]["measurement_class"],
            },
        },
        "source_reported_fit": {
            "band_edge_mass_ratio": source_m0,
            "band_edge_mass_half_width": float(parameters["ANT70_M0"]["half_width"]),
            "Ep_ev": source_ep,
            "Ep_half_width_ev": float(parameters["ANT70_EP"]["half_width"]),
            "interaction_gap_ev": source_eg,
            "interaction_gap_half_width_ev": float(parameters["ANT70_EG"]["half_width"]),
            "fit_parameter_covariance_reported": False,
        },
        "rounded_table_reproduction": {
            "method": "ordinary_least_squares_of_mr_squared_vs_inverse_period_using_source_A4_small_mass_approximation",
            "band_edge_mass_ratio": table_mass_edge,
            "Ep_ev": table_ep_ev,
            "interaction_gap_ev": table_gap_ev,
            "mass_squared_rmse": table_rmse_mass_squared,
            "exactly_reproduces_source_reported_parameters": False,
            "interpretation": "Table I contains rounded sample averages and does not expose the underlying approximately fifteen mass determinations per specimen, weighting, or fit covariance.",
        },
        "temperature_lineage": {
            "source_reported_optical_pair_slope_ev_per_k": source_reported_optical_slope,
            "ratio_check_slope_ev_per_k": ratio_check_slope,
            "transport_to_optical_slope_ev_per_k": transport_to_optical_slope,
            "source_reported_optical_pair_normalized_80k_ev": source_reported_optical_80_ev,
            "ratio_check_normalized_80k_ev": ratio_check_80_ev,
            "candidate_ids": sorted(ingestion_candidates),
            "transport_to_optical_normalized_80k_ev": transport_to_optical_80_ev,
            "hansen_source_specific_ingestion_mapping": "unresolved_no_per_marker_source_labels",
            "reason": "Antcliffe reports a 77 K photoconductive threshold, a 4.2 K threshold-derived proxy, and a low-temperature transport-model gap. Hansen labels the study magneto-optical but does not identify which low-temperature value was paired with the 77 K point.",
        },
        "hansen_descriptive_comparison": {
            "independent_validation": False,
            "hansen_gap_4p2k_ev": hansen_4p2,
            "hansen_gap_77k_ev": hansen_77,
            "hansen_gap_80k_ev": hansen_80,
            "residual_hansen_minus_source_optical_proxy_4p2k_ev": (
                hansen_4p2 - source_optical_4p2_ev
            ),
            "residual_hansen_minus_source_transport_gap_4p2k_ev": (
                hansen_4p2 - source_transport_gap_ev
            ),
            "residual_hansen_minus_derived_optical_77k_ev": hansen_77 - optical_77_ev,
            "residual_hansen_minus_source_reported_optical_pair_normalized_80k_ev": (
                hansen_80 - source_reported_optical_80_ev
            ),
            "residual_hansen_minus_ratio_check_normalized_80k_ev": (
                hansen_80 - ratio_check_80_ev
            ),
            "residual_hansen_minus_transport_to_optical_normalized_80k_ev": (
                hansen_80 - transport_to_optical_80_ev
            ),
        },
        "decision": {
            "primary_source_recovered": True,
            "primary_transport_table_reconstructed": True,
            "source_reported_band_parameters_reconstructed": True,
            "hansen_exact_ingestion_mapping_resolved": False,
            "direct_hansen_validation_authorized": False,
            "controlling_decision": "primary_source_recovered_hansen_ingestion_mapping_unresolved",
        },
    }


def render_reference() -> str:
    return json.dumps(build_audit(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    print(render_reference(), end="")


if __name__ == "__main__":
    main()
