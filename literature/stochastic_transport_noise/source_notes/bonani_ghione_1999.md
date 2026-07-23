# Bonani and Ghione (1999) source audit

**Source:** F. Bonani and G. Ghione, “Generation-recombination noise modelling in semiconductor devices through population or approximate equivalent current density fluctuations,” *Solid-State Electronics* **43**, 285–295 (1999).  
**DOI:** `10.1016/S0038-1101(98)00253-6`  
**Verification status:** publisher article text, section structure, model comparison, and conclusions inspected; complete coefficient-level equation transcription remains pending.

## Question answered by the paper

The paper compares two GR-noise representations inside a device-level drift-diffusion framework:

1. **Fundamental population-source formulation:** zero-mean Langevin population sources are inserted directly into the electron, hole, and trap continuity equations.
2. **Approximate equivalent-current formulation:** homogeneous-system population noise is converted into an effective current-density source, often after a monopolar reduction.

The fundamental formulation is treated as the reference.

## Physical model

The reported reference calculation uses:

- bipolar electron and hole drift-diffusion transport;
- open-circuit voltage-noise evaluation through an impedance-field/Green-function method;
- finite uniformly doped semiconductor samples;
- ohmic contacts;
- direct and trap-assisted GR processes;
- explicit trap occupation for SRH transitions;
- boundary-sensitive numerical device solutions.

## Source-covariance result

The paper states that fundamental GR population sources are white at the primitive level and have amplitudes proportional to the sum of the corresponding generation and recombination transition rates.

This supports the R06 event-level rule

\[
Q=\sum_r \nu_r\nu_r^T a_r,
\]

rather than assigning noise intensity from the net recombination residual.

For direct pair processes, electron and hole population fluctuations are correlated. For trap-assisted processes, the trap occupation source couples to both carrier populations through the transition stoichiometry.

## Boundary and minority-carrier result

The paper finds that approximate equivalent-current sources derived under homogeneous conditions become inaccurate when ohmic boundary effects are not negligible. It further finds that the monopolar approximation can fail even in doped material because minority-carrier impedance fields remain relevant.

The equivalent and monopolar approaches reproduce the fundamental result only after empirical field- and geometry-dependent corrections to lifetime or fluctuation spectra.

## Consequences for R06

### Established prior art

R06 cannot claim novelty for:

- bipolar Langevin drift-diffusion GR-noise modelling;
- explicit electron, hole, and trap population sources;
- propagation of distributed population sources to a terminal voltage through an impedance field;
- demonstrating that equivalent-current or monopolar noise models fail near boundaries or when minority carriers contribute;
- correcting reduced noise models with geometry- and field-dependent effective parameters.

### Required modelling rule

The initial stochastic solver should use population/reaction sources as the reference implementation. An equivalent-current representation may be added only as a derived approximation and must be benchmarked against the population-source result.

### Required benchmark

For a uniformly doped finite sample with ohmic contacts, R06 should compare:

1. full bipolar population-source noise;
2. bipolar equivalent-current noise;
3. monopolar equivalent-current noise.

The discrepancy should be mapped against normalized field, sample length relative to minority diffusion length, and frequency.

## No-double-counting implication

The paper reinforces that an equivalent current source already contains part of the carrier-response dynamics. Combining it with the original population source would double count the same microscopic transition.

R06 should therefore keep two mutually exclusive source backends:

- primitive population/event sources;
- a separately tested reduced equivalent-current model.

They must never be enabled simultaneously for the same process.

## Unresolved items

1. Transcribe the exact direct and SRH source cross-spectral matrices.
2. Record the paper’s PSD normalization and transform convention.
3. Extract the exact ohmic boundary conditions for fluctuation variables.
4. Quantify the published discrepancy curves for later benchmark tolerances.
5. Determine whether the paper’s multidimensional implementation includes displacement current explicitly in the terminal observable or uses an equivalent open-circuit weighting formulation.

## Novelty consequence

The general claim “bipolar spatially resolved GR noise differs from a lumped Lorentzian” is already occupied. R06 must instead produce a precise new output such as a controlled reduction error, a thermodynamically complete finite-contact covariance, or an HgCdTe-specific regime boundary unavailable from the existing bipolar ohmic-contact theory.