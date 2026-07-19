from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IRPT = ROOT / "manuscript/observation_model_uncertainty/irpt"
MAIN = (IRPT / "manuscript.tex").read_text(encoding="utf-8")


def _tex_files() -> list[Path]:
    return sorted(IRPT.rglob("*.tex"))


def _all_tex() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in _tex_files())


def test_irpt_main_file_uses_elsevier_structure() -> None:
    assert r"\documentclass[preprint,12pt]{elsarticle}" in MAIN
    assert r"\journal{Infrared Physics \& Technology}" in MAIN
    assert r"\bibliographystyle{elsarticle-num}" in MAIN
    assert r"\bibliography{references}" in MAIN
    assert r"\begin{frontmatter}" in MAIN
    assert r"\end{frontmatter}" in MAIN


def test_every_irpt_input_exists() -> None:
    for tex_path in _tex_files():
        text = tex_path.read_text(encoding="utf-8")
        for relative in re.findall(r"\\input\{([^}]+)\}", text):
            candidate = Path(relative)
            if candidate.suffix != ".tex":
                candidate = candidate.with_suffix(".tex")
            target = tex_path.parent / candidate
            if not target.exists():
                target = IRPT / candidate
            assert target.exists(), f"missing input {relative} referenced by {tex_path}"


def test_every_citation_key_exists_in_bibtex() -> None:
    tex = _all_tex()
    cited: set[str] = set()
    for group in re.findall(r"\\cite\{([^}]+)\}", tex):
        cited.update(item.strip() for item in group.split(","))
    bib = (IRPT / "references.bib").read_text(encoding="utf-8")
    available = set(re.findall(r"@\w+\{([^,]+),", bib))
    assert cited
    assert cited <= available
    assert available == {
        "Hansen1982",
        "Seiler1990",
        "Laurenti1990",
        "Chu1994",
        "Moazzami2005",
        "Sarusi1989",
        "Yue2006",
    }


def test_all_results_table_inputs_and_labels_exist() -> None:
    results = (IRPT / "sections/03_results.tex").read_text(encoding="utf-8")
    expected = {
        "table1_specimen_provenance": "tab:specimen-provenance",
        "table2_candidate_definitions": "tab:candidate-definitions",
        "table3_edge_ensemble": "tab:edge-ensemble",
        "table4_material_model_comparison": "tab:model-comparison",
        "table5_claim_boundaries": "tab:claim-boundaries",
    }
    for stem, label in expected.items():
        assert rf"\input{{tables/{stem}.tex}}" in results
        table = (IRPT / "tables" / f"{stem}.tex").read_text(encoding="utf-8")
        assert rf"\label{{{label}}}" in table


def test_irpt_placeholders_are_administrative_not_scientific() -> None:
    tex = _all_tex()
    placeholders = re.findall(r"\[([^\]]*(?:required|Required|Insert|Assign)[^\]]*)\]", tex)
    assert placeholders
    allowed_terms = (
        "author",
        "affiliation",
        "postal",
        "telephone",
        "archive",
        "repository url",
        "roles",
        "funding",
        "competing",
        "acknowledgments",
    )
    for placeholder in placeholders:
        lowered = placeholder.lower()
        assert any(term in lowered for term in allowed_terms), placeholder
    forbidden = (
        "verify equation",
        "physics required",
        "result required",
        "citation required",
        "data required",
    )
    assert not any(term in tex.lower() for term in forbidden)


def test_irpt_latex_preserves_core_claim_boundaries() -> None:
    tex = _all_tex().lower()
    for statement in (
        "no single fitted edge is selected",
        "does not establish a preferred universal hgcdte gap equation",
        "not a universal optimal-design proof",
        "no candidate is promoted as a corrected or production edge",
    ):
        assert statement in tex
