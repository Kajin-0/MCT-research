# Historical HgCdTe evidence program closure

**Date:** 2026-07-20  
**Parent:** Issue #132  
**Closure tranche:** Issue #159

## Decision

The historical magneto-optical and edge-observation integration program is complete under its predeclared non-identifiability stop rules.

The program produced provenance-separated primary and secondary records, exact-table and sign constraints, source-bound observation operators, real-spectrum digitization audits, source-lineage-aware comparisons, composition-uncertainty propagation, vacancy-state evidence, and an executable paired acquisition protocol. It does not identify one universal HgCdTe gap law.

## Answers to the five controlling questions

### 1. Independent magneto-optical laboratories

Guldner and Weiler are independent laboratory lineages and are qualitatively compatible with the low-temperature semimetal-semiconductor transition. They do not support a few-meV quantitative ranking.

Weiler reports an approximately `3 meV` conditional fitted-gap uncertainty. Its reported composition uncertainties propagate through its own gap slope to `8.945-27.840 meV`. The paper also reports an interband/intraband model discrepancy up to approximately `4 meV`.

Authorized conclusion: qualitative cross-laboratory consistency.  
Unauthorized conclusion: few-meV agreement or disagreement among material equations.

### 2. Groves same-specimen sign change

For `x=0.161 +/- 0.003`, the source reports negative gap at 4 K and positive gap at 77 K.

- Schmit-Stelzer is positive throughout the 4 K composition interval and fails the sign constraint.
- Chu crosses zero inside the composition interval and is ambiguous.
- Hansen, Seiler, Laurenti, and provisional Hansen-Pade satisfy the negative 4 K sign.
- All tested equations satisfy the positive 77 K sign.

Authorized conclusion: the sign constraint rejects at least one historical low-temperature extrapolation.  
Unauthorized conclusion: selection of one universal equation.

### 3. Absorption observation spread

The integrated evidence retains several-to-tens-of-meV dependence on observation definition and specimen state:

```text
Moazzami fitted-model spans                    6.414 and 6.830 meV
Finkman alpha=20 to 1000 cm^-1                15.028-37.638 meV
Finkman 500 um zero intercept vs alpha=500    20.107-21.348 meV
Mroczkowski vacancy e-fold change               2.767 meV
Yue processing-conditioned anomaly              9.7-11.3 meV
```

These values describe different physical coordinates. They are not samples from one common uncertainty distribution.

### 4. Chang nonparabolic-Urbach operator

The Chang operator is implemented as a source-bound research candidate and passes synthetic recovery. The published Figure 2 cannot establish a real-spectrum enlargement of the existing `6.414-6.830 meV` spread because native data, resolved 77/80 K temperature, and same-specimen `W` and `b` are missing.

Synthetic fixed-parameter perturbations move the recovered edge by approximately `0.265-1.720 meV`. These are sensitivity diagnostics, not specimen uncertainty.

### 5. Hansen-Seiler-Laurenti ordering

No ordering is stable.

- Fixed absorption threshold changes the nominal winner on the real Moazzami spectra.
- Separating one Chu source-class offset changes the raw winner.
- Seiler and Hansen differ by only `0.091 meV` in Chu offset-transfer MAE.
- The manuscript's nominal Seiler advantage over Hansen is `0.177-0.255 meV`.
- Weiler composition propagation is `8.945-27.840 meV`.
- Different low-temperature sources and observation classes favor different comparators.

No historical equation is promoted.

## Stop-rule closure

Every controlling stop condition is active:

```text
composition uncertainty dominates model separation       yes
source or observation treatment changes nominal winner   yes
observation-class offsets are not universally estimable   yes
model-conditioned composition is present                  yes
independent specimen/source validation is insufficient    yes
```

Further unpaired literature accumulation or coefficient fitting is not authorized.

## Output completion

Issue #132 required:

- source-ingestion ledgers;
- machine-readable specimen and observation records;
- schema and fail-closed provenance tests;
- exact transcription tests;
- digitization sensitivity audits where justified;
- source-lineage-aware analysis tools;
- one consolidated decision memo.

These outputs are complete. Figure-only Guldner and Weiler trends are deliberately not digitized because their expected information gain is below the `8.945-27.840 meV` composition-propagation scale. That exclusion is a stop-rule result, not an incomplete extraction.

## Controlling next track

Historical-source integration closes. The next primary research track is the paired acquisition protocol merged in PR #142:

```text
8 physical specimens
2 paired observation classes
2 temperature blocks
32 primary observations
independent sigma_x target near 0.001
hard maximum sigma_x 0.0015
measured carrier state
measured vacancy proxy
co-registered measurement areas
```

## Reopening criteria

Reopen the historical-evidence program only for:

1. protocol-compliant paired data with independent composition, carrier, and vacancy measurements;
2. native calibrated Chang data with resolved temperature and same-specimen shape parameters;
3. an exact primary table whose expected information gain exceeds current composition and observation-model uncertainty scales.

The completed observation-model manuscript does not require reopening.
