# What the retained chemical actions identify

## 1. Exact observable and gauge

Let Φ=(Φ6,Φ8) be the original fixed physical8atom reference, ranks2/4,
P=ΦΦ† in exact normalization, Q=1−P, and W=P6/2−P8/4. The actual reference
coefficients embed by physical G labels from7809 into10827, with no truncation
or extra normalization; bytes are independently verified. Our positive-Gram
normalization changes compressed matrices by at most4.4e-14meV. This is floating
analysis bookkeeping, not a substituted physical reference.

For member m=h,c define preliminary PBE density Dm0, first hybrid-inner state
Dm1, direct HSE exchange Xm0/Xm1 and local potentials Lm0(PBE),Lm0(HSE),Lm1(HSE).
The archive measures full six-column actions of

    Am0 = Xm0 + Lm0(HSE) − Lm0(PBE),
    Am1 = Xm1 + Lm1(HSE) − Lm0(PBE),
    Cj = Acj − Ahj,       aj = tr(W Cj).

Kinetic and the fixed species nonlocal/SOC operators cancel WITHIN each
activation. They do not cancel in total Cd-minus-host H. Thus Cj is the
*chemical difference of HSE activations*, not the complete screened impurity
Vscr=Hc[Dc]−Hh[Dh]. No PBE centroid or inverse-eta response is added to aj.
Direct Fock actions on Φ are retained; ACE off-span actions are not substituted.

Traces and the Q-action norm are invariant under scalar energy-reference changes
and unitary rotations within the two fixed sectors. Physical changes of the
projectors are different. For another pair P'a, the trace change is bounded by

    [||P6−P'6||1/2 + ||P8−P'8||1/4] ||A−cI||.

This needs an operator bound and physical frame comparison. Original e90 k4/q4
cold-smearing host frames do not automatically supply the e50 Γ/q1 FD frame or
state. Their measured high-G tails and earlier transfer/refusal results remain.

## 2. A scalar-looking compression need not be a closed operator

**PROVEN:** for Hermitian C and any Hermitian closed-P approximation B with
QBP=0,

    ||(C−B)P|| >= ||QCP||.

Apply Q to the difference. Equality for the full operator norm is attained by
B=PCP+QCQ: the remaining off-diagonal Hermitian block has norm||QCP||.
The six action columns identify QCP without knowing QCQ. This is a sharp
lower bound on a CLOSED-SPACE OPERATOR approximation, not on tr(WC).

**CALCULATED:** at j=1 the retained C1 has||QCP||=95.541080meV and smallest
leakage singular value91.550099meV. Hence even its weakest unit trial direction
in P has substantial out-of-space action. The nearly scalar compression
(scalar-free norm0.214856meV) and positive sector Rayleigh interval do not
justify a six-state-only chemical Hamiltonian. These numbers are finite-array
calculations; no directed-rounding enclosure is claimed. Independent QR and
compensated scalar contractions agree to much better than1e-9meV.
This does not falsify a six-/eight-band effective Kane theory that retains
the eliminated-sector self-energy; its properly qualified kernel is extra
microscopic information, not the measured trace alone.

Full H, not C alone, enters the Schur term B†(z−QHQ)^−1B. On Im z=eta>0,
its norm is at most||B||²/eta for Hermitian QHQ. On the real axis a bound
||B||²/d requires an independently proved distance d>0 to the complement.
Neither B=QHP nor that isolation is supplied by a chemical-activation action.
Changing QCQ while preserving all measured P columns changes the Schur term;
nearby complement eigenvalues can arbitrarily enhance it. No gap, pole eligibility
or random-alloy mass is inferred from the95.54meV number.

## 3. A sharp, lower-information chemical-sign certificate

For any Hermitian unmeasured remainder E in the FIXED P compression,

    |tr(W E)| <= ||W||1 ||PEP|| = 2 ||PEP||.

