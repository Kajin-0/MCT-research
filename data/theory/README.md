# Historical theory data products

These files preserve numerical predictions from prior HgCdTe theory papers. They are **not experimental observations** and must not be mixed into experimental residual metrics.

## Krishnamurthy et al. 1995

### `krishnamurthy1995_hg078cd022_table2.csv`

Direct transcription of Table II for Hg$_{0.78}$Cd$_{0.22}$Te. It contains the calculated finite-temperature gap, two reported hyperbolic-dispersion parameters, and the effective-mass ratio from 1 to 600 K.

Important qualifications:

- the model is hybrid empirical-pseudopotential/tight-binding, not modern first-principles AHC;
- the low-temperature gap includes the paper's stated 13.6 meV zero-point correction;
- the exact decomposition of the tabulated gap into electron–phonon and dilation contributions requires further audit;
- the printed unit/normalization of the parameter transcribed as `gamma_reported` should be confirmed before external reuse;
- the paper’s overall comparison accuracy is approximately 10–15 meV, so sub-meV structure in the table is not automatically physically resolved.

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
- Krishnamurthy 1–300 K shift: 105.06 meV;
- Hansen 1–300 K shift: 89.58 meV;
- Laurenti 1–300 K shift: 87.89 meV.

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
