# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #187  
**Execution mode:** independent, public-data-first, reproducible computation

This is the sole controlling research ledger. `research/active_progress.md` is retired.

## Completed Paper I

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction**

Paper I is scientifically frozen. Historical composition uncertainty, source lineage, specimen state, and edge definition prevent sub-meV universal-law ordering from being interpreted as a specimen-level material result. Remaining actions are administrative submission packaging.

## Active flagship manuscript

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

The controlling forward chain is:

```text
latent signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic, tail, and free-carrier response
-> thickness/instrument response
-> declared observation operator
-> reported observable
```

The analytical core was merged in PR #181. Deterministic manuscript figures and tables were merged in PR #183. DOI intake and route selection were merged in PR #185.

## Principal theorem

For the declared Gaussian-gap, power-law local-edge, uniform carrier-translation, and single-pass Beer-Lambert model, five nominal parameters

```text
Eg0
Delta_carrier
ln sigma_G
ln A
ln d
```

enter a dense single-state spectrum only through

```text
Eg0 + Delta_carrier
sigma_G
A*d
```

Therefore:

```text
dR/dEg0 = dR/dDelta_carrier
dR/dlnA = dR/dlnd
rank(J) <= 3
```

Two physically different parameterizations preserving those combinations produce 281-point spectra differing by no more than the committed numerical bound `2.22e-16`. A calibrated nontranslational carrier marker raises rank to four but leaves one combined null direction.

This is the flagship manuscript's principal result. Component studies are supporting physical corollaries, not separate repetitions of the same conclusion.

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
```

Synthetic values are not specimen fits.

## Obtained-source correction

The following full texts were already available and have now been recorded by DOI, original filename, rights state, and SHA-256 in:

```text
literature/acquisition/2026-07-21-obtained-source-disposition.json
```

```text
10.1016/0038-1098(85)90315-1   Dingrong 1985
10.1007/s11664-007-0162-0       Chang 2007
10.1063/1.2245220                Chang 2006
```

Restricted PDFs are not committed to the public repository.

## Chang route disposition

The proposed published-paper multi-thickness validation is rejected.

Chang 2007 Figure 1 is a calculated detector-cutoff curve, not an independent measured same-specimen thickness series. The 2006 and 2007 papers do not supply the native multi-thickness spectra, effective-thickness covariance, or same-specimen `W`, `b`, and amplitude required for the declared validation.

Chang Figure 3 remains eligible for a later single-spectrum absorption reproduction, but it is not the present milestone.

Issue #186 was closed without merging its design branch.

## Active Dingrong source-table reproduction

Issue #187 tests the real In-doped specimen reported by Dingrong et al.:

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

The source supplies an explicit finite-temperature Kane density integral and Table 1 values for the intrinsic-gap input, Fermi elevation, total filled edge, and operational optical gap.

### Source-internal consistency result

Using the printed equation with the printed momentum matrix

```text
P = 8.0e-8 eV cm
```

undershoots the four printed Fermi elevations by approximately:

```text
-11.193, -12.472, -10.273, -11.142 meV
RMS = 11.297 meV
```

The four rounded table rows independently imply:

```text
P = 8.5078, 8.5663, 8.4673, 8.5014 x 10^-8 eV cm
mean = 8.5107 x 10^-8 eV cm
```

Using that row-implied mean reduces the Fermi-shift RMS discrepancy to `0.785 meV`. This is a source-consistency inference from rounded table values, not a new universal momentum matrix.

The source's own filled-edge values differ from its operational optical gaps by `0-4 meV` across the four temperatures.

Controlling record:

```text
data/validation/dingrong1985_table1_reproduction.json
```

Scope boundary:

- source Table 1 reproduction is active;
- complete below-gap free-carrier spectrum validation remains incomplete;
- external Haga/Tang definitions required by the below-gap branch are not silently invented;
- band-gap renormalization is not inferred;
- source intrinsic-gap inputs are not endorsed as a universal law;
- calibrated native spectra and covariance remain absent.

## Manuscript and infrastructure freeze

No additional figure styling, route-score refinement, metadata framework, or manuscript reorganization is authorized unless it directly supports the Dingrong reproduction, a targeted rank-theorem prior-art audit, or final journal submission.

## Authorized next work

1. complete and CI-validate Issue #187;
2. compare the source finite-temperature integral with the existing illustrative zero-temperature carrier approximation;
3. integrate the qualified source-table result into the flagship claim matrix and manuscript;
4. perform a targeted prior-art audit of the unified rank theorem and tail-only rank theorem;
5. decide whether the source-table result is sufficient for a methods paper or whether one digitized/full-spectrum case is still required;
6. complete bibliography, archive DOI, authorship, declarations, and journal packaging.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- treating a reported edge as a latent material gap without an observation operator;
- equating composition width, gap width, Urbach energy, PL FWHM, and quasiparticle linewidth;
- presenting the Chang calculated thickness curve as independent experimental validation;
- silently changing Dingrong's printed parameter to force agreement;
- treating the row-implied `P` as a universal HgCdTe constant;
- conflating carrier filling with band-gap renormalization;
- claiming complete Dingrong free-carrier-spectrum validation from Table 1;
- repeating route-ranking or manuscript-packaging infrastructure before a scientific validation result;
- requiring collaborators before independent progress can continue;
- escalating to expensive first-principles or atomistic work without a decision-changing validation target.
