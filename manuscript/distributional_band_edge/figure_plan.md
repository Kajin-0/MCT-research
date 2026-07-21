# Figure plan

## Governing rule

Every plotted quantitative value must be loaded from an immutable repository record or regenerated through a tested public function. No value is to be copied manually from prose.

All figures must distinguish:

- exact theorem or invariant;
- source reproduction;
- bounded synthetic sensitivity;
- external material validation.

Synthetic panels must carry an explicit `synthetic sensitivity` label in the caption or panel title.

## Figure 1 — Forward hierarchy from latent gap to reported observable

### Purpose

Define the object of the paper and prevent a reported edge from being read as `Eg(x,T)` without an observation operator.

### Panels

**A. Forward hierarchy**

```text
latent signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic and tail absorption
-> optical depth / thickness / instrument
-> declared edge or cutoff operator
-> reported observable
```

**B. Claim classes**

Show the five evidence states used by the manuscript:

```text
exact theorem
numerical verification
source reproduction
bounded synthetic sensitivity
external material validation
```

### Data

No numerical data. Render from the definitions in `README.md` and `claim_matrix.md`.

### Message

The measured edge is the output of a forward chain, not an unqualified scalar material property.

## Figure 2 — Near-critical transition broadening and censoring

### Purpose

Show that latent-law choice and specimen composition variation affect different parts of the apparent transition distribution.

### Data record

`data/validation/near_critical_transition_model_dependence.json`

### Panel A — Central transition temperature by latent law

- x-axis: latent law;
- y-axis: `central_critical_temperature_k`;
- annotate the cross-model span `25.080275 K`.

### Panel B — Conditional transition width versus composition sigma

For each entry of `latent_gap_models`:

- x-axis: `composition_sigma`;
- y-axis: `conditional_sigma_temperature_k`;
- dashed comparison: `linearized_sigma_temperature_k`.

### Panel C — Single-crossing and always-normal probabilities

- x-axis: `composition_sigma`;
- y-axis: probability;
- plot `single_crossing_probability` and `always_normal_probability`;
- do not label either curve as a topological phase fraction.

### Panel D — Local approximation error

- x-axis: `composition_sigma`;
- y-axis: `sigma_approximation_error_k`;
- emphasize the broad-distribution censoring regime.

### Message

At small `sigma_x`, latent-law spread dominates. At larger `sigma_x`, conditional-root censoring invalidates a simple Gaussian transition-width interpretation.

### Claim IDs

C02–C04.

## Figure 3 — One distributed spectrum, multiple apparent Urbach energies

### Purpose

Demonstrate the non-unique inversion from an exponential-looking tail to a gap-distribution width.

### Data and implementation

- `data/validation/herrmann_gaussian_tail_reproduction.json`;
- `src/mct_research/spectral_convolution.py`.

### Panel A — Convolved absorption and fit windows

Regenerate the source-aligned square-root spectrum. Plot `log10(alpha)` versus normalized energy. Overlay the five declared absorption windows:

```text
0.1-100 cm^-1
1-100 cm^-1
10-100 cm^-1
10-500 cm^-1
100-500 cm^-1
```

### Panel B — Apparent tail energy versus fit window

- x-axis: fit-window label;
- y-axis: `W_fit/s`;
- annotate `0.50504` for the source window and `0.80871` for the upper window;
- annotate the `60.1%` increase.

### Panel C — High R-squared does not imply a unique width

Plot `R^2` against `W_fit/s` for all windows. The intended visual is that several fits have `R^2 > 0.99` while producing materially different tail energies.

### Panel D — Inversion interval for an observed 4 meV tail

Display the declared operator-family interval

```text
sigma_G = 6.995-12.661 meV
```

as an interval, not as a posterior distribution.

### Message

The same spectrum can support several strong exponential fits with different inferred tail scales.

### Claim IDs

C05–C08.

## Figure 4 — Thickness-defined cutoff and tail-only rank limit

### Purpose

Show that geometry moves detector cutoff and that repeated tail-only cutoffs do not recover all absorption parameters.

### Data and implementation

- `data/validation/chang_2006_cutoff_identifiability.json`;
- `src/mct_research/detector_cutoff.py`.

### Panel A — 50% cutoff energy versus effective thickness

Use `half_response_cutoffs`:

- x-axis: effective thickness in um, logarithmic scale;
- left y-axis: cutoff energy in meV;
- distinguish intrinsic and tail branches;
- annotate the 5-to-20 um shift `-16.636 meV`.

### Panel B — Equivalent cutoff wavelength

- x-axis: effective thickness in um;
- y-axis: cutoff wavelength in um;
- annotate the 5-to-20 um shift `+2.494 um`.

### Panel C — Tail-only singular values

Plot relative singular values from `all_tail_design`. Show two resolved and two near-null directions.

### Panel D — Mixed-branch singular values

Plot relative singular values from `mixed_branch_design`. Annotate rank four and condition number `199.81`.

### Message

