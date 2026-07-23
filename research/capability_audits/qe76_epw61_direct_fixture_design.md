# QE 7.6 / EPW 6.1 direct raw-vertex fixture design

**Program:** R02  
**Issue:** #309  
**Predecessor:** #300 / closed PR #305  
**State:** design only; no QE execution authorized

## Why testcode is excluded

Two separately authorized exporter-disabled diamond sequences completed all five declared upstream programs, but the QE testcode wrapper did not leave the EPW stdout at either post-run capture location.

```text
attempt 1 run       29962340413
attempt 1 artifact  8546683709
attempt 2 run       29971955581
attempt 2 artifact  8550168667
successful programs 10 / 10
preserved EPW stdout 0
```

The second attempt consumed the sole replacement authorization. Further capture-location guessing under issue #300 is prohibited.

The direct design removes only testcode output management. It does not change the source, pseudopotential, scientific inputs, command order, working directory, patch, or thresholds.

## Pinned source

```text
repository          QEF/q-e
release             qe-7.6
commit              9f93ddec427d2b9a45bb72d828c6d324f62fcabd
test-suite driver   test-suite/run-epw.sh
run-epw Git blob    8f6a915fb656e424f8e4c03b3e5ea301d83953ae
fixture             test-suite/epw_base
material role       upstream nonpolar software fixture only
```

## Source-level reconstruction

The pinned `run-epw.sh` defines the relevant branches:

- branch `1`: execute `pw.x` with the supplied input and explicit stdout/stderr paths;
- branch `2`: execute `ph.x`, then run `EPW/bin/pp.py` using `pp.in`;
- branch `3`: execute `epw.x` with the supplied input and explicit stdout/stderr paths.

The corresponding upstream testcode sequence is reconstructed as:

```text
1. pw.x  -input scf.in
2. ph.x  -input ph.in
3. python EPW/bin/pp.py < pp.in
4. pw.x  -input scf_epw.in
5. pw.x  -input nscf_epw.in
6. epw.x -input epw1.in
```

Every command uses one copied fixture directory as its working directory. This preserves the input files' relative `outdir`, `prefix`, `save/`, and `dvscf_dir` behavior.

## Evidence design

Before any future execution, the design assigns each command unique output paths outside the fixture tree:

```text
evidence/commands/01-pw-scf.stdout.txt
evidence/commands/01-pw-scf.stderr.txt
...
evidence/commands/06-epw.stdout.txt
evidence/commands/06-epw.stderr.txt
```

A future executor must open those destinations before starting each process. Output preservation cannot depend on later discovery, globbing, testcode cleanup, or content heuristics.

The manifest records:

- exact command order;
- one common working directory;
- executable labels rather than unpinned binaries;
- argv and stdin separately;
- unique stdout/stderr destinations;
- pinned source and `run-epw.sh` blob identity;
- fixture-input hashes;
- an immutable manifest payload hash;
- `execution_authorized=false`.

## Design tests

Synthetic tests must establish:

- the exact six-command order and branch mapping;
- retention of the `pp.py < pp.in` step;
- unique output paths;
- evidence outside fixture cleanup scope;
- deterministic inert JSON output;
- shell quoting represented only as text;
- failure on missing or hash-mismatched input;
- failure on duplicate output paths;
- failure if any execution authorization becomes true;
- absence of process-launch APIs in the manifest builder.

## Stop conditions

Stop at design without requesting execution if:

- a working-directory transition remains ambiguous;
- the direct sequence differs from the pinned upstream branches;
- an input must be altered;
- output cannot be opened before process start;
- evidence overlaps the fixture cleanup tree;
- the observational exporter changes scientific control flow;
- source, pseudopotential, patch, or thresholds drift.

## Authorization boundary

Authorized under #309:

- source inspection;
- contract and manifest design;
- pure Python path resolution;
- synthetic filesystem tests;
- inert JSON dry-run output.

Not authorized:

- configure or build;
- `pw.x`, `ph.x`, `epw.x`, or `pp.py` execution;
- a disabled or enabled fixture sequence;
- retries or sweeps;
- CdTe, HgTe, HgCdTe, SOC fixture, A1, A2, or A3.

A later executable fixture requires a separate bounded issue after this design is merged.
