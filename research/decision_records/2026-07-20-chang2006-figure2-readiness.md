# Chang 2006 Figure 2 replication readiness

**Date:** 2026-07-20  
**Issue:** #149  
**Parent program:** #132

## Question

Can the published Chang et al. 2006 Figure 2 provide a quantitative real-spectrum validation of the committed nonparabolic-Urbach observation operator?

## Source identity

```text
Y. Chang et al.
Narrow gap HgCdTe absorption behavior near the band edge including nonparabolicity and the Urbach tail
Applied Physics Letters 89, 062109 (2006)
DOI 10.1063/1.2245220
source asset SHA-256 37a08e3fc37fc3b795b1a9d7ac3b3b662f9f96c2cad4cddbf79bc0fe3b57b41d
```

No copyrighted source file, page image, figure crop, or digitized curve is committed.

## Source-readiness audit

Figure 2 is not a provenance-complete numerical dataset.

```text
figure composition                         x = 0.21
caption temperature                        80 K
body/conclusion temperature                77 K
native numeric absorption data             not recovered
calibration metadata                       not recovered
same-specimen Urbach width W               not reported
same-specimen hyperbola parameter b        not reported
Figure 2 fitted Eg, W, b, and amplitude     not tabulated
carrier density                            only low 10^15 cm^-3 range
```

The paper reports `b = 103 +/- 2 meV` for a separate `x=0.23`, `77 K` band calculation. It is not the Figure 2 specimen and is not authorized as an exact `x=0.21` input.

The source also states that the Urbach width may vary between specimens and across locations within one specimen. A same-lineage or nearby-composition value therefore cannot substitute for same-specimen, same-area provenance.

## Synthetic confounding screen

The readiness audit uses a declared synthetic curve only:

```text
Eg = 0.100 eV
W  = 0.012 eV
b  = 0.100 eV
A  = 50000 cm^-1
105 spectral points from 0.088 to 0.400 eV
```

The hypothetical coordinate screen assumes:

```text
sigma_E          = 0.0005 eV
sigma_ln(alpha)  = 0.03
```

These values are not assigned to the published figure. They are used only to determine whether figure coordinate precision or missing physical parameters are the controlling limitation.

The local weighted Jacobian in `[Eg, ln W, ln b, ln A]` gives:

```text
condition number                    255.688
corr(Eg, ln W)                        0.731
corr(Eg, ln b)                        0.801
corr(ln b, ln A)                     -0.930
linearized sigma(Eg)                  0.345 meV
```

This shows substantial parameter correlation even under an idealized correct-model synthetic case.

## Fixed-parameter transfer sensitivity

When only `Eg` and amplitude are fitted to the exact synthetic curve, modest errors in fixed transferred parameters shift the recovered edge:

```text
W error       edge bias
-20%          -1.720 meV
-10%          -0.825 meV
+10%          +0.765 meV
+20%          +1.490 meV

b error       edge bias
-10%          -0.975 meV
 -5%          -0.470 meV
 +3%          +0.265 meV
 +5%          +0.435 meV
+10%          +0.835 meV
```

A `+10%` error in `W` leaves a root-mean-square log residual of only `0.0201`. A `+3%` error in `b` leaves a residual of `0.00568`. Curves can therefore appear visually close while the edge moves by a scientifically relevant fraction of a meV to more than a meV.

These are deterministic sensitivities of the declared synthetic case, not uncertainty estimates for the real specimen.

## Decision

### Authorized

- preserve Figure 2 as evidence that the model was compared with an experimental `x=0.21` absorption curve;
- use the source as a high-priority native-data and parameter-provenance recovery target;
- use the synthetic audit to demonstrate why same-specimen `W` and `b` are required;
- apply the committed operator to a future native spectrum only under its existing provenance and domain gates.

### Unauthorized

- digitize Figure 2 into a material-gap point;
- claim the plotted curve quantitatively validates the repository operator;
- assign the synthetic `0.345 meV` value as the uncertainty of Figure 2;
- transfer the reported `x=0.23` value of `b` as exact for `x=0.21`;
- infer `W` from another specimen or measurement area;
- choose between 77 K and 80 K without source clarification;
- fit `Eg`, `W`, `b`, and amplitude freely from the published plot and describe the result as a source reproduction.

## Reopening gate

Quantitative real-spectrum validation requires:

1. native numerical absorption data and calibration;
2. same-specimen, same-area Urbach-width provenance;
3. same-specimen `b` provenance or independently fixed band parameters;
4. resolved measurement temperature;
5. explicit carrier-state metadata;
6. a predeclared fit window and uncertainty propagation.

Until those conditions are met:

```text
quantitative operator validation        blocked
Figure digitization for gap inference   blocked
screen-only source recovery             high priority
material-gap fit authority              blocked
```
