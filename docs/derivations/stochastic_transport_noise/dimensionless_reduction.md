# R06 dimensionless reduction

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** Phase 1 analytical reduction; no numerical regime map yet

## 1. Purpose

The original project prompt listed several useful similarity parameters, but some are redundant after a reference scale and Einstein relation are selected. This document derives a minimal baseline set for the nondegenerate isothermal model and identifies the additional groups required by traps, contacts, optics, and the terminal circuit.

The reduction is not valid automatically in degenerate HgCdTe. Section 10 states what changes when generalized Einstein relations are required.

## 2. Reference scales

Let

\[
V_T=\frac{k_BT}{q},
\qquad
x=L\xi,
\qquad
t=\tau_r\theta,
\]

\[
n=n_r N,
\qquad
p=n_r P,
\qquad
\phi=V_T\psi.
\]

Use a reference diffusion coefficient `D_r` and current-density scale

\[
J_r=\frac{qD_r n_r}{L}.
\]

The dimensionless electric field is

\[
e=-\frac{d\psi}{d\xi},
\]

so the dimensional field is

\[
E=\frac{V_T}{L}e.
\]

The frequency variable is

\[
\Omega=\omega\tau_r.
\]

## 3. Nondegenerate drift-diffusion equations

With the Boltzmann Einstein relation `D_s = mu_s V_T`, define

\[
d_n=\frac{D_n}{D_r},
\qquad
d_p=\frac{D_p}{D_r}.
\]

The dimensionless currents are

\[
j_n=\frac{J_n}{J_r}
=d_n\left(Ne+\frac{dN}{d\xi}\right),
\]

\[
j_p=\frac{J_p}{J_r}
=d_p\left(Pe-\frac{dP}{d\xi}\right).
\]

Define the transport-to-recombination ratio

\[
\delta=\frac{D_r\tau_r}{L^2}.
\]

Then

\[
\frac{\partial N}{\partial\theta}
=
\delta\frac{\partial j_n}{\partial\xi}
+\mathcal G-\mathcal R,
\]

\[
\frac{\partial P}{\partial\theta}
=
-\delta\frac{\partial j_p}{\partial\xi}
+\mathcal G-\mathcal R,
\]

where

\[
\mathcal G=\frac{\tau_r G}{n_r},
\qquad
\mathcal R=\frac{\tau_r R}{n_r}.
\]

The commonly proposed diffusion-length parameter is therefore

\[
\Pi_D=\frac{L}{\sqrt{D_r\tau_r}}=\delta^{-1/2}.
\]

Only one of `Pi_D` and `delta` is independent.

## 4. Poisson equation and screening

Define the reference Debye length

\[
L_{D,r}
=
\sqrt{\frac{\varepsilon V_T}{qn_r}}
=
\sqrt{\frac{\varepsilon k_BT}{q^2n_r}}.
\]

For constant permittivity,

\[
\frac{d^2\psi}{d\xi^2}
=-\Lambda^2
\left(
P-N+N_D^+-N_A^-+Q_t+Q_f
\right),
\]

where all charge densities inside the parentheses are normalized by `n_r`, and

\[
\Lambda=\frac{L}{L_{D,r}}.
\]

Thus the requested `Pi_lambda` is `Lambda`.

## 5. Applied field and voltage

The normalized terminal voltage is

\[
U=\frac{V_b}{V_T}=\frac{qV_b}{k_BT}.
\]

For a uniform field `E=V_b/L`,

\[
\frac{qEL}{k_BT}=U.
\]

Therefore the originally listed

\[
\Pi_E=\frac{qEL}{k_BT}
\]

is not independent from normalized applied voltage in the uniform-field limit. In a space-charge-modified device, the local field is a state variable; the independent control remains the terminal voltage `U`, while `e(x)` is an output.

## 6. Derived time-scale ratios

### 6.1 Transit time

Using the reference mobility `mu_r=D_r/V_T`, the drift transit time at uniform field is

\[
t_{\mathrm{tr}}=\frac{L}{\mu_r E}.
\]

Hence

