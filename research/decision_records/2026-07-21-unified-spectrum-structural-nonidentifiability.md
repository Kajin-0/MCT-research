# Decision record: unified spectrum structural non-identifiability

**Date:** 2026-07-21  
**Issue:** #177  
**Status:** candidate controlling result pending PR validation

## Decision

Adopt the composed distributed-gap, uniform carrier-translation, and single-pass response model as the first unified spectrum-level identifiability theorem for the flagship publication.

Authorize it for:

1. proving exact forward-model invariances;
2. distinguishing structural from statistical uncertainty;
3. constructing spectrally indistinguishable parameter sets;
4. defining minimum external constraints for latent-gap recovery;
5. testing how independently calibrated carrier-dependent spectral structure changes rank.

Do not authorize it as a complete microscopic HgCdTe absorption model.

## Base forward model

$$
\alpha_{\mathrm{loc}}(E\mid G)=A(E-G)_+^p,
$$

$$
G\sim\mathcal N(E_g^{(0)}+\Delta_c,\sigma_G^2),
$$

$$
R(E)=1-\exp[-d\bar\alpha(E)].
$$

The five nominal parameters

```text
Eg0
Delta_carrier
ln sigma_G
ln A
ln d
```

enter through only

```text
Eg0 + Delta_carrier
sigma_G
A * d
```

in the base model.

## Exact base-model invariances

### Gap/carrier translation

```text
Eg0 -> Eg0 + delta
Delta_carrier -> Delta_carrier - delta
```

leaves the spectrum unchanged, so

$$
\frac{\partial R}{\partial E_g^{(0)}}
=
\frac{\partial R}{\partial\Delta_c}.
$$

### Amplitude/thickness product

```text
A -> c*A
d -> d/c
```

leaves the spectrum unchanged, so

$$
\frac{\partial R}{\partial\ln A}
=
\frac{\partial R}{\partial\ln d}.
$$

Therefore

$$
\boxed{\operatorname{rank}(J)\le3}
$$

regardless of spectral point count or measurement noise.

## Exact counterexample

```text
set 1: Eg0=0.100 eV, Delta=0.030 eV, sigma=0.010 eV,
       A=30000, d=10 um

set 2: Eg0=0.120 eV, Delta=0.010 eV, sigma=0.010 eV,
       A=15000, d=20 um
```

Across 281 response points from `0.08` to `0.22 eV`, the maximum absolute spectral difference is

```text
2.22e-16
```

or machine precision.

## Numerical base-model rank

The dense-spectrum singular values are

```text
2.10943527e2
3.12774161e0
3.79499126e-1
3.36022167e-11
4.59184616e-14
```

and numerical rank is three.

Known carrier shift alone leaves the amplitude/thickness null. Known thickness alone leaves the gap/carrier null. Constraining both leaves `(Eg0, ln sigma_G, ln A)`, which are locally full rank in the declared design.

## Absolutely calibrated nontranslational carrier marker

Add the generic diagnostic term

$$
\alpha_m(E)=B\Delta_c(E_r/E)^2.
$$

This marker is not the Dingrong free-carrier absorption model.

It breaks both simple pairwise identities because:

- the marker depends on $\Delta_c$ but not on $E_g^{(0)}$;
- thickness multiplies both interband and marker absorption, whereas $A$ multiplies only the interband branch.

However, the marked spectrum depends on four combinations:

```text
Eg0 + Delta_carrier
sigma_G
A * d
Delta_carrier * d
```

so one combined invariance remains.

For any $c>0$:

```text
d -> c*d
A -> A/c
Delta_carrier -> Delta_carrier/c
Eg0 -> Eg0 + Delta_carrier*(1-1/c)
```

leaves all four combinations unchanged.

The infinitesimal null vector for

```text
(Eg0, Delta_carrier, ln sigma_G, ln A, ln d)
```

is

```text
(Delta_carrier, -Delta_carrier, 0, -1, +1)
```

and the exact Jacobian relation is

$$
\Delta_c J_{E_g}
-
\Delta_c J_{\Delta_c}
-
J_{\ln A}
+
J_{\ln d}
=0.
$$

## Marked-spectrum numerical result

For `B=1000 cm^-1 eV^-1` and `E_r=0.1 eV`, the singular values are

```text
2.05808179e2
6.76801242e0
3.05553476e0
3.57325799e-1
3.58461331e-11
```

and numerical rank is four.

The maximum absolute residual of the combined null relation is `2.28e-11`.

Independently known effective thickness removes the remaining combined null and leaves `(Eg0, Delta_carrier, ln sigma_G, ln A)` locally full rank in the declared marked design.

## Authorized conclusions

- Exact forward invariances cannot be removed by better signal-to-noise or denser sampling.
- The unmarked single-state spectrum identifies at most the translated mean gap, gap width, and amplitude-thickness product.
- In the unmarked model, independent carrier-state and effective-thickness information are both required for latent-gap recovery.
- An absolutely calibrated nontranslational carrier feature raises rank from three to four.
- The marker does not independently identify all five parameters; one combined scaling/translation null remains until an external scale such as effective thickness is known.
- Full spectra remain more informative than cutoffs because they identify the available combinations and test model adequacy.

## Unauthorized conclusions

- The Gaussian/power-law spectrum is not a complete HgCdTe material model.
- The generic carrier marker is not a physical free-carrier law.
- Effective thickness is not assumed equal to physical thickness.
- Spatial carrier-gap correlation, interference, reflection, transport, and energy-dependent collection remain outside scope.
- Structural rank does not determine practical covariance after external constraints are supplied.

## Validation gates

Merge requires:

- machine-precision base-model counterexample;
- numerical base-model rank three;
- direct confirmation of both base Jacobian-column identities;
- external-constraint rank tests;
- marked-spectrum rank four;
- rejection of the incorrect pairwise-null claim after the marker is enabled;
- direct confirmation of the combined marked-spectrum null vector;
- full marked-spectrum rank when thickness is known;
- public API, immutable result, derivation, active-state update, and complete CI on Python 3.11 and 3.13.

## Next decision

After merge, begin the flagship manuscript analytical core. The next validation priority is a calibrated real spectrum or same-specimen multi-state dataset that can test at least one forward operator without requiring external collaboration.
