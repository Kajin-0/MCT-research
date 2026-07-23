from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "data" / "validation" / "r04_manuscript_authorization_review.json"
DECISION_PATH = (
    ROOT
    / "research"
    / "decision_records"
    / "2026-07-23-r04-manuscript-authorization-review.md"
)
STATE_UPDATE_PATH = (
    ROOT
    / "research"
    / "programs"
    / "spatial_disorder"
    / "state_updates"
    / "2026-07-23-manuscript-authorization-review.md"
)


def load_review() -> dict:
    return json.loads(REVIEW_PATH.read_text(encoding="utf-8"))


def test_evidence_chain_is_exact_and_complete() -> None:
    review = load_review()
    evidence = review["evidence_basis"]

    assert review["portfolio_contribution"] == "R04"
    assert review["issue"] == 327
    assert evidence["prior_art_pr"] == 223
    assert evidence["prior_art_merge_commit"] == (
        "7e9f8295af66800fdaf1c7da1ad505ff3c6bce40"
    )
    assert evidence["public_data_pr"] == 308
    assert evidence["public_data_merge_commit"] == (
        "ad705f13995ae0eb42ec1ad72ab6ecac470ba226"
    )
    assert evidence["source_qualification_pr"] == 319
    assert evidence["source_qualification_merge_commit"] == (
        "75d2d84acd2d778b5e4ba922b20b2cf3879b4b18"
    )
    assert evidence["real_data_pr"] == 326
    assert evidence["real_data_merge_commit"] == (
        "c706da20115ae193aae1af460dca5e6962e39a09"
    )


def test_decision_authorizes_drafting_not_submission() -> None:
    review = load_review()
    authorization = review["authorization"]

    assert review["decision"] == "AUTHORIZE_RESTRICTED_MANUSCRIPT"
    assert authorization["outline_and_figure_planning"] is True
    assert authorization["restricted_manuscript_drafting"] is True
    assert authorization["submission"] is False
    assert authorization["submission_requires_separate_final_claim_audit"] is True
    assert authorization["new_R04_mechanism"] is False
    assert authorization["new_external_data_search"] is False
    assert authorization["HgCdTe_validation_claim"] is False
    assert authorization["physical_correlation_length_claim"] is False
    assert authorization["covariance_family_selection"] is False
    assert authorization["R05"] is False


def test_prior_art_and_candidate_contribution_are_separated() -> None:
    review = load_review()
    matrix = {entry["topic"]: entry for entry in review["claim_matrix"]}

    prior_art = matrix["finite_aperture_hgcdte_mapping_and_spatial_variation"]
    assert prior_art["classification"] == "established_prior_art"
    assert prior_art["novelty_claim_authorized"] is False

    gaussian = matrix["Gaussian_covariance_filtering_identity"]
    assert gaussian["classification"].startswith("established_mathematics")
    assert gaussian["novelty_claim_authorized"] == (
        "application_and_integrated_consequence_only"
    )

    scale_floor = matrix["absolute_probe_scale_calibration_floor"]
    assert scale_floor["classification"] == "candidate_distinct_integrated_R04_result"
    assert scale_floor["novelty_claim_authorized"] == (
        "candidate_not_exhaustive_guarantee"
    )

    blocked = matrix["HgCdTe_specimen_covariance_family_or_physical_correlation_length"]
    assert blocked["classification"] == "blocked"
    assert blocked["novelty_claim_authorized"] is False


def test_second_dataset_is_not_required_or_automatically_authorized() -> None:
    decision = load_review()["second_dataset_decision"]

    assert decision["required_before_drafting"] is False
    assert decision["automatic_search_authorized"] is False
    assert decision["large_multigigabyte_acquisition_authorized"] is False
    assert "would not resolve the blocked HgCdTe validation" in decision["reason"]


def test_four_result_and_four_figure_scope_ceiling() -> None:
    review = load_review()

    assert len(review["minimum_main_text_result_set"]) == 4
    assert len(review["main_figure_plan"]) == 4
    assert [figure["figure"] for figure in review["main_figure_plan"]] == [1, 2, 3, 4]
    claim = review["one_sentence_contribution_claim"].lower()
    assert "finite field of view" in claim
    assert "same-raster cross-scale dependence" in claim
    assert "HgCdTe" in review["provisional_title"]


def test_reviewer_risks_preserve_fatal_claim_boundaries() -> None:
    review = load_review()
    risks = {entry["risk"]: entry for entry in review["reviewer_risks"]}

    validation = risks["no_qualifying_HgCdTe_external_validation"]
    assert "fatal_for_material_validation_claim" in validation["disposition"]

    psf = risks["native_sample_plane_PSF_is_unmeasured"]
    assert "fatal_for_physical_correlation_length" in psf["disposition"]

    scope = risks["scope_is_too_broad"]
    assert scope["disposition"] == "requires_strict_scope_reduction"


def test_unsupported_claims_are_explicit() -> None:
    unsupported = set(load_review()["unsupported_claims_box"])

    assert "HgCdTe_or_CdSeTe_physical_correlation_length" in unsupported
    assert "universal_Gaussian_or_Matern_covariance_family" in unsupported
    assert "composition_assignment_from_PL_peak_wavelength" in unsupported
    assert "independent_validation_from_numerically_smoothed_scales" in unsupported
    assert "R05_random_mass_or_topological_conclusion" in unsupported


def test_decision_and_state_documents_exist_and_match() -> None:
    assert DECISION_PATH.is_file()
    assert STATE_UPDATE_PATH.is_file()

    text = " ".join(
        (
            DECISION_PATH.read_text(encoding="utf-8")
            + "\n"
            + STATE_UPDATE_PATH.read_text(encoding="utf-8")
        ).split()
    )
    assert "AUTHORIZE_RESTRICTED_MANUSCRIPT" in text
    assert "restricted manuscript drafting authorized" in text
    assert "manuscript submission not authorized" in text
    assert "HgCdTe external validation blocked" in text
    assert "R05 inactive" in text
