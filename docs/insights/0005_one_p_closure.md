# Insight 0005 — The one-$P$ Kane model is a testable constraint, not a symmetry identity

**Status:** analytically formulated and executable synthetic test passed  
**Novelty:** candidate methodology; prior-art status unconfirmed  
**Importance:** distinguishes true temperature renormalization of interband coupling from a scalar-gap-only model

## Statement

The conventional 8-band Kane Hamiltonian uses one momentum coupling $P$ for both

$$
\Gamma_6\leftrightarrow\Gamma_8
$$

and

$$
\Gamma_6\leftrightarrow\Gamma_7.
$$

For a projected, frequency-dependent, finite-temperature quasiparticle Hamiltonian, equality of the two effective reduced couplings is not guaranteed merely by cubic symmetry. The nested extension is

$$
P_8:\Gamma_6\leftrightarrow\Gamma_8,
\qquad
P_7:\Gamma_6\leftrightarrow\Gamma_7.
$$

The conventional model is recovered by the constraint

$$
P_8=P_7=P.
$$

## Closure diagnostic

Define

$$
\eta_P=
\frac{2|P_8-P_7|}{|P_8|+|P_7|}.
$$

The one-$P$ model is inadequate only when all of the following hold:

1. $\eta_P$ exceeds propagated numerical and first-principles uncertainty;
2. the two-$P$ model reduces the closure residual on held-out $\mathbf{k}$ points;
3. the result is stable against gauge construction and fitting window;
4. the trend is reproducible across temperatures or independent calculations;
5. the improvement cannot be attributed to an omitted higher-order invariant.

## Executable synthetic test

Synthetic matrices were generated with

$$
P_8=1.02P,
\qquad
P_7=0.98P.
$$

The standard one-$P$ fit produced a finite closure residual, while the two-$P$ model recovered both couplings to numerical precision and reduced the residual below $10^{-12}$.

This proves that the implemented closure test can distinguish a genuine split in reduced couplings from changes in $E_g$, $\Delta$, $F$, or $\gamma_i$.

## Physical interpretation

A measured or calculated $P_8\ne P_7$ would not automatically mean that the microscopic momentum operator has two unrelated bare matrix elements. The effective difference could arise from:

- state-dependent quasiparticle residues;
- energy-dependent self-energy evaluated near different poles;
- remote-band downfolding;
- phonon-induced wavefunction renormalization;
- alloy-disorder averaging;
- or an insufficient static 8-band reduction.

Therefore the result should be interpreted as failure of the **static one-$P$ effective model**, not immediately as a change in one bare atomic matrix element.

## Strong validation strategy

Fit the nested models on one set of $\mathbf{k}$ points and compare predictive residuals on symmetry-related held-out directions. Use covariance-weighted likelihood or cross-validation rather than declaring success from the in-sample residual alone.
