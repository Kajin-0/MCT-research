# R06 Phase 1A equation-level prior-art audit

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Date:** 2026-07-23  
**Status:** intermediate source audit; Phase 1A remains open

## 1. Scope of this increment

This audit deepens three of the six initially prioritized sources and adds a foundational Smith paper that had not been included in the first matrix:

1. Bonani and Ghione (1999): bipolar fundamental population sources versus reduced equivalent-current sources;
2. Bulashenko et al. (1998): analytical impedance-field propagation and equilibrium Nyquist consistency;
3. Iverson and Smith (1985): explicit deep-level dynamics in HgCdTe photoconductors;
4. Smith (1982): foundational finite intrinsic-photoconductor GR-noise theory, identified but not yet acquired in full text.

It also derives the reduced dimensionless control set and establishes a benchmark ladder.

## 2. Source-level conclusions

### 2.1 Bonani and Ghione (1999)

**DOI:** `10.1016/S0038-1101(98)00253-6`

The source compares a fundamental bipolar population-fluctuation model against approximate equivalent-current-density sources. The fundamental model uses electron, hole, and trap population Langevin sources and propagates them through a device drift-diffusion/impedance-field response.

The source establishes that:

- primitive GR population noise is tied to forward-plus-reverse transition activity rather than net recombination;
- direct pair processes correlate electron and hole populations;
- trap-assisted processes require coupled electron, hole, and trap fluctuations;
- homogeneous equivalent-current sources can fail near contacts;
- monopolar reductions can fail even in doped samples when minority-carrier weighting fields matter;
- empirical lifetime or source corrections may conceal a structural reduction error.

**R06 consequence:** the population/event-source formulation is the reference model. Equivalent-current and monopolar formulations are reduced models to be benchmarked, not co-enabled source terms.

### 2.2 Bulashenko et al. (1998)

**DOI:** `10.1063/1.367023`

The source derives an analytical impedance-field method for a nonuniform one-dimensional semiconductor junction with drift and diffusion. Distributed local fluctuations are mapped to a terminal voltage through a spatial transfer field.

The source establishes that:

- terminal-noise propagation by an impedance/adjoint field is established methodology;
- nonuniform field and carrier profiles can localize terminal sensitivity strongly near a junction;
- field/source cross correlations can be required for equilibrium Nyquist consistency;
- local source strength is not the same as local contribution to the terminal PSD;
- direct and adjoint terminal-noise solvers provide a natural independent-method pair.

**R06 consequence:** software architecture, Green functions, and adjoint weighting are not novelty. R06 must use the impedance-field method as an independent verification route for selected cases.

### 2.3 Iverson and Smith (1985)

**DOI:** `10.1063/1.335666`

The source treats a one-dimensional, low-level n-type HgCdTe photoconductor with a two-charge-state deep center. It imposes quasineutrality, reduces transport to coupled free-carrier and trap-population dynamics, includes ambipolar drift/diffusion and sweepout, and solves by frequency-domain Green functions.

The source establishes that:

- dynamic deep-level populations in HgCdTe GR-noise theory are established;
- deep traps introduce a distinct bound/free exchange-noise contribution;
- trap occupancy modifies effective lifetime, mobility, diffusivity, and sweepout;
- the terminal spectral corner need not equal one bare microscopic lifetime;
- a strong-screening, quasineutral trap model is an essential HgCdTe benchmark.

**R06 consequence:** explicit traps and trap-induced multimode behavior are not novelty. The potential contribution is the controlled error of the quasineutral/ohmic reduction, finite stochastic contacts, self-consistent space charge, or new dimensionless bounds.

### 2.4 Smith (1982)

**Citation:** D. L. Smith, “Theory of generation-recombination noise in intrinsic photoconductors,” *Journal of Applied Physics* **53**, 7051–7060 (1982).

The bibliographic record and abstract identify this as a foundational finite intrinsic-photoconductor theory involving drift, diffusion, sweepout, contact-region recombination, spatial correlation between fluctuation probability and lifetime, and a numerical HgCdTe specialization.

The DOI and full equation set remain unresolved in this audit.

**R06 consequence:** Smith 1982 must be acquired before claiming that the analytical lineage from classical intrinsic-photoconductor noise to Smith 1984 and Iverson-Smith 1985 has been reconstructed.

## 3. Revised novelty exclusions

The following are now explicitly excluded as novelty bases:

1. finite one-dimensional semiconductor noise;
2. drift-plus-diffusion noise propagation;
3. Poisson or long-range Coulomb modification of GR noise;
4. bipolar electron-hole-trap population sources;
5. dynamic deep traps in HgCdTe photoconductors;
6. field-dependent trap-modified sweepout;
7. Green-function or impedance-field terminal transfer;
8. equivalent-current versus population-source comparisons;
9. boundary-induced failure of homogeneous or monopolar reductions;
10. contact-controlled modification of HgCdTe responsivity and noise in principle.

## 4. Candidate contribution after this audit