The constant2 is optimal: E=−epsilon P6+epsilon P8 gives −2epsilon. Thus the
positive a1=39.811503589meV survives whenever||PEP||<19.905751794meV.
At equality the same extremizer erases it. This is a decision threshold, **not
a material or numerical remainder estimate**. It does not constrain QEQ.

Less information is sufficient than a whole-H norm: separate sector errors
epsilon6,m/epsilon8,m give chemical-trace error at most

    epsilon6,c + epsilon8,c + epsilon6,h + epsilon8,h.

Only the screened remainder's four normalized trace errors are necessary for
this sign test. Whole1e-8 FD/symmetry gates remain separate state-qualification
requirements; they are not converted to meV without a density-to-H bound.

For a fixed discretized symmetric screened exchange kernel, the Fock map X is
linear and self-adjoint in the real Hilbert-Schmidt pairing. Consequently

    tr(W X[deltaD]) = tr(X[W] deltaD).

This follows by swapping the kernel's two coordinates and spin indices. The
exchange part of the required remainder is one dual density contraction, not
an entire bandstructure. Hartree is also linear; local XC generally is not.
Its remaining part requires the actual potential difference or a bounded
directional derivative along the density path. This established Fock identity
does not determine deltaD, local screening or nonlinear Cd response from the
existing states. Nonlocal density, not local spin/charge alone, is essential.

## 4. Why one more scalar update cannot bound the limit

Let delta_m=a_m,1−a_m,0. If an INDEPENDENT uniform certificate bounds all future
observable increments by q^j|delta_m|, 0<=q<1, their summed tail is at most
q|delta_m|/(1−q). Applying this to the chemical increment gives the sufficient
sign threshold q<0.90103694. Applying it separately to both members, with the
measured |delta_h|+|delta_c|=37.870176706meV, instead gives q<0.51249540.
The first assumption is stronger than small member increments: it requires
continued host/Cd cancellation. Neither certificate is available. Even a true
scalar certificate would concern that specified sequence/activation, not cure
TR or establish a material mass. A changed, repaired iteration cannot inherit
an old sequence's increment bound without a separate proof.

Two values do not bound future increments: a smooth continuation can match
both and then acquire any chosen increment, e.g. adding lambda*t*(t−1) leaves
values at t=0,1 fixed but changes t=2 arbitrarily. This is an information
counterexample, not a realizability claim for this specified HSE functional.
Even a finite observed decreasing
sequence is not a uniform Jacobian or tail bound. The later severe host symmetry
failure additionally prevents using that old trajectory as the intended
nonmagnetic continuation. Its existence is not a theorem excluding all other
legitimate HSE algorithms or numerical states. The fully specified finite
HSE problem is in principle computable; the missing information is the actual
qualified state/response or a justified remainder certificate, not intrinsic
indeterminacy of an already fully specified Hamiltonian.

For a complete specified exact-HSE fixed-point map F, independent q<1 and
residual r would yield ||D−D*||<=r/(1−q), then an observable derivative bound
could propagate it. The native176-source ACE iteration also depends on its
empty-state interpolation span: identical occupied D can have different ACE
off-span completions. A local-rho or scalar-dexx convergence ratio alone does
not define or certify that full map. Existing direct-on-source agreement is
therefore insufficient, as expected from established ACE theory.

## 5. Actual density counterqualification

With native columns U and occupations f, D=U diag(f)U†. Θ maps G→−G and
(up,down)→(down*,−up*). For any normalized v,

    ||D−ΘDΘ^−1|| >= |sum_j f_j (|<Uj,v>|²−|<ΘUj,v>|²)|.

The independent check evaluates this scalar directly on native columns;
charge, FD occupations and old scalar acquisition gates remain correct.
Host second-state witness0.001395756895 already rules out the strict1e-8
nonmagnetic claim without any assumption of a Θ-closed reference. Native24Td
operations, a tiny quartet energy spread or zero LOCAL spin cannot replace
this nonlocal test. No occupations are averaged, and no old result is failed
retroactively under a gate it did not claim to meet.
The defect diagnoses these numerical trial/source states, not a magnetic
material ground state or a proof of which approximation caused the failure.
