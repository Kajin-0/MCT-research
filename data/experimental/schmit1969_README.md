# Schmit and Stelzer 1969 detector-cutoff reconstruction

## Primary source

```text
J. L. Schmit and E. L. Stelzer
Temperature and Alloy Compositional Dependences of the Energy Gap of Hg1-xCdxTe
Journal of Applied Physics 40, 4865-4869 (1969)
DOI: 10.1063/1.1657304
File Library asset: schmit1969.pdf
```

The source PDF is available in the user File Library but is not materialized as repository binary content. Its SHA256 is therefore unavailable and is not fabricated.

Canonical source files are:

```text
data/experimental/schmit1969_source_metadata.csv
data/experimental/schmit1969_specimens.csv
data/experimental/schmit1969_table3_cutoff_observations.csv
data/experimental/schmit1969_README.md
```

## Reconstructed source content

Table III contains 56 printed observations from eight detectors over approximately `20-300 K`. The repository retains the source table order and assigns stable internal specimen IDs `SS69_S01` through `SS69_S08` because Table III does not print historical sample names.

| Specimen | Nominal x | Printed limit | Fit-adjusted x | Rows |
|---|---:|---:|---:|---:|
| SS69_S01 | 0.600 | 0.030 | 0.599 | 4 |
| SS69_S02 | 0.580 | 0.050 | 0.572 | 6 |
| SS69_S03 | 0.325 | 0.010 | 0.329 | 8 |
| SS69_S04 | 0.266 | 0.003 | 0.262 | 6 |
| SS69_S05 | 0.217 | 0.006 | 0.223 | 8 |
| SS69_S06 | 0.195 | 0.006 | 0.201 | 6 |
| SS69_S07 | 0.180 | 0.006 | 0.183 | 10 |
| SS69_S08 | 0.170 | 0.006 | 0.174 | 8 |

## Measured and adjusted composition are distinct

The source determined absolute composition and uniformity using density measurements and electron-beam microprobe measurements. Microprobe standards were measured by density, and the paper gives the microprobe limit as approximately

```text
+/- 0.006 mole fraction.
```

The nominal compositions and their printed limits are source composition measurements.

The adjusted compositions were selected during construction of the source empirical relation. The paper states that the adjustments were typically within the limits of composition determination, but the adjusted values are still fit-dependent quantities rather than new independent measurements.

The repository therefore records

```text
adjusted_x_status = source_fit_adjusted_composition
adjusted_x_is_independently_measured = false
adjusted_x_is_eligible_for_held_out_composition_validation = false
```

A comparison that evaluates a model at adjusted `x` is partly conditioned on the original source fit and cannot be described as a clean composition holdout.

## Detector-type knowledge boundary

The source explicitly identifies:

```text
adjusted x = 0.572   photovoltaic detector
adjusted x = 0.329   photoconductive detector
```

The detector type of the other six specimens is not assigned by inference in this reconstruction.

## Operational observable

The experiment measured relative detector spectral response. The cutoff wavelength was defined at the half-peak response value and was generally about ten percent longer than the response-peak wavelength.

The stored measurement class is

```text
detector_half_peak_spectral_response_cutoff
```

and the stored energy field is

```text
cutoff_energy_ev.
```

The energy values are the source's conversion of the printed half-peak cutoff wavelengths. They remain operational detector cutoffs and are marked

```text
signed_gap_eligible = false
intrinsic_gap_eligible_without_observation_operator = false
energy_origin = source_converted_from_half_peak_cutoff_wavelength
```

The source's approximate ten-percent cutoff-versus-peak statement is contextual. It is not promoted to a universal correction from detector response to an intrinsic or signed gap.

The printed energy values are retained exactly. A numerical consistency test verifies that they agree with `1.23984/lambda_um` within the rounding of the printed table, but the calculated values do not replace the source column.

## Temperature and precision semantics

The source distinguishes temperature-control stability from absolute temperature accuracy:

```text
short-term control stability: approximately +/- 0.5 K
absolute temperature determination: believed better than 10 K
```

These are not interchangeable. Neither statement is converted to a pointwise Gaussian standard deviation.

The source states that the precision of cutoff wavelength and therefore the converted cutoff energy is better than one percent of the listed value. This is stored as a source-level precision statement, not as 56 independent one-sigma errors.

No pointwise covariance matrix is reported.

## Material and detector preparation

The HgCdTe was grown by the modified Bridgman technique. Detectors were mounted on germanium substrates with epoxy, lapped and etched to the desired thickness, and given indium contacts by evaporation or soldering.

Most detectors were fabricated at the Honeywell Radiation Center. The explicitly identified photovoltaic `x=0.572` and photoconductive `x=0.329` detectors were fabricated at the Honeywell Corporate Research Center.

## Temperature and optical apparatus

The flexible temperature-control method used an Air Products AC3L-110 open-cycle Joule-Thomson Cryotip with approximate capability

```text
4.2-300 K.
```

Gold-cobalt and gold-iron versus copper thermocouples were used, with the former mounted on the detector.

Relative response measurements used:

```text
Perkin-Elmer Model 98 single-pass monochromator
chopped globar radiation source
source-region-dependent prisms, mirrors, and windows
thermocouple response reference calibrated by the Naval Weapons Center
monochromator slit widths from 0.1 to 2.0 mm
spectral slit width generally below 0.05 of cutoff wavelength
incident power below 1.0 mW
```

Figure 1 contains representative response curves, but it is not digitized in this tranche because the complete numerical cutoff table is printed.

## Historical source equation

Schmit and Stelzer reported

```text
E_cutoff(eV) = 1.59*x - 0.25
             + 5.233e-4*T*(1 - 2.08*x)
             + 0.327*x^3
```

using the fit-adjusted compositions.

The source states that the relation is best for approximately

```text
0.17 < x < 0.33
T > 77 K
```

and is less strongly supported outside that region. The `x=0.262` detector was weighted more heavily because of composition uniformity and the accuracy of its density-based composition determination.

The cubic term was introduced to fit CdTe endpoint data. The equation is stored as historical fit metadata only. No samples from it are committed as observations, and the coefficients are not refitted in this tranche.

## Hansen lineage

Schmit and Stelzer 1969 is Hansen source `HSC_R01` and contributed fitted detector-cutoff data to the later Hansen reconstruction. It cannot independently validate Hansen.

Hansen later excluded the four lowest-composition Schmit/Stelzer specimens because of mercury inclusions. The repository records this as

```text
hansen_downstream_selection_status = excluded_by_Hansen_downstream
hansen_downstream_exclusion_reason = mercury_inclusions
```

for `SS69_S05` through `SS69_S08`.

This is downstream selection provenance. It does not delete the printed Table III observations or silently convert the Hansen rule into a Schmit source quality flag.

## Scientific boundary

This reconstruction supports:

- exact preservation of the eight-specimen, 56-row detector-cutoff table;
- specimen-preserving thermal-shape analyses under the operational cutoff definition;
- audit of measured versus source-adjusted composition;
- reconstruction of Hansen's source lineage and selection rules;
- later observation-operator studies.

It does not support:

- treating the cutoff energies as signed `Gamma6-Gamma8` gaps;
- treating adjusted compositions as independent measurements;
- independent validation of Hansen;
- a universal cutoff-to-intrinsic-gap correction;
- deleting the four Hansen-excluded specimens from the primary-source archive;
- sampling the source equation and labeling those samples as data;
- production-equation, manuscript, or submission authorization.
