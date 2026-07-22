# B0 source findings: QE 7.6 / EPW 6.1 SOC AHC/WFPT

**Date:** 2026-07-22  
**Program:** R02  
**Issue:** #285  
**Status:** restricted go; combined executable proof and minimal export design required

## Executive result

The source audit does not support direct authorization of an R02 material run.

It supports a narrower conclusion:

1. the QE/EPW stack has generic SOC electron–phonon infrastructure;
2. the WFPT/AHC path retains useful complex matrix intermediates;
3. the standard AHC self-energy accumulation collapses those intermediates to real band-diagonal shifts;
4. the upstream test suite exercises SOC and WFPT separately, but no documented regression test combines nonmagnetic SOC with WFPT/AHC;
5. therefore one bounded upstream/synthetic combined-path test and one minimal matrix-export design are mandatory before any CdTe proposal.

## Front-end AHC/SOC guard

The tagged QE 7.6 phonon input path recognizes

```text
electron_phonon = 'ahc'
```

and rejects

```text
elph_ahc AND domag
```

The visible guard does not reject every nonmagnetic

```text
noncolin = true
lspinorb = true
domag = false
```

state.

This proves only that nonmagnetic SOC is not rejected at that front-end condition. It does not prove the spinor dimensions, symmetries, first-order states, WFPT transforms, or AHC accumulation are correct downstream.

## Internal matrix content

`EPW/src/wfpt.f90` contains complex matrix-valued intermediates including objects equivalent to:

```text
dwf17(band, band, mode, k)
sthf17(band, band, mode, k)
dgf17(band, band, mode, k)
dwmatf_trunc(band, band, Cartesian, mode, k)
```

These are sufficient to reject the claim that the implementation is intrinsically scalar at every stage.

The source also distinguishes:

```text
lower Fan electron-phonon vertices
upper Fan / Sternheimer matrices
Debye-Waller matrices
hopping or gauge corrections
```

This internal structure is the main reason the route remains worth auditing.

## Standard self-energy collapse

The standard static AHC accumulators are allocated as

```text
sigma_ahc_uf(band, k, temperature)
sigma_ahc_hdw(band, k, temperature)
```

not as full band-by-band matrices.

The accumulation explicitly selects diagonal elements and takes their real parts. In schematic form:

```text
upper Fan:
  sigma_ahc_uf(n,k,T) += Re[sthmat(n,mode) + sthmat(n,mode)*]

Debye-Waller:
  sigma_ahc_hdw(n,k,T) += Re[dwf17(n,n,mode,k)]
```

The resulting quantities are then added to the usual band-diagonal real self-energy arrays.

Therefore the standard user-facing AHC result does **not** satisfy the complete R02 matrix-self-energy requirement, even though fuller matrix intermediates exist earlier in the path.

## Existing matrix printing is insufficient

EPW's detailed coupling printer can preserve real and imaginary parts of full electron–phonon coupling matrices when requested. That is useful for validating the lower-Fan vertex.

It does not by itself export the accumulated full upper-Fan and Debye–Waller self-energy matrices, preserve all mode-resolved signed contributions, or provide the canonical Kane-gauge transform metadata required by R02.

## Upstream test gap

The QE test suite documents separate categories:

```text
epw_soc   — SOC electron-phonon workflow tests
epw_wfpt  — WFPT/AHC workflow tests
```

No documented test category establishes their intersection:

```text
nonmagnetic SOC + WFPT + AHC
```

The separate existence of `epw_soc` and `epw_wfpt` is not evidence that the combined path works.

QE 7.6 release notes advertise EPW 6.1 and new LSDA support. They do not explicitly advertise or validate noncollinear-SOC WFPT/AHC.

## Consequence for R02

The current B0 classification is:

```text
front-end nonmagnetic-SOC AHC acceptance     plausible
complete downstream SOC correctness         unproven
internal upper-Fan/DW matrices               present
standard full-matrix self-energy output      absent
minimal extractor feasibility                plausible, unproven
combined upstream SOC+WFPT regression        absent
material calculation                         not authorized
```

## Required B0 executable proof

A later separately reviewed implementation PR may execute only an upstream or synthetic small-system test that demonstrates all of:

1. nonmagnetic fully relativistic wavefunctions survive `ph.x` AHC generation;
2. the state passes through `pw2wannier90` and EPW `lwfpt` without spinor truncation;
3. Kramers-related quantities transform consistently under time reversal;
4. lower-Fan, upper-Fan, and Debye–Waller intermediates are finite and reproducible;
5. a full complex matrix can be exported before diagonal reduction;
6. the exported matrix is Hermitian within a predeclared tolerance after the correct on-shell/static reduction;
7. a unitary rotation inside a degenerate subspace produces covariant matrix transformation;
8. the standard diagonal output is recovered from the exported matrix diagonal;
9. no material-specific CdTe response input is consumed.

This test is a software-capability test, not a CdTe scientific result.

## Minimal-export rule

A source change remains admissible only if it is a narrow observational export that:

- does not change the computed intermediates;
- does not change denominators, thresholds, symmetries, interpolation, or accumulation;
- writes full complex matrices with k, q, mode, temperature, gauge, and provenance metadata;
- can be disabled by default;
- has a round-trip and covariance test;
- reproduces the existing diagonal result from its diagonal elements.

If obtaining the matrix requires altering the scientific algorithm, reconstructing omitted off-diagonal terms after diagonal collapse, or maintaining a broad fork, the EPW/WFPT route stops.

## Short-/long-range implication

The full-matrix export must be taken at a stage where the analytic long-range vertex is either explicitly absent or separately labeled. A final matrix assembled after an undocumented polar add-back is inadmissible because the independent generalized-Fröhlich term would then double count the long-range contribution.

The failed CdTe Born tensors remain prohibited regardless of exporter feasibility.

## Updated B0 decision

```text
hybrid architecture                         RESTRICTED GO
QE 7.6 / EPW 6.1 source audit              CONTINUE
standard EPW AHC output for R02             INSUFFICIENT
minimal observational matrix exporter       DESIGN ALLOWED
combined upstream/synthetic SOC+WFPT test    PROPOSAL ALLOWED
CdTe/HgTe/alloy execution                    CLOSED
```

## Stop rule

Terminate the QE/EPW short-range candidate before a material run if either:

- the combined nonmagnetic-SOC WFPT/AHC executable proof fails; or
- the full matrix cannot be exported observationally and covariantly without changing the scientific algorithm.
