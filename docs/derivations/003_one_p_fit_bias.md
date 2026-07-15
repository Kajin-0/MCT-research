# Derivation 003 — Analytical bias of a one-$P$ fit when $P_8\ne P_7$

**Status:** derived and numerically verified  
**Claim level:** exact result for the declared matrix norm and basis  
**Novelty status:** prior-art audit incomplete

## 1. Nested models

Separate the linear conduction–valence coupling into two matrix templates:

$$
H^{(1)}(\mathbf k)
=P_8M_8(\mathbf k)+P_7M_7(\mathbf k),
$$

where $M_8$ contains only the $\Gamma_6\leftrightarrow\Gamma_8$ matrix elements and $M_7$ contains only the $\Gamma_6\leftrightarrow\Gamma_7$ matrix elements.

The conventional Kane model imposes

$$
P_8=P_7=P
$$

and therefore uses

$$
H_{1P}^{(1)}(\mathbf k)
=P\left[M_8(\mathbf k)+M_7(\mathbf k)\right].
$$

## 2. Template orthogonality

The two templates occupy disjoint matrix blocks. Consequently, at every $\mathbf k$,

$$
\operatorname{Re}\operatorname{Tr}
\left[M_8^{\dagger}(\mathbf k)M_7(\mathbf k)\right]=0.
$$

Thus $P_8$ and $P_7$ are independently identifiable in a full complex-matrix fit once nonzero $\mathbf k$ points are supplied. The two-parameter normal matrix has no cross term under an unweighted Frobenius metric.

## 3. Relative template norms

Using the explicit basis coefficients, the squared Frobenius norms are

$$
\|M_8(\mathbf k)\|_F^2
=\frac{8}{3}k^2,
$$

and

$$
\|M_7(\mathbf k)\|_F^2
=\frac{4}{3}k^2.
$$

Therefore,

$$
\|M_8\|_F^2=2\|M_7\|_F^2
$$

for every nonzero direction and magnitude. The result remains true after summing any set of $\mathbf k$ points with scalar point weights, provided all matrix elements share the same metric.

## 4. Biased one-$P$ estimate

Suppose the target Hamiltonian has true couplings $P_8$ and $P_7$, but it is fitted with the constrained one-$P$ model. The least-squares objective associated with the linear block is

$$
\chi^2(P)
=N_8(P_8-P)^2+N_7(P_7-P)^2,
$$

where

$$
N_8=\sum_jw_j\|M_8(\mathbf k_j)\|_F^2,
\qquad
N_7=\sum_jw_j\|M_7(\mathbf k_j)\|_F^2.
$$

Minimization gives

$$
P_{1P}^{*}
=\frac{N_8P_8+N_7P_7}{N_8+N_7}.
$$

Because $N_8=2N_7$,

$$
\boxed{
P_{1P}^{*}=\frac{2P_8+P_7}{3}
}.
$$

The conventional fitted $P$ is therefore not the arithmetic mean. It is biased toward the $\Gamma_8$ coupling because the $\Gamma_6\leftrightarrow\Gamma_8$ block contains twice the Frobenius information.

## 5. Irreducible residual

Let

$$
\Delta P=P_8-P_7.
$$

At the constrained optimum,

$$
P_8-P_{1P}^{*}=\frac{\Delta P}{3},
$$

and

$$
P_7-P_{1P}^{*}=-\frac{2\Delta P}{3}.
$$

The minimum residual in the linear block is

$$
\chi^2_{\min}
=\frac{2N_7}{3}(\Delta P)^2.
$$

Relative to the true linear-block norm,

$$
\rho_{P}^{2}
=
\frac{
\frac{2}{3}(P_8-P_7)^2
}{
2P_8^2+P_7^2
},
$$

or

$$
\boxed{
\rho_P=
\sqrt{
\frac{2(P_8-P_7)^2}
{3(2P_8^2+P_7^2)}
}
}.
$$

This is the unavoidable one-$P$ error before including other Hamiltonian blocks in the normalization.

## 6. Synthetic verification

For

$$
P_8=1.02P_0,
\qquad
P_7=0.98P_0,
$$

the exact constrained estimate is

$$
P_{1P}^{*}
=\frac{2(1.02)+0.98}{3}P_0
=1.006\overline{6}P_0.
$$

The executable matrix fit recovered this value to numerical precision. The unconstrained two-$P$ model recovered both input couplings and reduced its closure residual below $10^{-12}$.

## 7. Consequence for finite-temperature interpretation

If an AHC-projected Hamiltonian has $P_8(T)\ne P_7(T)$, a conventional one-$P$ fit will report

$$
P(T)=\frac{2P_8(T)+P_7(T)}{3}
$$

under the current metric. A seemingly stable $P(T)$ can therefore conceal opposite changes in $P_8$ and $P_7$.

This directly affects the leading hypothesis that the Kane velocity is temperature independent. Magneto-optical observables dominated by $\Gamma_6\leftrightarrow\Gamma_8$ coupling may track $P_8$ more closely than the one-$P$ matrix average. Therefore, a comparison to measured Kane velocity should not automatically validate equality of $P_8$ and $P_7$.

## 8. Limits of the result

The $2:1$ weighting is exact only for:

- the declared basis and standard Kane coefficients;
- an unweighted Frobenius metric over all complex matrix elements;
- scalar weights applied per $\mathbf k$ point;
- and a gauge in which the $\Gamma_8$ and $\Gamma_7$ template blocks retain their declared meaning.

A covariance-weighted fit changes the effective weights and therefore changes the constrained average. The general formula

$$
P_{1P}^{*}
=\frac{N_8P_8+N_7P_7}{N_8+N_7}
$$

remains valid when $N_8$ and $N_7$ are computed in the chosen metric and the two templates remain orthogonal in that metric.
