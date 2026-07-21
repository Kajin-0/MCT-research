# Decision record: unified spectrum structural non-identifiability

**Date:** 2026-07-21  
**Issue:** #177  
**Status:** candidate controlling result pending PR validation

## Decision

Adopt the composed distributed-gap, uniform carrier-translation, and single-pass response model as the first unified spectrum-level identifiability theorem for the flagship publication.

Authorize the model for:

1. proving exact forward-model invariances;
2. distinguishing structural from statistical uncertainty;
3. constructing exact spectrally indistinguishable parameter sets;
4. defining the minimum external constraints required for latent-gap recovery;
5. motivating jointly modeled carrier-dependent spectral backgrounds.

Do not authorize it as a complete microscopic HgCdTe absorption model.

## Unified forward model

The local edge is

$$
\alpha_{\mathrm{loc}}(E\mid G)=A(E-G)_+^p.
$$

The local gaps satisfy

$$
G\sim\mathcal N(E_g^{(0)}+\Delta_c,\sigma_G^2).
$$

The single-pass response is

$$
R(E)=1-\exp[-d\bar\alpha(E)].
$$

The complete spectrum therefore depends on the five nominal parameters

```text
Eg0
Delta_carrier
ln sigma_G
ln A
ln d
```

only through three combinations:

```text
Eg0 + Delta_carrier
sigma_G
A * d
```

## Exact invariances

### Gap/carrier translation

For any $\delta$,

```text
Eg0 -> Eg0 + delta
Delta_carrier -> Delta_carrier - delta
```

leaves the spectrum unchanged. Hence

$$
\frac{\partial R}{\partial E_g^{(0)}}
=
\frac{\partial R}{\partial\Delta_c}.
$$

### Amplitude/thickness product

For any $c>0$,

```text
A -> c*A
d -> d/c
```

leaves the spectrum unchanged. Hence

$$
\frac{\partial R}{\partial\ln A}
=
\frac{\partial R}{\partial\ln d}.
$$

## Structural theorem

The five-column spectral Jacobian contains two exact column equalities. Therefore

$$
\boxed{\operatorname{rank}(J)\le3}.
$$

This bound is independent of the number of spectral samples and measurement noise.

## Exact counterexample

The two parameter sets

```text
set 1: Eg0=0.100 eV, Delta=0.030 eV, sigma=0.010 eV,
       A=30000, d=10 um

set 2: Eg0=0.120 eV, Delta=0.010 eV, sigma=0.010 eV,
       A=15000, d=20 um
```

have equal mean edge and equal amplitude-thickness product.

Across 281 response points from `0.08` to `0.22 eV`, their maximum absolute spectral difference is

```text
2.22e-16
```

or machine precision.

## Numerical rank confirmation

For set 1 and fixed `p=1`, the dense-spectrum singular values are

```text
2.10943527e2
3.12774161e0
3.79499126e-1
3.36022167e-11
4.59184616e-14
```

The relative values are

```text
1.00000000
1.48273884e-2
1.79905556e-3
1.59294846e-13
2.17681302e-16
```

and numerical rank is three.

## External constraints

- Known carrier shift alone leaves the amplitude/thickness null and rank three among four remaining parameters.
- Known effective thickness alone leaves the gap/carrier translation null and rank three among four remaining parameters.
- Known carrier shift and known effective thickness leave `(Eg0, ln sigma_G, ln A)`, which are locally full rank in the declared design.

Both external constraints are required for latent-gap recovery under this model.

## Nontranslational carrier marker

A generic diagnostic carrier feature

$$
\alpha_{\mathrm{marker}}
=B\Delta_c(E_r/E)^2
$$

raises numerical rank from three to four for the declared scale `B=1000 cm^-1 eV^-1`.

The carrier marker separates `Eg0` from `Delta_c` because it changes spectral shape rather than only translating the edge. The amplitude/thickness null remains.

This marker is not the Dingrong free-carrier absorption model. It establishes a measurement-design principle only.

## Authorized conclusions

- Structural invariances cannot be removed by better signal-to-noise or denser spectral sampling.
- One single-state response spectrum identifies at most the mean translated gap, gap width, and amplitude-thickness product under the declared model.
- Independent carrier-state information and effective-thickness information are necessary for latent-gap recovery.
- A calibrated nontranslational carrier-dependent feature can break the gap/carrier translation null.
- Full spectra remain more informative than cutoffs because they can identify the three available combinations and test model adequacy.

## Unauthorized conclusions

- The Gaussian/power-law spectrum is not a complete HgCdTe material model.
- The generic carrier marker is not a physical free-carrier absorption law.
- Effective thickness is not assumed equal to physical thickness.
- The theorem does not include spatial carrier-gap correlation, interference, reflection, transport, or energy-dependent collection.
- Structural rank does not determine practical covariance after external constraints are supplied.

## Validation gates

Merge requires:

- machine-precision spectral equivalence for the exact counterexample;
- numerical rank three for the unmarked dense spectrum;
- direct confirmation of both Jacobian-column identities;
- rank tests under one and two external constraints;
- rank four after the nontranslational carrier marker is added;
- persistence of the amplitude/thickness null with the marker;
- public API, immutable result, derivation, active-state update, and complete CI on Python 3.11 and 3.13.

## Next decision

After merge, begin the flagship manuscript analytical core. The next validation priority is a calibrated real spectrum or same-specimen multi-state dataset that can test at least one of the forward operators without requiring external collaboration.
