# R06 carrier-statistics and generalized-Einstein gate

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** Phase 1C model decision; production calculations remain unauthorized

## 1. Decision

The reference HgCdTe transport closure will use Fermi–Dirac carrier statistics with a source-controlled nonparabolic density of states. For the narrow-gap conduction band, the intended reference is a Kane-type closure. A Boltzmann/parabolic model remains available only as a reduced benchmark whose error is computed against the reference state.

This decision is driven by the intended operating regime near 77 K, the small HgCdTe band gap, and the fact that density, compressibility, diffusion, screening, contact fluctuation strength, and equilibrium covariance all depend on the same statistics closure.

The project will not select a statistics model solely because it makes the drift-diffusion equations algebraically simpler.

## 2. Thermodynamic variables

For electrons define

\[
\eta_n=\frac{\mu_n-E_c}{k_BT},
\]

and for holes define

\[
\eta_p=\frac{E_v-\mu_p}{k_BT}.
\]

The carrier densities are evaluated from the selected density of states,

\[
n(\mu_n,T)=\int_{E_c}^{\infty}g_c(E)f(E;\mu_n,T)\,dE,
\]

\[
p(\mu_p,T)=\int_{-\infty}^{E_v}g_v(E)[1-f(E;\mu_p,T)]\,dE.
\]

The same numerical quadrature and band model must provide the thermodynamic susceptibilities

\[
\chi_n=\left(\frac{\partial n}{\partial\mu_n}\right)_T,
\qquad
\chi_p=\left(\frac{\partial p}{\partial\mu_p}\right)_T.
\]

Density and susceptibility may not be computed from inconsistent band models.

## 3. Generalized Einstein relation

For an isothermal carrier species `s`, with mobility defined relative to electrochemical-potential forcing, the generalized Einstein relation is

\[
\boxed{
\frac{D_s}{\mu_s}
=
\frac{n_s}{q\chi_s}
}
\]

or equivalently

\[
D_s
=
\mu_s\frac{k_BT}{q}\Theta_s,
\qquad
\Theta_s
=
\frac{n_s}{k_BT\chi_s}.
\]

`Theta_s` is the thermodynamic or generalized-Einstein factor. In the Boltzmann limit,

\[
\chi_s=\frac{n_s}{k_BT},
\qquad
\Theta_s=1.
\]

The implementation must compute `Theta_s` from the same density function used by charge neutrality and Poisson electrostatics.

## 4. Screening length

The differential screening coefficient must use charge susceptibility rather than a density inserted into a Boltzmann Debye formula.

For free electrons and holes,

\[
\kappa_{free}^2
=
\frac{q^2}{\varepsilon}(\chi_n+\chi_p).
\]

If ionized dopants or traps respond dynamically on the frequency and time scale under study, their equilibrium charge susceptibilities must be added with the appropriate charge-state factors. If they are frozen, they contribute mean charge but not differential screening.

Define

\[
L_{scr}=\kappa^{-1}.
\]

The Boltzmann Debye form is accepted only after demonstrating that it approximates this susceptibility-based result within the declared tolerance.

## 5. Contact fluctuation consequence

For a density-relaxation boundary

\[
\Gamma=S(c-c_{eq}),
\]

the linear particle-flux conductance is

\[
K_c=S\chi_c.
\]

The equilibrium contact-flux covariance is therefore

\[
Q_{\Gamma,eq}
=
\frac{2k_BT S\chi_c}{A_c}.
\]

The familiar expression

\[
Q_{\Gamma,eq}=\frac{2Sc_{eq}}{A_c}
\]

is the Boltzmann special case. The contact and bulk statistics models must therefore be identical at a shared equilibrium boundary.

## 6. Parabolic-band reduction check

For a three-dimensional parabolic band,

\[
n=N_c\mathcal F_{1/2}(\eta),
\]

with normalized complete Fermi integral `mathcal F`. The generalized-Einstein factor is

\[
\Theta(\eta)
=
\frac{\mathcal F_{1/2}(\eta)}
{\mathcal F_{-1/2}(\eta)}.
\]

The following values are numerical reduction checks, not HgCdTe material predictions:

