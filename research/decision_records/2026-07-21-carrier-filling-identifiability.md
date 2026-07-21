# Decision record: degenerate carrier-filled edge foundation

**Date:** 2026-07-21  
**Issue:** #175  
**Status:** candidate controlling result pending PR validation

## Decision

Adopt a declared zero-temperature spherical nonparabolic carrier model as the first executable carrier-filled edge operator.

Authorize it for:

1. separating latent gap, conduction filling, valence recoil, band-gap renormalization, and observation shifts;
2. quantifying failure of a parabolic Burstein-Moss estimate;
3. identifying measurement-design requirements;
4. bounded sensitivity analysis in the Dingrong 1985 density regime.

Do not authorize it as a complete reproduction of Dingrong's temperature-dependent edge or free-carrier absorption spectra.

## Analytical model

For one spin-degenerate spherical valley,

$$
k_F=(3\pi^2n)^{1/3}.
$$

The parabolic conduction energy is

$$
E_{\mathrm{par}}=\frac{\hbar^2k_F^2}{2m_e^*}.
$$

The declared nonparabolic branch satisfies

$$
E_c(1+\alpha E_c)=E_{\mathrm{par}}.
$$

The exact positive solution is

$$
E_c=\frac{2E_{\mathrm{par}}}
{1+\sqrt{1+4\alpha E_{\mathrm{par}}}}.
$$

With

$$
q=\alpha E_{\mathrm{par}},
$$

the parabolic relative overestimate is

$$
\boxed{
\frac{E_{\mathrm{par}}-E_c}{E_c}
=\frac{\sqrt{1+4q}-1}{2}
}.
$$

## Dingrong-density sensitivity result

Declared illustrative parameters:

```text
n          7.0e17 cm^-3
Eg0        0.100 eV
m_edge     0.010 m0
alpha      7.5 eV^-1
m_valence  0.35 m0
C_BGR      0.020 eV at 1e18 cm^-3
```

The parameters are not inferred for the Dingrong specimen.

Results:

```text
k_F                              0.0274688 A^-1
parabolic conduction energy      287.476 meV
nonparabolic conduction energy   140.154 meV
valence recoil                     8.214 meV
nonparabolic BM shift             148.367 meV
parabolic BM shift                295.690 meV
parabolic overestimate            147.323 meV
q = alpha*E_par                     2.1561
```

The fully parabolic filling shift is 1.993 times the nonparabolic result.

For the declared parameter set, the parabolic conduction error grows from `0.0046 meV` at `1e14 cm^-3` to `147.323 meV` at `7e17 cm^-3`. A 5% conduction-energy error occurs near `2.66e15 cm^-3`.

## Separate edge terms

The controlling observation model is

$$
E_{\mathrm{opt}}
=E_g^{(0)}
+\Delta E_{\mathrm{BM}}
+\Delta E_{\mathrm{BGR}}
+\Delta E_{\mathrm{obs}}.
$$

Positive filling and negative renormalization must not be collapsed into one empirical carrier correction.

For the illustrative density-scaled renormalization

$$
\Delta E_{\mathrm{BGR}}
=-C_{18}(n/10^{18})^{1/3},
$$

the declared case gives `-17.758 meV` and an illustrative optical edge of `230.609 meV`. This is not a Dingrong data-point reproduction.

## Identifiability result

One edge at one density is one scalar observation and has Jacobian rank at most one for parameters

```text
ln Eg0
ln m_edge
ln alpha
ln m_valence
ln C_BGR
```

A five-density series at

```text
1e16, 3e16, 1e17, 3e17, 7e17 cm^-3
```

has singular values

```text
2.55477493e-1
6.63828971e-2
4.64192311e-3
1.81849453e-4
2.31520896e-5
```

and local rank five, but

```text
condition number = 11034.75
weakest relative singular value = 9.06e-5
```

Formal full rank does not make an unconstrained five-parameter inversion reliable.

## Authorized conclusions

- Nonparabolicity can dominate the carrier-filling correction at the Dingrong density scale.
- A parabolic Burstein-Moss estimate can be wrong by an energy comparable to or greater than a narrow HgCdTe gap.
- One optical edge cannot separately identify latent gap, masses, nonparabolicity, and renormalization.
- A density series can restore local rank while remaining severely ill-conditioned.
- Independent Hall, mass, low-density gap, and renormalization information are required.

## Unauthorized conclusions

- The illustrative parameter set is not assigned to the Dingrong specimen.
- The illustrative optical edge is not compared as a source data point.
- The model is not a finite-temperature source reproduction.
- The free-carrier absorption background and two-mode phonon scattering are not implemented.
- The Dingrong correction is not transferred to low-density detector material.
- No universal HgCdTe band-gap-renormalization coefficient is identified.

## Validation gates

Merge requires:

- exact density-to-wavevector conversion;
- exact solution of the nonparabolic dispersion;
- parabolic and low-density limits;
- Dingrong-density numerical regression;
- monotonic density-crossover error;
- one-density rank-one confirmation;
- five-density rank and condition-number confirmation;
- input validation, public export, and complete GitHub Actions success on Python 3.11 and 3.13.

## Next decision

After merge, either:

1. recover sufficient source equations and spectra to implement Dingrong free-carrier absorption and temperature dependence; or
2. if source recovery remains incomplete, proceed to a combined carrier-plus-tail identifiability map and retain the Dingrong result as a bounded high-density sensitivity anchor.
