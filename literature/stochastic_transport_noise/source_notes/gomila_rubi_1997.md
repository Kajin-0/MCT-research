# Gomila and Rubí (1997) equation-level audit

**Source:** G. Gomila and J. M. Rubí, “Non-equilibrium thermodynamic description of junctions in semiconductor devices,” *Physica A* **234**, 851–871 (1997).  
**DOI:** `10.1016/S0378-4371(96)00320-2`  
**Author preprint:** `arXiv:cond-mat/9603066v2`  
**Verification status:** author preprint inspected at equation level.

## 1. Scope

The paper derives a phenomenological junction model from nonequilibrium thermodynamics of systems with an interface. It supplies, within one framework:

- bulk carrier balance equations;
- drift–diffusion constitutive laws;
- Poisson electrostatics;
- explicit surface balance equations;
- electrochemical-potential boundary conditions;
- equilibrium, entropy-production, and Onsager restrictions;
- an application to thermionic-emission–diffusion transport at a metal–semiconductor contact.

The paper is deterministic. It does not itself provide the fluctuating interface covariance needed by R06, but it fixes the thermodynamic variables and dissipative operator that such covariance must use.

## 2. Bulk equations

For electron and hole species `k=1,2` in each bulk region `+` and `−`, the paper writes particle continuity as Eq. (3),

\[
\frac{\partial n_k^\pm}{\partial t}
+
\frac{\partial J_k^\pm}{\partial x}=0.
\]

Poisson electrostatics is written as Eq. (5),

\[
\frac{\partial D^\pm}{\partial x}=q^\pm.
\]

The drift–diffusion particle flux is Eq. (6). It is rewritten in terms of the electrochemical potential

\[
\phi_k^\pm=\mu_k^\pm+q_kV^\pm
\]

as Eq. (9),

\[
eJ_k^\pm
=-n_k^\pm\widetilde\mu_k^\pm
\frac{\partial\phi_k^\pm}{\partial x}.
\]

This identifies electrochemical-potential gradients, rather than density differences alone, as the natural bulk thermodynamic forces.

## 3. Generalized Einstein relation

The paper gives Eq. (7),

\[
\frac{D_k^\pm}{\widetilde\mu_k^\pm}
=
\frac{n_k^\pm}{e}
\frac{\partial\mu_k^\pm}{\partial n_k^\pm}.
\]

For nondegenerate statistics this reduces to Eq. (13),

\[
\frac{D_k^\pm}{\widetilde\mu_k^\pm}
=
\frac{k_BT}{e}.
\]

### R06 consequence

The degenerate contact and bulk correction is controlled by the thermodynamic susceptibility `partial n/partial mu`, consistent with the R06 contact result

\[
Q_{\Gamma,eq}
=
\frac{2k_BT S}{A_c}
\left(\frac{\partial c}{\partial\mu}\right)_{eq}.
\]

The Boltzmann form `2Sc_eq/A_c` is a special case.

## 4. Surface storage equations

The interface is represented as a separate surface subsystem with areal densities. Equation (14) is

\[
\frac{\partial n_k^s}{\partial t}
+
[J_k]_- = 0,
\]

where

\[
[J_k]_-=J_k^+-J_k^-.
\]

Thus a discontinuity in particle current changes the interfacial stored population.

### R06 consequence

A dynamic interface trap or contact-storage model is not an ad hoc addition. It is the surface-state realization of the interface balance law. Eliminating it is a singular or asymptotic reduction that can generate memory and colored covariance.

## 5. Electrostatic boundary conditions

The paper gives

\[
[D]_- = q^s
\]

and

\[
[V]_- = 0
\]

as Eqs. (17)–(18), where `q^s` is the interfacial areal charge.

Combined with the surface charge balance, these equations imply continuity of total conduction-plus-displacement current.

## 6. General interfacial constitutive law

The boundary particle currents are functions of electrochemical-potential differences between the two bulk regions and the surface subsystem. Equations (19)–(20) have the abstract form

\[
\mathbf J^\pm
=-\frac{1}{T}
\mathbf F^\pm(\mathbf X^+,\mathbf X^-),
\]

where

\[
X_k^+=\phi_k^+-\phi_k^s,
\qquad
X_k^-=\phi_k^s-\phi_k^-.
\]

The constitutive functions obey:

1. equilibrium zero-current condition, Eq. (21),

\[
\mathbf F^\pm(\mathbf 0,\mathbf 0)=\mathbf 0;
\]

2. nonnegative entropy production, Eq. (22),

\[
\mathbf X^+\!\cdot\mathbf F^+
+
\mathbf X^-\!\cdot\mathbf F^-
\ge0;
\]

3. equilibrium Onsager symmetry, Eq. (23),

