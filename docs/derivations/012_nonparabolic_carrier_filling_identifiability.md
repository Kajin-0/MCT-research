# Derivation 012: nonparabolic carrier filling and edge identifiability

## 1. Scope

This derivation separates the optical effect of occupied conduction states from the latent zero-density HgCdTe gap.

The model includes:

- a zero-temperature spherical Fermi surface;
- one spin-degenerate valley, with configurable valley multiplicity;
- a Kane-type nonparabolic conduction branch;
- a parabolic valence recoil at the same vertical-transition wavevector;
- an optional negative density-scaled band-gap-renormalization term;
- a separate observation shift.

It does not yet include finite-temperature Fermi integrals, free-carrier absorption, anisotropy, multiple valleys, excitons, disorder tails, or a source-specific Dingrong parameter set.

## 2. Density and Fermi wavevector

For valley degeneracy $g_v$ and electron density $n$,

$$
n=\frac{g_v k_F^3}{3\pi^2}.
$$

Therefore

$$
\boxed{
k_F=\left(\frac{3\pi^2 n}{g_v}\right)^{1/3}
}.
$$

For

$$
n=7.0\times10^{17}\ \mathrm{cm^{-3}},
\qquad g_v=1,
$$

one obtains

$$
k_F=0.0274688\ \mathrm{\AA^{-1}}.
$$

## 3. Parabolic conduction estimate

Let $m_e^*$ be the band-edge conduction mass. The parabolic kinetic energy is

$$
E_{\mathrm{par}}
=\frac{\hbar^2 k_F^2}{2m_e^*}.
$$

Using

$$
\frac{\hbar^2}{2m_0}
=3.809982116\ \mathrm{eV\,\AA^2}
$$

and the declared sensitivity value

$$
m_e^*=0.010m_0,
$$

gives

$$
E_{\mathrm{par}}=287.476\ \mathrm{meV}.
$$

This value is not automatically the physical Fermi energy in a narrow-gap nonparabolic band.

## 4. Kane-type nonparabolic branch

Use the declared dispersion

$$
E_c(1+\alpha E_c)=E_{\mathrm{par}},
$$

where $\alpha$ has units of inverse energy.

The positive solution is

$$
\boxed{
E_c
=\frac{\sqrt{1+4\alpha E_{\mathrm{par}}}-1}{2\alpha}
=\frac{2E_{\mathrm{par}}}
{1+\sqrt{1+4\alpha E_{\mathrm{par}}}}
}.
$$

The rationalized form is numerically stable when $\alpha E_{\mathrm{par}}$ is small.

Define the dimensionless nonparabolicity parameter

$$
q=\alpha E_{\mathrm{par}}.
$$

Then

$$
\boxed{
\frac{E_c}{E_{\mathrm{par}}}
=\frac{2}{1+\sqrt{1+4q}}
}.
$$

## 5. Exact parabolic-error relation

The ratio of the parabolic estimate to the nonparabolic energy is

$$
\frac{E_{\mathrm{par}}}{E_c}
=\frac{1+\sqrt{1+4q}}{2}.
$$

Therefore the relative overestimate is

$$
\boxed{
\frac{E_{\mathrm{par}}-E_c}{E_c}
=\frac{\sqrt{1+4q}-1}{2}
}.
$$

The parabolic approximation is controlled by $q$, not by density alone.

For a permitted relative overestimate $\epsilon$,

$$
q<\epsilon+\epsilon^2.
$$

For example:

| tolerated parabolic overestimate | maximum $q$ |
|---:|---:|
| 1% | 0.0101 |
| 5% | 0.0525 |
| 10% | 0.1100 |
| 25% | 0.3125 |
| 50% | 0.7500 |
| 100% | 2.0000 |

Since

$$
q\propto\alpha m_e^{*-1}n^{2/3}g_v^{-2/3},
$$

the density at which the parabolic approximation fails depends strongly on the band-edge mass and nonparabolicity.

## 6. Dingrong-density sensitivity case

Use the declared illustrative values

```text
n          = 7.0e17 cm^-3
m_edge     = 0.010 m0
alpha      = 7.5 eV^-1
m_valence  = 0.35 m0
```

Then

$$
q=2.15607,
$$

and

$$
E_c=140.154\ \mathrm{meV}.
$$

The parabolic conduction estimate exceeds this by

$$
287.476-140.154
=147.323\ \mathrm{meV}.
$$

The conduction-only ratio is

$$
\frac{E_{\mathrm{par}}}{E_c}=2.051.
$$

Thus a parabolic filling model can produce an error larger than the latent gap of a narrow-gap HgCdTe specimen.

For the same declared $m_e^*$ and $\alpha$, the parabolic conduction-energy error grows as:

| density ($\mathrm{cm^{-3}}$) | parabolic error |
|---:|---:|
| $10^{14}$ | 0.0046 meV |
| $10^{15}$ | 0.0946 meV |
| $10^{16}$ | 1.731 meV |
| $10^{17}$ | 23.083 meV |
| $7\times10^{17}$ | 147.323 meV |

Under these declared parameters, a 5% conduction-energy error is reached near

$$
n\approx2.66\times10^{15}\ \mathrm{cm^{-3}}.
$$

