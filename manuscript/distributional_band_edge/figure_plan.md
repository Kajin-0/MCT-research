# Figure plan and implemented asset contract

## Governing rule

Every quantitative plotted value is loaded from an immutable repository record or regenerated through a tested public function. No value is copied manually from manuscript prose.

Every figure distinguishes among:

- exact theorem or invariant;
- numerical verification;
- source-conditioned reproduction;
- bounded synthetic sensitivity;
- external material validation.

Synthetic and source-conditioned panels carry explicit status labels. No generated figure claims external specimen validation.

## Implemented entry point

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

The public module is a thin deterministic presentation wrapper around the preserved numerical generation core:

```text
tools/build_distributional_band_edge_manuscript_assets.py
tools/_distributional_asset_core.py
```

The wrapper changes only SVG presentation details. It does not alter calculated arrays, fitted quantities, singular values, or immutable records.

## Figure 1 — Forward hierarchy from latent gap to reported observable

**Filename:** `figure1_forward_hierarchy.svg`  
**Claims:** C01, C20, C21  
**Evidence state:** conceptual definition

### Content

```text
latent signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic and tail absorption
-> optical depth / thickness / instrument
-> declared edge or cutoff operator
-> reported observable
```

The second region defines the manuscript evidence states:

```text
exact theorem
numerical verification
source reproduction
bounded synthetic sensitivity
external material validation
```

### Message

A reported edge is an output of a forward chain, not an unqualified scalar material property.

## Figure 2 — Near-critical transition broadening and censoring

**Filename:** `figure2_transition_distribution.svg`  
**Claims:** C02–C04  
**Evidence state:** bounded synthetic sensitivity  
**Record:** `data/validation/near_critical_transition_model_dependence.json`

### Panels

A. Central critical temperature by latent law, with the `25.080275 K` span.  
B. Exact conditional width and local linearized width versus `sigma_x`.  
C. Single-crossing and always-normal probabilities.  
D. Absolute local-width approximation error.

Exact and local/probability-pair curves are distinguished by line weight and opacity; latent laws are distinguished by line style.

### Boundary

Neither probability curve is labeled or interpreted as a measured topological phase fraction.

## Figure 3 — One distributed spectrum, multiple apparent tail energies

**Filename:** `figure3_herrmann_tail_nonuniqueness.svg`  
**Claims:** C05–C08  
**Evidence state:** source reproduction plus synthetic observation-operator sensitivity  
**Record:** `data/validation/herrmann_gaussian_tail_reproduction.json`

### Regenerated operator

The source-aligned square-root spectrum is regenerated through:

```text
mct_research.normalized_gaussian_gap_convolved_power_absorption
mct_research.fit_exponential_absorption_tail
```

Declared fit windows:

```text
0.1-100 cm^-1
1-100 cm^-1
10-100 cm^-1
10-500 cm^-1
100-500 cm^-1
```

### Panels

A. Regenerated Gaussian-gap-convolved absorption.  
B. `W_fit/s` by fit window, including the `60.1%` increase.  
C. `R^2` versus `W_fit/s`, showing that high fit quality does not select one width.  
D. Declared `sigma_G=6.995-12.661 meV` interval for an observed 4 meV tail.

The interval is not drawn or described as a posterior distribution.

## Figure 4 — Thickness-defined cutoff and tail-only rank limit

**Filename:** `figure4_chang_cutoff_rank.svg`  
**Claims:** C09–C12  
**Evidence state:** exact theorem plus bounded synthetic sensitivity  
**Record:** `data/validation/chang_2006_cutoff_identifiability.json`

### Panels

A. 50% cutoff energy versus effective thickness, with intrinsic/tail branch markers.  
B. Equivalent cutoff wavelength.  
C. Tail-only relative singular values, showing rank two.  
D. Mixed intrinsic/tail relative singular values, showing rank four and condition number `199.81`.

### Required annotations

```text
5-to-20 um energy shift      -16.636 meV
5-to-20 um wavelength shift   +2.494 um
```

### Boundary

Effective thickness is an observation-model parameter and is not automatically physical film thickness.

