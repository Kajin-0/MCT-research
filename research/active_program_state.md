# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Execution mode:** independent, public-data-first, reproducible computation

## Completed Paper I

The observation-model uncertainty manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It establishes that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap laws. Remaining work on that manuscript is submission administration, not expansion of the scientific scope.

## Active flagship program

The active research product is now:

> **A distributional, observation-aware theory of HgCdTe band-edge observables.**

The objective is to predict how a latent signed band structure becomes an absorption edge, photoluminescence peak, photoconductive cutoff, detector 50% cutoff, or magneto-optical Kane-mass estimate.

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

A reported gap is not assumed to equal `Eg(mean x, T)`.

## First executable result

`mct_research.distributional_gap` implements tested second-order propagation of a declared Gaussian composition width through any scalar signed-gap law:

```text
mean-gap curvature bias = 0.5 * d2Eg/dx2 * sigma_x^2
local gap width         = abs(dEg/dx) * sigma_x
critical-T width        = abs((dEg/dx)/(dEg/dT)) * sigma_x
```

At the Teppe sample-B nominal transition point (`x=0.155`, `T=77 K`) under the reconstructed Laurenti law:

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

These are precision-scale diagnostics. They do not assert that the Teppe specimen has either composition width, do not identify an optical linewidth, and do not define a topological invariant.

## Activated primary sources

The first full-text source set is:

- Wu 1983 — alloy-fluctuation contribution to bowing;
- Dingrong et al. 1985 — degenerate carrier-filled absorption and free-carrier background;
- Herrmann et al. 1992 — multimodal near-edge model and Gaussian-gap convolution;
- Ivanov-Omskii et al. 2009 — annealing-conditioned PL localization and linewidth;
- Chang et al. 2007 — nonparabolic Kane plus Urbach absorption and thickness-dependent cutoff;
- Teppe et al. 2016 — temperature-driven near-critical Kane mass and velocity.

Claim-level roles and limitations are recorded in `literature/notes/distributional_band_edge_primary_sources.md`.

## Static and finite-temperature methods

The selected-band CdTe static post-processing result remains independently reproducible on the same immutable physical artifact. It is retained as a validated mathematical and software component, not as a converged HgCdTe material prediction.

The present CdTe polar response remains unsuitable for a production AHC result. New AHC, SQS, CPA, SCBA, or alloy production calculations require a decision-changing observable, a published validation target, and a predeclared termination criterion.

## Deferred collaboration package

The paired same-specimen acquisition protocol remains a rigorous future validation design. Outreach, partner search, and facility access are inactive and are not dependencies of the current program.

The independent program must proceed using public full texts, auditable digitization, analytical derivation, reproducible numerical modeling, and existing published spectra.

## Authorized next work

1. verify derivative-step and higher-order stability of the distributional propagation;
2. compare transition-width predictions across latent gap laws without selecting a universal law;
3. reproduce Herrmann's Gaussian-gap-to-tail relation;
4. reproduce Chang's nonparabolic/tail operator and thickness-dependent cutoff under source limits;
5. implement a carrier-filled optical branch and test it against Dingrong's degenerate specimen;
6. test whether one distributional state model can jointly explain Ivanov-Omskii PL displacement and FWHM changes;
7. build cross-modal recoverability and rank-reversal maps;
8. draft the flagship manuscript only after at least one independent published-data reproduction passes.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- selecting one edge from an uncertainty ensemble without an operator declaration;
- identifying `sigma_x`, `sigma_E`, Urbach energy, PL FWHM, and quasiparticle linewidth as equivalent;
- interpreting a local opposite-sign fraction as a bulk topological invariant;
- treating nominal composition as a measured spatial distribution;
- transferring source-specific carrier, tail, or thickness corrections without provenance;
- requiring real collaborators before independent progress can continue;
- escalating to expensive atomistic or first-principles work without a decision-changing validation target;
- expanding Paper I with unrelated new mechanisms instead of preserving its completed claim.
