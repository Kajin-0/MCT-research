# R06 sign, terminal-current, Fourier, and PSD conventions

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** Phase 1A project convention; implementation is not yet authorized

## 1. Purpose

This document fixes the algebraic and spectral conventions that every later deterministic, linearized, and stochastic implementation must use. It does not by itself establish physical closure. Contact kinetics, trap kinetics, and primitive source covariances remain subject to the source audit.

The convention is selected to make all conservation checks executable and to prevent factor-of-two or sign changes from being hidden in code.

## 2. Geometry, charge, and field

The one-dimensional detector occupies

\[
0\le x\le L
\]

with constant cross-sectional area \(A\). The positive coordinate direction is from the left terminal to the right terminal.

Use:

- \(q>0\) for the elementary charge magnitude;
- electron charge \(-q\);
- hole charge \(+q\);
- electrostatic potential \(\phi\);
- electric field
  \[
  E=-\partial_x\phi;
  \]
- positive conventional current in the \(+x\) direction;
- positive particle flux in the \(+x\) direction.

The total charge density is

\[
\rho=q\left(p-n+N_D^+-N_A^-\right)+\rho_t+\rho_{\mathrm{fixed}}.
\]

Poisson's equation is

\[
\partial_x\!\left(\varepsilon\partial_x\phi\right)=-\rho.
\]

For constant \(\varepsilon\),

\[
\partial_x E=\frac{\rho}{\varepsilon}.
\]

Any implementation using the opposite voltage or Fourier convention must translate at the interface and must not change these internal definitions.

## 3. Particle flux and conventional current

The electron and hole particle fluxes are

\[
\Gamma_n=-\mu_n nE-D_n\partial_xn,
\]

\[
\Gamma_p=+\mu_p pE-D_p\partial_xp.
\]

The corresponding conventional current densities are

\[
J_n=-q\Gamma_n
    =q\mu_n nE+qD_n\partial_xn,
\]

\[
J_p=+q\Gamma_p
    =q\mu_p pE-qD_p\partial_xp.
\]

For net pair generation \(G\) and net pair recombination \(R\),

\[
\partial_t n=-\partial_x\Gamma_n+G-R
            =\frac{1}{q}\partial_xJ_n+G-R,
\]

\[
\partial_t p=-\partial_x\Gamma_p+G-R
            =-\frac{1}{q}\partial_xJ_p+G-R.
\]

A positive \(G-R\) therefore increases both \(n\) and \(p\). Internal pair generation or recombination does not create net charge.

When trap occupancy is dynamic, its charge-state equation must be included in the total charge balance. An algebraic trapped-charge term may be used only after a controlled elimination that preserves the relevant fluctuation spectrum.

## 4. Applied voltage and electrostatic boundary condition

Define the terminal voltage as

\[
V(t)=\phi(0,t)-\phi(L,t)
    =\int_0^L E(x,t)\,dx.
\]

The baseline voltage-driven gauge is

\[
\phi(0,t)=0,
\qquad
\phi(L,t)=-V(t).
\]

Thus a positive uniform field gives \(V=EL>0\).

The mean operating point may impose \(V(t)=V_b\). The small-signal boundary depends on the terminal circuit:

- ideal voltage bias: \(\delta V=0\), solve for \(\delta I\);
- ideal current bias: \(\delta I=0\), solve for \(\delta V\);
- finite external impedance: solve the device and circuit equations together.

Equilibrium Johnson-Nyquist verification must use a boundary condition under which the tested observable is not identically clamped.

## 5. Conserved terminal current

Define the conduction current density

\[
J_c=J_n+J_p.
\]

If charge conservation is closed,

\[
\partial_t\rho+\partial_xJ_c=0.
\]

Combining this equation with Poisson's equation gives

\[
\partial_x\!\left[J_c+\partial_t(\varepsilon E)\right]=0.
\]

The local total current density is therefore

\[
J_{\mathrm{tot}}(x,t)
=J_n+J_p+\partial_t(\varepsilon E).
\]

For a static, constant permittivity,

\[
J_{\mathrm{tot}}=J_n+J_p+\varepsilon\partial_tE.
\]

The terminal current is

\[
I(t)=A\,J_{\mathrm{tot}}(x,t),
\]

and must be independent of \(x\) within the stated numerical tolerance.

For constant \(A\) and \(\varepsilon\), spatial averaging gives the equivalent expression

\[
I(t)
=
\frac{A}{L}\int_0^L\left(J_n+J_p\right)\,dx
+
\frac{\varepsilon A}{L}\frac{dV}{dt}.
\]

Consequences:

