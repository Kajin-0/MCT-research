# Iverson and Smith (1985) equation-level audit

**Source:** A. Evan Iverson and D. L. Smith, “Theory of deep level trap effects on generation-recombination noise in HgCdTe photoconductors,” *Journal of Applied Physics* **58**, 579–587 (1985).  
**DOI:** `10.1063/1.335666`  
**Verification status:** user-supplied publisher PDF inspected in full; state equations, trap rates, Green functions, instantaneous covariance, spectral convention, noise decomposition, and HgCdTe parameter study verified.

## 1. Model actually treated

The paper studies a one-dimensional, low-level-excitation intrinsic photoconductor with an n-type majority population and a deep center having two accessible charge states. The numerical specialization is `x = 0.21` HgCdTe.

The detector length is `2L`, with ohmic contacts at `x=+-L`. All excess populations vanish at both contacts.

The theory is not a full drift-diffusion-Poisson model. It imposes quasineutrality,

\[
\Delta p+\Delta N^+=\Delta n,
\]

where `N+` is the positively charged deep-level population under the paper's charge-state convention.

The paper assumes:

- small photogenerated density relative to the equilibrium majority density;
- equilibrium electron density much greater than the charged deep-level population;
- one-dimensional transport;
- ohmic contacts;
- explicit deep-level population dynamics;
- ambipolar drift and diffusion after quasineutral reduction;
- constant-current terminal voltage noise;
- field-dependent sweepout;
- frequency-domain Green functions.

## 2. Spectral and terminal conventions

The paper uses

\[
G(V,\omega)=4\int_0^\infty
\cos(\omega t)
\langle\Delta V(t)\Delta V(0)\rangle dt
\]

and

\[
V_N=[G(V,\omega)\Delta f]^{1/2}.
\]

The factor `4` and bandwidth `Delta f` indicate the paper's engineering one-sided convention, although the independent variable is angular frequency. R06 must translate the normalization explicitly.

Under constant current, Eq. (5) relates terminal voltage to spatial integrals of electron and hole fluctuations. Because all excess densities vanish at the ohmic contacts, diffusion boundary terms drop out.

## 3. Microscopic deep-level rates

The electron and hole current densities are Eqs. (8a)-(8b). The deep-level transition rates are Eqs. (9a)-(9d):

\[
r_e=B_enN^+,
\]

\[
r_h=B_hp(N_T-N^+),
\]

\[
g_h=B_hp_1N^+,
\]

\[
g_e=B_en_1(N_T-N^+),
\]

with

\[
B_e=\langle v_e\rangle\sigma_e,
\qquad
B_h=\langle v_h\rangle\sigma_h.
\]

These are the same four Shockley-Read capture/emission channels written for the paper's `N^0/N^+` convention.

## 4. Dynamic state and operator structure

After applying quasineutrality, the coupled state can be represented by the free-electron fluctuation and charged-center fluctuation. Eqs. (10a)-(10f) define coupled operators containing:

- time derivatives;
- band-to-band lifetime;
- deep-level capture and emission rates;
- field-driven first derivatives;
- ambipolar second derivatives;
- coupling between free and bound populations.

Green functions are defined by Eqs. (11a)-(11d). The relevant frequency-domain transform uses

