# Program state: distributional band-edge observables

**Portfolio contribution:** R03  
**State:** active research program; no active manuscript

## Objective

Develop a constructive, falsifiable theory connecting latent signed-gap laws, specimen-state distributions, carrier and defect state, optical geometry, and modality-specific observation operators to the band edge reported by an experiment.

## Controlling issues

- #22 — HgCdTe band-tail and composition-fluctuation primary data;
- #167 — distributional band-edge program;
- #225 — differential curvature and deep-tail structure of Gaussian-disorder absorption tails;
- #235 — published-figure recoverability of logarithmic tail curvature;
- #251 — cross-material prior-art boundary for Gaussian-tail curvature and finite-window identifiability;
- #254 — Chang absorption figures as an independently anchored curvature-validation path.

## Implemented foundations

Representative layers include:

```text
src/mct_research/distributional_gap.py
src/mct_research/distributional_quadrature.py
src/mct_research/spectral_convolution.py
src/mct_research/detector_cutoff.py
src/mct_research/unified_spectrum.py
src/mct_research/tail_curvature.py
src/mct_research/published_tail_recoverability.py
src/mct_research/anchored_tail_validation.py
```

The repository contains:

- second-order propagation of declared composition distributions through signed-gap laws;
- exact bounded Gaussian quadrature and sign probabilities;
- Gaussian local-gap convolution into controlled absorption models;
- source-bounded detector-cutoff and thickness operators;
- rank and structural-identifiability diagnostics for composed spectrum models;
- analytical differential and deep-tail structure of the Gaussian-power threshold operator;
- finite-window publication-figure straightness and recoverability diagnostics;
- an explicit independent-anchor and anchor-uncertainty gate.

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

## HgCdTe prior-art boundary

An eight-paper full-text audit covers Finkman 1979/1984, Herrmann 1992/1993, Ariel 1995, and Chang 2004/2006/2007.

Established HgCdTe prior art includes:

- finite-range exponential and modified-Urbach fits;
- composition and temperature scaling of empirical tail slopes;
- Gaussian gap convolution producing a nearly exponential finite-range tail;
- use of `d alpha/dE` and `d2 alpha/dE2` to estimate average gap and depth grading;
- averaging a local absorption law over a spatially varying gap;
- first-derivative matching between Urbach and intrinsic branches;
- sensitivity of derivative observables to smoothing and interference removal.

Ariel 1995 analyzes `d alpha/dE` and `d2 alpha/dE2`, not `d2 log(alpha)/dE2`. For a true exponential,

$$
\alpha''=\alpha/W^2>0,
$$

while

$$
\frac{d^2\log\alpha}{dE^2}=0.
$$

## Cross-material prior-art boundary

Issue #251 audits random-potential, amorphous-semiconductor, kesterite, band-fluctuation, organic-semiconductor, and partial-moment precedents.

The following are not novel R03 claims:

1. correlated Gaussian disorder can generate a broad apparently exponential interval;
2. an intermediate Urbach-like regime can cross over to a deeper Gaussian tail;
3. a Gaussian distribution of local gaps can be convolved with direct-gap square-root absorption;
4. the local inverse logarithmic slope can be energy dependent and interpreted as an apparent Urbach energy;
5. narrow fitting windows can force arbitrary exponential fits and fit-dependent tail energies;
6. generic Gaussian partial moments and recurrence relations are standard mathematics;
7. the asymptotic tail class depends on the fluctuation kernel, and non-Gaussian kernels can produce a true exponential asymptote.

The closest audited precedents are:

- John et al. 1986/1988: correlated Gaussian random-potential density-of-states theory with an intermediate approximately exponential regime and a deeper Gaussian tail;
- O'Leary et al. 1995: density and joint-density-of-states functions averaged over Gaussian band-potential fluctuations across subgap and above-gap regimes;
- Gokmen et al. 2013: Gaussian local-gap averaging of direct-gap square-root absorption in kesterites;
- Guerra et al. 2019: a non-Gaussian band-fluctuation kernel selected to yield a true exponential asymptote;
- Kaiser et al. 2021: energy-dependent apparent Urbach energy and explicit narrow-fit-window arbitrariness;
- Winkler et al. 1972: generic partial-moment formulas and recurrences.

The two O'Leary article full texts were not recovered. Publisher abstracts and a first-party thesis record establish the Gaussian-potential averaging model, but do not support definitive equation-level exclusion of an equivalent curvature theorem.

The defensible conclusion is:

> The assembled all-`p` differential, asymptotic, and finite-window result was not located in the inspected primary-source material.

The repository does not support the stronger statement that no equivalent result exists in the literature.

## Gaussian-tail differential structure

For

$$
\alpha_p(E)=A\,\mathbb E[(E-G)_+^p],
\qquad
G\sim\mathcal N(\mu_G,\sigma_G^2),
$$

