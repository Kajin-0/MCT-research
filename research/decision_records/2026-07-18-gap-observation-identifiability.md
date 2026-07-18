# HgCdTe gap observation-operator identifiability decision

Date: 2026-07-18

## Question

Does the disagreement between the Chu-attributed intrinsic-absorption gaps and the provisional latent-gap equation identify a measurement-class correction?

## Signed discrepancy

Residual is defined as:

```text
reported Chu absorption-fit gap - provisional latent gap
```

Across the eight secondary room-temperature points:

```text
mean signed residual       = +9.03919 meV
RMSE                       = 11.99110 meV
maximum absolute residual  = 20.47161 meV
positive residuals         = 7 of 8
constant-offset-removed RMSE = 7.87906 meV
```

A single source offset is therefore insufficient.

## Mechanism audit

### Hg-vacancy absorption-edge shift

The cited HgCdTe study reports that vacancy-related transitions can place the apparent absorption edge approximately 9–12 meV below the actual gap. The present Chu residual is predominantly positive: the reported gap is above the provisional prediction.

Decision: reject Hg-vacancy redshift as an explanation of this signed discrepancy. The energy scale is similar, but the direction is wrong.

Primary source: DOI `10.1063/1.2221411`.

### Absorption-edge extraction method

The same study compared alpha-based, derivative and Z50 methods and reported scatter within approximately 2 meV for its samples. The present discrepancy retains `7.87906 meV` RMSE after removing a constant offset and reaches `20.47161 meV`.

Decision: method-selection scatter at the cited scale is insufficient.

### Burstein–Moss band filling

Band filling shifts an n-type absorption edge to higher energy, which is sign-compatible with seven of the eight residuals. The Chu 1991 absorption study also discusses the Burstein–Moss shift.

However, the secondary point table does not provide sample-level carrier density, carrier type, Fermi level or nonparabolic mass data.

Decision: retain Burstein–Moss as plausible, but do not estimate or apply a correction.

Primary methodological source: DOI `10.1016/0020-0891(80)90053-6`.

### Composition scale versus absorption-fit definition

The residual correlates strongly with both composition and the table's `alpha_at_gap` value:

```text
corr(residual, x)            = 0.96117
corr(residual, alpha_at_gap) = 0.92880
corr(x, alpha_at_gap)        = 0.98480
variance inflation factor    = 33.14
```

Leave-one-out regression gives:

```text
x only                    2.96169 meV RMSE
alpha_at_gap only         4.01511 meV RMSE
x plus alpha_at_gap       2.93084 meV RMSE
```

The two-predictor improvement is negligible relative to the severe collinearity. Composition calibration and absorption-fit definition cannot be separated with these eight points.

## Decision

- Do not change the universal material gap law from this discrepancy.
- Do not promote a production absorption-gap observation operator.
- Reject the Hg-vacancy mechanism for this dataset by sign.
- Reject extraction-method scatter as sufficient by scale.
- Retain Burstein–Moss as a plausible but unidentified source-specific mechanism.
- Preserve measurement class, extraction method, carrier statistics and composition provenance as first-class metadata in every future gap record.

## Evidence required to reopen

1. sample-level carrier density and carrier type for the Chu absorption specimens;
2. the primary absorption-fit definition and covariance for each reported gap;
3. composition measurements independent of a band-gap equation;
4. paired magneto-optical and absorption measurements on common specimens.

## Claim boundary

The analysis rejects or retains mechanisms using sign, scale and identifiability. It does not diagnose the Chu samples. The point table is a secondary transcription, and no defect or carrier measurements are available for those eight specimens.

## Reproducibility

- validated head: `602af3ca01cc02a3d776ef31ce5e30de47f2067f`
- workflow run: `29656215390`
- artifact: `8432943974`
- artifact digest: `sha256:746763d1dc28b2f6c85e3655b549984ec29aa401d2bf3cfe48edd1761a4cb613`
- compact reference: `validation/gap_observation_identifiability_reference_result.json`