\[
\widetilde K_i(x,x',\omega)
=\int_0^\infty e^{-i\omega t}K_i(x,x',t)dt.
\]

The transform sign differs from the R06 internal convention and must be translated.

## 5. Instantaneous population covariance

The full PDF resolves an important item left open in the first audit. Under the paper's n-type, low-level assumptions, Eqs. (30a)-(30d) give the zero-time correlations:

\[
\langle\Delta n(x,0)\Delta n(x',0)\rangle
=
\frac{\mathcal N^+(x)+p(x)}{Wd}
\delta(x-x'),
\]

\[
\langle\Delta N^+(x,0)\Delta n(x',0)\rangle
=
\frac{\mathcal N^+(x)}{Wd}
\delta(x-x'),
\]

\[
\langle\Delta n(x,0)\Delta p(x',0)\rangle
=
\frac{p(x)}{Wd}
\delta(x-x'),
\]

\[
\langle\Delta N^+(x,0)\Delta p(x',0)\rangle=0.
\]

Here

\[
\mathcal N^+(x)
=N^+(x)\left(1-\frac{N^+(x)}{N_T}\right)
\approx N^+(x)
\]

when `N+(x) << N_T`.

These equations show explicitly that free-electron and trap-population fluctuations are correlated. The paper uses a zero-time population-covariance representation, not a primitive white event-source matrix.

R06 must demonstrate that the event-level four-channel covariance reproduces these equilibrium population correlations after solving the associated Lyapunov/equilibrium covariance problem in the same reduced limit.

## 6. Noise decomposition

Equation (32) and the main text separate three terminal voltage-noise components:

1. band-to-band thermal GR noise;
2. background-photon generation noise;
3. thermal bound/free trap-exchange noise.

The components are added quadratically in the reported detector-noise calculation.

The deep level therefore does more than modify an effective lifetime. It adds a distinct stochastic population channel and modifies the transport response.

## 7. Trap-modified transport and rolloff

The paper shows that minority-carrier trapping changes effective mobility and diffusivity. Strong trapping reduces sweepout and lowers the rolloff frequency.

Consequently:

- the terminal corner is not generally one bare SRH lifetime;
- trap population, mobility reduction, diffusion, and contact sweepout jointly set the observed response;
- multiple physical noise components can roll off in approximately the same frequency range without being one microscopic process.

## 8. Verified HgCdTe specialization

The paper evaluates n-type `x=0.21` HgCdTe using a commonly observed deep center with approximate values:

- trap energy near `0.4 E_g` above the valence band;
- electron capture cross section near `1e-15 cm^2`;
- hole capture cross section near `1e-17 cm^2`;
- trap densities approximately `1e14-1e16 cm^-3`.

For the selected `T=77 K`, `E=40 V/cm`, and background flux near `1e17 photons/(cm^2 s)`, performance begins to degrade materially when trap density approaches or exceeds `1e16 cm^-3`.

The authors also reverse the capture-cross-section hierarchy as an exploratory case to demonstrate strong minority trapping. That case is not presented as measured HgCdTe behavior.

## 9. Established prior art

The following cannot be claimed as new:

- explicit dynamic deep-level populations in HgCdTe photoconductor GR-noise theory;
- four-channel capture/emission kinetics in the detector model;
- correlated free-carrier and trap population fluctuations;
- a bound/free thermal-noise component distinct from band-to-band GR noise;
- trap-modified mobility, diffusivity, and sweepout;
- Green-function frequency-domain finite-device noise;
- failure of one bare lifetime to control the measured rolloff.

## 10. Limitations relative to R06

- quasineutral ambipolar reduction;
- no self-consistent Poisson equation;
- ohmic absorbing contacts only;
- constant-current voltage-noise ensemble;
- zero-time population covariance rather than a full primitive source covariance;
- no finite stochastic contact exchange;
- no external circuit beyond ideal current bias;
- low-level n-type assumptions;
- selected material parameters and one trap family.

## 11. Mandatory benchmark

A reduced R06 implementation must impose:

- strong screening;
- low-level n-type excitation;
- one two-state trap;
- ohmic contacts;
- ambipolar transport;
- constant-current voltage observation;

and recover:

1. the coupled operator structure of Eqs. (10)-(11);
2. the population covariance of Eqs. (30a)-(30d);
3. separate band-to-band, background, and trap-exchange contributions;
4. the change in rolloff with trap-modified mobility/diffusion;
5. the reported weak-versus-strong minority-trapping trends.

## 12. Novelty consequence

Dynamic traps and trap-generated thermal noise in HgCdTe were already treated in 1985. A defensible R06 contribution must concern the controlled error of the quasineutral/ohmic reduction, stochastic finite contacts, self-consistent space charge, circuit loading, or a quantitative regime boundary unavailable in this prior theory.