## Figure 5 — Nonparabolic carrier filling and inversion conditioning

**Filename:** `figure5_carrier_filling.svg`  
**Claims:** C13–C15  
**Evidence state:** exact dispersion identity plus bounded synthetic sensitivity  
**Record:** `data/validation/dingrong_1985_carrier_filling_sensitivity.json`

### Regenerated operator

The density series is regenerated through:

```text
mct_research.carrier_filled_optical_edge_ev
```

and compared against the immutable crossover record before rendering.

### Panels

A. Parabolic and nonparabolic conduction filling energies versus density.  
B. Parabolic overestimate versus density.  
C. High-density energy decomposition.  
D. Five-density relative singular values and condition number `11034.75`.

### Required annotation

```text
parabolic overestimate at 7e17 cm^-3 = 147.323 meV
```

### Boundary

The declared masses and nonparabolicity are not a fit to the Dingrong specimen.

## Figure 6 — Exact spectral equivalence and structural rank

**Filename:** `figure6_unified_structural_rank.svg`  
**Claims:** C16–C20  
**Evidence state:** exact structural theorem plus numerical verification  
**Record:** `data/validation/unified_spectrum_structural_rank.json`

### Regenerated operator

Both exact-counterexample spectra are regenerated through:

```text
mct_research.unified_response_spectrum
```

They must remain equal within the committed machine-precision bound.

### Panels

A. Overlaid response spectra for the two physically different parameter sets, annotated

```text
max |difference| <= 2.22e-16
```

B. Unmarked relative singular values and rank three.  
C. Marked relative singular values and rank four.  
D. Exact invariant combinations and remaining marked-model null vector:

```text
(Delta, -Delta, 0, -1, +1)
```

### Message

Dense, noise-free sampling cannot recover parameters that the forward model combines exactly.

## Figure 7 — Measurement design and validation boundary

**Filename:** `figure7_measurement_design.svg`  
**Claims:** C20–C23  
**Evidence state:** measurement-design corollary and validation boundary

### Content

The first region states the base-model requirement:

```text
full calibrated spectrum
+ independent carrier state / validated shift
+ independent effective thickness or absorption amplitude
= locally identifiable remaining base parameters
```

The second region presents the analytical, numerical, source-reproduction, and real-spectrum validation status of each forward component.

### Message

The analytical core and deterministic figures are complete. External specimen validation remains open.

## Tables

### Table 1 — Theorem and proposition summary

**Filename:** `table1_theorem_summary.md`

Summarizes label, assumptions, result, and evidence class for the stable theorem hierarchy.

### Table 2 — Quantitative headline results

**Filename:** `table2_quantitative_results.md`

Loads the manuscript headline values directly from the five immutable JSON records.

### Table 3 — Claim provenance and validation status

**Filename:** `table3_claim_provenance.md`

Extracts C01–C23 from `claim_matrix.md` and preserves each claim class and current status.

## Asset summary

**Filename:** `distributional_band_edge_asset_summary.json`

Records:

- generating commit;
- exact generated filename list;
- figure and table counts;
- immutable source-record paths;
- explicit `external_material_validation=false` state;
- claim-boundary statement.

## Rendering contract

- Implemented final-review vector format: SVG.
- Planned journal-delivery vector format: PDF converted from approved SVG without changing data.
- Do not use color as the only encoding.
- Display units on every quantitative axis.
- Preserve the Herrmann `s` and `sigma_G` convention exactly.
- Include accessible SVG titles.
- Include record path, claim IDs, and generating commit in SVG metadata.
- Label synthetic and source-conditioned figures explicitly.
- Require byte-for-byte deterministic regeneration.
- Fail generation when regenerated headline values diverge from immutable records beyond declared tolerances.

## Validation

The builder is covered by:

```text
tests/test_distributional_band_edge_manuscript_assets.py
tests/test_distributional_band_edge_generated_assets.py
```

CI generates the complete review package, parses every SVG as XML, checks exact filenames and metadata, verifies all three tables, tests deterministic regeneration, enforces the visual-presentation fixes, and uploads the package as a workflow artifact.
