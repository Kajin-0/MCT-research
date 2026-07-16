# Historical theory data products

These files preserve numerical predictions from prior HgCdTe theory papers. They are **not experimental observations** and must not be mixed into experimental residual metrics.

## Krishnamurthy et al. 1995

### `krishnamurthy1995_hg078cd022_table1.csv`

Direct transcription of the spin-averaged 300 K Table I decomposition for Hg$_{0.78}$Cd$_{0.22}$Te. It contains the calculated valence- and conduction-edge contributions from intermediate bands 1-8 and the TA, LA, LO, and TO phonon branches.

The executable reproduction shows:

- `Delta Ev = -207.02 meV`;
- `Delta Ec = -80.46 meV`;
- `Delta Eg = +126.56 meV`;
- acoustic modes account for 73.78% of the combined edge-shift magnitude;
- acoustic modes contribute 103.69% of the net gap shift because optical modes oppose them by 4.64 meV;
- conduction-band intermediate states contribute `+236.59 meV` to the gap while valence-band intermediate states contribute `-110.03 meV`.

The one-temperature table establishes a signed, cancellation-sensitive 300 K decomposition. It does not identify branch-resolved thermal scales or explain the low-temperature turnover.

### `krishnamurthy1995_hg078cd022_table2.csv`

Direct transcription of Table II for Hg$_{0.78}$Cd$_{0.22}$Te. It contains the calculated finite-temperature gap, two reported hyperbolic-dispersion parameters, and the effective-mass ratio from 1 to 600 K.

Important qualifications:

- the model is hybrid empirical-pseudopotential/tight-binding, not modern first-principles AHC;
- the low-temperature gap includes the paper's stated 13.6 meV zero-point correction;
- closing Table I against Table II implies a `-7.90 meV` non-electron-phonon contribution at 300 K, consistent with the lattice-dilation term described in the paper;
- the `-7.90 meV` value is inferred from printed tables rather than independently tabulated;
- the printed unit/normalization of the parameter transcribed as `gamma_reported` should be confirmed before external reuse;
- the paper’s overall comparison accuracy is approximately 10-15 meV, so sub-meV structure in the table is not automatically physically resolved.

### `krishnamurthy1995_hg078cd022_kane_closure.csv`

Reproduces every Table II effective-mass ratio from the reported hyperbolic parameters and records the paper-convention equivalent velocity, the reduced `Eg/(2m*)` diagnostic, and restricted mass-model comparisons.

The robust paper-convention velocity drifts by 2.792% maximum over 1-300 K, below the declared 5% threshold. Large scalar `P(T)` renormalization is therefore not supported by this historical calculated dataset.

### `krishnamurthy1995_hg078cd022_legacy_comparison.csv`

Compares the tabulated 1995 gap with executable Hansen and Laurenti predictions at the same nominal composition $x=0.22$.

Both absolute values and thermal shifts relative to 1 K are retained. These answer different questions:

- absolute differences combine the zero-temperature composition law with the thermal law;
- within-model thermal shifts suppress constant intercept differences and are better for testing temperature dependence.

At 300 K:

- Krishnamurthy calculated gap: 218.66 meV;
- Hansen: 182.14 meV;
- Laurenti: 182.24 meV;
- absolute separation from the microscopic curve: approximately 36.5 meV;
- Krishnamurthy 1-300 K shift: 105.06 meV;
- Hansen 1-300 K shift: 89.58 meV;
- Laurenti 1-300 K shift: 87.89 meV.

Thus Hansen and Laurenti nearly coincide at this composition and temperature, but agreement between two empirical equations does not imply agreement with the historical microscopic model.

Conversely, around 150 K the Hansen thermal shift is close to the 1995 table. No single temperature is sufficient for model ranking; curve shape and source uncertainty are required.

## Use in the common benchmark

Historical theory curves should be scored separately from experiment under labels such as:

- `historical_theory_reference`;
- `mechanistic_shape_comparison`;
- `prior_model_reproduction`.

They may be used to:

- test whether a proposed analytical form can compress a mechanistic curve;
- identify structural features such as turnover or multiple thermal scales;
- define candidate calculation targets;
- compare modern calculations against historical predictions.

They may not be used as surrogate experimental data to claim improved physical accuracy.