Thickness changes the reported cutoff without changing latent `Eg`; branch diversity, not more tail-only points, is required to restore rank.

### Claim IDs

C09–C12.

## Figure 5 — Nonparabolic carrier filling and inversion conditioning

### Purpose

Quantify when a parabolic Burstein–Moss treatment fails and show that a density series can remain practically non-identifying.

### Data and implementation

- `data/validation/dingrong_1985_carrier_filling_sensitivity.json`;
- `src/mct_research/carrier_filling.py`.

### Panel A — Conduction filling energy versus density

Regenerate over the declared density sweep:

- x-axis: carrier density in `cm^-3`, logarithmic;
- y-axis: energy in meV;
- plot parabolic and nonparabolic conduction energies.

### Panel B — Parabolic overestimate

- x-axis: carrier density;
- y-axis: `E_par-E_c` in meV;
- mark the 5% crossover near `2.66e15 cm^-3`;
- mark the declared Dingrong-density point and `147.323 meV` overestimate.

### Panel C — Filling decomposition at `7e17 cm^-3`

Display:

```text
nonparabolic conduction 140.154 meV
valence recoil            8.214 meV
nonparabolic BM total   148.367 meV
parabolic BM total      295.690 meV
```

Label all values as bounded synthetic sensitivity.

### Panel D — Density-series singular values

Plot the five relative singular values and annotate condition number `11034.75`.

### Message

Nonparabolicity is not a perturbative correction at the declared high-density point, and formal full rank is not sufficient for a stable physical inversion.

### Claim IDs

C13–C15.

## Figure 6 — Exact spectral equivalence and structural rank

### Purpose

Present the central theorem visually.

### Data and implementation

- `data/validation/unified_spectrum_structural_rank.json`;
- `src/mct_research/unified_spectrum.py`.

### Panel A — Two physically different parameterizations

List the two exact-counterexample parameter sets and their preserved combinations:

```text
Eg0 + Delta = 0.130 eV
A*d = constant
sigma_G = 0.010 eV
```

### Panel B — Overlaid response spectra

Plot both 281-point spectra. They should visually overlap completely.

Inset or residual panel:

- plot absolute difference versus energy;
- annotate maximum `2.22e-16`.

### Panel C — Unmarked-spectrum singular values

Plot relative singular values. Annotate rank three and identify the two exact null mechanisms:

```text
Eg0 versus uniform carrier translation
absorption amplitude versus effective thickness
```

### Panel D — Marked-spectrum singular values and null vector

Plot marked-spectrum relative singular values. Annotate rank four and the remaining infinitesimal null vector:

```text
(Delta, -Delta, 0, -1, +1)
```

### Message

Dense, noise-free sampling cannot recover parameters that the forward model combines exactly.

### Claim IDs

C16–C20.

## Figure 7 — Measurement design and validation boundary

### Purpose

Translate the theorems into the minimum evidence needed for latent-gap recovery and clearly distinguish completed analytical work from external validation.

### Panel A — Base model external constraints

```text
full spectrum
+ independent carrier state / validated shift
+ independent effective thickness or absorption amplitude
= locally identifiable remaining base parameters
```

### Panel B — Marked model

```text
calibrated carrier-dependent spectral marker
raises rank 3 -> 4
but one independent scale remains necessary
```

### Panel C — Validation status

Use a compact status table:

| Component | Analytical | Numerical | Source reproduction | Real-spectrum validation |
|---|---:|---:|---:|---:|
| Transition distribution | yes | yes | not applicable | no |
| Herrmann tail | yes | yes | yes | no new specimen |
| Chang cutoff | yes | yes | source-bounded | no |
| Carrier filling | yes | yes | regime anchor | no |
| Unified theorem | yes | yes | not applicable | no |

### Message

The analytical paper is coherent and reproducible, but specimen-level validation remains an explicit and visible submission boundary.

## Tables

### Table 1 — Theorem and proposition summary

Generate from `theorem_index.md` with columns:

```text
label
assumptions
result
evidence class
external constraint implied
```

### Table 2 — Quantitative results

Generate from the five immutable JSON records with one row per manuscript headline result.

### Table 3 — Claim boundary and source provenance

Generate from `claim_matrix.md` and the primary-source audit.

## Rendering requirements

- Never encode synthetic and external-data panels identically.
- Use vector output for final submission (`PDF` or `SVG`) and high-resolution PNG only for review.
- Do not use color alone to distinguish claim state or model family.
- Display units on every numerical axis.
- Preserve the exact source convention for Herrmann `s` and `sigma_G`.
- Use logarithmic axes only where explicitly declared above.
- Include record path and generating commit in each figure metadata block.

## Planned generation entry point

The final asset builder should be added as:

```text
scripts/build_distributional_band_edge_manuscript_assets.py
```

with outputs under:

```text
manuscript/distributional_band_edge/generated/
```

The builder must read the immutable JSON records, regenerate spectra through public package functions, and fail if manuscript headline values differ from the committed records beyond declared tolerances.