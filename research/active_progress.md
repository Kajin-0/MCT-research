# Active research progress

**Last updated:** 2026-07-21  
**Controlling ref:** `agent/nonlinear-transition-quadrature` pending issue #169 PR  
**Controlling issue:** #167

Detailed historical results remain in `research/decision_records/`, `data/derived/`, and `data/validation/`. This file records the decisions and quantitative results that control new work.

## 1. Static selected-band state

- The CdTe finite-k workflow uses the isospectral selected-band polar Hamiltonian.
- The complete zincblende linear invariant space has four directions.
- The complete quadratic space has ten established Weiler directions.
- The conventional tied quadratic model fails matrix and spectral closure.
- An independent implementation reproduces the selected-band construction, invariant spaces, and conventional-model failure on an untouched `[110]` holdout.

Controlling numerical diagnostics remain:

```text
minimum selected overlap singular value       0.9998015324
maximum selected eigenvalue error              2.576e-14 eV
complete linear invariant dimension            4
complete quadratic invariant dimension         10
complete linear training residual              1.523e-7
complete linear [110] holdout residual          1.447e-7
complete quadratic training residual           1.255e-5
complete quadratic [110] holdout residual       7.956e-6
conventional quadratic training residual       0.287044
conventional quadratic [110] holdout residual   0.332112
P8                                              6.772222 eV A
P7                                              6.201826 eV A
```

Authorized conclusion: the static post-processing result is independently reproducible on the same immutable physical input.

Unauthorized conclusion: the underlying PBE calculation, pseudopotential, geometry, cutoff, band count, or material parameters are independently converged.

The CdTe polar response remains unsuitable for a production AHC result. Additional static replication on the same physical artifact, A1 execution, and unvalidated alloy production work are inactive.

## 2. Historical universal-gap program closure

The provisional Hansen-Padé thermal law remains archived:

```text
Eg(x,T) = Eg_Hansen(x,0) + 5.918273117836612e-4
          * (1-2*x) * T^3 / (T^2 + 18.059294367159467^2)
```

It is a constrained Seiler-family parameterization, not a production law.

The historical program established:

- Chu 1991 same-specimen thermal transfer favors Hansen over the provisional Padé law;
- Chu 1991 composition-series model ordering changes under source-offset treatment;
- Seiler and Hansen remain indistinguishable at the controlling scale;
- composition uncertainty, source lineage, carrier/defect state, and observation operator dominate the sub-meV empirical-law ordering;
- no universal HgCdTe gap law or production edge correction is identified.

No new unconstrained empirical coefficients are authorized.

## 3. Completed Paper I

PR #131 merged the submission-oriented manuscript:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

The two Moazzami 2005 solid-IRSE traces produce:

```text
x=0.226, T=300 K, d=15.40 um, 125 derived points
x=0.310, T=300 K, d=4.95 um, 115 derived points

fitted-model edge spans       6.414 and 6.830 meV
maximum coordinate shift      0.891 meV
Seiler-Hansen nominal margin  0.177-0.255 meV
```

Operational edge choice changes the nominal closest material comparator. No threshold is identified with the latent gap. The Seiler-Hansen ordering is descriptive only because specimen-level composition uncertainty is unavailable and both spectra share one source lineage.

Paper I is scientifically frozen. Remaining author, affiliation, archive, declaration, and submission actions are administrative.

## 4. Active flagship program

Issue #167 and merged PR #168 activate:

> **A distributional, observation-aware theory of HgCdTe band-edge observables.**

The controlling forward chain is:

```text
latent mean signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic, tail, and free-carrier response
-> thickness/instrument response
-> declared observation operator
-> reported gap observable
```

A reported absorption edge, PL peak, detector cutoff, photoconductive edge, or magneto-optical gap is not assumed to equal `Eg(mean x,T)`.

The full program specification is `docs/program/distributional_band_edge_flagship.md`.

## 5. Local distributional propagation

`mct_research.distributional_gap` implements:

```text
mean-gap curvature bias = 0.5 * d2Eg/dx2 * sigma_x^2
local gap width         = abs(dEg/dx) * sigma_x
critical-T width        = abs((dEg/dx)/(dEg/dT)) * sigma_x
```

At the Teppe sample-B nominal transition point under the reconstructed Laurenti law:

```text
x                                      0.155
T                                     77 K
Eg(mean x,T)                          -0.047812 meV
dEg/dx                                 1.7191085 eV
d2Eg/dx2                               0.4711102 eV
dEg/dT                                 0.3851780 meV/K

sigma_x = 0.001:
  curvature bias                       0.000236 meV
  sigma_E                              1.719109 meV
  sigma_Tc                             4.463153 K
  Gaussian opposite-sign fraction     0.488961

sigma_x = 0.005:
  curvature bias                       0.005889 meV
  sigma_E                              8.595543 meV
  sigma_Tc                            22.315766 K
  Gaussian opposite-sign fraction     0.498054
```

Authorized conclusion: near the nominal transition, composition variation is strongly amplified into local signed-gap and critical-temperature width.

Unauthorized conclusions:

- the Teppe specimen is not claimed to have either declared `sigma_x`;
- `sigma_E` is not identified with an Urbach energy, PL FWHM, or quasiparticle linewidth;
- the local opposite-sign fraction is not a bulk topological invariant;
- Laurenti is not selected as a universal law.

The immutable reference is `data/validation/teppe2016_distributional_transition_screen.json`.

## 6. Exact bounded-Gaussian transition distribution

Issue #169 adds deterministic quadrature for a Gaussian composition model conditioned on `0 <= x <= 1`. The implementation reports exact signed-gap moments, approximation errors, gap-sign probabilities, root multiplicity, no-crossing probability, and conditional critical-temperature moments.

