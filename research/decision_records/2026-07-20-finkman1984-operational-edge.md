# Finkman-Schacham 1984 operational-edge semantics

**Date:** 2026-07-20  
**Source:** DOI `10.1063/1.333828`

## Question

Does Finkman and Schacham 1984 provide an intrinsic HgCdTe band-gap law, or a source-bound absorption observation operator whose historically labeled `Eg` is an operational detector-related threshold?

## Source evidence

The directly measured HgCdTe material consists of six n-type `x=0.29` specimens from different crystals, produced by solid-state recrystallization or Bridgman growth. Reported metadata are:

```text
composition deviation             +/-0.005
carrier density at 77 K           0.9-3e15 cm^-3
Hall mobility at 77 K             3-5e4 cm^2/V s
sample thickness                  25-300 um
temperature range                 80-300 K
temperature stability             +/-0.3 K
instrument                        Perkin-Elmer 683
```

The empirical Hg-rich operator combines these measurements with prior `x approximately 0.205-0.220` data. Its conservative common domain is:

```text
0.205 <= x <= 0.29
80 <= T <= 300 K
20 <= alpha <= 1000 cm^-1
```

## Source-bound operator

Source Eq. (10) is preserved as an energy-at-fixed-absorption operator:

```text
E_alpha(alpha,T,x) =
  (T+81.9)/(3.267e4*(1+x))
  * [ln(alpha)+18.88-53.61*x]
  -0.3424 + 1.838*x + 0.148*x^4
```

The source then defines the quantity it calls `Eg` at:

```text
alpha = 500 cm^-1
```

because this crossing approximately represents the half-peak response of a 10 um photoconductive detector. The repository therefore names it:

```text
energy_at_alpha_500_cm1
```

It is a fixed-absorption-threshold observation, not an identified latent material gap.

The separately printed Eq. (11) is a rounded closed form of Eq. (10) at `alpha=500 cm^-1`. Across the declared domain, the rounded form is lower by `0.087-0.257 meV`. The two expressions must not be asserted to be machine-identical.

## Threshold dependence

The energy span between `alpha=20` and `1000 cm^-1` is:

```text
x=0.215,  80 K      15.955956 meV
x=0.215, 300 K      37.637923 meV
x=0.290,  80 K      15.028284 meV
x=0.290, 300 K      35.449671 meV
```

These are differences between declared observation operators. They are not uncertainty estimates for an intrinsic gap.

## Zero-intercept semantics

Source Eq. (12) gives the absorption coefficient at the transmission zero intercept:

```text
alpha_zero_intercept = e/d_cm
```

For `d=500 um`, this is `54.3656365692 cm^-1`, not `500 cm^-1`. At 300 K, the corresponding zero-intercept edge lies below the alpha-500 operational edge by:

```text
x=0.215      -21.348002 meV
x=0.290      -20.106840 meV
```

The source's Eq. (13) uses a different variable: `Zi` is the zero-intercept **cut-on wavenumber** in `cm^-1`, not the absorption coefficient. Its composition calibration is restricted to 300 K and 500 um thickness:

```text
x = 7.785e-2 + 1.096e-4*Zi - 3.713e-9*Zi^2
```

The absorption coefficient `e/d`, cut-on wavenumber `Zi`, and alpha-500 edge are therefore three distinct quantities.

## Decision

Authorized:

- preserve Finkman 1984 as exact historical operational-edge evidence;
- use Eq. (10) as a source-bound threshold operator inside its declared domain;
- preserve Eq. (11) with its rounding residual;
- use Eq. (12) and Eq. (13) only with their thickness, temperature, and variable semantics explicit;
- use the source as direct evidence that historically reported `Eg` values can encode detector-related observation choices.

Unauthorized:

- treat the alpha-500 edge as an intrinsic material-gap point;
- fit a universal HgCdTe gap law from this operator;
- pool the edge with magneto-optical gaps by default;
- interchange zero-intercept, alpha-500, detector cutoff, and latent-gap quantities;
- extrapolate the x^4 expression outside the declared Hg-rich domain;
- treat the approximate 10 um detector half-peak relationship as exact device physics;
- apply the Eq. (13) composition calibration outside 300 K and 500 um without the source correction.

## Program consequence

This source directly strengthens the controlling observation-model thesis: a quantity printed as `Eg` can be an operational threshold selected for detector relevance. Historical labels alone are insufficient to establish a common latent-gap observation class.
