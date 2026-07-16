# Insight 0008 — Matrix covariance must follow the gauge

**Status:** exact linear propagation result; implemented and tested  
**Novelty:** methodological; prior-art audit incomplete  
**Importance:** prevents internally inconsistent uncertainty after basis alignment

## Statement

If a projected operator changes basis as

$$
O'=U^\dagger O U,
$$

then the real-vectorized matrix changes as

$$
y'=T(U)y,
$$

where $T(U)$ is the $128\times128$ real representation of the similarity transformation.

Therefore,

$$
\boxed{
C'=T(U)CT(U)^T
}
$$

for the matrix covariance.

Rotating the Hamiltonian or self-energy while leaving its covariance unchanged assigns uncertainties to the wrong matrix directions and invalidates the generalized least-squares parameter covariance.

## Symmetry projection

For zone-center symmetry restoration,

$$
y_{\mathrm{sym}}=S_\Gamma y,
$$

so

$$
\boxed{
C_{\mathrm{sym}}=S_\Gamma C S_\Gamma^T
}.
$$

Because $S_\Gamma$ is rank reducing, the resulting covariance is generally singular. This is expected: symmetry-forbidden directions have been removed rather than measured with finite independent uncertainty.

## Executable checks

- A unitary gauge transformation preserves $\operatorname{Tr}C$.
- Isotropic covariance remains isotropic.
- The full end-to-end synthetic pipeline recovers injected Kane parameters after random gauge rotations and controlled symmetry breaking.

## Practical rule

Every operation applied to a projected matrix must expose its linear map on the observation vector so the same map can be applied to covariance. Matrix processing without uncertainty processing is incomplete.
