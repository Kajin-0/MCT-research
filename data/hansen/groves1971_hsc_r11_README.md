# Groves, Harman, and Pidgeon 1971 HSC_R11 primary-source audit

## Source

S. H. Groves, T. C. Harman, and C. R. Pidgeon, "Interband Magnetoreflection of Hg1-xCdxTe," *Solid State Communications* **9**, 451-455 (1971), DOI `10.1016/0038-1098(71)90320-6`.

The repository owner supplied the complete five-page article as `groves1971(1).pdf`. The observed binary SHA256 is:

```text
ccbad551b170c97d2550cd31533b80ec6715772793dc4b18b8d56466fd83083f
```

The copyrighted PDF is not committed.

## Measurement identity

This source is genuinely magneto-optical. It reports interband magnetoreflection in circular polarization on one n-type Hg1-xCdxTe specimen. The direct observations are magnetic-field-dependent reflectivity peaks in `sigma+` and `sigma-` spectra. Figure 1 states that resonance fields were obtained from peak positions and averaged between up and down field sweeps.

Figure 2 plots experimental resonance points with theoretical transition curves. Oscillations were followed to photon energies of about `0.3 eV`; the figure plots only to `0.2 eV`. The field axis extends to `100 kOe`, and the text reports reflectivity changes approaching 40 percent. About twenty transitions are observed.

No pointwise covariance is reported. The Figure 2 points are not digitized in this audit, and theoretical curves are not converted into pseudo-data.

## Specimen provenance

The source reports a single unnamed sample:

```text
dimensions                    12 x 4 x 0.32 mm^3
composition                   x = 0.161 +/- 0.003
composition method            electron microprobe
carrier type                  n-type
4 K effective concentration   9.4e14 cm^-3
4 K Hall mobility             2.6e6 cm^2/V s
reflecting surface            (100)
field orientation             H perpendicular to (100)
```

The specimen was homogeneous to better than the stated electron-microprobe error. The authors argue from the narrow magnetoreflection linewidths that the relevant local homogeneity must be several times better still. That qualitative inference is not converted into a smaller numerical composition uncertainty.

## Body measurement temperatures versus abstract labels

The source contains an important provenance distinction.

The Figure 2 data were taken with the sample on a liquid-helium cold finger, giving a sample temperature between `20 and 30 K`. Figure 3 labels the schematic low state as approximately `25 K`. A second set of data, not shown, was taken at `90-100 K`; Figure 3 labels the schematic high state as approximately `90 K`.

For those body-text states the authors require approximately

```text
E(Gamma6) - E(Gamma8) = -0.01 eV   at the lower state
E(Gamma6) - E(Gamma8) = +0.01 eV   at the higher state
```

The abstract instead summarizes the separation as slightly negative at `4 K` and slightly positive at `77 K`. It does not print numerical gap values at 4 or 77 K. Therefore the audit does not relabel the body estimates as exact 4 K and 77 K measurements.

## Model-conditioned quantities

The sign and magnitude of the small Gamma6-Gamma8 separation cannot be determined reliably by extrapolating the transition curves to zero field. Small positive and negative separations give similar transition energies at the fields used. The authors therefore combine transition curvature with temperature behavior and a multiband model.

The theoretical curves use the Pidgeon-Brown magnetic-field effective-mass Hamiltonian for coupled Gamma8, Gamma6, and Gamma7 bands. Source-reported parameters are:

```text
E(Gamma6)-E(Gamma8), lower state   approximately -0.01 eV
E(Gamma6)-E(Gamma8), higher state  approximately +0.01 eV
Ep                                  18.5 eV
Gamma8 valence mass                 -0.28 m0
fit-sensitivity interval            +/-0.1 m0
Gamma7-Gamma8 spin-orbit splitting approximately 1 eV
```

The `+/-0.1 m0` statement is not a statistical standard uncertainty. The authors state only that values outside the interval would give a noticeably poorer fit.

The circular-polarization splitting provides a comparatively direct heavy-valence-band cyclotron-mass constraint: the separation between corresponding `sigma-` and `sigma+` peaks is twice the Gamma8 valence-band cyclotron energy. The reported mass nevertheless remains tied to transition assignments and the coupled-band fit.

## Transition assignments

Strong transitions are assigned within the Gamma8-derived level ladders. Five weaker transitions are discussed separately. Transition (5) is assigned to the lowest Gamma6-to-Gamma8 transitions and is observed only in the low-temperature data. Transition (1) is assigned to conduction-band cyclotron resonance. Transitions (3) and (4) require finite-`k3` wave-function mixing. The origin of transition (2) is explicitly unresolved.

These assignments are retained as model evidence rather than as independent scalar gap observations.

## Hansen HSC_R11 boundary

Traceable source-native candidates are:

1. the approximate `-0.01 eV` body estimate over `20-30 K`;
2. the approximate `+0.01 eV` body estimate over `90-100 K`;
3. the abstract's qualitative negative sign at 4 K;
4. the abstract's qualitative positive sign at 77 K.

Hansen does not expose source-labeled HSC_R11 markers and does not state whether it used the body estimates, abstract temperature labels, selected Figure 2 points, or another transcription. Plot proximity is not used to choose among them.

```text
controlling decision
primary_source_recovered_interband_magnetoreflection_parameters_reconstructed_temperature_labels_and_hansen_marker_mapping_unresolved
```

Groves 1971 belongs to Hansen's fitted lineage. It cannot independently validate Hansen's empirical relation.

## Authorized and prohibited uses

Authorized:

- preserve the single-specimen composition and measurement geometry;
- retain source-native low/high signed-gap candidates with approximate status;
- use the heavy-valence-mass result as model-assisted source evidence;
- use the transition assignments to document observable provenance;
- carry the body/abstract temperature distinction into any Hansen reconstruction.

Not authorized:

- treat `-0.01 eV` and `+0.01 eV` as exact 4 K and 77 K values;
- digitize theoretical curves as experimental observations;
- invent pointwise covariance or cross-temperature correlation;
- assign Hansen markers by visual proximity;
- use this fitted-lineage source as independent validation;
- construct a production HgCdTe bandgap relation from this source alone.
