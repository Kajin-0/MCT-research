# Finkman-Ariel HgCdTe absorption-tail audit, 1979-1995

## Scope

This note audits three full-text primary sources supplied for Issue #225:

1. E. Finkman and Y. Nemirovsky, *Journal of Applied Physics* **50**, 4356-4361 (1979), DOI `10.1063/1.326421`;
2. E. Finkman and S. E. Schacham, *Journal of Applied Physics* **56**, 2896-2900 (1984), DOI `10.1063/1.333828`;
3. V. Ariel, V. Garber, D. Rosenfeld, and G. Bahir, *Applied Physics Letters* **66**, 2101-2103 (1995), DOI `10.1063/1.113916`.

The audit asks whether these papers already establish the differential logarithmic-curvature result developed in Issue #225, and whether their figures provide a paper-only validation path.

## Finkman and Nemirovsky 1979

### Specimens and measurement domain

The paper reports n-type Hg1-xCdxTe with:

- `0.205 <= x <= 0.220`;
- composition uncertainty approximately `+-0.003` from electron-beam microprobe;
- carrier concentration approximately `(1-2)e15 cm^-3`;
- electron mobility approximately `1e5 cm^2 V^-1 s^-1` at 77 K;
- temperatures from `80 K` to `300 K`;
- samples repeatedly thinned from approximately `80 um` to as little as `15 um`;
- transmission measured from approximately `500` to `2000 cm^-1`.

The authors explicitly identified source-induced specimen heating as an experimental artifact and reduced source intensity until the measured edge no longer shifted. Thickness nonuniformity was approximately `+-2 um`. Refractive-index uncertainty was approximately `+-3%`, with relative dispersion changes measured more precisely.

### Reported absorption law

For the declared interval

```text
20 <= alpha <= 1000 cm^-1
```

the paper fits

$$
\alpha(E,T,x)=\alpha_0(x)
\exp\left[
\frac{\sigma(E-E_0(x))}{T+T_0}
\right].
$$

Within the measured composition interval, the reported best-fit constants are approximately

```text
sigma = 5.65 +- 0.07 K cm
T0    = 80.5 +- 2 K
```

with a linear fit for `E0(x)` and an exponential composition dependence for `alpha0(x)`. The final summary gives

$$
\sigma=5.646,
\qquad
T_0=80.51\ \mathrm{K},
$$

$$
E_0=-3109+1.645\times10^4x\ \mathrm{cm^{-1}},
$$

and

$$
\ln\alpha_0=-20.44+51.70x.
$$

The authors state that the study is limited to approximately `alpha <= 2000 cm^-1` by available specimen thickness. They note that the absorption changes slope above approximately `1000 cm^-1`; they use a constant-alpha energy as an operational gap estimate and distinguish this from the true band gap.

### Figure-level validation value

Figures 3-6 show absorption coefficient on a logarithmic vertical axis against photon energy for four compositions and six temperatures. Multiple thicknesses from the same starting specimen are plotted together. The declared exponential fit interval is approximately `20-1000 cm^-1`, or about 1.70 decades.

These figures are stronger paper-only validation candidates than an abstract-level description because they contain plotted points and fitted lines across composition, temperature, and thickness. Their limitations are:

- no tabulated raw absorption points;
- finite line and symbol thickness;
- old spectrophotometer resolution not reported as a full covariance model;
- refraction and thickness corrections couple neighboring points;
- source-heating control was empirical;
- the published model was fitted over the same interval that would be tested for curvature.

### Novelty consequence

This paper establishes finite-range semilog linearity and a modified Urbach parameterization. It does not analyze

$$
\frac{d^2\log\alpha}{dE^2},
$$

does not introduce a Gaussian distribution of local gaps, and does not derive a deep-tail asymptotic distinction between a true exponential and a distributed-gap model.

## Finkman and Schacham 1984

### Specimens and measurement domain

The paper combines new measurements for:

- Hg0.71Cd0.29Te;
- CdTe;
- temperatures from `80 K` to `300 K`;
- HgCdTe thicknesses approximately `25-300 um`;
- six HgCdTe samples from multiple crystals and growth routes;
- n-type carrier concentration approximately `0.9-3e15 cm^-3`;
- 77 K mobility approximately `3-5e4 cm^2 V^-1 s^-1`.

The results are combined with the 1979 `x approximately 0.205-0.220` data.

### Reported absorption law

The paper writes

$$
\alpha=\alpha_0
\exp\left[
\frac{\sigma(E-E_0)}{w}
\right]
$$

and finds that the best temperature model is

$$
w=T+T_0,
$$

with `alpha0`, `sigma`, and `E0` taken temperature independent. For five of six HgCdTe samples, `sigma` and `T0` agree within approximately `+-5%`.

The reported global composition-temperature interpolation is

$$
E_\alpha(E,T,x)=
\frac{T+81.9}{(3.267\times10^4)(1+x)}
[\ln\alpha+18.88-53.61x]
-0.3424+1.838x+0.148x^4.
$$

The fit is reported to pass within approximately `0.002 eV` for the `x approximately 0.215` and `x=0.29` data, and within approximately `0.004 eV` for CdTe.

### Mechanism claim and its boundary

The abstract says that the tail is not caused by permanent lattice disorder but is a material property. The body is more qualified:

- well-behaved samples of the same composition have similar slopes at the same temperature;
- the slope was largely insensitive to carrier concentration, mobility, and growth method within the tested set;
- poor-quality samples showed gentler low-temperature slopes;
- composition fluctuations or lattice disorder may dominate those abnormal samples;
- the authors could not decide between excitonic explanations and elastic fluctuations of the gap.

