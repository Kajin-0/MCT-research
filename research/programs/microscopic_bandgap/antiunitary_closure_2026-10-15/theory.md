# Source completion and density symmetry are different requirements

PROVEN UNDER ASSUMPTIONS throughout: finite orthonormal spinor Hilbert space,
isometric antiunitary T with T²=-I, a fixed real screened two-point kernel and
norm-conserving spin-independent exchange convolution. No material stability or
novelty claim follows. The physical fixed-G implementation of T is audited.

## 1. Minimal completion, with a numerically stable constructor

The unique smallest invariant superspace containing S is S+TS. Its dimension is
n+rank[(I-P_S)TU], U an orthonormal basis of S. This is an exact rank statement.
Singular values of the DIRECT residual, not sqrt(1-sigma(U†TU)²), distinguish
small leakage from roundoff. Weyl's singular-value inequality gives the count
uncertainty if the residual perturbation is bounded; the recorded double-precision
checks are numerical evidence, not interval-arithmetic certification of exact rank.

A constructive invariant cover repeatedly adds q,Tq, where q is a normalized
residual of a source column after projection off the previous paired basis.
T²=-I gives <q,Tq>=0; invariance of the previous range makes both new vectors
orthogonal to it. The range stays inside S+TS in exact arithmetic. At most n
pairs suffice. The implementation reorthogonalizes and independently reports
source-cover, Gram and T-pair residuals. It is not claimed to minimize dimension
for a chosen approximate tolerance. A small residual in S alone is not enough:
the enlarged basis must also pass its own T-closure and Gram checks.

## 2. Exact obstruction to a density-preserving repair

Let D=Phi W Phi†, W positive real diagonal, and J(D)=TDT^-1. This J is a real
linear isometric involution on Hermitian operators. Its fixed-point projection
is Dbar=(D+J(D))/2. For any invariant Hermitian B,

    ||D-B|| >= ||D-J(D)||/2,
    ||D-Dbar|| = ||D-J(D)||/2.

The first follows by the triangle inequality and isometry. Thus this is the
exact operator-norm distance to invariant Hermitian matrices; Dbar attains it.
If 0<=D<=I, Dbar also has 0<=Dbar<=I and the same trace. It is a valid ensemble
density, but generally has different natural occupations. It is not necessarily
an idempotent zero-temperature state, f_beta of the old Hamiltonian, or an SCF
stationary point. A source-basis rotation preserving D cannot change this defect.
In an orthonormal source representation, rotations preserve D precisely when
they commute with W (including arbitrary rotations inside exactly equal-weight
blocks). Approximate energy degeneracy alone is not permission to average W.

For the native preliminary PBE data the certified numerical interval for this
distance is approximately2.599e-7; it is not zero. Later source8 needs a change
of approximately.499993. Neither is repaired by adding empty ACE columns.

The full finite-source defect is obtained on a reduced cover Q of Phi and TPhi,
not just the physical6frame. For B=Phi sqrt(W),

    ||BB†-P_Q BB†P_Q|| <= 2||B|| ||(I-P_Q)B||.

Apply this also to TB and sum, giving upper and lower defect bounds from the
compressed Hermitian matrix. Floating orthogonality allowances are explicitly
recorded; they are not physical/material errors or rigorous rounding intervals.

## 3. Source-exact compression and the missing actions

Let A=-V[D]>=0, C an orthonormal source, H=C†AC>0 and Y=AC. Then

    A_C=Y H^-1 Y† = A^(1/2) P_{A^(1/2)C} A^(1/2),
    A_C C=AC,  0<=A_C<=A.

If A commutes with T and range(C) is invariant, so does A_C, irrespective of
the basis chosen in C. If D is not invariant, the hypothesis on A is not supplied
by source completion. Conversely, if C is not invariant, even a symmetric A need
not yield symmetric ACE. Averaging an old nonclosed ACE generally loses its
direct source action. A positive176-dimensional H does not prove positivity or
conditioning of the enlarged H: the new direct actions are indispensable.

If ||(I-CC†)Phi||<=delta and ||A||<=a, source-action error obeys
|| (A-A_C)Phi ||<=a delta, since A-A_C vanishes on C and 0<=A-A_C<=A.
Its weighted exchange-energy error is at most .5 a ||W||_1 delta² (use the
quadratic residual, not the linear action bound). All comparisons require a
bound on A or a directly measured source action; closure alone supplies neither.

## 4. A legitimate NEW constrained ensemble protocol, not an old-run repair

For a real linear, trace-self-adjoint exchange map K, define E_x(D)=.5Tr D K(D).
If K commutes with J, K(Dbar)=.5[K(D)+K(JD)]. The new constrained functional
E_x(P_J D) has derivative K(Dbar) with respect to Hermitian D: P_J is self-adjoint
in real trace pairing and K(Dbar) is invariant. Thus an explicit constrained
ensemble calculation can use this operator without inventing occupations or
claiming equivalence to the refused old D. It must also treat local, entropy and
occupation equations consistently before claiming variational SCF convergence.

Native occupations below QE eps_occ=1e-8 can be omitted by its source bound.
The same deterministic occupation/source truncation must be used for D and JD;
linearity then concerns that actual truncated density. Physical trace/tail error
must be reported separately. Native trace energy must contract original source
occupations; auxiliary completion columns are not new electrons or occupied bands.

At fixed density and fixed cell, derivative in an ionic coordinate R is
.5Tr Dbar (partial_R K_R)(Dbar), plus the corresponding local/nonlocal ionic
terms. At stationary constrained states, envelope/Hellmann-Feynman conditions
are needed to drop state-response terms. An ACE projector derivative alone is
not this force. No force implementation or relaxed-ion equivalence is claimed;
the proposed fixed-ion operator experiment must refuse forces/stress.

## 5. Native qualification boundary

The352-column paired constructor is an auxiliary operator space, not a change
to176 solved bands. Native aceinit enforces nbndproj<=nbnd, so it must not be
silently reused with352. A fixed-source driver may apply unchanged direct vexx
in batches<=176 and reconstruct a new compression offline, independently testing
the enlarged Gram, source exactness, covariance and energy accounting. That
would qualify an operator constructor ONLY. It would neither supply a symmetric
SCF solution nor authorize returning to the broken8-source trajectory or Cd.

## Established literature / novelty boundary

ACE source interpolation, semidefinite ordering and adaptive compression are
established: [Lin (2016)](https://arxiv.org/abs/1601.07159),
[Lin and Lindsey (2017)](https://arxiv.org/abs/1703.05441). Their general accuracy
claims concern the method's stated convergence framework, not unconditional
symmetry of every truncated intermediate subspace. The pinned QE7.5 source
supplies the actual dimension, occupation and force restrictions; its
[input documentation](https://www.quantum-espresso.org/Doc/INPUT_PW.html)
describes domag=false/zero local magnetization for the nonmagnetic SOC setting.
The retained data prove why that local flag is insufficient here. Antiunitary
pairing and fixed-point projection are established mathematics. This application
and its numerical diagnostics have POTENTIAL NOVELTY — UNVERIFIED only.
