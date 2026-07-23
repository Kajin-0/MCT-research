# R02 state update: serial allocation patch removes crash; immutable harness stops

**Date:** 2026-07-23  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## Transition

```text
serial epwread allocation diagnosis
  SOURCE_DIAGNOSIS_SUPPORTED
  -> RUNTIME_SUPPORTED

strict immutable serial replay harness
  -> SERIAL_EPWREAD_PATCH_VALIDATION_STOP
```

## Established

- The exact minimal allocation patch applied cleanly to pinned QE 7.6 source.
- One serial QE/EPW build completed.
- All six upstream diamond preparation commands returned zero.
- The prepared state and replay clone contained 168 byte-identical files before replay.
- The exporter-disabled replay returned zero.
- The previous `wigner_divide_ndegen_epmat` segmentation fault did not recur.
- EPW read the saved Wannier state, performed electron-phonon interpolation, executed 216 `selfen_elec_` calls, and reached total-program completion.
- No exporter file was created and all exporter variables were unset.

## Binding stop

The strict harness did not pass.

```text
mutated preexisting file       diam.epb1
before size                    1,137,036 bytes
after size                     660 bytes
before SHA-256                 cae2607e190fbf4ef25ad27f49231bbfff011d5d42f234d86beccefdd9654b55
after SHA-256                  834e3e9735f346b065f8ec270c4cdce672d72a901f684e5afba1e08eac3d29c1
```

The predeclared literal completion strings `Electron Self-Energy` and `JOB DONE.` were also absent, although release-specific runtime text showed self-energy execution and total completion.

Neither the file-mutation policy nor marker contract may be relaxed after execution.

## Interpretation

The source diagnosis is now supported by runtime evidence: allocation before the serial read removes the observed crash.

The replay protocol remains unsuitable for attribution because it does not yet separate immutable consumed state from replay-written files, and its completion marker contract is not release-grounded.

## Authorization

Closed:

- any additional build, preparation, or replay under issue #350;
- patch adjustment or rerun;
- marker substitution or state allowlist relaxation;
- merging the executable patch branch;
- exporter attribution;
- MPI, SOC, CdTe, HgTe, HgCdTe, A1, A2, or A3.

Open only for design:

- trace `diam.epb1` read/write ownership in pinned EPW source;
- determine whether replay should set `epbwrite=.false.` without changing the intended self-energy calculation;
- define immutable consumed-state and declared-output sets separately;
- define release-specific completion observables from stable output sections or generated result files;
- draft a new bounded contract only after those questions are resolved.

## Controlling records

```text
first_principles/b0/r02_epw_serial_patch_validation_terminal_result.json
research/decision_records/2026-07-23-r02-serial-epwread-patch-validation-stop.md
```
