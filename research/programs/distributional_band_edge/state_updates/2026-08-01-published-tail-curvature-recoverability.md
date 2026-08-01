# R03 state update — published-tail curvature recoverability

**Date:** 2026-08-01  
**Issue:** #235  
**Source implementation:** stacked draft PR #237, extracted without PR #226 history  
**Decision:** `CURVATURE_NOT_IDENTIFIABLE_FROM_PUBLISHED_FIGURES`

## Result

The controlled Gaussian-power tail recoverability calculation is integrated as a self-contained R03 tranche. For every fixed finite log-absorption dynamic range, the best-straight-line departure tends to zero as the observed window moves deeper below the latent mean gap:

```text
epsilon_affine = O(abs(z_upper)^-2)
```

Consequently, finite-range semilog straightness cannot falsify the controlled Gaussian-power model unless the displayed window location relative to `mu_G`, the intrinsic amplitude, or an above-gap branch is independently constrained.

## Source-conditioned panel result

The immutable record preserves the declared 300 dpi panel geometry and a six-pixel marker-center uncertainty scenario for Finkman 1979 Figure 3 and Finkman 1984 Figure 4.

- Low-temperature traces do not reach the conservative 18-pixel threshold anywhere in the controlled subgap domain `z_upper <= 0`.
- High-temperature traces reach that threshold only when `z_upper` is approximately `-0.72` or greater.
- The source figures do not independently establish that standardized placement.

The six-pixel scenario is not source measurement covariance. The modified-Urbach relation is used only to define source-conditioned trace spans and is not interpreted as a Gaussian-disorder parameterization.

## Decision boundary

Manual digitization of these Finkman figures is not authorized as logarithmic-curvature validation.

Reopen only with at least one of:

1. numerical absorption data with measurement covariance;
2. an independently constrained mean-gap location or intrinsic amplitude;
3. enough above-gap data to identify the local intrinsic branch and locate the tail window;
4. a higher-resolution source with documented preprocessing and recoverable point centers.

This tranche does not establish Gaussian composition disorder, a microscopic Urbach mechanism, material validation, or manuscript authorization. It modifies no R04 or R05 assets.
