# Insight 0002 — Temperature renormalization should be tested as a model-closure problem

**Status:** proposed formal diagnostic  
**Novelty:** potentially useful methodology; prior-art audit incomplete

## Statement

A finite-temperature calculation should not assume that electron–phonon interaction merely changes the conventional Kane parameters. It should test whether the projected quasiparticle Hamiltonian remains inside the standard 8-band invariant manifold.

Let

\[
H_8^{\mathrm{QP}}(\mathbf k,T)
\]

be the projected, gauge-fixed, symmetry-restored quasiparticle Hamiltonian. Let

\[
H_{8K}(\mathbf k;\mathbf p)
\]

be the standard Kane Hamiltonian with

\[
\mathbf p=\{E_g,\Delta,P,F,\gamma_1,\gamma_2,\gamma_3\}.
\]

Determine the best-fit parameter vector by a full matrix fit, not an eigenvalue-only fit:

\[
\mathbf p^*(T)=
\underset{\mathbf p}{\operatorname{argmin}}
\sum_{\mathbf k}w_{\mathbf k}
\left\|H_8^{\mathrm{QP}}(\mathbf k,T)-H_{8K}(\mathbf k;\mathbf p)\right\|_F^2.
\]

Define the residual

\[
R(\mathbf k,T)=H_8^{\mathrm{QP}}-H_{8K}(\mathbf p^*)
\]

and normalized closure metric

\[
\rho(T)=
\sqrt{
\frac{\sum_{\mathbf k}w_{\mathbf k}\|R(\mathbf k,T)\|_F^2}
{\sum_{\mathbf k}w_{\mathbf k}
\|H_8^{\mathrm{QP}}(\mathbf k,T)-H_8^{\mathrm{QP}}(0,T)\|_F^2}
}.
\]

## Interpretation

- \(\rho\) at the numerical projection floor: temperature renormalizes the existing Kane parameters without requiring new structure.
- \(\rho\) significantly above the numerical floor: the conventional parameter manifold is not closed under the calculated self-energy.

## First extension to test

Allow separate interband couplings

\[
P_8:\Gamma_6\leftrightarrow\Gamma_8,
\qquad
P_7:\Gamma_6\leftrightarrow\Gamma_7.
\]

Define

\[
\eta_P=
\frac{2|P_8-P_7|}{|P_8|+|P_7|}.
\]

The standard one-\(P\) model is supported only if \(\eta_P\) is below the combined numerical, gauge, and physical uncertainty.

## Why this matters

A scalar \(E_g(T)\) fit can appear accurate while compensating errors in velocity, mass, and interband coupling. The closure test asks a stronger question: whether the complete low-energy Hamiltonian retains the assumed analytical form.

## Falsification and controls

Repeat the fit while varying:

- \(k\)-window;
- number and directions of sampled \(\mathbf k\) points;
- gauge construction;
- symmetry-restoration tolerance;
- self-energy linearization energy;
- and included remote bands.

A claimed nonclosure is credible only if it survives those controls.