Issue #225 derives the operator-specific recurrences and establishes

$$
\frac{d^2\log\alpha_p}{dE^2}\le0.
$$

The local apparent tail energy

$$
W_{\rm loc}(E)=\left[\frac{d\log\alpha_p}{dE}\right]^{-1}
$$

is nondecreasing with photon energy, and the deep-subgap limit is

$$
\sigma_G^2\frac{d^2\log\alpha_p}{dE^2}\to-1.
$$

This is an analytical observation-model result, not evidence that a measured HgCdTe tail is caused by composition disorder.

After the cross-material audit, the candidate contribution is the **assembled operator-specific theorem and measurement consequence**, not Gaussian convolution, square-root edge averaging, energy-dependent apparent Urbach energy, or partial-moment recurrence individually.

## Finite-window recoverability theorem

For a fixed displayed dynamic range

$$
R=\log_{10}(\alpha_{\max}/\alpha_{\min}),
$$

Issue #235 establishes that moving the Gaussian-power window to increasingly negative upper standardized energy gives

$$
\epsilon_{\rm affine}=O(|z_{\rm upper}|^{-2})\to0.
$$

Therefore tail straightness alone cannot falsify Gaussian convolution when the displayed window location relative to the latent mean gap or the intrinsic amplitude is unconstrained.

The six-pixel trace-center uncertainty and 18-pixel conservative gate used below are declared figure-analysis scenarios, not measured covariance.

## Finkman publication-figure gate

Source-conditioned 300 dpi calculations give:

| source trace | departure at $z_{\rm upper}=0$ | critical $z_{\rm upper}$ for 6 px | critical $z_{\rm upper}$ for 18 px |
|---|---:|---:|---:|
| Finkman 1984 Figure 4, 85 K | 12.102 px | -1.455 | not reached for $z\le0$ |
| Finkman 1984 Figure 4, 300 K | 25.510 px | -3.183 | -0.717 |
| Finkman 1979 Figure 3, 80 K | 12.289 px | -1.374 | not reached for $z\le0$ |
| Finkman 1979 Figure 3, 300 K | 26.337 px | -3.031 | -0.723 |

The low-temperature traces fail the conservative gate even if the upper point coincides with the latent mean gap. The high-temperature traces exceed it only when the upper point lies within approximately `0.72 sigma_G` below that gap. The source figures do not establish this standardized anchor.

**Decision:** manual digitization of the Finkman figures is not authorized. Reopen only with numerical source data and covariance, an independent mean-gap or intrinsic-amplitude constraint, or enough above-gap data to locate the displayed window in standardized coordinates.

## Chang independently anchored figure gate

Issue #254 tests whether the stronger Chang experimental context changes the decision. Chang 2004 reports simultaneous transmissivity and photoconductivity at the same sample locations, with photoconductivity used to determine the gaps. Chang 2006/2007 provide a smooth fitted tail-to-intrinsic join.

For a source Urbach interval,

$$
\Delta E=W\ln(\alpha_{\max}/\alpha_{\min}),
$$

is used only to map the displayed exponential trace into horizontal pixels. `W` is not identified with `sigma_G`.

At the most favorable controlled subgap placement, $z_{\rm upper}=0$:

| source scenario | maximum departure | departure / 6 px | 18 px gate |
|---|---:|---:|---:|
| Chang 2004 Figure 2(c), optimistic `100-4000 cm^-1` | 8.787 px | 1.465 | fail |
| Chang 2004 Figure 2(c), representative `100-1000 cm^-1` | 4.102 px | 0.684 | fail |
| Chang 2006 Figure 2, optimistic `200-4000 cm^-1` | 4.261 px | 0.710 | fail |
| Chang 2006 Figure 2, representative `200-2000 cm^-1` | 2.769 px | 0.462 | fail |

The optimistic Chang 2004 interval crosses six pixels only for

$$
z_{\rm upper}\gtrsim-0.713,
$$

and no declared trace reaches 18 pixels for any controlled subgap placement. Moving deeper below the mean gap decreases the departure.

The public papers also do not tabulate, trace by trace, the numerical photoconductive gap, its uncertainty or covariance, and the numerical alignment between the gap result and plotted absorption trace. A fitted tail-to-intrinsic transition is not an independent latent-gap covariance.

**Decision:** manual digitization of Chang 2004/2006/2007 is not authorized for logarithmic-curvature validation. The path is both figure-resolution limited and numerical-anchor/covariance limited.

The Chang papers remain useful for specimen metadata, temperature-dependent Urbach energies, tail-to-intrinsic model structure, and the existence of simultaneous photoconductive edge measurements. They do not supply the raw external falsification dataset required by R03.

## Retained candidate distinction

