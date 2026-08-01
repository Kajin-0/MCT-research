# Guldner et al. 1977 HSC_R15 primary-source audit

## Source

Y. Guldner, C. Rigaux, A. Mycielski, and Y. Couder, "Magnetooptical Investigation of Hg1-xCdxTe Mixed Crystals. II. Semiconducting Configuration and Semimetal to Semiconductor Transition," *physica status solidi (b)* **82**, 149-158 (1977), DOI `10.1002/pssb.2220820115`.

The exact ten-page article was attached in the active conversation as `guldner1977 (1)(1).pdf`. Binary inspection confirmed ten pages and produced:

```text
SHA256 85bdf09852eb02747158a80f7854d202a69a48d98c9c571a396f8a4cd51c8704
attachment ID file_000000006f0881fda163c0e4ae6a72c3
```

The PDF was rendered and checked against the source identity, title, volume, pages, and figures. The copyrighted binary is not committed.

## Measurement class

This source reports 4.2 K interband magnetoabsorption:

- photon energies from `120` to `370 meV`;
- magnetic fields to `60 kG`;
- Faraday geometry with circular `sigma+` and `sigma-` polarization;
- Voigt geometry with linear polarization parallel to the field;
- semiconducting alloys over approximately `0.17 <= x <= 0.30`;
- near-zero-gap cases around `x approximately 0.15` and `x=0.185`.

The direct observations are magnetotransmission minima. Interaction gaps are estimated from the zero-field convergence of identified transition series, while the remaining band parameters are adjusted in the Pidgeon-Brown model. The gap values are source-native, model-assisted determinations, not raw transmission observables.

## Material and specimen provenance

Part II states that composition was determined by density measurements and electron microprobe. It refers to Part I for the detailed experimental methods.

No source-native specimen identifiers, complete physical specimen count, per-specimen composition uncertainty, or exact Part I/Part II specimen linkage are printed. Those fields remain unresolved.

Five composition-gap groups are directly traceable:

```text
x approximately 0.250   epsilon0 = +161 meV
x approximately 0.215   epsilon0 =  +86 meV
x = 0.280               epsilon0 = +208 meV
x approximately 0.150   epsilon0 =  -30 meV
x = 0.185               epsilon0 =  +35 meV
```

The page-150 OCR rendering `x=0.35` is rejected: the rendered page, Figure 1 caption, and Figures 2-4 identify the alloy as `x approximately 0.25`.

No pointwise gap uncertainty or covariance is reported.

## Semimetal-to-semiconductor transition

Section 4 and Figure 11 report a linear interaction-gap dependence and:

```text
x0 = 0.165 +/- 0.005 at 4.2 K
```

Figure 11 combines semimetallic and semiconducting evidence. Exact marker coordinates and symbol-to-source assignments are not tabulated. Figure 11 is not digitized. The critical-composition uncertainty is not assigned as pointwise uncertainty to the five gap records.

## Representative band-parameter fits

For `x approximately 0.25`, `epsilon0=161 meV`:

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

The global constraints are:

```text
Delta = 1 eV, fixed and composition independent
gamma1 = 4.5 +/- 1.5
kappa = -1 +/- 0.5
gamma1 - 2 gamma = 2.5 +/- 0.5
m_h*/m0 = 0.4 +/- 0.1
```

These are source-level constraints, not a pointwise covariance model. The source identifies neglected valence-band warping as the dominant uncertainty in the Luttinger parameters and heavy-hole mass.

## Figure-derived model outputs

Figure 12 gives a nonlinear fitted `Ep(epsilon0)` trend without a printed equation or numerical table. Figures 13 and 14 show electron effective mass and Lande factor calculated from fitted band parameters. These are model-derived outputs, not direct measurements. Figures 12-14 are not digitized.

## Polaron anomalies are separate evidence

For `x=0.28`, `epsilon0=208 meV`, the source reports:

- a `19.5 meV` LO-phonon doublet and level-pinning feature in `sigma-`, with critical field `29.5 kG`;
- `19.5 meV` and `17 meV` pinned branches for `E parallel H`.

The source states that further theoretical analysis is required. These phonon energies and splittings are not intrinsic interaction gaps and do not enter the Hansen gap ledger.

## Part I versus Part II boundary

Part II relies on the model and experimental-method description from Part I. Figure 11 spans `0 <= x <= 0.3` and incorporates the semimetallic regime documented in Part I.

The five Part I scalar gaps are not counted again as independent Part II observations. Exact physical specimen linkage between the articles remains unresolved.

## Hansen HSC_R15 boundary

Five printed Part II candidates are preserved, but Hansen does not expose source-labelled HSC_R15 markers. It remains unclear whether Hansen ingested the printed scalar values, additional Figure 11 points, the combined linear relation, selected transition-derived values, or another transcription.

```text
controlling decision
primary_source_recovered_semiconducting_transition_interaction_gap_candidates_and_x0_reconstructed_hansen_marker_mapping_unresolved
```

This source belongs to Hansen's fitted lineage and cannot independently validate Hansen's empirical equation.

## Authorized and prohibited uses

Authorized:

- retain the five printed 4.2 K interaction-gap candidates with their composition qualifiers;
- retain `x0=0.165+/-0.005` as a source-reported critical composition;
- retain the measurement, composition-method, model, and binary-provenance metadata;
- preserve representative and global band-parameter constraints;
- preserve polaron anomalies as a separate evidence layer;
- preserve Figure 11-14 qualitative roles without digitization.

Not authorized:

- alter or replace the recorded PDF hash without the exact binary;
- invent pointwise composition uncertainty, gap uncertainty, covariance, specimen identity, or cross-part linkage;
- digitize Figure 11-14 without a separate resolution and uncertainty gate;
- count Part I points again as independent Part II observations;
- treat polaron energies or splittings as intrinsic gaps;
- treat calculated mass or Lande-factor curves as direct measurements;
- assign Hansen markers by plot proximity;
- use this fitted-lineage source as independent validation;
- construct a production HgCdTe bandgap relation or manuscript claim from this audit.
