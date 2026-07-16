# Modern AHC prior-art audit

Eight owner-supplied PDFs were audited and hashed in `literature/papers/README.md`.

## Highest-impact findings

- Allen and Heine 1976 already establishes combined Fan and Debye-Waller thermal band shifts, translational-invariance relations, interband terms, and strong cancellation in small-gap systems.
- Lihm and Park 2020 establishes a full Debye-Waller self-energy matrix with off-diagonal elements and phonon-renormalized wave functions across a thermal band-inversion problem.
- Ponce et al. 2015 requires nonadiabatic treatment and explicit small-q convergence for polar band extrema. Its 2017 erratum corrects Eqs. 4, 5, 7, 15, 16, 18, and 19 and must accompany the paper.
- Verdi and Giustino 2015 requires separation of long- and short-range polar vertices before interpolation.
- Nery and Allen 2016 shows that the polar correction can be a significant part of the total band renormalization.
- Brunin et al. 2020 shows that dynamical quadrupoles can dominate long-range acoustic and TO coupling, including in polar semiconductors.
- Giustino 2017 is the review and notation map, not the preferred claim-level source.

## Novelty consequence

Generic matrix AHC, off-diagonal Debye-Waller terms, wave-function renormalization, polar nonadiabatic corrections, and long-range quadrupole corrections are established prior art.

The remaining candidate must be HgCdTe-specific: project the complex self-energy into one fixed complete Gamma6 + Gamma8 + Gamma7 basis; recover conventional 8-band Kane invariants; verify gauge, symmetry, Hermiticity, closure, and uncertainty; and improve a held-out observable beyond a gap-only null.

## Later production requirements

Before production AHC: retain signed Fan/Debye-Waller cancellation; use the Ponce erratum; converge q grids and broadening; treat polar extrema nonadiabatically; separate long- and short-range vertices; assess quadrupoles for acoustic/TO modes; separate fixed-volume and lattice-expansion effects; and keep CdTe, HgTe, and alloy gates distinct.

This audit changes planning and claim boundaries only. It does not authorize production AHC, dense EPW, HgTe, or alloy calculations.