# LaTeX build instructions

The controlling manuscript source is `manuscript.tex`. It contains a self-contained `thebibliography` block. `references.bib` is supplied as a machine-readable bibliography; all figures are in `figures/`.

## Required tools

- XeLaTeX
- latexmk

## Build

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error manuscript.tex
```

The resulting PDF is `manuscript.pdf`.

## Clean

```bash
latexmk -C manuscript.tex
```

The source is a portable scientific-review preprint, not the final template of a
selected journal. The title, estimand separation, numerical results, and claim
boundaries are controlling. Journal-specific conversion should occur only after
specialist review and target-journal selection.
