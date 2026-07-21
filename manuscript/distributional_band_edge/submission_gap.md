# Submission gap and acquisition queue

## Current state

The analytical manuscript core is coherent and independently reproducible. The exact theorem hierarchy, numerical verification records, source-conditioned reproduction, bounded sensitivity calculations, claim matrix, and figure definitions are present.

The manuscript is **not yet ready for journal submission** because external material validation and publication packaging remain incomplete.

## Hard scientific submission blocker

### One calibrated external validation case

At least one real-spectrum case must test a forward operator without silently assigning missing specimen parameters.

A qualifying case should provide as many of the following as possible:

- source-native or auditable numerical spectrum;
- independently measured composition and uncertainty;
- measurement temperature;
- carrier type and density;
- physical and effective optical thickness provenance;
- reflectance or transmission convention;
- spectral resolution and calibration;
- edge/cutoff definition;
- fitted-parameter covariance or enough raw data to estimate it;
- processing and annealing state.

The validation does not need to identify every unified-model parameter. It must test at least one declared forward prediction while preserving unresolved parameters as nuisance or bounded quantities.

## Preferred validation routes

### Route A — Multi-thickness absorption or detector response

Test the exact exponential-tail prediction

```text
E_cut(d2)-E_cut(d1)=-W ln(d2/d1)
```

on the same material state or on a source series with defensible common optical parameters.

Minimum required provenance:

- effective thickness or optical-depth calibration;
- common tail width or independently fitted `W`;
- response criterion;
- evidence that the crossings remain on the tail branch.

### Route B — Same-specimen carrier-state series

Use Hall-measured carrier density and calibrated spectra at multiple density or temperature states. Test whether the optical edge follows the declared nonparabolic filling trend after retaining a separate renormalization term.

Minimum required provenance:

- same specimen or demonstrably equivalent specimens;
- Hall density and carrier type;
- temperature;
- mass/nonparabolicity assumptions;
- full spectrum or source-native edge values;
- free-carrier background treatment.

### Route C — Processing-conditioned PL displacement and linewidth

Test whether one declared distributional state can jointly predict PL displacement and FWHM across as-grown and annealed states.

This is a falsification route: failure of one-width closure is scientifically useful and consistent with the manuscript’s thesis.

## DOI acquisition queue for user-assisted paper retrieval

The user can assist by locating full-text papers or supplements using the exact DOIs below. Files should be added without changing the source claim until the equation and data audit is complete.

### Priority 1 — Direct validation blockers

#### Dingrong carrier-filled spectrum

```text
10.1016/0038-1098(85)90315-1
```

Need:

- complete equations for interband filling and below-gap absorption;
- all band, phonon, dielectric, and scattering parameters;
- tabulated or digitizable spectra at 77–300 K;
- source definition of the reported optical edge;
- any uncertainty or specimen-thickness information.

Potential payoff:

- replace the generic carrier marker with a source-grounded carrier-dependent spectral branch;
- test the nonparabolic filling calculation at a real high-density state.

#### Chang nonparabolic-Urbach and thickness response

```text
10.1007/s11664-007-0162-0
```

Need:

- complete fitted parameter tables;
- same-specimen `W`, `b`, amplitude, temperature, carrier state, and thickness;
- native or high-resolution spectra;
- exact 50% detector-response construction;
- any supplement or cited dataset containing Figure 2 values.

Potential payoff:

- external validation of the thickness/cutoff operator;
- determine whether mixed intrinsic/tail observations are feasible from one source.

#### Chang 2006 short-form paper

```text
10.1063/1.2245220
```

Need:

- the original analytical equations and continuity conventions;
- higher-quality Figure 2 or source data;
- any parameter values omitted or changed in the 2007 expansion.

Potential payoff:

- resolve discrepancies between the 2006 and 2007 presentations;
- improve source provenance for the implemented Chang operator.

### Priority 2 — Distributional and cross-modal validation

#### Herrmann multimodal broadening

```text
10.1016/0022-0248(92)90851-9
```

Need:

- complete Anderson formulas and band-filling definitions referenced by the paper;
- numerical parameters for the absorption, photoconductivity, and luminescence examples;
- any tables or source-quality figures suitable for digitization.

Potential payoff:

- extend the current source-scale reproduction into a fuller multimodal spectrum test;
- determine whether one distributional model can survive cross-modal comparison.

#### Ivanov-Omskii annealing and PL disorder

```text
10.1016/j.physb.2009.08.210
```

Need:

- the full localization equation lineage;
- tabulated temperature-dependent PL peak and FWHM values, not only summary values;
- composition estimates before and after annealing;
- excitation and instrumental linewidth details.

Potential payoff:

- test whether one width parameter can jointly explain PL displacement and FWHM;
- create an independent processing-state validation section.

