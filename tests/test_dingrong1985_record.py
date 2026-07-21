from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from mct_research.dingrong1985 import (
    DINGRONG_ELECTRON_DENSITY_CM3,
    DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM,
    audit_momentum_matrix,
    reproduce_table,
)

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "validation" / "dingrong1985_table1_reproduction.json"
DISPOSITION = (
    ROOT
    / "literature"
    / "acquisition"
    / "2026-07-21-obtained-source-disposition.json"
)


def test_record_matches_executable_source_reproduction() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    rows = record["source_table"]
    temperatures = [row["temperature_k"] for row in rows]
    gaps = [row["bandgap_ev"] for row in rows]
    source_shifts = [row["source_fermi_shift_ev"] for row in rows]
    source_energies = [row["source_fermi_energy_ev"] for row in rows]
    source_optical = [row["source_optical_gap_ev"] for row in rows]

    printed = reproduce_table(
        temperatures_k=temperatures,
        bandgaps_ev=gaps,
        source_fermi_shifts_ev=source_shifts,
        source_fermi_energies_ev=source_energies,
        source_optical_gaps_ev=source_optical,
        momentum_matrix_ev_cm=DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM,
        electron_density_cm3=DINGRONG_ELECTRON_DENSITY_CM3,
    )
    np.testing.assert_allclose(
        [point.reproduced_fermi_shift_ev for point in printed.points],
        record["printed_parameter_reproduction"]["reproduced_fermi_shifts_ev"],
        rtol=0.0,
        atol=2.0e-9,
    )
    np.testing.assert_allclose(
        printed.shift_rms_error_ev * 1000.0,
        record["printed_parameter_reproduction"]["shift_rms_error_mev"],
        rtol=0.0,
        atol=2.0e-6,
    )

    audit = audit_momentum_matrix(
        temperatures_k=temperatures,
        bandgaps_ev=gaps,
        source_fermi_shifts_ev=source_shifts,
        electron_density_cm3=DINGRONG_ELECTRON_DENSITY_CM3,
    )
    np.testing.assert_allclose(
        audit.row_implied_values_ev_cm,
        record["row_implied_parameter_audit"][
            "row_implied_momentum_matrices_ev_cm"
        ],
        rtol=0.0,
        atol=2.0e-17,
    )
    np.testing.assert_allclose(
        audit.mean_ev_cm,
        record["row_implied_parameter_audit"]["mean_momentum_matrix_ev_cm"],
        rtol=0.0,
        atol=2.0e-17,
    )

    implied = reproduce_table(
        temperatures_k=temperatures,
        bandgaps_ev=gaps,
        source_fermi_shifts_ev=source_shifts,
        source_fermi_energies_ev=source_energies,
        source_optical_gaps_ev=source_optical,
        momentum_matrix_ev_cm=audit.mean_ev_cm,
        electron_density_cm3=DINGRONG_ELECTRON_DENSITY_CM3,
    )
    np.testing.assert_allclose(
        implied.shift_rms_error_ev * 1000.0,
        record["row_implied_mean_reproduction"]["shift_rms_error_mev"],
        rtol=0.0,
        atol=2.0e-5,
    )
    assert record["external_source_table_reproduction_complete"] is True
    assert record["external_material_validation_complete"] is False


def test_obtained_source_disposition_records_all_three_user_files() -> None:
    disposition = json.loads(DISPOSITION.read_text(encoding="utf-8"))
    sources = disposition["sources"]
    assert {source["doi"] for source in sources} == {
        "10.1016/0038-1098(85)90315-1",
        "10.1007/s11664-007-0162-0",
        "10.1063/1.2245220",
    }
    assert all(len(source["sha256"]) == 64 for source in sources)
    assert all(
        source["rights"] == "publisher_restricted_notes_only"
        for source in sources
    )
    assert disposition["route_disposition"]["chang_multi_thickness_cutoff"][
        "status"
    ] == "rejected_from_published_papers"
    assert disposition["route_disposition"]["dingrong_table1_carrier_edge"][
        "status"
    ] == "active"
    assert disposition["external_material_validation_complete"] is False
