# HgCdTe impurity reference and threshold audit

Status: **PROVEN** identities and conditional threshold theorem; **CALCULATED**
binary-derived diagnostics; **HYPOTHESIS** concerning the physical alloy.
No experimental alloy-gap coefficients enter the calculation.

## 1. Full versus residual impurity T

Let an averaged inverse Green function be written relative to a pure host,

\[
\bar G^{-1}(z,x)=z-H_H-\Sigma_H(z,x),\qquad
\Sigma_H=xT_H+o(x).
\]

Re-reference the same Green function to a coherent Hamiltonian
\(H_b(x)=H_H+x\Delta H\). This is an exact Dyson identity:

\[
\Sigma_b=\Sigma_H-x\Delta H,
\qquad \partial_x\Sigma_b|_0=T_H-\Delta H.
\]

At the other endpoint, with \(y=1-x\), the corresponding identity is
\(\partial_y\Sigma_b|_{y=0}=T_C+\Delta H\).
The full host-referenced T already contains the first-order coherent contrast.
It must not be added to a baseline containing that same contrast.

In the scalar common-mode mass convention, let the full projected endpoint
T values be \(\tau_H,\tau_C\), and \(\Delta M=M_C-M_H\). Then

\[
u_0=\mu'(0)=\tau_H,\qquad u_1=\mu'(1)=-\tau_C.
\]

The endpoint cubic is therefore

\[
\boxed{\mu_3=M_H+\Delta M x
 +\frac{\tau_H+\tau_C}{2}k
 +\frac{\tau_H-\tau_C-2\Delta M}{2}k(1-2x)},
\quad k=x(1-x).
\]

Equivalently, define **residual** endpoint shifts

\[
t_H=\tau_H-\Delta M,\qquad t_C=\tau_C+\Delta M.
\]

Then the handoff form is valid:

\[
\mu_3=M_H+\Delta M x+k[(1-x)t_H+xt_C].
\]

Its pair-reciprocity condition is \(t_H=t_C\), or in full-T notation
\(\tau_H-\tau_C=2\Delta M\). It is not \(\tau_H=\tau_C\).
For the affine first-order limit \(\tau_H=\Delta M\),
\(\tau_C=-\Delta M\), the corrected expression is exactly the binary chord.
Using the full T as a residual instead adds the spurious term
\(\Delta M k(1-2x)\), even in that limit.

These statements assume the scalar branch/common-mode reduction has already
been defined consistently. For an operator-valued VCA reference, subtract its
actual projected derivative, rather than replacing it by the gap chord slope.
The self-consistent HgTe continuation remains a separate physical question.

## 2. Embedded derivatives retain excursions outside the impurity

Let \(P\) restrict the lattice Hilbert space to the finite support of \(V\).
With \(G=(z-H_0)^{-1}\), the embedded host resolvent is
\(g=PGP^\dagger\). Exactly,

\[
g'=-PG^2P^\dagger,\qquad T'=Tg'T.
\]

