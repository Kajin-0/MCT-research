# Blue 1964 optical-gap table reconstruction

**Program:** R01 empirical bandgap reconstruction  
**Issue:** #267  
**Source:** M. D. Blue, “Optical Absorption in HgTe and HgCdTe,” *Physical Review* **134**, A226–A234 (1964)  
**Source file:** `blue1964.pdf` in the user File Library  
**Binary status:** available to source search but not materialized in the active runtime; SHA256 unavailable

## Purpose

Blue reports one of the earliest numerical optical-gap composition tables for HgTe–CdTe alloys. The source is useful only when its observation model is retained.

The seven printed values are not direct modern signed `Gamma6-Gamma8` gaps. They are positive gap parameters selected by comparing high-absorption experimental curves with a direct-transition theoretical absorption model.

The reconstruction therefore uses the measurement class

```text
theory_conditioned_positive_optical_gap_parameter
```

and does not place the rows in a signed-gap benchmark by default.

## Experimental preparation

Ingots of HgTe or HgTe–CdTe with the desired nominal composition were prepared from purified elements. The constituents were sealed in a cleaned and baked quartz tube and heated above the calculated melting point for more than 30 hours.

The material was then slowly cooled, placed in a vertical Bridgman furnace, reheated above the melting point, and translated through the furnace gradient at approximately

```text
2 mm/h.
```

Because segregation caused CdTe content to vary along the ingot, chemical analyses of Hg, Te, and Cd were performed at several ingot positions.

Transmission specimens were cut normal to the ingot axis from sections of known composition. Freely suspended specimens thinner than approximately `6 um` could be prepared, while typical specimens were approximately `20 um` thick. Reflectance measurements used polished sections adjacent to the transmission specimens to limit composition mismatch from axial segregation.

## Optical apparatus and temperature range

Transmission measurements used a Perkin-Elmer model 112 infrared spectrometer with NaCl and KBr optics over approximately

```text
1–25 um.
```

The experimental system covered approximately

```text
90–373 K.
```

The seven numerical alloy-gap rows are associated with the room-temperature absorption curves in Figure 6. The repository records the temperature context as `room_temperature` and does not invent one exact kelvin value.

## Table identity

The article narrative states that the results for the seven Figure 6 samples are tabulated in

```text
Table II.
```

Text extraction renders the Roman numeral inconsistently. The repository follows the article narrative and labels the numerical source as Table II while retaining the OCR ambiguity in source metadata.

## Printed numerical observations

| CdTe atomic % | Fractional x | Positive optical-fit gap | Printed fit uncertainty |
|---:|---:|---:|---:|
| 0 | 0.000 | 0.030 eV | 0.020 eV |
| 0.5 | 0.005 | 0.040 eV | 0.020 eV |
| 14 | 0.140 | 0.120 eV | 0.040 eV |
| 22 | 0.220 | 0.220 eV | 0.020 eV |
| 25 | 0.250 | 0.250 eV | 0.020 eV |
| 28 | 0.280 | 0.280 eV | 0.020 eV |
| 32 | 0.320 | 0.365 eV | 0.010 eV |

The values are transcribed in

```text
data/experimental/blue1964_table2_optical_gaps.csv
```

with one row per specimen.

## Gap extraction method

Blue compared measured absorption curves with theoretical direct-transition curves at high absorption, described as approximately above

```text
10^3 cm^-1.
```

The source considered this preferable to selecting either:

- the point where the edge first rises;
- an arbitrary fixed high absorption value.

The extracted quantity is consequently model conditioned. It is not equivalent by construction to:

- Scott’s later `alpha=500 cm^-1` edge;
- Finkman’s `alpha=1000 cm^-1` edge;
- a Tauc intercept;
- a Camassel excitonic gap;
- a Seiler TPMA gap;
- a signed band-order parameter.

## Sign convention boundary

The table reports positive values for HgTe and the `0.5 atomic % CdTe` alloy:

```text
x=0.000   0.030 +/- 0.020 eV
x=0.005   0.040 +/- 0.020 eV
```

Modern signed-gap conventions assign inverted HgTe a negative `Gamma6-Gamma8` gap. Blue’s positive quantities therefore cannot be silently negated, interpreted as absolute values of a signed modern gap, or pooled with signed magneto-optical observations without an explicit observation model.

Every row is marked

```text
signed_gap_eligible = false
observable_sign_semantics = positive_parameter_not_signed_Gamma6_minus_Gamma8
```

## Uncertainty semantics

The row-specific energy uncertainties were estimated from the agreement between experimental and theoretical absorption curves. They are encoded as

```text
source_reported_curve_fit_bound_not_asserted_gaussian_sigma.
```

No pointwise covariance is reported.

The paper states that the alloy compositions determined by chemical analysis were believed accurate to better than one percent and later says that chemical-analysis accuracy was assumed to be one percent. The source does not make clear whether this means:

- one absolute atomic-percentage point;
- one percent relative to the reported concentration;
- a statistical standard deviation;
- a deterministic bound.

The repository therefore records

```text
one_percent_as_reported_scale_ambiguous_not_sigma_x
```

and does not construct `sigma_x`.

## Abstract-versus-table inconsistency

The abstract describes the alloy series as extending to

```text
28% CdTe.
```

Figure 6 and the printed numerical table include a

```text
32% CdTe
```

specimen.

Both statements are retained. The repository does not silently delete the 32% row, revise the abstract, or infer which statement the author intended.

## Hansen lineage

Blue 1964 is not present in the reconstructed list of Hansen’s 22 fitted sources. It predates Scott and Hansen and is cited by later HgCdTe work.

Its admissible role is

```text
historical external comparator for observation-model and sign-convention studies.
```

It is not treated as a blinded modern holdout, and its theory-conditioned positive optical-fit parameter is not directly commensurate with every Hansen input observable.

## Reproducibility and prohibited shortcuts

The source reconstruction contains exactly seven printed observations. It contains no digitized Figure 6 coordinates and no points sampled from the theoretical curves.

Prohibited:

- converting the two Hg-rich positive values to negative signed gaps;
- treating the printed uncertainty as Gaussian one-sigma without justification;
- assigning a numerical `sigma_x` from the ambiguous one-percent statement;
- assigning an exact kelvin value to `room_temperature`;
- resolving the abstract/table composition conflict by deleting or changing a row;
- sampling Figure 6 theory curves as observations;
- ranking analytical gap laws before declaring an observation operator.

## Scientific decision

The Blue numerical table is recoverable and suitable for a provenance-controlled historical observation-model study. It is not yet suitable for direct signed-gap model ranking.

This reconstruction does not establish:

- a signed HgTe endpoint;
- an independent validation or rejection of Hansen;
- a universal static composition law;
- a production equation;
- manuscript or submission readiness.