\[
\left.
\frac{\partial F_k^\alpha}{\partial X_j^\beta}
\right|_{eq}
=
\left.
\frac{\partial F_j^\beta}{\partial X_k^\alpha}
\right|_{eq}.
\]

### R06 consequence

The stochastic interface covariance should be tied to the symmetric dissipative Jacobian of this constitutive law. A scalar `S` boundary is only one diagonal, no-storage, near-equilibrium reduction.

For bipolar contacts, the linear interface conductance is generally a matrix. Electron–hole or left–right cross coefficients are allowed subject to Onsager symmetry and nonnegative entropy production.

## 7. Conserved terminal current

The surface charge balance is Eq. (24). Substituting the displacement jump gives Eq. (25),

\[
[I]_-=0,
\]

where Eq. (26) defines

\[
I^\pm
=
\frac{\partial D^\pm}{\partial t}
+J_c^\pm.
\]

The paper notes that the total electric current is a function of time only in the one-dimensional bulk model.

### R06 consequence

The R06 conduction-plus-displacement terminal current is independently supported by interface thermodynamics. Surface charge storage redistributes conduction and displacement current but does not violate terminal-current continuity.

## 8. No-surface-state reduction

When all surface densities vanish, the particle currents are continuous and the entropy production reduces to Eq. (48). The boundary relation becomes Eq. (49),

\[
\mathbf J^+
=-\frac{1}{T}
\mathbf M([\boldsymbol\phi]_-).
\]

The function `M` must satisfy:

\[
\mathbf M(\mathbf0)=\mathbf0,
\]

\[
[\boldsymbol\phi]_-
\cdot
\mathbf M([\boldsymbol\phi]_-)
\ge0,
\]

and the corresponding equilibrium Onsager symmetry.

### R06 consequence

The no-interface-state contact is still an electrochemical-potential discontinuity law. Replacing it by `S(c-c_eq)` requires a statistical and band-alignment specialization.

## 9. Thermionic-emission boundary

For a unipolar metal–semiconductor contact without interface states, Eq. (60) is

\[
eJ_e^+
=V_R(n_m-n_e^+),
\]

where `V_R` is a positive kinetic coefficient and `n_m` is the metal-controlled equivalent carrier density.

The paper rewrites this as the nonlinear electrochemical-potential discontinuity relation Eq. (61), demonstrating that it satisfies the thermodynamic restrictions.

### R06 consequence

The classical R06 boundary

\[
\Gamma^{out}=S(c-c_{eq})
\]

is structurally equivalent to this thermionic-emission density form after orientation, charge, and reservoir-density conventions are translated. The stochastic extension must use the same forward/reverse process that produces the deterministic relation.

## 10. Limitations relative to R06

- deterministic only;
- no fluctuating boundary terms or covariance matrix;
- generation–recombination processes are excluded from the derivation;
- the worked metal–semiconductor example is unipolar;
- no HgCdTe material specialization;
- no optical generation;
- no terminal PSD.

## 11. Prior-art consequence

The following are established and cannot support novelty:

- deriving contact boundary laws from interface thermodynamic forces;
- treating the interface as a dynamic areal subsystem;
- electrochemical-potential discontinuity boundary conditions;
- nonlinear thermionic-emission contact laws;
- matrix-valued bipolar interface response subject to Onsager symmetry;
- total conduction-plus-displacement current continuity through an interface.

## 12. Required R06 benchmark

Near equilibrium, linearize the interface law as

\[
\delta\mathbf J
=-\mathbf L_X\,\delta\mathbf X.
\]

The symmetric part of `L_X` must be positive semidefinite. The equilibrium primitive interface covariance should then satisfy the selected fluctuation–dissipation convention, schematically

\[
\mathbf Q_{interface}
\propto
2k_BT\,\mathrm{sym}(\mathbf L_X),
\]

with the precise factors fixed by whether particle flux, charge current, per-area flux, angular frequency, and one-/two-sided PSD are used.

The scalar event closure must be recovered when `L_X` is diagonal, there is no surface storage, and carrier statistics are classical.

## 13. Novelty update

The candidate contribution is no longer a stochastic contact boundary in isolation. It is narrowed to:

- a conservation-consistent stochastic implementation of established interface thermodynamics inside a finite bipolar HgCdTe photoconductor;
- controlled reduction from interface-state or thermionic-emission physics to an effective finite-`S` boundary;
- quantified error in terminal GR spectra, responsivity, and inferred lifetime when that reduction is used;
- an uncertainty-qualified HgCdTe regime map.

## 14. Remaining source need

The next most useful source is Gomila and Rubí, “Fluctuations generated at semiconductor interfaces,” *Physica A* **258**, 17–31 (1998), because it should provide the fluctuating extension of the deterministic framework audited here.