A defensible R06 contribution must be stated as a quantitative result rather than a list of included equations. Candidate outputs are:

1. a thermodynamically complete stochastic finite-contact boundary with demonstrated equilibrium FDT recovery and blocking/reservoir limits;
2. an asymptotic or numerical error bound for reducing bipolar drift-diffusion-Poisson-trap dynamics to a quasineutral ambipolar HgCdTe model;
3. a dimensionless inequality defining when a fitted terminal corner misestimates a microscopic trap or recombination time by more than a specified tolerance;
4. an HgCdTe regime map separating screening, diffusion, sweepout, trap, contact, and circuit poles with uncertainty-qualified boundaries;
5. a proof or counterexample establishing the bandwidth over which a finite set of spatial modes can mimic `1/f^alpha` behavior.

These remain hypotheses until the remaining high-overlap papers are audited.

## 5. Dimensionless result

For the isothermal nondegenerate baseline, choose

\[
\Pi_D=\frac{L}{\sqrt{D_r\tau_r}},
\qquad
\Lambda=\frac{L}{L_{D,r}},
\qquad
U=\frac{qV_b}{k_BT}.
\]

Then, under the same Einstein closure,

\[
\frac{\tau_r}{t_{\mathrm{tr}}}=\frac{U}{\Pi_D^2},
\]

and for a unipolar reference conductivity,

\[
\frac{\tau_r}{\tau_{\mathrm{dr}}}=\frac{\Lambda^2}{\Pi_D^2}.
\]

Thus normalized field/voltage, transit time, dielectric relaxation time, diffusion length, and Debye length are not all independent sweep coordinates.

Finite contacts require separate electron/hole and left/right Biot numbers,

\[
\mathrm{Bi}_{s,c}=\frac{S_{s,c}L}{D_s},
\]

plus forward and reverse stochastic exchange intensities. The deterministic Biot number alone cannot specify contact noise.

The complete derivation is in `docs/derivations/stochastic_transport_noise/dimensionless_reduction.md`.

## 6. Benchmark decision

The benchmark sequence is now:

- B0: algebraic sign and PSD normalization;
- B1: equilibrium resistor and FDT;
- B2: Gomila-Reggiani finite-size unipolar limit;
- B3: Iverson-Smith quasineutral dynamic-trap HgCdTe limit;
- B4: Bonani-Ghione population versus reduced-source comparison;
- B5: Bulashenko direct-resolvent versus adjoint/impedance-field comparison;
- B6: finite stochastic contact limits after Park and Smith full-text audits;
- B7: conventional bulk Lorentzian;
- B8: finite-mode apparent spectral slope;
- B9: HgCdTe parameter and uncertainty sensitivity.

The complete acceptance specification is in `benchmarks/transport_noise/phase1a_benchmark_spec.md`.

## 7. Remaining critical source audits

### Zocchi (2006)

DOI `10.1103/PhysRevB.73.035203`.

Required to determine whether the full coupled finite-length carrier/trap/Poisson/terminal-spectrum problem already includes substantially all of the proposed R06 state and observation structure.

### Park (2022)

DOI `10.1063/5.0111954`.

Required to determine whether finite surface recombination velocity was implemented only as a deterministic boundary or with a thermodynamically consistent stochastic contact source.

### Smith (1984)

DOI `10.1063/1.334155`.

Required to reconstruct the blocking-contact and responsivity/noise limit for intrinsic photoconductors and HgCdTe.

### Smith (1982)

DOI unresolved.

Required to reconstruct the foundational finite intrinsic-photoconductor model used by later HgCdTe work.

## 8. Confidence update

| Finding | Confidence | Remaining uncertainty |
|---|---:|---|
| Bipolar population-source GR theory is established | High | Exact normalization and coefficients still require clean transcription |
| Dynamic trap populations in HgCdTe noise are established | High | Exact source cross-covariance and boundary conditions remain to transcribe |
| Impedance-field terminal-noise propagation is established | High | Exact mapping to fixed-voltage current ensemble remains to derive |
| Quasineutral reduction can alter inferred lifetime/corner | High qualitatively | Quantitative error boundary not yet established |
| Finite stochastic contact exchange may remain a gap | Low-to-medium | Park and Smith equation audits are still missing |
| Dimensionless error map may be publishable | Medium as a useful result; low on novelty | Adjacent analytical literature remains incomplete |

## 9. Gate status

Phase 1A continues. Production simulation remains unauthorized.

Completed in this increment:

- three high-overlap equation-level source audits advanced;
- source-specific notes committed;
- Smith 1982 added to the acquisition queue;
- reduced dimensionless parameter set derived;
- benchmark ladder and preliminary numerical tolerances specified;
- original branch CI verified successful before this increment.

Still required:

1. Zocchi, Park, Smith 1984, and Smith 1982 source acquisition and audit;
2. exact stochastic contact covariance;
3. generalized Einstein/degeneracy decision for the HgCdTe baseline;
4. final Phase 1 novelty or synthesis decision;
5. updated clean-environment checks for the final branch head.