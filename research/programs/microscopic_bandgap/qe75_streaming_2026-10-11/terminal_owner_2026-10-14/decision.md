# Decision: terminal rule passes non-MPI kernel checks; no new native run

**2026-10-14 15:18 UTC.** Preserved and locally committed the prior scientific
checkpoint as `89922a7`: twelve real rooted HSE control updates, charge error
≤9.590905847289832e-11 electrons; total/Fock −484.05800703870875/
−8.967178784294628 Ry, dexx 2.2422123699072927e-5 Ry, unconverged. Original
owner RESULT remains FAILED; stream never ran. Its EACCES cause remains OPEN.

## New measured evidence

ONE bounded non-MPI sequence exercised two owned user services, each with two
tiny child actors, kernel 128-MiB memory, swap-zero, eight tasks, 12-second unit
deadline and 64-KiB file cap. The children create fresh sockets; only the child
fixture changes its own dumpability. No global permissions change, MPI/QE,
foreign process modification, Calcura or supervisor operation occurred.

| Actual case | Result |
|---|---|
| Live FD EACCES after both authenticated final receipts | Refused; pinned pidfd had no exit event |
| Unreaped child exits | Actual pidfds POLLIN=1, observed Z; only pending, not omission |
| Reaped child exits | Actual pidfds POLLIN\|POLLHUP=17, immutable descriptors retained |
| Exit-zero invocation and empty group | Terminal conjunction accepted; 0.297980 s, cgroup peak 17469440 bytes |
| Real exit-two service | Refused; 0.257810 s, cgroup peak 17596416 bytes |
| Foreign peer cgroup / substituted descriptor | Refused using actual kernel identities |

Both units were collected after the manager references were released; the old
lease registry was unchanged. Typed fake bindings, incomplete rank-final pair,
missing-proc claims while live, incomplete FD information and live parent/group
all refuse. Explicit pidfd-permission and stale-start-identity injections are
labelled models, not actual host permission errors or a forced PID reuse test.
No high-volume fork campaign or namespace manipulation was used.

The first setup-only attempt refused `sd_bus_open_user` with ENOMEDIUM because
the outside process lacked bus discovery environment. This failure is preserved
in `attempt1_bus_failure.json`. Connecting explicitly to the established user
bus without changing environment/global configuration fixed that source defect.
Actual `RefUnit` then retained the original invocation and true exit metadata;
closing the bus connection permitted collection. This is measured lifecycle
evidence, not status inferred from an unloaded unit's default zero fields.

Focused prospective account-path tests independently preserve the strict live
refusal and pending-without-accepted-sample behavior, output-budget and unknown
path refusals. Original SCF numerical tolerances are unchanged. These wiring
models and source checks are distinct from the actual Linux reproducer.

## Outcome and boundary

**PROVEN UNDER ASSUMPTIONS:** socket-bound live acquisition prevents numeric PID
reuse during binding; pinned process exit plus authenticated finals, matching
clean terminal manager and empty group supports terminal FD omission under the
closed-family assumptions. **CALCULATED:** the scoped non-MPI kernel cases pass.
**OPEN:** exact cause of historical native EACCES; actual prospective QE owner
integration, fresh paired trajectory and restart. No material or memory-gain claim.

**STOP / NATIVE RELEASE NOT ISSUED:** the user's first publication gate cannot
currently pass. Kajin SSH authentication was rejected; HTTPS has no credential;
the other existing local SSH identity authenticates as Brooks-Photonics without
access to Kajin-0/MCT-research. No force, credential/permission change, alternate
repository, main or DFT commit is used. Both checkpoints are retained locally.
The next required input is authorized ordinary-Git write access to the existing
research branch. Then finish and freeze the prospective native integration and
fresh identical inputs before considering ONE new bounded pair. Do not rerun
the old control or treat component tests as native pair acceptance.
