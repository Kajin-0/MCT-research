# Zocchi (2006) equation-level audit

**Source:** F. E. Zocchi, “Current and voltage noise spectrum due to generation and recombination fluctuations in semiconductors,” *Physical Review B* **73**, 035203 (2006).  
**DOI:** `10.1103/PhysRevB.73.035203`  
**Verification status:** user-supplied publisher PDF inspected in full; governing equations, boundary ensembles, terminal observables, source convention, asymptotes, and stated omissions verified.

## 1. Model class

The paper treats a uniform, one-dimensional, n-doped semiconductor of length `L` and cross-sectional area `A`, terminated by ideal metallic ohmic contacts. It is a **unipolar electron-plus-trap model**, not a bipolar electron-hole model.

The dynamic variables are:

- free-electron linear density `N(x,t)`;
- ionized-trap linear density `N_T(x,t)`;
- electric field `E(x,t)`.

The deterministic/stochastic equations are Eqs. (1)-(3):

\[
\partial_t N
=D\partial_x^2N+\mu\partial_x(EN)+g(N,N_T)-r(N,N_T),
\]

\[
\partial_t N_T=g(N,N_T)-r(N,N_T),
\]

\[
\partial_x E=\frac{q}{A\varepsilon}(N_T-N).
\]

The use of linear rather than volumetric densities explains the factor `A` in Poisson's equation.

## 2. Stochastic source convention

At the homogeneous equilibrium state,

\[
\langle N\rangle=\langle N_T\rangle=N_0,
\qquad
\langle g\rangle=\langle r\rangle=g_0.
\]

The paper takes generation and recombination to be statistically independent Poisson processes, each with spectral density `2 g_0`. Their difference

\[
\Delta g_r=g-r
\]

has zero mean and spectral density `4 g_0`.

This is consistent with the event-level principle that the covariance depends on the **sum** of forward and reverse rates. The paper does not derive a complete electron-hole-trap stoichiometric covariance because it has one free-carrier population and one ionized-trap population.

The paper reports spectra as functions of ordinary frequency `f` and evaluates transfer functions at `s=2 pi i f`. Its `4 g_0` convention must be translated through the R06 variance definition before numerical constants are copied.

## 3. Linearized operator

Writing

\[
N=N_0+n,
\qquad
N_T=N_0+n_T,
\qquad
E=E_e+E_i,
\]

the paper obtains Eqs. (6)-(8):

\[
\partial_t n
=D\partial_x^2n+\mu E_e\partial_xn
+\mu N_0\partial_xE_i
-\frac{n}{\tau_N}-\frac{n_T}{\tau_T}+\Delta g_r,
\]

\[
\partial_t n_T
=-\frac{n_T}{\tau_T}-\frac{n}{\tau_N}+\Delta g_r,
\]

\[
\partial_xE_i=\frac{q}{A\varepsilon}(n_T-n).
\]

The lifetimes are derivatives of the net mean rate, Eqs. (9)-(10). The nonlinear fluctuation product

\[
\mu\partial_x(E_i n)
\]

is discarded. The author describes this as neglecting Coulomb interaction among fluctuating electrons while retaining linear space-charge feedback through Poisson's equation.

## 4. Fixed-voltage current-noise ensemble

For current noise, the external voltage `V=E_eL` is fixed. The boundary conditions are

\[
n(0,t)=n(L,t)=0,
\]

and

\[
\int_0^L E_i(x,t)\,dx=0.
\]

The terminal current is explicitly written with conduction and displacement components in Eq. (12):

\[
i(t)=\frac{1}{L}\int_0^L
\left[-qj(x,t)+A\varepsilon\partial_tE_i(x,t)\right]dx.
\]

Using the fixed-voltage constraint and absorbing electron boundaries, it reduces to Eq. (14):

\[
i(t)=\frac{q\mu E_e}{L}\int_0^L n(x,t)\,dx.
\]

This directly verifies the R06 rule that the fixed-voltage terminal current is a spatially conserved conduction-plus-displacement observable and may reduce to a spatial average only after the boundary constraints are applied.

The current PSD is obtained by integrating the squared transfer function over statistically independent event positions, Eq. (15).

## 5. Open-circuit voltage-noise ensemble

