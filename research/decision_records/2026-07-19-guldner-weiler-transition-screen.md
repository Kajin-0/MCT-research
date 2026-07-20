# Guldner-Weiler low-temperature transition screen

Date: 2026-07-19  
Controlling issue: #132

## Question

Does the recovered low-temperature magneto-optical lineage provide a stronger discriminator among historical HgCdTe gap equations than the previously analyzed detector-cutoff class?

## Evidence boundary

Guldner Parts I and II are the primary magneto-optical sources. Part II reports a linear interaction-gap trend and a semimetal-to-semiconductor transition composition

```text
x0 = 0.165 +/- 0.005 at 4.2 K.
```

The primary paper presents its point series graphically in Fig. 11. Camassel 1988 Table II prints twelve numerical composition-gap rows attributed to Guldner and one separate row attributed to McCombe.

This tranche stores the twelve Guldner-attributed Camassel rows as a **secondary exact transcription with a primary-figure consistency screen**. They are not promoted to primary exact points because no pointwise numerical table or digitization-coordinate audit has been recovered from the Guldner source.

## Historical trend equations added

### Wiley-Dexter 1969

```text
Eg = -0.30 + 1.91x + 5e-4 T(1 - 2x)
```

Wiley and Dexter supplied this relation to their Kane-model effective-mass calculation. Their transport agreement is therefore not independent validation of the equation.

### Weiler 1977

```text
Eg = -0.31 + 1.88x + 5e-4 T(1 - 2x)
```

Weiler plotted this relation against magnetoreflectance-derived gaps at 24 and 91 K. The paper reports approximately 3 meV fitted-gap uncertainty and specimen-dependent composition uncertainties of approximately 0.005-0.015.

## Results

At 4.2 K, the model mean absolute residuals against the twelve Guldner-attributed rows are:

```text
provisional Hansen-Pade   5.376 meV
Hansen 1982               5.434 meV
Seiler 1990               6.466 meV
Laurenti reconstructed    7.337 meV
Chu 1983                  9.045 meV
Weiler 1977               9.347 meV
Wiley-Dexter 1969        15.228 meV
Schmit-Stelzer 1969      24.947 meV
```

The Hansen-Pade and Hansen mean absolute residuals differ by only 0.058 meV. This screen cannot identify either one over the other.

The predicted 4.2 K critical compositions are:

```text
Schmit-Stelzer        0.15552   below reported interval
Wiley-Dexter          0.15631   below reported interval
Chu                    0.16063   inside reported interval
Weiler                 0.16414   inside reported interval
Hansen                 0.16521   inside reported interval
Hansen-Pade            0.16603   inside reported interval
Seiler                 0.16740   inside reported interval
Laurenti               0.16826   inside reported interval
```

Thus the primary transition-composition constraint rejects the low-temperature zero crossings of Schmit-Stelzer and Wiley-Dexter. It does not distinguish the remaining six equations.

## Decision

Authorized conclusions:

- reject Schmit-Stelzer and Wiley-Dexter as descriptions of the 4.2 K transition composition within the reported Guldner interval;
- retain Weiler, Hansen, Hansen-Pade, Seiler, Laurenti, and Chu as consistent with the transition-composition constraint;
- report the secondary-table residual screen with its source-class limitation;
- state that Hansen and provisional Hansen-Pade are numerically indistinguishable on this dataset;
- preserve the McCombe row under its separate Wiley-McCombe specimen lineage.

Not authorized:

- label the Camassel transcription as primary Guldner point data;
- infer pointwise Guldner composition uncertainties from the single reported transition uncertainty;
- select Hansen-Pade over Hansen from a 0.058 meV MAE difference;
- pool this series with detector cutoffs or absorption edges without method offsets;
- fit new universal gap coefficients.
