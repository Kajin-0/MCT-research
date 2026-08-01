# Decision record: R04/R05 open-literature recovery 002

**Date:** 2026-07-31  
**Issue:** #400  
**Predecessor:** PR #401

## Decision

```text
PARTIAL_REANALYSIS_FEASIBLE
```

## Context

The user reported that the three remaining requested papers could not be found and reiterated that no outreach is desired. A bounded public-source recovery was therefore performed without contacting authors or facilities.

Two full texts were recovered from public sources:

- `10.1103/PhysRevMaterials.9.054602` — open access under CC BY 4.0;
- `10.1107/S1600577520013211` — official open IUCr PDF.

The author-uploaded listing for `10.3724/SP.J.1010.2012.00222` was identified, but the file was not reliably retrievable. Its abstract-level content was assessed against the quantitative APL companion already ingested in PR #401.

## Findings

### Near-critical prior

Bovkun et al. provide a controlled approximately 10 nm Hg1-xCdxTe QW series spanning x=0.040 to 0.061, including boundary-relevant samples at x=0.052 and 0.054. This materially improves specimen selection and detuning priors.

The paper does not provide local composition variance, a lateral covariance, local DOS, or a measured STS energy kernel.

### Spatial-kernel method

Biquard et al. directly infer a 580 nm pseudo-Voigt X-ray beam FWHM and convolve 10 nm SIMS or 15 nm STEM-EDX depth profiles with that measured kernel before comparing them with micro-Laue strain.

This validates the R04 requirement to kernel-match modalities. The profiles are cross-sectional depth records, not two-dimensional lateral covariance maps, and the material is not the Bovkun near-critical specimen class.

### Missing etched-surface paper

The unretrieved paper repeats the same decisive STM cautions already established by the APL companion: tip-induced band bending enlarges apparent gaps, and pit states blur gap information. Its absence does not block the literature-stage decision.

## Gate result

```text
local variance:       FAIL
correlation length:   FAIL
same population:      FAIL
near critical:        PARTIAL
resolution:           PARTIAL
matched null:         FAIL
robustness:           PARTIAL
decision changing:    PARTIAL
```

No source independently passes all eight gates. Cross-paper specimen synthesis remains prohibited.

## Program state

```text
NO_OUTREACH
LITERATURE_RECOVERY_EXHAUSTED_UNLESS_NEW_USER_PAPERS_APPEAR
R05_BLOCKED
```

This decision ends the required-paper search. New papers supplied later may be assessed, but the program must not keep searching indefinitely or substitute a larger simulation for missing matched evidence.