| `eta` | Boltzmann density relative error | `Theta-1` |
|---:|---:|---:|
| `-1` | approximately `10.9%` | approximately `11.5%` |
| `-2` | approximately `4.46%` | approximately `4.56%` |
| `-3` | approximately `1.71%` | approximately `1.73%` |
| `-4` | approximately `0.64%` | approximately `0.64%` |
| `-5` | approximately `0.24%` | approximately `0.24%` |

These values establish a useful preliminary warning threshold. They do not replace a direct Kane-model comparison.

## 7. Operational reduction criteria

### Reference calculations

All quantitative HgCdTe calculations use the Fermi–Dirac/nonparabolic closure unless a later decision record narrows the domain.

### Boltzmann benchmark

A Boltzmann reduction may be reported when all of the following are satisfied over every cell and continuation state used in the comparison:

1. electron and hole reduced chemical potentials are below the declared threshold;
2. density error is below the observable-specific tolerance;
3. susceptibility error is below the same tolerance;
4. generalized-Einstein-factor error is below the same tolerance;
5. screening-length, steady-current, and differential-conductance errors pass their direct comparisons.

Preliminary screening thresholds are:

- `eta <= -3`: candidate two-percent reduction domain;
- `eta <= -4`: candidate one-percent reduction domain.

A direct reference-model calculation supersedes these approximate parabolic-band thresholds. Strong nonparabolicity can invalidate a threshold inferred from parabolic Fermi integrals.

## 8. Required comparison metrics

For every proposed operating domain, report

\[
\epsilon_n
=
\frac{|n_B-n_K|}{\max(n_K,n_{floor})},
\]

\[
\epsilon_\chi
=
\frac{|\chi_B-\chi_K|}{\max(\chi_K,\chi_{floor})},
\]

\[
\epsilon_D
=
\frac{|D_B-D_K|}{\max(D_K,D_{floor})},
\]

\[
\epsilon_L
=
\frac{|L_{scr,B}-L_{scr,K}|}{L_{scr,K}},
\]

plus steady-current and differential-conductance errors

\[
\epsilon_I
=
\frac{|I_B-I_K|}{\max(|I_K|,I_{floor})},
\]

\[
\epsilon_G
=
\frac{|G_B-G_K|}{\max(|G_K|,G_{floor})}.
\]

Here subscripts `B` and `K` denote the Boltzmann reduction and the selected Kane/Fermi–Dirac reference.

## 9. Numerical requirements

1. Density integrals and susceptibilities must be monotone in chemical potential.
2. `chi_n`, `chi_p`, `D_n`, and `D_p` must remain positive.
3. Analytical differentiation, automatic differentiation, or a complex-step/verified finite-difference check must agree within a declared tolerance.
4. Charge-neutrality solutions must be bracketed and reproducible.
5. Low-density asymptotes must recover Boltzmann statistics.
6. A parabolic-band mode must reproduce standard normalized Fermi-integral identities.
7. Kane and parabolic modes must converge as nonparabolicity is removed.
8. The equilibrium compressibility used by the stochastic covariance must equal that used by deterministic diffusion and screening.

## 10. Source hierarchy

The Phase 1C statistics audit uses the following source families:

- Hansen, Schmit, and Casselman for the public composition/temperature gap relation and its measurement lineage;
- Seiler et al. for a low-composition magnetoabsorption gap constraint;
- Hansen and Schmit, Madarasz and Szmulowicz, Finkman and Schacham, and Lowney et al. for intrinsic-carrier-density relations;
- Lowney et al. for a nonlinear-gap, Kane-k.p intrinsic-density treatment over narrow-gap compositions and cryogenic-to-room temperature;
- Elliott et al. and related Kane-model sources for nonparabolic low-gap carrier behavior.

Every equation used in code still requires equation-level verification and a recorded validity interval. Bibliographic identification alone is insufficient.

## 11. Decision status

Accepted:

- Fermi–Dirac/nonparabolic statistics as the reference architecture;
- susceptibility-based generalized Einstein and screening relations;
- Boltzmann transport as a controlled reduced model;
- explicit error metrics and preliminary reduced-chemical-potential thresholds.

Not yet accepted:

- one final Kane density-of-states parameterization;
- numerical effective masses or Kane matrix elements for the full R06 domain;
- one universal intrinsic-density relation;
- quantitative HgCdTe predictions;
- Phase 2 production implementation.

The parameter source ledger and equation audit must close these remaining choices before the final Phase 1 gate.