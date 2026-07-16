# Insight 0017 — HgTe is the endpoint sign stress test

**Status:** primary-source prior art and computation-gate result.  
**Novelty status:** historical sign failure is established; a modern resolution is untested.

## Empirical endpoint behavior

Laurenti et al. use

$$
E_g(T)=E_g(0)+a\frac{T^2}{T+b}
$$

with

$$
a_{\mathrm{CdTe}}=-3.25\times10^{-4}\ \mathrm{eV/K},
\qquad b_{\mathrm{CdTe}}=78.7\ \mathrm K,
$$

and

$$
a_{\mathrm{HgTe}}=+6.3\times10^{-4}\ \mathrm{eV/K},
\qquad b_{\mathrm{HgTe}}=11\ \mathrm K.
$$

The algebraic HgTe and CdTe gaps therefore have opposite temperature slopes.

## Historical microscopic failure

Laurenti et al. also tested a temperature-dependent empirical-pseudopotential Debye–Waller model. It was qualitatively reasonable for CdTe but predicted the wrong temperature direction for HgTe.

The reported modeled band-edge movements from 0 to 300 K were approximately:

- CdTe conduction edge: $-16$ meV;
- CdTe valence edge: $+175$ meV;
- HgTe conduction edge: $+49$ meV;
- HgTe valence edge: $+190$ meV.

The total gap response is therefore a difference between much larger band-edge shifts. A plausible total gap can hide incorrect microscopic edge physics.

## Analytical implication

A stronger model should connect the signed thermal amplitude to the evolving $\Gamma_6$ and $\Gamma_8$ character rather than only interpolate endpoint slopes. A candidate low-rank structure is

$$
\Delta E_g^{\mathrm{ep}}(x,T)
=A_6(x)F_6(T)-A_8(x)F_8(T),
$$

followed by a separately treated quasiharmonic term. This is a hypothesis, not an established equation.

## Computation gate

1. Verify CdTe first using complete Fan plus Debye–Waller terms and the smallest converged grids.
2. Stop if CdTe cannot be reproduced consistently across implementations and experiment.
3. Only then calculate HgTe.
4. For HgTe, require separate, reference-consistent shifts of $E_{\Gamma_6}$ and $E_{\Gamma_8}$, not only their difference.
5. Stop if starting-point, gauge, or quasiharmonic uncertainty is comparable to the endpoint sign effect.

The eventual analytical target should reproduce both endpoint signs and trace them to symmetry-resolved thermal couplings under held-out validation.
