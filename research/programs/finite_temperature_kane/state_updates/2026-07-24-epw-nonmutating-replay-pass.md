# R02 state update: non-mutating serial EPW replay passes

**Date:** 2026-07-24  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## Transition

```text
serial epwread allocation diagnosis
  source-supported
  -> runtime-supported

non-mutating serial replay boundary
  design-supported
  -> runtime-validated for pinned non-SOC diamond fixture

same-state exporter attribution
  -> separately reviewed successor only
```

## Established

One pinned QE 7.6 / EPW 6.1 build, one upstream diamond preparation, and one exporter-disabled serial replay completed.

```text
builds                       1
preparations                 1
preparation commands         6 / 6 exit code 0
serial replays               1
replay exit code             0
selfen_elec_ calls            216
material calculations        0
```

The replay used:

```text
epbwrite   = .false.
epbread    = .false.
epwwrite   = .false.
epwread    = .true.
wannierize = .false.
elecselfen = .true.
```

The projected replay seed contained 162 files. The replay preserved every seed byte and created only:

```text
EPW.bib
linewidth.elself.300.000K
selecq.fmt
```

No `.epb`, raw-vertex, transient, or unknown file remained after replay.

Completion evidence passed:

```text
Total program execution       present
selfen_elec_ timer             216 calls
linewidth output              414,841 bytes
numeric rows                  5,184
fatal or signal markers       absent
```

## Classification

```text
PASS_NONMUTATING_SERIAL_REPLAY
```

## Interpretation

The serial restart harness and the merged non-mutating filesystem boundary are validated for the pinned non-SOC upstream diamond fixture.

The result does not evaluate the observational exporter. Therefore:

- exporter noninterference remains unvalidated;
- enabled/disabled attribution remains unperformed;
- matrix normalization remains only previously diagnostic/restricted evidence;
- SOC behavior remains closed;
- no material prediction is authorized.

The prior issue-350 strict stop remains historically binding. The present result validates a corrected prospective protocol and does not alter the earlier classification.

## Authorization

Closed:

- additional issue-371 build;
- additional issue-371 preparation;
- additional issue-371 replay;
- automatic retry;
- exporter-enabled execution under issue #371;
- MPI substitution;
- SOC or material calculations.

Permitted only through a separate review:

- reconcile the earlier same-state attribution design with the now-validated `epbwrite=.false.` seed boundary;
- define disabled A, disabled B, and exporter-enabled replays from one prepared seed;
- preserve the existing deterministic attribution rule and fixed numerical floors;
- authorize any execution only in a new bounded issue.

## Controlling record

```text
first_principles/b0/r02_epw_nonmutating_replay_terminal_result.json
research/decision_records/2026-07-24-r02-epw-nonmutating-replay-pass.md
```
