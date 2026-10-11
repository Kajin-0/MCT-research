# Persistent finite-phase handoff

- Task is separate from historical BLOCKED /goal; no goal API, agent/session,
  tmux, supervisor or stock-QE operation occurs.
- Start MCT `ea8823e`, existing `research/hgcdte-impurity-tmatrix-20261010`.
- Read full first package, DFT AGENTS, actual pinned source and preservation
  evidence. Stock/dirty state and 17 protected pins remain identical.
- New code/tests under `qe75_streaming_2026-10-11/checkpoint_phase`; compiled/tiny
  scratch under DFT `.local/qe75_lowram_20261011/checkpoint_phase` only.
- Implemented: no-copy hard-link capsules, atomic global manifest, SHA-256,
  exact provenance/layout matching, corruption/version/rank/symlink refusals,
  adoption/consumption and identity-checked cleanup. Fortran read-only storage
  adapter tested against a sealed still-open writer's normal delete-close.
- Implemented/tested: C ext4/block/quota probes, real tiny `fallocate` reservation,
  per-rank reservation/rollback, tmpfs refusal; Python checked-64 admission and
  runtime predicates. Not wired into native source/monitor.
- Initial project limit query EPERM was inconclusive. Separate unprivileged
  Q_GETINFO ESRCH establishes that quota type OFF. No privilege escalation or
  quota change. Do not reuse the early uncertainty as final blocker.
- Newly decisive negative: first package missed the outer-EXX stop/export branch.
  `close_outer_stop_gate.py` patches only a new private `electrons.f90` copy;
  compiled successfully. Review patch stored. Old compiled candidate untouched.
- Native restart needs old ACE/occupations, not a current-basis reconstruction;
  tiny negative-definite ACE counterexample retained. Native `punch` completes
  separate state files after electrons, so stream commit alone is insufficient.
- Final: 15 checkpoint/guard test methods and 24 storage regressions PASS. Generic
  capsule semantic/native qualification remains FALSE. No full native bridge,
  diagnostic build, native launch monitor or MPI/FFT/HSE fixture exists.
- Decision STOP_NO_NATIVE_STATE_BRIDGE. Do not run `pw.qstream.UNVALIDATED` or
  silently skip the native-state gate. One conditional two-atom fixture protocol
  retained, limits <=12-GiB family RAM, >=10-GiB disk reserve, <=600 s each.
- Original 22-GiB store currently fails new disk reserve; no 22-GiB allocation.
  No 16-atom run, queue, retries, paid resources or material bandgap/x_c claim.
- Next necessary work: implement native capture/import closure, then monitor and
  guard integration; native comparison remains conditional on those proofs/tests.
