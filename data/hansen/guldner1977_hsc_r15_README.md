# Guldner et al. 1977 HSC_R15 primary-source audit

## Source

Y. Guldner, C. Rigaux, A. Mycielski, and Y. Couder, "Magnetooptical Investigation of Hg1-xCdxTe Mixed Crystals. II. Semiconducting Configuration and Semimetal to Semiconductor Transition," *physica status solidi (b)* **82**, 149-158 (1977), DOI `10.1002/pssb.2220820115`.

The complete ten-page article is available in the repository owner's ChatGPT File Library as `guldner1977 (1).pdf`, file-library identifier:

```text
file_000000000f5481fd91088875f4b813da
```

The text and page images were audited. The File Library interface does not expose the binary bytes to the active runtime, so the exact SHA256 is deliberately recorded as `not_materialized_file_library_binary`. The hash must be added only after the exact PDF is attached in the active conversation or otherwise made available byte-for-byte. The copyrighted PDF is not committed.

## Measurement class

This source reports 4.2 K interband magnetoabsorption:

- photon energies from `120` to `370 meV`;
- magnetic fields to `60 kG`;
- Faraday geometry with circular `sigma+` and `sigma-` polarization;
- Voigt geometry with linear polarization parallel to the field;
- semiconducting alloys over approximately `0.17 <= x <= 0.30`;
- additional near-zero-gap semimetallic and semiconducting cases around `x approximately 0.15` and `x=0.185`.

The direct observations are magnetotransmission minima as functions of magnetic field. The interaction gap is estimated from the zero-field convergence of identified interband transition series. The remaining band parameters are adjusted in the Pidgeon-Brown coupled-band model. The printed interaction gaps are therefore source-native, model-assisted determinations rather than raw transmission observables.

## Material and specimen provenance

Part II states that alloy composition was determined by density measurements and electron microprobe. It refers to Part I for the experimental techniques and does not reprint the full growth, preparation, thickness, annealing, or mounting record.

No source-native specimen identifiers, complete physical specimen count, per-specimen composition uncertainty, or exact Part I/Part II specimen linkage are printed. Those fields remain unresolved.

Five composition-gap groups are directly traceable from text and figure captions:

```text
x approximately 0.250   epsilon0 = +161 meV
x approximately 0.215   epsilon0 =  +86 meV
x = 0.280               epsilon0 = +208 meV
x approximately 0.150   epsilon0 =  -30 meV
x = 0.185               epsilon0 =  +35 meV
```

The page-150 OCR rendering `x=0.35` is not accepted: the page image, Figure 1 caption, and Figures 2-4 consistently identify the representative alloy as `x approximately 0.25`.

No pointwise gap uncertainty or covariance is reported.

## Semimetal-to-semiconductor transition

Section 4 states that the measured interaction-gap dependence on composition is linear and reports:

```text
x0 = 0.165 +/- 0.005 at 4.2 K
```

Figure 11 combines the semimetallic and semiconducting composition range and includes experimental determinations from this work and cited sources. The exact marker coordinates and symbol-to-source assignments are not tabulated. Figure 11 is not digitized.

The reported critical composition is retained as a source-native scalar result. It is not converted into pointwise composition uncertainties for the five printed gap records.

## Representative band-parameter fits

For `x approximately 0.25`, `epsilon0=161 meV`, the printed fit is:

```text
Ep = 19 eV
gamma1 = 5
gamma = 1.5
kappa = -0.5
Delta = 1 eV
```

For `x approximately 0.215`, `epsilon0=86 meV`:

```text
Ep = 19 eV
gamma1 = 3
gamma = 0.25
kappa = -1.25
Delta = 1 eV
```

For `x=0.28`, `epsilon0=208 meV`, the polaron-section background fit uses:

```text
Ep = 19 eV
gamma1 = 5
gamma = 1.5
kappa = -0.5
```

No pointwise uncertainty is printed for these representative fit values.

The global constraints inherited and restated across the two-part study are:

```text
Delta = 1 eV, fixed and composition independent
gamma1 = 4.5 +/- 1.5
kappa = -1 +/- 0.5
gamma1 - 2 gamma = 2.5 +/- 0.5
m_h*/m0 = 0.4 +/- 0.1
```

The source identifies neglected valence-band warping as the major uncertainty in the modified Luttinger parameters and heavy-hole mass. These are source-level limits, not a pointwise covariance model.

## Figure-derived model outputs

Figure 12 reports a nonlinear variation of Kane energy `Ep` with interaction gap. No equation or numerical table is printed, and the source states that this variation is not theoretically interpreted.

Figures 13 and 14 show the band-edge electron effective mass and Lande factor calculated from the fitted band-parameter sets. They are model-derived outputs, not direct effective-mass or g-factor measurements.

Figures 12-14 are not digitized.

## Polaron anomalies are a separate evidence layer

For `x=0.28`, `epsilon0=208 meV`, the source reports resonant electron-phonon anomalies:

- a `19.5 meV` LO-phonon doublet and level-pinning feature in `sigma-` polarization, with critical field `29.5 kG`;
- `19.5 meV` and `17 meV` pinned branches in `E parallel H`.

The source states that a more detailed theoretical analysis is required. These phonon energies, splittings, and pinning branches are not intrinsic interaction gaps and are not entered into the Hansen gap ledger.

## Part I versus Part II boundary

Part II relies on the Pidgeon-Brown framework and experimental-method description from Part I. Figure 11 spans `0 <= x <= 0.3` and incorporates the semimetallic regime documented in Part I.

The five Part I scalar interaction gaps are not counted again as independent Part II observations. The exact physical specimen linkage between the two articles remains unresolved.

## Hansen HSC_R15 boundary

Five printed Part II gap candidates are preserved, but Hansen does not expose source-labelled HSC_R15 markers. It remains unclear whether Hansen ingested:

- the five printed Part II scalar values;
- additional Figure 11 points;
- the combined linear relation;
- selected transition-derived values;
- or another transcription.

```text
controlling decision
primary_source_recovered_semiconducting_transition_interaction_gap_candidates_and_x0_reconstructed_hansen_marker_mapping_unresolved
```

This source belongs to Hansen's fitted lineage and cannot independently validate Hansen's empirical equation.

## Authorized and prohibited uses

Authorized:

- retain the five printed 4.2 K interaction-gap candidates with exact versus approximate composition qualifiers;
- retain `x0=0.165+/-0.005` as the source-reported critical composition;
- retain composition-method, spectral-range, geometry, field, and model-provenance metadata;
- preserve representative and global band-parameter constraints;
- preserve polaron anomalies as a separate evidence layer;
- preserve Figure 11-14 qualitative roles without digitization.

Not authorized:

- invent a source PDF hash, pointwise composition uncertainty, gap uncertainty, covariance, specimen identity, or cross-part specimen linkage;
- digitize Figure 11-14 without a separate resolution and uncertainty gate;
- count Part I points again as independent Part II observations;
- treat polaron energies or splittings as intrinsic gaps;
- treat calculated mass or Lande-factor curves as direct measurements;
- assign Hansen markers by plot proximity;
- use this fitted-lineage source as independent validation;
- construct a production HgCdTe bandgap relation or manuscript claim from this audit.
