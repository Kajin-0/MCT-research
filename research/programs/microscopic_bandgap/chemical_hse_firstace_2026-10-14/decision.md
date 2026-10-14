# HSE first-ACE pilot: owner failed before MPI

**FAILED OWNER / HSE NOT RUN.** The sole host attempt stopped before MPI or
the private QE executable started. Cd was not launched. This assignment produced
no HSE energies, spectra, operator matrices, numerical residuals, or HSE resource
measurements. The accepted PBE response and all historical failures remain intact.

## Measured blocker

The frozen host socket pathname is 114 bytes:

    .../chemical_hse8_firstace_20261014/pair/host/lease.sock

Linux pathname AF_UNIX sockets have 108 bytes of `sun_path` storage, allowing
at most 107 pathname bytes plus a terminating NUL. The copied launcher omitted
this preflight check. One real non-MPI bind on the exact 114-byte address raises
`OSError: AF_UNIX path too long`; the shorter 105-byte `.../host/s` binds
successfully. That disposable socket was closed and its inode checked before
unlink. [address_result.json](address_result.json) records these observations.
The installed primary C header defines `char sun_path[108]`;
[unix_header_evidence.json](unix_header_evidence.json) pins the header.

The original unit `r07-owned-1a2876e4842d489fb357a487bb8799eb.service`, invocation
`c96634989d814adf9205d14559a88ad9`, retains manager status `exit-code`, exit 1.
READY exists; LAUNCH, RANKS, pw.out, GUARD_RESULT, and FINAL do not. The frozen
guard binds its server after READY and before MPI/PW creation, so this address
cannot reach the executable. Its cgroup is gone and the known lock is free.
Kernel MemoryPeak of 12,955,648 bytes belongs to Python owner setup, not HSE.

The original frontend exception is `FileNotFoundError` while reading the missing
GUARD_RESULT. The wrapper discarded underlying service stderr before raising;
the reproduced bind error must not be quoted as retained historical stderr.
Source ordering, exact-address reproduction, and manager/file observations
localize the unavoidable bind failure. See [owner_failure.json](owner_failure.json)
and [the retained unit journal](host_unit_journal.jsonl).

The user required: **“No retries; if first member fails owner/resource/science
fail-closed and do not launch Cd.”** That rule applies to this owner failure.
There was no second host unit, native launch, or Cd attempt. A corrected pathname
cannot promote the original result or permit reuse of failed-attempt state.

## Source work retained

**COMPILED / SOURCE-CONDITIONED, NOT NATIVE VALIDATED:** three privately modified
QE 7.5 objects compile and link against the untouched installed archive and
backends. Source is based on pristine tagged exx, electrons, and run_pwscf files.
The direct `vexx_k`, `aceupdate_k`, and `vexxace_k` arithmetic bodies remain
byte-identical; external matcalc remains in the unchanged library. Failed initial
source-anchor checks and their corrections are preserved. No original QE source,
stock executable, or protected DFT file was edited. Commands and ELF, compiler,
library, and source hashes are recorded in [build_results.json](build_results.json)
and [native_changes.patch](native_changes.patch).

The compiled observer captures 176 source orbitals, direct Fock action, Gram
matrices, compressed ACE and its on-span action, rank-specific G/FFT descriptors,
occupations, and first Fock energy. Six original physical Γ vectors are embedded
using exact reciprocal labels and acted on by direct Fock. Native local-potential
actions before and after exchange activation, together with density maps and
rhoR/rhoG, are intended to qualify a fixed-density projected operator change.
The stop saves `conv_elec=false` after complete first ACE and post-punch
publication. Diagnostic exit 0 would indicate pilot completion, not HSE
convergence. These paths compiled but never executed; numerical and readback
correctness remain unqualified.

Matched 8-atom, 176-band, 144-electron inputs froze before the attempt: a = 6.46 Å,
SG15 fully relativistic NC, 50/200/Fock-200 Ry, FD sigma = 0.001 Ry, HSE fraction
0.25 and screening 0.106 Bohr⁻¹, Γ/q1. The retained reference Gram error,
1.86 × 10⁻¹⁵, checks the PBE frame rather than HSE. Preliminary admission observed
29,728,247,808 bytes of available physical RAM and 64,714,117,120 bytes of free
disk. The 12 GiB/swap-zero/tasks-12/600 s and sampled 14 GiB output contracts were
configured. The 2.23 GB EXX subtotal and 320–365 s timing estimate remain
heuristics. No physical resource impossibility has been established.

## Prospective remedy and next scientific acquisition

[prospective_short_socket.patch](prospective_short_socket.patch) is **unapplied**.
It proposes a checked short pathname in a fresh `p2` root: 103 bytes for host,
101 for Cd. It retains typed nonce/PROFILE/JOB/cgroup authentication, refuses
READY/REFERENCED/escrow or other prior-attempt state, and passes the fresh root
explicitly to packet intake. It changes neither physics nor acceptance thresholds.
Future preflight must check both addresses before service creation and use a new
versioned freeze/evidence package. No `p2` directory or job was prepared here.

The next useful acquisition is the same matched Γ/q1 HSE first-ACE pair after
the small launch fix and a fresh authorized scope. It addresses functional
dependence more directly than further PBE grids. Full-SCF cost cannot be inferred
from this failed setup; it still requires actual first-ACE measurements.

Three focused source/reference/refusal checks pass. Frozen pins and protected
stock/dirty-DFT/old-ledger snapshots match. Sources, prepared inputs, and failure
evidence are archived. Other sessions, Calcura, supervisors, and the historical
goal are untouched. **STOP this failed-owner scope after commit/push.** HSE
chemical response, converged HSE, whole-SCF memory improvement, and physical
`x_c` remain unmeasured.
