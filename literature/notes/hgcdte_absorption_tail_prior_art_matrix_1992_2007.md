# HgCdTe absorption-tail prior-art matrix, 1992-2007

## Scope

This matrix defines the claim boundary for Issue #225 using five full-text papers supplied for audit:

1. Herrmann, Moellmann, and Tomm, *Journal of Crystal Growth* 117, 758-762 (1992), DOI `10.1016/0022-0248(92)90851-9`;
2. Herrmann et al., *Journal of Applied Physics* 73, 3486-3492 (1993), DOI `10.1063/1.352954`;
3. Chang et al., *Journal of Electronic Materials* 33, 709-713 (2004), DOI `10.1007/s11664-004-0070-5`;
4. Chang et al., *Applied Physics Letters* 89, 062109 (2006), DOI `10.1063/1.2245220`;
5. Chang et al., *Journal of Electronic Materials* 36, 1000-1006 (2007), DOI `10.1007/s11664-007-0162-0`.

The audit distinguishes explicit source claims from consequences not stated in the papers.

## Claim matrix

| Claim | Herrmann 1992 | Herrmann 1993 | Chang 2004 | Chang 2006 | Chang 2007 | Boundary for Issue #225 |
|---|---|---|---|---|---|---|
| HgCdTe below-edge absorption can be represented by an exponential Urbach law | Explicit | Explicit | Explicit | Explicit | Explicit | Established prior art |
| Gaussian distribution of local gaps is considered | Explicit Eq. (8) | Not used as the primary fitted tail model | No | No | No | Established in HgCdTe by 1992 |
| Gaussian gap convolution can look nearly exponential over a finite absorption range | Explicit for `1-100 cm^-1` | No new Gaussian-convolution derivation | No | No | No | Established prior art; not a novelty claim |
| Source Gaussian parameter is an ordinary standard deviation | Explicit: `sigma_G=s` | Not applicable | Not applicable | Not applicable | Not applicable | Repository convention corrected |
| Approximate mapping `W approximately s/2` | Explicit source statement for source-native Eqs. (2)-(6) convolved with Eq. (8) | Not independently rederived | No | No | No | Historical claim; simplified power-edge model does not reproduce it |
| Empirical exponential tail joined continuously to an intrinsic branch | Implicit region matching | Explicit | Tail fitted separately | Explicit value and first-derivative matching | Explicit value and first-derivative matching | Established model architecture |
| Band filling modifies the tail | Included in source intrinsic formulas | Explicitly modeled and tested by pumped absorption | Excluded for low-doped samples | Mostly excluded for selected low-doped samples | Excluded for selected 77 K low-doped samples | Competing effect; not in Issue #225 operator |
| Static versus dynamic disorder decomposition | Discussed qualitatively and through temperature behavior | Permanent plus temperature-dependent broadening | Explicit `W(T)` model; static term reported dominant | Referred to prior work | Referred to prior work | Established phenomenology; not mechanism identification |
| First derivative used to define or fit the optical edge | Not central | No curvature diagnostic | Photoconductivity used to determine gap | First derivative peaks at transition | Absorption and first derivative both fitted | First derivative prior art |
| Second derivative of `log(alpha)` used as a mechanism diagnostic | Not found | Not found | Not found | Not found | Not found | Candidate contribution remains open |
| Proof that `log(alpha)` is concave for the Gaussian-power operator | Not found | Not found | Not found | Not found | Not found | Candidate analytical result |
| Local apparent tail energy shown to increase monotonically with photon energy | Not found | Not found | Not found | Not found | Not found | Candidate analytical result |
| Deep-tail result `sigma_G^2 d2 log(alpha)/dE2 -> -1` | Not found | Not found | Not found | Not found | Not found | Candidate analytical result |
| Finite-dynamic-range test distinguishing Gaussian convolution from a true exponential | Not found | Not found | Not found | Not found | Not found | Candidate observation-design result |
| Unique conversion from Urbach energy to composition variance | Not established | Hypothesized alloy relation, not unique inversion | Static disorder combines alloy and structural terms | Not established | Not established | Unsupported |

## Paper-specific findings

### Herrmann 1992

The paper combines transmission, photocurrent, and luminescence spectroscopy. It reports exponential behavior over more than three decades, including absorption coefficients down to approximately `0.1 cm^-1` for high-quality material.

Its Eq. (8) is the ordinary Gaussian

$$
P(G)=\frac{1}{\sqrt{2\pi}s}
\exp\left[-\frac{(G-\bar G)^2}{2s^2}\right],
$$

so `sigma_G=s`.

The paper states that convolution of its Eqs. (2)-(6) with Eq. (8) gives a nearly exponential tail over `1-100 cm^-1` and an apparent broadening approximately `s/2`. This is the closest prior art to the current work.

