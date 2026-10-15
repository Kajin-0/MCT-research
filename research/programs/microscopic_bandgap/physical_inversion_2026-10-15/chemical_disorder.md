# Exact chemical/disorder accounting and the missing correlation

PROVEN UNDER ASSUMPTIONS: initially take bounded self-adjoint static H_omega in
one fixed physical Hilbert space and ensemble law mu_x; finite models suffice
for the counterexamples. Once self-consistency is solved, H_omega is held fixed
while z varies. Let

    Hbar = E_x H_omega, W_omega = H_omega-Hbar, E_x W=0,
    Gbar(z)=E_x (z-H_omega)^-1,
    Sigma_dis(z)=z-Hbar-Gbar(z)^-1.                       (A1)

Hbar is the mean of the actual configuration-dependent electronic operators,
not automatically H evaluated at an averaged charge/virtual atom. The lattice
and any background dependence must match. For an interacting problem a
configuration-dependent many-body self-energy must be included explicitly;
static HSE does not supply its material error or phonon zero-point correction.

## A1. Causal full-space split; reference changes

Embed constant configuration vectors J u(omega)=u in the direct-integral
Hamiltonian Hcal. Feshbach elimination of the orthogonal fluctuation space gives

    Sigma_dis = J* Hcal Q (z-Q Hcal Q)^-1 Q Hcal J.

Hence -Im Sigma_dis>=0 in the upper half-plane. Its high-frequency coefficient
is E(W^2), and Sigma_dis vanishes for a deterministic configuration operator.
This is established augmented-space/Dyson theory, derived here to fix the split.

An energy-independent Hermitian reference change Hbar->Hbar+B requires
Sigma->Sigma-B; Gbar is unchanged. Uniform energy shifts transform z and every
operator together. A configuration-dependent shift is NOT this gauge change.
Physical frames must rotate with their common embedding; same labels or
independently normalized band windows do not define that embedding.

The full host-referenced dilute expansion Sigma_H=x T_H+o(x) already contains
the coherent first-order substitution. Relative to H_H+x V its residual is
x(T_H-V)+o(x). Adding xT_H to that baseline double counts V. This is the
existing full/residual-T correction, not a new scattering result. Thresholds
can invalidate smooth higher concentration derivatives; no endpoint Hermite
or reciprocal law is assumed here.

## A2. Project AFTER the split; a projected difference need not be causal

Let P be a fixed electronic projector, Q_e=I-P and S=Sigma_dis. The exact
projected inverse is obtained from the Schur complement of z-Hbar-S:

    D_P=z-Hbar_PP-S_PP
       -(Hbar_PQ+S_PQ)(z-Hbar_QQ-S_QQ)^-1(Hbar_QP+S_QP).  (A2)

The chemical projected baseline contains
K_ch=Hbar_PQ(z-Hbar_QQ)^-1 Hbar_QP. The additive difference from that baseline
is S_PP plus the last Schur term in (A2) minus K_ch. It is NOT generally just
P S P, and it is not generally a positive-measure/causal kernel by itself.
The total projected Green function is causal. Positivity applies to the full
augmented kernel, not an arbitrary difference of two Schur kernels.

Explicit counterexample: H_+/-=[[0,t+/-d],[t+/-d,a]] with equal probabilities,
mean Hbar=[[0,t],[t,a]], P=(1,0). Direct averaging gives

    K_total-K_ch = d^2/(z-a) [1+4t^2/(z(z-a)-t^2-d^2)].   (A3)

For t=1,d=1/4,a=2 and z=2+.01i, its imaginary part is POSITIVE although
-Im Sigma_dis and -Im K_total are nonnegative. Duplicate the two-state block
in a spinful Gamma6 copy space and add a Gamma8 spectator to preserve Td/TR.
This strengthens the earlier fixed-trial warning with an explicit exact-mean
counterexample; it does not invalidate the host-invariant reaction kernel.
If P reduces Hbar, K_ch=0 and the total augmented eliminated kernel is causal.

## A3. Independent scalar and mass variances are insufficient

In a declared six-state Kane vertex class write W=u_s I+u_m J,
J=diag(I2,-I4). Center both fields. Suppose they are real stationary scalar
fields with Fourier covariance C_ab(q), a,b=s,m. This covariance is a positive
2x2 matrix; symmetry permits its real cross part. At second Born order,

    Sigma^(2)=int_q [C_ss Gc+C_mm J Gc J
                         +C_sm Gc J+C_ms J Gc].         (A4)

For the Gamma6/8 normalized traces, J P_alpha=j_alpha P_alpha, j6=+1,j8=-1,
so the only covariance combinations in THIS two-vertex trace contraction are

    S_+(q)=C_ss+C_mm+2 Re C_sm,
    S_-(q)=C_ss+C_mm-2 Re C_sm.                          (A5)

They multiply the corresponding projected coherent propagator. Heavy-hole
states remain in Gc and its momentum integral. This is a restricted-class
quotient, not a universal two-parameter theorem for real orbital alloy vertices.
The independent-disorder specialization has S_+=S_-; it is an assumption, not
Td/TR symmetry. Reaching a mass-only target does not permit discarding the
scalar/mass cross-contraction.

An exact atomic counterexample needs no Born approximation. Let u=+/-1 with
equal probabilities, c=+/-a u, m=m0+b u, and H=c I+m J. Both correlation choices
have the same mean m0 J, scalar variance a^2 and mass variance b^2. At m0=0,

    Sigma6=(+/-a+b)^2/z, Sigma8=(+/-a-b)^2/z,
    Sigma_m=(Sigma6-Sigma8)/2=+/-2ab/z.                  (A6)

All models are static Hermitian, Td/TR-compatible and causal. Recentring EACH
realization by its own c makes its entire relative spectral data identical
between the choices, while the physically aligned averaged responses differ.
The missing joint covariance changes a signed mass-channel kernel, not merely
a linewidth. This does NOT prove a sharp random-alloy pole or a physical x_c.

For independent Bernoulli one-body substitution in this restricted vertex
class, C_sm(q)=x(1-x) v_s(q) v_m(q)*. One physical composite substitution vertex
therefore determines both diagonal and cross terms. Cation and induced-Te pieces
are not separately invariant. A complete microscopic configuration map also
fixes Hbar and every fluctuation channel; one must not fit an extra covariance
on top of already-counted effects. Irreducible pair/cluster channels require
their own established centered-cluster accounting, not a fictitious new kappa3
noise field. At higher scattering orders more information can be required.

The quotient(A5) assumes a specified coherent Gc at SECOND Born order. It
does not determine a self-consistent finite-k SCBA matrix: off-diagonal
propagation also involves C_ss-C_mm and, for general complex cross covariance,
its imaginary part. Changing these while holding S_+/- fixed can change the
self-consistent G fed into the Gamma integral. In particular A5 is not the
W_+/- notation of Krishtopenko2022 Eq16. No two-function universal SCBA closure
or new exact alloy reduction is claimed.

**Scientific consequence:** the independent scalar/mass SCBA closure cannot be
activated from separate fluctuation strengths or own-Fermi-relative spectra
alone. The minimum at this order is the two surviving S_+/- contractions (or
equivalent response functions), plus the mean and a truncation-error bound.
No new universal discovery of correlated disorder is claimed.
