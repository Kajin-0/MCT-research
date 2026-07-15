# Insight 0001 — Average zincblende symmetry protects the Γ6–Γ8 crossing

**Status:** derived from representation theory  
**Novelty:** not claimed  
**Importance:** prevents an incorrect avoided-crossing interpretation

## Statement

For unstrained bulk $\mathrm{Hg}_{1-x}\mathrm{Cd}_x\mathrm{Te}$ after configurational and thermal averaging, the effective Hamiltonian at $\Gamma$ retains the macroscopic zincblende double-group symmetry. The $\Gamma_6$ and $\Gamma_8$ states belong to inequivalent irreducible representations.

If the self-energy respects the same symmetry,

$$
D(g)\Sigma(\Gamma,\omega,T)D^{\dagger}(g)=
\Sigma(\Gamma,\omega,T),
$$

then Schur's lemma requires

$$
\Sigma(\Gamma,\omega,T)=
\sigma_6\mathbf I_2\oplus
\sigma_8\mathbf I_4\oplus
\sigma_7\mathbf I_2.
$$

Therefore,

$$
\boxed{\Sigma_{\Gamma_6,\Gamma_8}(\Gamma,\omega,T)=0}
$$

for the symmetry-restored bulk problem.

## Consequence

Electron–phonon renormalization can move the $\Gamma_6$ and $\Gamma_8$ energies through one another without generically opening an avoided-crossing gap:

$$
E_g(T)=E_{\Gamma_6}^0-E_{\Gamma_8}^0
+\operatorname{Re}[\sigma_6(T)-\sigma_8(T)].
$$

The sign change of $E_g$ remains meaningful.

## Where off-diagonal terms can still matter

- inside the degenerate $\Gamma_8$ manifold;
- away from $\Gamma$;
- under strain or external fields;
- at interfaces and heterostructures;
- in individual unsymmetrized SQS configurations;
- between states sharing compatible symmetry.

## Computational check

After projection and symmetry restoration, calculate

$$
\epsilon_{68}=
\frac{\|P_6\Sigma P_8\|_F}
{\|\Sigma\|_F}.
$$

The value should approach the numerical symmetry tolerance. A finite value after convergence indicates incomplete symmetry restoration, a gauge problem, or genuine symmetry breaking in the modeled system.