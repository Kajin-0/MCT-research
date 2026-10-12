# Finite bridge-phase handoff

- Separate latest user authorization; start MCT b1a4772 on existing research
  branch. Historical BLOCKED goal untouched; no goal APIs, agents or sessions.
- Read pinned QE source and DFT AGENTS. All modifications are MCT artifacts or
  new DFT `.local/qe75_lowram_20261011/native_bridge` generated copies/objects.
  Existing q-e candidate, previous private PW, stock binaries, dirty DFT files
  and supervisors are unchanged. Preservation is recorded in validation.json.
- Implemented native old-state packet v2 and bridge source transformer. Packet
  covers xi, old occupations, current wg/et, outer counter/mode, nine scalars.
  ETHR must be included: outer continuation retains it, and actual stock
  zero-counter import ignores the text-file ETHR/ET. Test retains that negative.
- Native import uses unchanged exxinit signature with a private import flag;
  existing module callers' ABI is not changed by adding an optional parameter.
  Skip source producer and ACE rebuild; retain exact G/q/FFT map checks.
- Natural inner iteration-limit save added; partial-k counter unchanged;
  wavefunction import now refuses atomic/random fallback.
- Post-punch transaction binds completed native save/PPs/counters/mix files and
  every rank stream/state packet. Hardlinks plus fsync/atomic global pointer.
  Receipt-free retirement failure is refused. Native qualification FALSE.
- Old reserved-file/STATUS-new incompatibility fixed by explicit reserved-store
  API, typed 64-bit per-rank requests and checked C fallocate/quota admission.
- 21 serial methods + 24 inherited storage regression cases PASS; 14 native-unit
  compiles and six unchanged reader/ACE checks PASS. Private mixed-object binary
  links, never executed. Native XML/HDF5/FFT/MPI roundtrip remains NOT TESTED.
- Private binary: `native_bridge/link-only/pw.bridge.RUNTIME_REFUSED`.
  Exact source directory/binary/source hashes and child RSS in build_results.json.
  It requires a real owned monitor/lease/admission handshake; none is supplied.
  Never set runtime_authorized simply to bypass that gate.
- Final measured free disk ~30.259 GiB, available RAM ~29.658 GiB; no MPI family
  observed. Nominal 22-GiB stream + 10-GiB floor fails; no large file allocated.
- STOP_NATIVE_READBACK_AND_RUNTIME_OWNERSHIP_BOUNDARY, not full restart success.
  One next action: qualified owned monitor/lease + exact small fixture profile,
  then the existing conditional matched native readback/action protocol if all
  gates pass. No native run, retry, broad campaign or 16-atom admission implied.
- Full-stream rolling backup would exceed the single-generation storage
  contract. Consumption intentionally removes recovery availability before any
  in-place native writes. Preserve this limitation rather than silently promise
  last-checkpoint recovery through arbitrary producer replacement.
- No material gap, impurity t_H or x_c; existing scientific no-go results preserved.
