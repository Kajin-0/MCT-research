# R02 decision record: terminate the QE testcode-wrapped raw-vertex fixture

**Date:** 2026-07-23  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issues:** #300; successor #309  
**Decision:** terminate the QE testcode-wrapper fixture strategy; retain backend vertex normalization as unresolved.

## Question

Can a pinned upstream nonpolar diamond fixture run through QE testcode preserve exporter-disabled and exporter-enabled EPW output, expose the pre-contraction complex `epf17` vertices, and validate the external matrix-Fan normalization without changing scientific control flow?

## Fixed state

Both authorized attempts used the same:

```text
QE 7.6 / EPW 6.1 commit
9f93ddec427d2b9a45bb72d828c6d324f62fcabd

source-tree SHA-256
34ab80c2ed8a0e30d1aef01ac847c68106c8c2b7f7eaf8e05ecafbbcbac849

observational-patch SHA-256
b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1

fixture
upstream test-suite/epw_base diamond
```

Source, pseudopotential, fixture inputs, patch, thresholds, export window, and resource ceilings remained unchanged.

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

The evidence harness searched file contents heuristically and did not preserve the EPW stdout.

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

The deterministic filenames were reported as:

```text
test.out.230726.inp=epw1.in.args=3
test.err.230726.inp=epw1.in.args=3
```

The post-run harness nevertheless searched the wrong persistent working directory, so the output was not preserved.

## Aggregate result

```text
pinned builds                    2
successful disabled sequences    2
successful disabled programs    10/10
enabled sequences                 0
normalization analyses            0
material calculations             0
```

No source, patch, compiler, executable, fixture-program, or scientific failure was observed. The backend normalization question was not evaluated.

## Decision

The **QE testcode-wrapped fixture strategy is terminated** because the one audited replacement authorization was consumed without producing comparable immutable output.

This does not establish that:

- QE or EPW is scientifically incorrect;
- `epf17` normalization fails;
- enabled export changes standard output;
- the external matrix-Fan kernel disagrees with EPW;
- SOC spinors or material self-energies are validated.

## Follow-up boundary

Issue #309 is design-only. It may reconstruct a direct command sequence from pinned upstream `run-epw.sh` branches and generate an explicit manifest with immutable stdout/stderr redirection.

Before another execution can be authorized, that design must provide:

1. exact working directories and command ordering;
2. explicit stdout and stderr destinations for every command;
3. preservation before cleanup;
4. synthetic filesystem and shell-quoting tests;
5. a no-execution dry-run manifest;
6. a separate bounded execution issue.

No additional build, fixture execution, retry, sweep, CdTe, HgTe, HgCdTe, A1, A2, or A3 work is authorized by this record.
