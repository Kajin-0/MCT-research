# Insight 0022: a scalar gap requires spectral resolution

## Statement

Near the HgCdTe normal-to-inverted transition, the magnitude of a mean signed gap must be compared with the spectral widths of the participating $\Gamma_6$ and $\Gamma_8$ states.

A scalar $E_g(x,T)$ is operationally incomplete when the edge spectra overlap strongly.

## Complex quasiparticle edges

Let the relevant disorder- and interaction-renormalized poles at $\Gamma$ be

$$
z_6=E_6-i\eta_6,
\qquad
z_8=E_8-i\eta_8,
$$

where $\eta_n\ge0$ is the spectral half-width under a declared convention.

The disorder-averaged signed gap is

$$
\bar E_g=E_6-E_8.
$$

Define the dimensionless spectral-resolution ratio

$$
\boxed{
\mathcal R_g
=
\frac{|\bar E_g|}{\eta_6+\eta_8}
}.
$$

This is an operational resolution diagnostic, not a topological invariant.

## Interpretation

- $\mathcal R_g\gg1$: two edge features are spectrally well separated; a scalar signed gap is a useful leading descriptor.
- $\mathcal R_g\sim1$: the edges overlap; extracted gap values become method and lineshape dependent.
- $\mathcal R_g<1$: a single sharp gap is not a sufficient description of the spectrum.

Thresholds such as $\mathcal R_g>3$ may be adopted as conservative reporting criteria, but they are conventions that must be validated against the actual spectral lineshape and experimental resolution.

## Why mean-gap sign is insufficient

Disorder can produce both a real self-energy shift and an imaginary broadening:

$$
\Sigma_{\mathrm{dis}}
=
\operatorname{Re}\Sigma_{\mathrm{dis}}
+i\operatorname{Im}\Sigma_{\mathrm{dis}}.
$$

The real part may change the effective Kane mass or signed gap, while the imaginary part broadens the edge states and can fill the density-of-states gap.

Consequently, two statements are distinct:

1. the effective-medium mass parameter has a particular sign;
2. the measured spectrum has a resolved hard gap with that sign.

The 2022 SCBA HgCdTe work already demonstrates disorder-renormalized mass and density-of-states evolution. A new analytical model must not collapse those two outputs back into one number.

## Distinct gap concepts

The following must remain separate:

- **mean signed Kane gap:** $E_{\Gamma_6}-E_{\Gamma_8}$ from the real effective Hamiltonian;
- **spectral peak separation:** separation of maxima in $A(\mathbf k,\omega)$;
- **density-of-states gap:** interval of vanishing or sufficiently small DOS;
- **mobility gap:** interval without extended states;
- **optical edge:** criterion extracted from absorption, excitonic fitting, or a fixed absorption coefficient;
- **transport activation gap:** scale inferred from carrier transport.

They can differ in a disordered narrow-gap alloy.

## Joint electron-phonon and disorder problem

At finite temperature,

$$
G^{-1}(\mathbf k,\omega,T)
=
\omega-H_0(\mathbf k)
-\Sigma_{\mathrm{ep}}(\mathbf k,\omega,T)
-\Sigma_{\mathrm{dis}}(\mathbf k,\omega,T)
-\cdots.
$$

The contributions need not be simply additive after self-consistency, and their imaginary parts need not obey a naive Matthiessen rule near degeneracy.

The breadth-first analytical target should therefore be

$$
\boxed{
\bar E_g(x,T),
\quad
\eta_6(x,T),
\quad
\eta_8(x,T),
\quad
\mathcal R_g(x,T)
}
$$

before attempting a full temperature-dependent disorder calculation.

## Model-selection consequence

A proposed improvement of the mean gap by $\delta E_g$ is not physically distinguishable if

$$
|\delta E_g|
\ll
\eta_6+\eta_8
$$

or if it is below the experimental edge-definition and composition uncertainty.

This creates a direct stop rule:

> Do not spend large computational resources refining the mean gap below the spectral-width floor of the relevant specimen and observable.

## Topological caution

$\mathcal R_g$ does not classify a disordered topological phase. That requires an appropriate Green-function, scattering, real-space, or mobility-gap invariant.

The role of $\mathcal R_g$ is narrower: determine whether a sharp scalar-gap equation is an adequate observable-level compression.
