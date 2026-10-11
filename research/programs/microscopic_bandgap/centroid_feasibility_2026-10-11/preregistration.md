# Pre-registration: bounded synthetic centroid feasibility

2026-10-11. Base `c1a2ccde7f10ad3ff23c2d224ffa415f0545404a`; existing branch
`research/hgcdte-impurity-tmatrix-20261010`. This file and the machine-readable
configuration are committed **before evaluating the scan**. No pilot physical
input, new data, DFT, session, supervisor, goal API or empirical fit is involved.

## Model and fixed scan

Use the existing continuum package's N3 spectral family, with its positive
mixed-sector measures, and the earlier atomic test's illustrative reference
energy `e(x)=-0.3+1.1x` eV. This is a transparent synthetic specialization of
that family, not a recovered or qualified HgCdTe TB/CPA Hamiltonian.
The archived binary-derived TB vertex remains rejected for physical prediction.
The [model specification](model_and_certification.md) supplies one fixed-projector
self-adjoint realization and the exact integral formulas.

- Widths mean **half-widths** W: `0.5, 1.5, 5.0` eV; reference r=0.
- Analytical resolutions eta: `0.05, 0.10, 0.20` eV, never intrinsic linewidths.
- Interior x: `0.20, 0.25, 0.30, 0.35, 0.40`; no root search or interpolation.
- Alternatives: balanced redistribution a=0, positive a=1, negative a=-1.
  Their probability, endpoints, first endpoint spectral jets and full centroids
  agree; a changes unresolved mixed-sector spectral weight, not a fitted gap.
- Window: chi_W(E)=[1-(E/W)^2]^2 inside [-W,W], zero outside. It is positive,
  compact and C1, satisfying the prior bounded-functional/continuity gates.
- Compute all 135 rows: m6,n6,m8,n8, C6-C8, enclosed numerical errors, sign
  margins and retained weights. Known window exclusion is not omitted-spectrum
  numerical error. Never renormalize a band prefix or average signs into a gap.

## Independent errors and fixed acceptance gates

Analytic atom/uniform-bath integrals use 32-digit directed Decimal interval
arithmetic, a 64-term arctangent series with explicit remainder, and the
documented correctly rounded Decimal logarithm contract. Those enclosures,
not differences of quadrature grids, certify numerical errors. A fixed
composite Gauss-Legendre check uses orders 8 and 16 and segments of length
at most eta; neither observed convergence nor an assumed physical residual
replaces the analytic enclosure.

1. Model qualification: positive unit measures, declared fixed projectors and
   identical endpoint/coherent controls; independent formulas/checks pass.
2. Numerical gate: every centroid enclosure has radius <=0.0001 eV (0.1 meV),
   independent moment checks differ by <=1e-8 for m and <=W*1e-8 eV for n.
   A 32-digit context is an inexpensive guard against algebraic cancellation;
   it is not a requirement for material precision.
3. Mass floor: every sector's lower enclosed window mass >=0.05.
4. Within-model sign gate: at each x, all nine width/eta rows have the same
   nonzero sign with enclosed distance from zero >=0.001 eV (1 meV).
5. Alternative-robust gate: at each x all three alternatives also share that
   sign. Overall GO requires gates 1–5 at all registered x; otherwise NO-GO,
   retaining separate numerical, floor and sign failure reasons.

These are finite-grid model gates, not a uniform-x/resolution theorem, physical
uncertainty budget or composition transversality certificate. Passing cannot
establish physical x_c, an absorption edge, topology or a material sign bracket.

## Resource and stopping bounds

One exact 135-row scan, one independent quadrature evaluation per registered
order/row and focused tests. No random sampling, tuning, parameter expansion,
additional models or adaptive scans. Work is scalar/short-array algebra;
maximum independent quadrature grid is 200 segments x 16 nodes. Target elapsed
time <120 seconds and working arrays <256 MiB; no job queue is created.
An implementation error may be corrected with the same immutable model/grid;
failed scientific gates must not be repaired by changing parameters.

Save the complete rows, deterministic summary, decision and tests, then stop.
Model conclusions and the unchanged missing physical-input boundary are separate.
