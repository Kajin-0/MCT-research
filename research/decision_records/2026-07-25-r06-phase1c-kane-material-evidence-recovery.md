# R06 Phase 1C decision — Kane material-evidence recovery

**Date:** 2026-07-25  
**Controlling issue:** #346  
**Decision:** accept the candidate-source classification; keep the material closure blocked

## Decision

The first targeted material-evidence recovery pass identified six relevant HgCdTe
sources and classified them against the PR #385 evidence contract.

The classification is accepted as a Phase 1C source gate because it separates:

- direct Hall-derived intrinsic-density evidence;
- high-temperature Hall parameter inversion;
- calculated intrinsic-density fits and curves;
- final journal model fits with unrecovered coefficients;
- independent magneto-optical band-structure constraints.

No source supplies a complete accepted PR #385 observation point. No parameter
fit is authorized.

## Strongest direct source

Nemirovsky and Finkman 1979 is the strongest direct intrinsic-density candidate.
The institutional record reports Hall-based measurements on characterized,
uncompensated HgCdTe samples over:

```text
0.205 <= x <= 0.22 and x = 0.29,
approximately 150 K to 320 K.
```

The source remains non-countable because sample-level values, positive standard
uncertainties, composition uncertainty, and the neutrality/chemical-potential
basis have not been recovered.

## Strongest parameter-inversion source

Finkman 1983 reports fitting temperature-dependent Hall-derived carrier
concentrations in the near-intrinsic region to a Kane model and extracting band
parameters.

This is primary experimental evidence, but it does not authorize direct use of
its fitted quantities as the independent project inputs `N_*` and `alpha`.
Primary equations, sample-level data, fit assumptions, and uncertainty or
covariance information must be recovered first. A source-grounded mapping to the
project-defined model would still be required afterward.

## Historical model benchmarks

Hansen–Schmit 1983 remains the bounded analytic intrinsic-density benchmark.
Seiler et al. 1991 remains an open primary model-calculation and equation-lineage
source. Lowney et al. 1992 remains the final journal model source with an
unrecovered fit.

These sources may be used for historical model comparisons after symbol and
coefficient recovery. They must not be counted as independent experimental
material points.

## Independent adequacy evidence

Teppe et al. 2016 supplies independent, uncertainty-bearing HgCdTe
magneto-optical band-structure evidence, including a nearly constant Kane
velocity across its studied samples and temperatures.

It does not directly measure density, chemical compressibility, or generalized
Einstein factor. It is retained for the later restricted simplified-model versus
full-three-band adequacy decision, not for immediate `N_*`/`alpha` fitting.

## Unresolved observation classes

No direct HgCdTe chemical-compressibility or generalized-Einstein measurement
was recovered in this pass. No density candidate has independently known `eta`,
and no separately validated heavy-hole/split-off-band neutrality model is
available.

The absence is a recovery status, not a proof that such evidence does not exist.

## Authorization state

The material gate remains:

```text
blocked_no_accepted_hgcdte_reference_set
```

The following remain unauthorized:

- HgCdTe values or relations for `N_*` and `alpha`;
- equilibrium density and chemical compressibility;
- screening;
- detector coupling;
- predictive transport or noise.

## Required next work

1. Obtain and visually transcribe the full Nemirovsky–Finkman 1979 article,
   including point values, uncertainties, sample composition, and Hall-analysis
   assumptions.
2. Obtain and transcribe the full Finkman 1983 article, including measured data,
   fitted equations, parameter uncertainties, and covariance where available.
3. Complete symbol-level transcription of Seiler et al. 1991 equations (2)–(4)
   and treat digitized curves only as model-regression targets.
4. Continue targeted searches for chemical compressibility, thermodynamic
   density of states, quantum capacitance, or generalized-Einstein evidence in
   HgCdTe.
5. Derive whether the modern magneto-optical Kane velocity and gap can constrain
   a project parameterization without violating the heavy-hole and neutrality
   boundary.

## Phase 1C consequence

The evidence architecture is now populated with candidate sources, but the
material-validation exit criterion has not advanced from zero accepted points.
The next progress must come from primary data recovery or new independent
measurements, not additional deterministic solver scope.
