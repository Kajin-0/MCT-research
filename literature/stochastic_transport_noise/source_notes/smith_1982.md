# Smith (1982) equation-level audit

**Source:** D. L. Smith, “Theory of generation-recombination noise in intrinsic photoconductors,” *Journal of Applied Physics* **53**, 7051–7060 (1982).  
**DOI:** `10.1063/1.330006`  
**Verification status:** user-supplied publisher PDF inspected in full; governing equations, covariance theorem, Green-function construction, terminal ensemble, asymptotes, and HgCdTe example verified.

## 1. Model and operating ensemble

The paper develops a one-dimensional, charge-neutral, ambipolar theory for an intrinsic photoconductor of length `2L`, width `W`, and thickness `d`. The worked numerical example is n-type `x approximately 0.21` HgCdTe at 77 K.

The terminal is operated at **constant current**, and the fluctuating observable is terminal voltage.

The excess minority and majority densities are assumed equal:

\[
\Delta n=\Delta p\equiv\Delta P.
\]

No Poisson equation is solved. The model is therefore the strong-screening/quasineutral reduction of the broader R06 system.

## 2. Ambipolar transport equation

The excess density obeys Eq. (1a):

\[
\left(
\partial_t+\tau^{-1}+\mu E\partial_x-D\partial_x^2
\right)\Delta P(x,t)=f(x,t),
\]

where `tau` is the bulk excess-carrier lifetime and `mu`, `D` are the ambipolar mobility and diffusivity.

The contacts are perfect recombination sinks:

\[
\Delta P(-L,t)=\Delta P(L,t)=0.
\]

Uniform background generation is represented by

\[
f=\eta Q_B/d.
\]

The time evolution of a fluctuation is obtained from the homogeneous transport equation with an initial fluctuation profile.

## 3. Terminal-voltage observable

The paper begins from the one-sided cosine form of the Wiener-Khinchin relation,

\[
G(V,\omega)=4\int_0^\infty
\cos(\omega t)
\langle\Delta V(t)\Delta V(0)\rangle dt,
\]

and defines noise amplitude in bandwidth `Delta f` by

\[
V_N=[G(V,\omega)\Delta f]^{1/2}.
\]

Although the spectrum is written as a function of angular frequency, the bandwidth is in hertz. R06 must not import numerical factors without translating this convention explicitly.

After integrating the current-density equation and using the absorbing contact conditions, Eq. (6) gives

\[
\Delta V(t)
=-\frac{V(b+1)}{p_0+bn_0}
\frac{1}{2L}
\int_{-L}^{L}\Delta P(x,t)dx,
\]

where `b=mu_n/mu_p`. Thus the terminal voltage is driven by the spatially averaged excess density under constant current.

## 4. Green-function formulation

The Green function is defined by Eqs. (20a)-(20c):

