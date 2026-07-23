# R02 state update: direct EPW fixture stops at nonperturbation

**Date:** 2026-07-23  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## Transition

```text
pinned upstream raw-vertex normalization
  DIRECT EXECUTION GATE
  -> STOP_NONPERTURBATION_GATE

same-immutable-state attribution
  -> DESIGN ONLY
```

## Established

- One pinned QE 7.6 / EPW 6.1 build completed.
- One exporter-disabled and one exporter-enabled direct diamond sequence completed.
- All 12 commands returned zero.
- Twenty-four stdout/stderr files and 20,736 raw vertex rows were preserved.
- The raw normalization, scalar diagonal, q-weight, acoustic-mask, retarded-sign, complete-block, and synthetic covariance identities passed.
- No testcode or material input was used.

## Binding failure

```text
maximum enabled/disabled self-energy difference  1.9286256500095078e-7 eV
required limit                                    1e-12 eV
```

The exact nonperturbation requirement failed. The threshold cannot be relaxed retrospectively.

## Interpretation

The two compared runs independently regenerated the complete upstream fixture state. The result therefore cannot attribute the difference uniquely to exporter I/O rather than ordinary run-to-run variation.

Consequently:

- exporter causality is not established;
- exporter noninterference is not established;
- backend normalization is not promoted to a validated R02 capability;
- the internal normalization reconstruction remains diagnostic evidence only.

## Authorization

Closed:

- additional execution under issue #313;
- another build, third sequence, or threshold change;
- the two-independent-full-sequence comparison strategy;
- SOC and all material calculations.

Open only for design:

- determine whether one immutable saved EPW state can be replayed twice;
- identify exact read/restart artifacts and hashes;
- design a baseline disabled/disabled reproducibility control;
- design disabled/enabled replay without upstream regeneration;
- define a separate bounded execution issue only after identifiability is established.

## Controlling records

```text
first_principles/b0/r02_epw_direct_fixture_terminal_result.json
research/decision_records/2026-07-23-r02-epw-direct-fixture-nonperturbation-stop.md
```