1. Under ideal fixed voltage, \(dV/dt=0\), but the terminal current is the **spatial average** of conduction current, not generally the conduction current at an arbitrary point.
2. Local displacement current remains necessary to make \(J_{\mathrm{tot}}(x,t)\) position independent.
3. If \(\varepsilon\) is dispersive or lossy, the electric displacement \(D\), not a constant-\(\varepsilon\) approximation, must be used and the corresponding polarization fluctuations must be treated consistently.
4. A numerical result that reports pointwise \(J_n+J_p\) as the finite-frequency terminal current without an error criterion is rejected.

The finite-size analytical treatment of Gomila and Reggiani explicitly uses conduction plus displacement current and a spatial terminal-current construction, making it a required benchmark for this definition (DOI: `10.1063/1.1526915`).

## 6. Contact orientation and deterministic boundary form

Let the outward unit normal be

\[
\nu(0)=-1,
\qquad
\nu(L)=+1.
\]

Writing carrier boundaries in terms of outward particle flux avoids hidden left/right sign changes.

A provisional finite-rate boundary is

\[
\nu\Gamma_n=S_n\left(n-n_{n,\mathrm{eq}}\right),
\]

\[
\nu\Gamma_p=S_p\left(p-p_{p,\mathrm{eq}}\right).
\]

The limiting cases are:

- blocking contact: \(S_n=S_p=0\);
- ideal reservoir or infinitely fast surface relaxation: the appropriate contact-equilibrium electrochemical potentials or carrier populations are imposed;
- asymmetric contact: left and right equilibrium populations and rate parameters are independent inputs.

This Robin form is only a deterministic mean boundary. A stochastic finite-rate contact must be decomposed into forward and reverse injection/extraction events satisfying equilibrium detailed balance. The fluctuation intensity depends on the **sum** of forward and reverse event rates, not their net difference.

The 2022 finite-surface-recombination treatment by Park establishes that finite contact velocity affects finite-sample GR spectra, but its microscopic stochastic contact closure remains an explicit full-text audit item (DOI: `10.1063/5.0111954`).

## 7. Fourier transform

Use the complex Fourier pair

\[
X(\omega)=\int_{-\infty}^{\infty}x(t)e^{-i\omega t}\,dt,
\]

\[
x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}
X(\omega)e^{i\omega t}\,d\omega.
\]

Therefore,

\[
\partial_t x \longrightarrow i\omega X.
\]

The linearized residual must be written in one fixed form. R06 uses

\[
M\dot u=F(u)+B\xi.
\]

At a steady state \(u_0\), with

\[
J=\left.\frac{\partial F}{\partial u}\right|_{u_0},
\]

the frequency-domain perturbation equation is

\[
(i\omega M-J)\,\delta\hat u=B\hat\xi.
\]

If an implementation stores the deterministic residual as \(M\dot u+R(u)=0\), then \(J=-\partial R/\partial u\). Tests must verify equivalence rather than silently switching signs.

## 8. Two-sided angular-frequency PSD

For zero-mean, jointly stationary processes,

\[
C_{xy}(\tau)
=
\left\langle x(t+\tau)y^*(t)\right\rangle.
\]

Define the two-sided angular-frequency cross-PSD by

\[
S_{xy,\omega}^{(2)}(\omega)
=
\int_{-\infty}^{\infty}
C_{xy}(\tau)e^{-i\omega\tau}\,d\tau.
\]

Then

\[
C_{xy}(0)
=
\frac{1}{2\pi}
\int_{-\infty}^{\infty}
S_{xy,\omega}^{(2)}(\omega)\,d\omega.
\]

For a real scalar process,

\[
S_{xx,\omega}^{(2)}(-\omega)
=
S_{xx,\omega}^{(2)}(\omega).
\]

The one-sided angular PSD is

\[
S_{xx,\omega}^{(1)}(\omega)
=
2S_{xx,\omega}^{(2)}(\omega),
\qquad
\omega>0,
\]

so that

\[
\left\langle x^2\right\rangle
=
\frac{1}{2\pi}
\int_0^\infty
S_{xx,\omega}^{(1)}(\omega)\,d\omega.
\]

## 9. Hertz-domain PSD

Define the two-sided hertz-domain PSD as

\[
S_{xy,f}^{(2)}(f)
=
\int_{-\infty}^{\infty}
C_{xy}(\tau)e^{-i2\pi f\tau}\,d\tau.
\]

Under the definitions above,

\[
S_{xy,f}^{(2)}(f)
=
S_{xy,\omega}^{(2)}(2\pi f).
\]

