# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #169  
**Execution mode:** independent, public-data-first, reproducible computation

## Completed Paper I

The observation-model uncertainty manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It establishes that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap laws. Remaining work on that manuscript is submission administration, not expansion of the scientific scope.

## Active flagship program

The active research product is:

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

## Distributional model status

### Local propagation

`mct_research.distributional_gap` implements tested local propagation:

```text
mean-gap curvature bias = 0.5 * d2Eg/dx2 * sigma_x^2
local gap width         = abs(dEg/dx) * sigma_x
critical-T width        = abs((dEg/dx)/(dEg/dT)) * sigma_x
```

At nominal `x=0.155`, `T=77 K` under the reconstructed Laurenti law:

```text
sigma_x=0.001 -> sigma_E=1.719 meV, sigma_Tc=4.463 K
sigma_x=0.005 -> sigma_E=8.596 meV, sigma_Tc=22.316 K
```

These are precision-scale diagnostics, not asserted Teppe specimen widths, optical linewidths, or topological invariants.

### Exact bounded-Gaussian quadrature

`mct_research.distributional_quadrature` conditions the declared Gaussian composition model on `0 <= x <= 1` and computes:

- exact signed-gap mean, variance, skewness, and sign probabilities;
- local-approximation error;
- root multiplicity inside a declared temperature window;
- single-crossing probability;
- always-normal, always-inverted, multiple-crossing, and unresolved probability;
- conditional critical-temperature moments.

At mean `x=0.155`, the existing latent laws give central critical temperatures:

```text
Laurenti reconstructed              77.1241 K
Hansen-Schmit-Casselman             52.0438 K
archived provisional Hansen-Pade    52.5937 K
central model span                  25.0803 K
```

At `sigma_x=0.001`, exact composition-induced widths are `3.804-4.560 K` and local approximation errors are below `0.003 K`; latent-law uncertainty dominates.

At `sigma_x=0.005`, exact conditional widths are `18.345-22.290 K`, comparable to the central model span, and `0.36-1.30%` of the composition model remains normal throughout `0-300 K`.

At `sigma_x=0.010`, `8.60-14.12%` remains normal throughout the window. Conditional mean temperatures shift by `5.52-11.05 K`, and the local width overestimates the exact conditional width by `6.68-9.66 K` because the distribution is censored by no-crossing compositions.

Controlling rule: conditional transition moments must be reported with the single-crossing probability.

## Activated primary sources

The first full-text source set is:

- Wu 1983 — alloy-fluctuation contribution to bowing;
- Dingrong et al. 1985 — degenerate carrier-filled absorption and free-carrier background;
- Herrmann et al. 1992 — multimodal near-edge model and Gaussian-gap convolution;
- Ivanov-Omskii et al. 2009 — annealing-conditioned PL localization and linewidth;
- Chang et al. 2007 — nonparabolic Kane plus Urbach absorption and thickness-dependent cutoff;
- Teppe et al. 2016 — temperature-driven near-critical Kane mass and velocity.

Claim-level roles and limitations are recorded in `literature/notes/distributional_band_edge_primary_sources.md`; the central prior-art index is `literature/ledger.md`.

## Static and finite-temperature methods

The selected-band CdTe static post-processing result remains independently reproducible on the same immutable physical artifact. It is retained as a validated mathematical and software component, not as a converged HgCdTe material prediction.

The present CdTe polar response remains unsuitable for a production AHC result. New AHC, SQS, CPA, SCBA, or alloy production calculations require a decision-changing observable, a published validation target, and a predeclared termination criterion.

## Deferred collaboration package

The paired same-specimen acquisition protocol remains a rigorous future validation design. Outreach, partner search, and facility access are inactive and are not dependencies of the current program.

The independent program proceeds using public full texts, auditable digitization, analytical derivation, reproducible numerical modeling, and existing published spectra.

## Authorized next work

1. complete quadrature-order and root-grid convergence checks;
2. reproduce Herrmann's Gaussian-gap-to-tail relation;
3. reproduce Chang's nonparabolic/tail operator and thickness-dependent cutoff under source limits;
4. implement a carrier-filled optical branch and test it against Dingrong's degenerate specimen;
5. test whether one distributional state model can jointly explain Ivanov-Omskii PL displacement and FWHM changes;
6. build cross-modal recoverability and rank-reversal maps;
7. draft the flagship manuscript after at least one independent published-data reproduction passes.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- selecting one edge from an uncertainty ensemble without an operator declaration;
- identifying `sigma_x`, `sigma_E`, Urbach energy, PL FWHM, and quasiparticle linewidth as equivalent;
- reporting conditional critical-temperature moments without crossing probability;
- interpreting a local sign or no-crossing probability as a bulk topological invariant or measured phase fraction;
- assigning posterior meaning to unweighted latent-law spread;
- treating nominal composition as a measured spatial distribution;
- transferring source-specific carrier, tail, or thickness corrections without provenance;
- requiring real collaborators before independent progress can continue;
- escalating to expensive atomistic or first-principles work without a decision-changing validation target;
- expanding Paper I with unrelated new mechanisms instead of preserving its completed claim.
