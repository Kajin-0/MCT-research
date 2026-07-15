# Insight 0007 — The uncertainty model can make a nominally complete Kane fit unidentifiable

**Status:** derived and implemented  
**Novelty:** methodological; prior-art audit incomplete  
**Importance:** prevents false precision from unweighted matrix fitting

## Statement

Let $X$ be the stacked Kane invariant design matrix and let $C$ be the covariance of the vectorized projected Hamiltonian.

The relevant identifiability condition is

$$
\boxed{
\operatorname{rank}(C^{-1/2}X)=N_{\mathrm{par}}
},
$$

not merely

$$
\operatorname{rank}(X)=N_{\mathrm{par}}.
$$

A geometrically complete $\mathbf k$ grid can therefore become statistically incomplete when the matrix elements carrying a parameter have low precision or are strongly correlated with other elements.

## Example

Mixed-component directions such as $[110]$ are necessary to expose $\gamma_3$ because the relevant templates contain products such as

$$
k_xk_y,
\qquad
k_xk_z,
\qquad
k_yk_z.
$$

However, if the covariance assigns effectively zero precision to the corresponding off-diagonal valence-block elements, the whitened design can lose the $\gamma_3$ direction even though the raw design is full rank.

## Consequence

The computational sampling plan and uncertainty model cannot be designed independently. A first-principles calculation must converge the specific matrix elements that carry each target invariant, not only the eigenvalues or the total Hamiltonian norm.

## Required diagnostics

Every fit should report:

- rank and singular values of $C^{-1/2}X$;
- parameter covariance and correlation;
- sensitivity to covariance regularization;
- and the matrix elements dominating each poorly conditioned singular vector.

A parameter value from an unweighted fit is not a resolved physical result when the matrix uncertainties are anisotropic.
