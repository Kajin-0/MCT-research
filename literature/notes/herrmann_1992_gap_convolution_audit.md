# Herrmann 1992 Gaussian gap-distribution audit

## Source

K. H. Herrmann, K.-P. Moellmann, and J. W. Tomm, “Broadening mechanisms near the E0 transition in narrow-gap Hg1-xCdxTe (0.2 < x < 0.6),” *Journal of Crystal Growth* **117**, 758-762 (1992).

## Scope of this audit

This note isolates the claim used by the distributional band-edge program:

> A Gaussian-like distribution of local energy gaps, convolved with an intrinsic near-edge absorption model, can produce a nearly exponential apparent tail over experimentally relevant absorption coefficients.

It does not treat the paper as establishing a unique microscopic origin for every HgCdTe Urbach tail.

## Source-defined absorption regions

### Exponential tail

Herrmann et al. write the below-edge empirical law as their Eq. (1):

$$
\alpha(E)=\alpha_0\exp\left(\frac{E-E_{00}}{E_0}\right).
$$

The paper reports that photocurrent spectroscopy can verify this behavior over more than three decades and discusses absorption coefficients as low as approximately `0.1 cm^-1` in high-quality specimens.

### Intrinsic region

Above the gap the paper uses the Anderson narrow-gap interband expressions reproduced as Eqs. (2)-(6), including light-hole and heavy-hole contributions and nonequilibrium band-filling factors.

The complete source-native intrinsic branch depends on:

- Kane coupling and band parameters;
- light-hole and heavy-hole dispersions;
- carrier quasi-Fermi levels;
- band-filling factors;
- temperature;
- high-frequency dielectric response;
- Anderson 1977/1980 conventions external to the 1992 paper.

The full branch is therefore not yet a self-contained implementation target from this source alone.

## Source Gaussian convention

Herrmann et al. introduce the Gaussian-like gap distribution in Eq. (8):

$$
P(G)=
\frac{1}{2s\sqrt{\pi}}
\exp\left[-\frac{(G-\bar G)^2}{4s^2}\right].
$$

In ordinary Gaussian notation,

$$
G\sim\mathcal N(\bar G,\sigma_G^2),
\qquad
\boxed{\sigma_G=\sqrt{2}\,s}.
$$

This convention conversion is implemented by
`mct_research.spectral_convolution.herrmann_gap_sigma_ev`.

## Source claim

The paper states that convolving Eqs. (2)-(6) with Eq. (8) gives a nearly exponential tail over the relevant `1-100 cm^-1` absorption range. Interpreting the resulting spectrum through Eq. (1) gives approximately

$$
E_0\approx\frac{s}{2},
$$

with no temperature dependence for this inhomogeneous contribution. The authors propose that this could account for the permanent, low-temperature part of the measured broadening.

## Controlled reproduction used in this repository

The complete Anderson/Herrmann branch remains blocked by external definitions. The first reproducible operator therefore uses a declared family

$$
\alpha(E\mid G)=A(E-G)_+^p,
$$

where

$$
(y)_+=\max(y,0),
$$

and

$$
p\in\{0.5,1,2\}.
$$

The `p=0.5` member is the source-aligned square-root null model. The interval `0.5 <= p <= 2` is also consistent with the later Chang nonparabolic analysis as a sensitivity family, but no one exponent is declared universally correct.

The distributed spectrum is

$$
\bar\alpha(E)=
\int P(G)\alpha(E\mid G)\,dG.
$$

To isolate lineshape rather than an unknown matrix-element amplitude, the controlled reproduction declares

$$
\bar\alpha(\bar G)=1000\ \mathrm{cm^{-1}}.
$$

This is a normalization convention for the sensitivity calculation, not a universal HgCdTe constant.

### Numerical integration

For each photon energy, the implementation integrates only over the smooth interval `G <= E` instead of evaluating the thresholded integrand on one fixed global grid. This energy-dependent split removes the moving cusp at `G=E`.

For the square-root spectrum in the tested tail region, increasing the Gauss-Legendre order from `256` to `512` changes the absorption by at most `5.78e-7` relatively. Linear and quadratic branches agree with their closed Gaussian moments to approximately `1e-10` and `1e-9` relative tolerance, respectively.

## Reproduction result

For the square-root branch and the source-stated `1-100 cm^-1` fit range:

$$
\frac{W_{\mathrm{fit}}}{s}=0.50504,
\qquad
R^2=0.99570.
$$

Thus the controlled calculation independently reproduces the source statement

$$
W_{\mathrm{fit}}\approx\frac{s}{2}.
$$

The result is scale invariant: choosing `s=8 meV` gives

$$
W_{\mathrm{fit}}=4.040\ \mathrm{meV}.
$$

## Critical limitation discovered by the reproduction

The convolved spectrum is not exactly exponential. For the same square-root spectrum:

| absorption fit window | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---|---:|---:|
| `0.1-100 cm^-1` | 0.46096 | 0.99307 |
| `1-100 cm^-1` | 0.50504 | 0.99570 |
| `10-100 cm^-1` | 0.56806 | 0.99836 |
| `10-500 cm^-1` | 0.66828 | 0.99190 |
| `100-500 cm^-1` | 0.80871 | 0.99738 |

Moving from the source window to `100-500 cm^-1` increases the inferred tail energy by approximately `60.1%`, although both fits appear strongly log-linear.

## Intrinsic-edge sensitivity

Over the source window:

| intrinsic exponent $p$ | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---:|---:|---:|
| 0.5 | 0.50504 | 0.99570 |
| 1.0 | 0.50000 | 0.99620 |
| 2.0 | 0.48375 | 0.99712 |

The fitted slopes differ by only about `4.2%` across substantially different intrinsic-edge exponents. Therefore a high-quality exponential-looking tail does not identify the intrinsic branch.

## Identifiability consequence

Across the declared exponent and fit-window family, an observed

$$
W_{\mathrm{fit}}=4\ \mathrm{meV}
$$

is compatible with

$$
6.995\ \mathrm{meV}
\le \sigma_G \le
12.661\ \mathrm{meV},
$$

or equivalently

$$
4.946\ \mathrm{meV}
\le s \le
8.952\ \mathrm{meV}.
$$

The inversion range spans a factor of `1.81` before including carrier filling, phonons, shallow levels, excitons, composition correlation length, or instrumental response.

## What the source and reproduction support

- A distribution of local gaps can generate an apparently exponential below-gap tail.
- The Herrmann `W approximately s/2` scale is reproducible under the source-aligned square-root model and source absorption window.
- The fitted tail parameter is an observation-operator result, not the Gaussian standard deviation itself.
- Fit-window provenance is required for any attempted inversion.

## What they do not support

- `W`, `s`, `sigma_G`, `sigma_x`, PL FWHM, and quasiparticle linewidth are not interchangeable.
- An exponential tail does not prove alloy disorder as the unique mechanism.
- The controlled power-law operator is not the complete source-native Anderson/Herrmann model.
- A universal conversion from Urbach energy to composition variance is not identified.
- The result does not establish a spatial correlation length or microscopic disorder model.

## Next evidence requirement

The next stronger comparison should use a published calibrated spectrum with:

- declared absorption coefficient scale;
- explicit fit range;
- independently measured composition;
- carrier density and conductivity type;
- specimen temperature;
- thickness and optical inversion method;
- enough above-gap data to constrain the intrinsic branch independently of the tail.