\[
\frac{\tau_r}{t_{\mathrm{tr}}}
=
\frac{D_r\tau_r}{L^2}\frac{V_b}{V_T}
=
\delta U
=
\frac{U}{\Pi_D^2}.
\]

The transit-to-lifetime ratio is therefore derived from `U` and `Pi_D`; it is not an independent group under the baseline assumptions.

### 6.2 Dielectric relaxation

For a unipolar reference conductivity `sigma_r=q mu_r n_r`,

\[
\tau_{\mathrm{dr}}=\frac{\varepsilon}{\sigma_r}.
\]

Then

\[
\frac{\tau_r}{\tau_{\mathrm{dr}}}
=
\frac{D_r\tau_r}{L_{D,r}^2}
=
\delta\Lambda^2
=
\frac{\Lambda^2}{\Pi_D^2}.
\]

Thus dielectric-relaxation-to-recombination time is also derived from `Pi_D` and `Lambda` when the same carrier density, mobility, and Einstein relation define the scales.

For bipolar conductivity, replace `sigma_r` with `q(mu_n n_0+mu_p p_0)`; an equilibrium carrier-ratio factor then appears.

## 7. Contacts

At contact `c` for carrier `s`, define the contact Biot number

\[
\mathrm{Bi}_{s,c}=\frac{S_{s,c}L}{D_s}.
\]

Separate values are required for:

- electrons and holes;
- left and right contacts;
- mean exchange and any distinct interfacial storage process.

The original single parameter `Pi_C=S_cL/D` is insufficient for asymmetric bipolar devices.

Limiting cases:

\[
\mathrm{Bi}_{s,c}\to 0
\]

is blocking for that carrier under a pure exchange boundary, while

\[
\mathrm{Bi}_{s,c}\to\infty
\]

approaches a reservoir-pinned carrier population if the equilibrium density and electrochemical potential are specified consistently.

A stochastic contact also requires normalized forward and reverse event intensities; `Bi` alone does not determine the contact noise.

## 8. Optical generation

For Beer-Lambert generation,

\[
G(x)=G_0e^{-\alpha x},
\]

define

\[
A_\alpha=\alpha L
\]

and

\[
g_0=\frac{G_0\tau_r}{n_r}.
\]

The originally listed

\[
\Pi_G=\frac{G\tau}{n_0}
\]

must be interpreted carefully:

- `g_0` is an independent excitation amplitude;
- `A_alpha` controls spatial nonuniformity;
- normalization by an equilibrium carrier density rather than arbitrary `n_r` introduces an explicit injection-level ratio.

## 9. Trap and SRH groups

For a single trap family, define

\[
\eta_t=\frac{N_t}{n_r},
\qquad
\epsilon_t=\frac{E_t-E_i}{k_BT}.
\]

Microscopic capture and emission kinetics require dimensionless rates such as

\[
\kappa_n=c_n n_r\tau_r,
\qquad
\kappa_p=c_p n_r\tau_r,
\]

\[
\epsilon_n^{(r)}=e_n\tau_r,
\qquad
\epsilon_p^{(r)}=e_p\tau_r.
\]

Only combinations consistent with detailed balance should be treated as independent. If emission rates are generated from capture coefficients and equilibrium densities, they are derived rather than independently swept.

An algebraic SRH model can be written with normalized lifetime and density ratios, but the stochastic model should retain the event-rate groups until an adiabatic elimination is proven.

## 10. Mobility and carrier ratios

Select one carrier as the diffusion reference. Then

\[
M=\frac{\mu_n}{\mu_p}
=
\frac{D_n}{D_p}
\]

under the same nondegenerate Einstein relation.

Consequently `Pi_mu`, `d_n`, and `d_p` are not all independent. A convenient choice is

\[
d_n=1,
\qquad
d_p=M^{-1}.
\]

Additional independent equilibrium ratios include

\[
r_p=\frac{p_0}{n_r},
\qquad
r_n=\frac{n_0}{n_r},
\qquad
r_D=\frac{N_D^+-N_A^-}{n_r}.
\]

The reference density should be selected to remove one of these ratios where possible.

