# R06 Phase 1C statistics-interface targets

These targets validate a thermodynamic software contract. They do not validate an HgCdTe density-of-states model.

## H0 - input domain

Reject nonfinite reduced chemical potential, nonpositive temperature, nonpositive density scale, and inconsistent bipolar temperatures.

## H1 - one-evaluation contract

A carrier closure evaluation must return:

- density;
- positive chemical compressibility magnitude;
- generalized Einstein factor;
- temperature and reduced chemical potential;
- the explicit density scale used by the closure.

## H2 - density identity

For the parabolic benchmark,

\[
n=N_*\mathcal F_{1/2}(\eta).
\]

## H3 - susceptibility identity

For the same evaluation,

\[
\frac{\partial n}{\partial\mu}
=\frac{N_*}{k_BT}\mathcal F_{-1/2}(\eta).
\]

The analytical susceptibility must agree with a centered density derivative with respect to reduced chemical potential.

## H4 - generalized Einstein identity

\[
\Theta
=\frac{n}{k_BT\,\partial n/\partial\mu}
=\frac{\mathcal F_{1/2}}{\mathcal F_{-1/2}}.
\]

The identity must close to numerical precision.

## H5 - Boltzmann limit

For sufficiently negative reduced chemical potential,

\[
\mathcal F_{1/2}(\eta)\rightarrow e^\eta,
\qquad
\Theta\rightarrow 1.
\]

## H6 - degenerate correction

The benchmark generalized Einstein factor must depart from unity in the degenerate regime rather than silently forcing the classical Einstein relation.

## H7 - monotonicity

Carrier density must increase monotonically with reduced chemical potential.

## H8 - scale separation

Density and compressibility must scale linearly with the declared density scale, while the generalized Einstein factor remains scale independent.

## H9 - protocol compliance

The benchmark closure must satisfy the runtime carrier-statistics protocol used by future material closures.

## H10 - bipolar assembly

Electron and hole states must share one temperature. Their carrier charge number density is

\[
p-n,
\]

and the positive charge-susceptibility scale is the sum of the electron and hole compressibility magnitudes.

## H11 - model identity

The parabolic closure must remain labeled as a mathematical benchmark. Passing H0-H10 does not convert it into an HgCdTe material closure.

## H12 - source boundary

No test may claim reproduction of Madarasz 1985 or Lowney 1992. Hansen-Schmit may be used only as a bounded intrinsic-density benchmark, and the 1991 NIST nonlinear gap may be used only as a verified gap input or sensitivity control.

## Acceptance consequence

Passing H0-H12 authorizes closure-independent deterministic and later stochastic assembly. It does not authorize material-accurate equilibrium density, screening, noise, gain, responsivity, detectivity, or contact predictions.
