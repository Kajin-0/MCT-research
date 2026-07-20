# Chang 2004 same-point optical evidence

**Date:** 2026-07-20  
**Issue:** #143  
**Parent program:** #132

## Question

Does Chang et al. 2004 provide a numerical same-specimen calibration between absorption-derived and photoconductive HgCdTe gap observations, or does it provide only observation-model and experimental-feasibility evidence?

## Source identity

```text
Y. Chang et al.
Near-Bandgap Infrared Absorption Properties of HgCdTe
Journal of Electronic Materials 33, 709-713 (2004)
DOI 10.1007/s11664-004-0070-5
source asset SHA-256 de5dba52fa075fe197dbd182c00ef22ee620f0ad571e82e78f6b2a2698181424
```

The copyrighted source file and page images are not committed.

## Exact admissible observations

Table I reports the fitted Urbach-width decomposition

```text
W(T) = A + B coth(hbar omega_LO / 2 k T)
```

with:

```text
x approximately 0.40   A = 0.0190 +/- 0.0002 eV   B = 0.0012  +/- 0.0001  eV
x approximately 0.30   A = 0.0112 +/- 0.0003 eV   B = 0.0008  +/- 0.0001  eV
x approximately 0.21   A = 0.0124 +/- 0.0005 eV   B = 0.00067 +/- 0.00027 eV
```

The six values are exact table transcriptions. `A` is preserved as the static-disorder contribution and `B` as the dynamic electron-phonon contribution. They are observation-model parameters, not material-gap points.

The source prints the three compositions approximately and does not report specimen-level composition uncertainty or a recoverable independent composition method. The evidence package therefore records `composition_sigma = null`; no uncertainty is invented.

## Same-point pairing

The experimental method states that transmissivity and photoconductivity were measured simultaneously at the same sample point. Figure 1 shows absorption-coefficient and photoconductive quantum-efficiency curves at 77 K and 293 K.

The publication does not provide the information needed for a numerical method-offset estimate:

- the Figure 1 specimen composition is not identified;
- no paired numerical gap or edge table is reported;
- a complete photoconductive edge-extraction operator is not specified;
- specimen-level composition uncertainty is absent;
- the plotted curves alone do not identify one latent gap.

The pairing is therefore encoded as nonnumeric source metadata:

```text
same_point_pairing_documented              true
simultaneous_measurement_documented        true
paired_temperatures_K                      [77, 293]
specimen_composition_identified            false
numerical_paired_gap_table_reported        false
photoconductive_edge_operator_complete     false
paired_numeric_method_offset_identified    false
```

## Decision

### Authorized

- preserve the six exact Urbach `A` and `B` parameters as separate observation classes;
- use the source as evidence that same-point absorption and photoconductive measurement is experimentally feasible;
- use the source to motivate explicit tail treatment in absorption-edge inference;
- prioritize recovery of raw spectra, specimen mapping, laboratory records, theses, or workshop precursors from this lineage.

### Unauthorized

- treat `A` or `B` as a band-gap observation;
- digitize Figure 1 into a numerical absorption-photoconductive gap offset;
- pool absorption and photoconductive observations as interchangeable;
- infer a universal tail correction, source correction, or replacement gap law;
- assign a composition uncertainty not reported by the source.

## Program consequence

Chang 2004 is the strongest recovered source demonstrating same-point dual-modality optical measurement, but it does not by itself identify the observation-class offset required by the paired acquisition model. The controlling static-law reopening gate remains closed.

The next high-value acquisition from this lineage is native numerical data with:

1. specimen identity and independently measured composition with uncertainty;
2. raw absorption and photoconductive spectra from the same registered area;
3. temperature calibration;
4. explicit edge operators and fit covariance;
5. carrier-density and processing metadata.

No update to `research/active_progress.md` is required because the authorization boundary is unchanged: observation-model evidence expands, while numerical paired-offset and universal-law inference remain blocked.
