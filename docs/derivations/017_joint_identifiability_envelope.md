# Derivation 017: joint identifiability under instrument, family, fit, and operator uncertainty

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issues:** #196, #215, #218, #220, #224, #228, #232  
**Status:** controlled experiment-design envelope; not specimen inference

## 1. Scope

Earlier R04 tranches established separately:

- exact Gaussian covariance filtering by Gaussian and composite kernels;
- common absolute probe-scale calibration limits;
- Gaussian covariance-family falsification with three or more scales;
- parameter drift under covariance misspecification;
- nonlinear transmission and cutoff operation-order effects.

This derivation combines those effects into one question:

> Does a declared multiscale experiment still separate an alternative covariance family from its best Gaussian surrogate after realistic instrument and observation uncertainties are included?

The result is a design-level separation metric. It does not identify the covariance family or correlation length of an HgCdTe specimen.

## 2. Declared composite instruments

For measurement setting $i$, the instrument kernel is the separable model established in Derivation 015:

```text
elliptical Gaussian PSF
convolved with rectangular pixel or scan-bin integration
multiplied by finite-slab exponential depth weighting.
```

For the present family screen, the lateral second moment must be isotropic:

$$
s_i^2
=
\sigma_{{\rm PSF},i}^2
+
\frac{p_i^2}{12}.
$$

The exact Gaussian composite-kernel variance is denoted

$$
V_{i,G}^{\rm exact}.
$$

The moment-matched Gaussian-probe reduction gives

$$
V_{i,G}^{\rm red}
=
A\,F_G(s_i/\xi)\,F_{z,i},
$$

where $F_{z,i}$ is the existing Gaussian finite-depth attenuation.

Define the kernel-shape discrepancy

$$
\boxed{
b_{K,i}
=
\log V_{i,G}^{\rm exact}
-
\log V_{i,G}^{\rm red}.
}
$$

This discrepancy is not discarded. It is retained as an explicit systematic direction.

## 3. Controlled covariance-family comparison

For lateral Gaussian covariance,

$$
F_G(s/\xi)
=
\frac{1}{1+2s^2/\xi^2}
$$

in two dimensions.

For supported half-integer Matérn covariance,

$$
F_\nu(s/\ell)
=
\mathbb E[\rho_\nu(R)],
$$

with $\nu=1/2,3/2,5/2$ and $R$ distributed according to the difference of two Gaussian-probe coordinates.

The controlled alternative-family variance is

$$
\boxed{
V_{i,\nu}
=
A\,F_\nu(s_i/\ell)\,F_{z,i}.
}
$$

This is a separable lateral-family/common-Gaussian-depth model. It is not an exact theorem for a rectangular-pixel Matérn field in three dimensions.

## 4. Gaussian surrogate conventions

Each alternative-family dataset is forced through a Gaussian inverse under two established fitting conventions.

### 4.1 Weighted log-variance loss

$$
\chi_{\log V}^2
=
\sum_i w_i
\left[
\log V_{i,G}(A_G,\xi_G)
-
\log V_{i,\nu}
\right]^2.
$$

### 4.2 Weighted reciprocal-variance loss

$$
\chi_{1/V}^2
=
\sum_i
\frac{
\left[V_{i,G}^{-1}(A_G,\xi_G)-V_{i,\nu}^{-1}\right]^2
}{
\sigma_{1/V,i}^2
}.
$$

The fitted parameters and fitted variance vector are therefore convention-conditioned:

$$
(A_G,\xi_G,V_{i,G}^{\rm fit})
\longrightarrow
\text{depend on the declared loss.}
$$

If the two conventions cross an identifiability threshold differently, the design is classified as convention-sensitive and no unique Gaussian parameter estimate should be reported.

## 5. Observation operators

Let

$$
y_i=h(V_i)
$$

be the logarithm of a declared scalar observable.

The implementation supports four cases.

### 5.1 Log variance

$$
y_i=\log V_i,
\qquad
D_i=\frac{\partial y_i}{\partial\log V_i}=1.
$$

### 5.2 Log gap standard deviation

With local gap slope $g_x$,

$$
\sigma_{G,i}=|g_x|\sqrt{V_i},
$$

$$
y_i=\log\sigma_{G,i},
\qquad
D_i=\frac12.
$$

### 5.3 Transmission-effective absorption

The physically ordered operator is

$$
\alpha_{T,i}(E)
=
-\frac{1}{d}
\log\mathbb E_G
\left[
\exp(-d\alpha(E\mid G))
\right].
$$

The scalar closure is

$$
\bar\alpha_i(E)
=
\mathbb E_G[\alpha(E\mid G)].
$$

Jensen's inequality requires

$$
\alpha_{T,i}\le\bar\alpha_i.
$$

The operation-order shift is

