# Gomila and Rubí (1998) equation-level audit

**Source:** G. Gomila and J. M. Rubí, “Fluctuations generated at semiconductor interfaces,” *Physica A* **258**, 17–31 (1998).  
**PII printed in source:** `S0378-4371(98)00199-X`  
**DOI:** `10.1016/S0378-4371(98)00199-X`  
**Verification status:** user-supplied full paper inspected at equation level. The PDF itself prints the PII rather than a DOI.

## 1. Scope

The paper derives stochastic boundary conditions for carrier exchange through semiconductor interfaces. It treats:

- an ideal unipolar interface represented by one activated exchange process;
- ideal semiconductor-semiconductor and metal-semiconductor specializations;
- a nonideal interface with localized interface states;
- nonlinear nonequilibrium operation;
- the equilibrium linear-response fluctuation-dissipation limit.

It is the closest identified prior art to the R06 stochastic-contact construction.

## 2. Ideal interface: primitive activated process

For an ideal interface the exchange is represented by

\[
q_1 \rightleftharpoons q_2.
\]

After eliminating the internal reaction coordinate, the fluctuating boundary current is written in the paper’s particle-current convention as

\[
J_n(0,t)=\lambda_{12}z_1-\lambda_{21}z_2+\xi(t),
\]

where `z_i` are carrier activities and `lambda_ij` are transition coefficients.

The random interfacial flux has zero mean and time-domain covariance

