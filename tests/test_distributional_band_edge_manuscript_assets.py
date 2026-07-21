from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "distributional_band_edge"

REQUIRED_ASSETS = (
    "README.md",
    "manuscript_draft.md",
    "theorem_index.md",
    "claim_matrix.md",
    "figure_plan.md",
    "figure_manifest.json",
    "submission_gap.md",
)

REQUIRED_DOIS = (
    "10.1016/0038-1098(85)90315-1",
    "10.1007/s11664-007-0162-0",
    "10.1063/1.2245220",
    "10.1016/0022-0248(92)90851-9",
    "10.1016/j.physb.2009.08.210",
    "10.1038/ncomms12576",
    "10.1016/0020-0891(91)90110-2",
)


def load_json(relative_path: str) -> dict[str, object]:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def test_required_manuscript_assets_exist() -> None:
    missing = [name for name in REQUIRED_ASSETS if not (MANUSCRIPT / name).is_file()]
    assert missing == []


def test_theorem_index_has_stable_labels() -> None:
    text = (MANUSCRIPT / "theorem_index.md").read_text(encoding="utf-8")
    for label in (
        "Proposition 1",
        "Proposition 2",
        "Proposition 3",
        "Theorem 1",
        "Theorem 2",
        "Proposition 4",
        "Proposition 5",
        "Theorem 3",
        "Theorem 4",
        "Corollary",
    ):
        assert label in text


def test_claim_matrix_covers_all_declared_claims() -> None:
    text = (MANUSCRIPT / "claim_matrix.md").read_text(encoding="utf-8")
    for index in range(1, 24):
        assert f"C{index:02d}" in text
    assert "External material validation" in text
    assert "Partial / submission blocker" in text
    assert "calibrated native spectrum and covariance remain absent" in text


def test_submission_gap_contains_priority_doi_queue() -> None:
    text = (MANUSCRIPT / "submission_gap.md").read_text(encoding="utf-8")
    for doi in REQUIRED_DOIS:
        assert doi in text


def test_figure_manifest_references_existing_records_and_public_functions() -> None:
    manifest = load_json(
        "manuscript/distributional_band_edge/figure_manifest.json"
    )
    figures = manifest["figures"]
    assert isinstance(figures, list)
    assert len(figures) == 7
    assert len({figure["id"] for figure in figures}) == 7

    package = importlib.import_module("mct_research")
    for figure in figures:
        assert figure["external_validation"] is False
        assert figure["claim_ids"]
        assert figure["panels"]
        for record in figure["data_records"]:
            assert (ROOT / record).exists(), record
        for dotted_name in figure["public_functions"]:
            module_name, attribute = dotted_name.rsplit(".", 1)
            assert module_name == "mct_research"
            assert hasattr(package, attribute), dotted_name


def test_immutable_headline_values_match_manuscript_claims() -> None:
    transition = load_json(
        "data/validation/near_critical_transition_model_dependence.json"
    )
    assert transition["cross_model_results"][
        "central_critical_temperature_span_k"
    ] == pytest.approx(25.08027521699574)

    herrmann = load_json(
        "data/validation/herrmann_gaussian_tail_reproduction.json"
    )
    assert herrmann["derived_results"][
        "square_root_source_window_tail_energy_over_s"
    ] == pytest.approx(0.5050415592942678)
    assert herrmann["derived_results"][
        "fit_window_increase_fraction"
    ] == pytest.approx(0.6012644844884396)

    chang = load_json(
        "data/validation/chang_2006_cutoff_identifiability.json"
    )
    assert chang["thickness_results"][
        "source_valid_5_to_20_um_energy_shift_mev"
    ] == pytest.approx(-16.63553233343869)
    assert chang["all_tail_design"]["numerical_rank"] == 2
    assert chang["mixed_branch_design"]["numerical_rank"] == 4

    carrier = load_json(
        "data/validation/dingrong_1985_carrier_filling_sensitivity.json"
    )
    assert carrier["dingrong_density_result"][
        "parabolic_overestimate_ev"
    ] == pytest.approx(0.1473228243338829)
    assert carrier["five_density_identifiability_design"][
        "condition_number"
    ] == pytest.approx(11034.748776227327)

    unified = load_json(
        "data/validation/unified_spectrum_structural_rank.json"
    )
    assert unified["exact_counterexample"][
        "maximum_absolute_response_difference"
    ] == pytest.approx(2.220446049250313e-16)
    assert unified["unmarked_dense_spectrum"]["numerical_rank"] == 3
    assert unified["nontranslational_carrier_marker"]["numerical_rank"] == 4


def test_manuscript_preserves_submission_boundary() -> None:
    draft = (MANUSCRIPT / "manuscript_draft.md").read_text(encoding="utf-8")
    readme = (MANUSCRIPT / "README.md").read_text(encoding="utf-8")
    for text in (draft, readme):
        assert "external" in text.lower()
        assert "validation" in text.lower()
    assert "not a fit to the Dingrong specimen" in draft
    assert "not the Dingrong free-carrier absorption law" in draft
