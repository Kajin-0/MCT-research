# R06 stochastic finite-contact detailed-balance closure

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** project derivation; thermodynamic reference model; comparison with Park 2022 and Smith 1984 remains mandatory

## 1. Purpose

A deterministic finite surface-recombination boundary such as

\[
\Gamma_s\cdot\hat n=S_s(c_s-c_{s,\mathrm{eq}})
\]

specifies only the mean carrier flux. It does not specify the fluctuation intensity because zero mean flux at equilibrium results from cancellation of nonzero forward and reverse exchange events.

This document defines a minimal stochastic reservoir-exchange model that:

1. reproduces a finite-velocity Robin mean boundary;
2. satisfies local detailed balance;
3. retains finite equilibrium contact fluctuations;
4. distinguishes independent carrier exchange from pair recombination;
5. recovers blocking and fast-reservoir limits in controlled ways;
6. provides a covariance input for a finite-volume or finite-element boundary discretization.

The closure is a project derivation, not yet a source-established HgCdTe contact model.

## 2. Geometry and normal convention

The detector occupies `0 <= x <= L`.

The outward normals are

\[
\hat n_L=-\hat x,
\qquad
\hat n_R=+\hat x.
\]

For carrier species `s`, let

\[
\Gamma_s^{\mathrm{out}}=\Gamma_s\cdot\hat n_c
\]

be positive when particles leave the semiconductor through contact `c`.

Each boundary model is written in terms of particle flux first. Conventional current signs are applied afterward:

\[
J_n=-q\Gamma_n,
\qquad
J_p=+q\Gamma_p.
\]

This prevents electron-charge signs from being mixed into the event stoichiometry.

## 3. Boundary event counting

Consider a contact of area `A_c`. For species `s`, define independent counting processes:

- `N_{s,c}^{in}(t)`: particles injected from the reservoir into the semiconductor;
- `N_{s,c}^{out}(t)`: particles extracted from the semiconductor into the reservoir.

Let their propensities per unit area be

\[
a_{s,c}^{in}
\quad\text{and}\quad
 a_{s,c}^{out},
\]

with units `m^-2 s^-1`.

The mean outward particle flux is

\[
\overline{\Gamma}_{s,c}^{out}
=a_{s,c}^{out}-a_{s,c}^{in}.
\]

The area-averaged stochastic flux is

\[
\Gamma_{s,c}^{out}(t)
=
 a_{s,c}^{out}-a_{s,c}^{in}
+\eta_{s,c}(t).
\]

For independent Poisson event streams, the time-domain covariance is

