# R02 state update: serial `epwread` source diagnosis supported

**Date:** 2026-07-23  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## Transition

```text
serial epwread source diagnosis
  -> SOURCE_DIAGNOSIS_SUPPORTED

minimal patch validation
  -> NOT AUTHORIZED
```

## Established from pinned source

- `epmatwp` is five-dimensional allocatable global state.
- Normal `build_wannier` execution allocates it when `etf_mem == 0`.
- The `epwread` restart branch bypasses that allocation block.
- MPI `epw_read` restores the allocation explicitly.
- Serial `epw_read` reads and later divides `epmatwp` without a visible allocation.
- The observed exporter-disabled serial replay failed at that downstream division.
- For one serial process, `nirg_loc == nrr_g`, so the existing allocation expression has the required serial extent.

## Minimal inert correction

Move the existing allocation and zero initialization above the MPI/non-MPI preprocessor split.

The proposal preserves:

- MPI allocation dimensions;
- MPI offsets and broadcasts;
- serial record lengths and direct-read loops;
- restart file formats;
- Wigner degeneracies;
- all scientific contractions.

## Separate unresolved risk

The MPI actual fifth extent is `nirg_loc`, while the Wigner routine declares an explicit dummy extent of `nrr_g`. This did not cause the serial failure and is not modified by the minimal patch.

## Authorization

Open:

- static source inspection;
- synthetic allocation and bounds tests;
- inert patch review;
- upstream report review.

Closed:

- compilation;
- serial or MPI execution;
- patch application and execution;
- another preparation or replay;
- SOC and material calculations;
- automatic executable successor.

## Controlling records

```text
first_principles/b0/r02_epw_serial_epmatwp_source_audit.json
research/capability_audits/qe76_epw61_serial_epwread_epmatwp_diagnosis.md
research/decision_records/2026-07-23-r02-serial-epwread-source-diagnosis.md
research/patch_proposals/qe76-epw61-serial-epwread-epmatwp-allocation.patch
```
