# Conditional single-fixture protocol — NOT ADMITTED / NOT RUN

This is the permitted small native comparison design, **not** a prepared run,
queue or claim that code gates pass. The missing native state bridge closes its
first gate. No native spectra, EXX action/energy or ACE fingerprints exist from
this phase; all such result fields remain NOT RUN.

Proposed one fixture: primitive **two-atom HgTe**, the existing pinned SG15 Hg/Te
relativistic NC pseudopotentials, SOC, HSE fraction 0.25/screening 0.106, cutoffs
90/360/120 Ry, k2/q2, 48 bands, accurate-empty Davidson and 1e-10 convergence
settings. It is an engineering fixture, not the 16-atom/352-band experiment or a
parameter downgrade of that experiment. Both comparison members use **identical**
fixture physical/numerical settings and initial state; only storage differs.
Confirm the 48-band occupancy requirement from the actual native input/output;
refuse if invalid. No empirical gap input or alloy inference.

Use two MPI ranks × one thread, one k pool/exchange group and identical FFT/MPI
layout. A stock-algorithm control may require passive diagnostic instrumentation;
the installed stock binary remains byte-identical. Build that control and the
streamed candidate from the same pinned source, compiler flags and existing
backend libraries. Do not mistake mixed compiler/control differences for storage
effects. Record each binary, source, library, PP and deck fingerprint. Refuse if
initial wavefunctions, G/k index conventions or layout do not match.

Before launch: native old-state capture/import and interruption tests pass;
complete unit/source/build/guard evidence; exclusive MPI ownership verified;
per-rank actual stream/state extents reserved; >=10-GiB disk reserve retained;
RAM admission passes. Connect an owned-family monitor and maximum 600-s wall,
12-GiB family RSS and 4-GiB system-RAM guards. No detached owner or supervisor.
Launch control then streamed member **sequentially**, never two MPI families.
Stop immediately on resource failure, unsupported mode or discrepancy; no
automatic retry, altered physics, more fixtures or campaign.

Capture the first native EXX/ACE initialization, including a common deterministic
G-basis probe independent of eigenvector phases. Record full per-rank direct
exchange action on that probe, exchange energy and normalization, native
`Phi† V Phi` Gram matrices, ACE factors/projectors and their operator action,
source occupations/coverage and global reduction results. Reconcile raw
projectors' basis conventions; prefer their action/invariant contractions when
phases differ. Never accept exit status or only total energy as equivalence.

Preregistered numerical comparison: relative action/Gram/operator defects <=1e-12
with absolute floor 1e-13 in native Ry conventions, and <=1e-12 Ry exchange-energy
difference, with matching native fingerprints. These are strict engineering test
thresholds, not measured material accuracy. A different valid arithmetic path
may fail these thresholds; report and investigate rather than tune them after
seeing results. This protocol also requires a real interruption/restart checkpoint
identity check on the qualified native state. Successful first-action equality
alone does not validate complete SCF restart, full-HSE peak or the 352-band case.

No passive diagnostics, native source bridge or launch monitor has been built by
this phase. Consequently this fixture is not ready. The retained user conditions
require stopping at that gate, not invoking the old unqualified PW executable.
