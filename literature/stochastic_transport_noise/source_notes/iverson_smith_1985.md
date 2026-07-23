# Iverson and Smith (1985) equation-level audit

**Source:** A. Evan Iverson and D. L. Smith, “Theory of deep level trap effects on generation-recombination noise in HgCdTe photoconductors,” *Journal of Applied Physics* **58**, 579–587 (1985).  
**DOI:** `10.1063/1.335666`  
**Verification status:** full text inspected from an accessible article copy; covariance normalization and every appendix coefficient still require line-by-line transcription before implementation.

## Model actually treated

The paper studies a one-dimensional, low-level-excitation intrinsic photoconductor with an n-type majority population and a deep center having two charge states. The numerical specialization is approximately `x = 0.21` HgCdTe.

The theory is not a full drift-diffusion-Poisson model. It imposes quasineutrality in the form

\[
\Delta p+\Delta N^+=\Delta n,
\]

where `N+` is the occupied/charged deep-level population under the paper’s charge-state convention. This eliminates one free-carrier fluctuation before the transport problem is solved.

The paper assumes:

- small photogenerated density relative to the equilibrium majority density;
- one-dimensional transport over a detector of length `2L`;
- ohmic contacts;
- ambipolar mobility and diffusivity after quasineutral reduction;
- explicit deep-level population dynamics;
- field-dependent sweepout;
- a Green-function frequency-domain solution.

## Dynamic state and operator structure

After using quasineutrality, the coupled fluctuation state can be represented by a free-carrier fluctuation and a deep-center population fluctuation. The paper writes coupled differential operators, shown in its Eqs. (10a–f), containing:

- time derivatives;
- recombination/capture coefficients;
- field-driven first spatial derivatives;
- ambipolar second spatial derivatives;
- coupling between free and bound populations.

Green functions are then defined by the coupled operator equations in Eqs. (11a–b). The frequency-domain Green functions are introduced by a one-sided time transform in Eq. (15),

\[
\widetilde K_i(x,x',\omega)=\int_0^\infty e^{-i\omega t}K_i(x,x',t)\,dt.
\]

The sign convention differs from the R06 internal transform and must be translated rather than copied.

## Noise decomposition

The resulting voltage-noise calculation separates three physical components:

1. band-to-band thermal generation-recombination noise;
2. background-photon generation noise;
3. a distinct trap exchange noise associated with fluctuations between bound and free populations.

The third term is important for R06 because it demonstrates that a deep level does more than modify an effective lifetime. It introduces an additional stochastic population channel.

The paper reports that minority-carrier trapping can reduce the effective mobility and diffusivity and thereby weaken sweepout. Consequently, the measured corner or rolloff cannot generally be identified with a bare microscopic SRH lifetime.

## Verified numerical specialization

The paper evaluates approximately `x = 0.21`, n-type HgCdTe and uses a deep center motivated by measured capture parameters. It explores deep-level densities from roughly `10^14` to `10^16 cm^-3`. Its reported detector degradation becomes substantial near the upper part of that range for the selected operating conditions.

These are specimen/model-conditioned values, not universal HgCdTe parameters.

## Direct implications for R06

### Established prior art

The following cannot be claimed as new:

- explicit deep-level population dynamics in HgCdTe photoconductor GR-noise theory;
- a bound/free-carrier stochastic contribution distinct from ordinary band-to-band GR noise;
- field-dependent sweepout coupled to trap-modified mobility and diffusion;
- Green-function frequency-domain evaluation of finite photoconductor noise;
- failure of a single bare lifetime to control all observed rolloff behavior.

### Remaining distinction

The paper does not remove the R06 target because it uses quasineutral ambipolar reduction and ohmic contacts rather than self-consistent bipolar drift-diffusion-Poisson dynamics with finite stochastic contact exchange.

R06 must reproduce the quasineutral limit of this model before claiming a more general result.

## Mandatory benchmark extracted from this source

A reduced R06 implementation should be able to impose:

- strong screening;
- low-level n-type excitation;
- a single two-state trap;
- ohmic end contacts;
- ambipolar transport;

and recover a two-population modal structure with separate band-to-band and trap-exchange source contributions.

Exact numerical equality is not yet required because the article’s complete source normalization and parameter conventions have not been transcribed. The initial benchmark is structural: pole count, source decomposition, sweepout trend, and limiting behavior.

## Unresolved items

1. Transcribe the paper’s primitive fluctuation correlation functions and units.
2. Reconcile its charge-state notation with the R06 trap occupancy variable.
3. Determine whether the reported noise components are statistically independent or contain cross terms after the quasineutral elimination.
4. Derive the R06 strong-screening reduction and compare operator coefficients term by term.
5. Identify the exact ohmic fluctuation boundary conditions used by the Green functions.

## Novelty consequence

Any R06 novelty statement must explicitly acknowledge that dynamic trap populations and trap-generated thermal noise in HgCdTe photoconductors were already treated in 1985. A defensible contribution must concern the controlled error of quasineutral/ohmic reductions, stochastic finite contacts, self-consistent space charge, or experimentally interpretable dimensionless regime boundaries.