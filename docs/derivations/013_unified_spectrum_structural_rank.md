# Derivation 013: structural rank of a unified HgCdTe optical spectrum

## 1. Objective

This derivation combines three previously tested observation layers:

1. a distribution of local gaps;
2. a spatially uniform carrier-induced edge translation;
3. a single-pass Beer-Lambert response.

It asks whether an arbitrarily dense, noise-free optical response spectrum can separately recover:

- the zero-density latent gap;
- the carrier-induced edge shift;
- the local-gap width;
- the absorption amplitude;
- the effective absorbing thickness.

Under the declared model, the answer is no. Five nominal parameters enter through only three independent combinations.

## 2. Local absorption and gap distribution

Use the controlled local edge

$$
\alpha_{\mathrm{loc}}(E\mid G)
=A(E-G)_+^p,
$$

where

$$
(y)_+=\max(y,0).
$$

Let the local gap distribution be

$$
G\sim\mathcal N(\mu_G,\sigma_G^2).
$$

A spatially uniform carrier-induced shift is represented by

$$
\mu_G=E_g^{(0)}+\Delta_c.
$$

Here:

- $E_g^{(0)}$ is the zero-density latent gap;
- $\Delta_c$ is the net uniform carrier-dependent translation retained in the interband edge;
- $\sigma_G$ is the declared local-gap standard deviation.

The convolution derived previously has the scale form

$$
\boxed{
\bar\alpha(E)
=A\sigma_G^p
F_p\left(
\frac{E-E_g^{(0)}-\Delta_c}{\sigma_G}
\right)
}.
$$

## 3. Single-pass response

For effective thickness $d$,

$$
R(E)=1-\exp[-d\bar\alpha(E)].
$$

Substitution gives

$$
\boxed{
R(E)
=1-
\exp\left\{
-A d\,\sigma_G^p
F_p\left[
\frac{E-E_g^{(0)}-\Delta_c}{\sigma_G}
\right]
\right\}.
}
$$

The complete dense spectrum depends only on:

$$
\boxed{
\mu=E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
K=A d.
}
$$

Thus the five-parameter representation

$$
\theta=
(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A,\ln d)
$$

contains only three independently observable combinations.

## 4. Exact gap/carrier translation invariance

For any scalar $\delta$,

$$
E_g^{(0)}\rightarrow E_g^{(0)}+\delta,
$$

$$
\Delta_c\rightarrow\Delta_c-\delta
$$

leaves

$$
E_g^{(0)}+\Delta_c
$$

unchanged. Therefore

$$
\boxed{
R(E;E_g^{(0)}+\delta,\Delta_c-\delta)
=R(E;E_g^{(0)},\Delta_c)
}
$$

for every photon energy.

Differentiating gives the Jacobian identity

$$
\boxed{
\frac{\partial R}{\partial E_g^{(0)}}
=
\frac{\partial R}{\partial\Delta_c}.
}
$$

The two spectral Jacobian columns are identical.

No increase in signal-to-noise, spectral resolution, bandwidth, or number of points can distinguish two parameters that the forward operator includes only through their sum.

## 5. Exact amplitude/thickness invariance

For any positive scale $c$,

$$
A\rightarrow cA,
$$

$$
d\rightarrow d/c
$$

leaves the optical depth

$$
A d\,\sigma_G^p F_p
$$

unchanged. Hence

$$
\boxed{
R(E;cA,d/c)=R(E;A,d)
}
$$

for every photon energy.

Using logarithmic parameters,

$$
\boxed{
\frac{\partial R}{\partial\ln A}
=
\frac{\partial R}{\partial\ln d}.
}
$$

Absorption amplitude and effective thickness are structurally inseparable in a single-pass response spectrum unless one is constrained independently.

## 6. Structural rank theorem

The five Jacobian columns are

$$
J=\left[
J_{E_g},
J_{\Delta_c},
J_{\ln\sigma},
J_{\ln A},
J_{\ln d}
\right].
$$

The exact identities give

$$
J_{E_g}=J_{\Delta_c},
$$

and

$$
J_{\ln A}=J_{\ln d}.
$$

Therefore at most three independent columns remain:

$$
J_{E_g},
\qquad
J_{\ln\sigma},
\qquad
J_{\ln A}.
$$

Thus

$$
\boxed{
\operatorname{rank}(J)\le3.
}
$$

This bound is independent of the number of spectral points. A continuum of exact observations cannot exceed it.

## 7. Exact counterexample

Consider the two parameter sets:

| parameter | set 1 | set 2 |
|---|---:|---:|
| $E_g^{(0)}$ | 0.100 eV | 0.120 eV |
| $\Delta_c$ | 0.030 eV | 0.010 eV |
| $\sigma_G$ | 0.010 eV | 0.010 eV |
| $A$ | 30000 | 15000 |
| $d$ | 10 $\mu$m | 20 $\mu$m |

