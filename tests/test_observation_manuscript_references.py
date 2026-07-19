from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = (
    ROOT
    / "manuscript/observation_model_uncertainty/verified_references.md"
).read_text(encoding="utf-8")

EXPECTED_DOIS = {
    "10.1063/1.330018",
    "10.1116/1.576952",
    "10.1063/1.345119",
    "10.1063/1.356464",
    "10.1007/s11664-005-0019-3",
    "10.1063/1.343102",
    "10.1063/1.2221411",
}


def test_verified_reference_ledger_contains_each_required_doi_once() -> None:
    for doi in EXPECTED_DOIS:
        assert REFERENCES.count(doi) == 1


def test_verified_reference_ledger_preserves_authority_boundaries() -> None:
    required = (
        "strict material-law ranking is not identified",
        "not as a fitted universal correction",
        "boundary-limited fits are not treated as identified edges",
        "Copyrighted source pages and source figures are not redistributed",
        "not a separately published material law",
    )
    for statement in required:
        assert statement in REFERENCES


def test_verified_reference_ledger_covers_manuscript_roles() -> None:
    for heading in (
        "## Material-gap comparators",
        "## Observation models and experimental spectra",
        "## Primary support for observation-state terms",
    ):
        assert heading in REFERENCES
    for role in (
        "Hansen-Schmit-Casselman relation",
        "Published Seiler relation",
        "Laurenti relation",
        "Chu 1994 Kane-region rule",
        "Moazzami 2005 real-spectrum application",
        "Carrier filling and Burstein-Moss shift",
        "Mercury-vacancy influence on the absorption edge",
    ):
        assert role in REFERENCES
