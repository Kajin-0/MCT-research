# Prospective tests, confinement and resource boundary — NOT a release

This is a proposed DIFFERENT one-process acquisition domain. It neither passes
nor waives the old strict two-rank FD-inventory gate. Original R07S/16 and
lifecycle R07L/1601 ELF/profile/receipts remain unusable for it. No nonce,
execution profile, build or transient unit is created by this package.

## Required tests before separately authorized scientific execution

1. NEW pinned private postprocessing ELF/source/modules/PP/XML/rho/Phi, no
   old-file edit. Prove the needwf=false branch and all initialization globals;
   test missing/mutated input, forbidden fallback, wrongGamma/SOC/functional,
   double initialization and read-only source path failures. Explicit new
   world-size1 packet schema/reader, with saved_nbnd352 versus probe_count12.
2. Independently qualify singleton MPI under containment: actual worldsize1,
   correct process identity, all helpers/threads within the owned cgroup, no
   remote rank/network access. **One MPI rank is not proof of one process.**
   Installed OpenMPI help-mpi-runtime explicitly requires a PMIx server.
   Whether this build initializes in-process or needs an extra helper is
   unproved without a separately authorized harmless runtime test. If the
   selected strict single-process path needs a PMIx helper, it has NOT met
   this design's process condition: stop, do not silently admit a helper or
   auto mpirun. Any different process contract needs separate review.
3. Component checks: independent |G+k|² kinetic; actual density-to-FFT and
   HartreeG0/mode/charge conventions; local action versus independent explicit
   FFT convolution on full probes; PBE potential against independently
   evaluated functional directional derivatives/gradient-divergence and QE
   baseline; FR beta/D action versus independent angular/projector contraction.
   Compare ALL components to a FRESH admitted trusted QE initialization
   control on the same saved rho. Old refused actions are NEVER a control.
   A control evaluation adds12 query actions/member tested; beyond the primary
   pair's24, count it separately and obtain separate resource authorization.
4. Require physicalG bijections, full rhoG/readback, unchanged Phi and explicit
   Theta images, charge<=1e-8e, kinetic cancellation, component sum/Hermiticity/
   Theta<=1e-8, actual24/4 geometry/density groups and gauge evidence. Native
   density/potential/PP controls must distinguish copied inputs from actual
   applied operator state. Numerical2meV additionally needs the absolute error
   ledger in preferred_path.md, not merely these relative consistency tests.
5. Pin process start/ELF with a pidfd acquired by a trusted child/exec handshake;
   authenticate native begin/final after actual initialization and closed
   packets, and recheck hashes/readback after exit. Manager/wait exit0 AND
   original terminal-empty cgroup, no surviving helper and durable outside
   signoff are required. Missing/live FD denial remains fatal under any
   policy that still relies on that inventory. No JOBDONE/missingPID authority.

## Revised kernel write-confinement design — capability NOT proved

Protect the DFT tree by byte-hashed read-only staging of XML/rho/UPFs and common
Phi into a NEW input subdirectory; no hardlinks/symlinks to protected files,
no member wfc staging. Use a separately scoped output root only. File modes
alone are not a security boundary for the same UID. Mount/bind-RO/ProtectSystem
may require unavailable user-manager namespace privileges; sysctl userns=1
does NOT prove permission. No namespace/service test occurred this phase.

Preferred confinement to QUALIFY is unprivileged Landlock after no_new_privs:
read/execute allowlisted staged inputs and pinned runtime dependencies; handle
write/truncate/create/remove/refer rights, granting writes only to a finite
precreated output-file set. Deny directory creation/rename/link/unlink and
outside /tmp, /dev/shm, original saves and DFT paths. Source the correct
ABI-supported mask, not all newer header bits. Read-only VERSION query returned
**ABI7**, errno0 on6.17.0-41; no ruleset/restrict_self test proves enforcement.
Existing writable FDs/mappings bypass path-open restrictions: the trusted
pre-exec handoff must close inherited descriptors/mappings (apart from strictly
defined bounded stdio established under policy), then pin/report that state.
No inherited socket proves native identity. Do not accept an inherited unknown
write FD, SCM_RIGHTS, foreign output device or a permissive TMPDIR fallback.

Preallocate packet/stdout/stderr files; NEW native code must write these
existing exact inodes rather than old STATUS=NEW/dynamic restart paths.
Bound regular-file sizes and actual allocation, including deleted-open files.
Fixed-file allowlisting can bound logical payload, but RLIMIT_FSIZE is not an
aggregate quota; sparse extent metadata, backend temp files, memfd/shm and
outside-holder logs must be included. Deny unexpected bootstrap file creation;
if MPI/HDF5 needs one, fail and review its exact role rather than open /tmp.
Landlock TCP controls do not by themselves block UDP/all networking. A tested
socket-family/seccomp or namespace policy must prevent nonlocal network access;
pathname owner Unix IPC needs a narrow, authenticated exception. No such filter
or capability is claimed implemented here.

The outside holder must ALSO have bounded memory/output paths, stdio capture,
pending/result writes and readback workspace; a small startup RSS is no full
reader bound. A source-complete streaming reader or separately guarded reader
is required. It cannot silently turn a pipe into unbounded outside-cgroup disk
or memory. All owner-written files count in the SAME14GiB aggregate budget.
Kernel confinement may support a revised local contract, but it is not
host-wide MPI absence, a continuous quota or an authorized policy change.

## Resource audit and finite rejection criteria

Known logical one-rank dimensions:N21595, Ng173631, grid80^3, nkb712. Selected
buffers439,686,504B exclude important allocations and possible descriptor
padding. Expected same-field packet90,028,704B/member; input XML/rho/PP about
6MB/member plus8.81MB common probes. A NEW header changes that exact byte
formula and must be frozen from actual source. No copy of243.5MB/member wfc
is needed. No whole-SCF or parallel memory benefit is claimed.

Unknown complete simultaneous allocations: PP radial tables and USPP/SOC
helper arrays, global-sort/FFT descriptors/plans/workspace, PBE derivative
temporaries, XML/HDF5/library heaps/threads/MPI helper state, native output and
outside-reader peak. No timing upper bound derives from old~1GiB/4s or the
selected439.7MB subtotal. Known algorithmic work removes diagonalization and
352-column loading but still includes12 spinor local FFT applications and
large beta contractions;600s remains a hard stop, not guaranteed completion.

Any future contract retains unit RAM<=12GiB/swap0/tasks<=12/wall<=600s, host
available>=4GiB/free disk>=10GiB, aggregate retained output<=14GiB, one owned
family, fresh short socket<=107bytes, source/PP/input/ELF pins, no unsafe
outside-holder growth. Hard kernel memory/task/time controls are distinct from
sampled host/disk/output accounting. Without a tested quota or another actual
kernel aggregate-allocation bound, residual between-sample bursts/external
writers must remain explicit and independently reviewed; no false guarantee.

FALSIFY/STOP on any wrong physical label/unit/flag, fallback/import/occupation
change, component/gauge/Theta mismatch, input mutation, unexplained process or
output, unsupported containment, missing cross-validation/error budget, cap
crossing or inability to complete in scope. Do not rerun a failed identity,
relax old gates or reinterpret fixed saved-density output as SCF. Execution
NO-GO persists until separate reviewed implementation/admission authorization.
