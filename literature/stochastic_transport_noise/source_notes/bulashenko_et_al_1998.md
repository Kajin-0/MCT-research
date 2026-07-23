# Bulashenko et al. (1998) source audit

**Source:** O. M. Bulashenko, G. Gomila, J. M. Rubí, and V. A. Kochelap, “Extension of the impedance field method to the noise analysis of a semiconductor junction: Analytical approach,” *Journal of Applied Physics* **83**, 2610–2618 (1998).  
**DOI:** `10.1063/1.367023`  
**Stable institutional record:** `hdl:2445/22078`  
**Verification status:** published full text inspected through an institutional repository and an accessible article copy.

## Scope

The paper derives an analytical impedance-field method for local and terminal noise in a one-dimensional semiconductor junction when both drift and diffusion contribute. The worked structure is an inhomogeneous `n+–n` homojunction with nonuniform electric field and carrier density.

It is not a GR-photoconductor theory. Its relevance is methodological: it supplies an independent terminal-noise transfer formulation and an equilibrium Nyquist check for a nonuniform drift-diffusion device.

## Deterministic structure

The method assumes that the stationary electric-field and carrier profiles are known. Linearization then produces a transfer or impedance field that maps distributed microscopic current fluctuations to terminal voltage fluctuations.

The formulation allows:

- drift and diffusion simultaneously;
- spatially nonuniform charge and field;
- field-dependent mobility and diffusion coefficients;
- junction/contact regions with strong gradients;
- local decomposition of terminal-noise contributions.

## Terminal transfer formulation

The central observable has the form

\[
\delta V(\omega)=\int Z(x,\omega)\,\delta j_s(x,\omega)\,dx,
\]

with the terminal spectrum obtained by weighting the local source covariance with the impedance field. The exact paper notation and normalization must be retained when the benchmark is implemented.

This is the continuous adjoint analogue of the R06 matrix expression

\[
H_I=c^T(i\omega M-J)^{-1}B+d^T.
\]

The source and observation operators differ, but both propagate distributed fluctuations to a terminal observable without evaluating a local current at an arbitrary interior point.

## Equilibrium verification

The paper explicitly compares the integrated local equilibrium noise with the Nyquist terminal result. It identifies cross terms associated with electric-field fluctuations near the junction/interface as necessary contributors to the equilibrium balance.

This is a critical warning for R06: a decomposition into apparently independent local conduction sources can miss terminal equilibrium noise if the field-mediated correlations or observation operator are simplified inconsistently.

## Spatial interpretation

The paper shows that local contributions to terminal noise can be strongly concentrated near an inhomogeneous junction and can contain positive and negative cross contributions. A map of “where the noise comes from” is therefore transfer-function dependent; it is not identical to a map of local source intensity.

R06 figures should distinguish:

1. primitive local source covariance;
2. transfer/adjoint weighting;
3. weighted local contribution to the terminal PSD;
4. cross-correlation contributions.

## Direct implications for R06

### Established prior art

R06 cannot claim novelty for:

- impedance-field propagation of distributed drift-diffusion noise;
- analytical terminal-noise evaluation in a nonuniform one-dimensional semiconductor;
- local source-contribution maps;
- field/source cross terms required by equilibrium Nyquist consistency;
- using a transfer field as an independent alternative to direct stochastic state solves.

### Required independent solver

The stochastic implementation should provide two terminal-noise evaluations for selected cases:

1. direct resolvent covariance propagation;
2. adjoint/impedance-field propagation.

Agreement should be checked over frequency, not only at zero frequency.

### Required equilibrium metric

Define

\[
\epsilon_{\mathrm{FDT}}(\omega)
=
\frac{|S_V^{\mathrm{model}}(\omega)-4k_BT\operatorname{Re}Z(\omega)|}
{4k_BT\operatorname{Re}Z(\omega)}.
\]

The permitted tolerance must be separated into spatial-discretization, linear-solver, and source-normalization contributions.

## Limitations relative to R06

- unipolar junction example;
- no optical generation;
- no explicit HgCdTe material physics;
- no full electron-hole-trap GR closure;
- contact regions are part of a junction profile rather than finite stochastic surface-recombination boundaries;
- hot-carrier source corrections are discussed but not a baseline for R06.

## Unresolved items

1. Transcribe the exact impedance-field differential equation and boundary conditions.
2. Extract the complete local source-correlation tensor used in the worked example.
3. Record the PSD bandwidth and one-/two-sided convention.
4. Reproduce one published equilibrium local-contribution profile as a benchmark.
5. Determine the exact relation between its voltage weighting field and the R06 fixed-voltage current weighting operator.

## Novelty consequence

A terminal transfer-function formulation is established methodology. R06 novelty, if any, must lie in the physical closure and controlled HgCdTe/contact reductions, not in using a Green function, impedance field, or adjoint to compute terminal noise.