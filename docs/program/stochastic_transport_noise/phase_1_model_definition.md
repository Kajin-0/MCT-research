# R06 Phase 1 model definition

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #339  
**Status:** Phase 1 working specification; not a validated theory

## 1. Decision to be made

Phase 1 must determine whether a finite one-dimensional HgCdTe photoconductor admits a physically closed, fluctuation-dissipation-consistent stochastic drift-diffusion-Poisson formulation that can predict the externally measured terminal-current or terminal-voltage spectrum and expose controlled departures from a lumped generation-recombination model.

A positive Phase 1 decision requires all of the following:

1. deterministic conservation laws and signs are internally consistent;
2. contact and terminal boundary conditions are explicit;
3. the stochastic source representation has a derivable covariance;
4. equilibrium Johnson-Nyquist noise can be used as a non-negotiable verification target;
5. independent dimensionless control parameters are identified;
6. literature review supports a defensible prior-art boundary;
7. uncertain HgCdTe parameters can be represented as ranges without destroying falsifiability.

## 2. Geometry and terminal definition

The baseline detector occupies

\[
0 \le x \le L
\]

with constant cross-sectional area \(A\). The transport coordinate points from the left terminal to the right terminal. The externally imposed voltage is provisionally defined as

\[
V_b = \phi(0)-\phi(L),
\]

so a positive \(V_b\) produces a positive uniform electric field \(E=V_b/L\) when space charge is absent.

The final terminal observable must be selected from one of three explicitly modeled circuits:

1. ideal voltage bias, with terminal-current fluctuations measured;
2. ideal current bias, with terminal-voltage fluctuations measured;
3. finite external impedance, with loaded current and voltage fluctuations.

The ideal voltage-biased problem is the initial target, but the equilibrium Johnson-Nyquist test may require explicit inclusion of the external load or a Thevenin/Norton equivalent to avoid imposing a boundary condition that suppresses the fluctuating observable.

## 3. Deterministic state variables

The minimum state is

\[
u(x,t)=\{n,p,\phi\}.
\]

Depending on the literature and thermodynamic closure, the state may need to be enlarged to include:

- trap occupancy \(f_t\) or trapped charge \(\rho_t\);
- contact interfacial populations;
- lattice or carrier temperature for non-isothermal extensions;
- external-circuit charge or voltage.

Trap charge must not be included algebraically in Poisson's equation while its fluctuating occupancy is omitted from the stochastic dynamics unless a controlled adiabatic-elimination argument is given.

## 4. Sign convention

Use:

- \(q>0\): elementary charge magnitude;
- electron charge \(-q\);
- hole charge \(+q\);
- \(E=-\partial_x\phi\);
- positive conventional current in the \(+x\) direction;
- positive particle flux in the \(+x\) direction.

Electron and hole particle fluxes are

\[
\Gamma_n=-\mu_n n E-D_n\partial_x n,
\]

\[
\Gamma_p=+\mu_p p E-D_p\partial_x p.
\]

The corresponding conventional current densities are

\[
J_n=-q\Gamma_n=q\mu_n nE+qD_n\partial_x n,
\]

\[
J_p=+q\Gamma_p=q\mu_p pE-qD_p\partial_x p.
\]

For a net pair-generation rate \(G\) and net pair-recombination rate \(R\), both measured in \(\mathrm{m^{-3}s^{-1}}\), carrier conservation gives

\[
\partial_t n=-\partial_x\Gamma_n+G-R
=\frac{1}{q}\partial_xJ_n+G-R,
\]

\[
\partial_t p=-\partial_x\Gamma_p+G-R
=-\frac{1}{q}\partial_xJ_p+G-R.
\]

These signs must be tested by integrating each continuity equation over the device and comparing the result with boundary fluxes.

## 5. Electrostatics

For spatially varying permittivity,

\[
\partial_x\!\left(\varepsilon\partial_x\phi\right)
=-\rho,
\]

with

\[
\rho=q\left(p-n+N_D^+-N_A^-\right)+\rho_t+\rho_{\mathrm{fixed}}.
\]

For constant \(\varepsilon\), this reduces to

\[
\partial_x^2\phi=-\rho/\varepsilon.
\]

The treatment of ionized dopants must state whether complete ionization is assumed. At 77 K, incomplete ionization and compensation may be non-negligible and therefore require either explicit statistics or a justified parameterized net-ionized density.

## 6. Carrier statistics and transport coefficients

### 6.1 Nondegenerate closure

The Boltzmann approximation may be used only when the quasi-Fermi levels remain sufficiently far from the relevant band edges. A quantitative criterion must be declared, for example by requiring the local reduced chemical potentials to satisfy a bound such as

\[
\eta_n=(E_{Fn}-E_c)/(k_BT)\lesssim -2
\]

and the analogous hole condition, with the approximation error assessed using Fermi-Dirac integrals.

Under the nondegenerate, isothermal, locally equilibrated approximation,

\[
D_n=\mu_n k_BT/q,
\qquad
D_p=\mu_p k_BT/q.
\]

