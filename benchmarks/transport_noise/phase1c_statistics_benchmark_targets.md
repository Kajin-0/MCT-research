# R06 Phase 1C carrier-statistics benchmark targets

**Controlling issue:** #346  
**Status:** analytical and numerical target specification; no production material result

## S0 — normalized Fermi integrals

For a parabolic three-dimensional band, verify normalized complete Fermi integrals and the identity

\[
\frac{d\mathcal F_j}{d\eta}=\mathcal F_{j-1}.
\]

Reference points must include `eta = -8,-5,-4,-3,-2,-1,0,2,5`.

## S1 — Boltzmann asymptote

As `eta -> -infinity`, verify

\[
\mathcal F_j(\eta)\sim e^\eta,
\qquad
\Theta(\eta)=\frac{\mathcal F_{1/2}}{\mathcal F_{-1/2}}\to1.
\]

The relative errors in density, susceptibility, and `Theta` must decrease monotonically over the tested low-density sequence.

## S2 — preliminary reduction thresholds

For the parabolic reference, reproduce approximately:

| `eta` | density error from Boltzmann | `Theta-1` |
|---:|---:|---:|
| `-1` | `10.9%` | `11.5%` |
| `-2` | `4.46%` | `4.56%` |
| `-3` | `1.71%` | `1.73%` |
| `-4` | `0.64%` | `0.64%` |
| `-5` | `0.24%` | `0.24%` |

Acceptance tolerance for the tabulated check: absolute discrepancy below `5e-4` in fractional units.

## S3 — numerical susceptibility

For each density-of-states model, compare the implemented susceptibility against a complex-step derivative or a verified centered finite difference:

\[
\epsilon_\chi
=
\frac{|\chi_{implemented}-\chi_{check}|}
{\max(|\chi_{check}|,\chi_{floor})}.
\]

Target: `< 1e-8` for smooth quadrature regions and `< 1e-6` near adaptive-integration transitions.

## S4 — thermodynamic positivity

Across the accepted parameter domain require

\[
n>0,\quad p>0,\quad \chi_n>0,\quad \chi_p>0,
\quad D_n>0,\quad D_p>0.
\]

Any violation is a hard failure.

## S5 — nonparabolic-to-parabolic limit

When the nonparabolicity parameter is taken to zero, the Kane-mode density, susceptibility, generalized Einstein factor, and intrinsic density must converge to the parabolic-band result.

Report observed order or convergence rate with respect to the nonparabolicity control.

## S6 — charge-neutrality solve

For a homogeneous equilibrium state, solve charge neutrality using a bracketed chemical-potential root. Verify:

- residual below `1e-12` relative to the largest charged population;
- independence from initial guess within the bracket;
- monotonic root behavior;
- consistent intrinsic limit when net ionized doping tends to zero.

## S7 — screening reconstruction

Compute

\[
L_{scr}^{-2}=\frac{q^2}{\varepsilon}(\chi_n+\chi_p+\chi_{responsive}),
\]

and verify that the Boltzmann Debye result is recovered in the nondegenerate limit. Frozen dopant or trap charge must not appear in `chi_responsive`.

## S8 — contact FDT statistics consistency

For a classical density-relaxation contact, verify

\[
Q_{\Gamma,eq}=\frac{2k_BT S\chi}{A_c}.
\]

In the Boltzmann limit, confirm reduction to

\[
Q_{\Gamma,eq}=\frac{2Sc_{eq}}{A_c}.
\]

The bulk and boundary modules must return the same equilibrium susceptibility at identical state variables.

## S9 — intrinsic-density model comparison

Compare every accepted public intrinsic-density relation on one declared `(x,T)` grid. Report:

- pointwise ratios;
- maximum and median log error relative to the selected reference;
- regions with different extrapolation status;
- sensitivity of `L_scr`, equilibrium resistance, and contact covariance.

No single relation is declared authoritative until its equations and validity domain are audited.

## S10 — device-observable reduction check

For a small set of deterministic benchmark states only, compare Fermi–Dirac/nonparabolic and Boltzmann closures in:

- terminal current;
- differential conductance;
- screening length;
- contact equilibrium covariance coefficient;
- charge-neutrality chemical potential.

Boltzmann is accepted for an operating point only when every declared observable error is below the selected tolerance.

## Gate

These benchmarks may be implemented as small statistics prototypes during Phase 1C. They do not authorize a production drift-diffusion solver or material prediction.