from pathlib import Path

from tools.audit_moazzami2005_pixel_reversal_core import analyze

ROOT = Path(__file__).resolve().parents[1]
RESULT = analyze(ROOT)


def test_core_definition_is_source_coordinate_based_and_noncorrective() -> None:
    assert RESULT["method"]["deletion"] == "exact two-coordinate pair"
    assert RESULT["method"]["smoothing_interpolation_or_replacement"] == "forbidden"
    assert RESULT["decision"]["physical_origin_identified"] is False
    assert RESULT["decision"]["spectrum_correction_authorized"] is False


def test_questioned_figure6a_pair_is_present() -> None:
    specimens = {item["specimen_id"]: item for item in RESULT["specimens"]}
    rows = specimens["moazzami2005_x0.226"]["pixel_reversal_pairs"]
    assert any(
        0.196 < row["removed_energy_ev"][0] < 0.199
        and 0.196 < row["removed_energy_ev"][1] < 0.199
        and row["pixel_y_reversal"] == 3.0
        for row in rows
    )


def test_every_pair_has_four_coordinate_corners_and_no_boundary_certification() -> None:
    for specimen in RESULT["specimens"]:
        assert set(specimen["boundary_limited_candidate_ids"]).isdisjoint(
            specimen["identified_candidate_ids"]
        )
        for row in specimen["pixel_reversal_pairs"]:
            assert len(row["coordinate_corners"]) == 4
            assert {
                (corner["energy_sign"], corner["absorption_sign"])
                for corner in row["coordinate_corners"]
            } == {(-1, -1), (-1, 1), (1, -1), (1, 1)}
            assert row["decision"]["physical_origin_identified"] is False
            assert row["decision"]["spectrum_correction_authorized"] is False