\[
\left\langle\xi(t)\xi(t')\right\rangle
=
\frac{1}{A}
\left(
\lambda_{12}z_1+\lambda_{21}z_2
\right)
\delta(t-t').
\]

This is exactly a forward-plus-reverse event-activity result. The mean is the difference of the two activities; the covariance is their sum.

### R06 mapping

Identify

\[
a^{\mathrm{out}}=\lambda_{12}z_1,
\qquad
a^{\mathrm{in}}=\lambda_{21}z_2,
\]

up to the selected interface orientation. Then

\[
\bar\Gamma=a^{\mathrm{out}}-a^{\mathrm{in}},
\qquad
Q_\Gamma=\frac{a^{\mathrm{out}}+a^{\mathrm{in}}}{A}.
\]

The R06 forward/reverse contact covariance is therefore source-established in general form, not a novel project derivation.

## 3. Nonlinear generalized fluctuation relation

The source rewrites the ideal-interface mean law in terms of the electrochemical-potential discontinuity `[F]=F_2-F_1` and obtains a nonlinear relationship of the form

\[
\bar J_n=-\frac{1}{T}M([F]).
\]

The corresponding covariance is written as

\[
\left\langle\xi(t)\xi(t')\right\rangle
=
\frac{1}{A}
\frac{1}{T}M([F])
\coth\!\left(\frac{\beta[F]}{2}\right)
\delta(t-t').
\]

The source calls this a generalized fluctuation-dissipation relation for the one-process ideal interface.

In the linear regime,

\[
\bar J_n=-\frac{L}{T}[F],
\]

and

\[
\left\langle\xi(t)\xi(t')\right\rangle
=
\frac{2k_B L}{A}\delta(t-t').
\]

This is the direct source precedent for the R06 contact Onsager-FDT relation.

## 4. Ideal metal-semiconductor interface

For a nondegenerate semiconductor adjacent to a metal, the source obtains

\[
J_n
=
\frac{\lambda_{21}^{MS}}{N_C}
(n_m-n)+\xi,
\]

where

\[
n_m=N_C\exp(-q\beta\phi_{bn}).
\]

The covariance is

\[
\left\langle\xi(t)\xi(t')\right\rangle
=
\frac{1}{qA}
\left[-q\bar J_n+2I_s\right]
\delta(t-t'),
\]

under the paper’s current orientation, with

\[
I_s=q\lambda_{21}^{MS}\exp(-q\beta\phi_{bn}).
\]

After translating orientation, this is the familiar difference-versus-sum rule and yields thermal equilibrium noise when the net current vanishes and shot-noise scaling when one direction dominates.

The deterministic law is a thermionic-emission boundary. A simple Robin form is therefore a reduced special case of a barrier- and statistics-dependent interface law.

## 5. Nonideal interface with interface states

The source represents a nonideal interface by three independent activated exchange families:

\[
q_1\rightleftharpoons q_s,
\qquad
q_2\rightleftharpoons q_s,
\qquad
q_1\rightleftharpoons q_2.
\]

For each process,

\[
J_{ij}
=
\lambda_{ij}z_i-\lambda_{ji}z_j+\xi_{ij},
\]

with

\[
\left\langle\xi_{ij}(t)\xi_{ij}(t')\right\rangle
=
\frac{1}{A}
\left(
\lambda_{ij}z_i+\lambda_{ji}z_j
\right)
\delta(t-t').
\]

The elementary process noises are assumed independent. The observable interface currents are linear combinations of the same primitive event channels.

Two independent composite random currents are introduced:

\[
\xi_n=\xi_{12}+\xi_{s2},
\qquad
\xi_s=\xi_{s1}+\xi_{s2}.
\]

The paper derives nonzero cross covariance

\[
\left\langle\xi_n(t)\xi_s(t')\right\rangle
=
\frac{1}{A}
\left(
\lambda_{s2}z_s+\lambda_{2s}z_2
\right)
\delta(t-t').
\]

The cross term exists because the same `s <-> 2` elementary exchange event contributes to both composite currents.

### R06 consequence

This directly establishes the rule that state sources, interface-state currents, and terminal feed-through must be assembled from a shared primitive-event stoichiometry. Independent effective sources would double count events and omit mandatory cross covariance.

## 6. Interface-state strength and ideal limit

For the metal-semiconductor specialization, the paper’s stationary covariance expressions show that interface-state corrections scale with a ratio of interface-state exchange to net direct exchange, written using `lambda_2s/lambda_R`.

As this ratio tends to zero:

- the interface-state current variance vanishes;
- the interface/free-carrier cross covariance vanishes;
- the ideal metal-semiconductor result is recovered.

This provides a controlled hierarchy for R06:

1. ideal direct exchange;
2. explicit interface-state exchange;
3. reduced effective boundary after eliminating the interface state.

## 7. PSD and normalization convention

The source specifies delta-correlated time-domain covariances. It does not consistently state a modern one-sided/two-sided spectral convention in the equations audited.

R06 must therefore convert from the time-domain covariance definition rather than copy spectral prefactors directly.

## 8. What is established prior art

R06 cannot claim novelty for:

- stochastic semiconductor-interface boundary conditions;
- forward-minus-reverse mean flux and forward-plus-reverse covariance;
- nonlinear interface fluctuation relations;
- equilibrium Onsager-FDT recovery;
- ideal metal-semiconductor exchange noise;
- explicit interface-state stochastic currents;
- cross covariance generated by shared interface-state events;
- reduction from a multi-process nonideal interface to an ideal-interface limit.

## 9. Remaining R06 contribution

The defensible project target is no longer a new stochastic contact covariance. It is a verified reduction and error study:

> Quantify when established interface-event theory may be reduced to a deterministic finite-velocity boundary in a bipolar HgCdTe photoconductor without materially corrupting terminal noise, responsivity, bandwidth, or inferred lifetime.

Potential new outputs remain:

- dimensionless reduction-error boundaries;
- a bipolar electron-hole-interface-state implementation coupled to Poisson electrostatics;
- controlled elimination of fast interface states;
- uncertainty-qualified HgCdTe regime maps;
- comparison of direct exchange, pair recombination, and interface-state mediation.

## 10. Mandatory benchmarks

1. For one ideal process, recover mean difference and covariance sum exactly.
2. Recover the linear-response covariance `2 k_B L/A` in the source convention.
3. Recover the metal-semiconductor saturation-current covariance.
4. For three nonideal processes, construct the full covariance by stoichiometric assembly and reproduce the nonzero composite cross term.
5. Recover the ideal-interface limit as interface-state coupling tends to zero.
6. Verify positive semidefiniteness of the complete interface covariance matrix.

## 11. Limitations relative to R06

- unipolar carrier treatment;
- interface-local theory rather than a complete finite HgCdTe photoconductor solution;
- no bipolar electron-hole surface recombination channel;
- no optical generation;
- no self-consistent full-device terminal PSD in the same paper;
- no uncertainty-qualified HgCdTe parameterization;
- no quantitative criterion for replacing the interface model by a single deterministic `S`.