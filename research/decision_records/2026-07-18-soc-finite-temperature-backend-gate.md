# SOC finite-temperature matrix backend decision

**Date:** 2026-07-18  
**Status:** documented-capability audit completed

## Requirement

The research target requires one route that can simultaneously provide:

1. nonmagnetic spin-orbit electronic states;
2. an off-diagonal eight-band matrix in the declared selected-band gauge;
3. Fan plus Debye-Waller, or a controlled total thermal effect;
4. explicit polar long-range control;
5. fixed or reconstructable gauge handling;
6. held-out validation.

A final analytical reduction also requires mode- or frequency-resolved information.

## Result

No currently documented and project-validated backend passes every hard gate.

### QE `ph.x` AHC plus `postahc.x`

This is the closest explicit matrix backend. The pinned source exports first-order Fan vertices, an upper-Fan Sternheimer term, off-diagonal generalized-ASR Debye-Waller matrices and gauge overlaps. Four of six hard gates are documented.

Remaining blockers:

- no dedicated validation of the nonmagnetic SOC eight-band case;
- the current CdTe long-range polar response is rejected;
- a source/target long-range correction of Debye-Waller is undefined.

### EPW

EPW documents SOC spinor workflows, gauge handling and polar long-range subtraction/restoration. It closes four hard gates, but the standard self-energy route computes Fan-Migdal without Debye-Waller and the required off-diagonal eight-band self-energy export is unvalidated.

### ABINIT modern EPH

The modern EPH route includes Fan, Debye-Waller and polar corrections. Official documentation explicitly states that SOC is not supported as of May 2026, and the output is band-resolved rather than the required off-diagonal matrix.

### ABINIT legacy spinor route

The legacy workflow is compatible with spinors, but it is deprecated and lacks the required modern off-diagonal matrix, polar and gauge interfaces.

### ZG special displacement

ZG can combine ordinary SOC electronic calculations with a total thermal displacement effect, avoiding reliance on an explicit SOC Debye-Waller implementation. It does not yet provide an audited primitive-cell eight-band matrix, degenerate-manifold gauge restoration, finite-size polar correction, or complete mode-resolved reduction.

### Custom SOC Debye-Waller

A custom generalized-ASR SOC implementation could eventually close the method, but it is a large scientific-software project without an implementation or independent validation.

## Decision

- No direct A1 backend is selected.
- No real backend execution is authorized.
- The preferred next design is a synthetic **ZG selected-band matrix reconstruction oracle**.
- The secondary route is a dedicated **QE AHC nonmagnetic-SOC capability test**.
- A custom Debye-Waller implementation remains unauthorized.

ZG is prioritized because it can, in principle, include the total harmonic thermal effect through ordinary SOC electronic calculations. The next oracle must determine whether primitive-cell eight-band matrices can be reconstructed from distorted supercells without losing degeneracy, gauge, symmetry or held-out transfer.

## Evidence

```text
workflow run: 29651034170
artifact:     8431471817
digest:       sha256:607d8e5e0e8b858b0994ec97f9cba05e47ad404d6463a7e7c1f5539e002e635c
```

## Claim boundary

This is a capability and authorization decision, not a benchmark of numerical accuracy. An unverified route may be technically capable, but it cannot be selected until its missing hard gates are falsified explicitly.