Generally \(g'\ne-g^2\). The missing term is

\[
PG^2P^\dagger-g^2=PG(1-P^\dagger P)GP^\dagger.
\]

For real off-spectrum energy this is positive semidefinite. Squaring the
embedded resolvent discards propagation through the rest of the crystal and
underestimates the positive susceptibility in that Hermitian regime.
Independent tests compare the embedded Dyson solution with inversion of the
entire perturbed finite Hamiltonian, including a singular impurity potential.

## 3. Causal extension: the norm and energy derivative separate

For Hermitian, energy-independent \(V\), with \(z=E+i\eta\), \(\eta>0\),

\[
T-T^\dagger=T^\dagger(g-g^\dagger)T,
\]

and hence

\[
\boxed{-\frac{\operatorname{Im}T}{\eta}
 =T^\dagger P G^\dagger G P^\dagger T\succeq0.}
\]

This is the positive scattering-cloud norm at complex frequency. It is
generally **different** from \(-\operatorname{Re}T'\). Outside the spectrum,
their limits coincide as \(\eta\to0\). Inside a continuum, \(-\operatorname{Re}T'\)
need not be positive, while the norm can grow as \(1/\eta\) due to real on-shell
scattering. It cannot automatically be interpreted as a finite virtual-state
susceptibility or quasiparticle residue coefficient.

A one-level causal example is \(T=v+v^2/(z-v)\). At \(z=v+i\eta\),
\(\operatorname{Im}T<0\) but \(-\operatorname{Re}T'=-v^2/\eta^2<0\).
The numerical optical-theorem check is therefore separate from a derivative
sign check.

For the finite-support external vector \(a\), the local overlap also needs its
normalization: \(\tau=\sqrt{a^\dagger a}\sqrt S\cos\theta\),
\(S=\|Ta\|^2\), in the Hermitian case. A Bloch amplitude embedded on five
atoms is not a unit-normalized local vector. A global normalized Bloch-state
angle with a localized scattering cloud tends to zero with system volume;
that trivial volume scaling must not be described as physical state rotation.

## 4. A finite T does not imply a finite endpoint T prime

Assume a three-dimensional quadratic band extremum with a nonzero constant
coupling to the impurity channel. The weighted spectral density near the edge
is \(c\sqrt\epsilon\). On the gap side, at detuning \(\delta>0\),

\[
-T'\ \sim\ \int_0^\Lambda
 \frac{c\sqrt\epsilon\,d\epsilon}{(\epsilon+\delta)^2}
 =\frac{\pi c}{2\sqrt\delta}+O(1).
\]

Thus the off-continuum positivity theorem permits an unbounded positive
susceptibility. A finite mesh or finite \(\eta\) can conceal that divergence.
More generally, with dispersion \(\epsilon\sim q^z\) and coupling amplitude
\(T_{qa}\sim q^\ell\), the singular integral scales as
\(\delta^{(d+2\ell)/z-2}\). It converges at the edge only when
\(d+2\ell>2z\); equality produces a logarithm. In three dimensions a
quadratic channel with constant coupling is singular, whereas a linear Kane
channel or a symmetry-suppressed quadratic channel can be finite.

This is a conditional infrared theorem, not a declaration that the physical
HgCdTe gap has a fractional composition law. Channel selection, other bands,
bulk inversion asymmetry, self-consistency and linewidths must be checked.

### Exactly integrable concentration counterexample

For the normalized model density
\(\rho(\epsilon)=3\sqrt\epsilon/(2\Lambda^{3/2})\), \(0<\epsilon<\Lambda\),

\[
g(-\delta)=\frac3{\Lambda^{3/2}}
 [-\sqrt\Lambda+\sqrt\delta\arctan\sqrt{\Lambda/\delta}].
\]

For \(T=v/(1-vg)\), define \(t_0=v/(1+3v/\Lambda)\), away from a
threshold resonance. Then

\[
T(-\delta)=t_0+\frac{3\pi}{2\Lambda^{3/2}}t_0^2\sqrt\delta+O(\delta).
\]

For a weak attractive impurity with \(t_0<0\), the independent-impurity pole
equation \(E=xT(E)\) has

\[
\boxed{E=x t_0+
 \frac{3\pi t_0^2\sqrt{-t_0}}{2\Lambda^{3/2}}x^{3/2}+O(x^2).}
\]

The first endpoint slope exists, but the second derivative diverges. The
remaining term divided by \(x^2\), or by \(k^2\), is unbounded at that
endpoint. A two-sided Hermite identity can still be written inside the
interval; its **bounded smooth remainder** is not automatic. Pair-curvature
tomography and rational R33 closure require this regularity to be established.
The example is verified against direct quadrature and a bracketed pole solve.
It is not a self-consistent CPA calculation.

## Prior-art boundary

Dyson re-referencing, the T-matrix optical theorem, threshold singularities and
Hermite interpolation are established mathematics. No priority is claimed.
The primary scattering reference used in the audit is
[Spicka, Lipavsky and Morawetz, PRB 55, 5084 (1997)](https://www.k-morawetz.de/paper/prb1.pdf),
which explicitly distinguishes a host-referenced impurity T and the averaged
self-energy \(cT\). The significance here is correcting the particular HgCdTe
prediction protocol and testing it with a reconstructed lattice model.
