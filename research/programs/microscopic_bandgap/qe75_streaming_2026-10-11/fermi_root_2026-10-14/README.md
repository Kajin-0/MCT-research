# Private Fermi-root qualification and one native control (2026-10-14)

Read [decision](decision.md), [reset handoff](handoff_ledger.md) and
[native numerical qualification](control_numerical_qualification.json).
Root solver passes; control12HSE updates/charge/finalreadback recorded; production
owner fails on post-final rank0 FD EACCES. No stream, retry or HSE convergence.

- [Frozen prospective policy](preregistration.md), [freeze](frozen_protocol.json), [resume preflight](resume_preflight.json).
- [All18 retained inputs](input_audit.json), [root proof/physical scope](derivation.md), [source qualification](root_qualification.json), [independent checks](validation.json).
- [Actual native scalar-object check](native_float_validation.json), [private builds](build_results.json), [solver patch](solver.patch).
- [Actual full-SCF values](numerical_result.json), [raw owner refusal](raw/control/RESULT.json), [native provenance](raw_provenance.json), [registry](discovery_registry.md).

No command in this package authorizes another run. Do NOT invoke owner run,
prepare/build or restart against consumed ATTEMPT records. Cheap read-only
summarize.py checks existing snapshots; all source/physical/frozen gates remain.
No broad regression suite needed. Preserve the unmodified failed owner record.

Raw QE pw.out is byte exact, including trailing formatter spaces; the scoped
Git attribute ignores whitespace ONLY there. Large scientific payloads remain
privately retained/hashed; no UPFs, executables or native scratch committed.
