# Insight 0010 — Current covariance propagation is conditional on the estimated gauge

**Status:** documented limitation  
**Importance:** prevents under-reporting uncertainty in projected Kane parameters  
**Implementation status:** gauge-map covariance is propagated; gauge-estimation uncertainty is not

## Statement

The current pipeline estimates a unitary gauge rotation $\widehat U$ from an overlap matrix and then transforms an operator as

$$
O'=\widehat U^\dagger O\widehat U.
$$

For a **fixed** $\widehat U$, the real observation map is linear and the implemented covariance transformation

$$
C'=T(\widehat U)C T(\widehat U)^T
$$

is exact.

However, $\widehat U$ is itself estimated from finite-precision wavefunctions or overlap matrices. The present covariance therefore means

$$
\boxed{
\operatorname{Cov}(O'\mid\widehat U)
}
$$

rather than the full marginal covariance

$$
\operatorname{Cov}(O').
$$

## Missing contribution

If the overlap-derived gauge fluctuates by $\delta U$, then to first order

$$
\delta O'
\approx
\widehat U^\dagger\delta O\widehat U
+
\delta U^\dagger O\widehat U
+
\widehat U^\dagger O\delta U.
$$

The existing implementation includes only the first term. It does not yet include:

- covariance of the estimated overlap matrix;
- covariance of the Procrustes/polar-decomposition rotation;
- correlations between $O$ and $\widehat U$;
- nonlinear amplification when principal angles approach $\pi/2$ or singular values of the overlap become small.

## Reporting rule

Until gauge-estimation uncertainty is implemented, every parameter covariance derived from processed matrices must be described as:

> conditional on the fixed overlap-derived gauge used in the projection.

Principal-angle and minimum-singular-value diagnostics remain mandatory. A parameter shift should not be considered resolved when it is comparable to the variation obtained by plausible gauge reconstructions, subspace windows, or overlap perturbations.

## Deferred extension

A later uncertainty layer may use one or more of:

1. bootstrap or replicate wavefunction calculations;
2. Monte Carlo perturbation of overlap matrices;
3. differential propagation through the polar decomposition;
4. joint covariance of operator and overlap data;
5. Bayesian treatment of the subspace gauge.

This extension is deferred because it is not required to reconstruct Hansen data, audit prior art, or compare analytical bandgap models. It becomes necessary before reporting precision finite-temperature changes in off-diagonal Kane parameters from ab initio matrices.