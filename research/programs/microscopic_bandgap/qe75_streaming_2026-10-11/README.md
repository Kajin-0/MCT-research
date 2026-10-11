# QE 7.5 one-q-plane exchange storage — finite engineering checkpoint

**Decision:** storage implementation and small validation **PASS**; native paired
SCF **NOT QUALIFIED / NOT RUN**. No hardware purchase or physics reduction.
The historical blocked R07 goal is unchanged.

The separately authorized [checkpoint/resource phase](checkpoint_phase/README.md)
adds tested no-copy ownership and reservation components but stops at the absent
complete native-state bridge. It also corrects a missed outer-stop/export refusal
path in the dated first patch. The earlier build is not promoted to native-ready.

The pinned source, dependency proof and lossless store remove the simultaneous
residence of eight exchange q planes for the prepared CPU/NC/SOC/fresh-SCF path.
Nominal `exxbuff` allocation becomes **2.75 GiB instead of 22 GiB**, saving
**19.25 GiB (87.5%)**. This is an allocation result, not a measured full-PW peak.
All 352 source/ACE bands, HSE parameters, SOC, meshes, cutoffs and solver accuracy
remain unchanged. Scratch storage holds the full uncompressed buffer.

- [Lifetime and equivalence proof](dependency_proof.md)
- [Implementation, resource and checkpoint boundaries](implementation_and_gates.md)
- [Finite validation results](verification.md), [machine-readable evidence](validation.json)
- [Decision and next narrowly bounded gate](decision.md)
- [Upstream source pins](source_manifest.json), [preservation checks](preservation_and_resources.json)
- [Candidate patch](qe75_qstream.patch), [new store module](exx_qstream.f90)
- [Reproducible patch application](apply_candidate.py), [compile/link/unit validation](validate_candidate.py)
- [Tiny spinor/kernel test](store_kernel_test.f90), [focused audit tests](test_qstream_package.py)

Private source/compiler/objects and **unexecuted** `pw.qstream.UNVALIDATED` live at
`/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/`.
Nothing replaces `.local/qe-env/bin/pw.x` or its libraries. The candidate uses
fresh SCF only and deliberately rejects EXX checkpoint import/export.

Reproduce only after sourcing DFT `scripts/env.sh`, with the recorded private
toolchain and pristine pinned source; the application script refuses other paths
or dirty source. `apply_candidate.py PRIVATE/q-e` installs the helper and edits
four source/build files. `validate_candidate.py PRIVATE --link-only` compiles
and links, runs tiny test executables, and **never invokes PW or MPI**. It is not
a launch command or runtime authorization. Existing numerical data and all
17 source/supervisor pins remain unchanged. No DFT repository commit is made.

The helper and tests are GPL-2.0-or-later. The QE-derived patch is distributed
with [QE's original GPL license](QE_GPL_LICENSE.txt); original upstream authorship
is retained. The patch alone requires the accompanying new helper file. It uses
zero context to avoid carrying upstream trailing whitespace: direct application
requires `git apply --unidiff-zero`; the guarded application script is unchanged.
