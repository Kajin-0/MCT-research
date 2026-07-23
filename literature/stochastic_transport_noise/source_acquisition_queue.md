# R06 priority source-acquisition queue

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** one critical full paper remains before the finite-contact prior-art gate can close

## Purpose

This queue distinguishes bibliographic identification from equation-level verification. A DOI or abstract is insufficient for implementation equations, stochastic covariance, boundary conditions, or novelty decisions.

## Critical full paper still required

### Park (2022)

- **Title:** Generation-recombination noise in uniformly doped semiconductors with contacts of finite surface recombination velocities
- **Author:** C. H. Park
- **Journal:** *Journal of Applied Physics* **132**, 214501 (2022)
- **DOI:** `10.1063/5.0111954`
- **Required extraction:**
  - exact finite-contact boundary equations;
  - whether contact fluctuations are included or only a deterministic Robin condition;
  - source covariance and PSD normalization;
  - blocking and reservoir limits;
  - terminal ensemble;
  - overlap with the R06 forward/reverse contact-event closure.
- **Priority:** decisive. This is now the only critical full-paper acquisition blocking the finite-contact novelty decision.

## Supplied and audited on 2026-07-23

The user supplied full readable copies of the following papers. The article files are not committed to the public repository because redistribution rights have not been established.

### Zocchi (2006)

- **DOI:** `10.1103/PhysRevB.73.035203`
- **Status:** full equation audit complete.
- **Result:** establishes full-frequency finite-length unipolar electron-trap current and voltage spectra with drift, diffusion, linearized Poisson coupling, dielectric relaxation, and distinct terminal ensembles.
- **Record:** `source_notes/zocchi_2006.md`.

### Smith (1984)

- **DOI:** `10.1063/1.334155`
- **Status:** full equation audit complete.
- **Result:** establishes quasineutral ambipolar HgCdTe GR-noise theory with finite deterministic contact recombination velocities and blocking/absorbing limits; no explicit stochastic contact exchange source was found.
- **Record:** `source_notes/smith_1984.md`.

### Smith (1982)

- **DOI:** `10.1063/1.330006`
- **Status:** DOI resolved and full equation audit complete.
- **Result:** establishes finite HgCdTe photoconductor GR noise with drift, diffusion, absorbing contacts, spatial source-lifetime correlation, and non-Lorentzian frequency asymptotes.
- **Record:** `source_notes/smith_1982.md`.

### Iverson and Smith (1985)

- **DOI:** `10.1063/1.335666`
- **Status:** full covariance and Appendix audit advanced.
- **Result:** establishes explicit dynamic deep-level populations, four capture/emission rates, correlated carrier/trap population fluctuations, and a separate bound/free thermal-noise component in HgCdTe.
- **Record:** `source_notes/iverson_smith_1985.md`.

### Bulashenko et al. (1998)

- **DOI:** `10.1063/1.367023`
- **Status:** full equation audit complete.
- **Result:** establishes analytical impedance-field propagation and demonstrates that electrostatic/sample-contact cross terms are required for equilibrium Nyquist recovery.
- **Record:** `source_notes/bulashenko_et_al_1998.md`.

### Shockley and Read (1952)

- **DOI:** `10.1103/PhysRev.87.835`
- **Status:** four-channel kinetic audit complete.
- **Result:** supplies the authoritative capture/emission kinetics and steady SRH reduction; it does not provide a stochastic covariance, which R06 must construct from the primitive event channels.
- **Record:** `source_notes/shockley_read_1952.md`.

## Useful but non-blocking source request

### Bonani and Ghione (1999)

- **DOI:** `10.1016/S0038-1101(98)00253-6`
- **Current status:** substantial publisher-text audit completed.
- **A clean equation-quality copy would still help with:**
  - exact electron-hole-trap source cross-spectral matrices;
  - normalization constants;
  - fluctuation boundary conditions;
  - quantitative benchmark tolerances.

This copy is useful but no longer blocks the main Phase 1A novelty decision.

## Source-ingestion rule

For every supplied source, the project records:

1. article version and provenance;
2. DOI and bibliographic identity;
3. exact equations and sections inspected;
4. model state and geometry;
5. deterministic and stochastic boundary conditions;
6. primitive noise representation and covariance convention;
7. terminal ensemble;
8. direct overlap and novelty consequences.

User-supplied copyrighted PDFs are not committed unless redistribution permission is explicit.

## Gate rule

The finite-contact prior-art gate remains open only for Park 2022. If Park also uses a deterministic finite-velocity boundary without a contact event covariance, the R06 stochastic finite-contact closure remains a plausible candidate contribution. If Park already provides a thermodynamically complete forward/reverse contact covariance with equilibrium fluctuation-dissipation recovery, R06 must reframe that part as a benchmark or implementation study.