Both sets have

$$
E_g^{(0)}+\Delta_c=0.130\ \mathrm{eV}
$$

and

$$
A d=300000
$$

in the corresponding declared units.

For a 281-point response spectrum over `0.08-0.22 eV`, the maximum absolute numerical difference is

$$
2.22\times10^{-16}.
$$

The two physically different parameter descriptions are spectrally indistinguishable to machine precision.

## 8. Dense-spectrum numerical rank

For the first parameter set with $p=1$, deterministic quadrature, and no additional carrier-dependent spectral feature, the Jacobian singular values are

```text
2.10943527e2
3.12774161e0
3.79499126e-1
3.36022167e-11
4.59184616e-14
```

Relative to the largest:

```text
1.00000000
1.48273884e-2
1.79905556e-3
1.59294846e-13
2.17681302e-16
```

The numerical rank is three at a relative tolerance of $10^{-8}$, in agreement with the exact theorem.

The two null singular directions are numerical representations of:

1. zero-density gap versus carrier translation;
2. absorption amplitude versus effective thickness.

## 9. Effect of external constraints

### Known carrier shift

If independent Hall data and a validated carrier model fix $\Delta_c$, the remaining parameters are

$$
(E_g^{(0)},\ln\sigma_G,\ln A,\ln d).
$$

Their spectrum still has rank three because $A$ and $d$ remain confounded.

### Known effective thickness

If $d$ is independently known, the remaining parameters are

$$
(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A).
$$

Their spectrum still has rank three because $E_g^{(0)}$ and $\Delta_c$ remain confounded.

### Both known

If both the carrier shift and effective thickness are constrained, the remaining parameters

$$
(E_g^{(0)},\ln\sigma_G,\ln A)
$$

are locally full rank in the declared numerical design.

Therefore both external constraints are required for latent-gap recovery under this forward model.

## 10. Breaking the translation degeneracy

A carrier effect need not be only a rigid interband translation. Suppose an independently calibrated carrier-dependent spectral marker is added:

$$
\alpha_{\mathrm{marker}}(E)
=B\Delta_c\left(\frac{E_r}{E}\right)^2.
$$

This term changes spectral shape and amplitude with $\Delta_c$ but not with $E_g^{(0)}$.

It is a generic identifiability marker, not the Dingrong free-carrier absorption law.

Using the declared diagnostic scale

```text
B = 1000 cm^-1 eV^-1
E_r = 0.1 eV
```

produces singular values

```text
2.05808179e2
6.76801242e0
3.05553476e0
3.57325799e-1
3.58461331e-11
```

and numerical rank four.

The gap/carrier translation null is removed because the carrier parameter now changes a nontranslational spectral feature. The amplitude/thickness null remains exact.

This demonstrates the required measurement principle:

> A carrier-dependent background can separate carrier state from latent gap only if its spectral shape and absolute calibration are retained in the same forward model.

## 11. Why dense spectra are still valuable

The theorem does not imply that spectra are uninformative. Dense spectra can identify the three combinations

$$
E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
A d
$$

more robustly than one cutoff or one fitted edge.

They can also reveal model inadequacy through curvature, residual structure, or additional spectral features.

The theorem states only that exact invariances cannot be defeated statistically.

## 12. Measurement-design requirements

A program intended to recover the zero-density latent gap should obtain at least:

1. independent carrier density and a validated filling/renormalization model;
2. independently calibrated effective thickness or absorption amplitude;
3. a full calibrated spectrum rather than one cutoff;
4. enough spectral range to identify gap-distribution width and intrinsic-edge shape;
5. a carrier-dependent spectral background, when available, modeled jointly rather than subtracted without provenance;
6. multiple carrier states or temperatures on the same specimen to test whether a rigid-translation model is adequate.

## 13. Claim boundaries

The theorem assumes:

- a Gaussian local-gap distribution;
- a fixed local-edge exponent;
- a spatially uniform carrier-induced edge translation;
- multiplicative absorption amplitude;
- single-pass Beer-Lambert response;
- one effective thickness.

It does not include:

- carrier-gap spatial correlations;
- multiple optical paths;
- interference and reflectance;
- energy-dependent collection efficiency;
- a physical free-carrier absorption law;
- finite-temperature carrier statistics;
- a complete microscopic HgCdTe absorption model.

## 14. Controlling result

> Under the declared unified observation model, an arbitrarily dense single-state response spectrum has structural rank at most three for five nominal parameters. Independent carrier-state and effective-thickness information are necessary, not merely helpful, for recovering the latent zero-density gap.
