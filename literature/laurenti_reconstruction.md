# Laurenti 1990 equation reconstruction

**Target:** J. P. Laurenti et al., “Temperature dependence of the fundamental absorption edge of mercury cadmium telluride,” *Journal of Applied Physics* **67**, 6454 (1990).  
**Status:** analytical formula reconstructed with high confidence; original paper, fitted dataset, validity range, and coefficient uncertainty not yet acquired.  
**Use:** benchmark baseline, not a substitute for reconstructing the original Laurenti evidence.

## Reconstructed analytical form

The equation reproduced in the supplementary material of Teppe et al. is

$$
E_g^{\mathrm L}(x,T)=
-0.303(1-x)+1.606x-0.132x(1-x)
+10^{-4}A(x)\frac{T^2}{T+B(x)},
$$

where

$$
A(x)=6.3(1-x)-3.25x-5.92x(1-x),
$$

and

$$
B(x)=11(1-x)+78.7x.
$$

Here $E_g$ is in eV, $T$ is in K, and $x$ is the Cd mole fraction in $\mathrm{Hg}_{1-x}\mathrm{Cd}_x\mathrm{Te}$.

## Evidence chain

### Primary reproduction

Teppe et al., *Nature Communications* **7**, 12576 (2016), Supplementary equation (1), explicitly attribute the equation to Laurenti et al. Their PDF text extraction preserves all coefficients but scrambles their visual ordering. The recoverable coefficient set is:

- composition terms: `0.303`, `1.606`, `0.132`;
- temperature numerator: `6.3`, `3.25`, `5.92`, $10^{-4}T^2$;
- denominator: `11`, `78.7`, and $T$.

The Nature article states that this supplementary equation reproduces the temperature-driven transition of its nominal $x=0.155$ sample near 77 K.

### Independent executable reproduction

A public scientific-analysis implementation, `Ryan3141/FTIR_Analyzer`, contains the same function:

```cpp
-0.303*(1-x) + 1.606*x - 0.132*x*(1-x)
+ (6.3*(1-x) - 3.25*x - 5.92*x*(1-x))
  * 1E-4*T*T / (11*(1-x) + 78.7*x + T)
```

This is secondary evidence, not a primary literature source, but it independently resolves the two-dimensional ordering that is lost in the PDF text extraction.

## Numerical verification

For the nominal Teppe transition sample,

$$
x=0.155,
$$

the reconstructed equation gives

$$
E_g^{\mathrm L}(0.155,77\ \mathrm K)
=-4.78\times10^{-5}\ \mathrm{eV}
=-0.0478\ \mathrm{meV},
$$

and the exact root is

$$
\boxed{T_c^{\mathrm L}(0.155)=77.124\ \mathrm K.}
$$

This agrees with the reported approximately 77 K gap closure to 0.12 K. The agreement is too specific to be explained by the corrupted coefficients being assembled arbitrarily.

Other useful checks are

$$
E_g^{\mathrm L}(0.175,2\ \mathrm K)=12.08\ \mathrm{meV},
$$

$$
E_g^{\mathrm L}(0.155,2\ \mathrm K)=-24.32\ \mathrm{meV},
$$

and

$$
x_c^{\mathrm L}(77\ \mathrm K)=0.155028.
$$

The low-temperature signed gaps are not expected to equal every optical-absorption magnitude reported by Teppe because sample labels, signed versus unsigned gap definitions, and extraction methods must be audited separately.

## Structural interpretation

The temperature term is a composition-dependent Varshni-type form:

$$
\Delta E_g(x,T)=10^{-4}A(x)\frac{T^2}{T+B(x)}.
$$

Consequently,

$$
\left.\frac{\partial E_g}{\partial T}\right|_{T=0}=0,
$$

unlike Hansen's exactly linear temperature term. At high temperature,

$$
\Delta E_g(x,T)
=10^{-4}A(x)\left[T-B(x)+O(T^{-1})\right],
$$

so the model approaches a composition-dependent linear slope while retaining low-temperature curvature.

The endpoint coefficients have clear roles:

- HgTe, $x=0$: $A=+6.3$, $B=11$ K;
- CdTe, $x=1$: $A=-3.25$, $B=78.7$ K.

The sign reversal allows the HgTe signed gap to increase with temperature while the CdTe gap decreases.

## Confidence classification

| Item | Confidence | Reason |
|---|---|---|
| algebraic formula above | high | complete coefficient set from Teppe plus independent executable reproduction and exact transition check |
| attribution to Laurenti 1990 | high | explicitly cited by Teppe and Novik |
| exact original typography | not independently viewed | original Laurenti full text unavailable |
| original samples and measurement methods | unknown | primary paper unavailable |
| fitted data, weights, exclusions, and uncertainties | unknown | primary paper unavailable |
| original validity range | unknown | primary paper unavailable |
| suitability for signed Kane gaps near inversion | empirical and measurement-dependent | Laurenti measured a fundamental absorption edge; Teppe applied the equation to a signed Kane gap |

## Benchmark rule

The reconstructed equation may now enter the common benchmark as a **published-coefficient legacy baseline**. It must not be described as a reproduced Laurenti fit until the original paper and source data are acquired.

Required scores are:

1. published coefficients with reported composition used directly;
2. published coefficients with composition uncertainty propagated;
3. comparison within optical-edge sources;
4. transfer test to signed magneto-optical gaps;
5. refit of the same functional form only after a common provenance-controlled dataset exists.
