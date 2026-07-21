# MCT Research

A hypothesis-driven, reproducible research program for the electronic structure and measurable band-edge observables of $\mathrm{Hg}_{1-x}\mathrm{Cd}_x\mathrm{Te}$ (HgCdTe/MCT).

## Active scientific objective

The repository now develops a **distributional, observation-aware theory of HgCdTe band-edge measurements**.

The central question is not only

$$
E_g=E_g(x,T),
$$

but

> Given a latent signed band structure, specimen-state distribution, carrier/defect state, geometry, and measurement operator, what gap will an absorption, photoluminescence, detector-cutoff, photoconductive, or magneto-optical experiment report?

A reported gap is not assumed to equal $E_g(\bar x,T)$.

## Completed Paper I

The first manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It shows that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap equations. The result is a non-identifiability statement, not the selection of a universal replacement equation.

## Flagship program

The active publication program connects:

1. latent mean signed-gap laws;
2. specimen-level and local composition distributions;
3. alloy-disorder and curvature effects;
4. carrier filling and band-gap renormalization;
5. nonparabolic Kane absorption;
6. Urbach and defect-related tails;
7. free-carrier absorption;
8. optical thickness, interference, and collection geometry;
9. modality-specific edge operators;
10. the apparent width and location of the normal/inverted transition.

The program specification is in:

- `docs/program/distributional_band_edge_flagship.md`
- `research/decision_records/2026-07-21-distributional-band-edge-program-activation.md`
- issue `#167`

## First executable distributional result

`mct_research.distributional_gap` implements a tested second-order propagation of a declared Gaussian composition width through any scalar signed-gap law:

$$
\mathbb E[E_g(X,T)]
\approx
E_g(\bar x,T)
+
\frac12 E_{g,xx}(\bar x,T)\sigma_x^2,
$$

$$
\sigma_{E,x}
\approx
|E_{g,x}(\bar x,T)|\sigma_x,
$$

and near a critical point,

$$
\sigma_{T_c}
\approx
\left|
\frac{E_{g,x}}{E_{g,T}}
\right|
\sigma_x.
$$

At the Teppe sample-B nominal transition regime, using the reconstructed Laurenti law at $x=0.155$ and $T=77$ K:

```text
Eg(mean x,T)                         -0.0478 meV
dEg/dx                                1.71911 eV
dEg/dT                                0.38518 meV/K

sigma_x = 0.001:
  sigma_E                              1.719 meV
  sigma_Tc                             4.463 K
  Gaussian local opposite-sign frac   0.48896

sigma_x = 0.005:
  sigma_E                              8.596 meV
  sigma_Tc                            22.316 K
  Gaussian local opposite-sign frac   0.49805
```

These values are precision-scale diagnostics. They do not assert that the Teppe specimen has either composition width, do not identify an optical linewidth, and do not define a bulk topological invariant.

The reference record is:

- `data/validation/teppe2016_distributional_transition_screen.json`

The derivation is:

- `docs/derivations/008_distributional_gap_observables.md`

## Activated primary-source chain

The first full-text flagship source set is:

- Wu 1983 — alloy-fluctuation contribution to bandgap bowing;
- Dingrong et al. 1985 — degenerate carrier-filled absorption;
- Herrmann et al. 1992 — multimodal near-edge broadening and Gaussian-gap convolution;
- Ivanov-Omskii et al. 2009 — annealing-conditioned PL localization and linewidth;
- Chang et al. 2007 — nonparabolic Kane plus Urbach absorption and thickness-dependent cutoff;
- Teppe et al. 2016 — temperature-driven Kane-mass sign change near the transition.

Claim-level source roles and limitations are recorded in:

- `literature/notes/distributional_band_edge_primary_sources.md`

## Existing technical foundation

The repository also contains:

- Hansen, Laurenti, and constrained provisional gap baselines;
- composition-aware weighted fitting and group-preserving cross-validation;
- absorption-edge uncertainty and source-bounded observation operators;
- a homogeneous bulk 8-band Kane implementation;
- one-$P$ and two-$P$ matrix-level parameter projection;
- gauge alignment and zone-centre symmetry restoration;
- Hermitian covariance propagation and generalized least squares;
- integrity-checked `MatrixDataset` storage;
- strict adapters for full $8\times8$ first-principles exports;
- a reproducible static CdTe selected-band post-processing result;
- finite-temperature matrix and reconstruction oracles.

Synthetic recovery establishes implementation correctness only. It is not experimental or material validation.

## Static and first-principles status

The selected-band CdTe post-processing framework is independently reproducible on the same immutable physical artifact. It establishes the mathematical projection and software behavior, not convergence of the underlying electronic-structure calculation.

The current CdTe polar response is not suitable for a production Allen-Heine-Cardona result. New AHC, SQS, CPA, SCBA, or production alloy calculations require a decision-changing observable, an external validation target, and a predeclared termination criterion.

## Research standards

Every important result must include:

1. assumptions and observable definitions;
2. derivation or computational provenance;
3. dimensional and limiting-case checks;
4. uncertainty and sensitivity analysis;
5. comparison with primary literature;
6. a stated falsification test;
7. a clear distinction between source-established facts and project inference.

No novelty claim is accepted merely because a result appears in the repository.

## Claim restrictions

The active program does not permit:

- treating nominal composition as a measured composition distribution;
- equating $\sigma_x$, $\sigma_E$, Urbach energy, PL FWHM, and quasiparticle linewidth;
- treating detector cutoff as a direct material gap;
- treating PL, absorption, photoconductive, and magneto-optical gaps as interchangeable;
- inferring a bulk topological invariant from a local sign probability;
- reopening unconstrained empirical gap fitting;
- requiring external collaborators before independent research can continue.

## Repository organization

- `docs/program/` — controlling research programs and computation gates
- `docs/derivations/` — formal derivations and limiting-case checks
- `docs/insights/` — concise research findings and conjectures
- `research/` — active state, progress, and decision records
- `literature/` — source ledger, audits, and claim-level notes
- `benchmarks/` — analytical model specifications and benchmark status
- `src/mct_research/` — executable models and uncertainty propagation
- `tests/` — numerical, symmetry, ingestion, covariance, and identifiability tests
- `data/` — provenance-controlled experimental, theoretical, and validation records
- `manuscript/` — reproducible manuscript assets
- `first_principles/` — parameterized calculation assets and provenance ledgers
- `tools/` — data conversion and research workflow utilities

## Validation

Install and run:

```bash
python -m pip install -e '.[test]'
pytest
```

GitHub Actions is the controlling clean-environment validation path. Exact test counts should be taken from the workflow attached to the evaluated commit rather than from an older README snapshot.

## Current next steps

1. test derivative-step and higher-order stability of the distributional approximation;
2. compare transition-width predictions across latent gap laws;
3. reproduce Herrmann's Gaussian-gap-to-tail limit;
4. reproduce Chang's nonparabolic/tail and thickness operators under source restrictions;
5. implement the Dingrong degenerate carrier branch;
6. test Ivanov-Omskii PL displacement and width jointly;
7. build cross-modal recoverability and rank-reversal maps;
8. begin the flagship manuscript after an independent published-data reproduction passes.