$$
\boxed{
b_{O,i}
=
\log\bar\alpha_i
-
\log\alpha_{T,i}
\ge0.
}
$$

### 5.4 Fixed-response cutoff energy

The physically ordered cutoff is extracted after transmission averaging. The scalar closure extracts the cutoff from mean absorption.

For the declared monotone response,

$$
E_{{\rm cut},T}
\ge
E_{{\rm cut},\bar\alpha}.
$$

Therefore

$$
\boxed{
b_{O,i}
=
\log E_{{\rm cut},\bar\alpha}
-
\log E_{{\rm cut},T}
\le0.
}
$$

For nonlinear operators, the local variance-to-observable sensitivity is evaluated by a symmetric logarithmic perturbation:

$$
D_i
=
\frac{
\log O(V_i e^\epsilon)
-
\log O(V_i e^{-\epsilon})
}{2\epsilon}.
$$

## 6. Correlated instrument calibration

Let the shared instrument log-parameter vector be

$$
q
=
(
\log\sigma_x,
\log\sigma_y,
\log p_x,
\log p_y,
\log\alpha,
\log d
).
$$

For setting $i$, define the established composite-kernel sensitivity row

$$
J_i
=
\frac{\partial\log V_i}{\partial q}.
$$

With declared instrument covariance $C_q$,

$$
\boxed{
C_{V,{\rm inst}}
=
J C_q J^T.
}
$$

The same calibration modes affect every scale, so this covariance is generally non-diagonal.

Let independent observation uncertainty in log variance be

$$
C_{V,{\rm obs}}
=
\operatorname{diag}(\tau_1^2,\ldots,\tau_N^2).
$$

Mapping into log-observable space with

$$
D=\operatorname{diag}(D_1,\ldots,D_N)
$$

gives

$$
C_{y,{\rm obs}}
=
D C_{V,{\rm obs}} D^T,
$$

$$
C_{y,{\rm inst}}
=
D C_{V,{\rm inst}} D^T.
$$

## 7. Systematic-envelope construction

The full declared covariance is built in stages:

$$
C_0=C_{y,{\rm obs}},
$$

$$
C_1=C_0+C_{y,{\rm inst}},
$$

$$
C_2=C_1+(Db_K)(Db_K)^T,
$$

$$
\boxed{
C_3=C_2+b_O b_O^T.
}
$$

The rank-one terms conservatively treat the full declared kernel-reduction and operation-order shifts as one-standard-deviation correlated systematic directions.

This is an explicit modeling choice, not a claim that the discrepancies are random Gaussian errors. The staged results are reported so the conclusion is not hidden inside one aggregate covariance.

## 8. Rank-aware separation

For alternative-family log-observables $y_\nu$ and the best Gaussian-surrogate observables $y_G^{\rm fit}$, define

$$
r
=
y_\nu-y_G^{\rm fit}.
$$

At covariance stage $k$,

$$
\boxed{
\Delta_k^2
=
r^T C_k^+ r,
}
$$

where $C_k^+$ is the Moore-Penrose pseudoinverse over numerically supported covariance directions.

The reported distance is

$$
\Delta_k=\sqrt{\Delta_k^2}.
$$

This is a multivariate standardized separation, not a posterior probability or discovery significance.

A declared threshold $\Delta_*$ gives the following diagnostic categories:

```text
Delta_3 >= Delta_*                         resolved under full envelope
Delta_0 < Delta_*                          observation limited
Delta_0 >= Delta_* > Delta_1               instrument-calibration limited
Delta_1 >= Delta_* > Delta_2               kernel-shape limited
Delta_2 >= Delta_* > Delta_3               observation-operator limited
```

## 9. Required self-consistency

For Gaussian truth evaluated through the same reduced Gaussian family,

$$
r=0
$$

under both fitting conventions, up to numerical tolerance.

The exact composite-Gaussian discrepancy remains visible only through $b_K$ and does not create a false Gaussian-family residual.

## 10. Interpretation

The staged envelope separates four questions:

1. Would the family difference be visible with observation noise alone?
2. Does shared instrument calibration remove that visibility?
3. Does reducing the actual PSF/pixel kernel to one Gaussian width remove it?
4. Does the optical or cutoff operation order remove it?

A family difference that survives only before one of these additions is not experimentally identifiable under the declared design.

## 11. Claim restrictions

This derivation does not establish:

- a specimen covariance family;
- a specimen point variance or correlation length;
- an exact composite-kernel Matérn theorem;
- a universal relationship between pixel pitch and optical PSF;
- that rank-one systematic outer products are uniquely correct uncertainty models;
- that $\Delta$ is a Bayesian model probability or frequentist discovery significance;
- that one fitting convention is universally preferred;
- manuscript readiness or novelty.

The next scientific step after this controlled envelope is an experimentally specified PSF, pixel geometry, thickness, absorption-depth model, and multiresolution dataset or published-data path.
