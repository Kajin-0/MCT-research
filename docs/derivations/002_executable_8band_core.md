# Derivation 002 — Executable bulk 8-band Kane core and invariant projection

**Status:** implemented and unit-tested  
**Claim level:** executable mathematical infrastructure  
**Novelty status:** methodology only; prior-art audit incomplete

## 1. Purpose

This implementation converts the finite-temperature research program into a falsifiable matrix model. It provides:

1. a homogeneous bulk 8-band Kane Hamiltonian,
2. explicit basis and unit conventions,
3. Hermiticity and time-reversal checks,
4. full-matrix parameter recovery,
5. a model-closure residual,
6. and a pre-fit identifiability diagnostic for the selected $\mathbf{k}$ grid.

The implementation intentionally excludes strain, magnetic field, heterostructure operator ordering, and bulk-inversion-asymmetry terms. Those extensions should be added only after the bulk core is validated.

## 2. Basis and units

The ordered basis is

$$
\begin{aligned}
&|\Gamma_6,+1/2\rangle,\ |\Gamma_6,-1/2\rangle,\\
&|\Gamma_8,+3/2\rangle,\ |\Gamma_8,+1/2\rangle,
|\Gamma_8,-1/2\rangle,\ |\Gamma_8,-3/2\rangle,\\
&|\Gamma_7,+1/2\rangle,\ |\Gamma_7,-1/2\rangle.
\end{aligned}
$$

The implementation uses:

- energy in eV,
- wave vector in $\text{\AA}^{-1}$,
- Kane coupling $P$ in eV$\cdot\text{\AA}$,
- $\alpha=\hbar^2/(2m_0)=3.809982116\ \text{eV}\,\text{\AA}^2$.

The relation between $P$ and the Kane energy is

$$
E_P=\frac{P^2}{\alpha}.
$$

## 3. Parameter vector

The fitted parameter vector is

$$
\mathbf p=
\left(E_v,E_g,\Delta,P,F,\gamma_1,\gamma_2,\gamma_3\right).
$$

The $\Gamma$-point energies are

$$
E_{\Gamma_8}=E_v,
\qquad
E_{\Gamma_6}=E_v+E_g,
\qquad
E_{\Gamma_7}=E_v-\Delta.
$$

The sign of $E_g$ is retained, so inverted HgTe-like ordering corresponds to $E_g<0$.

## 4. Matrix-level parameter recovery

The Hamiltonian is affine in the parameter vector:

$$
H_{8K}(\mathbf k;\mathbf p)
=H_{\mathrm{fixed}}(\mathbf k)
+\sum_a p_a M_a(\mathbf k).
$$

The fixed part contains the parameter-independent free-electron contribution to the $\Gamma_6$ block. The template matrices are generated exactly as

$$
M_a(\mathbf k)=
H_{8K}(\mathbf k;\mathbf e_a)-H_{\mathrm{fixed}}(\mathbf k),
$$

where $\mathbf e_a$ is a unit vector in parameter space.

For target matrices $H^{\mathrm{target}}(\mathbf k_j)$, the implementation solves

$$
\mathbf p^*
=
\underset{\mathbf p}{\operatorname{argmin}}
\sum_j w_j
\left\|
H^{\mathrm{target}}(\mathbf k_j)
-H_{8K}(\mathbf k_j;\mathbf p)
\right\|_F^2.
$$

Real and imaginary matrix elements are both retained. This is stronger than fitting only eigenvalues because it preserves interband coupling and phase-sensitive matrix structure after gauge fixing.

## 5. Closure residual

After projection, define

$$
R(\mathbf k_j)=
H^{\mathrm{target}}(\mathbf k_j)
-H_{8K}(\mathbf k_j;\mathbf p^*).
$$

The implemented normalized residual is

$$
\rho=
\sqrt{
\frac{
\sum_j w_j\|R(\mathbf k_j)\|_F^2
}{
\sum_j w_j
\|H^{\mathrm{target}}(\mathbf k_j)-H^{\mathrm{target}}(0)\|_F^2
}
}.
$$