The voltage-noise analysis is restricted to:

- zero external electric field;
- open electrical terminals;
- zero current density at both ends.

The boundary conditions are

\[
J(0,s)=J(L,s)=0,
\]

with `E_i(0,s)=0`; the equations imply `E_i(L,s)=0`. The carrier boundary conditions reduce to

\[
\partial_xN_{x_0}(0,s)=\partial_xN_{x_0}(L,s)=0.
\]

The fluctuating voltage is

\[
V_{x_0}(s)=-\int_0^L E_i(x,s)\,dx,
\]

and the voltage PSD is again an integral over event position.

The paper therefore treats current and voltage spectra as different terminal ensembles. It explicitly rejects the shortcut `S_V=R^2S_I` when resistance itself fluctuates.

## 6. Independent dimensionless structure

The paper defines

\[
\frac{1}{\tau}=\frac{1}{\tau_N}+\frac{1}{\tau_T},
\qquad
\frac{1}{\tau_\varepsilon}=\frac{q\mu N_0}{A\varepsilon}.
\]

For finite samples, the characteristic function contains

\[
\xi^2(s)=
\frac{L^2\tau_T}{D\tau_\varepsilon\tau}
\frac{(1+s\tau_\varepsilon)(1+s\tau)}{1+s\tau_T}.
\]

At zero frequency,

\[
\xi_0^2=\frac{L^2\tau_T}{D\tau_\varepsilon\tau}.
\]

This confirms that diffusion, trap relaxation, effective lifetime, and dielectric relaxation enter through coupled ratios rather than independent corner frequencies.

## 7. Spectral results

Verified results include:

- the long-sample current spectrum reduces to a single Lorentzian with effective lifetime `tau`, Eq. (19);
- finite samples have field-, diffusion-, screening-, and boundary-dependent spectra, Eqs. (20)-(25);
- for `tau_N > tau_T`, a midfrequency Lorentzian with approximately `tau_T` appears, while `tau_N < tau_T` gives more complex behavior;
- high-field current noise saturates rather than continuing to scale with field;
- low-field current noise is proportional to `V^2`;
- long-sample open-circuit voltage noise has an intermediate `f^-2` PSD region and a diffusion-controlled high-frequency asymptote

\[
S_V(f)\propto f^{-7/2}.
\]

Thus, strongly non-Lorentzian terminal spectra from finite diffusion and electrostatic coupling are established prior art.

## 8. Explicit omissions

The paper states that it does not include the single-particle autocorrelation associated with diffusion. Other limitations are:

- one mobile carrier species;
- one trap population;
- uniform material and coefficients;
- ideal ohmic or open terminal conditions;
- no finite stochastic contact exchange;
- no optical generation profile;
- no direct electron-hole pair covariance;
- no practical HgCdTe material model;
- small fluctuations about a uniform state;
- no nonlinear fluctuation-fluctuation Coulomb term.

## 9. Consequences for R06

### Established and unavailable as novelty

R06 cannot claim novelty for:

- finite-length full-frequency GR current noise with drift, diffusion, Poisson coupling, and traps;
- conduction-plus-displacement terminal current;
- separate fixed-voltage and open-circuit noise ensembles;
- multiple time scales from trap and dielectric relaxation;
- non-Lorentzian terminal asymptotes caused by distributed diffusion;
- event-position transfer-function integration.

### Required benchmark

A reduced R06 solver must reproduce:

1. Eqs. (6)-(8) in the unipolar uniform-coefficient limit;
2. the fixed-voltage boundary ensemble and Eq. (14);
3. the long-sample Lorentzian Eq. (19);
4. the finite-sample dependence on `V/V_T` and `xi(s)`;
5. the open-circuit zero-field boundary ensemble;
6. the `f^-7/2` high-frequency voltage-PSD asymptote.

### Remaining candidate gap

The paper does not provide the targeted bipolar HgCdTe model, finite stochastic contacts, optical generation, microscopic SRH event channels, or a controlled error map between the full model and conventional lifetime inference.

## 10. Novelty decision

The original broad R06 formulation is substantially occupied. Zocchi is the strongest source supporting a narrow quantitative contribution rather than a novelty claim based on combining drift-diffusion, Poisson, traps, finite length, and terminal spectra.