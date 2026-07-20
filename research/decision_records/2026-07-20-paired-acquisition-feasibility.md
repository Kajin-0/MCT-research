# Paired HgCdTe acquisition feasibility and pilot decision

**Date:** 2026-07-20  
**Controlling issue:** #161  
**Parent protocol:** Issue #141 / PR #142

## Decision

The paired acquisition protocol is scientifically specified but requires a separate, fail-closed collaboration-readiness layer before specimens move between organizations.

The readiness model now distinguishes:

```text
capability review
logistics pilot
pre-screening pool
full 8-specimen experiment
```

No lower stage inherits the scientific authority of a higher stage.

## Why the separation is necessary

The full protocol depends on multiple organizations agreeing on specimen geometry, temperature metrology, registered measurement areas, state-altering operations, calibration, native-data release, covariance, data rights, and chain of custody.

A nominal statement that a laboratory can perform FTIR, Hall, positron, or magneto-optical measurements is insufficient. The collaboration must establish that the actual specimen geometry, temperatures, uncertainty, native files, calibration records, and processing sequence satisfy the protocol.

## Logistics pilot

The bounded pilot uses:

```text
2 specimens
x 2 modalities
x 2 temperature blocks
= 8 primary observations
```

The two specimens span composition. They do not span independent carrier and vacancy levels.

The pilot may validate:

- sample flow and survivability;
- same-area registration;
- sample-temperature control;
- technical repeatability;
- calibration and covariance transfer;
- native-file hashing, delivery, and parsing;
- pre/post state stability;
- analysis execution on partner-generated data.

It may not estimate a carrier term, vacancy term, carrier-vacancy aliasing, or the complete five-parameter model.

## Full-readiness gate

Full execution remains blocked until:

1. every required role is confirmed with evidence;
2. all thirteen cross-cutting pilot gates are confirmed;
3. the logistics pilot is complete;
4. a pre-screening plan is frozen;
5. a measured candidate pool yields eight specimens satisfying:

```text
maximum sigma_x                     <= 0.0015
same carrier polarity               required
carrier separation                  >= 3 combined sigma
vacancy separation                  >= 3 combined sigma
abs(carrier-vacancy correlation)    <= 0.5
specimen IDs frozen                 required
processing histories frozen         required
```

The full experiment plan must then be explicitly promoted from `blocked_pending_prescreening` to `ready`.

## Authorized conclusions

- External capability review is now machine-auditable.
- A logistics pilot can be authorized independently of the full experiment.
- Successful logistics do not imply scientific identifiability.
- Actual pre-screening measurements, not process labels, control final readiness.
- Confidential commercial details may remain external when a stable evidence identifier and accountable owner are retained.

## Unauthorized conclusions

- No partner is identified or endorsed.
- No access, schedule, or cost is guaranteed.
- No universal project price is estimated.
- No scientific gate from PR #142 is relaxed.
- A logistics pilot is not treated as the full 32-observation experiment.
- A capability marked confirmed without evidence is not accepted.

## Program consequence

The next actionable task is no longer additional protocol design. It is to populate the feasibility template through documented partner conversations and supporting evidence. The repository can then distinguish a known blocker from an unknown capability and can authorize a logistics pilot without prematurely authorizing the full scientific experiment.
