# Submission-readiness checklist

**Manuscript:** Observation-model uncertainty and identifiability in HgCdTe bandgap extraction  
**Status:** scientific asset gate satisfied; editorial and bibliography work remains

## Scientific submission gate

- [x] At least two real spectra pass the fail-closed contract.
- [x] Every plotted spectrum and extracted edge has explicit source and calibration provenance.
- [x] No synthetic record is used as experimental fit authority.
- [x] Free and fixed fractional-power candidates are evaluated.
- [x] Fixed absorption thresholds are evaluated and precision-gated.
- [x] Chu 1994 is enabled only inside its source-supported domain.
- [x] Boundary-limited candidates and exclusions are preserved.
- [x] Model-family, threshold, and combined envelopes are exported.
- [x] Hansen, published Seiler, Laurenti, and provisional Hansen-Pade are compared.
- [x] A scientifically material conclusion changes under admissible observation definitions.
- [x] Composition and carrier uncertainty remain separate identifiability limits.
- [x] No universal correction, selected production edge, or universal Hansen replacement is reported.

## Frozen manuscript assets

- [x] Figure 1: real spectrum with fitted observation models.
- [x] Figure 2: extracted edge versus observation definition.
- [x] Figure 3: material-model residual intervals.
- [x] Figure 4: latent-gap and observation-term identifiability diagram.
- [x] Figure 5: paired `2 x 2 x 2` acquisition design.
- [x] Tables 1-5 required by Issue #129.
- [x] Machine-readable real-spectrum and conceptual summaries.
- [x] Byte-for-byte rebuild tests for every generated asset.
- [x] SHA-256 manifest for every generated asset.
- [x] Working manuscript draft with abstract through conclusions and captions.
- [x] Claim-guard tests derive reported numerical values from the frozen CSV tables.

## Required before journal submission

- [ ] Verify the complete Hansen primary citation from the primary source.
- [ ] Verify the complete Laurenti primary citation and retain the reconstruction limitation.
- [ ] Verify complete author, title, journal, volume, page, and year metadata for all references.
- [ ] Add primary references for carrier-filling and vacancy-edge mechanisms only after exact source verification.
- [ ] Select the target journal and apply its manuscript template, reference style, length limits, and figure requirements.
- [ ] Add author names, affiliations, corresponding-author details, acknowledgments, funding, conflict-of-interest, and contribution statements.
- [ ] Perform a line-by-line technical review against Tables 1-5 and the claim-boundary record.
- [ ] Perform a final typography and notation pass: `band gap` versus `bandgap`, Hg(1-x)Cd(x)Te notation, units, symbols, and significant figures.
- [ ] Export journal-ready raster or vector figures from the frozen SVGs without altering data content.
- [ ] Confirm all focused and full repository workflows pass on the final merge head.

## Optional strengthening evidence

These items may strengthen the paper but are not prerequisites for the current submission claim:

- [ ] Native instrument-export data for the two Moazzami spectra.
- [ ] A clean low-temperature spectrum whose experimental markers can be separated from fitted curves.
- [ ] An independent cross-laboratory spectrum with reported composition uncertainty and carrier state.
- [ ] Same-specimen magneto-optical and absorption measurements implementing the paired design.

Optional evidence must not delay submission unless it changes a controlling conclusion. Chang 2006 remains a low-temperature target, but numerical extraction is not authorized while experimental markers overlap the fitted curves.

## Explicit stop rules

- Do not open another source-screen PR solely to accumulate literature.
- Do not fit another universal empirical HgCdTe coefficient set from the present data.
- Do not select one edge from the exported ensemble.
- Do not identify a fixed absorption threshold with the latent material gap.
- Do not promote the provisional Hansen-Pade relation to a production equation.
- Do not treat the two Moazzami specimens as independent cross-laboratory validation.