There is no numerical \(2\pi\) multiplier in this particular PSD definition; the \(2\pi\) appears in the argument and in the angular-frequency variance integral. Other software conventions sometimes absorb \(1/(2\pi)\) into the angular PSD. Such outputs must be converted explicitly.

For \(f>0\),

\[
S_{xx,f}^{(1)}(f)
=
2S_{xx,f}^{(2)}(f),
\]

and

\[
\left\langle x^2\right\rangle
=
\int_0^\infty
S_{xx,f}^{(1)}(f)\,df.
\]

All publication figures will report one-sided PSD per hertz unless a figure explicitly states otherwise.

## 10. Transfer functions and matrix PSD

Let the terminal fluctuation be

\[
\delta\hat I
=
c^T\delta\hat u+d^T\hat\xi.
\]

Then

\[
H_I(\omega)
=
c^T(i\omega M-J)^{-1}B+d^T,
\]

and

\[
S_{I,\omega}^{(2)}(\omega)
=
H_I(\omega)
Q_{\xi,\omega}^{(2)}(\omega)
H_I^\dagger(\omega).
\]

For multiple terminal outputs,

\[
S_{y,\omega}^{(2)}
=
H_yQ_\xi H_y^\dagger
\]

is a Hermitian positive-semidefinite matrix. Numerical code must test Hermiticity and the smallest eigenvalue to a tolerance tied to solver error.

## 11. Equilibrium fluctuation-dissipation convention

In the classical regime and at thermal equilibrium, use:

### One-sided, per hertz

\[
S_V^{(1)}(f)
=
4k_BT\,\operatorname{Re}Z(2\pi f),
\]

\[
S_I^{(1)}(f)
=
4k_BT\,\operatorname{Re}Y(2\pi f).
\]

For a frequency-independent resistor,

\[
S_V^{(1)}=4k_BTR,
\qquad
S_I^{(1)}=\frac{4k_BT}{R}.
\]

### Two-sided, per hertz

\[
S_V^{(2)}(f)
=
2k_BT\,\operatorname{Re}Z(2\pi f),
\]

\[
S_I^{(2)}(f)
=
2k_BT\,\operatorname{Re}Y(2\pi f).
\]

### Two-sided angular convention used internally

\[
S_{V,\omega}^{(2)}(\omega)
=
2k_BT\,\operatorname{Re}Z(\omega),
\]

\[
S_{I,\omega}^{(2)}(\omega)
=
2k_BT\,\operatorname{Re}Y(\omega).
\]

These are convention translations of the Johnson-Nyquist equilibrium result, not new theory. The foundational sources are Johnson, DOI `10.1103/PhysRev.32.97`, and Nyquist, DOI `10.1103/PhysRev.32.110`.

The classical approximation must be checked by \(hf\ll k_BT\). A quantum fluctuation-dissipation form is outside the baseline scope unless frequencies approach the thermal frequency scale.

## 12. Required convention tests

Before Phase 2 or Phase 3 is accepted, automated tests must verify:

| Test | Required result |
|---|---|
| Uniform field | \(V=EL\) with the selected voltage sign |
| Electron drift | Positive \(E\) gives positive conventional \(J_n\) |
| Hole drift | Positive \(E\) gives positive conventional \(J_p\) |
| Pair generation | Positive \(G-R\) increases both \(n\) and \(p\) |
| Integrated continuity | Volume-rate change equals net boundary flux plus volume source |
| Total-current conservation | \(\max_x|J_{\mathrm{tot}}(x)-\bar J_{\mathrm{tot}}|/J_{\mathrm{scale}}\) below tolerance |
| Fixed-voltage terminal current | Matches the spatial average of conduction current |
| Fourier derivative | Numerical sinusoid gives \(i\omega\) multiplier |
| PSD variance | Time-domain variance matches integrated one-sided PSD |
| One/two-sided conversion | Positive-frequency one-sided PSD equals twice the two-sided PSD |
| Hz/rad-s conversion | Variance is invariant under the declared mapping |
| Equilibrium FDT | Terminal PSD agrees with \(4k_BT\operatorname{Re}Z\) or \(4k_BT\operatorname{Re}Y\) in one-sided hertz form |

## 13. Status

The deterministic signs, terminal-current observable, Fourier transform, and PSD conversion are fixed by this document.

Still unresolved:

1. the microscopic contact event model;
2. whether transport noise is represented through primitive flux events or a verified equivalent-current formalism;
3. the exact trap state and charge convention;
4. external-circuit degrees of freedom required for each equilibrium test;
5. generalized Einstein and fluctuation relations under degenerate HgCdTe statistics.

No stochastic solver may be declared physically closed until these items and the source-covariance document agree.
