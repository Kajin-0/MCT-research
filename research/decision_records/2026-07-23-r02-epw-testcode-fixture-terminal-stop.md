# R02 decision record: terminate the QE testcode-wrapped raw-vertex fixture

**Date:** 2026-07-23  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issues:** #300, successor #309  
**Decision:** terminate the QE testcode-wrapper fixture strategy; retain the raw-vertex normalization question as unresolved.

## Question

Can the pinned upstream nonpolar diamond fixture be used through QE testcode to preserve disabled- and enabled-export EPW stdout, export the pre-contraction complex `epf17` vertices, and validate the external matrix-Fan normalization without changing scientific control flow?

## Fixed scientific state

Both authorized attempts used the same:

```text
QE 7.6 / EPW 6.1 source commit
9f93ddec427d2b9a45bb72d828c6d324f62fcabd

source-tree SHA-256
34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849

observational patch SHA-256
b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1

fixture
upstream test-suite/epw_base diamond
```

The source, pseudopotential, fixture inputs, patch, thresholds, export window, and resource ceilings were unchanged.

## Attempt 1

```text
workflow run          29962340413
artifact              8546683709
artifact digest       sha256:9073466e47eff31d301d7d9b54675edffc420e7f160cecd3c8a523c057166971
builds                1
scientific sequences  1 disabled-export
upstream programs     5/5 passed
enabled sequence      not executed
analyzer              not executed
```

The harness searched file contents heuristically and did not preserve the EPW stdout.

## Audited replacement

```text
workflow run          29971955581
artifact              8550168667
artifact digest       sha256:59e73383c7b25a77cb6bc45a19adae80e0c644c1dfc26509c1e7175620e2fe61
builds                1
scientific sequences  1 disabled-export
upstream programs     5/5 passed
enabled sequence      not executed
analyzer              not executed
```

The deterministic testcode filename was correctly identified as:

```text
test.out.230726.inp=epw1.in.args=3
test.err.230726.inp=epw1.in.args=3
```

However, the capture step assumed those files remained in the test-suite root. QE testcode emitted, relocated, or removed them before the post-run capture step.

## Aggregate result

```text
pinned builds                    2
successful disabled sequences    2
enabled sequences                 0
normalization analyses            0
material calculations             0
```

No source, patch, compiler, executable, fixture-program, or scientific failure was observed. The backend normalization question was not evaluated.

## Decision

The **QE testcode-wrapped fixture strategy is terminated** for this gate because the sole audited replacement authorization was consumed without producing comparable immutable outputs.

This decision does not establish that:

- QE or EPW is scientifically incorrect;
- the `epf17` normalization fails;
- enabled export changes standard output;
- the external matrix-Fan kernel disagrees with EPW;
- SOC spinors or material self-energies are validated.

## Follow-up boundary

Issue #309 is design-only. It may reconstruct a direct sequence from the pinned upstream `run-epw.sh` branches and generate an explicit command manifest with immutable stdout/stderr redirection.

Before another QE execution can be authorized, the direct design must provide:

1. exact working directories and command ordering;
2. explicit stdout and stderr destinations for every command;
3. preservation before any cleanup;
4. synthetic filesystem and shell-quoting tests;
5. a dry-run manifest that invokes no QE executable;
6. a separate bounded execution issue.

No additional build, fixture execution, retry, sweep, CdTe, HgTe, HgCdTe, A1, A2, or A3 work is authorized by this record.
