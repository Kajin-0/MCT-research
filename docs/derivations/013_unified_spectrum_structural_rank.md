# Derivation 013: structural rank of a unified HgCdTe optical spectrum

## 1. Objective

This derivation combines:

1. a distribution of local gaps;
2. a spatially uniform carrier-induced edge translation;
3. a single-pass Beer-Lambert response.

It asks whether an arbitrarily dense, noise-free spectrum can separately recover:

- zero-density latent gap;
- carrier-induced edge shift;
- local-gap width;
- absorption amplitude;
- effective absorbing thickness.

Under the base model, five nominal parameters enter through only three independent combinations.

## 2. Unified base model

Use the controlled local edge

$$
\alpha_{\mathrm{loc}}(E\mid G)=A(E-G)_+^p,
$$

with

$$
G\sim\mathcal N(\mu_G,\sigma_G^2),
\qquad
\mu_G=E_g^{(0)}+\Delta_c.
$$

The convolved absorption has the scale form

$$
\boxed{
\bar\alpha(E)
=A\sigma_G^p
F_p\left(
\frac{E-E_g^{(0)}-\Delta_c}{\sigma_G}
\right).
}
$$

For effective thickness $d$,

$$
R(E)=1-\exp[-d\bar\alpha(E)],
$$

or

$$
\boxed{
R(E)=1-
\exp\left\{
-Ad\,\sigma_G^p
F_p\left[
\frac{E-E_g^{(0)}-\Delta_c}{\sigma_G}
\right]
\right\}.
}
$$

The dense spectrum depends only on

$$
\boxed{
\mu=E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
K=Ad.
}
$$

## 3. Exact gap/carrier translation invariance

For any scalar $\delta$,

$$
E_g^{(0)}\rightarrow E_g^{(0)}+\delta,
\qquad
\Delta_c\rightarrow\Delta_c-\delta
$$

leaves the spectrum unchanged. Therefore

$$
\boxed{
\frac{\partial R}{\partial E_g^{(0)}}
=
\frac{\partial R}{\partial\Delta_c}.
}
$$

No increase in signal-to-noise, bandwidth, or number of spectral points can separate two parameters that enter only through their sum.

## 4. Exact amplitude/thickness invariance

For any $c>0$,

$$
A\rightarrow cA,
\qquad
d\rightarrow d/c
$$

leaves the response unchanged. With logarithmic parameters,

$$
\boxed{
\frac{\partial R}{\partial\ln A}
=
\frac{\partial R}{\partial\ln d}.
}
$$

Absorption amplitude and effective thickness are structurally inseparable in the base single-pass model unless one is constrained independently.

## 5. Structural rank theorem

Let

$$
\theta=(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A,\ln d).
$$

The Jacobian columns satisfy

$$
J_{E_g}=J_{\Delta_c},
\qquad
J_{\ln A}=J_{\ln d}.
$$

Thus at most three independent columns remain and

$$
\boxed{
\operatorname{rank}(J)\le3.
}
$$

The bound is independent of the number of spectral samples. A continuum of exact observations cannot exceed it.

## 6. Exact counterexample

Consider:

| parameter | set 1 | set 2 |
|---|---:|---:|
| $E_g^{(0)}$ | 0.100 eV | 0.120 eV |
| $\Delta_c$ | 0.030 eV | 0.010 eV |
| $\sigma_G$ | 0.010 eV | 0.010 eV |
| $A$ | 30000 | 15000 |
| $d$ | 10 $\mu$m | 20 $\mu$m |

Both have

$$
E_g^{(0)}+\Delta_c=0.130\ \mathrm{eV}
$$

and equal $Ad$. Across 281 response points from `0.08` to `0.22 eV`, the maximum absolute difference is

$$
2.22\times10^{-16}.
$$

The two distinct parameter descriptions are spectrally indistinguishable to machine precision.

## 7. Dense-spectrum numerical rank

For set 1, fixed $p=1$, and no additional carrier-dependent feature, the singular values are

```text
2.10943527e2
3.12774161e0
3.79499126e-1
3.36022167e-11
4.59184616e-14
```

with relative values

```text
1.00000000
1.48273884e-2
1.79905556e-3
1.59294846e-13
2.17681302e-16
```

and numerical rank three at relative tolerance $10^{-8}$.

## 8. External constraints in the base model

