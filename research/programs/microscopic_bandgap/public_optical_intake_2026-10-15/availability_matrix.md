# Ranked specimen/source availability

Checked 2026-10-15. **YES** means the actual accessible item satisfies the
column, not that a paper implies it was once acquired. **U** means unknown or
unqualified. **NO** in the last column means no complete package was located
and admitted, not nonexistence. Confidence refers to the evidence classification,
not a probability of data survival. Ranking is information gain/access route,
not closeness of a fitted gap to a preferred answer.

| Rank / candidate | Public article/SI | Public raw same-specimen ≥3-field line profiles | Acquired polarization + calibration | Signal/reference/dark, energy/B/T/window/background error records | Independent assay + spatial/footprint errors | Complete public package? / confidence |
|---|---|---|---|---|---|---|
| 1. Teppe2016 A, lowest-temperature series | YES [T1,T2] | NO located; published maps/fit summaries only | U | U | U; nominal A labels differ in precision | **NO / high** for publisher/local rejection; retention U |
| 2. Orlita2014 graded near-critical layer | YES preview/author text/SI [O1–O3] | NO located; figure traces/maps only | U; theoretical circular channels insufficient | U | U; growth profile is not a calibrated uncertainty/assay bundle | **NO / high** for publisher/local rejection; retention U |
| 3. Teppe2016 B, low-temperature series | YES [T1,T2] | NO located | U | U | U | **NO / high**; no better raw-access route than A |
| 4. Guldner1977 II Fig.8–10 specimens | Inherited primary audit [G1] | NO located in accepted archive | Published polarization evidence; raw calibration U | U | Article-level density/microprobe; per-specimen errors U | **NO / moderate**, inherited audit; no fresh full-text retrieval claimed |
| 5. Weiler1977 series | Inherited primary audit [W1] | NO located | Published circular reflectance evidence; raw channels U | U | Inherited audit records substantial inhomogeneity/errors | **NO / moderate**; warmer series, not best low-T candidate |
| Exclude. Teppe S5 A/B 77 K waterfall | YES [T2], p4 | NO: a PDF plot, not raw numerical scans | U | U | U | **NO / high**; useful line-family map, not requested raw low-T object |
| Unresolved. HAL article records | Indexed article records [H1–H3] | U: landing/API file inventories inaccessible | U | U | U | **NO admission / limited access**; do not assert repository is empty |
| Exclude. Public HgTe transport repositories | YES metadata [X1,X2] | NO for this optical observable | Not applicable | Not applicable | Not applicable | **NO / high** wrong measurement/device |
| Exclude. Public polarized Nd-gallate spectra | YES metadata [X3] | Numerical optical data described, but wrong material | Not HgCdTe | Not qualifying HgCdTe records | Not applicable | **NO / high** wrong material; no download/analysis |

Source IDs resolve to direct URLs/locations in [sources.json](sources.json).
For historical Guldner/Weiler details see the unchanged
[Stage0 matrix](../evidence_acquisition_2026-10-11/stage0_availability_matrix.md).

Published context, **not independently accepted metrology**: Teppe A/B are
approximately 3.2 µm MBE layers; A is labelled x=0.175 (Methods 0.17), B=0.155.
Their low-temperature field maps are at 2 K, in a setup reaching 16 T; the
reported resolution is 0.5 meV and spectra are normalized to B=0. S5 instead
plots both specimens at 77 K. No specimen-resolved assay interval follows from
those nominal labels. The Orlita layer has a graded profile and an approximately
3.2 µm plateau near nominal x=0.17; its Methods specify a 1.8 K bolometer,
not a complete specimen-temperature calibration record. These published
conditions motivate the ranking, not a certification of the requested errors.

## Specimen/state cautions that remain decision-relevant

Teppe's A is the first request target because the article identifies a cryogenic
near-critical HH family and a correspondence route. Growth monitoring does not
by itself establish an independently calibrated Cd assay; no optical-fit-derived
x is accepted. No cross-paper identity of the Orlita and Teppe specimens is
asserted. Layer thickness/buffer relaxation does not establish negligible
residual strain or composition grading. Full specimen-temperature, carrier/Pauli
and footprint bounds remain U even where a nominal temperature is printed.
Teppe's Hall-density figure is useful context but does not supply original
Hall traces with a complete carrier-error budget linked to each optical scan.

Orlita's primary methods describe normalized transmission and residual-carrier
blocking. Thus transmission minima cannot simply be substituted for the p_z=0
Kane transition center. The relevant [author text](https://arxiv.org/html/1310.0969)
also explains asymmetric Landau-band line shapes. The optical forward adapter
and bounded tails are indispensable even if raw records are later obtained.

## Local records deliberately rejected as raw

The manifest classifies the existing experimental/validation CSVs, calculated
distributional screen and paper library. Explicit fitted gaps, figure annotations,
nominal composition, velocity summaries and publisher PDFs are **not** raw
independently assayed line profiles. No new digitization was attempted. No
calibration, channel or assay error was set to zero because it is unreported.
