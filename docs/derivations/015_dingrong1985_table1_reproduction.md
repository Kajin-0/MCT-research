# Dingrong 1985 Table 1 carrier-shift reproduction

## Scope

This note reproduces the finite-temperature carrier-density equation and Table 1 comparison in:

```text
Q. Dingrong et al.
Infrared absorption in In-doped degenerate Hg1-xCdxTe
Solid State Communications 56, 813-816 (1985)
DOI: 10.1016/0038-1098(85)90315-1
```

The calculation tests the source-defined Fermi elevation and its consistency with the reported operational absorption edge. It does not reproduce the complete below-gap free-carrier spectrum.

## Source-defined specimen

```text
x                         0.19
carrier type              n-type
Hall density              7.0e17 cm^-3
transmission thickness    0.16 mm
refractive index used     3.5
spectral range            7-17 um
measurement temperatures  77-300 K
edge operator             extrapolation to alpha = 2000 cm^-1
```

The Hall density is reported as approximately constant from 5 to 300 K.

## Printed density equation

The source defines

```text
eta = (Ef-Ec)/(kT)
phi = Eg/(kT)
epsilon = (E-Ec)/(kT)
```

and prints

```text
Ne = [3/(4*pi^2)] sqrt(3/2) (kT)^3/P^3
     integral_0^infinity
       epsilon^(1/2) (epsilon+phi)^(1/2) (2 epsilon+phi)
       / [1+exp(epsilon-eta)] d epsilon.
```

The reported momentum matrix is

```text
P = 8.0e-8 eV cm.
```

For fixed `Ne`, `T`, `Eg`, and `P`, the integral is monotone in `eta`. The implementation evaluates it by Gauss-Legendre quadrature on a finite interval whose upper bound is at least `max(80, eta+40)`, then solves for `eta` by bisection.

The Fermi elevation is

```text
Ef-Ec = eta*kT.
```

In the paper's notation the conduction-band minimum is the intrinsic optical-gap endpoint, so Table 1 lists this quantity as `Ef-Eg`.

## Table 1 targets

```text
T(K)   Eg(eV)   source Ef-Eg(eV)   source Ef(eV)   source Eg,op(eV)
77     0.078          0.155             0.233             0.230
100    0.085          0.153             0.238             0.238
200    0.120          0.134             0.254             0.250
300    0.154          0.117             0.271             0.268
```

`Eg,op` is not a latent quasiparticle gap. It is the source's operational edge obtained by extrapolating the measured absorption edge to `2000 cm^-1`.

## Reproduction with the printed parameter

Using the printed equation, printed density, and printed `P` gives:

```text
T(K)   reproduced Ef-Eg(eV)   residual versus Table 1 (meV)
77          0.143807                    -11.193
100         0.140528                    -12.472
200         0.123727                    -10.273
300         0.105858                    -11.142
```

```text
RMS shift discrepancy       11.297 meV
maximum absolute discrepancy 12.472 meV
```

The discrepancy is systematic and much larger than the rounding of the tabulated energies. Therefore, the printed equation and printed parameter do not jointly reproduce the printed table.

## Row-implied momentum matrix audit

At fixed tabulated `eta`, the density equation scales as `P^-3`. Each source row therefore implies

```text
P = [C(T,Eg,eta)/Ne]^(1/3),
```

where `C` contains the thermal prefactor and dimensionless integral.

The four rows independently imply:

```text
77 K    8.5078e-8 eV cm
100 K   8.5663e-8 eV cm
200 K   8.4673e-8 eV cm
300 K   8.5014e-8 eV cm
```

Their mean and sample standard deviation are:

```text
mean P   = 8.5107e-8 eV cm
sigma P  = 0.0411e-8 eV cm
```

The clustering across four temperatures is substantially tighter than the 6.38% offset from the printed `8.0e-8` value. Possible explanations include a typographical or convention mismatch, an unreported parameter choice, or cumulative rounding. The repository does not choose among these explanations without further source evidence.

## Reproduction using the row-implied mean

Using the row-implied mean as a diagnostic—not as a fitted universal material constant—gives:

```text
T(K)   reproduced shift(eV)   residual (meV)
77          0.155064              +0.064
100         0.151774              -1.226
200         0.134955              +0.955
300         0.117207              +0.207
```

```text
shift RMS discrepancy        0.785 meV
maximum shift discrepancy    1.226 meV
```

The resulting total filled edges differ from the reported operational optical gaps by at most `4.955 meV`.

The source's own tabulated filled edges differ from `Eg,op` by:

```text
3, 0, 4, 3 meV
```

with RMS `2.915 meV`. This quantifies the agreement claimed by the authors while retaining the operational edge definition.

## Comparison with the previous illustrative model

The repository's earlier zero-temperature sensitivity example used:

```text
n           7e17 cm^-3
m_edge      0.010 m0
alpha       7.5 eV^-1
m_valence   0.35 m0
BGR         0
```

and produced a temperature-independent filling shift of `148.367 meV` because those illustrative parameters were not temperature dependent.

Against the four Dingrong shifts, its residuals are:

```text
-6.633, -4.633, +14.367, +31.367 meV
```

with RMS `17.718 meV`. The illustrative model therefore does not reproduce the real source temperature trend and remains a bounded sensitivity calculation rather than a specimen fit.

## Scientific interpretation

The useful result is twofold:

1. The finite-temperature Kane density formulation captures the structure of the four-temperature carrier shift much better than the previous constant zero-temperature sensitivity estimate.
2. The paper contains a source-internal numerical inconsistency between its printed `P` and Table 1. Reproducing the paper requires reporting that inconsistency, not silently changing the input.

## Claim boundaries

- The row-implied `P` is not a new universal HgCdTe momentum matrix.
- The source intrinsic-gap values are inputs, not validation of a universal gap equation.
- The comparison does not infer band-gap renormalization.
- `Eg,op` remains an operational `2000 cm^-1` extrapolated edge.
- Table 1 is not a calibrated native spectrum or covariance-bearing dataset.
- The complete below-gap Haga-Tang model is not reconstructed because the paper refers to external functions and two-mode effective-charge definitions.
- External source-table reproduction is complete; complete external material-spectrum validation is not.

## Controlling implementation and record

```text
src/mct_research/dingrong1985.py
data/validation/dingrong1985_table1_reproduction.json
tests/test_dingrong1985.py
tests/test_dingrong1985_record.py
```