- Known carrier shift leaves $(E_g^{(0)},\ln\sigma_G,\ln A,\ln d)$ with rank three because $A$ and $d$ remain confounded.
- Known thickness leaves $(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A)$ with rank three because $E_g^{(0)}$ and $\Delta_c$ remain confounded.
- Known carrier shift and known thickness leave $(E_g^{(0)},\ln\sigma_G,\ln A)$, which are locally full rank in the declared design.

Both external constraints are required for latent-gap recovery in the unmarked base model.

## 9. Adding an absolutely calibrated carrier-dependent marker

A carrier effect need not be only a rigid translation. Add the generic diagnostic term

$$
\alpha_m(E)
=B\Delta_c\left(\frac{E_r}{E}\right)^2,
$$

so the optical depth is

$$
\tau(E)
=d\left[
A f(E;E_g^{(0)}+\Delta_c,\sigma_G)
+B\Delta_c h(E)
\right].
$$

This is an identifiability marker, not the Dingrong free-carrier absorption law.

The marker breaks the two **simple pairwise** invariances:

$$
J_{E_g}\ne J_{\Delta_c},
\qquad
J_{\ln A}\ne J_{\ln d}.
$$

However, the five parameters still enter through only four combinations:

$$
\mu=E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
K=Ad,
\qquad
M=\Delta_c d.
$$

Therefore one combined invariance remains.

## 10. Exact combined finite invariance with the marker

For any $c>0$, define

$$
d' = cd,
$$

$$
A'=A/c,
$$

$$
\Delta_c'=\Delta_c/c,
$$

and

$$
E_g^{(0)\prime}
=E_g^{(0)}+\Delta_c\left(1-\frac1c\right).
$$

Then

$$
E_g^{(0)\prime}+\Delta_c'
=E_g^{(0)}+\Delta_c,
$$

$$
A'd'=Ad,
$$

and

$$
\Delta_c'd'=\Delta_c d.
$$

Hence the complete marked response remains unchanged.

The infinitesimal null vector in coordinates

$$
(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A,\ln d)
$$

is

$$
\boxed{
v=(\Delta_c,-\Delta_c,0,-1,1).
}
$$

Thus

$$
\boxed{
Jv
=
\Delta_c J_{E_g}
-\Delta_c J_{\Delta_c}
-J_{\ln A}
+J_{\ln d}
=0.
}
$$

The marker raises the structural rank from at most three to at most four; it does not make all five parameters identifiable by itself.

## 11. Numerical marked-spectrum rank

Using

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

For the declared $\Delta_c=0.030$ eV, the maximum absolute residual of the combined Jacobian null relation is

```text
2.28e-11.
```

If effective thickness is independently known, the remaining parameters

$$
(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A)
$$

are locally full rank in the declared marked-spectrum design.

The correct measurement principle is therefore:

> An absolutely calibrated carrier-dependent spectral feature can raise rank and separate the simple gap/carrier translation, but one external scale such as effective thickness is still required to remove the remaining combined invariance.

## 12. Why dense spectra remain valuable

The theorem does not imply that spectra are uninformative. In the base model, dense spectra can identify

$$
E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
Ad
$$

more robustly than one cutoff. They can also reveal model inadequacy through curvature and residual structure.

The theorem states that exact forward invariances cannot be defeated statistically.

## 13. Measurement-design requirements

Latent-gap recovery should include:

1. independent carrier density and a validated filling/renormalization model;
2. independently calibrated effective thickness or absorption amplitude;
3. a full calibrated spectrum rather than one cutoff;
4. enough spectral range to identify gap width and intrinsic-edge shape;
5. carrier-dependent spectral structure modeled jointly with absolute calibration;
6. multiple carrier states or temperatures on the same specimen to test the rigid-translation assumption.

## 14. Claim boundaries

The theorem assumes:

- a Gaussian local-gap distribution;
- fixed local-edge exponent;
- spatially uniform carrier translation;
- multiplicative absorption amplitude;
- single-pass Beer-Lambert response;
- one effective thickness.

The generic marker is not a physical free-carrier model. Carrier-gap spatial correlations, reflection, interference, multiple paths, transport, and energy-dependent collection remain outside scope.

## 15. Controlling result

> Under the unmarked unified model, an arbitrarily dense single-state response spectrum has structural rank at most three for five nominal parameters. A calibrated nontranslational carrier feature can raise rank to four, but one combined scaling/translation invariance remains until an external scale such as effective thickness is supplied.
