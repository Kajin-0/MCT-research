# Decision record: published HgCdTe tail figures do not independently resolve logarithmic curvature

**Date:** 2026-07-22  
**Program:** R03 — distributional band-edge observables  
**Issue:** #235  
**Status:** controlled recoverability result; manual digitization not authorized

## Decision

Do not manually digitize the Finkman 1979 or Finkman 1984 absorption-tail figures for the purpose of validating the Gaussian-power logarithmic-curvature theorem.

The figures remain useful historical and source-model records, but they do not independently locate the displayed tail interval relative to the latent mean gap. Without that location, finite-range straightness cannot distinguish a true exponential from a sufficiently deep Gaussian-convolution tail.

## Controlling theorem

For

$$
\alpha_p(E)=A\sigma_G^pF_p(z),
\qquad
z=(E-\mu_G)/\sigma_G,
$$

fix a finite log-absorption range

$$
R=\log_{10}(\alpha_{\max}/\alpha_{\min}).
$$

As the upper endpoint $z_2$ is translated to the deep subgap regime, the standardized interval width satisfies

$$
z_2-z_1=O(|z_2|^{-1}),
$$

while the logarithmic curvature remains finite. The departure from the best affine log-absorption fit therefore satisfies

$$
\epsilon_{\rm affine}=O(|z_2|^{-2})\to0.
$$

Thus, for every finite dynamic range and every positive figure-resolution tolerance, there is a sufficiently negative $z_2$ for which the Gaussian-power model is visually and numerically indistinguishable from a straight exponential tail.

## Source-conditioned figure results

The calculation uses declared 300 dpi audit-render geometry and a six-pixel marker-center uncertainty scenario. Six pixels is not claimed to be source measurement covariance.

### Finkman and Schacham 1984, Figure 4

```text
x = 0.29
absorption range = 5-1000 cm^-1
panel width = 545 px over 0.20-0.30 eV
selected vertical span = 562 px
```

| trace | source-conditioned horizontal span | curvature departure at $z_2=0$ | critical $z_2$ for 6 px | critical $z_2$ for 18 px |
|---|---:|---:|---:|---:|
| 85 K | 114.354 px | 12.102 px | -1.455 | not reached for $z_2\le0$ |
| 300 K | 261.665 px | 25.510 px | -3.183 | -0.717 |

### Finkman and Nemirovsky 1979, Figure 3

```text
x = 0.205
selected fit range = 20-1000 cm^-1
panel width = 848 px over 0.08-0.18 eV
selected vertical span = 641.180 px
```

| trace | source-conditioned horizontal span | curvature departure at $z_2=0$ | critical $z_2$ for 6 px | critical $z_2$ for 18 px |
|---|---:|---:|---:|---:|
| 80 K | 136.429 px | 12.289 px | -1.374 | not reached for $z_2\le0$ |
| 300 K | 321.818 px | 26.337 px | -3.031 | -0.723 |

## Interpretation

The low-temperature traces fail the conservative 18-pixel threshold even under the most favorable controlled subgap placement, $z_2=0$.

The high-temperature traces exceed that threshold only if their upper displayed point lies within approximately

$$
0.72\sigma_G
$$

below the latent mean gap. The source figures do not establish this standardized anchor. Their empirical gap or cut-on definitions cannot be silently equated with $\mu_G$.

Source scatter, finite line thickness, baseline uncertainty, interference removal, and smoothing are not included in the six-pixel scenario. Including them can only weaken the figure-level recovery claim.

## Ariel 1995 boundary

Ariel et al. use $d\alpha/dE$ and $d^2\alpha/dE^2$ to estimate average gap and grading. This is derivative prior art and an important warning about noise and smoothing. It is not the current discriminator because

$$
\alpha''=\alpha/W^2>0
$$

for a true exponential, whereas

$$
\frac{d^2\log\alpha}{dE^2}=0.
$$

The observables must not be conflated.

## Authorized claims

- A Gaussian-power tail can be made arbitrarily straight over a fixed finite dynamic range by moving the window sufficiently deep below the latent mean gap.
- Tail straightness alone is therefore not a model-independent falsification test.
- The source-conditioned pixel calculations are reproducible under the declared panel and uncertainty scenarios.
- The Finkman figures require an external gap-location or above-gap constraint before curvature digitization becomes scientifically informative.

## Unauthorized claims

- The measured Finkman tails are caused by Gaussian composition disorder.
- The empirical Finkman gap equals the latent mean gap $\mu_G$.
- Six pixels is a measured statistical standard deviation.
- Visual linearity proves a true Urbach mechanism.
- Publication-figure digitization would constitute specimen or material validation.
- This negative gate authorizes manuscript preparation.

## Reopening criterion

Reopen published-spectrum validation only when at least one of the following becomes available:

1. numerical absorption data with measurement covariance;
2. an independent mean-gap location and intrinsic-amplitude constraint;
3. above-gap data sufficient to constrain the local intrinsic branch and standardized window location;
4. a higher-resolution figure with documented preprocessing and recoverable point centers.

Absent one of those inputs, further manual digitization is low-value work and should remain terminated.
