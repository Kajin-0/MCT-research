# HgCdTe absorption-tail prior-art matrix, 1979-2007

## Scope

This matrix defines the claim boundary for Issue #225 using eight full-text primary papers supplied for audit:

1. Finkman and Nemirovsky, *Journal of Applied Physics* 50, 4356-4361 (1979), DOI `10.1063/1.326421`;
2. Finkman and Schacham, *Journal of Applied Physics* 56, 2896-2900 (1984), DOI `10.1063/1.333828`;
3. Herrmann, Moellmann, and Tomm, *Journal of Crystal Growth* 117, 758-762 (1992), DOI `10.1016/0022-0248(92)90851-9`;
4. Herrmann et al., *Journal of Applied Physics* 73, 3486-3492 (1993), DOI `10.1063/1.352954`;
5. Ariel et al., *Applied Physics Letters* 66, 2101-2103 (1995), DOI `10.1063/1.113916`;
6. Chang et al., *Journal of Electronic Materials* 33, 709-713 (2004), DOI `10.1007/s11664-004-0070-5`;
7. Chang et al., *Applied Physics Letters* 89, 062109 (2006), DOI `10.1063/1.2245220`;
8. Chang et al., *Journal of Electronic Materials* 36, 1000-1006 (2007), DOI `10.1007/s11664-007-0162-0`.

The audit distinguishes explicit source claims from consequences not stated in the papers.

## Claim matrix

| Claim | Finkman 1979 | Finkman 1984 | Herrmann 1992 | Herrmann 1993 | Ariel 1995 | Chang 2004 | Chang 2006 | Chang 2007 | Boundary for Issue #225 |
|---|---|---|---|---|---|---|---|---|---|
| HgCdTe below-edge absorption can be represented by an exponential or modified Urbach law | Explicit over `20-1000 cm^-1` | Explicit over approximately `5-1000 cm^-1` | Explicit | Explicit | Assumed below gap | Explicit | Explicit | Explicit | Established prior art |
| Gaussian distribution of local gaps is considered | No | Discussed as a possible mechanism, not fitted as Gaussian | Explicit Eq. (8) | Not primary fitted model | No; linear depth grading instead | No | No | No | Established in HgCdTe by 1992 |
| Gaussian gap convolution can look nearly exponential over a finite absorption range | No | No | Explicit for `1-100 cm^-1` | No new derivation | No | No | No | No | Established prior art; not a novelty claim |
| Source Gaussian parameter is an ordinary standard deviation | Not applicable | Not applicable | Explicit: `sigma_G=s` | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable | Repository convention corrected |
| Approximate mapping `W approximately s/2` | No | No | Explicit source statement for source-native Eqs. (2)-(6) convolved with Eq. (8) | Not independently rederived | No | No | No | No | Historical source claim; simplified power-edge model does not reproduce it |
| Empirical exponential tail joined to an intrinsic branch | Operational constant-alpha edge | Operational constant-alpha edge | Implicit region matching | Explicit | Piecewise Urbach/Kane qualitative model | Tail fitted separately | Explicit value and first-derivative matching | Explicit value and first-derivative matching | Established model architecture |
| Band filling modifies the tail or join | Not modeled | Not modeled | Included in source formulas | Explicitly modeled and tested | Acknowledged as omitted quantitative effect | Excluded for low-doped samples | Mostly excluded for selected samples | Excluded for selected 77 K samples | Competing effect; not in Issue #225 operator |
| Static versus dynamic disorder or material-property interpretation | No mechanism resolution | Tail called a material parameter for well-behaved samples; poor samples may reflect disorder | Permanent and temperature-dependent broadening | Permanent plus temperature-dependent broadening | Not mechanism study | Explicit `W(T)` model; static term reported dominant | Referred to prior work | Referred to prior work | Established phenomenology; mechanism remains non-unique |
| First derivative used to define or fit the edge | No | Tangent/zero-intercept method on transmission | Not central | Not curvature diagnostic | Explicit `d alpha/dE` peak | Photoconductivity determines gap | First derivative peaks at transition | Absorption and first derivative both fitted | First-derivative edge diagnostics are prior art |
| Second derivative of absorption used to infer gap variation | No | No | No | No | Explicit `d2 alpha/dE2` extrema for `Eg,min`, `Eg,max` | No | No | No | Direct absorption second derivatives are prior art |
| Depth-averaged local absorption over a varying gap | No | No | Real-space fluctuations discussed | Real-space fluctuations assumed | Explicit integral over linearly graded `Eg(z)` | No | No | No | Averaging local absorption over a gap distribution is prior art in a depth-gradient setting |
| Second derivative of `log(alpha)` used as a mechanism diagnostic | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Candidate contribution remains open |
| Proof that `log(alpha)` is concave for the Gaussian-power operator | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Candidate analytical result |
| Local apparent tail energy shown to increase monotonically with photon energy | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Candidate analytical result |
| Deep-tail result `sigma_G^2 d2 log(alpha)/dE2 -> -1` | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Not found | Candidate analytical result |
| Finite-dynamic-range test distinguishing Gaussian convolution from a true exponential | Not found | Not found | Not found | Not formulated | Not found | Not found | Not found | Not found | Candidate observation-design result |
| Unique conversion from Urbach energy to composition variance | Not established | Rejected as universally identifiable | Not established | Hypothesized alloy relation, not unique inversion | Linear grading inferred only under model assumptions | Static disorder combines alloy and structural terms | Not established | Not established | Unsupported |

