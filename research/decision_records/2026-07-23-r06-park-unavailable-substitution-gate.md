# R06 Park-unavailable substitution gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Issues:** #341 and #343  
**Decision:** Park 2022 is removed as a blocking dependency; proceed through triangulation against adjacent interface-noise theory

## Evidence limitation

The full text of C. H. Park, “Generation-recombination noise in uniformly doped semiconductors with contacts of finite surface recombination velocities,” *Journal of Applied Physics* **132**, 214501 (2022), DOI `10.1063/5.0111954`, is unavailable to the project.

Its abstract verifies only that:

- the model is a uniformly doped majority-carrier n-type semiconductor;
- contacts have finite surface recombination velocities;
- a new finite-velocity boundary replaces the ohmic boundary;
- the voltage-noise spectrum depends on field and contact velocity.

The abstract does not establish whether the paper includes primitive stochastic contact exchange, interface states, state-terminal cross covariance, local detailed balance, or equilibrium FDT recovery.

No equation or covariance will be inferred from the abstract.

## Decision

The project will not halt because one paper is inaccessible.

Park is reclassified from a required implementation source to an unresolved overlap risk. The stochastic-contact question will be triangulated against adjacent primary literature that treats semiconductor interfaces, thermionic emission, surface recombination, and fluctuating boundary conditions.

Novelty confidence is reduced rather than asserted.

## Replacement source set

### Highest priority

1. G. Gomila and J. M. Rubí, “Fluctuations generated at semiconductor interfaces,” *Physica A* **258**, 17–31 (1998). This source is directly relevant because its abstract states that carrier-exchange fluctuations are represented by interfacial fluctuating terms in boundary conditions, including nonideal interfaces and interface states.
2. G. Gomila, O. M. Bulashenko, and J. M. Rubí, “Local noise analysis of a Schottky contact: combined thermionic-emission–diffusion theory,” *Journal of Applied Physics* **83**, 2619–2630 (1998), DOI `10.1063/1.367024`. This source treats diffusion noise, thermionic-emission interface noise, and bulk-contact cross correlation in one model.
3. G. Gomila and J. M. Rubí, “Non-equilibrium thermodynamic description of junctions in semiconductor devices,” *Physica A* **234**, 851–871 (1997), DOI `10.1016/S0378-4371(96)00320-2`, arXiv `cond-mat/9603066`. This source derives surface equations and boundary conditions from interface nonequilibrium thermodynamics.

### Supporting sources

4. K. S. Champlin, “Generation-Recombination Noise in Semiconductors—The Equivalent Circuit Approach,” *IRE Transactions on Electron Devices* **7**, 29–38 (1960), DOI `10.1109/T-ED.1960.14588`.
5. “On the influence of diffusion and surface recombination upon the GR noise spectrum of semiconductors,” *Physica* **26**, 751–760 (1960), DOI `10.1016/0031-8914(60)90065-3`.
6. H. S. Min and D. Ahn, “Langevin noise sources for the Boltzmann transport equations with the relaxation-time approximation in nondegenerate semiconductors,” *Journal of Applied Physics* **58**, 2262–2265 (1985), DOI `10.1063/1.335943`.

## Revised claim boundary

The following is no longer a defensible provisional novelty statement:

> Introduce fluctuating exchange terms at semiconductor contacts.

The adjacent literature indicates that fluctuating semiconductor-interface boundary conditions and thermionic-emission contact noise were already formulated.

The candidate R06 contribution is narrowed to one or more of:

1. a controlled specialization of general interface fluctuation theory to finite bipolar HgCdTe photoconductors with dynamic bulk traps and optical generation;
2. a conservation-consistent assembly of contact state sources, direct terminal feed-through, and cross covariance in a finite-volume drift-diffusion-Poisson solver;
3. quantified error introduced by replacing an interface-state or thermionic-emission contact model with one deterministic surface-recombination velocity;
4. an uncertainty-qualified regime boundary showing when contact fluctuations materially change inferred HgCdTe GR lifetime or noise amplitude;
5. a reproducible benchmark synthesis if the physical closure itself is fully established.

## Provisional contact model status

The project event model

\[
\overline{\Gamma}^{out}=a^{out}-a^{in},
\qquad
Q^{\Gamma}=\frac{a^{out}+a^{in}}{A_c}
\]

remains accepted as a thermodynamic implementation template because it separates mean flux from event activity and is positive semidefinite by construction.

It is not claimed as original and is not yet accepted as a quantitative HgCdTe metal-contact model.

## Authorization

Authorized under issue #343:

- audit the adjacent interface-noise sources;
- translate their interface fluxes and covariance matrices into the R06 sign and PSD conventions;
- derive the fast-reservoir elimination;
- compare independent carrier exchange, pair recombination, thermionic emission, and dynamic interface-trap mechanisms;
- specify equilibrium FDT and terminal cross-correlation tests;
- prepare the final Phase 1 proceed/reframe/terminate decision.

Still unauthorized:

- production material sweeps;
- predictive HgCdTe contact claims;
- manuscript drafting;
- novelty claims based solely on adding contact noise;
- arbitrary additive terminal or Johnson sources.

## Requested resources

The most useful additional full paper is:

- G. Gomila and J. M. Rubí, “Fluctuations generated at semiconductor interfaces,” *Physica A* **258**, 17–31 (1998).

Secondary useful papers are:

- Gomila, Bulashenko, and Rubí 1998, DOI `10.1063/1.367024`;
- Champlin 1960, DOI `10.1109/T-ED.1960.14588`;
- the 1960 *Physica* surface-recombination paper, DOI `10.1016/0031-8914(60)90065-3`.

## Gate consequence

Phase 1A may proceed without Park. The final novelty confidence must explicitly state that Park’s equation-level overlap remains unknown. Phase 1B begins as an adjacent-source triangulation, not as production solver implementation.