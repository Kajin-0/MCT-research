# Gap-free projected resolvent certificate from full-action residuals

PROVEN UNDER ASSUMPTIONS, finite HermitianH and Im(z)=eta>0. This is a
resolvent/Galerkin identity, not an exact alloy closure or priority claim.
Let V be an orthonormal query basis, A=V*HV, R=HV−VA, and original physical
P=VC+ΔP. Neither the complement spectrum nor a real-axis gap is required.
First set ΔP=0. With H0=A⊕QHQ and E=H−H0, two resolvent identities yield

    G−G0 = G0 E G0 + G0 E G E G0.

Projected first term vanishes: E is off-diagonal in V⊕Q. Put
Z=(z−A)^−1C and Zbar=(conj(z)−A)^−1C. Then

    g−gA = (R Zbar)* G (R Z),
    ||g−gA||op <= ||R Zbar||op ||R Z||op /eta.

This *second-order* bound can greatly improve the simple first-order
||P|| ||RZ||/eta, even if the total residual||R|| is large. We do not replace
residuals by auxiliary eigenvalues, assume a complement gap, require small
||R|| globally, or continue the formula to eta=0.

## Measured actions and a minimum independent error input

A uniform error bound on ALL of H is unnecessary. Let measured Y approximate
HV with a certified ||Y−HV||op<=epsilon, define measured A=(V*Y+Y*V)/2 and
measured R=Y−VA. Form H0=A⊕QHQ for the trueH. Its VV perturbation deltaA has
norm<=epsilon (up to an explicitly included measured anti-Hermitian residue).
The same identity, now retaining the first-order term, gives

    ||g−gA||op <= epsilon ||Zbar|| ||Z||
       + (||RZbar||+epsilon||Zbar||)
         (||RZ||+epsilon||Z||)/eta.

Here the epsilon means an operator norm for the WHOLE measured query matrix,
not an unaggregated per-column or per-element tolerance. If individual column
bounds are available, their Euclidean sum bounds epsilon. For imperfect
Hermiticity of V*Y, its measured anti-Hermitian norm is added to the allowance.
The query-frame contribution is bounded by

    (2||VC|| ||ΔP||+||ΔP||²)/eta.

Thus a coarse independently justified action certificate can suffice. We
report both the exact-action conditional model and the action-error capacity
needed to decide a sign. The example1e-6Ry allowance is an EXPLICIT ASSUMPTION,
not a proven interval enclosure of the native floating computation or material
Hamiltonian. Control-action agreement is not a proof for all query columns.
No physical/native numerical sign is promoted beyond those assumptions.

## Observable and denominator protection

For fixed original physical Γ6/Γ8 probes define gα=Tr(Pα*GPα)/dα,
aα=−Im(gα)/pi. This is a causal finite-resolution projected response. It is
neither intrinsic linewidth, sharp Γgap, absorption, topological mass nor a
common-mode quasiparticle pole. No new physical projector definition is fitted.
The inverse ordering K=Re[(z−1/g6)−(z−1/g8)] is allowed only after each gα has
an independently nonzero complex-disc margin. If |gα−gAα|<=deltaα<|gAα|,

    |1/gα−1/gAα| <= deltaα/[|gAα|(|gAα|−deltaα)].

Sum the two inverse errors for the ordering interval. If a denominator disc
contains zero, no inverse/sign is certified. Green/spectral bounds still hold.
All eta and errors are in matched units; 1Ry=13.605693122994eV here. Energy-zero
shift H->H+cI,z->z+c changes each Kα by c but leaves their difference invariant.
The μ used to select Re(z) is a finite304 reference, not a claimed fullspace μ.

## Independent FD nonstationarity test

For finite Galerkin FD F commuting with A, supported D=VFV*,
||[H,D]||op=||RF||op and ||[H,D]||F=sqrt(2)||RF||F. The slight in-space
floating commutator is subtracted for a conservative measured lower witness.
Combining with 2||H|| gives a conditional lower bound on distance to ANY
fullspaceFD fσ(H−μ), not merely the chosen μ. It remains above1e-8 here.
Cubic covariance and finite-space charge do not remove this obstruction.

## Falsification and missing information

Independent Hermitian baths with negative complement/near-poles verify the
second-order equality and bound. No eta->0, adjusted-μ, or material limit is
exchanged. Unknown action error, non-Hermitian retarded effectiveH, unfixed
projectors, or a zero denominator invalidate the corresponding certificate.
To sharpen small-eta response, the missing information is specifically the
residual response R(z−A)^−1P (or a certified complement selfenergy), not generic
more digits of sorted band energies. To release HSESCF/Cd the missing input is
instead a stationary full-H occupied solve and nonlinear same-state update.

## Physical probes outside the query space: moment shortcut refused

Original P has actual5.8135e-7operator leakage outsideV. The extra native6probe
controls measure HP; do not replace them by HV(V*P). Their difference1.3912e-5Ry
is small but nonzero. The first two original-frame moments P*HP and (HP)*HP are
measured by those controls. A claim of four closed exact moments is REFUSED.

For X=HP, write X=VC+e. Hermiticity makes both cross terms available fromHV:

    X*HX = C*AC + (HVC)*e + e*(HVC) + e*H e.

Only the last term is unknown and ||e*H e||<=M||e||². This squared leakage
bound, with the captured conservative M, is much smaller than incorrectly
propagating a whole vector H e at first order. The same identity bounds the
next physical block diagonal. These are finite-model/operator-bound statements;
action arithmetic and nonorthogonality allowances are separate, not hidden.
The third-moment unknown block allowance is1.2130e-7Ry³; fourth is not closed.
No high-energy block Rayleigh expectation is called a material band.

The resolvent proof also holds for self-adjoint unbounded H when the finite
columns ofV lie inD(H). Its off-diagonal block is bounded finite-rank; subtracting
it gives a self-adjoint block-diagonalH0, with the same1/eta bound. The bounded
commutator/||H|| FD witness above is only asserted in the finite plane-wave
model. Extending a numerical response certificate beyond that model would
also require action-error control for the omitted plane-wave output/functional
approximation; the native50Ry packets alone do not supply that input.

Artificial C=cI tests preserve the304basis actions A,R, not the12additional
physical control actions outsideV. They are a deliberately weaker falsification
family, not complete alternative native/HSEmodels. The initially tested13c
values and final18mathematically directed root cases all retained negative
ordering. This is a negative counterexample search, NOT a proof of uniqueness,
not proof that small-eta signs can change, and not an indistinguishability
theorem for the complete316query dataset. The universal residual bound itself
is valid after discarding extra information; no completion is used to tighten it.
