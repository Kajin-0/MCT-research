from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental"
GATE_PATH = DATA / "scott1969_figure2_extraction_gate.csv"
README_PATH = DATA / "scott1969_figure2_extraction_README.md"
DIGITIZED_PATH = DATA / "scott1969_figure2_digitized.csv"
CALIBRATION_PATH = DATA / "scott1969_figure2_calibration.csv"

PDF_SHA = "7b2e5790745897ecd75bd22134e5d9293397820c3b7851eb5a9e648a5c441324"
PAGE_SHA = "1fbdea6692eec2f411b8dd0b01cddb02d46e426066cb140a87fc6ee4af63d694"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_gate_authorizes_only_figure2_direct_markers() -> None:
    rows = {row["record_id"]: row for row in _read(GATE_PATH)}
    assert set(rows) == {"SCOTT69_F2", "SCOTT69_F5"}
    assert rows["SCOTT69_F2"]["role"] == "direct_marker_source"
    assert rows["SCOTT69_F2"]["page_asset_status"] == (
        "uploaded_pdf_rendered_600dpi_with_immutable_hash"
    )
    assert rows["SCOTT69_F2"]["numerical_rows_authorized"] == "true"
    assert rows["SCOTT69_F5"]["role"] == "provenance_cross_check_only"
    assert rows["SCOTT69_F5"]["status"] == "rejected_as_independent_dataset"
    assert rows["SCOTT69_F5"]["numerical_rows_authorized"] == "false"


def test_materialized_source_and_calibration_contract() -> None:
    rows = _read(CALIBRATION_PATH)
    assert len(rows) == 17
    assert {row["source_pdf_sha256"] for row in rows} == {PDF_SHA}
    assert {row["page_image_sha256"] for row in rows} == {PAGE_SHA}
    assert {row["renderer"] for row in rows} == {"pypdfium2"}
    assert {row["renderer_version"] for row in rows} == {"5.8.0"}
    assert {row["render_dpi"] for row in rows} == {"600"}
    assert {row["page_image_width_px"] for row in rows} == {"4900"}
    assert {row["page_image_height_px"] for row in rows} == {"6580"}
    assert {row["pdf_page_number"] for row in rows} == {"4"}
    assert {row["article_page"] for row in rows} == {"4079"}

    by_axis: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_axis[row["axis"]].append(row)

    assert {float(row["source_tick_value"]) for row in by_axis["temperature"]} == {
        0.0,
        40.0,
        80.0,
        120.0,
        160.0,
        200.0,
        240.0,
        280.0,
    }
    assert {float(row["source_tick_value"]) for row in by_axis["fixed_alpha_edge_energy"]} == {
        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
    }

    temp = by_axis["temperature"][0]
    energy = by_axis["fixed_alpha_edge_energy"][0]
    assert float(temp["axis_fit_max_abs_residual"]) < 0.52
    assert float(temp["axis_fit_rmse"]) < 0.26
    assert float(energy["axis_fit_max_abs_residual"]) < 0.00164
    assert float(energy["axis_fit_rmse"]) < 0.00085
    assert all("Equation (3) not used" in row["notes"] for row in rows)


def test_direct_marker_ledger_has_exact_series_counts() -> None:
    rows = _read(DIGITIZED_PATH)
    assert len(rows) == 70
    assert len({row["marker_id"] for row in rows}) == 70
    counts = Counter(row["specimen_label"] for row in rows)
    assert counts == {
        "61": 8,
        "53": 6,
        "46": 9,
        "40.5": 8,
        "38.5": 8,
        "35": 8,
        "31": 8,
        "25": 7,
        "23": 8,
    }


