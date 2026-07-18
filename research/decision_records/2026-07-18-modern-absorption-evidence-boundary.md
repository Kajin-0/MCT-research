# Modern primary HgCdTe absorption evidence boundary

**Date:** 2026-07-18  
**Status:** controlling evidence decision  
**Decision:** authorize observation-model research; do not authorize a production correction or static-gap refit.

## Question

Do modern, accessible primary HgCdTe absorption studies provide evidence that can advance the project despite the lack of a second fully provenance-complete `x-Eg-T` point dataset?

## Distinct authority classes

The audit separates three scientific uses:

1. **Static material-gap fit authority** requires point-level gap observations, independent composition metrology, temperature, measurement definition, and uncertainty.
2. **Absorption observation-model authority** requires the primary measurement method and curve to be recoverable independently of a new material-gap claim.
3. **Mechanism authority** may establish how defects, carrier filling, Fermi level, or extraction definitions bias the observed edge without supplying a universal gap equation.

Conflating these classes would either discard valuable spectra or incorrectly promote measurement curves into material-law evidence.

## Chang et al. 2006

Source: Yong Chang et al., *Applied Physics Letters* 89, 062109 (2006), DOI `10.1063/1.2245220`.

Recovered:

- author-posted primary full text;
- measured absorption curve for nominal `Hg0.79Cd0.21Te` near `80 K`;
- explicit Urbach/intrinsic-region model and operational transition energy;
- n-type conductivity and carrier concentration in the low `1e15 cm-3` range;
- partial defect characterization.

Missing:

- machine-readable absorption points;
- archived primary figure image and axis calibration in this repository;
- point uncertainty;
- independent composition-method provenance within the recovered paper.

Classification:

- absorption observation-model authority: **conditional**;
- static material-gap fit authority: **blocked**.

## Moazzami et al. 2005

Source: K. Moazzami et al., *Journal of Electronic Materials* 34, 773-778 (2005), DOI `10.1007/s11664-005-0019-3`.

Recovered:

- author-posted primary full text;
- twelve MBE samples on CdZnTe with reported range `x=0.22-0.60`;
- FTIR transmission over `40-300 K`;
- room-temperature spectroscopic ellipsometry on four samples;
- same-specimen FTIR/ellipsometry agreement near absorption turn-on;
- composition- and temperature-dependent absorption-model parameters.

Critical boundary:

- growth, composition, and thickness details are deferred to earlier publications;
- the final absorption model explicitly inserts the Hansen bandgap equation;
- extracted bandgap values therefore do not form an independent material-gap validation dataset.

Classification:

- absorption observation-model authority: **conditional**;
- cross-method observation evidence: **valuable**;
- static material-gap fit authority: **blocked**.

## Moazzami et al. 2004

Source: *physica status solidi (c)* 1, 662-665 (2004), DOI `10.1002/pssc.200304161`.

Recovered only from the primary abstract:

- MBE layers;
- automated compositional control by spectroscopic ellipsometry;
- varying composition, thickness, and temperature;
- fitted absorption-model parameters.

Full text and point-level spectra were not recovered.

Classification: **blocked**.

## Yue et al. 2012 and 2019

Sources:

- DOI `10.1088/1674-1056/21/1/017804`;
- DOI `10.1088/1674-1056/28/1/017104`.

The 2012 study reports that transmission-derived composition depends on reference temperature in doped HgCdTe and recommends using very low temperature because shallow levels shift the observed edge.

The open 2019 topical review presents absorption and photoluminescence behavior for bulk, LPE, and MBE material near `x≈0.3`, organized by defect state, doping, conductivity type, Fermi level, and temperature. It is strong mechanism evidence that an observed optical edge is not automatically the latent material gap.

Classification:

- 2012: blocked pending full point-level evidence;
- 2019: mechanism-review authority only, not universal static-gap fit authority.

## Figure digitization gate

Seven high-value figures are registered in a digitization manifest, including:

- Chang 2006 Figure 2;
- Moazzami 2005 Figures 4, 6a, 6b, 8, and 9;
- Yue 2019 Figure 4.

No figure is currently authorized for numerical digitization because the exact source page image and axis-calibration record are not archived in the repository. Parsed captions and webpage previews are insufficient for audit-grade point recovery.

## Decision

The modern evidence changes the program state as follows:

- **observation-model research is authorized** because two independent primary studies provide recoverable absorption methodology and figure-level spectra;
- **production observation correction is not authorized** because no machine-readable, uncertainty-bearing common-specimen archive is recovered;
- **static material-gap refitting remains unauthorized** because no modern source supplies independent composition, point uncertainty, and an independent gap series;
- **measurement-class separation remains mandatory**;
- **figure digitization remains blocked** until source images and calibration records are archived.

## Next analytical target

Build a synthetic and formula-level observation-model benchmark that compares:

1. Urbach plus nonparabolic/Kane transition models;
2. the Moazzami fractional-power above-gap law;
3. transmission versus ellipsometry transfer near absorption turn-on;
4. sensitivity of inferred edge energy to carrier filling, defect tails, thickness, and extraction threshold.

This benchmark may use published equations and metadata immediately. It may not claim specimen-level validation until the registered figures or original numerical data are recovered.

## Machine-readable records

- `data/evidence/hgcdte_absorption_observation_source_recovery.csv`
- `data/evidence/hgcdte_absorption_figure_digitization_manifest.csv`
- `tools/audit_absorption_observation_source_recovery.py`
- `tests/test_absorption_observation_source_recovery.py`