The three-model screen uses mean composition `x=0.155`, temperature window `0-300 K`, quadrature order 256, and composition scenarios `sigma_x = 0.001, 0.003, 0.005, 0.010`.

Central critical temperatures are:

```text
Laurenti reconstructed              77.1241 K
Hansen-Schmit-Casselman             52.0438 K
archived provisional Hansen-Pade    52.5937 K
central model span                  25.0803 K
```

### High-precision scenario: `sigma_x=0.001`

```text
model       crossing P   exact sigma_Tc   local width error
Laurenti    1.000000       4.46435 K        +0.00221 K
Hansen      1.000000       4.55975 K        +0.00014 K
Padé        1.000000       3.80408 K        -0.00104 K
```

The derivative approximation is effectively exact, but the 25.08 K latent-law span is about 5.5-6.6 times the composition-induced width.

Authorized result: at `sigma_x=0.001`, latent-law uncertainty dominates nonlinear composition propagation.

### Intermediate scenario: `sigma_x=0.005`

```text
model       crossing P   always normal P   exact conditional sigma_Tc
Laurenti    0.996439       0.003561          22.2899 K
Hansen      0.986951       0.013049          21.8538 K
Padé        0.986951       0.013049          18.3449 K
```

Composition-induced width is now comparable to the central model span. Conditional moments require explicit crossing probability.

### Broad scenario: `sigma_x=0.010`

```text
model       crossing P   always normal P   mean shift     width error
Laurenti    0.913966       0.086034          +5.5170 K     -6.6812 K
Hansen      0.858810       0.141190         +11.0501 K     -9.6575 K
Padé        0.858810       0.141190          +9.8254 K     -7.4308 K
```

The local implicit-function Gaussian becomes materially misleading because the finite observation window censors composition realizations without a transition. A conditional mean and width are incomplete without the crossing probability.

The immutable reference is `data/validation/near_critical_transition_model_dependence.json`; the derivation is `docs/derivations/009_bounded_composition_transition_distribution.md`.

## 7. Activated full-text source chain

The initial flagship source audit covers:

- Wu 1983 — alloy-fluctuation contribution to bowing beyond VCA;
- Dingrong et al. 1985 — degenerate carrier-filled absorption and free-carrier background;
- Herrmann et al. 1992 — Gaussian-gap convolution, multimodal broadening, and shallow-level contributions;
- Ivanov-Omskii et al. 2009 — processing-conditioned PL localization, inferred disorder, and linewidth;
- Chang et al. 2007 — nonparabolic Kane plus Urbach absorption and thickness-dependent cutoff;
- Teppe et al. 2016 — temperature-driven Kane-mass sign change and approximately constant velocity.

The claim-level audit is `literature/notes/distributional_band_edge_primary_sources.md` and the central claim ledger is `literature/ledger.md`.

## 8. Absorption observation boundaries retained from Paper I

- Every edge record must preserve calibration, modality, temperature, thickness, composition provenance, carrier state, tail treatment, fit window, model definitions, thresholds, covariance, and the raw or auditable spectrum.
- The exporter returns all valid candidates and exclusions; it never selects a corrected material gap.
- The Chang nonparabolic-Urbach operator remains source-bounded and cannot be freely fit without same-specimen parameter provenance.
- Finkman-Schacham operational edges remain detector-response operators, not latent-gap measurements.
- Herrmann's full hybrid operator remains incomplete until the external Anderson branch, band-filling factors, quasi-Fermi mapping, and Kane conventions are reconstructed.

## 9. Deferred collaboration program

The paired eight-specimen, two-modality, two-temperature acquisition protocol remains a rigorous future validation design:

```text
8 specimens x 2 modalities x 2 temperatures = 32 primary observations
```

Its composition, state-separation, correlation, drift, replicate, and provenance gates remain valid.

However:

- facility search, outreach approval, and external sending are inactive;
- no collaborator, access, cost, or schedule is assumed;
- the protocol is not a dependency of the independent flagship program.

## 10. Authorized next work

1. complete quadrature-order and root-grid convergence checks for the nonlinear transition screen;
2. reproduce Herrmann's Gaussian-gap-to-exponential-tail relation;
3. reproduce Chang's nonparabolic/tail continuity and thickness-dependent cutoff under source restrictions;
4. implement a carrier-filled optical branch and test the Dingrong degenerate regime;
5. test whether one distributional specimen-state model can jointly explain Ivanov-Omskii PL displacement and FWHM;
6. build cross-modal recoverability and operator-induced rank-reversal maps;
7. begin the flagship manuscript after at least one independent published-data reproduction passes;
8. activate SQS, CPA, SCBA, or first-principles work only if a low-cost result identifies a decision-changing observable that requires it.

## 11. Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- selecting one edge from an uncertainty ensemble without an operator declaration;
- treating nominal composition as a measured spatial distribution;
- equating `sigma_x`, `sigma_E`, Urbach energy, PL FWHM, and quasiparticle linewidth;
- treating detector cutoff as a direct material gap;
- treating PL, absorption, photoconductive, and magneto-optical gaps as interchangeable;
- reporting conditional transition moments without their crossing probability;
- interpreting always-normal/no-crossing probability as a measured topological phase fraction;
- assigning Bayesian meaning to unweighted latent-law spread;
- transferring source-specific carrier, tail, defect, or thickness corrections without provenance;
- claiming the bounded Gaussian model is microscopically complete;
- claiming static electronic-structure convergence from the post-processing reproduction;
- additional static replication on the same artifact;
- broad source accumulation without a decision-changing target;
- requiring real collaborators before independent progress can continue;
- unsupported novelty claims.
