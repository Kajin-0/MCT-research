# Program state: finite-temperature Kane and electronic structure

**Portfolio contribution:** R02  
**State:** validated infrastructure with gated physical calculations

## Objective

Develop symmetry-resolved 8-band Kane parameterization and finite-temperature matrix workflows that can connect first-principles endpoint calculations to defensible HgCdTe electronic-structure models.

## Controlling issues

- #2 — finite-temperature prior-art audit;
- #4 — binary endpoint calculation sequence;
- #5 — Gamma double-group and broader Kane symmetry extensions;
- #6 — deferred generalized matrix-data pipeline;
- #46 — CdTe lattice and thermal-expansion provenance;
- #90 — historical electronic-structure authorization ledger.

## Completed foundations

- homogeneous bulk 8-band Kane implementation;
- one-`P` and two-`P` matrix projection;
- zone-centre degeneracy handling, symmetry restoration, and gauge alignment;
- Hermitian covariance and generalized least-squares tools;
- strict selected-band first-principles adapters;
- reproducible static CdTe post-processing on an immutable artifact;
- finite-temperature matrix and reconstruction oracles.

## Unresolved scientific questions

- whether the available endpoint calculations are sufficiently converged for material inference;
- how electron-phonon self-energies should be projected into the Kane basis;
- whether scalar parameter renormalization is adequate or matrix-valued temperature dependence is required;
- what alloy interpolation or disorder treatment is justified between CdTe and HgTe.

## Manuscript status

No active manuscript is recorded. The current result is infrastructure and methodological foundation, not a converged finite-temperature HgCdTe prediction.

## Authorized next gates

- close CdTe structural and polar-response provenance gaps;
- validate endpoint exports and convergence before HgTe production work;
- perform decision-changing, bounded calculations with predeclared stopping rules;
- compare projected parameters against independent experimental observables.

## Unsupported claims

This program does not currently support:

- converged AHC corrections for CdTe, HgTe, or HgCdTe;
- a validated finite-temperature 8-band parameter set;
- production SQS, CPA, SCBA, or alloy calculations;
- a new universal bandgap equation derived from incomplete endpoint data;
- treating software projection correctness as material validation.

## Shared dependencies

Kane Hamiltonians, symmetry utilities, matrix datasets, endpoint provenance, and gap benchmarks are shared with distributional observables and any future correlated-random-mass program.

## Computation gate

No expensive calculation should begin unless it targets a decision-changing observable, has an independent validation target, and includes an explicit termination criterion.