### 6.2 Degenerate closure

When degeneracy is relevant, carrier densities and generalized Einstein relations must be derived from the selected density-of-states model. The diffusion coefficient cannot be assigned by the Boltzmann Einstein relation without an error estimate.

HgCdTe nonparabolicity may require a Kane-type density of states. Phase 1 must decide whether the full nonparabolic relation materially changes the dimensionless regime boundaries or whether a simpler effective-density-of-states closure is adequate for the intended parameter range.

## 7. Recombination and generation

The baseline net SRH recombination law is

\[
R_{\mathrm{SRH}}=
\frac{np-n_i^2}
{\tau_p(n+n_1)+\tau_n(p+p_1)}.
\]

Phase 1 must distinguish:

- the **net** recombination term appearing in the mean continuity equations;
- the forward capture/emission event rates needed to construct a stochastic covariance;
- algebraic lifetime parameters from microscopic transition rates;
- trap occupancy dynamics from an adiabatically reduced SRH law.

Using \(2R_{\mathrm{SRH}}\), \(|R_{\mathrm{SRH}}|\), or another heuristic as a noise intensity is prohibited unless derived from the underlying forward and reverse event rates.

Optical generation is initially either uniform,

\[
G_{\mathrm{opt}}(x)=G_0,
\]

or Beer-Lambert,

\[
G_{\mathrm{opt}}(x)=\eta_{\mathrm{int}}\alpha\Phi_0e^{-\alpha x},
\]

with illumination direction, reflection losses, and photon-flux convention stated explicitly.

## 8. Boundary conditions

### 8.1 Electrostatic boundary conditions

The baseline voltage-driven condition is

\[
\phi(0)=0,
\qquad
\phi(L)=-V_b.
\]

Equivalent gauge choices are permitted if \(V_b=\phi(0)-\phi(L)\) is preserved.

### 8.2 Carrier boundary conditions

At each contact, one of the following must be selected and thermodynamically completed:

1. **Ohmic reservoir:** carrier electrochemical potentials or equilibrium carrier densities are imposed consistently with the metal work function and contact potential.
2. **Finite surface recombination/injection:** normal carrier flux is related to the departure from a contact-equilibrium population through electron and hole surface velocities.
3. **Blocking contact:** the relevant normal particle flux vanishes.

A provisional finite-recombination form is

\[
\Gamma_n\cdot\hat n=S_n(n-n_{n,\mathrm{eq}}),
\qquad
\Gamma_p\cdot\hat n=S_p(p-p_{p,\mathrm{eq}}),
\]

but the signs, equilibrium populations, injection counterparts, and fluctuation covariance must be derived separately at \(x=0\) and \(x=L\). A deterministic Robin condition alone is not a complete stochastic contact model.

## 9. Terminal current and displacement current

The local conduction current is

\[
J_c=J_n+J_p.
\]

Using charge continuity and Poisson's equation, the spatially conserved total current in one dimension is expected to be

\[
J_{\mathrm{tot}}(x,t)=J_n+J_p+\varepsilon\partial_tE,
\]

for constant \(\varepsilon\), with additional polarization terms included if the dielectric model is frequency dependent.

The terminal current is

\[
I(t)=A J_{\mathrm{tot}}(x,t),
\]

which must be independent of the evaluation position to within the discrete conservation tolerance.

A code path that evaluates \(A(J_n+J_p)\) at an arbitrary interior point at finite frequency is unacceptable unless displacement current is demonstrably negligible under a quantified criterion.

## 10. Linearized frequency-domain problem

Let \(u_0(x)\) solve the nonlinear steady-state residual

\[
F(u_0;\theta)=0.
\]

For a perturbation \(\delta u\),

\[
u=u_0+\delta u,
\]

and Fourier convention

\[
\delta u(t)=\Re\{\hat u(\omega)e^{j\omega t}\},
\]

the linearized deterministic operator is

\[
\left(j\omega M-J\right)\hat u=\hat b,
\]

where \(J=\partial F/\partial u|_{u_0}\). The exact sign of \(J\) depends on whether the residual is written as \(M\dot u-F(u)=0\) or \(M\dot u+F(u)=0\); the implementation and derivation must use one form consistently.

The stochastic extension is

\[
\left(j\omega M-J\right)\hat u=B\hat\xi,
\]

and the terminal fluctuation is

\[
\delta\hat I=c^T\hat u+d^T\hat\xi.
\]

Therefore,

\[
H_I(\omega)=c^T(j\omega M-J)^{-1}B+d^T,
\]

and

\[
S_I(\omega)=H_IQ_\xi H_I^\dagger.
\]

This expression is formal until the primitive processes, covariance normalization, contact terms, and terminal feed-through are derived.

## 11. Primitive stochastic processes to audit

Phase 1 must determine whether the minimal independent process set contains:

