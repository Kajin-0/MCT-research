# Herrmann 1992 Gaussian gap-distribution audit

## Source

K. H. Herrmann, K.-P. Moellmann, and J. W. Tomm, “Broadening mechanisms near the E0 transition in narrow-gap Hg1-xCdxTe (0.2 < x < 0.6),” *Journal of Crystal Growth* **117**, 758-762 (1992), DOI `10.1016/0022-0248(92)90851-9`.

## Scope

This note isolates the source claims relevant to the distributional band-edge program:

1. a Gaussian-like distribution of local energy gaps can produce a nearly exponential apparent absorption tail over a finite absorption window;
2. the authors report an approximate relation between the apparent Urbach broadening and their Gaussian width parameter;
3. the paper does not derive the logarithmic curvature or the deep-tail asymptotic of that convolution.

The paper does not establish a unique microscopic origin for every HgCdTe Urbach tail.

## Source-defined absorption regions

### Exponential tail

Herrmann et al. describe the empirical below-edge law by their Eq. (1),

$$
\alpha(E)=\alpha_0\exp\left(\frac{E-E_{00}}{E_0}\right).
$$

They report that photocurrent spectroscopy verifies exponential behavior over more than three decades and reaches absorption coefficients as low as approximately `0.1 cm^-1` for high-quality specimens.

### Intrinsic region

Above the gap, the paper uses the Anderson narrow-gap interband expressions reproduced as Eqs. (2)-(6), with light-hole and heavy-hole contributions and nonequilibrium band-filling factors.

The complete source-native intrinsic branch depends on:

- Kane coupling and band parameters;
- light-hole and heavy-hole dispersions;
- carrier quasi-Fermi levels;
- band-filling factors;
- temperature;
- high-frequency dielectric response;
- Anderson 1977/1980 conventions external to this paper.

The source-native convolution is therefore more specific than the repository's controlled power-edge sensitivity family.

## Correct source Gaussian convention

The printed Eq. (8) is

$$
P(G)=
\frac{1}{\sqrt{2\pi}\,s}
\exp\left[-\frac{(G-\bar G)^2}{2s^2}\right].
$$

Therefore

$$
\boxed{\sigma_G=s}.
$$

The source parameter `s` is already the ordinary Gaussian standard deviation.

### Correction to the previous repository transcription

An earlier repository transcription used

$$
\frac{1}{2s\sqrt{\pi}}
\exp\left[-\frac{(G-\bar G)^2}{4s^2}\right],
$$

which is a different Gaussian convention and implies `sigma_G=sqrt(2)*s`. That transcription is not what appears in the source PDF. It artificially stretched the energy axis and made the simplified square-root operator appear to reproduce the source's approximate `s/2` relation.

The corrected conversion is implemented by
`mct_research.spectral_convolution.herrmann_gap_sigma_ev`, which now returns `s` unchanged.

## Source claim

Herrmann et al. state that convolving Eqs. (2)-(6) with Eq. (8) produces a nearly exponential tail over the experimentally relevant `1-100 cm^-1` absorption range. Interpreting the resulting spectrum through Eq. (1) gives approximately

$$
E_0\approx\frac{s}{2},
$$

with no temperature dependence for this inhomogeneous contribution. They propose that this contribution could be identified with permanent low-temperature broadening.

This source statement already establishes the qualitative finite-window point: a Gaussian-distributed gap model can look exponential over a declared absorption interval.

## Controlled operator used in the repository

The repository uses the declared family

$$
\alpha(E\mid G)=A(E-G)_+^p,
$$

where

$$
(y)_+=\max(y,0),
\qquad
p\in\{0.5,1,2\}.
$$

The `p=0.5` member is a square-root null model. The wider family is a sensitivity basis, not the complete Anderson/Herrmann absorption branch.

The distributed spectrum is

$$
\bar\alpha(E)=\int P(G)\alpha(E\mid G)\,dG.
$$

To isolate lineshape from an unknown matrix-element prefactor, the controlled calculation declares

$$
\bar\alpha(\bar G)=1000\ \mathrm{cm^{-1}}.
$$

This normalization is not a source-measured universal constant.

## Corrected numerical result

For the square-root branch and the source-stated `1-100 cm^-1` fit range,