The paper does not analyze logarithmic curvature or deep-tail asymptotics. It also identifies shallow-level contributions and does not claim that every observed tail is uniquely due to alloy-gap fluctuations.

### Herrmann 1993

This paper treats the exponential Urbach component as an empirical below-gap branch and multiplies it by a band-filling factor. The branch is joined continuously to a Kane/Anderson intrinsic branch. Pumped-absorption measurements support the bandlike character of states involved in the fitted tail.

The paper assumes that permanent broadening is associated with real-space band-edge fluctuations due to alloy disorder, but it also discusses localized states and carrier-state effects. It does not derive the Gaussian-convolution curvature theorem.

The paper itself demonstrates fit-window sensitivity indirectly: a THM sample can be described by `W=3.8 meV` over approximately `130-150 meV`, whereas `W=2.1 meV` fits better only over approximately `145-150 meV`. This is empirical evidence that a reported tail width depends on the fitted spectral interval, although the authors do not formulate the observation as a structural identifiability theorem.

### Chang 2004

The paper measures temperature-dependent absorption from approximately `4.2 K` to `300 K` using an interference-matrix inversion and simultaneous photoconductivity measurements. It fits an exponential Urbach tail and models

$$
W(T)=A+B\coth\left(\frac{\hbar\omega_{LO}}{2kT}\right),
$$

separating temperature-independent static disorder from phonon-related dynamic disorder. The static contribution is reported to dominate for the measured MBE material.

The paper reports lateral composition standard deviation approximately `0.0006` for one `x=0.2182` wafer, corresponding to approximately `0.8 meV` total gap shift, and argues that lateral nonuniformity is negligible for its transmission measurements. That statement concerns the mapped macroscopic wafer variation, not necessarily microscopic local-gap statistics.

The plotted absorption library is mainly in the approximate `10^2-10^4 cm^-1` range. It is valuable for intrinsic/tail joining and temperature trends but is not an ideal deep-subgap curvature dataset.

### Chang 2006

The paper constructs a nonparabolic intrinsic absorption model from hyperbolic conduction/light-hole bands and a heavy-hole branch, then imposes an exponential Urbach law below the transition.

The join requires continuity of the absorption coefficient and its first derivative, giving

$$
E_0\approx E_g+\frac{W}{2}.
$$

The model does not impose second-derivative continuity and does not test whether the below-gap data have zero or negative logarithmic curvature. The measured range is reported as approximately `10^2-10^4 cm^-1`.

### Chang 2007

This expanded treatment retains the same piecewise architecture and provides more detail on the 14-band-derived intrinsic branch. It fits both the absorption coefficient and its first derivative. Figure 3 contains a published `x=0.21`, approximately `80 K` spectrum, and Figure 4 compares the first derivative of data and model.

The data are potentially digitizable for testing the transition and intrinsic branch, but the displayed tail range is again approximately `10^2 cm^-1` and above. It does not resolve the deep tail needed to estimate the predicted asymptotic curvature.

## Consolidated prior-art conclusion

The following statement is not novel:

> A Gaussian distribution of HgCdTe local gaps can generate a nearly exponential apparent absorption tail over a finite observation interval.

Herrmann 1992 states this explicitly.

The narrower result not found in these five papers is:

> For the controlled Gaussian-distributed sharp power-edge operator, `log(alpha)` is concave, the local apparent tail energy is nondecreasing with photon energy, and the deep-tail logarithmic curvature approaches `-1/sigma_G^2`, so the model cannot possess a true exponential asymptote.

The associated paper-only validation target is not to prove alloy disorder. It is to determine whether published spectra have sufficient dynamic range and uncertainty control to distinguish zero log curvature from the negative curvature predicted by the controlled operator.

## Public-data suitability ranking

| Rank | Source | Use | Limitation |
|---:|---|---|---|
| 1 | Herrmann 1992 | Deepest stated dynamic range; source convolution claim; historical benchmark | Numerical absorption points are not tabulated; source-native intrinsic branch is complex |
| 2 | Herrmann 1993 | Multiple modalities and explicit window-dependent fitted `W`; pumped absorption | Thick specimens limit high-absorption transmission accuracy in some figures |
| 3 | Chang 2007 | Digitizable absorption and first-derivative figures; detailed intrinsic model | Tail display begins near `10^2 cm^-1`; insufficient deep-tail range |
| 4 | Chang 2004 | Temperature and composition series; static/dynamic decomposition | Figures emphasize `10^2-10^4 cm^-1`; no reported measurement covariance |
| 5 | Chang 2006 | Compact analytical source for the piecewise model | Short paper and limited plotted tail data |

## Next literature targets

The highest-value next sources are papers with raw or finely plotted absorption below `1 cm^-1`, explicit specimen thickness, and declared spectral resolution. Priority should be given to the original Finkman/Schacham HgCdTe exponential-tail measurements and the 1995 absorption-derivative paper cited by Herrmann 1993.
