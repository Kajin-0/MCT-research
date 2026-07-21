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
    assert "raw-spectrum validation incomplete" in text


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
    assert transition["cross_model_results"]["central_temperature_span_k"] == pytest.approx(
        25.080275431
    )

    herrmann = load_json(
        "data/validation/herrmann_gaussian_tail_reproduction.json"
    )
    source_fit = herrmann["source_aligned_reproduction"]
    assert source_fit["w_over_s"] == pytest.approx(0.505039046)
    sensitivity = herrmann["fit_window_sensitivity"]
    assert sensitivity["relative_change_source_to_upper"] == pytest.approx(
        0.601291362
    )

    chang = load_json(
        "data/validation/chang_2006_cutoff_identifiability.json"
    )
    shifts = chang["thickness_shift_demo"]
    assert shifts["energy_shift_mev"] == pytest.approx(-16.635532333)
    assert shifts["wavelength_shift_um"] == pytest.approx(2.493666494)

    carrier = load_json(
        "data/validation/dingrong_1985_carrier_filling_sensitivity.json"
    )
    declared = carrier["declared_density_point"]
    assert declared["parabolic_overestimate_mev"] == pytest.approx(147.323063)

    unified = load_json(
        "data/validation/unified_spectrum_structural_rank.json"
    )
    assert unified["unmarked_spectrum"]["numerical_rank"] == 3
    assert unified["exact_counterexample"]["max_absolute_difference"] <= 2.22e-16
    assert unified["marked_spectrum"]["numerical_rank"] == 4
