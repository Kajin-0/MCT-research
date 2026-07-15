# Derivation 004 — Gauge-aligned, symmetry-restored, covariance-weighted Kane projection

**Status:** implemented and locally unit-tested  
**Claim level:** mathematical and computational reliability layer  
**Novelty status:** methodology; prior-art audit incomplete

## 1. Why this layer is necessary

A first-principles calculation does not return a unique matrix representation of the low-energy Hamiltonian. Within an isolated or nearly degenerate subspace, the calculated Bloch basis may be changed by an arbitrary unitary matrix without changing the physical subspace.

If the target basis matrix is $\Psi$ and the chosen Kane reference basis is $\Phi$, then

$$
\Psi\rightarrow \Psi U,
\qquad U^\dagger U=I
$$

represents the same electronic subspace. Matrix elements such as $P$, $P_8$, $P_7$, and $\gamma_3$ are therefore meaningless until the gauge is fixed.

The finite-temperature AHC problem makes this more severe because the electronic eigenvectors themselves may change with temperature. Off-diagonal self-energy terms cannot be interpreted by comparing raw eigenvectors from independent calculations.

## 2. Unitary Procrustes alignment

Let $\Phi,\Psi\in\mathbb C^{N\times m}$ have orthonormal columns:

$$
\Phi^\dagger\Phi=I_m,
\qquad
\Psi^\dagger\Psi=I_m.
$$

Choose the target gauge by minimizing

$$
U_*=\underset{U^\dagger U=I}{\operatorname{argmin}}
\|\Psi U-\Phi\|_F^2.
$$

Expanding the norm gives

$$
\|\Psi U-\Phi\|_F^2
=2m-2\operatorname{Re}\operatorname{Tr}
\left(U^\dagger\Psi^\dagger\Phi\right).
$$

Define the overlap matrix

$$
M=\Psi^\dagger\Phi.
$$

With singular-value decomposition

$$
M=L\Sigma R^\dagger,
$$

the maximizing unitary is

$$
\boxed{U_*=LR^\dagger}.
$$

This is the unitary polar factor of the overlap. The aligned target basis is

$$
\boxed{\Psi_{\mathrm{aligned}}=\Psi U_*}.
$$

## 3. Principal-angle diagnostics

The singular values satisfy

$$
\sigma_i(M)=\cos\theta_i,
$$

where $\theta_i$ are the principal angles between the target and reference subspaces.

Two gauge-invariant diagnostics follow.

### Projector distance

Let

$$
P_\Phi=\Phi\Phi^\dagger,
\qquad
P_\Psi=\Psi\Psi^\dagger.
$$

Then

$$
\boxed{
d_P=
\frac{\|P_\Phi-P_\Psi\|_F}{\sqrt{2m}}
=
\sqrt{\frac{1}{m}\sum_i\sin^2\theta_i}
}.
$$

### Aligned-basis residual

At the Procrustes optimum,

$$
\boxed{
d_B^2=
\frac{\|\Psi U_*-\Phi\|_F^2}{m}
=2-\frac{2}{m}\sum_i\cos\theta_i
}.
$$

The alignment becomes unstable as

$$
\sigma_{\min}(M)\rightarrow0.
$$

Therefore, every projected parameter set must report at least:

- $\sigma_{\min}$;
- the maximum principal angle;
- $d_P$;
- and $d_B$.

A smooth eigenvalue curve is not sufficient evidence of a stable basis.

## 4. Symmetry-constrained gauge at $\Gamma$

At the zone center, the Kane basis decomposes as

$$
\Gamma_6\oplus\Gamma_8\oplus\Gamma_7
$$

with dimensions $2+4+2$.

Near the zero-gap transition, an unconstrained $U(8)$ alignment could numerically mix $\Gamma_6$ and $\Gamma_8$ states merely because their eigenvalues approach one another. That would destroy the physical meaning of the signed gap.

The correct zone-center gauge is block restricted:

$$
\boxed{
U_\Gamma=U_6\oplus U_8\oplus U_7
}.
$$

Each irreducible subspace is aligned independently. The symmetry labels, not energy ordering, anchor the crossing.

