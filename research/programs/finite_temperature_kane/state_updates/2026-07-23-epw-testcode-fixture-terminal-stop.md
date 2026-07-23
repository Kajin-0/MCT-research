# R02 state update: EPW testcode fixture terminal stop

**Date:** 2026-07-23  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## State transition

```text
upstream raw-vertex normalization through QE testcode
  ACTIVE DESIGN/EXECUTION GATE
  -> TERMINAL_HARNESS_STOP

direct-executable fixture
  -> DESIGN ONLY under issue #309
```

## Established

- The pinned QE 7.6 / EPW 6.1 source and corrected disabled-by-default observational patch are byte-qualified.
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

Both authorized attempts failed during post-run testcode output preservation. The first used content heuristics. The sole replacement used the correct deterministic filename but assumed the wrong persistent directory. Neither attempt preserved EPW stdout, so no enabled sequence or analyzer was run.

## Authorization

Closed:

- additional execution under issue #300;
- the QE testcode wrapper as the normalization fixture;
- automatic reruns or further capture-location guesses;
- all material calculations.

Open only for design:

- issue #309 direct command reconstruction;
- explicit stdout/stderr redirection;
- synthetic capture and shell-quoting tests;
- a no-execution dry-run command manifest.

Any future QE execution requires a separate bounded issue after the design-only gate is merged.

## Controlling records

```text
first_principles/b0/r02_epw_raw_vertex_fixture_contract.json
first_principles/b0/r02_epw_raw_vertex_fixture_harness_stop_29962340413.json
first_principles/b0/r02_epw_raw_vertex_fixture_terminal_harness_stop_29971955581.json
research/decision_records/2026-07-23-r02-epw-testcode-fixture-terminal-stop.md
```
