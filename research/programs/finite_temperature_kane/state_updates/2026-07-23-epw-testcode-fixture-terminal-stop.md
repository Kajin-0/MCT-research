# R02 state update: EPW testcode fixture terminal stop

**Date:** 2026-07-23  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## Transition

```text
upstream raw-vertex normalization through QE testcode
  ACTIVE GATE
  -> STOP_HARNESS_BUDGET_EXHAUSTED

direct-executable fixture
  -> DESIGN ONLY under issue #309
```

## Established

- The pinned QE 7.6 / EPW 6.1 source and corrected disabled-by-default observational patch were byte-qualified.
- Two pinned builds completed.
- Two exporter-disabled upstream diamond sequences completed all five programs successfully.
- No material input was used.

## Not established

- exporter-enabled/disabled standard-output equivalence;
- raw complex-vertex export from an enabled sequence;
- backend scalar-normalization equivalence;
- SOC-spinor compatibility;
- CdTe, HgTe, HgCdTe, or A1 readiness.

## Reason for stop

Both authorized attempts failed during post-run testcode output preservation. The first used content heuristics. The sole replacement used the correct deterministic filename but assumed the wrong persistent working directory. Neither attempt preserved EPW stdout, so no enabled sequence or analyzer was run.

## Authorization

Closed:

- additional execution under issue #300;
- QE testcode as the normalization-fixture wrapper;
- automatic reruns or additional capture-location guesses;
- all material calculations.

Open only for design:

- issue #309 direct command reconstruction;
- explicit stdout/stderr redirection;
- synthetic capture and shell-quoting tests;
- a no-execution dry-run command manifest.

Any future QE execution requires a separate bounded issue after the design-only gate is merged.

## Controlling records

```text
first_principles/b0/r02_epw_raw_vertex_fixture_terminal_result.json
research/decision_records/2026-07-23-r02-epw-testcode-fixture-terminal-stop.md
```
