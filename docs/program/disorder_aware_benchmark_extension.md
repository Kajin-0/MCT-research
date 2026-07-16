# Disorder-aware extension to the analytical benchmark

## Purpose

The existing mean-gap benchmark compares functions for

$$
\bar E_g(x,T).
$$

Near inversion, that comparison is incomplete if alloy or quasiparticle width is comparable to the mean signed gap. This extension defines a staged benchmark without requiring immediate SQS, CPA, or SCBA production calculations.

## Model ladder

### D0: sharp mean-gap model

$$
E_g=\bar E_g(x,T).
$$

Examples: Hansen, Laurenti, constrained polynomial, one-oscillator and two-oscillator mean laws.

### D1: specimen-level composition uncertainty

$$
x_s^{\mathrm{true}}
\sim
p(x_s\mid x_s^{\mathrm{reported}},\sigma_{x,s}).
$$

All temperatures measured on the same specimen share the same latent composition. This models metrology uncertainty, not microscopic alloy disorder.

### D2: local gap distribution

$$
E_g^{\mathrm{local}}
\sim
\mathcal N
\left[
\bar E_g(x,T),
\sigma_g^2(x,T,L)
\right],
$$

where $L$ or an equivalent $N_{\mathrm{eff}}$ declares the coarse-graining scale.

The ideal uncorrelated-alloy baseline is

$$
\sigma_g
=
\left|\partial_x\bar E_g\right|
\sqrt{\frac{x(1-x)}{N_{\mathrm{eff}}}}.
$$

### D3: spectral self-energy model

$$
A(\mathbf k,\omega)
=-\frac{1}{\pi}
\operatorname{Im}
\operatorname{Tr}
\left[
\omega-H_0-\Sigma(\mathbf k,\omega)
\right]^{-1}.
$$

This level distinguishes real edge shifts, linewidths, band mixing, density-of-states filling, and non-Lorentzian lineshapes.

### D4: localization or mobility model

This level introduces real-space localization, mobility edges, or a topological invariant suitable for disorder. It is outside the first analytical-gap benchmark and should be activated only when the target observable requires it.

## Noninterchangeable width definitions

Every width datum must be labeled as one of:

- local composition standard deviation;
- local signed-gap standard deviation;
- quasiparticle spectral HWHM or FWHM;
- optical Urbach energy;
- fitted absorption-edge width;
- density-of-states pseudogap width;
- sample-to-sample variation;
- lateral or depth composition gradient.

Conversion among these quantities requires a declared physical model. No universal equality is assumed.

## Validation data hierarchy

1. **Independent composition maps:** SIMS, EDX/EPMA, XRD-calibrated composition, or another independently documented method.
2. **Fixed-specimen temperature spectra:** raw or calibrated absorption, reflectivity, ellipsometry, or magnetospectroscopy.
3. **Lineshape parameters:** linewidth, Urbach energy, edge width, or spectral peak separation with uncertainty.
4. **Spatial statistics:** variance and correlation length of composition or edge energy.
5. **Transport or localization evidence:** activation, mobility edge, or real-space conduction maps.

A paper reporting only one cutoff wavelength cannot identify D2 or D3.

## Metrics

### Mean prediction

- MAE and maximum error in meV;
- critical-composition and critical-temperature error;
- source- and measurement-class residual structure.

### Width prediction

- MAE or log-error of the declared width;
- coverage of measured edge or spectral intervals;
- calibration of predicted opposite-sign fraction when spatially resolved data exist;
- predictive likelihood of the full lineshape where raw spectra are available.

### Resolution metric

For HWHM edge widths $\eta_6$ and $\eta_8$,

$$
\mathcal R_g
=
\frac{|\bar E_g|}{\eta_6+\eta_8}.
$$

Report the fraction of the validation domain in which:

- $\mathcal R_g>3$;
- $1<\mathcal R_g\le3$;
- $\mathcal R_g\le1$.

These bins are operational reporting categories, not topological classifications.

## Cross-validation

Use the same group-aware splits as the mean benchmark:

- leave one composition/specimen out;
- held-out temperature windows;
- held-out source;
- held-out measurement class.

Width parameters must not be trained and tested on points extracted from the same fitted lineshape without specimen grouping.

## Model-selection rules

1. Do not fit D2 if no width or spatial-statistics evidence exists.
2. Do not fit D3 from scalar edge energies alone.
3. Prefer D0 or D1 when the width is bounded far below experimental error and model separation.
4. Prefer D2 when local composition or edge distributions are measured and a Gaussian or other simple distribution is adequate.
5. Require D3 when edge spectra overlap, lineshapes are nontrivial, or real and imaginary self-energy effects must be separated.
6. Activate D4 only for mobility, localization, or topological classification questions.

## Computation gate

SQS, CPA, or SCBA work is justified only if it can discriminate among D1--D3 at the target observable and accuracy.

The decision memo must specify:

- the width definition being predicted;
- the relevant spatial and energy resolution;
- the expected scale relative to $|\bar E_g|$;
- the smallest configuration ensemble or disorder model capable of resolving it;
- the experimental datum that will validate it;
- the result that terminates the disorder branch.

## Immediate evidence tasks

1. acquire primary HgCdTe optical band-tail papers;
2. locate specimen-level composition variance or correlation-length data;
3. extract edge linewidths from the prioritized Laurenti, Camassel, Seiler, Teppe, and related spectra when available;
4. determine whether reported broadening is homogeneous, inhomogeneous, excitonic, instrumental, or compositional;
5. compare the inferred width with the Hansen--Laurenti and nested eight-band model-separation scales.
