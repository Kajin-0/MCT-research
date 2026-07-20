# Guldner-Weiler 1977 magneto-optical evidence decision

**Date:** 2026-07-20  
**Parent program:** Issue #132

## Question

Can the recovered Guldner and Weiler primary magneto-optical papers support a few-meV independent cross-laboratory ranking of HgCdTe material-gap equations?

## Primary-source result

The two Guldner papers provide seven composition/inter\-action-gap pairs printed explicitly in text or figure captions at 4.2 K:

```text
x       interaction gap (meV)
0.025   -261
0.050   -207
0.115    -90
0.150    -30
0.185     35
0.250    161
0.280    208
```

The source reports density and electron-microprobe composition measurements and a zero-gap crossing at `x=0.165 +/- 0.005`. It does not report specimen-level composition uncertainty for the individual anchors. The complete composition trend is Figure 11 and is not numerically ingested.

Weiler reports ten magnetoreflectance specimens between `x=0.175` and `0.269` at 24 and 91 K. Its fitted-gap uncertainty is approximately `+/-3 meV`, but its composition uncertainty is:

```text
microprobe specimens       +/-0.006 to +/-0.015
transmission specimens     +/-0.005
```

The transmission-derived compositions use a room-temperature cut-on near 92% maximum transmission calibrated against chemical assay. They are not independent optical-gap validation records.

## Quantitative uncertainty result

Weiler's own empirical relation gives

```text
dEg/dx = 1.88 - 0.001*T   eV per composition fraction.
```

Therefore:

```text
T=24 K, sigma_x=.005/.006/.015 -> 9.280/11.136/27.840 meV
T=91 K, sigma_x=.005/.006/.015 -> 8.945/10.734/26.835 meV
```

Even the smallest reported composition uncertainty produces an energy scale about three times the stated gap-fit uncertainty. The largest produces roughly nine times the fit uncertainty. These scales are far larger than the `0.177-0.255 meV` descriptive Seiler-Hansen separation in the completed observation-model manuscript.

## Model and observable dependence

Both studies fit Pidgeon-Brown-family Landau-level models, but they use different optical observables:

```text
Guldner   interband magnetoabsorption/magnetotransmission
Weiler    interband magnetoreflectance
```

Weiler reports that its parameters produce intraband transition energies up to about `4 meV` above observed values near `60 kG`. Guldner's parameters agree better with the intraband results but give a poorer fit to Weiler's interband data. This is direct evidence that a fitted gap and parameter set retain observable/model dependence even within nominally similar magneto-optical methods.

## Authorized conclusions

- The three primary full texts are recovered.
- The seven exact Guldner anchors may be retained as `magneto_interband_fit` observations.
- Guldner and Weiler represent independent laboratory lineages.
- Composition uncertainty dominates Weiler's quoted gap-fit precision for material-law comparison.
- The interband/intraband discrepancy is admissible evidence of model/observable-class dependence.
- Qualitative independent-laboratory comparison is authorized.

## Unauthorized conclusions

- No Guldner Figure 11 or Weiler Figure 3 point may be treated as exact without a separate coordinate-sensitivity audit.
- Missing Guldner specimen-level `sigma_x` values may not be invented.
- Magnetoabsorption and magnetoreflectance points may not be pooled by default.
- Transmission-derived Weiler composition is not independent material-gap validation.
- A few-meV cross-laboratory ranking is not identifiable.
- No Hansen, Seiler, Laurenti, Guldner, or Weiler material law is selected.

## Program consequence

The primary magneto-optical recovery requirement of Issue #132 is satisfied at the source and exact-anchor level. It strengthens the program's non-identifiability conclusion rather than reopening universal equation fitting. Further digitization is justified only for a predeclared question whose expected information gain exceeds the approximately `9-28 meV` composition-propagation scale.
