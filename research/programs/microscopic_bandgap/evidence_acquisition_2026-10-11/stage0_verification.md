# Stage-0 verification and stopping audit

2026-10-11. Existing branch `research/hgcdte-impurity-tmatrix-20261010`;
base commit `59af123c725e44d073cf8665d5ea8dd968c4e9fd`.

The [Stage-0 source ledger](stage0_sources.json) pins 21 local inputs and records
nine primary-source/access routes, six rejected sample rows and 14 bounded
web/GitHub search queries. Public supplements were read with the native web
tool; fresh historical full-text access and raw-data retrieval are not claimed.
Source locations, access failures, published rights and unknown raw permissions
are explicit. Search results cannot establish nonexistence of private archives.
No publisher PDF, full text, plot digitization or laboratory data is committed.

Read-only reproduction from the repository root:

```bash
.venv/bin/python research/programs/microscopic_bandgap/evidence_acquisition_2026-10-11/check_stage0.py
.venv/bin/python research/programs/microscopic_bandgap/evidence_acquisition_2026-10-11/check_evidence.py
```

The first checker verifies pinned bytes/hashes, sample/source correspondence,
local links, declared NO-GO/unknown certificate fields and exact pilot arithmetic.
It verifies declared scope counters, not independent process telemetry. It does
not turn inaccessible raw data into accepted data or prove web completeness.
The second preserves the previous 584-record corpus, 24-publication ledger and
its independent symbolic checks. The original evidence package, data, source
audits and analytical derivations remain unchanged.

Independent source checks distinguish Teppe's author-request data statement
from its public PDF supplement, Orlita's growth profile from a complete assay
map, and the inherited Guldner approximate composition from older condensed
“exact caption” shorthand. Weiler's cold/composition/method limitations are
retained. The only numerical arithmetic checks concern design targets; no
Landau-level reconstruction or stage-1 observation fit is executed.

Domain D is reviewed against the primary semimetal/heavy-hole description and
the prior positive-measure continuum counterexample. The conditional shell
argument is a plausibility witness with explicit nonzero-coupling assumptions,
not a material-support proof. The weaker bracket is the intermediate-value
theorem for a declared continuous operational ordering observable, not a
relaxation of T16/T17. It is not applied to certify a new experimental interval.

Scope: additive Stage-0 reports/ledger/checker, package navigation and R07 state
only. No shared dataset, unrelated program, previous acceptance gate, historical
goal status, model/session setting or permission is changed. No tmux session,
agent fork, Codex process, contact, paid action, native calculation, queue or
supervisor is created. The existing paper evidence sufficed; SciDownl and shell
network downloads were unnecessary. Git whitespace, links, frozen provenance
and focused prior theorem/source regressions are checked before commit/push.
Stop at the [NO-GO decision](stage0_report.md); stage 1 is not admitted.

## Completed checks

Both provenance checkers passed: 21 Stage-0 input hashes, nine source-access
rows, six unaccepted sample rows and 13 Stage-0 local links; the earlier
584-record corpus and 24-publication ledger also passed. Exact pilot arithmetic
is a design check, not a specimen assay or material certificate.

The following focused prior theorem/threshold/source regressions passed with
exit status 0:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  tests/test_r07_analytical_first.py \
  tests/test_r07_threshold_causal_closure.py \
  tests/test_gamma8_threshold.py \
  tests/test_scalar_cpa_threshold.py \
  tests/test_guldner1977_hsc_r14_primary_audit.py \
  tests/test_guldner1977_hsc_r15_primary_audit.py
```

`git diff --check` passed. These checks validate provenance, scope and retained
mathematics; they do not validate raw-data availability or physical x_c.
