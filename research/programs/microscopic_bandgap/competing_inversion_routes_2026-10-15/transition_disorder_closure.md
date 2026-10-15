# Minimal predictive closure for the no-atom optical route

## Exact chemical mean and a different quotient of disorder

Retain the previous exact split H_omega(B)=Hbar(B)+W_omega(B), E W=0,
after each specified physical electronic state is solved. Hbar is NOT
H[E density]. Full impurityT contains the first coherent substitution; relative
to an already shifted mean subtract that part. Projection of the averaged
Dyson equation uses its full Schur complement. Do not add PBE response and
fixed-D HSE activation as independent gap coefficients.

For optical prediction the exact positive transition measure is

    S_J(B,domega)=E sum_{a occupied,b empty}
          |<b|J(B)|a>|^2 delta_(Eb-Ea)(domega).             (L1)

Finite temperature uses the corresponding occupation factors. The retarded
Kubo response includes the positive/negative frequency pair and known optical
prefactors. S is not the DOS or a product of averaged single-particle spectra.
The full disorder law and state determine it, but one-particle Sigma alone
generally does not: optical vertex correlations are additional information.

At a finite matrix level define the self-adjoint Liouvillian on Hilbert–Schmidt
operator space, L_omega A=[H_omega,A]. Its resolvent spectral matrix elements
with a declared transition source A=Pe J Po encode(L1) when occupied/empty
subspaces and normalization are fixed/qualified. It is causal as a Stieltjes
transform. Changing a common energy zero, even by configuration-dependent
C_omega I, leaves L_omega EXACTLY unchanged. With fixed particle number the
occupations are unchanged as well. This is the origin of routeB's exact
common-mode cancellation, not a cancellation available to a single-particle
resolvent in general.

Consequently the disorder that matters is the **commutator-active** operator
L_W=[W,.], not an arbitrary separate scalar strength. Spatial scalar W(r)
can remain active, because it need not commute with kinetic/current states.
The quotient by C I is exact for this finite canonical model; it is not a
claim that every alloy's charge-transfer field is harmless. Current operators,
occupations, position ordering and optical form factors must still be supplied.

## A controlled weak-contrast candidate

Suppose finite-dimensional Lbar is self-adjoint, E L_W=0 and
||L_W||<=w_L. The crude w_L<=2||W|| is sufficient, but can be very wasteful:
for arbitrary random C I one has w_L=0 even when one-particle atoms disappear.
At z=omega+i eta, eta>0, set R0=(z-Lbar)^-1 and r=w_L/eta<1. The same
uniform resolvent expansion used previously gives a rigorous quadratic closure

    B_L=E[L_W R0 L_W],
    R_B=(z-Lbar-B_L)^-1,
    ||E R_L-R_B|| <= eta^-1
           [r^3/(1-r)+r^4/(1-r^2)].                     (L2)

For a normalized fixed source this bounds its spectral-transform error; for
source norm A0 multiply by A0^2. The quadratic series proof is independent of
SCBA: its remainder starts at r^3 after centering, and the Dyson resummation
adds at most r^4/(1-r^2). It is not an all-strength exact effective medium.

If actual transition source A_omega differs from the fixed one by HS norm<=eA,
the extra transform error is <=(2||A0|| eA+eA^2)/eta. Occupation changes and
current/source errors therefore require a real certificate, not a fixed-source
assumption disguised as a material fact. The bound is finite-resolution; it
does not justify eta->0 with fixed w_L or an unbounded continuum operator
without the corresponding domain/control proof.

For a finite frequency window I the transform error eR bounds the resolved
spectral-mass error by |I| eR/pi and its centered first-moment error by
eR/pi integral_I |omega-E*|domega (with source norm factors included). This
is a bounded finite-window forward prediction. Resolvent/Lorentz smoothing
does not have a finite absolute first tail moment on the whole line, so L2
alone must NOT be inserted as a certificate for B3's full centroid. A declared
finite-window line adapter, deconvolution/error or a finite-moment physical
resolution kernel is still required. No concealed eta->0 step is used.

For a scalar/mass vertex W=u_s I+u_m J at orbital level, the FULL finite-q
covariance tensor gives the appropriate Liouvillian contraction; spatial
scalar, common/mass cross and orbital/directional pair contributions must all
be retained. The old two S_+/- combinations suffice only for fixed-Gc diagonal
one-particle Born traces. They do not close this two-particle kernel or a
self-consistent finite-k SCBA matrix. A2's pair s-p term lies outside I,J
entirely. Once the full microscopic operators/statistical law are supplied,
mean, covariance and higher clusters are linked, not independent fit parameters.

## Exact counterexample: identical one-particle Green functions, different optics

Consider a two-orbital cell at canonical one-electron filling, J=sigma_x,
and two ensembles with equal probabilities:

    A: H=diag(a,-a) or diag(-a,a),
    B: H=diag(a,a) or diag(-a,-a),  a>0.

In BOTH ensembles the two diagonal averaged single-particle functions equal
z/(z^2-a^2), and off-diagonals vanish. Their aligned mean operators also
coincide. In A the ground-to-excited transition is2a with nonzero current.
In B H commutes with J: there is no finite-frequency absorption. Ground-state
degeneracy can be assigned a canonical mixed state; the zero commutator is
independent of that choice. Add the SAME independent continuous scalar C I
to both ensembles: all one-particle spectral measures become continuous while
remaining identical between A and B, and the optical distinction survives.

This proves that even exact sector Green functions cannot alone identify a
physical magneto-optical criterion in the general class. The missing joint
information is response/vertex correlation, not another derivative of an
already known scalar self-energy. The example is a deliberately simple causal
finite operator model, not literal zincblende optics. Its principle is standard
Kubo/vertex physics, independently derived/tested here, and not claimed novel.

## Practical disposition

This closure permits a bounded forward optical prediction from an independently
qualified mean + transition-source + commutator-disorder law/error, without
requiring a single-particle atom or a common gap. Its common-mode quotient
can reduce the information burden. Present PBE/H304 Gamma data do not provide
finite-B currents, transition sources or this covariance. Thus it is a
conditional candidate with falsification criteria, not an activated HgCdTe
model. A measured three-field response can test the Kane reduction; it cannot
replace the missing nonempirical microscopic inputs by fitting a bowing law.
