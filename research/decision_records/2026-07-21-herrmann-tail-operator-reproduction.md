# Corrective decision record: Herrmann Gaussian-gap tail operator

**Original date:** 2026-07-21  
**Corrected:** 2026-07-22  
**Issues:** #171, #225  
**Status:** prior reproduction claim retracted; controlled operator retained

## Correction trigger

Full-text inspection of the uploaded Herrmann, Moellmann, and Tomm 1992 source showed that the repository had transcribed Eq. (8) incorrectly.

The printed source distribution is

$$
P(G)=\frac{1}{\sqrt{2\pi}s}
\exp\left[-\frac{(G-\bar G)^2}{2s^2}\right],
$$

so

$$
\boxed{\sigma_G=s}.
$$

The previous repository record used an inequivalent `4s^2` denominator and therefore set `sigma_G=sqrt(2)s`. That convention error stretched the controlled energy axis by `sqrt(2)`.

## Retraction

The following prior statement is retracted:

> The controlled square-root calculation independently reproduces the Herrmann source scale `W approximately s/2`.

With the corrected source convention and all other controlled choices unchanged,

```text
p = 0.5
fit range = 1-100 cm^-1
W_fit/s = 0.35712
R^2 = 0.99570
```

The source reports approximately `W/s=0.5`. The simplified power-edge operator is therefore approximately `28.6%` below the source target and does not reproduce that quantitative coefficient.

## Corrected decision

Retain the Gaussian local-gap convolution with a declared power-law intrinsic edge as:

1. an analytical observation operator;
2. a finite-window identifiability test;
3. a bridge from latent gap distributions to apparent absorption tails;
4. the foundation for the differential and asymptotic curvature result in #225.

Do not describe it as a quantitative reproduction of the source-native `s/2` mapping.

## Source fact retained

Herrmann et al. state that convolution of their Eqs. (2)-(6) with their standard-Gaussian Eq. (8) produces a nearly exponential tail over `1-100 cm^-1`, with apparent broadening approximately

$$
W\approx\frac{s}{2}.
$$

This establishes the qualitative finite-window Gaussian-to-exponential observation as prior art.

## Controlled calculation retained

The repository uses

$$
\alpha(E\mid G)=A(E-G)_+^p,
$$

with a square-root member `p=0.5`, declared normalization `alpha(mean gap)=1000 cm^-1`, and energy-dependent split Gaussian quadrature.

The numerical integral remains validated against exact Gaussian moments and quadrature convergence. The correction changes source labeling and source-normalized numerical claims, not the underlying dimensionless operator.

## Fit-window result retained

The corrected square-root spectrum gives:

```text
fit range        W_fit/s       R^2
0.1-100          0.32595       0.99307
1-100            0.35712       0.99570
10-100           0.40168       0.99836
10-500           0.47254       0.99190
100-500          0.57184       0.99738
```

Changing only the fit window from `1-100` to `100-500 cm^-1` increases `W_fit` by `60.1%` while preserving a strong exponential fit.

Across `p=0.5`, `1`, and `2`, the source-window ratio spans

```text
W_fit/s = 0.34206-0.35712
```

Thus the finite-window non-uniqueness remains valid.

## Corrected inverse-problem consequence

For a reported

$$
W_{\mathrm{fit}}=4\ \mathrm{meV},
$$

the declared model/window family permits

```text
sigma_G = s = 6.995-12.272 meV
range factor = 1.75
```

This excludes additional uncertainty from carrier filling, phonons, shallow levels, excitons, optical inversion, and instrumental response.

## Authorized claims

- Gaussian gap distributions can generate strongly Urbach-like finite-range tails.
- Herrmann 1992 already states that qualitative finite-window result.
- The simplified power-edge calculation does not reproduce the source's approximate `s/2` coefficient under the printed convention.
- A fitted Urbach-like energy is an observation-operator result.
- Fit range, intrinsic branch, and normalization are required provenance for inversion.
- The inverse mapping from one fitted tail energy to a latent gap width is non-unique.
- The exact differential and deep-tail curvature consequences remain separate candidate results.

## Unauthorized claims

- Do not restore agreement by redefining the source parameter `s`.
- `W_fit`, Herrmann `s`, `sigma_G`, `sigma_x`, PL FWHM, and quasiparticle linewidth are not interchangeable.
- A high-quality exponential fit is not proof of alloy disorder.
- The current operator is not the complete Kane/Anderson-Herrmann model.
- No spatial correlation length or microscopic composition variance is inferred.
- No universal HgCdTe disorder correction is identified.

## Next decision

The lower-cost path is to retain the scale-free curvature theorem and evaluate detectability using published spectra. Implement the complete source-native branch only if reproducing the historical `s/2` coefficient becomes decision-changing for a manuscript claim.