Therefore the paper is prior art for both intrinsic/material-parameter interpretations and mechanism non-uniqueness. It does not justify treating every HgCdTe exponential tail as one universal mechanism.

### Figure-level validation value

Figure 4 plots `alpha` from approximately `5` to `1000 cm^-1` against photon energy for Hg0.71Cd0.29Te at temperatures from approximately `85 K` to `300 K`, with measured points and fitted straight lines on a semilog presentation. This spans about 2.30 decades and is the strongest current single published figure for testing whether resolved curvature remains after digitization uncertainty.

The same caveats apply as in 1979: plotted fits are not raw tabulated data, and the original analysis presupposes an exponential family. A valid reanalysis must propagate digitization, axis calibration, line-width, and smoothing uncertainty.

### Novelty consequence

This paper establishes an empirical exponential tail, temperature-composition scaling, and sample-quality dependence. It does not calculate logarithmic curvature, local apparent tail energy, or the asymptotic form of a Gaussian-distributed local-gap operator.

## Ariel et al. 1995

### Model and derivative observables

Ariel et al. use a qualitative two-region model:

$$
\alpha\propto
\exp\left(\frac{E-E_g}{E_t}\right),
\qquad E<E_g,
$$

and

$$
\alpha\propto\sqrt{E-E_g},
\qquad E>E_g.
$$

They propose:

- the maximum of `d alpha/dE` as an approximate average-gap marker;
- extrema of `d2 alpha/dE2` as estimates of `Eg,min` and `Eg,max` in a linearly graded layer;
- the separation of those extrema as an estimate of `Delta Eg`.

For a depth-dependent gap they explicitly average the local absorption coefficient:

$$
\alpha(E)=\frac{1}{d}
\int_0^d
\alpha'[E,E_g(z)]\,dz.
$$

This is direct prior art for using derivatives of an absorption spectrum to diagnose a distribution of gaps along the growth direction.

### Experimental results and limitations

The paper studies bulk, LPE, and MOCVD HgCdTe at room temperature. It reports:

- bulk gap variation below approximately `0.005 eV`;
- LPE variation approximately `0.02 eV`, corresponding to an estimated built-in field of `10-20 V/cm` under a linear-gradient assumption;
- MOCVD built-in field around `30 V/cm`;
- epitaxial layer thickness approximately `10-25 um`;
- the CdTe/HgCdTe transition region cannot be neglected for layers thinner than approximately `15 um`.

The authors explicitly warn that numerical differentiation amplifies noise and interference fringes. Smoothing is required, but excessive smoothing can move the derivative peaks. Their derivative result is therefore already an observation-operator result dependent on preprocessing.

### Exact distinction from Issue #225

Ariel et al. differentiate `alpha`, not `log(alpha)`. The Issue #225 diagnostic is

$$
K_{\log}(E)
=
\frac{d^2\log\alpha}{dE^2}
=
\frac{\alpha''}{\alpha}
-
\left(\frac{\alpha'}{\alpha}\right)^2.
$$

For a true exponential

$$
\alpha=\alpha_0e^{E/W},
$$

Ariel's second derivative is

$$
\alpha''=\frac{\alpha}{W^2}>0,
$$

whereas

$$
K_{\log}=0.
$$

The two diagnostics are therefore not interchangeable. Ariel's method localizes the transition and estimates a finite depth-grading interval under a piecewise Urbach/Kane model. Issue #225 tests whether the subgap lineshape itself has zero logarithmic curvature or the negative curvature predicted by a Gaussian distributed-gap power-edge operator.

Ariel et al. do not derive the Gaussian-power moment identities, log-concavity theorem, monotonic local apparent tail energy, or deep-tail limit.

## Consolidated claim boundary after the three-paper audit

Established prior art now includes:

- empirical exponential and modified-Urbach fits over finite HgCdTe absorption ranges;
- composition and temperature scaling of those fits;
- use of `d alpha/dE` and `d2 alpha/dE2` to estimate average gap and depth grading;
- averaging a local absorption law over a depth-dependent gap;
- warnings that derivative inference depends on smoothing and interference removal;
- explicit uncertainty about the microscopic origin of the exponential tail.

The remaining narrower candidate result is:

> For a Gaussian distribution of local gaps convolved with a sharp one-sided power-law edge, `log(alpha)` is concave, the local apparent exponential energy increases with photon energy, and the deep-tail logarithmic curvature approaches `-1/sigma_G^2`; this supplies a scale-normalized test against a true exponential, whose logarithmic curvature is zero.

This remains a model-conditioned observation theorem. It does not identify composition disorder as the mechanism of a measured tail.

## Paper-only validation ranking

1. **Finkman and Schacham 1984, Figure 4** - measured points and fitted lines over approximately `5-1000 cm^-1`; strongest single finite-window curvature candidate.
2. **Finkman and Nemirovsky 1979, Figures 3-6** - composition, temperature, and thickness replication over approximately `20-1000 cm^-1`, with plotted points extending beyond that interval.
3. **Herrmann 1992** - deepest stated range, approximately `0.1 cm^-1`, but source-native model complexity and limited point recovery remain obstacles.
4. **Herrmann 1993** - explicit empirical fit-window sensitivity and multiple optical modalities.
5. **Ariel 1995, Figure 5** - useful for preprocessing and derivative-method comparison, but it supplies `d2 alpha/dE2`, not the raw `alpha` required for a controlled log-curvature analysis.

Before digitization, perform a synthetic recoverability calculation using the actual axis dimensions, symbol sizes, and dynamic ranges of the 1979 and 1984 figures. Stop if the predicted curvature is smaller than the digitization and baseline uncertainty.
