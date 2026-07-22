# Ariel et al. 1996 same-wafer uniformity abstract audit

**Program:** R04 measurement-kernel-aware spatial disorder  
**Issue:** #302  
**Source:** V. Ariel, V. Garber, G. Bahir, S. Krishnamurthy, and A. Sher, *Monitoring HgCdTe Layer Uniformity by the Differential Absorption Technique*, Applied Physics Letters 69(13), 1864-1866 (1996)  
**Record status:** accessible abstract and bibliographic records audited; full text not retrieved  
**DOI status:** unresolved from an authoritative accessible record; intentionally not guessed

## Source-bounded result

The accessible abstract reports a room-temperature differential-absorption procedure applied at different points on the same HgCdTe wafer. This is the strongest audited evidence so far that the Ariel derivative method was extended from a specimen-level depth-grading estimator to a same-wafer spatial sampling procedure.

Its deterministic R04 qualification is:

```text
spatial_observation_method_context
```

It is not a calibrated spatial map, a multiresolution benchmark, or direct external validation.

## Reported observation chain

```text
room-temperature wafer transmission
-> filtering of interference fringes and high-frequency noise
-> thickness estimation from the fringe spectrum
-> absorption coefficient extraction
-> first and second derivatives with respect to photon energy
-> approximate band-gap estimate from derivative extrema
-> repetition at different points on the same wafer
```

The abstract states that the repeated-point procedure can determine lateral and transverse band-gap fluctuations. The accessible record does not expose the numerical decomposition, point coordinates, or depth model needed to reproduce that separation.

## Abstract-level numerical records

```text
minimum layer thickness with reliable transmission     8 micrometres
reported thickness accuracy                            approximately +/-0.1 micrometre
reported differential-absorption accuracy              approximately +/-0.5 meV
reported lateral effective scales                      1
```

The accuracy values are method-level statements. They are not repeat covariance, pointwise uncertainty arrays, or evidence of independent spatial samples.

## What is confirmed

- one HgCdTe wafer is measured at different points;
- the observable is room-temperature optical transmission processed through differential absorption;
- interference fringes and high-frequency noise are filtered;
- fringe spectra are used for thickness estimation;
- lateral and transverse fluctuation recovery is an explicit method objective;
- the method is described as simple, nondestructive, and room-temperature compatible.

## What remains unresolved

The accessible abstract and bibliographic records do not provide:

- an authoritative DOI record;
- full article text;
- specimen identifiers or number of wafers;
- number of measured positions;
- point spacing or physical coordinates;
- acquisition order;
- aperture, numerical aperture, beam diameter, or PSF;
- a raster or map geometry;
- original transmission, absorption, or derivative arrays;
- repeated measurements at one point;
- observation covariance;
- multiple effective lateral kernels;
- the numerical rule separating lateral from transverse fluctuations.

Unknown metadata is retained as unknown or not retrieved. It is not filled by assumption.

## R04 interpretation

Different positions on the same wafer establish spatial sampling intent and same-specimen context. They do not establish:

```text
registered raster
independent pixel count
known sampling kernel
probe-scale sweep
covariance-family closure
```

One optical configuration remains one effective lateral scale unless the full source reports multiple independently characterized kernels.

The reported approximately +/-0.5 meV accuracy cannot be inserted directly as diagonal observation covariance. A usable uncertainty model would require the definition of that accuracy, repeats, preprocessing sensitivity, position dependence, and shared calibration errors.

## Relation to Ariel 1995

Ariel et al. 1995 provides the explicit depth-averaged derivative-absorption observation model and its linear-grading limitations. Ariel et al. 1996 states that the method is repeated at different wafer points and used to address lateral and transverse fluctuations.

Together, the sources motivate a future joint observation model, but the abstract alone does not provide the arrays or metadata required to fit it.

## Price and Boyd review status

Price and Boyd, DOI `10.1088/0268-1242/8/6S/006`, is bibliographically verified as a review of FTIR, EDX, optical reflectance, and other HgCdTe composition methods. Its full text was not retrieved through the accessible public record in this tranche. No spatial-resolution or aperture claim is imported from its abstract.

## Minimum upgrade

A quantitative upgrade requires:

1. authoritative full text and DOI metadata;
2. original transmission, absorption, and derivative arrays;
3. point coordinates, count, spacing, and acquisition order;
4. aperture and measured or reconstructable PSF;
5. repeat uncertainty or observation covariance;
6. exact filtering and derivative parameters;
7. numerical lateral/transverse separation rule;
8. specimen thickness and interface-profile metadata;
9. at least two additional calibrated effective scales, or one reusable high-resolution numerical map.

## Claim boundary

This audit does not infer a wafer covariance, correlation length, covariance family, point variance, independent sample count, or detector performance. It does not convert method accuracy into covariance and does not authorize a novelty or manuscript claim.