#### Finkman exponential band tail

```text
10.1063/1.333828
```

Need:

- complete temperature/composition dependence of the exponential tail;
- specimen and absorption-method details;
- any numerical tables or high-quality figures.

Potential payoff:

- independent tail model against which to test the fit-window non-uniqueness result.

### Priority 3 — Near-critical and prior-art boundaries

#### Teppe temperature-driven Kane transition

```text
10.1038/ncomms12576
```

Need:

- supplementary information;
- sample-specific composition uncertainty;
- fitted gap/mass covariance;
- full temperature and field series;
- exact simplified Kane-model assumptions.

Potential payoff:

- test transition-width propagation against a real same-specimen temperature series;
- strengthen the distinction between a local gap-sign distribution and a measured magneto-optical transition.

#### Krishtopenko disorder-induced transition

```text
10.1103/PhysRevB.106.115203
```

Need:

- supplement or arXiv source if available;
- exact disorder parameter definitions and mapping to Cd-composition fluctuations;
- predicted observable quantities, not only phase boundaries.

Potential payoff:

- sharpen the novelty boundary between microscopic disorder renormalization and the present observation-operator transition width.

#### Chu intrinsic absorption spectroscopy

```text
10.1016/0020-0891(91)90110-2
```

Need:

- parameter tables across `x=0.165-0.45` and `4.2-300 K`;
- native or digitizable absorption spectra;
- reported Burstein-Moss, Urbach, and intrinsic-carrier treatments;
- exact edge definitions.

Potential payoff:

- potentially supply a broader real-spectrum validation case than Chang.

### Priority 4 — Existing Paper I spectrum provenance

#### Moazzami spectroscopic ellipsometry

```text
10.1007/s11664-005-0019-3
```

Need:

- any author-supplied numerical data behind Figure 6;
- ellipsometry model files or optical constants;
- specimen carrier and composition uncertainty not present in the article.

Potential payoff:

- convert the existing calibrated digitization into source-native external data;
- link Paper I and the flagship paper without merging their scientific claims.

## How to add a retrieved paper

For each obtained source:

1. preserve the original filename and DOI in acquisition metadata;
2. record whether the file is publisher PDF, author manuscript, supplement, or extracted data;
3. do not commit copyrighted PDFs to a public repository unless distribution rights are clear;
4. commit only source notes, permitted data, digitization records, equations, and hashes;
5. update `literature/ledger.md` and the relevant source-audit note;
6. open a source-audit issue before modifying a scientific operator.

## Publication packaging still required

### Figures and tables

- implement `scripts/build_distributional_band_edge_manuscript_assets.py`;
- render Figures 1–7 from `figure_manifest.json`;
- regression-test all headline values;
- generate vector figures and manuscript tables.

### Bibliography

- verify title, author order, year, volume, pages, and DOI for every cited source;
- distinguish the 2006 and 2007 Chang papers;
- verify all reconstructed historical gap-law citations;
- add Paper I citation only after its archival identifier exists.

### Manuscript editing

- integrate stable proposition and theorem labels from `theorem_index.md` into the final manuscript format;
- reduce repeated caveats by using claim-state labels and a consolidated limitations section;
- perform notation consistency review for `Eg0`, signed gap, `G`, `sigma_G`, `W`, `s`, `A`, and `d`;
- separate material-state parameters from observation-operator parameters in every table and caption.

### Administrative packaging

- authors and affiliations;
- CRediT roles;
- conflicts and funding statements;
- data/code availability statement;
- archive DOI and immutable release;
- suggested reviewers and exclusions;
- cover letter;
- journal-specific formatting.

## Journal-positioning decision

The manuscript should be positioned as an analytical and computational **semiconductor optical metrology / inverse-problem** paper, not as a new universal HgCdTe bandgap equation and not as a first-principles materials calculation.

Candidate venue classes, to be selected after external validation:

1. applied-physics journal with strong analytical and optical-spectroscopy scope;
2. semiconductor-materials journal familiar with HgCdTe characterization;
3. instrumentation/metrology journal if the external validation becomes the dominant contribution.

The venue should not be fixed before the validation route determines whether the paper reads primarily as physics, semiconductor characterization, or measurement science.

## Submission decision rule

Submission is authorized when all of the following are true:

- all exact theorem statements pass code and manuscript consistency checks;
- all synthetic results are visibly labeled;
- one external validation case is complete or the paper is explicitly reframed and internally approved as a theorem/methods paper without specimen-level validation;
- final figures are generated from immutable data;
- bibliography and prior-art boundaries are verified;
- archive and authorship metadata are complete.

External collaborators are not a prerequisite. Public full texts, author manuscripts, supplements, auditable digitization, and reproducible computation remain the primary acquisition strategy.