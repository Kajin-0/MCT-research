# Program state: distributional band-edge observables

**Portfolio contribution:** R03  
**State:** active research program; no active manuscript

## Objective

Develop a constructive, falsifiable theory connecting latent signed-gap laws, specimen-state distributions, carrier and defect state, optical geometry, and modality-specific observation operators to the band edge reported by an experiment.

## Controlling issues

- #22 — HgCdTe band-tail and composition-fluctuation primary data;
- #167 — distributional band-edge program;
- #225 — finite-window nature and differential curvature of Gaussian-disorder absorption tails.

## Completed foundations

Representative implemented layers include:

```text
src/mct_research/distributional_gap.py
src/mct_research/distributional_quadrature.py
src/mct_research/spectral_convolution.py
src/mct_research/detector_cutoff.py
src/mct_research/unified_spectrum.py
```

The repository contains:

- second-order propagation of declared composition distributions through signed-gap laws;
- exact bounded Gaussian quadrature and sign probabilities;
- Gaussian local-gap convolution into controlled absorption models;
- source-bounded detector-cutoff and thickness operators;
- rank and structural-identifiability diagnostics for composed spectrum models.

## Active scoped result: finite-window Gaussian-disorder tails

Issue #225 develops a separate analytical layer:

```text
src/mct_research/tail_curvature.py
```

For

$$
\alpha_p(E)=A\,\mathbb E[(E-G)_+^p],
\qquad
G\sim\mathcal N(\mu_G,\sigma_G^2),
$$

the Gaussian density and one-sided power edge are log-concave, so their convolution obeys

$$
\frac{d^2\log\alpha_p}{dE^2}\le0.
$$

The local apparent tail energy

$$
W_{\rm loc}(E)
=\left[\frac{d\log\alpha_p}{dE}\right]^{-1}
$$

is therefore nondecreasing with photon energy. The deep-subgap asymptotic has

$$
\sigma_G^2\frac{d^2\log\alpha_p}{dE^2}\to-1,
$$

not zero. Within this controlled model, an Urbach-like exponential is necessarily a finite-window approximation rather than the true deep-tail asymptote.

This is an analytical observation-model result, not evidence that a measured HgCdTe tail is caused by composition disorder.

## Unresolved scientific questions

- which latent distributions are supported by specimen-level evidence;
- how local-gap distributions relate to Urbach tails, PL widths, and detector cutoffs without conflation;
- whether measured spectra have sufficient dynamic range and covariance control to resolve the predicted log curvature;
- when carrier filling, free-carrier absorption, and defect state materially reorder inferred edges;
- which cross-modal measurements can identify latent parameters rather than only combinations.

## Manuscript status

The weak manuscript and submission bundle associated with PR #194 were retired from active publication status. This does not retire the program or its validated modules.

No active manuscript is currently authorized. A new manuscript requires a coherent theorem or experimentally anchored result, independent prior-art review, and a clean work-specific evidence package. Issue #225 does not by itself authorize manuscript writing.

## Authorized next gates

- complete claim-level primary-source audits;
- reproduce source-bounded optical and carrier branches;
- test differential tail-curvature recoverability under realistic spectral noise and baseline uncertainty;
- test recoverability across modalities and thicknesses;
- connect distributional operators to independently characterized specimen distributions;
- split future papers by distinct scientific claim rather than forcing all operators into one flagship.

## Unsupported claims

This program does not currently support:

- treating nominal composition as a measured distribution;
- equating composition variance, gap variance, Urbach energy, PL FWHM, and quasiparticle linewidth;
- treating detector cutoff as a direct material gap;
- inferring a bulk topological invariant from local sign probability;
- treating log-concavity or finite-window curvature as proof of one microscopic tail mechanism;
- claiming submission readiness from synthetic recovery alone.

## Shared dependencies

This program uses empirical gap laws, Kane infrastructure, spatial-kernel models, literature records, and detector observation operators shared across the portfolio.

## Split criterion

Create separate candidate works when a result has its own central theorem, validation target, and falsification test. Do not preserve a single flagship structure merely for repository convenience.
