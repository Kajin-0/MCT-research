# What is still indispensable; why more iterations are not the next experiment

## Established information and the current boundary

The fresh eight-source host fails the intended nonmagnetic-state interpretation:
its nonlocal density TR witness is near1, although local spin density is zero.
The actual176-column ACE span has two large missing TR directions (~.90525 each)
plus smaller residuals. Source-action exactness is not operator symmetry. The
27s new direct-kernel probe gives an internal covariance residual~1.65e-16, but
its original cross-run BYTE control refused at~1.4e-17Ry. Do not promote that
experiment to an accepted bit-canonical replay. It supplies diagnostic native
covariance data, not an independently symmetry-qualified HSE SCF.

**Indispensable next input:** a symmetry-qualified nonmagnetic self-consistent
host operator/density matrix, before interpreting a matched Cd Γ8 edge. It must
come from a numerically qualified symmetry-complete exchange approximation or
independent direct-exchange control, not by relabeling the broken quartet's mean.
The currently frozen176-column ACE contract does not supply it. Continuing the
broken trajectory or running Cd cannot independently repair this missing input.

### Minimal symmetry completion theorem (established linear algebra)

For an antiunitary Theta with Theta²=-I and any source subspace S, the unique
smallest Theta-invariant subspace containing S is

    S_complete=S+ThetaS,
    dim(S_complete)=dim(S)+rank[(I-P_S)ThetaS].

Proof: invariance of a superspace containing S forces it to contain ThetaS.
Conversely Theta(S+ThetaS)=ThetaS-S=S+ThetaS. The dimension formula is the
rank of the orthogonal complement. With orthonormal columns U, the squared
leakage singular values are eigenvalues of I-(U†ThetaU)†(U†ThetaU).

For measured first-source176 columns, two leakage singular values are~.90525;
at threshold1e-5 only those two are resolved above threshold. At1e-6 there are10.
This does NOT prove that adding2columns is sufficient at the original1e-8
operator tolerance: smaller components and Gram/roundoff errors require explicit
residual control. Exact completion has dimension at most352, not necessarily178.

Simply averaging V_ACE with its TR transform is not an equivalent source-exact
repair: ThetaS need not lie in S, so the averaged action on S need not equal
the original direct action. Likewise forcing half occupations or changing the
SCF band count is a new numerical/variational protocol. Native aceinit enforces
nbndproj<=nbnd and assumes matching dimensions; its unreviewed extension cannot
be claimed to preserve all source/energy accounting. No such change is launched
or silently introduced here. This is the concrete algorithmic qualification
boundary under the preserved176-band/ACE-arithmetic contract.

## Why charge-density-only input cannot close this problem

**PROVEN counterexample:** occupy the two spin plane waves e^(+iG.r)|up/down>
in a periodic cell, or instead e^(-iG.r)|up/down>, G!=0. Both have exactly the
same local2x2 spin density I/V, hence the same local charge and zero spin density.
Their nonlocal one-body density matrices differ and are exchanged by Theta.
For a nonconstant translationally invariant screened Coulomb kernel, exchange
on the +G up test state samples v(0) for the first source and v(2G) for the second.
Those generally differ. Local charge/spin fields therefore do not identify the
nonlocal exchange operator even with fixed geometry/species/kernel. This is a
finite counterexample, not new material magnetism or a novelty claim. The actual
native local-zero/nonlocal-TR witness makes this information distinction relevant.

## Ranked acquisition by information gained

| Rank | Input | Information gained | Least work and acceptance |
|---|---|---|---|
| 1, now measured diagnostically | Direct kernel covariance with canonical Θ source | Separates a gross fresh-kernel covariance failure from the already measured ACE defect |27s real operator probe, noSCF; internal1.65e-16, overall byte-replay REFUSED; retain raw evidence |
| 2, indispensable | Symmetry-complete ACE/direct control and a qualified nonmagnetic host state | Decides whether the intended Γ6/Γ8 nonmagnetic reduction is usable |First prove constructor/source/occupation/energy equivalence, explicitly bound closure residual and compare direct actions; then one prospectively scoped short control. No guessed energy shift or empirical gap input |
| 3 | Matched Cd self-consistent operator in that SAME qualified domain | Separates chemical response from an uncontrolled host branch |Reuse fixed physical frame and independently bounded windows; original Cd full-SCF remains unrun |
| 4 | HSE k/q and finite-cell qualification | Determines whetherΓ-only/ordered-cell response transfers toward material physics |Source/resource bounds first. Measured one-q buffer1,216,512,000B;8q subtotal9,732,096,000B ONLY. Whole-RAM/output bounds remain OPEN; neither impossibility nor safety follows from that subtotal |
| 5 | Random-alloy directional/environment input plus causal remainder/transversality bounds | Makes a physical x_c identifiable |A qualified impurity/cluster or Γ-projected causal kernel with controlled missing correlations/background dependence, not endpoint/interior polynomial fitting |

Prior identifiability theorems remain in analytical_first/threshold_causal. One
orderedx=.25 configuration and finite source activations do not determine an
alloy composition law. No materialx_c, topological crossing or detector cutoff
can be inferred from these data. The minimum next input is genuinely independent
of the existing scalar local density; nothing is closed by fitting a bowing term.

**Decision:** stop native work at this falsified host/approximation boundary.
Preserve the successful acquisitions AND original refusals. A new symmetry-safe
SCF/constructor protocol is required before another chemical HSE trajectory;
an unchanged native rerun would add no justified physical information.
