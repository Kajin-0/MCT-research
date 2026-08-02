# Strengthened HgCdTe fitted-intercept manuscript source

This directory is the controlling repository source package for:

> **Extraction-model and fit-domain dependence of fitted HgCdTe optical intercepts: a two-spectrum case study**

## Contents

- `manuscript.tex` - root LaTeX source;
- `frontmatter.tex` - title, abstract, and keywords;
- `sections/*.tex` - complete manuscript sections;
- `references.tex` - self-contained bibliography used by the manuscript;
- `references.bib` - machine-readable bibliography;
- `BUILD.md` - local build instructions;
- `SOURCE_SHA256SUMS` - committed source checksums.

The CI workflow generates the vector figures from committed analysis outputs and
existing frozen repository figures, converts them to PDF, compiles the manuscript,
and uploads a complete ZIP containing `PACKAGE_SHA256SUMS` and the compiled PDF.
Binary build outputs are workflow artifacts rather than committed files.

The older `../irpt/` manuscript is retained for provenance only and is not the
controlling strengthened source.
