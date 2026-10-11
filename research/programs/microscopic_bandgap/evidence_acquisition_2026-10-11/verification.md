# Verification and reproduction

Date: 2026-10-11. Baseline commit:
`94958c7dd4f683cbf6dc0f2247f1fa15286c96b3` on
`research/hgcdte-impurity-tmatrix-20261010`.

The investigation checks sources and qualifications, not a new material model.
The decision is `MISSING_QUALIFIED_PHYSICAL_EVIDENCE_STOP`; no physical x_c,
uniform material residual or positive composition modulus is populated.

## Evidence integrity and symbolic checks

Run the standalone read-only checker from the repository root:

```bash
.venv/bin/python research/programs/microscopic_bandgap/evidence_acquisition_2026-10-11/check_evidence.py
```

It checks all frozen record hashes and byte counts, coverage of all 22
`data/calculated/*.json` records, source-ID/DOI uniqueness, primary URLs,
inherited source hashes against their recorded audit, local links and absence
of asserted physical certificate values. It also checks, using exact rational
arithmetic, a three-point counterexample to inference of an all-pairs modulus,
the positive-kernel finite-energy secant identity and the pilot's composition,
discrimination and resource arithmetic. These are nonmaterial witnesses/design
checks; no density-functional, supercell or physical numerical calculation runs.

For this session only, downloaded copies under `/tmp` can additionally be checked:

```bash
.venv/bin/python research/programs/microscopic_bandgap/evidence_acquisition_2026-10-11/check_evidence.py --verify-temporary-copies
```

**Passed:** 584 frozen records, 24 primary publications (Part I/II counted
separately), six freshly downloaded PDF hashes, 30 local links and exact symbolic
checks. All inherited PDF hashes match an identified local audit record.

The ordinary checker does not require those ephemeral copies. Published source
links and source hashes remain in `sources.json`. No publisher PDF, complete
extracted text, raster page or external native wavefunction is committed.
Selected primary tables/figures/equations were rendered for visual cross-check;
that does not replace stated abstract-only or inherited-copy access tiers.

## Existing theorem and historical-source regressions

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q \
  tests/test_r07_analytical_first.py \
  tests/test_r07_threshold_causal_closure.py \
  tests/test_gamma8_threshold.py \
  tests/test_scalar_cpa_threshold.py \
  tests/test_guldner1977_hsc_r14_primary_audit.py \
  tests/test_guldner1977_hsc_r15_primary_audit.py
```

**Passed: 56 tests**, completed in under one second of command wall time.
They preserve the earlier identifiability/threshold counterexamples, conditional
causal bounds and direct historical-source uncertainty semantics. They validate
no physical HgCdTe prediction. An initial invocation without `PYTHONPATH=src`
failed at import collection; the corrected repository invocation above passed.
No dependency or source-code change was needed.

## Scope and stopping audit

Only this evidence package, R07's state file and R07's contribution-registry row
are changed. All prior packages, scientific data, source audits, tests and native
calculation infrastructure remain frozen. Corpus hashes cover 584 tracked text,
JSON, CSV and source records totaling 7,063,195 bytes; scope metadata covers all
22 frozen calculation JSON. Cross-program material is triaged, not rederived.

Read-only extraction used `pypdf` 6.20.0 installed into `/tmp/r07-pdf-tools`,
primary publisher/author downloads and existing Ghostscript for selected pages.
SciDownl was permitted by the user but was not needed. Existing numerical
processes/supervisors were neither inspected for intervention nor changed.
No native DFT/MPI/HSE/supercell job, new queue, runner or supervisor was created.
No messages were sent to source authors or laboratories. No old goal API,
status, controls or usage budget was accessed or modified.

Git whitespace, local-link/provenance checks and scope review passed before
the commit/push. The report stops at its substantiated missing-input boundary;
the single pilot remains a proposal. Push targets the existing research branch;
there is no merge to main or manuscript promotion.