## Paper-specific findings

### Finkman and Nemirovsky 1979

The paper measures n-type material over `0.205 <= x <= 0.220` and `80-300 K`. Multiple thicknesses from the same specimen are combined. It explicitly reports source-heating artifacts and refractive-index/thickness limitations.

For

```text
20 <= alpha <= 1000 cm^-1
```

it fits

$$
\alpha=\alpha_0
\exp\left[\frac{\sigma(E-E_0)}{T+T_0}\right].
$$

The final summary gives approximately

```text
sigma = 5.646 K cm
T0 = 80.51 K
E0 = -3109 + 1.645e4 x  cm^-1
ln(alpha0) = -20.44 + 51.70 x
```

The paper notes that the slope changes above approximately `1000 cm^-1`, and a constant-alpha edge remains an operational quantity below the true gap. Figures 3-6 contain plotted points and straight fits across four compositions and six temperatures. They are suitable for finite-window reanalysis but do not address logarithmic curvature.

### Finkman and Schacham 1984

This paper extends the modified-Urbach analysis to `x=0.29` and CdTe over `80-300 K`, combining the results with the 1979 data. The authors find the best form with `w=T+T0`, while `alpha0`, `sigma`, and `E0` remain temperature independent. Five of six HgCdTe samples agree in `sigma` and `T0` within approximately `+-5%`.

The paper calls the slope a material parameter for well-behaved specimens, but explicitly states that poor-quality samples may be dominated by composition fluctuations or lattice disorder. It cannot choose between excitonic models and elastic gap fluctuations. Therefore it is strong prior art for mechanism caution, not proof of one universal tail origin.

Figure 4 shows measured points and fits over approximately `5-1000 cm^-1`, a span of about 2.30 decades. It is the strongest current single figure for a paper-only finite-window curvature test.

### Herrmann 1992

The paper combines transmission, photocurrent, and luminescence spectroscopy. It reports exponential behavior over more than three decades, including absorption coefficients down to approximately `0.1 cm^-1` for high-quality material.

Its Eq. (8) is the ordinary Gaussian

$$
P(G)=\frac{1}{\sqrt{2\pi}s}
\exp\left[-\frac{(G-\bar G)^2}{2s^2}\right],
$$

so `sigma_G=s`.

The paper states that convolution of its Eqs. (2)-(6) with Eq. (8) gives a nearly exponential tail over `1-100 cm^-1` and an apparent broadening approximately `s/2`. This is the closest prior art to the current model. The paper does not analyze logarithmic curvature or deep-tail asymptotics.

### Herrmann 1993

This paper treats the exponential Urbach component as an empirical below-gap branch and multiplies it by a band-filling factor. The branch is joined continuously to a Kane/Anderson intrinsic branch.

It also demonstrates fit-window sensitivity empirically: a THM sample can be described by `W=3.8 meV` over approximately `130-150 meV`, whereas `W=2.1 meV` fits better over approximately `145-150 meV`. The authors do not formulate this as an identifiability theorem.

### Ariel et al. 1995

Ariel et al. use a qualitative piecewise Urbach/Kane model and explicitly average the local absorption coefficient over a linearly graded depth profile:

$$
\alpha(E)=\frac{1}{d}\int_0^d\alpha'[E,E_g(z)]\,dz.
$$

They use the maximum of `d alpha/dE` as an average-gap marker and extrema of `d2 alpha/dE2` to estimate `Eg,min` and `Eg,max`. Their experimental results report gap variation below `0.005 eV` in bulk samples, approximately `0.02 eV` in LPE layers, and inferred built-in fields of `10-20 V/cm` for LPE and around `30 V/cm` for MOCVD under a linear-gradient assumption.