\[
\left\langle
\eta_{s,c}(t)\eta_{s',c'}(t')
\right\rangle
=
\delta_{ss'}\delta_{cc'}
\frac{a_{s,c}^{out}+a_{s,c}^{in}}{A_c}
\delta(t-t').
\]

This equation defines the primitive time-domain normalization. Conversion to the internal two-sided angular-frequency covariance and the reported one-sided per-hertz PSD must follow `conventions.md`.

At equilibrium,

\[
a_{s,c}^{out}=a_{s,c}^{in},
\]

so the mean flux vanishes while the covariance remains nonzero.

## 4. Classical nondegenerate reservoir closure

For a nondegenerate carrier density `c_s` adjacent to the contact, choose

\[
a_{s,c}^{out}=S_{s,c}c_s,
\]

\[
a_{s,c}^{in}=S_{s,c}c_{s,c}^{eq},
\]

where `S_{s,c}` has units `m s^-1` and `c_{s,c}^{eq}` is the semiconductor carrier density in equilibrium with that contact reservoir under the selected electrostatic gauge and band alignment.

The mean boundary condition is

\[
\overline{\Gamma}_{s,c}^{out}
=S_{s,c}(c_s-c_{s,c}^{eq}).
\]

The primitive boundary-flux covariance is

\[
Q_{s,c}^{\Gamma}
=
\frac{S_{s,c}(c_s+c_{s,c}^{eq})}{A_c}.
\]

At equilibrium,

\[
Q_{s,c,eq}^{\Gamma}
=
\frac{2S_{s,c}c_{s,c}^{eq}}{A_c}.
\]

The factor of two here comes from equal forward and reverse event activity. It is not the one-sided/two-sided PSD conversion factor.

## 5. Local detailed balance

Let `mu_{s,c}` be the reservoir electrochemical potential and `mu_s` the semiconductor electrochemical potential evaluated at the boundary.

For an injection event defined as transferring one particle from reservoir to semiconductor, local detailed balance requires

\[
\ln\frac{a_{s,c}^{in}}{a_{s,c}^{out}}
=
\frac{\mu_{s,c}-\mu_s}{k_BT}
\]

for the selected sign and event convention.

At equilibrium, `mu_s=mu_{s,c}` and the forward and reverse rates are equal.

For the classical density closure, the relation follows when

\[
\frac{c_s}{c_{s,c}^{eq}}
=
\exp\!\left(\frac{\mu_s-\mu_{s,c}}{k_BT}\right)
\]

under the same density-of-states and electrostatic reference.

The equilibrium carrier density cannot therefore be chosen independently of contact potential, band alignment, and carrier statistics.

## 6. Fermionic occupancy closure

For a resolved interfacial state of energy `E`, let `f_s` be its semiconductor-side occupation and `f_c` the reservoir Fermi occupation. A symmetric exchange model is

\[
a^{in}=\kappa f_c(1-f_s),
\]

\[
a^{out}=\kappa f_s(1-f_c).
\]

Then

\[
\frac{a^{in}}{a^{out}}
=
\frac{f_c/(1-f_c)}{f_s/(1-f_s)}
=
\exp\!\left(\frac{\mu_c-\mu_s}{k_BT}\right).
\]

This provides a microscopic template for degenerate contacts. A continuum contact model would integrate over energy, transmission, and transverse modes.

R06 will not use the classical `S c` closure quantitatively in degenerate HgCdTe unless comparison with an energy-resolved model establishes a controlled error.

## 7. Boundary control-volume covariance

Suppose the boundary-adjacent finite-volume cell has volume

\[
V_1=A_c\Delta x_1.
\]

An injection event changes the cell carrier number by `+1`; extraction changes it by `-1`. The carrier-density source in the cell is

\[
\zeta_{s,c}(t)
=
\frac{1}{A_c\Delta x_1}
\left(
\frac{dN_{s,c}^{in}}{dt}
-
\frac{dN_{s,c}^{out}}{dt}
\right).
\]

Its covariance is

\[
\left\langle
\zeta_{s,c}(t)\zeta_{s,c}(t')
\right\rangle
=
\frac{a_{s,c}^{in}+a_{s,c}^{out}}
{A_c\Delta x_1^2}
\delta(t-t').
\]

The same event enters the external terminal current with its carrier charge and orientation. Therefore the boundary state source and direct terminal-current feed-through are correlated and must be assembled from the same primitive event channel.

Creating one independent density source and another independent contact-current source would double count the boundary event.

## 8. Event stoichiometry including terminal charge

Augment the stochastic state with an external transferred-charge coordinate `Q_ext`. For a carrier event `r`, define a stoichiometric vector

\[
\nu_r=
\begin{bmatrix}
\Delta N_n\\
\Delta N_p\\
\Delta N_t\\
\Delta Q_{ext}/q
\end{bmatrix}.
\]

Examples depend on terminal orientation.

For an electron injected from the left metal into the semiconductor boundary cell:

- semiconductor electron number increases by one;
- external circuit charge transfer is determined by the selected terminal-current sign.

The covariance contribution is

\[
Q_r=\nu_r\nu_r^T a_r.
\]

This automatically produces state-terminal cross covariance and ensures that direct feed-through is not added independently.

The exact `Q_ext` sign table must be fixed with the circuit orientation before implementation.

## 9. Independent exchange versus surface pair recombination

Separate electron and hole Robin boundaries represent independent exchange with reservoirs:

\[
n\rightleftharpoons n_c,
\qquad
p\rightleftharpoons p_c.
\]

A surface recombination event is different:

\[
e^-+h^+\rightarrow \text{reservoir excitation},
\]

with stoichiometry

\[
\nu_{rec}=(-1,-1,\ldots).
\]

It generates positive electron-hole source covariance because both populations change in the same event.

The reverse surface-generation event has stoichiometry `(+1,+1,...)`.

A boundary described by a single “surface recombination velocity” may therefore hide at least two different physical closures:

1. independent carrier exchange with a metal reservoir;
2. pair recombination/generation through interface states.

They produce different cross-covariances and potentially different terminal-current feed-through.

R06 must not identify them without a microscopic or source-supported argument.

## 10. Interfacial trap state

If contact recombination proceeds through a localized interface trap, introduce an occupancy state `f_{t,c}` and four primitive channels analogous to bulk SRH:

1. electron capture;
2. electron emission;
3. hole capture;
4. hole emission.

The interfacial trap occupancy then couples electron and hole exchange and can introduce its own pole.

An effective finite-velocity boundary may be obtained only after eliminating this interfacial state. The elimination generally produces frequency-dependent admittance and colored contact covariance.

This is a plausible mechanism by which a nominally simple contact velocity can generate multimode terminal noise.

## 11. Blocking-contact limit

For the classical exchange model,

\[
S_{s,c}\rightarrow 0
\]

implies

\[
a_{s,c}^{in},a_{s,c}^{out}\rightarrow 0,
\]

so both mean exchange and primitive contact-exchange noise vanish.

This limit is physically appropriate only when no other interface-state, tunneling, capacitive, or displacement-current process remains.

A blocking contact can still contribute terminal displacement current through electrostatic coupling even when particle exchange vanishes.

## 12. Fast-reservoir limit

As

\[
S_{s,c}\rightarrow\infty,
\]

the boundary carrier population is rapidly driven toward `c_{s,c}^{eq}`. In a resolved finite-volume model, both the deterministic relaxation rate and the primitive event intensity diverge while the boundary fluctuation variance can remain finite after fast-variable elimination.

Therefore the reservoir limit must not be implemented by simply setting the contact-noise source to zero when imposing a Dirichlet density.

Two valid approaches are:

1. retain a large but finite exchange rate and demonstrate convergence;
2. analytically eliminate the boundary population and derive the induced Dirichlet-reservoir covariance.

The second approach is preferable for conditioning but remains to be derived.

## 13. Contact Biot number and noise strength

Define

\[
\mathrm{Bi}_{s,c}=\frac{S_{s,c}L}{D_s}.
\]

`Bi` controls deterministic exchange relative to diffusion, but the equilibrium noise strength also depends on:

- equilibrium carrier density;
- contact area;
- carrier statistics;
- reservoir temperature;
- microscopic transmission or capture mechanism;
- whether interfacial storage states are present.

Two contacts with the same `Bi` can therefore have different stochastic covariance.

## 14. Linearized contact admittance

For the classical closure, write

\[
c_s=c_{s,c}^{eq}+\delta c_s.
\]

The mean linearized outward flux is

\[
\delta\Gamma_{s,c}^{out}=S_{s,c}\delta c_s.
\]

The equilibrium primitive flux covariance is

\[
Q_{s,c,eq}^{\Gamma}
=
\frac{2S_{s,c}c_{s,c}^{eq}}{A_c}.
\]

This pair is the boundary analogue of a dissipative conductance and its equilibrium fluctuation source. A complete device-level FDT proof must combine it with bulk transport, bulk reactions, electrostatic response, and the external circuit.

## 15. Nonequilibrium extension

Away from equilibrium, the Poisson closure gives

\[
Q_{s,c}^{\Gamma}
=
\frac{a_{s,c}^{in}+a_{s,c}^{out}}{A_c},
\]

while the mean flux is the difference of the same rates.

This distinction is essential at high injection or bias. A large net current can result from strongly asymmetric rates, while the noise depends on their sum.

The classical closure predicts

\[
Q_{s,c}^{\Gamma}
=
\frac{S_{s,c}(c_s+c_{s,c}^{eq})}{A_c}.
\]

Whether this is valid for an HgCdTe metal contact under bias is an unresolved material/contact question.

## 16. Terminal FDT acceptance test

At zero bias and uniform temperature, assemble all primitive event channels and solve the loaded terminal problem. Define

\[
\epsilon_{FDT}(\omega)
=
\frac{
\left|S_I^{(1)}(\omega)-4k_BT\operatorname{Re}Y(\omega)\right|
}
{4k_BT\operatorname{Re}Y(\omega)}.
\]

The contact closure is rejected if mesh refinement, frequency refinement, and linear-solver convergence do not reduce `epsilon_FDT` below the declared benchmark tolerance.

A post hoc additive Johnson source is prohibited.

## 17. Required comparison with prior art

Before acceptance, compare this derivation against:

- Park 2022, DOI `10.1063/5.0111954`;
- Smith 1984, DOI `10.1063/1.334155`;
- Bonani and Ghione 1999, DOI `10.1016/S0038-1101(98)00253-6`;
- relevant stochastic boundary-condition and semiconductor-contact literature identified in the continuing search.

The project derivation must be revised if those sources already contain a more complete or contradictory contact covariance.

## 18. Current decision

The classical forward/reverse exchange model is accepted only as the **reference thermodynamic contact closure for implementation design**. It is not yet accepted as a quantitative model of an HgCdTe metal contact.

The finite-contact novelty question remains unresolved until source comparison is complete.