# M4 finite-phase handoff

**Outcome:** foreground fake-family ownership/lease/resource gate PASS SMALL-SCALE;
native M4 integration/admission BLOCKED; M5 NOT RUN. Start `f0d948e`; branch
`research/hgcdte-impurity-tmatrix-20261010`. See [decision.md](decision.md),
[validation.json](validation.json) and the parent [EXECUTION_PLAN.md](../EXECUTION_PLAN.md).
The historical blocked goal is unchanged.

Read DFT `AGENTS.md`, the retained M3b/checkpoint decisions and
[ownership_and_limits.md](ownership_and_limits.md) before using these files.
All disposable work is under DFT `.local/qe75_lowram_20261011/runtime_admission/`;
no DFT commit. Stock QE, original 16-atom/352-band decks and all 17 protected
input/PP/supervisor pins were preserved. `calcura:$0`, `commander:$1`, `research:$3`
were read-only inspected and preserved. Validation ended with no live owned
workers, no kernel lease holder and a FINISHED own ledger; recheck live state.

Reproduce focused tests from this folder using the existing MCT environment:

```bash
/home/User/repos/MCT-research/.venv/bin/python validate.py
```

This runs exactly five bounded suites, copies their small evidence, checks
fingerprints and protected state, and inspects preflight; it never starts PW or
MPI. The venv is needed for retained NumPy checkpoint tests; no install is needed.
If the global own ledger is non-FINISHED, stop instead of clearing it. Tests use
unique new job roots. Do not reset/reuse an old root or take over an unknown lease.

`fixture_preflight.py check` is read-only apart from its evidence JSON.
`fixture_preflight.py link-control` is a one-shot private link from existing M3b
stock-mode objects and refuses an existing output. It has already run; do not
relink or execute its binary to bypass qualification. Control:
`pw.control.M4_UNVALIDATED`, SHA256
`8d06ab83f3c7d0d683f2a371e10b7f85c8b351c87ec44dd2687c8f5f48b83500`.
Stream candidate remains `pw.bridge.RUNTIME_REFUSED`, SHA256
`b19a730cb09e945f0f9abd9ce9aca599cd9a8423aadf0d9f383f7da50ee835ff`.
The Python coordinator acquired a live-lease fence; no new native Fortran source
or streamed executable was built or run in M4.

Retain the decisive negatives: dual cleanup-authority crash needs explicit
identity-verified reconciliation; unreadable mappings prevent global MPI proof;
native rank registration, profile binding, diagnostic/readback, layout/output
bound and common initial-wave certification are absent. Original nominal 22 GiB
plus 10 GiB reserve still does not fit. No full-size fixture, supervisors,
queue, empirical fit, physical gap or `x_c` is authorized by this handoff.

Private first failed suite preserved a canonical-hash framing mismatch; a later
failed suite preserved the unreadable-maps refusal. A standalone worker test
then found a missing module search path. These software defects were corrected;
the strict native inventory refusal is retained. The last validated 65 methods
are the acceptance record, not a claim that those early runs passed.

**Next permissible gate, if assigned:** implement the typed compiled native
rank/lease adapter and first-ACE/readback instrumentation with source/unit
checks, certify exact small-layout budgets and resolve inventory uncertainty.
Reassess all native gates before considering the single sequential conditional
fixture. This phase ends here; no automatic next campaign or goal resume.
