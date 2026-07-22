# Program state: distributional band-edge observables

**Portfolio contribution:** R03  
**State:** active research program; no active manuscript

## Objective

Develop a constructive, falsifiable theory connecting latent signed-gap laws, specimen-state distributions, carrier and defect state, optical geometry, and modality-specific observation operators to the band edge reported by an experiment.

## Controlling issues

- #22 — HgCdTe band-tail and composition-fluctuation primary data;
- #167 — distributional band-edge program;
- #225 — differential curvature and deep-tail structure of Gaussian-disorder absorption tails;
- #235 — published-figure recoverability of logarithmic tail curvature.

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

## Corrective source audit: Herrmann 1992

Herrmann, Moellmann, and Tomm 1992 print

$$
P(G)=\frac{1}{\sqrt{2\pi}s}
\exp\left[-\frac{(G-\bar G)^2}{2s^2}\right],
$$

so

$$
\sigma_G=s.
$$

An earlier repository transcription used an inequivalent `4s^2` denominator and incorrectly set `sigma_G=sqrt(2)s`. The convention and affected source-normalized records have been corrected.

Under the corrected convention, the simplified square-root power-edge operator gives

$$
W_{\rm fit}/s=0.35712
$$

over `1-100 cm^-1`, not the source-reported approximate `s/2`. The former quantitative reproduction claim is retracted. The `60.1%` fit-window sensitivity from `1-100` to `100-500 cm^-1` remains valid.

## Prior-art boundary

An eight-paper full-text audit covers Finkman 1979/1984, Herrmann 1992/1993, Ariel 1995, and Chang 2004/2006/2007.

Established prior art includes:

- finite-range exponential and modified-Urbach fits in HgCdTe;
- composition and temperature scaling of empirical tail slopes;
- Gaussian gap convolution producing a nearly exponential finite-range tail;
- use of `d alpha/dE` and `d2 alpha/dE2` to estimate average gap and depth grading;
- averaging a local absorption law over a spatially varying gap;
- first-derivative matching between Urbach and intrinsic branches;
- sensitivity of derivative observables to smoothing and interference removal.

Ariel 1995 is the closest derivative precedent but analyzes `d alpha/dE` and `d2 alpha/dE2`, not `d2 log(alpha)/dE2`. For a true exponential,

$$
\alpha''=\alpha/W^2>0,
$$

while

$$
\frac{d^2\log\alpha}{dE^2}=0.
$$

The audited papers did not state:

- exact derivative identities for the Gaussian-power moment operator;
- log-concavity of its absorption;
- monotonic increase of local apparent tail energy;
- the deep-tail limit `sigma_G^2 d2(log alpha)/dE2 -> -1`;
- the finite-window non-falsifiability result or a scale-normalized curvature-recoverability test.

These remain candidate contributions subject to wider cross-material prior-art review.

## Gaussian-tail differential structure

Issue #225 develops

```text
src/mct_research/tail_curvature.py
```

For

$$
\alpha_p(E)=A\,\mathbb E[(E-G)_+^p],
\qquad
G\sim\mathcal N(\mu_G,\sigma_G^2),
$$

the Gaussian density and one-sided power edge are log-concave, so

$$
\frac{d^2\log\alpha_p}{dE^2}\le0.
$$

The local apparent tail energy

$$
W_{\rm loc}(E)=\left[\frac{d\log\alpha_p}{dE}\right]^{-1}
$$

is nondecreasing with photon energy. The deep-subgap asymptotic satisfies

$$
\sigma_G^2\frac{d^2\log\alpha_p}{dE^2}\to-1,
$$

not zero. This is an analytical observation-model result, not evidence that a measured HgCdTe tail is caused by composition disorder.

## Published-figure recoverability result

Issue #235 adds

```text
src/mct_research/published_tail_recoverability.py
```

For a fixed finite displayed dynamic range

$$
R=\log_{10}(\alpha_{\max}/\alpha_{\min}),
$$

moving the Gaussian-power window to increasingly negative upper standardized energy gives

$$
\epsilon_{\rm affine}=O(|z_{\rm upper}|^{-2})\to0.
$$

Therefore tail straightness alone cannot falsify Gaussian convolution when the displayed window location relative to the latent mean gap or the intrinsic amplitude is unconstrained.