If the target operator is represented in the original target gauge as $O$, then after $\Psi\rightarrow\Psi U$ its matrix is

$$
\boxed{O\rightarrow U^\dagger O U}.
$$

## 5. Exact symmetry projection at $\Gamma$

For one copy each of $\Gamma_6$, $\Gamma_8$, and $\Gamma_7$, Schur's lemma requires a symmetry-preserving zone-center operator to be scalar in each irreducible block.

Let $P_r$ be the projector onto irrep $r$ and $d_r$ its dimension. Define

$$
\boxed{
\mathcal S_\Gamma[O]
=
\sum_{r\in\{6,8,7\}}
\frac{\operatorname{Tr}(P_rO)}{d_r}P_r
}.
$$

Explicitly,

$$
\mathcal S_\Gamma[O]
=
\frac{\operatorname{Tr}(P_6O)}{2}P_6
+
\frac{\operatorname{Tr}(P_8O)}{4}P_8
+
\frac{\operatorname{Tr}(P_7O)}{2}P_7.
$$

This map is idempotent,

$$
\mathcal S_\Gamma^2=\mathcal S_\Gamma,
$$

and self-adjoint under the Frobenius inner product. It is therefore the orthogonal projection onto the symmetry-preserving zone-center operator space.

Consequently,

$$
\boxed{
\mathcal S_\Gamma[O]
=
\underset{X\in\mathcal V_\Gamma}{\operatorname{argmin}}
\|O-X\|_F
},
$$

where $\mathcal V_\Gamma$ is the allowed irrep-scalar subspace.

The symmetry residual is

$$
\boxed{
\epsilon_\Gamma=
\frac{\|O-\mathcal S_\Gamma[O]\|_F}{\|O\|_F}
}.
$$

A large $\epsilon_\Gamma$ may indicate finite-SQS symmetry breaking, an incomplete configurational average, a gauge error, or an actual symmetry-breaking perturbation.

## 6. Time-reversal pair restoration

Let $U_T$ be the unitary part of time reversal in the declared Kane basis. A pair of matrices must satisfy

$$
H(\mathbf k)=U_TH(-\mathbf k)^*U_T^\dagger.
$$

The minimum symmetric average for the $+\mathbf k$ matrix is

$$
\boxed{
H_{\mathrm{TR}}(\mathbf k)
=
\frac12\left[
H(\mathbf k)+U_TH(-\mathbf k)^*U_T^\dagger
\right]
}.
$$

The corresponding $-\mathbf k$ matrix is constructed by the reciprocal expression. The implemented map is idempotent and exactly satisfies the pair relation to numerical precision.

## 7. Covariance-weighted projection

After gauge and symmetry processing, vectorize the complex target matrices into real observation vectors $y_j$. Let $X_j$ contain the vectorized Kane invariant templates and let $C_j$ be the observation covariance.

The generalized least-squares objective is

$$
\boxed{
\chi^2(\mathbf p)
=
\sum_j
\left(y_j-X_j\mathbf p\right)^T
C_j^{-1}
\left(y_j-X_j\mathbf p\right)
}.
$$

Stacking the whitened systems gives

$$
\widetilde X=
\begin{pmatrix}
C_1^{-1/2}X_1\\
C_2^{-1/2}X_2\\
\vdots
\end{pmatrix},
\qquad
\widetilde y=
\begin{pmatrix}
C_1^{-1/2}y_1\\
C_2^{-1/2}y_2\\
\vdots
\end{pmatrix}.
$$

The solution is

$$
\boxed{
\widehat{\mathbf p}
=
\left(\widetilde X^T\widetilde X\right)^{-1}
\widetilde X^T\widetilde y
}.
$$

If the supplied covariances are absolute, the parameter covariance is

$$
\boxed{
\operatorname{Cov}(\widehat{\mathbf p})
=
\left(\widetilde X^T\widetilde X\right)^{-1}
}.
$$

If only relative weights are known, this matrix is multiplied by the estimated residual variance

$$
\widehat s^2=\frac{\chi^2}{N_{\mathrm{obs}}-N_{\mathrm{par}}}.
$$

