# R02 decision record: direct EPW raw-vertex fixture fails the nonperturbation gate

**Date:** 2026-07-23  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #313  
**Closed executable PR:** #315  
**Decision:** terminate the two-independent-full-sequence exporter comparison at the predeclared nonperturbation gate.

## Objective

Determine whether a disabled-by-default observational exporter can expose the complex `epf17` vertices from a pinned upstream nonpolar diamond fixture while leaving EPW's standard scalar lower-Fan output unchanged and reproducing that scalar result through the external matrix-Fan kernel.

## Fixed state

```text
QE / EPW                  7.6 / 6.1
source commit             9f93ddec427d2b9a45bb72d828c6d324f62fcabd
source-tree SHA-256       34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849
run-epw Git blob          8f6a915fb656e424f8e4c03b3e5ea301d83953ae
observational patch       b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1
fixture                   upstream test-suite/epw_base diamond
```

The direct sequence used no QE testcode and no output discovery. Disabled and enabled runs used separate copied fixture directories under the same pinned QE source tree so the upstream `../../pseudo/` path remained unchanged.

## Execution identity

```text
workflow run              29974357056
job                       89102877132
head                      973f480035dd9d0e5d9471b1a94ccd84825ce8e0
artifact                  8550988501
artifact digest           sha256:516340d80619da0145a29d53c9ab0fbbf6e747649f3254b5fafb78ebba589da4
```

Execution completed:

```text
pinned builds             1
fixture sequences         2
commands                  12 / 12 exit code 0
stdout/stderr files       24 preserved
raw rows                  20,736
material calculations     0
focused tests             28 / 28 passed
```

## Diagnostic results

The exported records are internally consistent with EPW's scalar contraction:

```text
normalization identity residual        2.168404344971009e-19 Ry^2
per-row real diagonal residual          6.505213034913027e-19 eV
summed real diagonal residual           2.0816681711721685e-16 eV
synthetic external covariance residual  1.9544770354189817e-16 eV
q-weight closure residual               0
complete four-band blocks               pass
acoustic masking                        pass
retarded imaginary sign                 pass
```

The selected four-band real diagonal was reconstructed as:

```text
backend
[-0.06467139846995636,
  0.14460109671625750,
  0.14360781769560450,
  0.14402652715529615] eV

external matrix-Fan reconstruction
[-0.06467139846995656,
  0.14460109671625750,
  0.14360781769560432,
  0.14402652715529620] eV
```

## Binding failure

The contract required enabled and disabled standard EPW output to agree within `1e-12 eV`.

Observed:

```text
maximum self-energy difference  1.9286256500095078e-7 eV
maximum energy difference       1.554600004283202e-9 eV
maximum dimensionless difference 5.509000011727494e-8
```

The self-energy difference exceeds the declared threshold by approximately `1.93e5`.

Therefore:

```text
standard_output_unchanged = false
classification            = STOP_NONPERTURBATION_GATE
```

## Attribution boundary

The exporter-enabled and exporter-disabled comparisons were two separately regenerated complete fixture sequences. Their electronic, phonon, Wannier, and EPW states were intended to be equivalent but were not byte-identical saved states.

The observed difference could result from:

- exporter I/O perturbing execution;
- ordinary independent-run numerical variation upstream of the final EPW contraction;
- both.

This run cannot distinguish those explanations. It would be incorrect to claim that the exporter caused the difference, but it would also be incorrect to claim observational noninterference.

The threshold was predeclared and cannot be relaxed after observing the result.

## Decision

Terminate the **two-independent-full-sequence exporter strategy**.

The diagnostic normalization identities remain useful evidence, but they do not override the nonperturbation failure and do not validate a production backend.

The following remain closed:

- another build or sequence under #313;
- threshold relaxation;
- SOC-spinor fixture;
- CdTe, HgTe, HgCdTe, A1, A2, or A3;
- dense EPW or generalized-Fröhlich material prediction.

## Next rational gate

A design-only attribution gate may examine a stronger experiment:

1. prepare one immutable electronic/phonon/Wannier state once;
2. duplicate that same saved state byte-for-byte;
3. replay only the final EPW self-energy stage with the exporter disabled and enabled;
4. preserve exact state hashes and output streams;
5. predeclare a baseline reproducibility control before another execution is authorized.

That gate must first establish whether EPW's available read/restart files allow the final self-energy stage to be replayed without regenerating the upstream state. No execution is authorized by this decision record.
