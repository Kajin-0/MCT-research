# Complete runtime bounds: what is proved and still missing

**No native MPI/QE resource envelope is completed here.** Physical/experimental
caps remain unchanged. This section separates kernel caps, conditional operator
bounds, actual reservations and producer coverage.

## New non-MPI probe

One fixed C process, no fork/exec/MPI, no IP connection, no C-created data files.
The actual kernel sample has memory.max64MiB, swap.max0, pids.max4,
oom.group1, pids.current1; no OOM/max event. Manager/cgroup memory peak2MiB.
One synced 4096-byte extent is byte/block checked on the supported ext4 backend,
with quota status/headroom checked. Pipe capture is limited to32KiB; HELLO's
own buffer is4096 bytes and a final DONE/refusal is bounded. Per-file16KiB/core0,
nofile64 and 8s manager+1s stop limits are verified. The owner remains outside
the cgroup and is sampled independently. A failed isolation observation is
not qualified merely because these resource checks pass.

The single run refused before ACK, so its sampled lifetime is short; it cannot
certify a sustained100ms monitor cadence, a45s MPI family peak or a continuous
4GiB/10GiB host floor. Shared manager/journal costs and unrelated actors remain
outside the family/accounting theorem. Reservation of our blocks is not a
quota on other writers or a reservation of the host's remaining disk.

## Conditional resident-mapping bound and telemetry obstruction

**PROVEN UNDER ASSUMPTIONS.** Suppose no more than N live process leaders
exist, each has a hard address-space ceiling A installed before exec, starts
with VmSize<=A and cannot raise/bypass it. Exact resident mappings occupy
virtual address space, including each separately mapped alias. Thus

    summed exact resident-mapping bytes <= N A + bounded outside mappings.

TasksMax constrains task creation; inferring N additionally requires bounded
actual membership, no unadmitted migration and no limit raise. Treating every
task as a leader is then conservative. Retain the prior migration counterexample.
For example N32, A256MiB and outside128MiB gives8.125GiB, below the unchanged
12GiB summed-RSS guard. **These AS/outside limits were not installed or tested
on MPI.** This is an independently checked candidate bound, not a native memory
prediction or physics change. Raising a limit, initial mappings already above
it, uncounted/migrated processes, or unbounded outside control invalidates it.
The initial draft extended this directly to **reported** proc RSS. Source
review rejected that extension: upstream [Linux6.17 mm counter helpers](https://raw.githubusercontent.com/torvalds/linux/v6.17/include/linux/mm.h)
use per-CPU reads, and [proc memory snapshots](https://raw.githubusercontent.com/torvalds/linux/v6.17/fs/proc/task_mmu.c)
explicitly allow inconsistent snapshots. A reported-statistic bound needs a
separately certified one-sided accounting/snapshot error E:

    reported sum <= N A + bounded outside mappings + E.

E is UNKNOWN here; `monitored_rss_upper_bound` refuses without it. No raw-proc
memory bound, vendor-kernel precision or continuous measurement is manufactured.
memory.max512MiB is different kernel charge accounting; it neither replaces
the RSS theorem nor reserves completion capacity. Kernel accounting may have
documented transient overrun/reclaim/OOM behavior; caps do not prove success.

## Aggregate-file counterexample and indispensable producer quantity

**PROVEN.** RLIMIT_FSIZE=L and NOFILE=F do not imply aggregate retained file
bytes<=L F. One process can repeatedly create a new file of sizeL, close it
and retain it, using one data fd at a time. For arbitrarily chosen finite m,
retained bytes=m L, without violating either limit. TasksMax and a finite
runtime deadline supply no numerical m absent an independently certified
operation/rate or producer-generation bound. No such writer was executed.

Consequently exact aggregate admission requires a bound on **all retained
producer generations/inodes**, their maximum extents, simultaneously live and
retained aliases, metadata and block rounding. Installed sm default16MiB and
a conditional two-segment32MiB payload are insufficient: PRRTE/PMIx session,
topology/data-store/error generations and all selected components/path defaults
must be covered. The installed default `/dev/shm` cannot be hidden from the
certificate; controlled private backing paths need actual enforcement/readback.
No false complete sum is returned by `complete_budget` when any term is unknown.

**Ranked remaining resource input:** one complete pinned local-runtime
producer/generation/path certificate for the exact two-rank no-respawn harness,
or a separately proven aggregate enforcement mechanism compatible with strict
ext4/quota/reservation policy. No permission/global configuration changes,
tmpfs substitution or unbounded native discovery run is proposed. Namespace
realization/production live owner admission remain prerequisites before this
certificate could authorize even the small MPI run. QE's broader wave/state,
HDF5/FFT/ACE/RAM/output gates remain independently unpassed.
