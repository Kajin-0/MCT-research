# Static-composition cross-source stop decision

Date: 2026-07-18

## Question

Does the available point-level evidence justify replacing the Hansen zero-temperature HgCdTe composition polynomial?

## Evidence examined

The audit compared four named equations on two composition sources:

- eight room-temperature gap points transcribed from Chu and Sher Table 4.4 and attributed to the Chu, Mi and Tang absorption experiments;
- independently composed Seiler samples 3–5 at 2–10 K.

The Chu table is secondary evidence. The primary point table, pointwise uncertainties and original composition metrology have not been recovered.

## Direct model screen

| Model | Chu 300 K RMSE | Seiler 2–10 K RMSE |
|---|---:|---:|
| Hansen | 16.2664 meV | **3.8867 meV** |
| Chu 1983 | **3.2568 meV** | 15.9735 meV |
| Laurenti | 11.6940 meV | 11.7503 meV |
| Provisional Hansen-Padé | 11.9911 meV | 4.1762 meV |

The source that strongly prefers the Chu formula is the same source family from which that formula was derived. The preference does not transfer to independently composed Seiler samples.

## Diagnostic static corrections

Minimal corrections were fitted only to the Chu table and evaluated by leave-one-composition-out validation before unchanged transfer to Seiler.

| Correction | Chu held-out RMSE | Seiler transfer RMSE | Universal candidate |
|---|---:|---:|---|
| affine | 2.9617 meV | 7.2647 meV | no |
| quadratic | 3.1382 meV | 6.8157 meV | no |
| endpoint-preserving two-term | **2.8242 meV** | **6.6914 meV** | no |

The fitted corrections improve the secondary Chu table but materially degrade the independent Seiler source.

## Composition-scale diagnostic

Inverting the provisional equation at each Chu point yields an effective affine composition mapping:

```text
x_effective = -0.0112490502 + 1.0594349678 x_reported
```

The mapping fits the Chu table with:

```text
RMS composition residual = 0.00159634
room-temperature gap RMSE = 2.14937 meV
```

Transferred unchanged to Seiler, the gap RMSE becomes `8.84832 meV`. The mapping is therefore source-specific, not a universal alloy-composition correction.

## Decision

- Do not fit or promote a new static-composition polynomial.
- Retain Hansen as the static baseline inside the provisional thermal model.
- Retain Chu 1983 only as a provenance-separated historical comparator.
- Retain the provisional Hansen-Padé temperature kernel; this audit does not falsify its transferred temperature shape.
- Treat source-dependent composition calibration as plausible but unproven.
- Stop static-law coefficient development until stronger composition provenance is available.

## Required evidence to reopen

At least one of the following is required:

1. primary point-level Chu 1991 absorption gaps with composition method and uncertainty;
2. another independently composed low-temperature composition-gap series;
3. new specimen-level composition and gap measurements made on one common metrology scale.

## Claim boundary

This audit does not identify the cause of the cross-source disagreement. Possible causes include composition calibration, optical-gap definition, sample physics and source-formula bias. The result establishes only that the current evidence does not support a universal replacement for the Hansen static polynomial.

## Reproducibility

- workflow run: `29653370206`
- artifact: `8432129170`
- artifact digest: `sha256:7b7def156e98fe41d56d4b65fc632c4aaa413e8317e6e2fab3c9945ca8d88ccc`
- validated analysis head: `dd7872b2f1bcf967b0937d53851bcdbf166032d9`
- compact reference: `validation/static_composition_cross_source_reference_result.json`