Source-conditioned 300 dpi panel calculations use a declared six-pixel marker-center uncertainty scenario:

| source trace | departure at $z_{\rm upper}=0$ | critical $z_{\rm upper}$ for 6 px | critical $z_{\rm upper}$ for 18 px |
|---|---:|---:|---:|
| Finkman 1984 Figure 4, 85 K | 12.102 px | -1.455 | not reached for $z\le0$ |
| Finkman 1984 Figure 4, 300 K | 25.510 px | -3.183 | -0.717 |
| Finkman 1979 Figure 3, 80 K | 12.289 px | -1.374 | not reached for $z\le0$ |
| Finkman 1979 Figure 3, 300 K | 26.337 px | -3.031 | -0.723 |

The low-temperature traces fail the conservative 18-pixel gate even if the upper displayed point coincides with the latent mean gap. The high-temperature traces exceed that gate only when the upper point lies within approximately `0.72 sigma_G` below the latent mean gap. The source figures do not establish this standardized anchor.

**Decision:** manual digitization of the Finkman figures is not authorized as a curvature-validation step. Reopen only with numerical source data and covariance, an independent mean-gap or intrinsic-amplitude constraint, or enough above-gap data to locate the displayed window in standardized coordinates.

The pixel dimensions and six-pixel uncertainty are audit scenarios, not source measurement covariance. The modified-Urbach trace spans are source-conditioned empirical slopes, not Gaussian-disorder parameters.

## Published-data assessment

The Chang 2004/2006/2007 spectra primarily cover approximately `10^2-10^4 cm^-1`. They are useful for intrinsic/tail joining but do not visibly provide the deep-subgap range needed for asymptotic curvature.

Herrmann 1992 reaches approximately `0.1 cm^-1`, but numerical data are not tabulated and the source-native intrinsic branch is complex. Figure digitization is scientifically useful only after an independent standardized window-location anchor is available.

No new laboratory experiment is required. The validation program remains restricted to public literature, numerical or digitized published spectra, and synthetic detectability calculations tied to reported instrument and figure limits.

## Unresolved scientific questions

- which latent distributions are supported by specimen-level evidence;
- how local-gap distributions relate to Urbach tails, PL widths, and detector cutoffs without conflation;
- whether any published numerical spectrum has enough covariance and above-gap information to resolve log curvature;
- when carrier filling, free-carrier absorption, and defect state materially reorder inferred edges;
- which cross-modal measurements identify latent parameters rather than only combinations.

## Manuscript status

The weak manuscript and submission bundle associated with PR #194 were retired from active publication status. This does not retire the program or its validated modules.

No active manuscript is authorized. A new manuscript requires a coherent theorem, a defensible prior-art boundary, and a public-data or source-bounded falsification path. Issues #225 and #235 do not by themselves authorize manuscript writing.

## Authorized next gates

- complete the wider cross-material logarithmic-curvature prior-art audit;
- seek numerical published absorption data with measurement covariance;
- seek an independently constrained mean-gap location or above-gap intrinsic branch;
- reproduce source-native optical or carrier branches only when decision-changing;
- test another public spectrum only after a data- or figure-level recoverability gate passes;
- split future papers by distinct scientific claim rather than forcing all operators into one flagship.

## Unsupported claims

This program does not currently support:

- treating nominal composition as a measured distribution;
- equating composition variance, gap variance, Urbach energy, PL FWHM, and quasiparticle linewidth;
- treating detector cutoff as a direct material gap;
- inferring a bulk topological invariant from local sign probability;
- treating log-concavity or negative curvature as proof of one microscopic mechanism;
- claiming the source `s/2` relation has been reproduced by the controlled power-edge model;
- claiming Ariel's `d2 alpha/dE2` diagnostic is logarithmic curvature;
- equating an empirical Finkman gap with the latent mean gap `mu_G`;
- treating six audit-render pixels as a measured statistical standard deviation;
- claiming submission readiness from synthetic recovery alone.

## Shared dependencies

This program uses empirical gap laws, Kane infrastructure, literature records, and detector observation operators shared across the portfolio. Spatial-disorder implementation and manuscripts remain intentionally untouched.

## Split criterion

Create separate candidate works when a result has its own central theorem, validation target, and falsification test. Do not preserve a single flagship structure merely for repository convenience.