This threshold is model dependent and must not be transferred without the mass and nonparabolicity assumptions.

## 7. Valence recoil and direct-transition shift

For a parabolic valence mass $m_v^*$, vertical momentum conservation adds

$$
E_v(k_F)=\frac{\hbar^2 k_F^2}{2m_v^*}.
$$

The zero-temperature Burstein-Moss shift is

$$
\boxed{
\Delta E_{\mathrm{BM}}
=E_c(k_F)+E_v(k_F)
}.
$$

For

$$
m_v^*=0.35m_0,
$$

the Dingrong-density sensitivity case gives

$$
E_v(k_F)=8.214\ \mathrm{meV}
$$

and

$$
\Delta E_{\mathrm{BM}}=148.367\ \mathrm{meV}.
$$

The corresponding fully parabolic shift would be

$$
295.690\ \mathrm{meV},
$$

or 1.993 times the nonparabolic result.

## 8. Separate many-body and observation terms

The measured edge must be written as

$$
\boxed{
E_{\mathrm{opt}}
=E_g^{(0)}
+\Delta E_{\mathrm{BM}}
+\Delta E_{\mathrm{BGR}}
+\Delta E_{\mathrm{obs}}
}.
$$

The terms have different meanings:

- $E_g^{(0)}$: zero-density latent gap;
- $\Delta E_{\mathrm{BM}}>0$: state-filling shift;
- $\Delta E_{\mathrm{BGR}}<0$: many-body gap renormalization;
- $\Delta E_{\mathrm{obs}}$: tail, threshold, instrument, or fitting bias.

A cancellation between positive filling and negative renormalization does not mean either term is absent.

For sensitivity analysis the repository includes

$$
\Delta E_{\mathrm{BGR}}
=-C_{18}\left(\frac{n}{10^{18}\ \mathrm{cm^{-3}}}\right)^{1/3},
$$

where $C_{18}$ is a declared positive magnitude. This is not a universal HgCdTe renormalization law.

With

```text
Eg0  = 0.100 eV
C18  = 0.020 eV
```

at the Dingrong density,

$$
\Delta E_{\mathrm{BGR}}=-17.758\ \mathrm{meV}
$$

and the illustrative edge is

$$
E_{\mathrm{opt}}=230.609\ \mathrm{meV}.
$$

This number is not a reproduction of a source data point because the parameter set is not inferred from the Dingrong specimen.

## 9. One-edge structural non-identifiability

Consider parameters

$$
\theta=
(\ln E_g^{(0)},
\ln m_e^*,
\ln\alpha,
\ln m_v^*,
\ln C_{18}).
$$

One measured edge at one density is one scalar function

$$
y=F(n;\theta).
$$

Its Jacobian has one row, so

$$
\boxed{
\operatorname{rank}(J)\le1
}.
$$

Even with perfectly known density, one edge cannot separately identify the latent gap, conduction mass, nonparabolicity, valence mass, and renormalization coefficient.

## 10. Five-density design

For the declared density series

```text
1e16
3e16
1e17
3e17
7e17 cm^-3
```

and the sensitivity parameters above, the predicted edges are

```text
111.369
123.721
148.439
186.579
230.609 meV
```

The log-parameter Jacobian singular values are

```text
2.55477493e-1
6.63828971e-2
4.64192311e-3
1.81849453e-4
2.31520896e-5
```

The local rank is five, but

$$
\boxed{
\kappa(J)=1.1035\times10^4
}.
$$

The weakest normalized direction is only

$$
9.06\times10^{-5}
$$

of the strongest.

Thus a five-density sweep can be formally full rank while remaining too ill-conditioned for a reliable unconstrained five-parameter inversion.

## 11. Measurement-design consequence

A useful carrier-filling experiment should include:

1. independent Hall density and uncertainty at every optical temperature;
2. a low-density anchor where filling and renormalization are small;
3. intermediate densities that resolve the transition from $n^{2/3}$ behavior;
4. high densities that reveal nonparabolic curvature;
5. an independent mass or Kane-parameter constraint;
6. a separate model or measurement for band-gap renormalization;
7. the full spectrum, not one edge coordinate;
8. a free-carrier background model using the same carrier state.

Adding more edge points at nearly the same density improves precision but does not resolve structural confounding.

## 12. Dingrong source boundary

Qian Dingrong et al. report:

- nominal $x=0.19$;
- $n\approx7.0\times10^{17}\ \mathrm{cm^{-3}}$;
- 77–300 K spectra over approximately 7–17 $\mu$m;
- a Burstein-Moss interpretation of the edge;
- below-gap free-carrier absorption;
- an inferred ionized-impurity concentration near $3.4\times10^{18}\ \mathrm{cm^{-3}}$.

The available source record does not yet support a complete numerical reproduction of every band parameter, free-carrier equation, and temperature-dependent spectrum. The current result is therefore a bounded sensitivity and identifiability result.

## 13. Authorized result

> At degenerate HgCdTe carrier densities, nonparabolicity is not a small correction. One optical edge cannot isolate a carrier correction, and even a five-density series may remain severely ill-conditioned without independent mass and renormalization constraints.

The result does not authorize a universal Dingrong correction or its transfer to low-density detector absorbers.
