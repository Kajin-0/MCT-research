# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #189  
**Execution mode:** independent, public-data-first, reproducible computation

This is the sole controlling research ledger. `research/active_progress.md` is retired.

## Completed Paper I

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction**

Paper I is scientifically frozen. Historical composition uncertainty, source lineage, specimen state, and edge definition prevent sub-meV universal-law ordering from being interpreted as a specimen-level material result. Remaining work is administrative submission packaging.

## Active flagship manuscript

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

The controlling forward chain is:

```text
latent signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic, tail, and free-carrier response
-> effective thickness and instrument response
-> declared observation operator
-> reported observable
```

Completed milestones:

```text
PR #181  analytical manuscript core
PR #183  deterministic seven-figure and three-table pipeline
PR #185  DOI intake and validation-route gate
PR #188  Dingrong Table 1 reproduction and source-state correction
```

## Publication-framing decision

Issue #189 controls the prior-art and novelty boundary.

The manuscript is framed as:

> **an HgCdTe-specific semiconductor optical-metrology and inverse-problem methods paper**

It is not framed as:

- new general structural-identifiability theory;
- a universal HgCdTe bandgap equation;
- a complete microscopic absorption theory;
- a completely externally validated detector model.

Established prior art includes:

- structural identifiability;
- output-preserving parameter symmetries;
- identifiable parameter combinations;
- the Beer-Lambert optical-depth product;
- thickness-dependent detector cutoff;
- Gaussian gap distributions producing apparent exponential tails.

Candidate application-specific contributions are:

- the explicit HgCdTe combinations `Eg0+Delta`, `sigma_G`, and `A*d`;
- the resulting rank-three bound for the declared distributed spectrum;
- the tail-only Chang rank-two bound;
- the marked-model combined null vector;
- the exact five-parameter spectral counterexample;
- the quantified fit-window and mixed-branch results;
- the Dingrong printed-parameter consistency result;
- the external-measurement prescription implied by the symmetries.

Controlling files:

```text
literature/prior_art/2026-07-21-flagship-rank-theorem-audit.md
data/validation/flagship_novelty_claim_matrix.json
research/decision_records/2026-07-21-flagship-publication-framing.md
manuscript/distributional_band_edge/claim_matrix.md
```

## Central model-specific result

For the declared Gaussian-gap, power-law local edge, uniform carrier translation, and single-pass response, five nominal parameters

```text
Eg0
Delta_carrier
ln sigma_G
ln A
ln d
```

enter only through

```text
Eg0 + Delta_carrier
sigma_G
A*d
```

Therefore

```text
dR/dEg0 = dR/dDelta_carrier
dR/dlnA = dR/dlnd
rank(J) <= 3
```

The amplitude-thickness product is inherited from optical-depth physics. The HgCdTe-specific translated-gap combination, combined rank bound, exact counterexample, and measurement consequences are the candidate contribution.

Two parameter sets preserving the three combinations generate 281-point spectra with maximum difference `2.22e-16`.

A controlled nontranslational carrier marker raises rank to four but leaves one combined null direction. The marker is not the Dingrong free-carrier absorption law.

## Supporting quantitative results

```text
central near-critical latent-law span                25.0803 K
maximum conditional-width linearization error         9.657 K
Herrmann source-window W_fit/s                         0.50504
fit-window increase in apparent W                       60.1%
5-to-20 um synthetic cutoff energy shift             -16.636 meV
5-to-20 um synthetic cutoff wavelength shift          +2.494 um
tail-only cutoff rank                                  <= 2
mixed-branch condition number                         199.81
illustrative high-density parabolic overestimate      147.323 meV
five-density illustrative condition number          11034.75
Dingrong printed-P Fermi-shift RMS discrepancy         11.297 meV
Dingrong row-implied-P Fermi-shift RMS discrepancy      0.785 meV
```

Synthetic values are not specimen fits.

## Obtained sources

The following full texts are already obtained and recorded by DOI, original filename, SHA-256, rights state, and authorized use:

