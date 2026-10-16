# Antiunitary response reduction with an imperfect reference

## 1. Spinor convention and exact theorem

Use the original NC spinor Hilbert space, physical integer G labels and fixed
spin axes. At Gamma the sphere is closed under G→−G. Our convention is

    (Theta u)(G) = (u_down(−G)*, −u_up(−G)*).

Theta is antiunitary, Theta²=−I and Theta^-1=−Theta. Its global phase has no
effect on conjugation. For any Hermitian frozen response C define

    T(C)=Theta C Theta^-1,       C_even=(C+T(C))/2,
    C_odd=(C−T(C))/2.

**PROVEN:** T is a real-linear involution on Hermitian operators. C_even/odd
are Hermitian, sum to C and have parity T(C_even)=C_even, T(C_odd)=−C_odd.
For Hermitian W with T(W)=W, tr(WC) is real and tr(WC_odd)=0: antiunitary
conjugation complex-conjugates the trace, while Hermiticity makes it real.
This applies to W=P6/2−P8/4 only when BOTH sector projectors are Theta invariant.

Let V be an orthonormal six-column reference, Y=CV, J=V†Theta V. If Theta V=VJ
EXACTLY, J is unitary skew-symmetric, J J*=−I, and

    T(C)V = −Theta(Y) J* = Theta(Y) J†.

No assumption that C maps P into P is made. Thus exact Kramers closure would
make full even/odd six-column actions identifiable, including Q outputs.

## 2. The actual reference fails exact closure

**CALCULATED:** original reference sector residuals are1.26847e-7 (Gamma6) and
9.53824e-8 (Gamma8); full residual||R||=1.28639923e-7, where

    Theta V=VJ+R,       R=Q Theta V,       P=VV†, Q=I−P.

This exceeds the inherited1e-8 gate; it is not rounded to zero. Source/frame
normalization defects are ~1e-15. Positive-Gram coordinates are used only for
algebra, with original trace and normalization corrections recorded. No physical
frame/occupation/source is replaced. The same7809→10827 G embedding is retained.

Write A=V†Y and B=QY. Hermiticity identifies the cross block B†, but leaves
QCQ unknown. To avoid an arbitrary energy-reference dependence, put

    a=tr(A)/6,
    C_a = V A V† + B V† + V B† + a Q,
    C = C_a + Q Z Q,       Z=Q(C−aI)Q.

C_a is a DECLARED mathematical representative of the measured columns; it is
not a new physical operator. Under C→C+cI, a→a+c and C_a→C_a+cI. A zero-QQ
representative without this anchor would introduce spurious origin dependence.
Tiny measured anti-Hermitian compression noise (~3.2e-12meV) is separately
recorded when forming Hermitian algebra; no native input is edited or repaired.

The actual missing transformed action is exactly

    T(C)V = −Theta(C_a Theta V) − Theta(Z R).

If ||Z||<=M, each even/odd action differs from its known-column centre by at
most M||R||/2, including after Q projection. Weyl's singular-value inequality
therefore gives an interval of this radius for EACH singular value and the
operator norm. The even/odd uncertainties are correlated with opposite signs.
Their operator norms are not additive contributions to the total norm.

For the trace the ambiguity is much smaller:

    delta tr(W C_even/odd) = +/- tr(W6 R† Z R)/2,
    |delta trace| <= (M/2) ||R W6 R†||1,
    W6=diag(1/2,1/2,−1/4,−1/4,−1/4,−1/4).

The actual half nuclear-norm coefficient is1.15028439e-14; the action coefficient
is6.43199616e-8. These are respectively quadratic and linear in reference
closure error. This trace bound is sharp in the class of Hermitian bounded
QQ completions, choosing Z along the sign of R W6 R†.

**PROVEN information NO-GO:** without closure OR a completion bound, the six
columns do not uniquely determine either physical parity action or parity
trace. Adding lambda*u*u† for u in Q leaves CV unchanged. On the actual R,
a measured nonzero u†R W6 R†u permits arbitrary parity-trace change as lambda
varies. No claim that every such completion is realizable by this HSE functional
is made. The specified full functional/state is computable in principle.
Exact reconstruction requires C on the six residual directions R (or QZQR),
not a whole new spectrum. The trace alone needs only the relevant R† Z R
contraction. Neither missing action is silently set to zero.

## 3. Scope of C, symmetry and gauges

For m=host,Cd and source j=0,1, the measured action is

    A_mj = X_HSE[D_mj] + L_HSE[rho_mj] − L_PBE[rho_m0],
    C_j = A_Cd,j − A_host,j.

