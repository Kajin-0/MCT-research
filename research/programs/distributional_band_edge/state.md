# Program state: distributional band-edge observables

**Portfolio contribution:** R03  
**State:** active research program; no active manuscript

## Objective

Develop a constructive, falsifiable theory connecting latent signed-gap laws, specimen-state distributions, carrier and defect state, optical geometry, and modality-specific observation operators to the band edge reported by an experiment.

## Controlling issues

- #22 — HgCdTe band-tail and composition-fluctuation primary data;
- #167 — distributional band-edge program;
- #225 — differential curvature and deep-tail structure of Gaussian-disorder absorption tails.

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

Full-text inspection of Herrmann, Moellmann, and Tomm 1992 established that their printed Eq. (8) is

$$
P(G)=\frac{1}{\sqrt{2\pi}s}
\exp\left[-\frac{(G-\bar G)^2}{2s^2}\right],
$$

so

$$
\sigma_G=s.
$$

An earlier repository transcription used an inequivalent `4s^2` denominator and incorrectly set `sigma_G=sqrt(2)s`. The source convention and all source-normalized validation records have been corrected.

Under the corrected convention, the simplified square-root power-edge operator gives

$$
W_{\rm fit}/s=0.35712
$$

over `1-100 cm^-1`, not the source-reported approximate `s/2`. The former quantitative reproduction claim is retracted. The source-native Anderson/Herrmann branch or its normalization materially affects that historical coefficient.

The finite-window sensitivity result remains valid: changing the fit window from `1-100` to `100-500 cm^-1` increases the fitted tail energy by `60.1%` while preserving high log-linear fit quality.

## Prior-art boundary

Herrmann 1992 explicitly states that Gaussian gap convolution can give a nearly exponential HgCdTe tail over the finite `1-100 cm^-1` absorption range. That qualitative finite-window observation is prior art and must not be claimed as new.

A five-paper full-text audit covering Herrmann 1992/1993 and Chang 2004/2006/2007 did not find:

- exact derivative identities for the Gaussian-power operator;
- a proof that its log absorption is concave;
- monotonic increase of local apparent tail energy;
- the deep-tail limit `sigma_G^2 d2(log alpha)/dE2 -> -1`;
- a finite-dynamic-range curvature test against a true exponential.

These define the remaining candidate contribution, subject to wider literature review.

## Active scoped result: Gaussian-tail differential structure

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
W_{\rm loc}(E)
=\left[\frac{d\log\alpha_p}{dE}\right]^{-1}
$$

is therefore nondecreasing with photon energy. The deep-subgap asymptotic satisfies

$$
\sigma_G^2\frac{d^2\log\alpha_p}{dE^2}\to-1,
$$

not zero. Within this controlled model, a true deep-tail Urbach exponential is impossible.

This is an analytical observation-model result, not evidence that a measured HgCdTe tail is caused by composition disorder.

## Published-data assessment

The uploaded Chang 2004/2006/2007 spectra primarily cover approximately `10^2-10^4 cm^-1`. They are suitable for testing the intrinsic/tail join and first derivative but do not visibly provide the deep-subgap dynamic range needed to resolve the asymptotic curvature.

Herrmann 1992 reports the deepest useful range, reaching approximately `0.1 cm^-1`, but numerical data are not tabulated. Published-figure digitization remains possible, with uncertainty dominated by graph resolution and unavailable measurement covariance.

No new laboratory experiment is required. The validation program is restricted to public literature, digitized published spectra, and synthetic detectability studies tied to reported instrument limits.

## Unresolved scientific questions

- which latent distributions are supported by specimen-level evidence;
- how local-gap distributions relate to Urbach tails, PL widths, and detector cutoffs without conflation;
- whether published spectra have sufficient dynamic range to resolve predicted log curvature;
- when carrier filling, free-carrier absorption, and defect state materially reorder inferred edges;
- which cross-modal measurements can identify latent parameters rather than only combinations.

## Manuscript status

The weak manuscript and submission bundle associated with PR #194 were retired from active publication status. This does not retire the program or its validated modules.

No active manuscript is authorized. A new manuscript requires a coherent theorem, a defensible prior-art boundary, and a public-data or source-bounded falsification path. Issue #225 does not by itself authorize manuscript writing.

## Authorized next gates

- complete the wider claim-level primary-source audit;
- correct and validate all records affected by the Herrmann source-convention error;
- quantify differential tail-curvature recoverability under digitization, spectral noise, and baseline uncertainty;
- digitize one published spectrum only after its usable range is shown to be informative;
- reproduce source-native optical or carrier branches only when decision-changing;
- split future papers by distinct scientific claim rather than forcing all operators into one flagship.

## Unsupported claims

This program does not currently support:

- treating nominal composition as a measured distribution;
- equating composition variance, gap variance, Urbach energy, PL FWHM, and quasiparticle linewidth;
- treating detector cutoff as a direct material gap;
- inferring a bulk topological invariant from local sign probability;
- treating log-concavity or negative curvature as proof of one microscopic tail mechanism;
- claiming the source `s/2` relation has been reproduced by the controlled power-edge model;
- claiming submission readiness from synthetic recovery alone.

## Shared dependencies

This program uses empirical gap laws, Kane infrastructure, literature records, and detector observation operators shared across the portfolio. Spatial-disorder implementation and manuscripts remain intentionally untouched.

## Split criterion

Create separate candidate works when a result has its own central theorem, validation target, and falsification test. Do not preserve a single flagship structure merely for repository convenience.