```text
10.1016/0038-1098(85)90315-1   Dingrong 1985
10.1007/s11664-007-0162-0       Chang 2007
10.1063/1.2245220                Chang 2006
```

Disposition record:

```text
literature/acquisition/2026-07-21-obtained-source-disposition.json
```

Restricted PDFs are not committed to the public repository.

## Chang route disposition

The published-paper multi-thickness validation route is rejected.

Chang 2007 Figure 1 is a calculated detector-cutoff curve, not an independent measured same-specimen thickness series. The papers do not supply native multi-thickness spectra, effective-thickness covariance, or the complete same-specimen parameter set required for the previously declared validation.

Chang remains valid prior art and a source-bounded model basis. The project-specific tail-only rank result is analytical, not claimed as external validation.

## Dingrong source-table reproduction

The real source specimen has:

```text
x                         0.19
carrier type              n-type
Hall density              7.0e17 cm^-3
transmission thickness    0.16 mm
refractive index used     3.5
spectral interval         7-17 um
temperatures              77, 100, 200, 300 K
edge operator             extrapolation to 2000 cm^-1
```

Using the printed finite-temperature density equation and printed

```text
P = 8.0e-8 eV cm
```

undershoots the reported Fermi elevations by

```text
-11.193, -12.472, -10.273, -11.142 meV
RMS = 11.297 meV
```

The four rounded rows imply

```text
P = 8.5078, 8.5663, 8.4673, 8.5014 x 10^-8 eV cm
mean = 8.5107 x 10^-8 eV cm
```

Using the row-implied mean as a source-consistency diagnostic reduces the Fermi-shift RMS discrepancy to `0.785 meV`. It is not a revised universal material constant.

The source filled edge and operational optical gap differ by `0-4 meV`, RMS `2.915 meV`.

Controlling record:

```text
data/validation/dingrong1985_table1_reproduction.json
```

Scope boundary:

- the finite-temperature source table is reproduced and audited;
- the complete below-gap free-carrier spectrum is not reproduced;
- external Haga-Tang function definitions are not invented;
- band-gap renormalization is not inferred;
- rounded table values do not replace calibrated native spectra and covariance.

## Manuscript state

The manuscript draft has been revised to:

- incorporate the Dingrong Table 1 result;
- identify general structural-identifiability and optical-depth ingredients as prior art;
- describe rank bounds as model-specific HgCdTe results;
- remove the stale zero-temperature-only Dingrong limitation;
- replace the unconditional external-spectrum blocker with a journal-dependent validation decision;
- preserve explicit source and model boundaries.

Deterministic figures and tables remain controlled by immutable records. No further visual or metadata work is authorized unless required by journal submission.

## Authorized next work

1. complete CI and merge Issue #189;
2. verify complete bibliography metadata for the identifiability, optical-inversion, and HgCdTe sources;
3. decide whether the Dingrong source-table result is sufficient for the selected methods-paper venue or whether one digitized calibrated spectrum is required;
4. perform a targeted digitization only if it changes that submission decision;
5. convert approved SVG figures to journal format;
6. complete archive DOI, authorship, affiliations, CRediT, funding, conflicts, data/code statement, cover letter, and reviewer list.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- treating a reported edge as a latent material gap without an observation operator;
- equating composition width, gap width, Urbach energy, PL FWHM, and quasiparticle linewidth;
- presenting structural identifiability, parameter symmetries, or the Beer-Lambert product as new;
- presenting the Chang calculated thickness curve as independent experimental validation;
- describing the model-specific rank bounds as unprecedented general mathematics;
- silently changing Dingrong's printed parameter to force agreement;
- treating the row-implied `P` as a universal HgCdTe constant;
- conflating carrier filling with band-gap renormalization;
- claiming complete Dingrong free-carrier-spectrum validation from Table 1;
- repeating route-ranking, figure-styling, metadata, or manuscript-architecture infrastructure;
- requiring collaborators before independent progress can continue;
- escalating to expensive first-principles or atomistic work without a decision-changing validation target.