\[
\left(
\partial_t+\tau^{-1}+\mu E\partial_x-D\partial_x^2
\right)K(x,x',t)
=\delta(x-x')\delta(t),
\]

with

\[
K(\pm L,x',t)=K(x,\pm L,t)=0,
\qquad
K=0\quad(t<0).
\]

The carrier fluctuation evolves as

\[
\Delta P(x,t)=\int_{-L}^{L}K(x,x',t)\Delta P(x',0)dx'.
\]

The paper uses both direct Green functions and an adjoint symmetry

\[
K(x,x',t)=K(-x',-x,t)
\]

to interpret the spatial weighting of background fluctuations.

## 5. Instantaneous fluctuation covariance

The crucial covariance is not postulated as a lumped lifetime source. Using a theorem attributed to Van Vliet, Appendix II derives

\[
\langle
\Delta P(x'',0)\Delta P(x',0)
\rangle
=
\frac{p_0+P_B(x')}{Wd}
\delta(x''-x').
\]

The local fluctuation probability therefore follows the local mean minority population:

- `p_0` gives thermal equilibrium fluctuations;
- `P_B(x)` gives background-generated fluctuations.

This is a population-covariance representation rather than an explicit forward/reverse event covariance. It is a mandatory reduced benchmark, not the final R06 stochastic closure.

## 6. Thermal and background contributions

The terminal noise separates into two components that add in quadrature:

1. thermal GR noise proportional to `p_0`;
2. background GR noise proportional to the spatially averaged `P_B` and a correlation factor `F(omega)`.

The response function is

\[
\phi(\omega)=\operatorname{Re}Q(\omega),
\]

while `F(omega)` accounts for the spatial correlation between:

- where a background fluctuation is likely to occur;
- how long a fluctuation at that position survives before recombination or contact sweepout.

This is a direct prior-art example in which a terminal GR spectrum is not determined by one spatially averaged lifetime.

## 7. Spatial-correlation limits

At zero bias, the low-frequency correlation factor approaches:

- `F(0) -> 6/5` when the diffusion length exceeds the half-length;
- `F(0) -> 1` in the bulk-like long-device limit.

At high field,

\[
F(0)\rightarrow\frac{2}{3}.
\]

The sign of the spatial correlation changes physically:

- low bias: fluctuations are likely near the center, where survival is long;
- high bias: background density and survival weighting peak toward opposite ends.

The paper reports that this correlation can make detectivity exceed the conventional BLIP normalization by a finite model-dependent factor; it does not violate the underlying photon statistics because the conventional reduction omitted spatial weighting.

## 8. Frequency-domain departures from a Lorentzian

The paper finds:

- a low-frequency plateau;
- a field-dependent rolloff frequency;
- dips in the thermal component associated with drift response structure;
- diffusion removes exact zeros predicted by a drift-only model;
- high-frequency response factor `F(omega) proportional to omega^-1/2`;
- thermal voltage-noise amplitude `V_N proportional to omega^-3/4`;
- background voltage-noise amplitude `V_N proportional to omega^-1`.

Therefore the corresponding voltage PSD asymptotes are

\[
S_{V,\mathrm{thermal}}\propto\omega^{-3/2},
\qquad
S_{V,\mathrm{background}}\propto\omega^{-2}.
\]

Non-single-Lorentzian HgCdTe photoconductor spectra caused by drift, diffusion, absorbing contacts, and spatial source weighting were therefore established in 1982.

## 9. Assumptions and limitations

- quasineutral excess carriers;
- one ambipolar population rather than separate electron and hole dynamics;
- ideal high-recombination contacts;
- constant coefficients;
- one bulk lifetime;
- no explicit trap state;
- no Poisson screening or displacement-current mode;
- no contact stochastic source;
- constant-current voltage-noise ensemble;
- local covariance based on population statistics, not primitive event propensities.

## 10. Required R06 benchmark

R06 must recover this model by imposing:

1. strong screening and low-level injection;
2. ambipolar reduction;
3. absorbing contacts;
4. uniform background generation;
5. constant-current terminal observation;
6. one bulk lifetime;
7. the Smith instantaneous covariance.

Required quantitative checks include:

- the exact Green-function boundary problem;
- `F(0)` limits `6/5`, `1`, and `2/3`;
- removal of drift-only spectral zeros by diffusion;
- high-frequency PSD slopes `-3/2` and `-2` for thermal and background components.

## 11. Novelty consequence

The following are not new:

- finite HgCdTe photoconductor GR noise with both drift and diffusion;
- absorbing-contact sweepout;
- spatial correlation between fluctuation probability and survival time;
- field-dependent terminal rolloff not equal to one bulk lifetime;
- non-Lorentzian high-frequency asymptotes;
- separate thermal and optical-background noise components.

A defensible R06 result must quantify the error introduced by Smith's quasineutral, one-population, absorbing-contact reduction when space charge, bipolar transport, dynamic traps, stochastic finite contacts, or external loading are restored.