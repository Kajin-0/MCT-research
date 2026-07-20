# Chang 2006 nonparabolic-Urbach observation operator

**Date:** 2026-07-20  
**Issue:** #145  
**Parent program:** #132

## Question

Can Chang et al. 2006 be added to the HgCdTe absorption-edge uncertainty ensemble as a provenance-controlled observation operator without promoting it to a material-gap equation or introducing unconstrained tail parameters?

## Source

```text
Y. Chang et al.
Narrow gap HgCdTe absorption behavior near the band edge including nonparabolicity and the Urbach tail
Applied Physics Letters 89, 062109 (2006)
DOI 10.1063/1.2245220
```

The copyrighted source is not committed.

## Implemented operator

The intrinsic branch follows the source's hyperbolic nonparabolic absorption expression, Eq. (9), containing heavy-hole and light-hole contributions.

The source gives the smooth-join approximation

```text
E0 approximately Eg + W/2
```

in Eq. (13). The implementation therefore uses

```text
alpha_tail(E) = alpha_intrinsic(E0) exp((E-E0)/W)
E0 = Eg + W/2
```

below the join and the Eq. (9) intrinsic shape at and above the join.

This construction is exactly continuous at `E0`. It is derived from source Eqs. (1), (9), and (13). The ambiguous absolute exponential prefactor printed in the first branch of Eq. (14) is not used literally.

## Declared source domain

The implementation deliberately uses a conservative domain tied to the demonstrated source specimens and calculation:

```text
composition_x          0.21 to 0.23
temperature_k          77 to 80 K
energy minus edge      -0.020 to +0.300 eV
```

The 300 meV upper limit follows the more conservative statement in the abstract rather than the broader discussion bound.

## Parameter contract

The candidate is disabled by default. Enabling it requires explicit, positive, provenance-bound values for:

- Urbach width `W`;
- hyperbola curvature parameter `b`;
- a Chang-specific absorption fit window;
- Chang-specific edge search bounds;
- deterministic grid size.

`W` and `b` are not optimized in this tranche. For each candidate edge, the positive multiplicative amplitude is solved analytically in log space.

A valid fit requires:

```text
at least 20 points total
at least 5 points below E0
at least 10 points at or above E0
all used energies inside the declared relative-energy domain
```

The operator fails closed when provenance, composition, temperature, relative-energy coverage, or branch coverage is inadequate.

## Validation

Synthetic validation using a known piecewise Chang curve recovers:

```text
Eg          0.100000 eV
amplitude   50000 cm^-1
W           0.012 eV
b           0.100 eV
E0          0.106 eV
```

within the declared deterministic numerical tolerances. Continuity at `E0` is explicitly tested. Opt-in adds exactly one candidate to the existing ensemble, while the disabled configuration adds none.

The pre-existing fractional-power, threshold, and Chu 1994 contract tests remain unchanged and pass.

## Decision

### Authorized

- use the Chang 2006 candidate for research-only absorption observation-model sensitivity;
- compare its fitted edge against the other declared candidates when a spectrum lies inside the source domain and `W` and `b` have explicit provenance;
- report its edge and contribution to the model-family and combined uncertainty envelopes;
- preserve the continuity-normalization choice and source-domain limits in every output.

### Unauthorized

- describe Chang 2006 as a universal material-gap law;
- fit `W`, `b`, and `Eg` freely from the same spectrum in this tranche;
- extrapolate outside `0.21 <= x <= 0.23`, `77 <= T <= 80 K`, or the declared relative-energy interval;
- silently infer missing parameter provenance;
- select the Chang candidate as a corrected or recommended gap;
- use this synthetic validation as evidence that the operator improves agreement on a real specimen.

## Program consequence

The absorption-edge uncertainty framework now contains a physically richer optional candidate that explicitly represents nonparabolicity and an Urbach tail. This broadens the declared observation-model ensemble but does not alter any existing experimental result until the operator is applied to a provenance-complete spectrum in its source domain.

Production correction, single-edge selection, and universal material-law fitting remain forbidden.
