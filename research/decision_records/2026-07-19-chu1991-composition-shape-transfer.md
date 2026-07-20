# Chu 1991 composition-shape transfer

Date: 2026-07-19  
Controlling issue: #132

## Question

Does the eight-specimen Chu 1991 turning-point edge series at 300 K distinguish absolute material-gap agreement from composition-shape transfer after allowing one source-specific observation-class offset?

## Evidence boundary

Chu, Mi, and Tang, *Infrared Physics* **32**, 195-211 (1991), DOI `10.1016/0020-0891(91)90110-2`, report eight printed Figure 3 turning-point labels:

```text
x       0.170  0.200  0.226  0.276  0.330  0.366  0.416  0.443
edge eV 0.124  0.161  0.205  0.273  0.347  0.396  0.470  0.507
```

The source defines the edge as the intersection of the sharply rising absorption region and the flatter intrinsic-absorption region. Values remain `printed_figure_labels` with a 0.5 meV rounding half-width. Density and electron-microprobe composition metrology have a reported RMS range of approximately 0.003-0.005.

The Chu 1983 equation is not independent validation because the 1991 paper derives and validates that source-family relation using these measurements.

## Analysis

Two comparisons are preserved separately.

### Raw absolute residuals

Among comparators not sharing the circular Chu source lineage, raw absolute MAEs are:

```text
Schmit-Stelzer 1969         8.579 meV
provisional Hansen-Pade     9.889 meV
Laurenti reconstructed     10.401 meV
Hansen 1982                15.491 meV
Seiler 1990                15.674 meV
Weiler 1977                16.037 meV
Wiley-Dexter 1969          28.134 meV
```

This ranking combines composition-law shape with the source's turning-point observation offset.

### Leakage-safe source-offset transfer

For each held-out specimen, one additive observation-class offset is estimated from the other seven specimens and transferred to the holdout. The resulting MAEs are:

```text
Seiler 1990                 4.186 meV
Hansen 1982                 4.277 meV
Schmit-Stelzer 1969         4.912 meV
provisional Hansen-Pade     7.479 meV
Laurenti reconstructed     11.886 meV
Weiler 1977                17.449 meV
Wiley-Dexter 1969          20.376 meV
```

The nominal independent winner therefore changes from Schmit-Stelzer to Seiler when one source-specific observation offset is separated from composition dependence.

Seiler and Hansen differ by only 0.091 meV in leave-one-out MAE and are not distinguishable on this evidence.

## Composition-bias robustness

A shared composition calibration shift was swept over

```text
-0.005 <= delta_x <= +0.005.
```

Leave-one-out offset-transfer MAE envelopes are:

```text
Seiler                      4.132-4.229 meV
Hansen                      4.222-4.320 meV
Schmit-Stelzer              4.724-5.097 meV
provisional Hansen-Pade     7.424-7.521 meV
Laurenti                   11.534-12.238 meV
```

The minimum provisional Padé MAE exceeds the maximum Hansen MAE by 3.104 meV. The Padé composition-shape disadvantage therefore survives the declared shared composition-bias interval.

## Decision

Authorized:

- distinguish raw absolute agreement from composition-shape transfer;
- report that one source-class offset reverses the nominal non-circular model ranking;
- report that Hansen and Seiler transfer composition shape better than the provisional Padé and Laurenti forms on this turning-point series;
- report that the Hansen-Padé separation survives a shared +/-0.005 composition shift;
- retain the result as direct evidence for observation-operator confounding.

Not authorized:

- select Seiler over Hansen from a 0.091 meV difference;
- treat the fitted offset as a universal absorption correction;
- treat Chu 1983 agreement as independent validation;
- pool these turning-point labels with magneto-optical gaps or detector cutoffs as interchangeable values;
- refit a universal HgCdTe gap equation.

## Consequence

The useful quantity in this source is not the raw absolute winner. It is the change in ranking after a leakage-safe observation-class offset is separated from composition shape. This strengthens the program's identifiability result and further weakens the provisional Hansen-Pade model without authorizing a replacement law.