- bulk electron and hole diffusive flux fluctuations;
- paired generation and recombination events;
- trap capture and emission events with shared occupancy correlations;
- contact injection and extraction events;
- external resistor or source fluctuations;
- dielectric polarization fluctuations if a lossy dielectric model is used.

Potential double counting must be checked. For example, adding both local current-density noise and independent carrier-density GR noise may duplicate the same microscopic transitions if their derivations are not based on distinct primitive events.

## 12. PSD and Fourier conventions

The program will use a one-sided frequency PSD in hertz for reported detector spectra unless Phase 1 identifies a reason to use another convention:

\[
\langle \delta I^2\rangle=\int_0^\infty S_I^{(1)}(f)\,df.
\]

Internal derivations may use a two-sided angular-frequency PSD. Every conversion must state:

\[
\omega=2\pi f,
\]

and distinguish the factor of two associated with one-sided versus two-sided spectra from the factor of \(2\pi\) associated with hertz versus radians per second.

For a passive resistor at equilibrium, the required one-sided hertz-domain terminal relations are

\[
S_V^{(1)}(f)=4k_BTR,
\qquad
S_I^{(1)}(f)=4k_BT/R.
\]

The selected circuit boundary condition must make the relevant relation observable rather than identically constrained.

## 13. Initial nondimensionalization

A provisional scale set is

\[
\tilde x=x/L,
\quad
\tilde n=n/n_{\mathrm{ref}},
\quad
\tilde p=p/n_{\mathrm{ref}},
\quad
\tilde\phi=q\phi/(k_BT),
\quad
\tilde t=t/\tau_{\mathrm{ref}}.
\]

Candidate groups include:

\[
\Pi_\lambda=\frac{L}{L_{\mathrm{Debye}}},
\qquad
L_{\mathrm{Debye}}=\sqrt{\frac{\varepsilon k_BT}{q^2n_{\mathrm{ref}}}},
\]

\[
\Pi_{D,n}=\frac{L}{\sqrt{D_n\tau_{\mathrm{ref}}}},
\qquad
\Pi_{D,p}=\frac{L}{\sqrt{D_p\tau_{\mathrm{ref}}}},
\]

\[
\Pi_V=\frac{qV_b}{k_BT},
\qquad
\Pi_{C,n}=\frac{S_nL}{D_n},
\qquad
\Pi_{C,p}=\frac{S_pL}{D_p},
\]

\[
\Pi_G=\frac{G_{\mathrm{ref}}\tau_{\mathrm{ref}}}{n_{\mathrm{ref}}},
\qquad
\Pi_\alpha=\alpha L.
\]

The scaling analysis must determine whether `Pi_E` is independent of `Pi_V` for a nonuniform field. In a voltage-driven finite device, \(qEL/k_BT\) is a local or derived field measure, whereas \(qV_b/k_BT\) is the independent terminal forcing.

## 14. Numerical architecture requirements

Later implementation should separate:

1. material and statistical closures;
2. deterministic residual and Jacobian;
3. boundary and terminal models;
4. nondimensional scaling;
5. steady nonlinear solver;
6. linearized frequency solver;
7. stochastic covariance assembly;
8. terminal transfer operator;
9. eigenmode and non-normality analysis;
10. verification and benchmark cases.

At least two independent approaches are required for selected cases. The preferred pairing is:

- conservative finite volume or mixed finite element for the nonlinear and linearized device equations;
- independent finite-difference/eigenfunction or reduced analytical calculation for benchmark limits.

Monte Carlo simulation is optional and should not replace covariance derivation.

## 15. Acceptance metrics for later phases

Each reported curve must be associated with the applicable metrics:

- mesh-refinement change in terminal observables;
- residual norms by governing equation;
- integrated charge-conservation error;
- maximum spatial variation of total terminal current;
- frequency-grid refinement error;
- condition number or iterative-solver convergence information;
- sensitivity to boundary-condition implementation;
- error relative to analytical limiting cases;
- uncertainty interval from poorly constrained material parameters.

## 16. Phase 1 unresolved decisions

1. Is an algebraic SRH law sufficient for stochastic closure, or must trap occupancy be dynamic?
2. What contact model recovers detailed balance and equilibrium terminal noise?
3. What is the correct external-circuit representation for both biased-noise prediction and equilibrium verification?
4. Which HgCdTe carrier-statistics model is necessary at 77 K over the intended composition and doping range?
5. Which primitive noise-source formulation avoids double counting while remaining numerically tractable?
6. Is the linearized operator sufficiently normal for an eigenmode-sum interpretation, or are biorthogonal/pseudospectral methods required?
7. What quantitative error threshold defines validity of the lumped single-Lorentzian approximation?
8. Which parameter ranges are supported by public HgCdTe literature rather than exploratory assumptions?

## 17. Stop rule

Do not advance to broad deterministic or stochastic simulations until a decision record confirms that the governing equations, state variables, contacts, terminal circuit, stochastic covariance strategy, PSD convention, dimensionless groups, material-parameter ranges, and prior-art boundary are sufficiently specified to make later numerical output interpretable and falsifiable.