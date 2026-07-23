from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_PATH = ROOT / "data" / "validation" / "r04_cdsete_phase1_decision.json"
README_PATH = ROOT / "data" / "external" / "cdsete2024" / "README.md"
AUDIT_PATH = ROOT / "literature" / "notes" / "cdsete2024_open_data_audit.md"


def load_decision() -> dict:
    return json.loads(DECISION_PATH.read_text(encoding="utf-8"))


def test_archive_provenance_is_exact() -> None:
    decision = load_decision()
    source = decision["source"]
    provenance = decision["archive_provenance"]

    assert source["article_doi"] == "10.1038/s41467-024-52889-z"
    assert source["dataset_doi"] == "10.5281/zenodo.13869384"
    assert source["license"] == "CC-BY-4.0"
    assert provenance["integrity_pass"] is True
    assert provenance["zenodo_md5"] == "1401ee9b5372edb78f888d152940fc79"
    assert provenance["observed_md5"] == provenance["zenodo_md5"]
    assert provenance["observed_sha256"] == (
        "cc3e1ce1a02266da2d0e0f301464a9d8a519855f33a597adeb7f16048684c9a6"
    )
    assert provenance["archive_member_count"] == 61


def test_primary_field_is_frozen_and_complete() -> None:
    field = load_decision()["predeclared_primary_field"]

    assert field["path"] == "Datasets/Figure 3e.csv"
    assert field["article_panel"] == "Figure 3e"
    assert field["observable"] == "Gaussian-fitted photoluminescence peak wavelength"
    assert field["observable_units"] == "nm"
    assert field["map_shape"] == [24, 24]
    assert field["x_range_micrometre"] == [0.0, 12.545]
    assert field["y_range_micrometre"] == [0.0, 12.545]
    assert field["missing_value_count"] == 0
    assert field["primary_field_frozen_before_multiscale_results"] is True


def test_raw_cube_and_native_psf_are_not_promoted() -> None:
    decision = load_decision()
    content = decision["archive_content_decision"]
    instrument = decision["instrument_contract"]

    assert content["raw_per_pixel_pl_spectral_cube_present"] is False
    assert content["source_data_derived_pl_maps_present"] is True
    assert content["physical_coordinate_axes_present"] is True
    assert content["measured_native_sample_plane_psf_present"] is False
    assert content["repeat_maps_of_same_region_present"] is False
    assert instrument["native_psf_measured"] is False
    assert instrument["numerical_spot_diameter_reported"] is False
    assert instrument["native_effective_kernel_bounded"] is False


def test_phase_two_is_restricted_go_only() -> None:
    decision = load_decision()
    authorization = decision["phase_2_authorization"]
    prohibited = set(authorization["prohibited"])

    assert decision["decision"] == "RESTRICTED_GO"
    assert authorization["authorized"] is True
    assert authorization["mode"] == "restricted pixel-space and added-kernel demonstration"
    assert "HgCdTe experimental validation" in prohibited
    assert "physical deconvolution of the unmeasured native sample-plane kernel" in prohibited
    assert "treating numerically smoothed maps as independent physical measurements" in prohibited
    assert "manuscript authorization" in prohibited
    assert decision["headline"]["hgcdte_external_validation"] == "blocked"


def test_required_documents_exist_and_preserve_claim_boundary() -> None:
    assert README_PATH.is_file()
    assert AUDIT_PATH.is_file()

    combined = (
        README_PATH.read_text(encoding="utf-8")
        + "\n"
        + AUDIT_PATH.read_text(encoding="utf-8")
    )
    normalized = " ".join(combined.split())
    assert "RESTRICTED_GO" in normalized
    assert "does not contain the raw per-pixel PL spectral cube" in normalized
    assert "must not report a latent physical correlation length" in normalized
    assert "HgCdTe external validation remains `blocked`" in normalized
