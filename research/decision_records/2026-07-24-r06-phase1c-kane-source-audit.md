# R06 Phase 1C Kane-source audit decision

**Date:** 2026-07-24  
**Issue:** #346  
**Decision:** `ARCHITECTURE_RECOVERED_IMPLEMENTATION_BLOCKED_ON_SYMBOL_EXACT_TRANSCRIPTION`

## Decision

Accept the official open Seiler-Lowney-Littler-Yoon 1991 proceedings paper as a primary architecture source and as the equation-lineage bridge to Madarasz and Szmulowicz.

Do not authorize a source-exact HgCdTe intrinsic-density implementation.

## Evidence accepted

- exact source identity and official NIST distribution;
- exact nonlinear `Eg(x,T)` relation;
- declared `x,T` calculation domain;
- Kane three-band model;
- full conduction-band Fermi-Dirac statistics;
- separate nondegenerate heavy-hole treatment;
- `Delta`, `P`, and `m_hh` values;
- Newton neutrality solve and integration-by-parts strategy;
- explicit dependence on Madarasz Eqs. (1) and (2).

## Blocking evidence

The mathematical typography of the printed density equations is corrupted in available machine extraction. The repository lacks:

- a visual symbol-exact transcription of Eqs. (2)-(4);
- verified normalization and unit conversion;
- immutable numerical reference points;
- verified coefficients for the 1992 fitted intrinsic-density relation.

## Authorization

Authorized next:

- manual equation transcription from an equation-quality primary rendering;
- independent algebra and unit audit;
- immutable reference-point construction;
- source-to-code tests after the above are complete.

Not authorized:

- reconstructing missing symbols from secondary sources;
- implementing a presumed Madarasz or Lowney equation set;
- fitting curves from figures;
- model-comparison sweeps;
- material-accurate or predictive HgCdTe claims.

## Phase effect

The material-source gate remains open. The correct next action is equation transcription, not expansion of the deterministic transport architecture.
