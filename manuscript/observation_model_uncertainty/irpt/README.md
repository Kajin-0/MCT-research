# Infrared Physics & Technology submission package

This directory contains the editable Elsevier LaTeX version of the manuscript and the standalone submission files required for the selected target journal.

## Package contents

- `manuscript.tex` — main `elsarticle` entry point.
- `frontmatter.tex` — title, fail-closed author placeholders, 222-word abstract, and seven keywords.
- `sections/` — numbered introduction, methods, results, discussion, limitations, and conclusions.
- `tables/` — five editable LaTeX tables generated from the frozen CSV records.
- `references.bib` — seven verified primary references in BibTeX format.
- `declarations.tex` — data, CRediT, funding, conflict, acknowledgment, and AI declarations.
- `highlights.txt` — five standalone submission highlights, each no longer than 85 characters.
- `cover_letter.md` — fail-closed cover-letter draft.
- `figures/` — created during the PDF workflow from the frozen SVG figures; generated PDFs are not authoritative source data.

## Regenerate editable tables

From the repository root:

```bash
python -m tools.build_observation_model_irpt_tables \
  --repository-root . \
  --output-dir manuscript/observation_model_uncertainty/irpt/tables
```

Repository tests require byte-for-byte equality between a fresh table build and the committed table files.

## Compile locally

A TeX Live installation containing `elsarticle`, `latexmk`, `booktabs`, `longtable`, `siunitx`, and standard graphics packages is required. Convert the frozen SVG figures to PDF without changing their view boxes, then run:

```bash
cd manuscript/observation_model_uncertainty/irpt
latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode manuscript.tex
```

The GitHub workflow `.github/workflows/irpt-latex-manuscript.yml` performs the conversion and compilation in TeX Live 2026 and retains the PDF, log, bibliography log, metadata, and SHA-256 evidence.

## Authority hierarchy

1. Frozen CSV records and machine-readable analysis summaries control numerical claims.
2. Frozen SVG files control figure content.
3. Generated LaTeX tables must reproduce byte-for-byte from the CSV records.
4. `verified_references.md` controls bibliographic identity and authority limits.
5. The LaTeX manuscript controls journal formatting and cross-references, but may not broaden the scientific claim boundary.

## Remaining human inputs

Do not remove the fail-closed placeholders until these values are confirmed:

- final author order and affiliations;
- corresponding-author contact details;
- CRediT roles;
- funding statement;
- competing-interest declaration;
- acknowledgments;
- public archive DOI or final repository URL;
- suggested reviewers after conflict checks;
- confirmation of originality, author approval, and exclusive submission.
