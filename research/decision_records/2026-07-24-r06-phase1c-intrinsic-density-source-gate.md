# R06 Phase 1C intrinsic-density source gate

**Date:** 2026-07-24  
**Program:** stochastic transport and finite-size noise  
**Controlling issue:** #346

## Decision

**Proceed with material-source auditing, but do not implement a source-exact HgCdTe intrinsic-density closure yet.**

The equation lineage is now sufficiently clear to prevent source conflation:

1. Madarasz, Szmulowicz, and McBath (1985), DOI `10.1063/1.335685`, is the earlier Kane intrinsic-density/effective-mass calculation.
2. Madarasz and Szmulowicz (1985), DOI `10.1063/1.335868`, is the Fermi-Dirac extension.
3. The official open Seiler-Lowney-Littler-Yoon 1991 precursor follows the Madarasz outline and provides the nonlinear-gap calculation architecture.
4. Lowney et al. (1992), DOI `10.1063/1.351371`, is the final nonlinear-gap journal calculation and fitted result.

## Evidence accepted

The official 1991 source supports:

- Kane three-band `k.p` conduction-band treatment;
- full Fermi-Dirac conduction statistics;
- nondegenerate heavy-hole statistics;
- `Delta = 1 eV`;
- `P = 8.49e-8 eV cm`;
- `m_hh = 0.55 m0`;
- Newton solution of the reduced Fermi energy;
- integration by parts before numerical quadrature;
- the exact nonlinear `Eg(x,T)` expression already recorded in the repository.

## Evidence rejected as insufficient

The following are not accepted as implementation evidence:

- corrupted machine extraction of Eqs. (2)-(4);
- equation reconstruction from later reviews;
- detector papers that quote an intrinsic-density fit without recovering its original provenance;
- presumed 1992 fit coefficients inferred from figures;
- silent insertion of conventional degeneracy factors or unit prefactors.

## Consequence

The existing statistics prototype remains a benchmark and architecture test. It must not be renamed or promoted to a material-accurate HgCdTe closure.

The next active branch should audit low-temperature electron mobility, hole mobility, and static permittivity while equation-quality intrinsic-density copies are pursued in parallel.

## Exit criteria

The intrinsic-density gate can be reconsidered only after:

- symbol-exact primary equations are available;
- atomic-unit normalization is independently checked;
- numerical reference points are committed;
- the 1992 fitted expression is verified if used.
