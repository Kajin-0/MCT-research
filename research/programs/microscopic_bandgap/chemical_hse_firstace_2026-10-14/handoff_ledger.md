# Context reset — 2026-10-14 23:14 UTC

Baseline: clean pushed `40d2b9e`; bounded 8-atom HSE Γ/q1 first-ACE pair authorized.
**Result: owner failed before MPI, QE never started, Cd not run.** Inputs and
source/ELF/PP/reference pins froze beforehand. Three private objects compile and
link. No HSE energy, wave, operator matrix, peak, timing, or chemical response
exists. Prior PBE +0.392177 eV and all historical failures are unchanged.

Private DFT root:
`.local/qe75_lowram_20261011/chemical_hse8_firstace_20261014/`.
Candidate `build4/pw.hse8.firstace` is compiled but unexecuted. It uses the pristine
archive plus observers/stop in three objects, without streaming or the 48-band
Fermi solver. Frozen domain: 8 atoms, 176 spinor bands/144 electrons, SG15 FR NC,
a = 6.46 Å, 50/200/Fock-200 Ry, FD 0.001 Ry, HSE 0.25/0.106 Bohr⁻¹, Γ/q1.
Preliminary source SCF threshold is 10⁻⁹ Ry. The post-punch first-ACE stop leaves
`conv_elec=false`; diagnostic exit 0 would not mean HSE convergence.

Failed unit: `r07-owned-1a2876e4842d489fb357a487bb8799eb.service`.
Invocation: `c96634989d814adf9205d14559a88ad9`.
READY/REFERENCED exist; LAUNCH/RANKS/GUARD_RESULT/pw.out/FINAL are absent.
Manager exit 1 is retained; original cgroup is absent, known lock free, and old
ledger exact. Kernel peak 12,955,648 bytes is owner setup only. The frontend
FileNotFoundError for missing GUARD_RESULT is recorded. Underlying original
service stderr was discarded; do not fabricate it from the reproducer.

The frozen socket address is 114 bytes. Linux `sun_path[108]` includes the NUL.
Exact source ordering places bind before MPI creation. One real non-MPI bind
reproduced long-path refusal and successful 105-byte `.../host/s`, followed by
close and inode-checked removal. This does not qualify a native owner or MPI run.
Reuse of current failed-attempt state is refused.

`prospective_short_socket.patch` is **unapplied**. It proposes a fresh `p2` root,
host/Cd socket lengths 103/101 bytes, pre-service address validation, stronger
attempt-state refusal, and explicit packet-root binding. No `p2` directories,
inputs, services, or queued jobs exist. A future corrected pilot requires a new
authorized freeze/evidence scope; do not retry the old pair or promote its FAIL.

Three focused source/reference/refusal tests passed in 0.032 seconds. Frozen pins
and protected stock/dirty-DFT snapshots match bytewise. Private objects/ELF,
prepared inputs/reference, and immutable manager/journal evidence are retained.
No old source, supervisor, session, Calcura, goal, 16-atom target, main, or DFT
commit was changed.

Read decision, preregistration, verification, owner_failure, address_result, and
DFT AGENTS. Finish this finite failed-owner scope with research commit/push using
the existing Kajin SSH identity. Next science remains the corrected matched HSE
first-ACE acquisition. Do not launch more PBE grids or invent HSE/material `x_c`.
