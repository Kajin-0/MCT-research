# Decision record: Herrmann Gaussian-gap tail operator

**Date:** 2026-07-21  
**Issue:** #171  
**Status:** candidate controlling result pending PR validation

## Decision

Adopt the Gaussian local-gap convolution with a declared power-law intrinsic edge as the first explicit spectral observation operator in the flagship program.

The operator is authorized as:

1. a controlled reproduction of the Herrmann et al. 1992 inhomogeneous-broadening argument;
2. an analytical and numerical identifiability test;
3. a bridge from latent gap distributions to measured absorption tails.

It is not authorized as the complete Anderson-Herrmann HgCdTe absorption model or as a universal conversion from Urbach energy to composition disorder.

## Source fact

Herrmann et al. 1992 define

$$
P(G)=\frac{1}{2s\sqrt{\pi}}
\exp\left[-\frac{(G-\bar G)^2}{4s^2}\right],
$$

so

$$
\sigma_G=\sqrt{2}s.
$$

They report that convolution with their intrinsic edge produces a nearly exponential tail over `1-100 cm^-1`, with fitted broadening energy approximately

$$
W\approx s/2.
$$

## Independent reproduction

The repository uses

$$
\alpha(E\mid G)=A(E-G)_+^p,
$$

with the source-aligned square-root member `p=0.5`, a declared normalization `alpha(mean gap)=1000 cm^-1`, and energy-dependent split Gaussian quadrature.

The numerical integral is mapped onto `G <= E` for every photon energy. This removes the moving threshold cusp from the interior of the quadrature interval. In the declared tail test, the maximum relative change from order `256` to `512` is `5.78e-7`.

For the source fit window:

```text
p = 0.5
fit range = 1-100 cm^-1
W_fit/s = 0.50504
R^2 = 0.99570
```

The source scale is independently reproduced.

## New result

The same square-root spectrum gives:

```text
fit range        W_fit/s       R^2
0.1-100          0.46096       0.99307
1-100            0.50504       0.99570
10-100           0.56806       0.99836
10-500           0.66828       0.99190
100-500          0.80871       0.99738
```

Changing only the fit window from `1-100` to `100-500 cm^-1` increases `W_fit` by `60.1%` while preserving a visually and statistically strong exponential fit.

Across `p=0.5`, `1`, and `2`, the source-window ratio spans only:

```text
W_fit/s = 0.48375-0.50504
```

Thus the fitted slope is much more sensitive to the observation window than to the tested intrinsic-edge exponent, and high `R^2` does not identify either quantity.

## Inverse-problem consequence

For a reported

$$
W_{\mathrm{fit}}=4\ \mathrm{meV},
$$

the declared model/window family permits:

```text
sigma_G = 6.995-12.661 meV
s       = 4.946-8.952 meV
range factor = 1.81
```

This range excludes additional uncertainty from carrier filling, phonons, shallow levels, excitons, optical inversion, and instrumental response.

## Authorized claims

- Gaussian gap distributions can generate strongly Urbach-like finite-range tails.
- The Herrmann approximately-`s/2` scale is reproducible under the source-aligned branch and fit range.
- A fitted Urbach-like energy is an observation-operator result.
- Fit range, intrinsic branch, and normalization are required provenance for inversion.
- The inverse mapping from one fitted tail energy to a latent gap width is non-unique.

## Unauthorized claims

- `W_fit`, Herrmann `s`, `sigma_G`, `sigma_x`, PL FWHM, and quasiparticle linewidth are not interchangeable.
- A high-quality exponential fit is not proof of alloy disorder.
- The current operator does not include complete Kane nonparabolicity, band filling, free-carrier absorption, shallow levels, excitons, or instrument transfer.
- No spatial correlation length or microscopic composition variance is inferred.
- No universal HgCdTe disorder correction is identified.

## Validation gates

Merge requires:

- agreement with exact Gaussian moments for linear and quadratic local edges;
- deterministic zero-width limit;
- order-256 versus order-512 quadrature convergence;
- reproduction of `W_fit/s approximately 0.5` for the source window;
- explicit fit-window non-uniqueness test;
- public API and documentation consistency;
- complete GitHub Actions success on Python 3.11 and 3.13.

## Next decision

After merge, prioritize one calibrated published spectrum with enough above-gap coverage to constrain the intrinsic branch independently of the tail. If no such spectrum is recoverable, proceed to the source-bounded Chang operator and treat the Herrmann result as an analytical identifiability result rather than external material validation.