## 11. Degenerate transport

For degenerate or strongly nonparabolic HgCdTe, write

\[
D_s=\mu_s V_T\chi_s,
\]

where `chi_s` is the generalized Einstein factor derived from the selected density-of-states and Fermi-integral closure.

Then the transport equations contain independent functions or parameters `chi_n` and `chi_p`. The equality

\[
\frac{D_n}{D_p}=\frac{\mu_n}{\mu_p}
\]

no longer holds generally.

The minimal group set must then include:

- reduced electron and hole chemical potentials;
- nonparabolicity parameters;
- generalized Einstein factors or the parameters needed to compute them.

R06 should first test whether `chi_s-1` materially changes the target regime boundaries. If not, the nondegenerate model may be retained with a quantified error bound.

## 12. Terminal circuit

Let the device small-signal resistance scale be

\[
R_r=\frac{L}{Aq\mu_r n_r}.
\]

Define normalized external impedance

\[
z_{\mathrm{ext}}(\Omega)=\frac{Z_{\mathrm{ext}}(\omega)}{R_r}.
\]

Ideal voltage bias, ideal current bias, and finite loading are distinct limits of `z_ext`; they are not interchangeable boundary labels.

If contact capacitance or external capacitance is included, normalized products such as

\[
\Omega R_r C
\]

enter the loaded transfer function.

## 13. Minimal baseline control set

For a symmetric, nondegenerate, isothermal, single-trap, voltage-driven one-dimensional model, a practical independent set is:

1. `Pi_D = L/sqrt(D_n tau_r)`;
2. `Lambda = L/L_D,r`;
3. `U = qV_b/(k_BT)`;
4. mobility ratio `M = mu_n/mu_p`;
5. equilibrium carrier and compensation ratios after one density normalization is removed;
6. four contact Biot numbers `Bi_n,L`, `Bi_n,R`, `Bi_p,L`, `Bi_p,R`;
7. optical depth `A_alpha`;
8. normalized generation amplitude `g_0`;
9. trap-density ratio `eta_t`;
10. trap energy `epsilon_t`;
11. a nonredundant set of capture/emission rate ratios;
12. normalized external impedance `z_ext(Omega)`.

Derived groups include:

- normalized field in the uniform limit: `Pi_E=U`;
- transit ratio: `tau_r/t_tr=U/Pi_D^2`;
- dielectric-relaxation ratio: `tau_r/t_dr=Lambda^2/Pi_D^2` for the unipolar reference closure;
- contact diffusion lengths once `Pi_D` and `Bi` are fixed.

## 14. Recommended sweep hierarchy

Do not sweep the full Cartesian product.

### Tier 1: analytical structure

- `Pi_D`;
- `Lambda`;
- `U`;
- symmetric `Bi`;
- `Omega`.

### Tier 2: bipolar and trap structure

- mobility ratio;
- equilibrium carrier ratio;
- trap density;
- capture-rate asymmetry;
- trap energy.

### Tier 3: measurement and asymmetry

- left/right contact asymmetry;
- optical depth;
- injection level;
- external impedance.

This hierarchy separates whether multimode behavior originates from transport/screening, trap kinetics, contacts, or measurement loading.

## 15. Acceptance checks for the reduction

1. Dimensional reconstruction must recover SI equations exactly.
2. Two dimensional parameter sets with identical independent groups must produce identical normalized solutions.
3. Derived time-scale ratios must not be swept independently in baseline studies.
4. Strong-screening limits must be taken through `Lambda -> infinity` while resolving the associated boundary layers.
5. Bulk limits require both large `Pi_D` or appropriate domain scaling and contact separation from the observation kernel; large length alone is not sufficient.
6. Degenerate corrections must be evaluated before quantitative HgCdTe regime boundaries are claimed.

## 16. Current conclusion

The initial prompt’s groups are physically useful, but `Pi_E`, transit time, dielectric relaxation time, mobility ratio, and diffusion ratios contain redundancies under the baseline nondegenerate scaling. The reduced set above should control Phase 2 implementation and later regime maps.