The implementation returns:

- the complete parameter covariance matrix;
- parameter standard errors;
- the parameter correlation matrix;
- $\chi^2$ and reduced $\chi^2$;
- singular values and the whitened design condition number;
- and covariance-regularization diagnostics.

## 8. Covariance changes identifiability

The correct rank condition is not merely

$$
\operatorname{rank}(X)=N_{\mathrm{par}}.
$$

It is

$$
\boxed{
\operatorname{rank}(C^{-1/2}X)=N_{\mathrm{par}}
}.
$$

Thus, a mixed-direction $\mathbf k$ grid is necessary to identify $\gamma_3$, but it is not sufficient if the covariance model assigns negligible precision to the matrix elements carrying the mixed invariants.

The experimental or numerical error model is part of the model-identification problem.

## 9. Covariance regularization

An estimated covariance may be nearly singular. The implementation diagonalizes

$$
C=V\Lambda V^T
$$

and clips eigenvalues below

$$
\lambda_{\mathrm{floor}}
=r_C\lambda_{\max}.
$$

The whitener is then

$$
C^{-1/2}
=
V\Lambda_{\mathrm{clip}}^{-1/2}V^T.
$$

Every result must be checked against the covariance floor $r_C$. A parameter conclusion that changes materially with reasonable regularization is not resolved.

## 10. Current executable checks

The combined suite currently passes 20 local tests, including:

- arbitrary global unitary gauge recovery;
- independent $\Gamma_6$, $\Gamma_8$, and $\Gamma_7$ gauge recovery;
- correct operator transformation under basis rotation;
- rejection of nearly orthogonal subspaces;
- exact removal of forbidden zone-center couplings;
- idempotent time-reversal symmetrization;
- covariance-weighted recovery of noiseless Kane parameters;
- downweighting of a deliberately corrupted high-variance zone-center matrix;
- and all previous Hamiltonian, closure, and two-$P$ tests.

A GitHub Actions workflow now tests Python 3.11 and 3.13 on every push and pull request.

## 11. Acceptance protocol for real AHC matrices

A temperature-dependent parameter change should not be called physical unless all of the following hold:

1. The relevant subspace has acceptable principal angles and $\sigma_{\min}$.
2. The extracted parameters are stable under allowed gauge choices.
3. The zone-center symmetry residual is below the claimed effect size.
4. Time-reversal residuals are below the claimed effect size.
5. The whitened design is full rank.
6. The result is stable against covariance regularization.
7. The result is stable across a justified $k$-window interval.
8. The parameter shift exceeds its propagated covariance and systematic numerical floor.
9. A nonzero closure residual exceeds the null distribution generated by gauge, symmetry, and numerical perturbations.

## 12. Stronger gauge-covariant closure target

The present implementation aligns the basis first and then fits the Hamiltonian. A stronger future diagnostic is

$$
\boxed{
\rho_{\mathrm{gc}}
=
\underset{U\in\mathcal G}{\min}
\underset{\mathbf p}{\min}
\left\|
W\left[U^\dagger H^{\mathrm{target}}U-H_{8K}(\mathbf p)\right]
\right\|_2
},
$$

where $\mathcal G$ is the physically allowed gauge group and $W$ is the covariance whitener.

This would distinguish genuine model nonclosure from a poor but physically equivalent matrix gauge.

## 13. Limitations

- The code currently vectorizes all complex matrix elements. Hermitian redundancy is therefore counted explicitly; a supplied covariance should represent those correlations.
- Full cubic double-group operations away from $\Gamma$ are not yet implemented.
- The current gauge utilities assume the relevant subspaces have already been selected or disentangled.
- No real DFT, GW, or AHC matrix dataset has yet been processed.
- The matrix convention still requires a term-by-term external benchmark before scientific parameter values are reported.

## Literature anchors

- N. Marzari and D. Vanderbilt, generalized Wannier gauges for composite bands.
- I. Souza, N. Marzari, and D. Vanderbilt, disentanglement of connected subspaces.
- J.-M. Lihm and C.-H. Park, matrix-valued electron–phonon self-energy and wavefunction renormalization.
