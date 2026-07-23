from pathlib import Path

from tools.audit_moazzami2005_local_feature_sensitivity import analyze

ROOT = Path(__file__).resolve().parents[1]


def _result() -> dict:
    return analyze(ROOT)


def test_audit_is_systematic_and_noncorrective() -> None:
    result = _result()
    assert result["decision"]["specimen_count"] == 2
    assert result["method"]["point_replacement"] == "forbidden"
    assert result["method"]["smoothing"] == "forbidden"
    assert result["method"]["probability_semantics"].startswith("none")
    assert result["decision"]["physical_origin_identified"] is False
    assert result["decision"]["spectrum_correction_authorized"] is False


def test_every_contiguous_one_three_and_five_point_window_is_evaluated() -> None:
    for specimen in _result()["specimens"]:
        assert specimen["window_sizes_samples"] == [1, 3, 5]
        n = specimen["fit_point_count"]
        expected = sum(n - width + 1 for width in (1, 3, 5))
        assert len(specimen["all_window_scenarios"]) == expected
        assert specimen["decision"]["all_contiguous_windows_audited"] is True


def test_boundary_limited_candidates_are_not_certified_as_stable() -> None:
    for specimen in _result()["specimens"]:
        assert specimen["boundary_limited_candidate_ids"]
        assert specimen["identified_candidate_ids"]
        assert set(specimen["boundary_limited_candidate_ids"]).isdisjoint(
            specimen["identified_candidate_ids"]
        )
        assert (
            specimen["decision"][
                "boundary_limited_candidates_used_for_stability_certification"
            ]
            is False
        )


def test_visible_figure6a_irregularity_is_source_pixel_grounded() -> None:
    specimens = {item["specimen_id"]: item for item in _result()["specimens"]}
    reversals = specimens["moazzami2005_x0.226"][
        "raw_source_pixel_monotonicity_reversals"
    ]
    assert any(
        0.196 < row["left_energy_ev"] < 0.199
        and 0.196 < row["right_energy_ev"] < 0.199
        and row["pixel_y_reversal"] > 0.0
        for row in reversals
    )


def test_feature_windows_are_combined_with_all_four_coordinate_corners() -> None:
    for specimen in _result()["specimens"]:
        assert (
            specimen["decision"][
                "coordinate_corners_combined_with_source_pixel_reversal_windows"
            ]
            is True
        )
        for record in specimen["feature_joint_coordinate_records"]:
            assert len(record["coordinate_corners"]) == 4
            assert {
                (row["energy_sign"], row["absorption_sign"])
                for row in record["coordinate_corners"]
            } == {(-1, -1), (-1, 1), (1, -1), (1, 1)}


def test_output_is_deterministic() -> None:
    assert analyze(ROOT) == analyze(ROOT)