Native exchange occupation truncation is kept explicit: its linear map acts on
the source density actually used by Fock. Here weights below the native1e-8
cutoff have maximum<4.25e-53 (measured separately); the full occupation density
and exchange source are not silently identified in the general theorem.

It is the matched chemical HSE ACTIVATION, relative to each member's preliminary
PBE potential. Direct native Fock actions on the actual probes are used, never
off-span ACE replacements. Kinetic and fixed NC nonlocal/SOC cancel WITHIN each
activation. C is not total H_Cd[D_Cd]−H_host[D_host], a screened impurity mass,
or a spectral gap. Both old finite-acquisition PASS and later failures remain.

Block-unitary changes inside Gamma6/Gamma8 leave projectors, traces and Q
singular values invariant; the antiunitary sewing matrix transforms as
J→U†JU*. Scalar energy shifts cancel in tr W and Q action. The anchored
representative respects both gauges, and the norm certificate bounds the
centred operator C−aI. Independent checks use actual-data column formulas,
block-unitary/scalar gauges and a changed global Theta phase.

Local potential snapshots have exactly zero three magnetic components, so
their frozen scalar multiplication operators are Theta even. This is checked
on all retained members/stages. It does not certify the NONLOCAL density as
even, nor identify its diagonal with the stored mixed local density to arbitrary
precision. The source-conditioned kernel is real and inversion even; direct
Fock is linear/covariant. No group average of an old ACE is used.

## 4. Full finite-rank density defect

For native U,f, D=U diag(f)U† and D^T=(Theta U)diag(f)(Theta U)†. In a basis Q_s
covering BOTH sets, the Hermitian matrix

    K=(Q_s†U)diag(f)(U†Q_s)−(Q_s†Theta U)diag(f)((Theta U)†Q_s)

has all nonzero eigenvalues of D−D^T. Its eigenvalues and Frobenius norm give
the FULL operator/HS defects, not just a compressed lower witness. This352 is
an algebraic union, not new solved bands or the original16atom HSE target.
In floating
arithmetic, let weighted span residuals be e1,e2, Gram error g<1, and
b>=||U sqrt(f)||. Correct their sum by
[(1+g)g/(1−g)]*(||U sqrt(f)||F+||Theta U sqrt(f)||F), since the exact projector
is Q_s(Q_s†Q_s)^−1Q_s†. Twice b times that corrected sum bounds omitted
density. Add [g/(1−g)]*||K|| in the norm being reported for positive-Gram
normalization of K. Separate operator/Frobenius allowances are recorded.
Frobenius residuals control either omitted norm; no cancellation of O(144) traces
is used to infer a1e-7 defect. Original columns/occupations are never changed.
The interval formulas are analytic; numerical evaluations are not directed-
rounding enclosures. An independent normalized-vector expectation verifies the
largest absolute defect. The earlier lower witnesses are preserved, not replaced.

## 5. What even projection cannot repair

The pair (C_even,C_odd) is a decomposition of a FROZEN response. In general

    [H[D]+H[Theta D Theta^-1]]/2 != H[(D+Theta D Theta^-1)/2].

Direct Fock and Hartree are linear; nonlinear local XC prevents asserting this
identity generally. A special exception is possible if the local density is
already Theta invariant, the stored rho is exactly the diagonal of D, and the
functional depends only on those unchanged local arguments: then the frozen
operator identity can hold despite nonlinear XC. Zero local spin alone does
not supply all these consistency conditions. Even in that exception D_even
has not been shown to equal f_sigma(H[D_even]−mu), to minimize a free energy,
or to solve the native eigenstate/charge problem. C is moreover a difference
of responses from multiple densities, not one self-consistent H[D_even].

To turn the source-odd defect into an EVEN-response error bound, let D=D_e+D_o
and assume a twice differentiable covariant H on the whole connecting segment.
If sup||H''||<=L2 in specified density/operator norms, then

    ||P_even H[D]−H[D_e]|| <= (L2/2)||D_o||².

The linear term cancels between D_e+D_o and D_e−D_o. Multiplication by||W||1=2
bounds the associated trace. Local-XC/near-vacuum differentiability and L2 are
not certified here. Linear direct-Fock odd response has a finite-grid bound,
but that is not a bound on nonlinear even screening or stationary-state error.

For an SCF solution additionally require an independently controlled inverse
of I−J_F (appropriate even-sector FD response/Jacobian, with charge constraint),
nonlinear remainder/stability and occupied full-H/complement residuals. Those
inputs are absent. A large even frozen response can include INDIRECT bias from
a broken/nonstationary trajectory. No trace immunity to the EXPLICIT C_odd
implies immunity to such feedback, a sharp pole, material inversion or x_c.
