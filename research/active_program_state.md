# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #171  
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

`mct_research.distributional_quadrature` conditions the declared Gaussian composition model on `0 <= x <= 1` and computes exact gap moments, sign probabilities, transition-root multiplicity, crossing probability, and conditional critical-temperature moments.

At mean `x=0.155`, the existing latent laws give:

```text
Laurenti reconstructed              77.1241 K
Hansen-Schmit-Casselman             52.0438 K
archived provisional Hansen-Pade    52.5937 K
central model span                  25.0803 K
```

At `sigma_x=0.001`, exact composition-induced widths are `3.804-4.560 K`; latent-law uncertainty dominates.

At `sigma_x=0.005`, exact conditional widths are `18.345-22.290 K`, and `0.36-1.30%` of the composition model remains normal throughout `0-300 K`.

At `sigma_x=0.010`, `8.60-14.12%` remains normal throughout the window. Conditional means shift by `5.52-11.05 K`, while local linearization overestimates the conditional width by `6.68-9.66 K` because no-crossing compositions censor the root distribution.

Controlling rule: conditional transition moments must be reported with the single-crossing probability.

## First explicit spectral observation operator

`mct_research.spectral_convolution` propagates a Gaussian local-gap distribution through the controlled intrinsic-edge family

```text
alpha(E | G) = A * max(E-G, 0)^p
```

and fits a declared exponential tail only over a caller-specified absorption range.

Herrmann et al. 1992 Eq. (8) uses

```text
P(G)=exp(-(G-Gbar)^2/(4*s^2))/(2*s*sqrt(pi))
sigma_G=sqrt(2)*s
```

The implementation uses energy-dependent split Gauss-Legendre quadrature over `G <= E`. This removes the moving threshold cusp from the interior of the integration interval. For the tested square-root tail, the maximum relative change from quadrature order `256` to `512` is `5.78e-7`.

For the source-aligned square-root edge (`p=0.5`), normalization `alpha(Gbar)=1000 cm^-1`, and the source-stated `1-100 cm^-1` range:

```text
W_fit / s = 0.50504
R^2       = 0.99570
```

This independently reproduces the source statement `W approximately s/2`.

However, the same spectrum gives:

```text
fit window       W_fit / s    R^2
0.1-100          0.46096      0.99307
1-100            0.50504      0.99570
10-100           0.56806      0.99836
10-500           0.66828      0.99190
100-500          0.80871      0.99738
```

Changing only the fit window from `1-100` to `100-500 cm^-1` increases the inferred tail energy by `60.1%`, although both fits appear strongly exponential.

Across intrinsic exponents `p=0.5`, `1`, and `2`, the source-window value changes only from `0.48375s` to `0.50504s`; a high-quality tail fit therefore weakly constrains the intrinsic branch.

For an observed `W_fit=4 meV`, the declared operator family permits:

```text
sigma_G = 6.995-12.661 meV
source s = 4.946-8.952 meV
inversion range factor = 1.81
```

Authorized conclusion: a Gaussian gap distribution can generate an Urbach-like tail and reproduce the Herrmann scale under source-aligned conditions.

Unauthorized conclusion: an Urbach energy does not uniquely identify `sigma_G`, `sigma_x`, a microscopic disorder mechanism, or the complete Anderson-Herrmann model.

The immutable record is `data/validation/herrmann_gaussian_tail_reproduction.json`.

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

1. complete CI validation and merge the Herrmann spectral operator;
2. identify one calibrated published absorption spectrum suitable for external operator validation;
3. reproduce Chang's nonparabolic/tail continuity and thickness-dependent cutoff under source limits;
4. implement a carrier-filled optical branch and test it against Dingrong's degenerate specimen;
5. test whether one distributional state model can jointly explain Ivanov-Omskii PL displacement and FWHM changes;
6. build cross-modal recoverability and operator-induced rank-reversal maps;
7. begin the flagship manuscript once the first real-spectrum reproduction passes.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- selecting one edge from an uncertainty ensemble without an operator declaration;
- identifying `sigma_x`, `sigma_E`, Herrmann `s`, Urbach energy, PL FWHM, and quasiparticle linewidth as equivalent;
- reporting conditional critical-temperature moments without crossing probability;
- interpreting a local sign or no-crossing probability as a bulk topological invariant or measured phase fraction;
- assigning posterior meaning to unweighted latent-law spread;
- treating high log-linear `R^2` as proof of one tail mechanism;
- inferring a gap-distribution width without recording the intrinsic branch, normalization, and fit window;
- treating nominal composition as a measured spatial distribution;
- transferring source-specific carrier, tail, or thickness corrections without provenance;
- requiring real collaborators before independent progress can continue;
- escalating to expensive atomistic or first-principles work without a decision-changing validation target;
- expanding Paper I with unrelated new mechanisms instead of preserving its completed claim.
