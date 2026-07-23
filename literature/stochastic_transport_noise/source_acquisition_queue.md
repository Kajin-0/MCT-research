# R06 priority source-acquisition queue

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** sources required before the Phase 1A literature gate can close

## Purpose

This queue distinguishes papers whose bibliographic identity is known from papers whose equations and boundary conditions have actually been inspected. A DOI is not treated as equation-level verification by itself.

## Highest-priority full papers still required

### 1. Zocchi (2006)

- **Title:** Current and voltage noise spectrum due to generation and recombination fluctuations in semiconductors
- **Author:** F. E. Zocchi
- **Journal:** Physical Review B 73, 035203 (2006)
- **DOI:** `10.1103/PhysRevB.73.035203`
- **Needed for:** full coupled carrier/trap/Poisson operator, carrier and trap boundary conditions, primitive covariance, current-versus-voltage ensemble, PSD convention, and displacement-current treatment.
- **Priority:** critical. This is the closest identified general-theory overlap.

### 2. Park (2022)

- **Title:** Generation-recombination noise in uniformly doped semiconductors with contacts of finite surface recombination velocities
- **Author:** C. H. Park
- **Journal:** Journal of Applied Physics 132, 214501 (2022)
- **DOI:** `10.1063/5.0111954`
- **Needed for:** exact finite-contact boundary equations, whether contact fluctuations are included or only a deterministic Robin boundary is used, limiting behavior as surface velocity tends to zero or infinity, and PSD normalization.
- **Priority:** critical. This determines whether stochastic finite-contact closure remains a plausible gap.

### 3. Smith (1984)

- **Title:** Effects of blocking contacts on generation-recombination noise and responsivity in intrinsic photoconductors
- **Author:** D. L. Smith
- **Journal:** Journal of Applied Physics 56, 1663 (1984)
- **DOI:** `10.1063/1.334155`
- **Needed for:** contact-region model, blocking and ohmic limits, responsivity/noise transfer, sweepout parameterization, HgCdTe specialization, and the exact relationship between terminal corner frequency and bulk lifetime.
- **Priority:** critical HgCdTe benchmark.

### 4. Smith (1982)

- **Title:** Theory of generation-recombination noise in intrinsic photoconductors
- **Author:** D. L. Smith
- **Journal:** Journal of Applied Physics 53, 7051–7060 (1982)
- **DOI:** unresolved in the current audit
- **Needed for:** the foundational finite intrinsic-photoconductor derivation used by later Smith and Iverson-Smith work, including diffusion, drift, contact-region recombination, spatial lifetime correlation, responsivity, and detectivity.
- **Priority:** critical. A publisher PDF, scanned article, or verified DOI is requested.

## Useful equation-quality copies

The following papers have been substantially audited from accessible copies, but a clean publisher or author PDF would improve exact transcription and benchmark construction:

### Bonani and Ghione (1999)

- **DOI:** `10.1016/S0038-1101(98)00253-6`
- **Need:** exact source cross-spectral matrices, fluctuation normalization, and boundary conditions.

### Bulashenko et al. (1998)

- **DOI:** `10.1063/1.367023`
- **Need:** exact impedance-field differential equation, local source tensor, and PSD bandwidth convention.

### Iverson and Smith (1985)

- **DOI:** `10.1063/1.335666`
- **Need:** complete Appendix source correlations, charge-state notation, and fluctuation boundary conditions.

### Shockley and Read (1952)

- **DOI:** `10.1103/PhysRev.87.835`
- **Need:** clean equation audit of forward and reverse capture/emission kinetics before the R06 stochastic SRH propensities are frozen.

## Submission format

Any of the following is sufficient for source ingestion:

1. the publisher PDF;
2. an author manuscript with all equations and figures;
3. a DOI plus a stable full-text location;
4. a scanned article with readable equations and page numbers.

For every supplied source, R06 will record file provenance, article version, equation locations, and whether the source is legally redistributable. Supplied papers will not be committed to the public repository unless redistribution rights are explicit.

## Gate rule

Phase 1A cannot claim the finite-contact novelty boundary is resolved until Zocchi 2006, Park 2022, and Smith 1984 have been inspected at equation level. Smith 1982 is additionally required before the HgCdTe analytical benchmark lineage is considered complete.