$$
\frac{W_{\mathrm{fit}}}{s}=0.35712,
\qquad
R^2=0.99570.
$$

For `s=8 meV`,

$$
W_{\mathrm{fit}}=2.857\ \mathrm{meV}.
$$

The source target is approximately `W/s=0.5`. The simplified power-edge operator therefore falls short by approximately `28.6%` and **does not reproduce the source's quantitative mapping**.

This is scientifically useful: it shows that the source's full intrinsic branch, transition convention, or normalization materially affects the numerical mapping. The mismatch must not be repaired by redefining the source parameter.

## Fit-window dependence that survives the correction

For the same corrected square-root spectrum:

| absorption fit window | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---|---:|---:|
| `0.1-100 cm^-1` | 0.32595 | 0.99307 |
| `1-100 cm^-1` | 0.35712 | 0.99570 |
| `10-100 cm^-1` | 0.40168 | 0.99836 |
| `10-500 cm^-1` | 0.47254 | 0.99190 |
| `100-500 cm^-1` | 0.57184 | 0.99738 |

Moving from `1-100` to `100-500 cm^-1` increases the fitted tail energy by approximately `60.1%`, although both fits remain strongly log-linear.

The dimensionless fit-window result is unchanged because the previous error only mislabeled the Gaussian scale.

## Intrinsic-edge sensitivity

Over `1-100 cm^-1`:

| intrinsic exponent $p$ | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---:|---:|---:|
| 0.5 | 0.35712 | 0.99570 |
| 1.0 | 0.35355 | 0.99620 |
| 2.0 | 0.34206 | 0.99712 |

The fitted slopes differ by only about `4.2%` across the tested exponents. A high-quality exponential-looking tail does not identify the intrinsic branch.

## Corrected inverse-problem consequence

For a reported

$$
W_{\mathrm{fit}}=4\ \mathrm{meV},
$$

the declared exponent and fit-window family permits

$$
6.995\ \mathrm{meV}
\le \sigma_G=s \le
12.272\ \mathrm{meV}.
$$

The range spans a factor of `1.75` before including carrier filling, phonons, shallow levels, excitons, optical inversion, or instrumental response.

## Prior-art boundary after full-text inspection

### Explicitly present in Herrmann 1992

- Gaussian local-gap convolution as an inhomogeneous-broadening mechanism;
- an approximately exponential tail over the finite `1-100 cm^-1` window;
- an approximate source-native relation `E0 approximately s/2`;
- possible association of the temperature-independent contribution with permanent broadening.

### Not found in Herrmann 1992

- a proof of log-concavity for the convolved spectrum;
- exact first- and second-derivative identities for the Gaussian-power operator;
- the local apparent tail energy as an energy-dependent diagnostic;
- the asymptotic result `sigma_G^2 d2(log alpha)/dE2 -> -1`;
- a finite-dynamic-range hypothesis test against a true exponential;
- a unique inversion from observed tail energy to composition variance.

The finite-window appearance itself is prior art. The remaining candidate contribution is the explicit differential and asymptotic structure of the declared observation operator, together with a falsifiable curvature diagnostic.

## What the source and corrected calculation support

- Gaussian-distributed local gaps can generate an apparently exponential finite-window tail.
- Fit-window provenance is required for inversion.
- The controlled power-edge operator does not reproduce the source's approximate `s/2` coefficient under the source's printed convention.
- A fitted tail parameter is an observation-operator result, not automatically a microscopic disorder width.

## What they do not support

- `W`, `s`, `sigma_G`, `sigma_x`, PL FWHM, and quasiparticle linewidth are not interchangeable.
- An exponential tail does not prove alloy disorder as the unique mechanism.
- The controlled power-law operator is not the complete source-native Anderson/Herrmann model.
- No universal conversion from Urbach energy to composition variance is identified.
- No spatial correlation length is inferred.

## Next evidence requirement

The next source-bounded step is not another free power-law sweep. It is either:

1. implement the source-native Anderson/Herrmann branch sufficiently to test the reported `s/2` relation without altering the source convention; or
2. treat the source coefficient as unresolved and proceed with the scale-free curvature theorem and published-spectrum detectability analysis.

The second route is currently lower cost and better aligned with the paper-only evidence program.
