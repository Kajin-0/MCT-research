# R03 state update — Gaussian-power tail theorem integration

**Date:** 2026-08-01  
**Issue:** #225  
**Source branch:** superseded PR #226  
**Current-main integration:** clean analytical tranche after PRs #408 and #409

## Decision

```text
OPERATOR_SPECIFIC_THEOREM_RETAINED
PUBLISHED_FIGURE_CURVATURE_NOT_IDENTIFIABLE
BROAD_NOVELTY_CLAIMS_WITHDRAWN
NO_MANUSCRIPT_AUTHORIZATION
```

## Integrated analytical result

For

$$
\alpha_p(E)=A\,\mathbb{E}[(E-G)_+^p],
\qquad
G\sim\mathcal{N}(\mu_G,\sigma_G^2),
\qquad p\ge0,
$$

with

$$
z=(E-\mu_G)/\sigma_G,
\qquad
F_p(z)=\int_0^\infty t^p\phi(z-t)\,dt,
$$

the integrated tranche preserves:

$$
F_p'=F_{p+1}-zF_p,
$$

$$
F_p''=F_{p+2}-2zF_{p+1}+(z^2-1)F_p,
$$

$$
\frac{d^2\log\alpha_p}{dE^2}\le0,
$$

and the deep-tail limits

$$
\alpha_p(E)\sim A\sigma_G^p\Gamma(p+1)\phi(z)(-z)^{-(p+1)},
$$

$$
\sigma_G^2\frac{d^2\log\alpha_p}{dE^2}\to-1.
$$

The local inverse logarithmic slope is therefore nondecreasing with energy inside the declared controlled model. The model has a Gaussian deep tail with an algebraic prefactor, not a true Urbach-exponential asymptote.

## Corrective Herrmann boundary

The Herrmann 1992 source distribution uses the ordinary Gaussian convention `sigma_G=s`. The earlier repository transcription using a `4*s^2` denominator and `sigma_G=sqrt(2)*s` is superseded.

For the simplified square-root power-edge calculation:

```text
1–100 cm^-1:   W_fit/s = 0.3571183113580045
100–500 cm^-1: W_fit/s = 0.5718408687380571
relative increase = 0.6012644844884394
```

The source's approximate `W=s/2` coefficient is not reproduced by this controlled operator. The fit-window sensitivity remains valid.

## Claim boundary inherited from PR #409

The following are established prior art and are not project novelty:

- apparently exponential finite intervals from Gaussian or correlated disorder;
- an intermediate Urbach-like regime followed by a deeper Gaussian tail;
- Gaussian averaging of a direct-gap square-root edge;
- energy-dependent apparent Urbach energy;
- fit-window-dependent exponential parameters;
- generic partial-moment recurrences;
- kernel-dependent asymptotic class.

The retained candidate is only the assembled operator-specific differential, curvature, asymptotic, and recoverability package. No equivalent assembled theorem was located in the inspected primary-source material, but the unresolved O'Leary 1995 full texts prevent a universal novelty determination.

## Recoverability boundary inherited from PR #408

Historical Finkman publication figures do not independently locate the displayed window relative to `mu_G` and therefore cannot validate logarithmic curvature. Manual digitization remains unauthorized for this purpose.

## Authorized use

- preserve and test the analytical observation operator;
- preserve the corrected Herrmann convention and deterministic references;
- use the result for observation design and identifiability analysis;
- retain the theorem as a bounded R03 candidate result.

## Prohibited use

- infer Gaussian composition disorder from a visually straight absorption tail;
- equate apparent Urbach energy with composition variance;
- claim novelty for Gaussian convolution, square-root-edge averaging, local inverse slope, or partial-moment recurrences individually;
- claim the Gaussian asymptotic for non-Gaussian disorder kernels;
- treat publication-figure digitization as material validation;
- authorize manuscript writing or submission.

## Remaining external gates

1. recover and audit the two O'Leary 1995 full texts, or record a formal source-unavailable boundary;
2. obtain numerical absorption data with uncertainty or covariance;
3. obtain an independent mean-gap, intrinsic-amplitude, or above-gap anchor;
4. apply the published recoverability gate before any fitting or mechanism claim.
