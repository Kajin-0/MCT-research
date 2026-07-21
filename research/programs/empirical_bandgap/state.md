# Program state: empirical bandgap reconstruction

**Portfolio contribution:** R01  
**State:** active foundation; primary-data acquisition dependent

## Objective

Reconstruct the provenance, specimen definitions, observables, and fitted datasets behind historical HgCdTe composition- and temperature-dependent bandgap equations, then compare candidate analytical laws under controlled validation.

## Controlling issues

- #1 — Hansen reconstruction;
- #8 — common analytical benchmark;
- #17 — Seiler two-photon magnetoabsorption dataset;
- #20 — Camassel LPE composition series.

## Completed foundations

- executable historical and provisional gap laws;
- composition-aware fitting and validation infrastructure;
- uncertainty, rank, and conditioning diagnostics;
- specimen- and source-aware data schemas;
- signed-gap evaluation usable by downstream programs.

## Unresolved scientific questions

- what data and edge definition Hansen actually fitted;
- whether fixed-specimen temperature series change model ranking;
- how composition calibration and specimen state affect apparent residuals;
- whether a defensible analytical evolution outperforms historical relations out of sample.

## Manuscript status

No active manuscript is recorded for this program. A future paper requires a reconstructed primary dataset, held-out validation, and a claim stronger than another unconstrained polynomial fit.

## Authorized next gates

- acquire and audit primary full texts and specimen tables;
- reproduce published coefficients where source data permit;
- perform group-preserving validation across specimens and observables;
- quantify model ranking under composition and edge-definition uncertainty.

## Unsupported claims

This program does not currently support:

- a new universal HgCdTe bandgap equation;
- sub-meV superiority inferred from heterogeneous nominal compositions;
- treating optical cutoff, PL peak, magneto-optical gap, and intrinsic gap as interchangeable;
- fitting additional flexibility without held-out evidence.

## Shared dependencies

Gap-law code, provenance records, uncertainty tools, literature ledgers, and validation datasets are shared with the distributional, spatial-disorder, and Kane programs.

## Pause criterion

Pause model expansion when primary-data reconstruction or independent validation—not model flexibility—is the limiting factor.