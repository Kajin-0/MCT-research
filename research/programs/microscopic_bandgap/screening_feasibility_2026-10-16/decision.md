# Decision: retain the chemical screening observation; admit neither new run

2026-10-16, from clean/pushed **5dc77a9**. Analytical/read-only phase. **Zero
native QE, MPI, build, source edit or DFT write.** The useful new measurement is
already obtainable from the accepted matched HSE packets; another outer step is
not needed to reject a closed six-state interpretation.

**CALCULATED, independently checked:** the second-state chemical activation
has a positive fixed-frame Γ6-minus-Γ8 trace, **+39.811503589 meV**, but its
action outside the six reference states has norm **95.541080 meV**. All six
leakage singular values exceed **91.550098 meV**. The compression is nearly
sector-scalar; that does **not** make its full action a six-state mass operator.
The first-state leakage was120.135460meV and the relaxation changes the outside
action by32.450817meV. These are operator-action norms, not gap errors, linewidths
or estimates of the missing self-energy. See [theory](theory.md) and
[actual-data results](retained_result.json).

**CALCULATED, decisive for another unchanged update:** the ACTUAL matched host
source density gives time-reversal defect lower witnesses3.27666e-7 before and
**0.001395756895** after the one relaxation. The Cd witnesses are2.12e-11 and
4.01839e-7. An independent unit-vector scalar contraction confirms each within
5.2e-15. A small Cd first-state lower witness is not an upper certificate.
Host and second-state Cd therefore fail the prospective strict1e-8 nonmagnetic
qualification. This is new qualification of the retained pair, **not a change
to its accepted finite-acquisition verdict**. Correct FD charge and local zero
spin do not establish a nonlocal TR-invariant state.

| Choice | Scientific gain if qualified | Evidence / resource decision |
|---|---|---|
| A: fresh third build with the unchanged176-source algorithm | One more finite chemical-screening increment, not convergence or a material mass | **NO-GO now.** Source-density symmetry is already disqualified; first/second ACE source exactness cannot cure this. Full-H/FD residual and a symmetry-qualified update are absent. The accepted observer explicitly stops at build2 and is not qualified restart. New source/continuation cannot be assumed. |
| A: extrapolate the two accepted chemical traces | A limiting activation sign only if future increments have an independently uniform bound | **NO-GO for a limiting sign.** Sufficient geometric factors are derived below, but none is measured/certified. Scalar dexx is not such a certificate. |
| B: original16atom e90/f120, stock | Nonlinear screened Cd response at a more useful dilute composition | **NO-GO under12GiB:** nominal source buffer22GiB, prior interrupted RSS26.722GiB; complete bound/time not available. |
| B: one-q streaming of that original target | Same physical problem if full-state/native equivalence and resource gates pass | **NO-GO independently of RAM:** one lossless generation still requires22GiB scratch, exceeding the14GiB owned aggregate cap by8GiB before other output. Whole352-band SCF/restart equivalence remains unqualified. |

The best science-per-cost result is the **read-only A contraction completed
here**, not a new admitted acquisition. Retain the measured chemical screening:
first activation+44.184097meV, after one relaxation+39.811504meV, change
−4.372594meV (exchange+1.239720, local response−5.612314meV). Every Rayleigh
difference confined separately to the two reference sectors is positive for
the updated activation: **[39.591459,40.032986]meV**. This is a statement about
one fixed compression, not ordered-cell spectral edges or random-alloy inversion.

## Quantitative stop and the one future input

**PROVEN UNDER ASSUMPTIONS:** a chemical *projected remainder* of operator norm
less than19.905752meV would preserve the positive trace. This radius is sharp;
it is NOT an achieved error bound. With independently bounded future geometric
increments, sign certification would require q<0.90103694 for the chemical
increment directly, or q<0.51249540 for a common bound on the separate host/Cd
increments. The latter accounts for cancellation: those measured increments
are−16.748792/−21.121385meV. No q is inferred from these observations.

ONE ranked future physics input is the **matched, symmetry-qualified same-state
full-H action on the original six physical probes**, including the screened
change relative to these retained states and explicit state-residual qualification.
It must come from legitimate host/Cd electronic states, not invented occupations
or the nonstationary152/304 trial. It would directly determine the missing
projected remainder and full-H coupling QHP; another total-energy scalar cannot.
[Input/acceptance contract](minimum_input.md) gives falsification, error allocation
and exact reasons that this acquisition is **not presently launch-ready**.

Existing original e90 host frames remain reusable numerical references. They
do not identify an e50/Γ FD state, screened Cd response or an isometric e90→e50
transfer. The original1e-8 gates, cold-solver failures, stream occupation failure,
owner refusals, byte-splice refusal and H304 nonstationarity remain immutable.
No public-optical search, empirical coefficient, physical gap/x_c, convergence
or memory-saving claim. **STOP at the missing qualified state/remainder input.**
