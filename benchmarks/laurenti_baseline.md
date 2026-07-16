# Laurenti legacy baseline and Hansen comparison

**Status:** analytical formula implemented and numerically verified; no experimental model ranking yet.  
**Implementation:** `mct_research.gap_models.laurenti_gap_ev`  
**Provenance:** high-confidence reconstruction documented in `literature/laurenti_reconstruction.md`.

## 1. Legacy models

### Hansen 1982

$$
E_g^{\mathrm H}(x,T)=
-0.302+1.93x-0.81x^2+0.832x^3
+5.35\times10^{-4}T(1-2x).
$$

### Laurenti 1990

$$
E_g^{\mathrm L}(x,T)=
-0.303(1-x)+1.606x-0.132x(1-x)
+10^{-4}A(x)\frac{T^2}{T+B(x)},
$$

with

$$
A(x)=6.3(1-x)-3.25x-5.92x(1-x),
$$

$$
B(x)=11(1-x)+78.7x.
$$

## 2. Structural difference

Hansen imposes

$$
\frac{\partial^2E_g^{\mathrm H}}{\partial T^2}=0.
$$

Laurenti instead gives

$$
\frac{\partial E_g^{\mathrm L}}{\partial T}
=10^{-4}A(x)\frac{T[T+2B(x)]}{[T+B(x)]^2},
$$

and

$$
\boxed{
\frac{\partial^2E_g^{\mathrm L}}{\partial T^2}
=2\times10^{-4}A(x)\frac{B(x)^2}{[T+B(x)]^3}
}.
$$

Therefore

$$
\left.\frac{\partial E_g^{\mathrm L}}{\partial T}\right|_{T=0}=0,
$$

while its high-temperature slope tends to

$$
\lim_{T\to\infty}
\frac{\partial E_g^{\mathrm L}}{\partial T}
=10^{-4}A(x).
$$

The two legacy equations consequently test different physical hypotheses even before any coefficients are refitted:

- Hansen: temperature dependence is affine at every composition;
- Laurenti: temperature dependence crosses over from quadratic near zero temperature to an asymptotically linear regime.

## 3. Numerical comparison

All entries below are signed gaps in meV using the published coefficients.

| $x$ | $T$ (K) | Hansen | Laurenti | Laurenti − Hansen |
|---:|---:|---:|---:|---:|
| 0.150 | 2 | -27.17 | -33.41 | -6.24 |
| 0.150 | 77 | +0.92 | -8.64 | -9.56 |
| 0.155 | 2 | -18.47 | -24.32 | -5.85 |
| 0.155 | 77 | +9.21 | -0.05 | -9.26 |
| 0.155 | 120 | +25.09 | +16.77 | -8.32 |
| 0.175 | 2 | +16.10 | +12.08 | -4.02 |
| 0.175 | 77 | +42.18 | +34.43 | -7.75 |
| 0.200 | 77 | +82.97 | +77.78 | -5.19 |
| 0.250 | 77 | +163.47 | +165.34 | +1.86 |
| 0.300 | 77 | +243.04 | +253.98 | +10.94 |

The difference changes sign with composition. A single global energy offset cannot map one equation into the other.

## 4. Critical-temperature comparison

| $x$ | $T_c^{\mathrm H}$ (K) | $T_c^{\mathrm L}$ (K) | Laurenti − Hansen |
|---:|---:|---:|---:|
| 0.145 | 96.47 | 119.51 | +23.04 |
| 0.150 | 74.54 | 98.83 | +24.29 |
| 0.155 | 52.04 | 77.12 | +25.08 |
| 0.160 | 28.94 | 54.03 | +25.09 |
| 0.165 | 5.20 | 28.30 | +23.09 |

Near the inversion transition, the two historical equations differ by roughly 23–25 K over a broad composition interval. This is large enough to be experimentally discriminable only when composition uncertainty is controlled at the level established in `docs/insights/0012_critical_temperature_composition_identifiability.md`.

## 5. Teppe consistency check

For nominal $x=0.155$,

$$
T_c^{\mathrm L}=77.124\ \mathrm K,
$$

which matches Teppe's reported transition near 77 K. This verifies the reconstructed transcription because Teppe explicitly used the Laurenti equation. It is **not** an independent validation of Laurenti's physical accuracy: the same paper is part of the reproduction chain, and its nominal composition may be equation-calibrated or composition-limited.

## 6. Benchmark requirements

Both legacy equations must be scored under identical conditions:

1. published coefficients, nominal reported composition;
2. published coefficients, composition uncertainty propagated;
3. optical-edge sources only;
4. signed magneto-optical sources only;
5. source-level holdout;
6. measurement-class transfer;
7. full temperature curves with one shared latent composition per specimen.

The decisive diagnostic is not whether Laurenti passes through the Teppe critical point. It is whether its nonzero curvature and composition dependence reduce held-out residual structure across independently calibrated specimens and measurement classes.

## 7. Current interpretation

Laurenti is the correct second legacy baseline for this project because it introduces low-temperature curvature without adding a free fit to the reconstructed benchmark. It also establishes that replacing Hansen's linear temperature term with a nonlinear thermal law is historically prior art. Any novel successor must therefore improve on both Hansen and Laurenti, not Hansen alone.
