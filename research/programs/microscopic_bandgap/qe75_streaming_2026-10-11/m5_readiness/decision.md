# M5-readiness decision: new component gates pass; native execution remains blocked

Finite phase starting from `1d74a0d`, existing branch
`research/hgcdte-impurity-tmatrix-20261010`. Historical blocked goal unchanged.
No PW, HSE, MPI launcher or real MPI communicator was run. Both new private
readiness executables were linked and fingerprinted, never executed.

| Gate | Result and limitation |
|---|---|
| Typed PROFILE/JOB binding | **PASS COMPONENT:** two independently computed canonical digests; JOB binds PROFILE. Native API no longer demands equality of hashes of distinct objects. |
| Compiled lease transport and two real peers | **PASS COMPONENT:** exact C wire ABI, real Unix peer credentials/pidfds/flock, nonce, unique ranks, lost/dead rank, altered digest and stale identity refusals. Peers are serial test executables, not MPI ranks. |
| Native world-rank registration adapter | **COMPILED AND LINKED:** real `mp_world` rank/size, registration and all-rank checks before state reads; native scope demands a different receipt from ABI tests. Real MPI collective behavior **NOT RUN**. |
| First-ACE direct/energy/Gram/projector/action instruments | **COMPILED BOTH MODES / SERIAL CODEC CHECKED:** deterministic global-G probe, raw Phi/V-Phi/Gram/energy/occupations before Cholesky, factor/xi/ACE-probe action afterward. Native values and noninterference **NOT RUN**. |
| Existing wave/density/ACE HDF5 decoding | **PASS BITWISE:** pristine QE serial `qeh5_module` versus independent h5py, 1,208,137 complex values. Existing files unchanged. Does not validate MPI scatter, SCF restore or either stop path. |
| Exact component allocation formulas | **PASS UNDER DESCRIPTOR ASSUMPTIONS:** signed-64-bit stream/state/diagnostic extents verified against emitted serial files. Actual small FFT descriptor and complete native output envelope **UNCERTIFIED**. |
| Common initial-wave certificate | **BLOCKED:** inspected save is 44-band/k4/Fock180Ry, fixture is 48-band/k2/Fock120Ry. It is not relabelled as a matched seed. |
| Global process inventory | **UNKNOWN / REFUSE:** 36 mappings unreadable in validation snapshot; no permission change or inference that unreadable processes are harmless. |
| Production native admission / matched fixture | **NOT ISSUED / NOT RUN:** M4 guardian is still JSON/fake-worker-only. Native binary packets and bridge-child mapping require production integration; component broker cannot issue native authority. |

The first decisive failure boundary remains **production ownership/state admission**.
Linked instrumentation is not a live native lease, common state or restart
certificate. Its absence, incompatible seed, missing actual layout/output bound
and UNKNOWN inventory each independently forbid the conditional fixture. No
600-second or near-12-GiB native experiment was attempted.

**Independent negative:** ACE agrees with direct exchange on its interpolation
span, not generally on an arbitrary deterministic G-space probe. The synthetic
`V=-I` / two-column subspace counterexample gives unequal direct/ACE probe actions
while agreeing exactly on the source columns. The eventual test must compare
control-direct with streamed-direct, and control-ACE with streamed-ACE. It must
not demand direct=ACE outside that span or manufacture equality by changing the
probe. This is an established ACE property, not a novelty claim.

**Validation:** [78 focused methods](validation.json): 13 new readiness, 7 M4
preflight, 17 M4 lifecycle, 21 retained bridge-codec, 15 checkpoint and 5 source
checks. Twelve native-unit compiles pass, four core exchange/energy/ACE bodies
are byte-identical to M3b, and both private candidates link with matching dynamic
backends. Compilation peak ~185 MiB is not a native SCF peak. See
[build_results.json](build_results.json), [link_results.json](link_results.json),
[readback_results.json](readback_results.json) and [unit_results.json](unit_results.json).
Original stock QE, original 352-band inputs, dirty DFT tree, 17 protected
input/PP/supervisor pins, prior candidates and tmux sessions remain unchanged.
Final tested lease holders/owned workers are empty.

**HDF5 qualification caveat:** the installed parallel-HDF5 dependency transitively
loads libmpi. The decoder never initializes MPI or runs PW; explicit exported
MPI/PMPI Init/Init_thread refusal stubs are independently exercised and the
readback passes with those traps present. This is not a claim that its dependency
graph lacks MPI. The initialization/stub defects in the initial serial harness
are retained in [contract_and_failures.md](contract_and_failures.md); stock QE and
the real files were not defective or modified by those corrections.

**Decision — STOP.** Source and serial-I/O gates materially advanced; M5 is not
ready for native execution. A further scoped phase would need the production
native packet/hook integration and independently certified matched initial state,
actual small layout/output lifetime bound and complete ownership evidence. These
are engineering inputs/gates, not physical HgCdTe results. No full 16-atom run,
lowered target physics, empirical fit, physical gap or `x_c` is claimed.