No equivalent single result was located in the inspected material that combines, for arbitrary `p>=0` in the declared one-sided Gaussian-power threshold operator:

- operator-specific first- and second-derivative identities;
- log-concavity of the absorption;
- monotone local inverse logarithmic slope;
- normalized deep-tail logarithmic curvature approaching `-1`;
- fixed-range best-affine residual decreasing as `O(|z_upper|^-2)`;
- a source-conditioned HgCdTe recoverability and no-digitization consequence.

This is a bounded candidate distinction, not a positive novelty determination.

## Published-data assessment

- Finkman 1979/1984 provide useful dynamic range but no standardized window-location anchor.
- Chang 2004/2006/2007 provide stronger edge context but inadequate figure-level curvature and no tabulated same-trace gap covariance.
- Herrmann 1992 reaches approximately `0.1 cm^-1`, but numerical data are not tabulated and the source-native intrinsic branch is complex.
- Ivanov-Omskii 2009 supplies PL disorder-width information, not a raw absorption-curvature dataset.

No audited historical HgCdTe paper currently supplies all of:

1. numerical absorption values;
2. measurement uncertainty or covariance;
3. an independent same-specimen mean-gap or above-gap anchor;
4. sufficient dynamic range for the logarithmic-curvature test.

No new laboratory experiment is required by the current program. The remaining validation target is a public numerical dataset, author-provided file, thesis appendix, institutional repository deposit, or machine-readable supplement meeting those four requirements.

## Unresolved scientific questions

- which latent distributions are supported by specimen-level evidence;
- how local-gap distributions relate to Urbach tails, PL widths, and detector cutoffs without conflation;
- whether any unpublished or repository-hosted numerical HgCdTe spectrum has enough covariance and above-gap information to resolve log curvature;
- whether the O'Leary 1995 full texts contain a closer equation-level precedent;
- when carrier filling, free-carrier absorption, and defect state materially reorder inferred edges;
- which cross-modal measurements identify latent parameters rather than only combinations.

## Manuscript status

The weak manuscript and submission bundle associated with PR #194 were retired from active publication status. This does not retire the program or its validated modules.

No active manuscript is authorized. A new manuscript requires a coherent theorem, a defensible prior-art boundary, and an externally anchored public-data or source-bounded falsification path. Issues #225, #235, #251, and #254 do not by themselves authorize manuscript writing.

## Authorized next gates

- retrieve and inspect the O'Leary 1995 article full texts, or preserve the formal source-unavailable boundary after reasonable attempts;
- seek raw or tabulated HgCdTe absorption data with uncertainty or covariance;
- seek a same-specimen independent mean-gap, photoconductive-gap, intrinsic-amplitude, or above-gap branch anchor;
- search thesis appendices, institutional repositories, machine-readable supplements, and author deposits before considering any further plot digitization;
- reproduce source-native optical or carrier branches only when a candidate numerical dataset makes that work decision-changing;
- stop the Gaussian-tail manuscript path if a close source establishes an equivalent assembled theorem or no externally anchored falsification path can be found;
- split future papers by distinct theorem and validation target rather than forcing all operators into one flagship.

## Unsupported claims

This program does not currently support:

- treating nominal composition as a measured distribution;
- equating composition variance, gap variance, Urbach energy, PL FWHM, and quasiparticle linewidth;
- treating detector cutoff or photoconductive cutoff as a direct latent material gap;
- inferring a bulk topological invariant from local sign probability;
- treating log-concavity or negative curvature as proof of one microscopic mechanism;
- claiming the source `s/2` relation has been reproduced by the controlled power-edge model;
- claiming Ariel's `d2 alpha/dE2` diagnostic is logarithmic curvature;
- equating an empirical Finkman gap with the latent mean gap `mu_G`;
- treating six audit-render pixels as a measured statistical standard deviation;
- identifying source Urbach energy with `sigma_G`;
- treating the Chang fitted transition as an independent latent-gap covariance;
- treating digitized Finkman or Chang curves as material validation after their recoverability gates failed;
- claiming novelty for Gaussian averaging of a square-root direct-gap edge;
- claiming novelty for energy-dependent apparent Urbach energy or fit-window dependence;
- claiming novelty for generic partial-moment recurrence relations;
- claiming a universal Gaussian deep tail across disorder kernels;
- claiming that an equivalent assembled theorem is absent from all literature;
- claiming submission readiness from synthetic recovery, prior-art narrowing, or publication-figure no-go results alone.

## Shared dependencies

This program uses empirical gap laws, Kane infrastructure, literature records, and detector observation operators shared across the portfolio. Spatial-disorder implementation and manuscripts remain intentionally untouched.

## Split criterion

Create separate candidate works when a result has its own central theorem, validation target, and falsification test. Do not preserve a single flagship structure merely for repository convenience.