# Dornhaus and Nimtz 1977 HSC_R13 primary-source audit

## Source

R. Dornhaus and G. Nimtz, "Transverse Magnetoresistance of Hg1-xCdxTe in the Extreme Quantum Limit," *Solid State Communications* **22**, 41-45 (1977), DOI `10.1016/0038-1098(77)90939-5`.

The repository owner supplied the complete five-page article as `dornhaus1977.pdf`. The observed binary SHA256 is:

```text
245d79984caf798916820e36d8afc0f0f9d54d8961a9da443d1491c3885c3200
```

The copyrighted PDF is not committed.

## Corrected measurement classification

Hansen grouped HSC_R13 with magneto-optical gap evidence. The primary source is not optical. It reports transverse magnetoresistance and Hall-effect measurements in the extreme quantum limit.

Nine commercially available n-type Hg1-xCdxTe crystals were measured in steady fields from superconducting coils to `8 T` and a Bitter magnet to `15 T`. Measurements were made at `4.2 K`; samples 5 and 8 also have lower-temperature records at `1.5 K` and `1.43 K`.

The direct observations are transverse voltage/resistivity and Hall voltage versus magnetic field. The principal derived experimental summary is an approximate exponent in

```text
rho_perpendicular proportional to B^alpha
```

over source-selected field intervals. The authors state that no exact power law was found in most samples.

## Specimen and geometry provenance

Table 1 identifies nine samples with compositions from `x=0.165` to `0.216`. The source prints `+/-0.005` adjacent to samples 1, 4, 7, and 8 only. No composition method is stated. The uncertainty is not propagated to the other rows.

Two geometries were used:

- disks of about `10 mm` diameter and `0.5 mm` thickness in a van der Pauw arrangement;
- bars of about `2 x 10 x 0.5 mm^3`.

Evaporated indium contacts were about `1 mm` in diameter. The authors estimate the finite-electrode error to be below `5%`. Some circular slices were cut into multiple bars and remeasured, but the paper does not map those pieces to Table 1 sample numbers. Cross-row specimen correlation is therefore unresolved.

The authors selected high-mobility specimens with marked Shubnikov-de Haas oscillations. They report no carrier freeze-out in the measured field range. Surface conduction is tested by repeated bromine-methanol etching but is explicitly not fully excluded.

## Table 1 reconstruction

The audit preserves all nine Table 1 sample records and thirteen printed power-law fit intervals.

At `4.2 K`, the reported exponents span:

```text
alpha = 1.0 to 2.0
```

The lower-temperature piecewise fits extend the complete printed range to:

```text
alpha = 1.0 to 2.3
```

This is more detailed than the abstract's approximate `1.5 to 2` summary.

Samples 5 and 8 each have two low-temperature field intervals with different exponents. Those are retained as separate records rather than collapsed into a single specimen value.

## Gap and band-parameter provenance

Table 1 prints composition-indexed values of:

- `Eg` at `4.2 K`;
- band-edge mass `m0*`;
- band-edge `g0*`.

The five unique gap entries are:

```text
x=0.165   Eg=0.0140 eV
x=0.170   Eg=0.0245 eV
x=0.185   Eg=0.0470 eV
x=0.200   Eg=0.0700 eV
x=0.216   Eg=0.0960 eV
```

These values are not raw magnetoresistance observations. The article uses them with composition- and density-dependent effective-mass curves to discuss access to the quantum limit and the influence of Kane nonparabolicity. It does not state an independent procedure in this paper for extracting the five gaps from the measured transverse magnetoresistance.

The gap, mass, and g-factor columns are therefore retained as `source_tabulated_transport_model_parameter`, not as direct scalar gap measurements. Their deeper lineage may pass through the authors' 1976 review cited as reference 17, but that secondary source is not substituted for the primary article and the exact derivation remains unresolved.

## Transport interpretation

The main result is a transport-law comparison, not a bandgap measurement.

For most samples the authors estimate the hierarchy

```text
lambda_F > r_s > R
```

with Fermi wavelength `lambda_F`, Thomas-Fermi impurity-potential range `r_s`, and magnetic length `R`. The observed exponents lie between the idealized long-range and short-range impurity predictions.

The conduction-band nonparabolicity introduces a magnetic-field-dependent longitudinal effective mass. Because no quantitative low-temperature HgCdTe calculation was available, the authors account for this only roughly by assigning an additional `0.5` to the magnetoresistance exponent. Subtracting that estimate gives corrected exponents of roughly `1 to 1.5`.

This correction is qualitative. It is not a new set of measured exponents and is not converted into bandgap data.

## Hansen HSC_R13 boundary

Five source-native composition-gap candidates can be traced from Table 1. Hansen does not expose source-labelled HSC_R13 markers and does not state whether it used these five unique entries, repeated the `x=0.20` value for all five samples, used effective-mass curves, or used another transcription.

```text
controlling decision
primary_source_recovered_extreme_quantum_limit_magnetotransport_table_reconstructed_gap_parameters_not_direct_observations_hansen_marker_mapping_unresolved
```

Dornhaus 1977 belongs to Hansen's fitted lineage. It cannot independently validate Hansen's empirical relation.

## Authorized and prohibited uses

Authorized:

- preserve all nine sample records and thirteen alpha-field-temperature intervals;
- use the direct transverse-magnetoresistance records to document the measurement class;
- retain the five composition-indexed Table 1 gap parameters as possible Hansen ingestion candidates;
- retain sample-specific printed composition uncertainties without extending them to unmarked rows;
- use the source to document nonparabolic transport-model assumptions and experimental controls.

Not authorized:

- treat the Table 1 gap column as independently measured transverse-magnetoresistance gaps;
- count the repeated `x=0.20`, `Eg=0.070 eV` rows as five independent gap observations;
- infer unprinted composition uncertainties or sample-piece correlations;
- convert the rough `0.5` nonparabolicity correction into experimental data;
- digitize theoretical curves in Figures 1, 2, 5, or 6 as observations;
- invent covariance or statistical confidence intervals;
- assign Hansen markers by plot proximity;
- use this fitted-lineage source as independent validation;
- construct a production HgCdTe bandgap relation from this source alone.