This is direct prior art for derivative analysis and for averaging local absorption over a gap distribution. It remains distinct from Issue #225 because it differentiates `alpha`, not `log(alpha)`.

For a true exponential,

$$
\alpha''=\alpha/W^2>0,
$$

whereas

$$
\frac{d^2\log\alpha}{dE^2}=0.
$$

Ariel et al. also warn that noise and interference fringes require smoothing, while excessive smoothing moves derivative peaks. This preprocessing dependence must be included in any curvature recoverability study.

### Chang 2004

The paper measures temperature-dependent absorption from approximately `4.2 K` to `300 K` using an interference-matrix inversion and simultaneous photoconductivity measurements. It fits an exponential Urbach tail and models

$$
W(T)=A+B\coth\left(\frac{\hbar\omega_{LO}}{2kT}\right),
$$

separating temperature-independent static disorder from phonon-related dynamic disorder. The static contribution is reported to dominate for the measured MBE material.

The plotted absorption library is mainly in the approximate `10^2-10^4 cm^-1` range. It is valuable for intrinsic/tail joining and temperature trends but is not an ideal deep-subgap curvature dataset.

### Chang 2006

The paper constructs a nonparabolic intrinsic absorption model, then imposes an exponential Urbach law below the transition. Continuity of absorption and its first derivative gives

$$
E_0\approx E_g+\frac{W}{2}.
$$

The model does not impose second-derivative continuity and does not test logarithmic curvature.

### Chang 2007

This expanded treatment retains the same piecewise architecture and fits both the absorption coefficient and its first derivative. The data are useful for the intrinsic/tail join, but the displayed tail range begins near `10^2 cm^-1` and does not resolve the deep tail.

## Consolidated prior-art conclusion

The following statements are not novel:

- HgCdTe absorption can appear exponentially linear on a semilog plot over a finite range;
- a Gaussian distribution of local gaps can generate a nearly exponential apparent tail over a finite interval;
- derivatives of absorption can locate an average edge and estimate band-gap grading;
- a local absorption law can be averaged over a spatially varying gap.

The narrower result not found in these eight papers is:

> For the controlled Gaussian-distributed sharp power-edge operator, `log(alpha)` is concave, the local apparent tail energy is nondecreasing with photon energy, and the deep-tail logarithmic curvature approaches `-1/sigma_G^2`, so the model cannot possess a true exponential asymptote.

The associated paper-only validation target is not to prove alloy disorder. It is to determine whether published spectra have sufficient dynamic range and uncertainty control to distinguish zero log curvature from the negative curvature predicted by the controlled operator.

## Public-data suitability ranking

| Rank | Source | Use | Limitation |
|---:|---|---|---|
| 1 | Finkman 1984 Figure 4 | Clear measured points and fitted lines over approximately `5-1000 cm^-1`; strongest single finite-window test | No raw table; fitted line may bias digitization; old instrument covariance unavailable |
| 2 | Finkman 1979 Figures 3-6 | Composition, temperature, and thickness replication over approximately `20-1000 cm^-1` | About 1.70 fitted decades; source heating and optical inversion uncertainty |
| 3 | Herrmann 1992 | Deepest stated range; source Gaussian-convolution claim | Numerical points not tabulated; source-native branch complex |
| 4 | Herrmann 1993 | Multiple modalities and explicit window-dependent fitted `W` | Thick specimens and competing localized-state features |
| 5 | Chang 2007 | Digitizable absorption and first-derivative figures; detailed intrinsic model | Tail display begins near `10^2 cm^-1` |
| 6 | Ariel 1995 | Direct derivative and grading precedent; preprocessing warnings | Published figure is `d2 alpha/dE2`, not raw `alpha` for log-curvature recovery |
| 7 | Chang 2004 | Temperature and composition series; static/dynamic decomposition | Figures emphasize `10^2-10^4 cm^-1`; no measurement covariance |
| 8 | Chang 2006 | Compact analytical source for the piecewise model | Limited plotted tail data |

## Next research gate

Before manually digitizing a spectrum, construct a synthetic recoverability calculation tied to the actual panel size, symbol width, axis range, and declared absorption interval of Finkman 1984 Figure 4 and Finkman 1979 Figures 3-6. Terminate the digitization branch if the expected negative log curvature is smaller than the digitization, baseline, and smoothing uncertainty.
