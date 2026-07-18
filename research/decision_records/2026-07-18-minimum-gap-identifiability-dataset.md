# Minimum paired HgCdTe gap-identifiability dataset

Date: 2026-07-18

## Objective

Define the smallest practical dataset that can separate a latent HgCdTe gap law from absorption-class effects without fitting another empirical polynomial.

At one fixed temperature, the local audit model contains five coefficients:

1. latent gap intercept;
2. latent composition slope;
3. absorption-class offset;
4. carrier-filling contribution;
5. vacancy-edge contribution.

A magneto-optical observation measures the latent terms. A paired intrinsic-absorption observation on the same specimen measures the same latent terms plus the three absorption-specific terms.

## Why the existing table cannot answer the question

The secondary Chu table contains absorption-derived gaps and reported compositions, but no paired magneto-optical gap, Hall carrier state or vacancy-sensitive measurement.

Its design matrix has rank `2/5`:

- latent intercept and absorption offset are exactly aliased;
- carrier filling is unobserved;
- vacancy-edge bias is unobserved.

Adding paired gap classes raises rank to `3/5`. Hall or a vacancy proxy alone raises rank to `4/5`. Both are required for the declared five-parameter separation.

## Algebraic minimum

Three specimens with paired magneto-optical and absorption measurements can reach rank `5/5` when composition, carrier state and vacancy state provide independent contrasts.

Per temperature block:

```text
specimens                    = 3
paired gap observations      = 6
residual degrees of freedom  = 1
condition number             = 3.26272
maximum leverage             = 1.00000
```

Decision: this is an algebraic demonstration only. It has insufficient redundancy for an audit-grade model test.

## Audit-grade target

The recommended design is the full two-level factorial over:

- composition: coded low/high, corresponding to target `x=0.24` and `x=0.30`;
- carrier state: independently measured low/high contrast;
- vacancy state: independently measured low/high contrast.

This gives eight specimens. Each specimen receives both magneto-optical and intrinsic-absorption measurements.

Per temperature block:

```text
specimens                    = 8
paired gap observations      = 16
rank                         = 5/5
residual degrees of freedom  = 11
condition number             = 2.61803
maximum leverage             = 0.43750
information determinant      = 65536
```

For 1 meV independent observation noise, the local standard errors are:

```text
latent intercept             0.3536 meV
latent composition slope     0.2500 meV per coded x
absorption offset            0.5000 meV
carrier-filling scale        0.3536 meV per proxy
vacancy-edge scale           0.3536 meV per proxy
```

The design is repeated at a low-temperature block and at 300 K, producing 32 paired gap observations.

## Exhaustive minimum check

Every subset of the full `2^3` candidate family containing three through eight specimens was evaluated: 219 candidate subsets in total.

```text
specimens  candidate subsets  full-rank subsets  audit-grade subsets  best maximum leverage
3          56                 24                 0                    1.0000
4          70                 62                 0                    0.7500
5          56                 56                 0                    0.7258
6          28                 28                 0                    0.5833
7           8                  8                 0                    0.6121
8           1                  1                 1                    0.4375
```

Decision: the eight-specimen full factorial is the unique audit-grade qualifier under the declared thresholds and within this two-level candidate family.

This is not a universal proof over all continuous or multilevel optimal designs.

## Composition uncertainty requirement

At `x=0.25`, a 2 meV latent-gap error budget allows approximately:

```text
6 K:    sigma_x <= 0.001190
77 K:   sigma_x <= 0.001254
300 K:  sigma_x <= 0.001507
```

Practical requirement: use composition metrology with `sigma_x` near `1e-3` or better.

## Required specimen-level records

- one specimen identifier shared across all modalities;
- independent composition and uncertainty;
- measured temperature and uncertainty;
- magneto-optical gap and uncertainty;
- raw intrinsic-absorption spectrum;
- absorption extraction definition and covariance;
- Hall carrier type, density and mobility at each temperature;
- measured vacancy-sensitive proxy or controlled paired anneal state;
- thickness, strain state, doping and processing history.

The acquisition template is:

`data/templates/paired_gap_identifiability_acquisition_template.csv`

## Decision

- Authorize the eight-specimen paired acquisition design as the next evidence target.
- Do not authorize another static or thermal gap coefficient from current data.
- Do not authorize a production observation correction from current data.
- Treat the three-specimen design only as an algebraic smoke test.
- Require independent carrier and vacancy contrasts; nominal process labels are not substitutes.

## Claim boundary

The design oracle is a local linearized identifiability analysis. Full rank does not prove that the physical observation model is complete. The eight-specimen minimum is established only within the declared `2^3` candidate family and the declared condition, leverage and residual-degree thresholds.

## Reproducibility

- validated head: `c35cb19d7726f58a2d36faa9a0efc9fa57e9b1f9`
- workflow run: `29656588212`
- artifact: `8433051173`
- artifact digest: `sha256:5131b3fa84a53a0166c15a951d2541b536b3e97a264785dd2b2d25097bb6669e`
- compact reference: `validation/minimum_gap_identifiability_dataset_reference_result.json`
