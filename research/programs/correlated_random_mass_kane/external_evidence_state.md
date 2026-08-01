# R05 external-evidence state overlay

**Program:** R05 — Correlated random-mass Kane regime  
**Controlling issue:** #405  
**Predecessor:** PR #404  
**State:** `MATERIAL_ACTIVATION_BLOCKED`  
**Evidence decision:** `EVIDENCE_GATE_FAILED`  
**Recommendation:** `R05_REACTIVATION_NOT_RECOMMENDED`

This file is the authoritative overlay for the post-Phase-0 material-evidence branch. It supplements the retained method-benchmark state in `state.md`.

## Retained result

R05 retains the validated one-dimensional correlated random-mass versus matched scalar-null method benchmark, its numerical convergence suite, and its declared finite-box threshold screen.

Those results establish a method distinction within the controlled model. They do not establish that a real HgCdTe specimen occupies the required parameter regime.

## Evidence-gate result

All eight specimen-level reopening gates from issue #395 fail under the currently available evidence:

```text
local variance:       FAIL
correlation length:   FAIL
same population:      FAIL
near critical:        FAIL
resolution:           FAIL
matched null:         FAIL
robustness:           FAIL
decision changing:    FAIL
```

The near-critical literature series is a specimen-selection design envelope. The wafer maps are large-scale drift stress cases. The micro-Laue response is a depth-kernel method benchmark. The STM records define artifact exclusions. None is a substitute for a matched local covariance and spectroscopy dataset.

## Authorization state

```text
new random-mass simulation:   NOT AUTHORIZED
higher-dimensional solver:    NOT AUTHORIZED
full-Kane disorder model:     NOT AUTHORIZED
material activation:          BLOCKED
manuscript claim:              DENIED
```

## Interpretation boundary

`R05_REACTIVATION_NOT_RECOMMENDED` means the current evidence package cannot support reactivation. It does not mean correlated random-mass physics is disproved, nor that qualifying private data cannot exist.

## Reopening condition

Reopen only when new evidence supplies a source-qualified near-critical local mass/gap covariance and matched low-energy spectroscopy with a measured resolution kernel and same-population linkage.

The first reopening action must be evidence ingestion and validation. It must not be a larger simulation or a full-Kane calculation.
