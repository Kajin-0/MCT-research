# Decision addendum: local robustness of the external-validation route selection

**Date:** 2026-07-21  
**Issue:** #184  
**Parent decision:** `2026-07-21-external-validation-route-selection.md`  
**Status:** candidate controlling addendum pending PR validation

## Question

Does the selected Chang route depend on one fragile provisional criterion value?

## Current top actionable routes

```text
Chang thickness/cutoff       24
Dingrong carrier spectrum    20
current margin                4
```

## One-level adverse Chang change

The largest possible score reduction from changing one Chang criterion by one allowed level is:

```text
3 points
```

This can occur through a one-level reduction in a criterion with weight three, such as falsification power or flagship relevance.

Resulting margin against unchanged Dingrong:

```text
24 - 3 - 20 = 1
```

Chang remains selected.

## One-level favorable Dingrong change

The largest possible score increase from changing one Dingrong criterion by one allowed level is:

```text
2 points
```

This can occur through improved calibrated-spectrum evidence or one-level reduction in nuisance penalty.

Resulting Chang margin against improved Dingrong:

```text
24 - (20 + 2) = 2
```

Chang remains selected.

## Simultaneous two-route stress

Apply both changes at once:

```text
(24 - 3) - (20 + 2) = -1
```

Dingrong would lead by one point.

## Decision

The Chang selection is:

```text
robust to any single one-level criterion revision: yes
robust to simultaneous adverse/favorable route changes: no
```

Therefore the route is sufficiently stable for the current acquisition request, but it is not treated as a permanent hierarchy.

Any meaningful source retrieval can change multiple criteria simultaneously. The complete route ranking must be recomputed after every source audit.

## Scientific interpretation

This result supports requesting the Chang pair first without claiming that Chang is intrinsically more important than Dingrong.

- Chang is currently the most implementation-ready route.
- Dingrong remains the highest-value single source for extending the physical carrier branch.
- A strong Dingrong retrieval or weak Chang source audit may reverse the implementation order.

## Claim boundary

The robustness calculation concerns the declared resource-allocation gate only. It is not:

- evidence for either physical model;
- uncertainty on a material parameter;
- a Bayesian model probability;
- or an authorization to suppress a lower-ranked source.
