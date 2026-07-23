import json
from pathlib import Path

from tools.build_moazzami_local_feature_reference import build, write_csv

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_JSON = (
    ROOT / "data/validation/moazzami2005_local_feature_sensitivity_reference.json"
)
REFERENCE_CSV = (
    ROOT / "data/validation/moazzami2005_local_feature_sensitivity_summary.csv"
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
    assert pair["identified_nominal_max_shift_mev"] < 1.0
    assert pair["identified_joint_max_shift_mev"] < 1.0
    assert result["decision"]["physical_origin_identified"] is False
    assert result["decision"]["spectrum_correction_authorized"] is False


def test_stress_diagnostic_does_not_erase_operator_dominance() -> None:
    result = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
    assert result["decision"][
        "operator_span_dominance_survives_all_sliding_windows"
    ] is True
    for specimen in result["specimens"]:
        assert specimen["minimum_operator_span_to_hansen_seiler_ratio"] > 19.0
