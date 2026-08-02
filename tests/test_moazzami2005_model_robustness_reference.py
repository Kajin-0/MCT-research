import json
from pathlib import Path

from tools.build_moazzami_model_robustness_reference import build, write_csv

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_JSON = (
    ROOT / "data/validation/moazzami2005_model_robustness_reference.json"
)
REFERENCE_CSV = ROOT / "data/validation/moazzami2005_model_robustness_summary.csv"


def test_compact_model_robustness_reference_regenerates_exactly() -> None:
    expected = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
    assert build(ROOT) == expected


def test_compact_model_robustness_csv_regenerates_byte_for_byte(
    tmp_path: Path,
) -> None:
    output = tmp_path / "model-robustness.csv"
    write_csv(output, build(ROOT))
    assert output.read_bytes() == REFERENCE_CSV.read_bytes()


def test_compact_reference_preserves_claim_boundaries() -> None:
    result = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
    assert result["decision"][
        "fixed_absorption_coordinates_excluded_from_fitted_model_span"
    ]
    assert result["decision"]["unique_physical_gap_identified"] is False
    assert result["decision"]["universal_hgcdte_claim_authorized"] is False
    by_id = {item["specimen_id"]: item for item in result["specimens"]}
    assert by_id["moazzami2005_x0.226"][
        "maximum_fit_domain_or_weighting_shift_mev"
    ] > 5.7
    assert by_id["moazzami2005_x0.310"][
        "maximum_fit_domain_or_weighting_shift_mev"
    ] > 5.4
    assert by_id["moazzami2005_x0.226"][
        "line_envelope_compatible_nominal_span_mev"
    ] < 3.0
    assert by_id["moazzami2005_x0.310"][
        "line_envelope_compatible_nominal_span_mev"
    ] < 2.2
