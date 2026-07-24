# R01 state update: Stankiewicz-Giriat 1972 HSC_R10 primary-source audit

## Result

The complete seven-page HSC_R10 source was recovered and audited.

The source is hydrostatic-pressure Hall transport, not a direct magneto-optical or absorption-edge experiment. Four composition-defined specimens were measured from 77 to 295 K and up to 10,000 atm. Signed zero-pressure gaps and pressure/temperature coefficients were inferred through a simplified Kane/Groves-Paul carrier model.

## Reconstructed source-native records

- four composition records with `x = 0.070, 0.095, 0.130, 0.180`, each `+/-0.005`;
- eight Table 1 signed-gap values at 77 and 280 K;
- four pressure coefficients;
- four temperature coefficients;
- fixed model assumptions `Ep=18 eV`, `mh*=0.55 m0`, and overlap energy zero;
- Equation 4 for `x<0.2`:

```text
E0(x,T) = -0.303 + 1.91x + 5.25e-4(1-2x)T eV
```

## Limitation

The source warns that the specimens were not perfectly intrinsic and that fixed-model assumptions introduce error beyond measurement uncertainty. Pointwise covariance is not reported.

Hansen does not identify whether HSC_R10 used Table 1 values, Equation 4, Figure 6 markers, or another transcription. No marker assignment is inferred by proximity.

```text
primary_source_recovered_table1_and_equation4_reconstructed_hansen_marker_mapping_unresolved
```

This source remains part of Hansen's fitted lineage and is not independent validation.
