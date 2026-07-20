# Submission-readiness checklist

**Manuscript:** Observation-model uncertainty and identifiability in HgCdTe band-gap extraction  
**Status:** scientific, bibliography, target-journal, LaTeX, technical-review, and render gates satisfied; author-supplied submission metadata remains

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
- [x] Figure 5: paired complete-factorial `2 x 2 x 2` acquisition design.
- [x] Tables 1-5 required by Issue #129.
- [x] Machine-readable real-spectrum and conceptual summaries.
- [x] Byte-for-byte rebuild tests for every generated asset.
- [x] SHA-256 manifest for every generated asset.
- [x] Working manuscript draft with abstract through conclusions and captions.
- [x] Claim-guard tests derive reported numerical values from the frozen CSV tables.

## Verified bibliography gate

- [x] Verify the complete Hansen citation.
- [x] Verify the complete Seiler citation.
- [x] Verify the complete Laurenti citation and retain the reconstruction limitation.
- [x] Verify the complete Chu 1994 citation.
- [x] Verify the complete Moazzami 2005 citation.
- [x] Add an HgCdTe-specific primary carrier-filling/Burstein-Moss reference.
- [x] Add an HgCdTe-specific primary mercury-vacancy absorption-edge reference.
- [x] Record reference roles and authority limits in `verified_references.md`.

## Target-journal gate

- [x] Select *Infrared Physics & Technology* as the primary target.
- [x] Record *Journal of Electronic Materials* as fallback and *Journal of Applied Physics* as stretch target.
- [x] Confirm the research-paper scope includes infrared materials, characterization, semiconductor physics, and validated modeling.
- [x] Reduce the submission abstract below the 250-word limit.
- [x] Provide seven keywords.
- [x] Provide five highlights, each no longer than 85 characters.
- [x] Add data-availability and generative-AI declaration language.
- [x] Preserve fail-closed placeholders for author, affiliation, funding, conflict, CRediT, acknowledgment, archive, and reviewer details.

## Manuscript production gate

- [x] Convert the working manuscript to editable Elsevier LaTeX with numbered cross-references.
- [x] Render the verified reference ledger in Elsevier numeric bibliography style.
- [x] Perform a line-by-line technical review against Tables 1-5 and the claim-boundary record.
- [x] Perform a final typography and notation pass: `band gap` versus `bandgap`, Hg1-xCdxTe notation, units, symbols, and significant figures.
- [x] Export journal-ready vector figures from the frozen SVGs without altering data content.
- [x] Add final alt text for all figures.
- [x] Compile the full manuscript under TeX Live 2026.
- [x] Render and inspect every PDF page for clipping, overlap, broken glyphs, and table overflow.
- [x] Confirm all focused and full repository workflows pass on the reviewed head.

## Author-supplied fields required before submission

- [ ] Replace author, affiliation, corresponding-author, and postal-address placeholders.
- [ ] Add the public archive DOI or final repository URL.
- [ ] Confirm the funding statement.
- [ ] Confirm the competing-interest statement.
- [ ] Assign CRediT roles.
- [ ] Confirm acknowledgments or explicitly omit them.
- [ ] Select conflict-free suggested reviewers.

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
