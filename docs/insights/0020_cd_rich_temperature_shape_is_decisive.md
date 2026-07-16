# Insight 0020 — Cd-rich within-specimen temperature shifts decisively separate Hansen and Laurenti

**Status:** exact comparison of published equations; experimental test design; not a validation result

## Problem

Absolute-gap comparisons are often dominated by composition offsets and measurement-class differences. A stronger observable on one fixed specimen is the thermal shift relative to a low-temperature reference:

$$
\Delta_T E_g^{M}(x,T;T_0)
=
E_g^{M}(x,T)-E_g^{M}(x,T_0),
$$

where $M$ is Hansen or Laurenti.

Define the model-shape separation

$$
D(x,T;T_0)
=
\Delta_T E_g^{\mathrm L}(x,T;T_0)
-
\Delta_T E_g^{\mathrm H}(x,T;T_0).
$$

Using $T_0=2$ K removes most fixed calibration and intercept differences.

## Main result

For Laurenti’s directly measured Cd-rich specimens, the predicted separation grows rapidly with composition and temperature:

| $x$ | $D(77\,\mathrm K)$ | $D(150\,\mathrm K)$ | $D(300\,\mathrm K)$ |
|---:|---:|---:|---:|
| 0.500 | 0.22 meV | 0.52 meV | 1.17 meV |
| 0.620 | 5.00 meV | 7.75 meV | 12.37 meV |
| 0.710 | 9.46 meV | 14.98 meV | 24.38 meV |
| 0.805 | 14.85 meV | 24.12 meV | 40.21 meV |
| 0.925 | 22.53 meV | 37.69 meV | 64.60 meV |
| 0.955 | 24.59 meV | 41.41 meV | 71.43 meV |
| 0.970 | 25.63 meV | 43.32 meV | 74.96 meV |
| 1.000 | 27.77 meV | 47.22 meV | 82.21 meV |

The high-Cd series are therefore much more informative about thermal-law shape than the narrow-gap detector compositions.

## Composition uncertainty is not the limiting factor for this test

For a fixed specimen, uncertainty in $x$ affects the separation through

$$
\sigma_{D,x}
=
\left|\frac{\partial D}{\partial x}\right|\sigma_x.
$$

At $x=0.970$, $T=300$ K, and a deliberately conservative

$$
\sigma_x=0.003,
$$

we obtain

$$
\sigma_{D,x}=0.71\ \mathrm{meV},
$$

while

$$
D=74.96\ \mathrm{meV}.
$$

If each edge value has independent 3 meV uncertainty, the two-temperature shift has

$$
\sigma_{\Delta E}=\sqrt{2}(3\ \mathrm{meV})=4.24\ \mathrm{meV}.
$$

Combining this with composition uncertainty gives approximately

$$
\sigma_D=4.30\ \mathrm{meV},
$$

or a nominal model separation of

$$
\boxed{17.4\sigma.}
$$

This significance is an experiment-design estimate. Real systematic correlation and digitization uncertainty must be modeled separately.

## Optimal digitization order

The Figure 2 extraction should not begin by digitizing every curve equally.

1. Digitize $x=0.970$, $0.955$, and $0.925$ first, emphasizing the lowest and highest measured temperatures.
2. Digitize $x=0.805$ as an intermediate-composition cross-check.
3. Use $x=0.500$ as a near-null control: both equations predict nearly temperature-independent behavior there.
4. Preserve the full specimen grouping so differences are scored as within-specimen shifts.
5. Digitize inherited Hg-rich series only after the direct LPE series because their composition values were adjusted during model construction.

## Scientific implication

The immediate Hansen-versus-Laurenti thermal-law question does not require AHC. It can be resolved by the already published Cd-rich experimental series if those points are digitized accurately.

The narrow-gap region remains important for inversion physics, but it is a poor first arena for distinguishing these two empirical thermal forms because their within-specimen shift difference is only a few meV there.

## Stop rule

If the Cd-rich direct series do not distinguish the equations after source-aware digitization, uncertainty propagation, and specimen-level fitting, then the available figure resolution is inadequate and author-supplied numerical data should be requested before introducing a more complex analytical model.