def test_marker_values_reproduce_the_tick_calibration() -> None:
    calibration = _read(CALIBRATION_PATH)
    fits = {}
    for axis in {"temperature", "fixed_alpha_edge_energy"}:
        row = next(item for item in calibration if item["axis"] == axis)
        fits[axis] = (
            float(row["axis_fit_slope_per_pixel"]),
            float(row["axis_fit_intercept"]),
        )

    t_slope, t_intercept = fits["temperature"]
    e_slope, e_intercept = fits["fixed_alpha_edge_energy"]

    for row in _read(DIGITIZED_PATH):
        x = float(row["rectified_pixel_x"])
        y = float(row["rectified_pixel_y"])
        assert math.isclose(
            float(row["temperature_k"]),
            t_slope * x + t_intercept,
            abs_tol=0.0011,
        )
        assert math.isclose(
            float(row["fixed_alpha_edge_ev"]),
            e_slope * y + e_intercept,
            abs_tol=5.1e-7,
        )


def test_observation_and_uncertainty_semantics_are_fail_closed() -> None:
    rows = _read(DIGITIZED_PATH)
    assert {row["measurement_class"] for row in rows} == {
        "fixed_absorption_optical_edge_alpha_500_cm_inverse"
    }
    assert {row["signed_gap_eligible"] for row in rows} == {"false"}
    assert {
        row["intrinsic_gap_eligible_without_observation_operator"] for row in rows
    } == {"false"}
    assert {row["pointwise_experimental_covariance"] for row in rows} == {
        "not_reported"
    }
    assert {row["pixel_half_width_x"] for row in rows} == {"6"}
    assert {row["pixel_half_width_y"] for row in rows} == {"6"}
    assert {row["temperature_extraction_half_width_k"] for row in rows} == {
        "1.75"
    }
    assert {row["energy_extraction_half_width_ev"] for row in rows} == {
        "0.0047"
    }


def test_marker_ranges_and_shared_specimen_groups() -> None:
    rows = _read(DIGITIZED_PATH)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["specimen_label"]].append(row)
        assert 0.0 <= float(row["temperature_k"]) <= 300.0
        assert 0.0 <= float(row["fixed_alpha_edge_ev"]) <= 0.8
        assert 2750.0 <= float(row["pixel_x"]) <= 4700.0
        assert 450.0 <= float(row["pixel_y"]) <= 2600.0
        assert row["visibility_status"] == (
            "direct_x_marker_center_visually_separable"
        )
        assert row["marker_assignment_basis"] == (
            "direct_marker_center_only_not_connecting_line_or_equation"
        )

    for label, series_rows in grouped.items():
        assert len({row["shared_specimen_group"] for row in series_rows}) == 1
        temperatures = [float(row["temperature_k"]) for row in series_rows]
        assert temperatures == sorted(temperatures)
        assert len(temperatures) == len(set(temperatures))


def test_source_quality_flags_are_preserved() -> None:
    rows = _read(DIGITIZED_PATH)
    flags = {
        label: {row["source_quality_flag"] for row in rows if row["specimen_label"] == label}
        for label in {"25", "38.5", "53", "61"}
    }
    assert flags["25"] == {
        "high_residual_absorption_attributed_mainly_to_inhomogeneity"
    }
    assert flags["38.5"] == {
        "kinked_absorption_edge_attributed_to_compositional_nonuniformity"
    }
    assert flags["53"] == {
        "kinked_absorption_edge_attributed_to_compositional_nonuniformity"
    }
    assert flags["61"] == {
        "outside_equation3_stated_x_le_0p6_range_but_directly_measured"
    }


def test_readme_records_hashes_counts_and_figure5_restrictions() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    required = {
        PDF_SHA,
        PAGE_SHA,
        "70 direct markers",
        "sample an Equation (3) curve as data",
        "add Figure 5 markers as independent observations",
        "replace a density-measured composition with a fit-required value",
        "Coordinate-extraction bounds",
        "They are not source measurement covariance",
        "pointwise_experimental_covariance = not_reported",
    }
    missing = sorted(item for item in required if item not in text)
    assert not missing, f"missing Scott digitization statements: {missing}"
