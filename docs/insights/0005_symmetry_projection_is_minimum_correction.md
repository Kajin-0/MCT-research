# Insight 0005 — Zone-center symmetry restoration is the unique minimum-norm correction

**Status:** exact mathematical result for the declared irrep decomposition  
**Novelty:** not claimed  
**Importance:** separates controlled symmetry restoration from arbitrary matrix editing

## Statement

For the Kane zone-center decomposition

$$
\Gamma_6\oplus\Gamma_8\oplus\Gamma_7,
$$

with one copy of each irrep, define projectors $P_6$, $P_8$, and $P_7$ with dimensions $2$, $4$, and $2$.

The symmetry-preserving part of any projected operator $O$ is

$$
\boxed{
\mathcal S_\Gamma[O]
=
\frac{\operatorname{Tr}(P_6O)}{2}P_6
+
\frac{\operatorname{Tr}(P_8O)}{4}P_8
+
\frac{\operatorname{Tr}(P_7O)}{2}P_7
}.
$$

This map is an orthogonal projector under the Frobenius inner product:

$$
\mathcal S_\Gamma^2=\mathcal S_\Gamma,
$$

and

$$
\langle A,\mathcal S_\Gamma[B]\rangle_F
=
\langle\mathcal S_\Gamma[A],B\rangle_F.
$$

Therefore,

$$
\boxed{
\mathcal S_\Gamma[O]
=
\underset{X\in\mathcal V_\Gamma}{\operatorname{argmin}}
\|O-X\|_F
},
$$

where $\mathcal V_\Gamma$ is the space of zone-center operators allowed by the average cubic symmetry.

## Consequence

Removing a finite $\Gamma_6$–$\Gamma_8$ coupling after configurational averaging is not an arbitrary deletion. It is part of the unique least-change projection onto the symmetry-allowed operator space.

The removed norm

$$
\epsilon_\Gamma
=
\frac{\|O-\mathcal S_\Gamma[O]\|_F}{\|O\|_F}
$$

must still be reported. It measures how much information is being attributed to finite-SQS symmetry breaking, incomplete averaging, numerical gauge error, or an actual physical symmetry-breaking perturbation.

## Practical rule

A temperature-dependent gap or Kane-parameter change should not be reported with uncertainty below the corresponding symmetry-restoration scale unless the origin of the removed component has been independently resolved.
