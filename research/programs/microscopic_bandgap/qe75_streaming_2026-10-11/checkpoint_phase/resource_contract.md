# Exact admission arithmetic and qualified reservation primitives

**CALCULATED / IMPLEMENTED:** checked signed-64-bit arithmetic, filesystem-block
rounding, local ext4 identification, user/group/project quota probes, per-rank
exclusive reservation and rollback, physical-RAM/disk/wall predicates. These
are library APIs and unit tests; they are **not wired into a native launch monitor
or producer callback** and do not establish safe native runtime.

For rank extents `B_r=16 R_r Nband_r Nq`, calculate each block-rounded extent
separately, plus a declared bounded output/state envelope. Require

`available_blocks × block_bytes >= sum(rounded_extents) + output_envelope + 10 GiB`.

Every multiply/add/round operation rejects signed-64 overflow. Compare the
required allocation to each active quota's hard and soft byte headroom (Linux
generic quota limits use 1024-byte blocks); do not depend on grace. Missing or
unreadable inventory refuses. Actual new files' owner/group/project are checked,
not merely the parent directory. User/group quota types return `ESRCH` here.
Project `Q_GETQUOTA` initially returned **EPERM**; a separate read-only
`Q_GETINFO` returned **ESRCH**, establishing that type is not enabled. EPERM alone
was never interpreted as unlimited. No privileges, quotas or permissions changed.

Reserve each owned new regular file using 64-bit `fallocate`, then `fdatasync` and
`fstat` the real logical size and allocated blocks. Reject sparse/nonreserved
extents, shared/preexisting/foreign inodes, unknown/non-ext4 backends and tmpfs.
Each step rechecks physical reserve. On failure only newly created matching
inodes are rolled back; existing collision files are preserved. This protects
admitted stream extents from later lack-of-space writes under the documented
local-filesystem contract. It is not immunity to I/O failure or proof of unlimited
quota for other QE files. The output envelope is an admission budget, not a
promise that arbitrary native outputs have been physically preallocated.

Admission requires at least `12 GiB + 4 GiB` MemAvailable. Runtime predicates
reject family RSS >12 GiB, MemAvailable <4 GiB, free disk <10 GiB, elapsed wall
>=600 s, bad/nonfinite time or failed filesystem probe. Family measurement,
exclusive MPI ownership and termination of owned descendants must be connected
by a launch monitor before any native job. No monitor/job/queue is created here.

Measured after small tests: **30.2890 GiB** available disk, **29.6643 GiB** available
physical RAM, filesystem block 4096 bytes. Small two-rank kilobyte reservation
tests pass. The **original nominal 22-GiB stream alone** plus 10-GiB disk reserve
already exceeds current availability; a 1-GiB output envelope strengthens the
refusal. No 22-GiB file is created or reserved. This directly refuses the
16-atom pilot under the new guard; the user did not authorize that pilot here.

Actual tests include block-rounding/overflow, quota/soft-limit/unknown-inventory
refusal, RAM/disk/time rejection, two per-rank ext4 reservations, rollback after
a preexisting second-rank collision and tmpfs refusal using an anonymous memfd.
They allocate only kilobytes. Other filesystem backends, active-quota enforcement
and live multi-rank resource monitoring are not claimed validated.

Primary API references: [Linux fallocate](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/fallocate.2),
[quota queries](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/quotactl.2),
[fsync](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/fsync.2).
All quantitative admission rules are explicit project engineering policy;
successful small reservations are not a material or full-SCF memory certificate.
