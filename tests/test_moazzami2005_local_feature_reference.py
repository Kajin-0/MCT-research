import json
from pathlib import Path

import pytest

from tools.build_moazzami_local_feature_reference import build, write_csv

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_JSON = (
    ROOT / "data/validation/moazzami2005_local_feature_sensitivity_reference.json"
)
REFERENCE_CSV = (
    ROOT / "data/validation/moazzami2005_local_feature_sensitivity_summary.csv"
)
ADDENDUM = (
    ROOT
    / "manuscript/observation_model_uncertainty/local_feature_robustness_addendum.md"
)


def test_compact_reference_regenerates_exactly() -> None:
    expected = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
    assert build(ROOT) == expected


def test_summary_csv_regenerates_byte_for_byte(tmp_path: Path) -> None:
    output = tmp_path / "summary.csv"
    write_csv(output, build(ROOT))
    assert output.read_bytes() == REFERENCE_CSV.read_bytes()


def test_questioned_pair_claim_boundary() -> None:
    result = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
    by_id = {item["specimen_id"]: item for item in result["specimens"]}
    specimen = by_id["moazzami2005_x0.226"]
    pair = specimen["questioned_pair"]
    assert pair["removed_energy_ev"] == [0.196491228, 0.19754386]
    assert pair["pixel_y_reversal"] == 3.0
    assert pair["identified_nominal_max_shift_mev"] == pytest.approx(
        0.11687500000001627
    )
    assert pair["identified_joint_max_shift_mev"] == pytest.approx(
        0.9594410000000053
    )
    assert pair["identified_operator_span_after_pair_deletion_mev"] == pytest.approx(
        5.1218749999999975
    )
    assert (
        pair["identified_joint_max_shift_mev"]
        < pair["identified_operator_span_after_pair_deletion_mev"]
    )
    assert result["decision"]["physical_origin_identified"] is False
    assert result["decision"]["spectrum_correction_authorized"] is False


def test_stress_diagnostic_does_not_erase_operator_dominance() -> None:
    result = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
    assert result["decision"][
        "operator_span_dominance_survives_all_sliding_windows"
    ] is True
    for specimen in result["specimens"]:
        assert specimen["minimum_operator_span_to_hansen_seiler_ratio"] > 19.0


def test_manuscript_addendum_preserves_numerics_and_semantics() -> None:
    text = ADDENDUM.read_text(encoding="utf-8")
    for value in (
        "0.196491228",
        "0.197543860",
        "0.116875 meV",
        "0.959441 meV",
        "4.984",
        "3.385",
        "19.6",
        "19.2",
    ):
        assert value in text
    assert "not a random sample" in text
    assert "No smoothing, interpolation, point replacement" in text
    assert "physical origin" in text
    assert "no correction of the nominal reconstructed trace is warranted" in text.lower()
    assert "Boundary-limited candidates" in text
    assert "two-point reconstruction irregularity" in text
    assert "secondary robustness check" in text
    assert "avoid highlighting" in text
    assert "not as a material feature" in text
    assert "physical `core`" in text
    assert "Full numerical precision is retained in machine-readable records" in text
