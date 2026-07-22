# Camassel 1988 Table I reconstruction

**Primary source:** J. Camassel, J. P. Laurenti, A. Bouhemadou, R. Legros, A. Lusson, and B. Toulouse, “Composition dependence of the Gamma8-Gamma6 transition in mercury cadmium telluride: A reexamination,” *Physical Review B* **38**, 3948–3959 (1988).  
**DOI:** `10.1103/PhysRevB.38.3948`  
**Table:** Table I, page 3950  
**Working asset:** `camassel1988.pdf` in the user File Library

The File Library binary is not materialized in the active runtime, so a SHA256 could not be computed. The dataset records that state explicitly. A future binary audit may add a hash without changing the scientific rows.

## Experimental series

The paper reports eleven Cd-rich Hg1-xCdxTe specimens measured at approximately 2 K:

- ten LPE epitaxial layers;
- one THM bulk reference;
- compositions from `x=0.50` to `x=1.00`;
- ionic-microprobe composition determination for every specimen;
- source-reported standard composition accuracy of approximately `0.5 composition percentage points`, represented as `0.005` in fractional `x` units.

The source calls this composition accuracy the dominant experimental limitation and notes a typical gap sensitivity of approximately `20 meV` per composition percentage point. Its own scale therefore implies roughly `10 meV` gap ambiguity from composition alone. The value `0.005` is preserved as a source-reported standard accuracy; this reconstruction does not silently assert that it is a Gaussian one-standard-deviation parameter.

Typical LPE layer thicknesses were approximately 4–10 micrometres, and most substrates were CdTe containing approximately 4% Zn. Those are series-level descriptions, not specimen-specific values, so they are not assigned row by row.

## Optical observables

Table I contains two related but distinct observation classes.

### Reflectivity exciton-polariton gap

Clear reflectivity structures were obtained over approximately

```text
0.78 <= x <= 1.00
```

The tabulated transverse `n=1` exciton-polariton energy is denoted `E_T`. For the four reflectivity-only specimens, the reported gap closes with the theoretical exciton binding energy:

```text
Eg = E_T + R_theory.
```

For the two dual-modality specimens, MCT49 and MCT47, the reported gap closes with the specimen experimental binding energy.

### Absorption and derivative-absorption excitonic gap

Transmission and first-derivative spectra supplement the lower-composition range. Seven rows provide an absorption threshold, an experimental binding energy, and a tabulated gap:

```text
Eg = E_T + R_experimental.
```

MCT49 and MCT47 occur in both modalities. Their observations share one specimen and one composition error and must not be treated as independent specimens.

## Exact Table I column interpretation

The flattened PDF text can make the seven experimental binding energies appear detached from their rows. The closure identities resolve the alignment:

```text
MCT49: 1.3440 + 0.0080 = 1.3520   reflectivity
       1.3420 + 0.0080 = 1.3500   absorption

MCT47: 1.1260 + 0.0065 = 1.1325   reflectivity
       1.1435 + 0.0065 = 1.1500   absorption
```

The remaining values `6.0, 6.0, 5.0, 3.0, 3.0 meV` align with MCT56, MCT61, MCT31, MCT67, and MCT68, respectively.

## Files

### `camassel1988_specimens.csv`

Eleven specimen rows with composition, growth method, common temperature, composition-accuracy semantics, and source state.

### `camassel1988_table1_observations.csv`

Thirteen long-form observations:

```text
6 reflectivity exciton-polariton gaps
7 absorption/derivative-absorption excitonic gaps
```

Each row records `E_T`, binding energy, binding-energy basis, tabulated `E_g`, measurement class, specimen group, and the absence of a Table I energy covariance.

## Source fit and uncertainty boundary

Camassel et al. fitted the Cd-rich composition dependence with fixed endpoint values and a constant bowing term. They reported:

```text
constant bowing parameter C = 0.132 eV
maximum departure from linear interpolation at x=0.5 = 33 meV
cubic coefficient D = 0.033 eV
maximum cubic contribution = 1.56 meV
fit standard deviation: approximately 1.77 meV parabolic versus 1.73 meV cubic
```

The source itself judged the cubic improvement physically insignificant relative to composition accuracy. These are in-source fit results, not independent validation of a universal law.

## Admissibility

The dataset is useful for:

- independent ionic-microprobe Cd-rich specimen anchors;
- measurement-class-specific static composition checks;
- calibrating Laurenti-linked Cd-rich specimens;
- testing whether model separations exceed source composition uncertainty.

It is not an independent held-out test of the later Laurenti 1990 Cd-rich relation because that work uses the same experimental lineage and anchors. Reflectivity and absorption observations from the same specimen must retain shared composition covariance.

## Prohibited interpretations

- Treating `0.005` as a Gaussian sigma without an explicit modeling choice.
- Treating the two x=0.71 specimens as one specimen.
- Counting MCT49 or MCT47 twice as independent composition anchors.
- Pooling reflectivity and absorption classes without a declared observation model.
- Treating the tabulated gaps as raw band gaps independent of exciton modeling.
- Assigning pointwise energy covariance not reported in Table I.
- Claiming sub-5-meV model superiority when the source composition scale corresponds to roughly 10 meV.
- Treating the source’s parabolic fit as an independent held-out validation of Laurenti 1990.
- Authorizing a production equation or manuscript from this transcription alone.
