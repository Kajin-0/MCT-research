# Derivation 005 — Covariance propagation through gauge and symmetry processing

**Status:** derived, implemented, and synthetically verified  
**Claim level:** exact linear uncertainty propagation  
**Novelty status:** methodological; prior-art audit incomplete

## 1. Observation vector

For an $8\times8$ complex matrix $O$, define the real observation vector

$$
y=\mathcal V(O)
=\begin{pmatrix}
\operatorname{Re}\operatorname{vec}O\\
\operatorname{Im}\operatorname{vec}O
\end{pmatrix}
\in\mathbb R^{128}.
$$

Let

$$
C=\operatorname{Cov}(y)
$$

be the covariance supplied by replicate calculations, numerical convergence studies, or an explicit uncertainty model.

## 2. Gauge rotation is a linear observation map

After a basis change $\Psi\rightarrow\Psi U$, the operator matrix transforms as

$$
O' = U^\dagger O U.
$$

Because this is linear in $O$, there exists a real matrix

$$
T(U)\in\mathbb R^{128\times128}
$$

such that

$$
\boxed{
\mathcal V(U^\dagger O U)=T(U)\mathcal V(O)
}.
$$

The transformed covariance is therefore

$$
\boxed{
C'=T(U)CT(U)^T
}.
$$

Using the rotated matrix with the unrotated covariance would assign uncertainties to the wrong linear combinations of matrix elements.

## 3. Unitary gauge rotations preserve total isotropic variance

The Hilbert–Schmidt norm is invariant under unitary similarity:

$$
\|U^\dagger O U\|_F=\|O\|_F.
$$

Therefore the real representation $T(U)$ is orthogonal:

$$
T(U)^TT(U)=I_{128}.
$$

For any covariance,

$$
\operatorname{Tr}C'
=
\operatorname{Tr}\left[TCT^T\right]
=
\operatorname{Tr}C.
$$

The gauge rotation redistributes uncertainty among matrix elements but does not change the total variance.

For an isotropic covariance

$$
C=\sigma^2I,
$$

we obtain

$$
C'=\sigma^2I.
$$

This identity is used as an executable consistency test.

## 4. Symmetry restoration is a noninvertible linear projection

Let

$$
O_{\mathrm{sym}}=\mathcal S_\Gamma[O]
$$

be the zone-center irrep projection. Its real representation is

$$
y_{\mathrm{sym}}=S_\Gamma y,
$$

with

$$
S_\Gamma^2=S_\Gamma.
$$

The covariance must become

$$
\boxed{
C_{\mathrm{sym}}=S_\Gamma C S_\Gamma^T
}.
$$

Unlike a unitary gauge transformation, $S_\Gamma$ is rank reducing. The projected covariance is generally singular because forbidden matrix directions have been removed exactly.

This singularity is physical and should not be replaced silently by independent finite errors in the eliminated components.

## 5. General chain rule

For a sequence of linear matrix-processing operations

$$
y_n=T_nT_{n-1}\cdots T_1y_0,
$$

the covariance is

$$
\boxed{
C_n=
T_nT_{n-1}\cdots T_1
C_0
T_1^T\cdots T_{n-1}^TT_n^T
}.
$$

The implemented ingestion sequence is typically

$$
\text{raw matrix}
\xrightarrow{\text{gauge}}
\text{reference gauge}
\xrightarrow{\text{symmetry}}
\text{macroscopic symmetry form}
\xrightarrow{\text{GLS}}
\text{Kane parameters}.
$$

Every stage transforms both the mean matrix and its covariance.

## 6. Parameter covariance after processing

Let $X$ be the Kane design after all matrices and covariances have been processed. Generalized least squares gives

$$
\widehat p=
(X^TC^{-1}X)^{-1}X^TC^{-1}y
$$

and

$$
\boxed{
\operatorname{Cov}(\widehat p)
=(X^TC^{-1}X)^{-1}
}.
$$

If a symmetry projection makes $C$ singular, the fit uses an explicitly regularized inverse or a reduced-coordinate representation. The sensitivity to that regularization must be reported.

## 7. End-to-end synthetic verification

The executable test performs the following sequence:

1. Generate exact Kane Hamiltonians from a known parameter set.
2. Apply independent random unitary gauges at each $\mathbf k$.
3. Add a controlled, symmetry-forbidden $\Gamma_6$–$\Gamma_8$ term at $\Gamma$.
4. Attach a known matrix covariance.
5. Recover the reference gauge from overlap matrices.
6. Push the covariance through the gauge rotation.
7. Apply zone-center symmetry restoration to both matrix and covariance.
8. Fit the recovered matrices using covariance-weighted projection.

The injected values of

$$
E_v,E_g,\Delta,P,F,\gamma_1,\gamma_2,\gamma_3
$$

are recovered within $2\times10^{-9}$ relative or absolute tolerance in the current test, while the forbidden zone-center term is removed and recorded by the pre-projection symmetry residual.

The complete local suite currently reports **23 tests passed**.

## 8. Data integrity and provenance

The matrix dataset format records:

- composition;
- temperature;
- volume;
- $\mathbf k$;
- matrix type;
- optional frequency;
- complex $8\times8$ matrix;
- basis-overlap matrix;
- optional $128\times128$ covariance;
- per-record metadata;
- global provenance.

Datasets are stored in a versioned compressed NPZ representation and may be verified with SHA-256 before loading.

## 9. Consequence for AHC calculations

Convergence uncertainty cannot be attached only to final eigenvalues if the research objective is to recover temperature-dependent Kane parameters. The required uncertainty object is the covariance of the projected matrix elements, or enough statistically independent replicates to estimate it.

At minimum, repeated calculations over convergence settings should retain the correlated variation of:

- diagonal band-edge blocks;
- $\Gamma_6\leftrightarrow\Gamma_8$ coupling elements;
- $\Gamma_6\leftrightarrow\Gamma_7$ coupling elements;
- and the mixed valence terms carrying $\gamma_2$ and $\gamma_3$.

A matrix correction smaller than its transformed covariance or symmetry-restoration scale is not a resolved physical parameter shift.