A synthetic perturbation outside the declared Kane manifold produces a nonzero residual, demonstrating that the fit does not automatically absorb arbitrary matrix structure into the standard parameters.

## 6. Exact tests currently passed

The test suite verifies:

- Hermiticity below $10^{-13}$ in Frobenius norm;
- time-reversal invariance below $10^{-13}$;
- exact $2+4+2$ degeneracy structure at $\Gamma$;
- exact synthetic recovery of all eight fitted parameters;
- relative projection residual below $10^{-12}$ for noiseless synthetic data;
- detection of a deliberately introduced non-Kane perturbation;
- rank deficiency for an axis-only $\mathbf{k}$ grid;
- full rank after adding a mixed-component direction.

The current automated result is **11 tests passed**.

## 7. First methodological result: $\mathbf{k}$-grid identifiability

Sampling only the Cartesian axes gives a design rank of seven rather than eight. The reason is structural. On an axis-only grid,

$$
k_xk_y=k_xk_z=k_yk_z=0,
$$

so the mixed quadratic invariants carrying $\gamma_3$ vanish. Therefore, $\gamma_3$ is exactly unidentifiable regardless of numerical precision or the number of radial samples.

At least one mixed-component direction is required, such as

$$
[110],\quad [101],\quad [011],\quad \text{or}\quad [111].
$$

This is a necessary design condition for any first-principles extraction of the full Kane parameter set.

## 8. Second methodological result: the small-$k$ conditioning problem

The matrix templates scale differently:

$$
M_{E_g},M_{\Delta},M_{E_v}=O(1),
\qquad
M_P=O(k),
\qquad
M_F,M_{\gamma_i}=O(k^2).
$$

Consequently, the uncertainty in quadratic parameters scales approximately as

$$
\sigma_{\gamma_i},\sigma_F
\propto
\frac{\sigma_H}{k_{\max}^2},
$$

where $\sigma_H$ is the characteristic matrix uncertainty. Driving the fit window toward $k=0$ reduces higher-order truncation bias but amplifies numerical and first-principles noise.

For the current seven-direction, three-shell grid, the unscaled design condition number was:

| $k_{\max}$ ($\text{\AA}^{-1}$) | Condition number |
|---:|---:|
| 0.0025 | $1.34\times10^5$ |
| 0.0050 | $3.35\times10^4$ |
| 0.0100 | $8.38\times10^3$ |
| 0.0200 | $2.10\times10^3$ |
| 0.0400 | $5.24\times10^2$ |

The approximate $k_{\max}^{-2}$ scaling is the expected signature of quadratic-in-$k$ parameter extraction.

## 9. Correct fitting strategy

The correct procedure is not to choose the smallest possible $k$ window. It is to perform a multi-window analysis:

1. fit over several $k_{\max}$ values;
2. propagate matrix uncertainty through the design matrix;
3. monitor parameter drift and closure residual;
4. identify a stability interval where truncation bias and variance are both controlled;
5. extrapolate only when the scaling of the omitted invariants is established.

The final reported Kane parameters should include both:

- statistical/numerical covariance at fixed window;
- systematic window-dependence uncertainty.

## 10. Immediate next extensions

1. Implement explicit cubic-group representation matrices and rotation tests.
2. Add gauge-alignment utilities for projected ab initio subspaces.
3. Add separate $P_8$ and $P_7$ templates and compare closure residuals.
4. Add covariance-weighted generalized least squares.
5. Add higher-order invariant templates to diagnose whether residuals are cubic, quartic, symmetry-breaking, or frequency-dependent.
6. Benchmark the implementation against published HgTe and CdTe dispersions.

## Source convention

The basis and parameter convention follows the standard HgTe/CdTe 8-band framework described by Novik et al., arXiv:cond-mat/0409392. The executable implementation must still be cross-checked term by term against the published matrix convention before use with external data.
