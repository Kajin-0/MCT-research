# Yue et al. 2006 temperature-resolved vacancy anomaly

**Date:** 2026-07-20  
**Source:** DOI `10.1063/1.2221411`

## Question

What exact experimental authority follows from the five-specimen temperature-dependent absorption study, and does the Hg-vapor anneal comparison provide an independently calibrated vacancy correction?

## Exact specimen inventory

```text
sample  class  x      thickness_um  carrier density       density T   deltaE
B2      bulk   0.232  >200          0.72e15 cm^-3         77 K        11.3 meV
B9      bulk   0.337  >200          0.14e15 cm^-3         77 K        10.5 meV
Mag     MBE    0.298   6.0          3.25e15 cm^-3        300 K        10.0 meV
M16     MBE    0.308   6.1          5.81e15 cm^-3        300 K         9.7 meV
M17     MBE    0.306   7.9          4.19e15 cm^-3        300 K         0.0 meV
```

`deltaE` is the source's extrapolated zero-temperature anomalous-edge separation. The source interprets it as a localized-level to valence-band separation. It is not a direct defect-level measurement or a latent-gap shift.

## Processing contrast

The MBE specimens share the same broad growth platform but are separate physical specimens:

```text
Mag     as grown                              deltaE = 10.0 meV
M16     Hg vapor, 400 C / 30 min             deltaE =  9.7 meV
M17     Hg vapor, 240 C / 24 h               deltaE =  0.0 meV
```

The source lineage describes the M16 condition as increasing Hg-vacancy density and the M17 condition as optimized for removing Hg vacancies. Vacancy concentration was not measured in the paper, and the comparison is not a before/after measurement on one specimen.

Four of five samples show the anomalous 30-70 K reversal. M17 is monotonic across the measured range. Representative turning behavior is:

```text
B9     reversal above approximately 33 K; minimum near 55 K
Mag    reversal above approximately 50 K; minimum near 70 K
```

Derived bounded diagnostics are:

```text
bulk mean deltaE                             10.90 meV
Mag + M16 mean deltaE                         9.85 meV
positive-anomaly range                        9.7-11.3 meV
positive-anomaly mean                        10.375 meV
M17 deltaE                                    0.0 meV
```

## Observation operators

The source does not apply one common edge definition to all specimens.

For thick bulk material, the spectrum is extrapolated to:

```text
alpha_Eg = -65 + 1.88*T + (8694 - 10.31*T)*x  [cm^-1]
```

For thin MBE epilayers, the edge is the intersection of the exponential region and the Kane plateau. Alternative bulk second-derivative and Z50 determinations scatter by less than 2 meV.

The less-than-`+/-0.8 meV` value reported by the source concerns critical-point determination. It is not assigned as a specimen-level uncertainty to every Table I `deltaE` value.

## Composition provenance

The compositions were inferred from the 11 K absorption spectrum using the source's absorption relation and published gap-composition relations. They are therefore:

```text
absorption_derived_circular_for_material_law_validation
```

No independent composition uncertainty is reported. The rows cannot serve as independent calibration points for a universal material-gap law.

Carrier-density comparisons also remain bounded: bulk values are reported at 77 K and MBE values at 300 K, so a pooled carrier-density versus `deltaE` correlation is unauthorized.

## Decision

Authorized:

- preserve the exact five-specimen table;
- preserve the bulk and MBE observation classes separately;
- classify the source as temperature-resolved, processing-conditioned vacancy-anomaly evidence;
- use M17 as a conditional vacancy-removing anneal control;
- strengthen the requirement for measured vacancy state and processing history in future paired acquisition.

Unauthorized:

- treat absorption-derived composition as independent validation;
- treat `deltaE` as a direct defect level or latent-gap correction;
- infer a universal approximately 10 meV vacancy correction;
- assign `+/-0.8 meV` to each Table I row;
- claim measured vacancy concentration or same-specimen causality;
- pool bulk and MBE critical points without their observation operators;
- correlate carrier density across mixed measurement temperatures;
- use the rows in uncertainty-weighted material-law fitting.

## Program consequence

Together with Mroczkowski 1983, this source supplies two complementary historical constraints:

1. fixed nominal composition shows vacancy-conditioned tail broadening;
2. temperature-resolved processing-conditioned specimens show a 9.7-11.3 meV anomaly that disappears in the source's vacancy-removing anneal condition.

The appropriate next step remains direct vacancy-proxy measurement in a paired, composition-controlled design rather than a literature-derived correction coefficient.
