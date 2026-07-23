# R02 decision record: serial `epwread` source diagnosis supported

**Date:** 2026-07-23  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #335  
**Predecessor:** #332 / terminal result `e48abeb2d691f4cef6e4048e0987e205773c728d`  
**Decision:** `SOURCE_DIAGNOSIS_SUPPORTED`

## Question

Does the pinned QE 7.6 / EPW 6.1 serial restart path contain an allocation or shape defect sufficient to explain the exporter-disabled same-state replay SIGSEGV?

## Finding

Yes. The source provides a complete allocation-lifetime explanation:

1. `epmatwp` is allocatable global state.
2. Normal `build_wannier` execution allocates it for `etf_mem == 0`.
3. `epwread` bypasses that normal allocation block.
4. The MPI `epw_read` branch explicitly allocates it before reading.
5. The serial `epw_read` branch does not visibly allocate it before direct reads.
6. The array is subsequently passed to `wigner_divide_ndegen_epmat`.
7. The observed serial replay terminates in that routine at the first division.

The exporter was disabled and the failure occurred before self-energy evaluation.

## Dimension result

The pinned distribution formulas give, for one serial process:

```text
irn_start = 1
irn_stop  = nrr_g * nmodes
irg_start = 1
irg_stop  = nrr_g
nirg_loc  = nrr_g
```

Therefore the existing MPI allocation expression:

```fortran
ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc))
```

also has the correct serial extent.

## Minimal correction

Move the existing allocation and zero initialization above the `#if defined(__MPI)` split in `epw_read`.

This is preferable to adding a second serial-only allocation because it:

- creates one common ownership point;
- preserves the MPI expression exactly;
- avoids branch drift;
- leaves MPI offsets and broadcasts unchanged;
- leaves serial record lengths and direct-read loops unchanged;
- changes no physics or restart format.

## Separate MPI risk

`wigner_divide_ndegen_epmat` declares a fifth dummy extent of global `nrr_g`, while MPI allocates a local fifth extent of `nirg_loc`. The observed serial failure does not test this relation. It is recorded as a latent source risk and is not modified by the minimal serial fix.

## Classification basis

```text
missing serial allocation evidence       direct
observed crash location                  consistent
alternative file-corruption explanation weak
exporter involvement                     excluded
minimal patch structure                  static only
runtime patch validation                 absent
```

## Decision

```text
classification                    SOURCE_DIAGNOSIS_SUPPORTED
minimal inert patch               defined
synthetic shape proof             defined
upstream report draft             prepared
patch compilation                 not authorized
patch execution                   not authorized
MPI validation                    not established
scientific capability restored    no
```

The next possible gate is a separately authorized bounded patch validation. This decision does not create or authorize that gate automatically.
