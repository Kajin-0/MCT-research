# R07 threshold-retaining causal reduction and inversion certificates

Date: 2026-10-11. Contribution: R07 only. Persistent research goal resumed by
the user. This package extends the [analytical foundation](../analytical_first_2026-10-11/README.md);
it leaves its negative results and all numerical acceptance gates intact.

**Decision: stop physical prediction at the missing material-input boundary.**
Three distinct derivation/falsification cycles give a useful conditional
equation and stronger error certificates. They do not supply a physical HgCdTe
kernel or x_c. No empirical alloy-gap coefficient enters the work.

The most consequential reduction is **PROVEN UNDER ASSUMPTIONS**: for two
positive Feshbach measures on a common support-free real interval, the change
of the mass kernel is bounded by the change of the common inverse. This remains
true at a finite threshold endpoint even when the energy derivatives diverge.
If the branch-denominator errors are ε6, ε8 and the true reduced mass has an
independently certified lower composition secant slope m>0, then

    |x_c - x_c,app| <= max(ε6, ε8)/m.

The earlier certificate [ε_m+(L_m/u)ε_s]/m remains valid under its own
hypotheses. The joint positive-measure argument avoids separately estimating
an infinite L_m in the common real gap. It does not transfer to a retarded
continuum: a bounded positive-density bath explicitly falsifies that extension.

A second **PROVEN UNDER ASSUMPTIONS** result supplies a causal threshold
closure. Retain a nonnegative infrared density exactly, and linearize only
its positive complement:

    D_α,T(z,x) = (1+A_α,R)z - [e_α+C_α,R+A_α,R t_α]
                - K_α,IR(z,x),       α=6,8.

The complement has a uniform finite first derivative if its density is bounded
by B ε^p with p>1 and its remote support is uniformly separated. Explicit
value errors scale as h^p (1<p<2), h² log(1+Λ/h) (p=2), or h² (p>2).
A square-root channel is kept, rather than represented by a divergent A.
The causal equation applies to static positive-measure kernels with the
specified threshold information; it is not an assertion about the actual
alloy's density or its self-consistent concentration exponent.

**FALSIFIED:** threshold exponent/amplitude, regular static/dynamic moments,
total weight and support distances together uniquely determine an exact
inversion. A common infrared measure can be added to the prior positive
four-pole moment counterexample without removing its distinct crossing roots.
An interior, physically qualified mass contraction or an error bound on it
remains indispensable. Endpoint single impurities do not universally supply it.

| Artifact | Contents |
|---|---|
| [derivation.md](derivation.md) | Exact fractional split, positive lower envelope, uniform remainder and derivative bounds, joint mass/root theorem |
| [cycles_and_boundary.md](cycles_and_boundary.md) | Three competing discovery/falsification cycles, counterexamples, minimum information, ranked inputs and decision ledger |
| [literature.md](literature.md) | Primary-source checks and conservative novelty classification |
| [verification.md](verification.md) | Independent integrals/matrices, frozen synthetic audit and reproduction |

The [helpers](../../../../src/mct_research/threshold_causal_closure.py) and
[tests](../../../../tests/test_r07_threshold_causal_closure.py) are additive
mathematical checks. They establish no material validation. The DFT repository,
detached supervisors, existing queues, unrelated program states and main branch
are untouched. No new expensive calculation is proposed or launched.

Temperature, broadened peak prediction and topology remain separate tasks.
The persistent broad research goal is not marked complete: a defensible physical
equation still needs independent material information and its accuracy gates.
