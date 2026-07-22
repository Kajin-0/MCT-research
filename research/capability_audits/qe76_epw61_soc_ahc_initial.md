# Initial capability audit: QE 7.6 / EPW 6.1 for R02 short-range SOC AHC

**Date:** 2026-07-22  
**Program:** R02  
**Issue:** #285  
**Status:** source-grounded initial matrix; no material calculation authorized

## Scope

This audit asks whether Quantum ESPRESSO 7.6 / EPW 6.1 can produce the short-range, symmetry-resolved electron–phonon information required by R02 without reusing the failed CdTe Born-charge response.

It is not a numerical validation of CdTe. It identifies what is supported, what appears possible only from internal arrays, and what still requires an executable or source-level proof.

## Capability matrix

| Requirement | Initial status | Evidence and interpretation |
|---|---|---|
| Current maintained release | supported | QE 7.6 was released in July 2026 and includes EPW 6.1. |
| Nonmagnetic fully relativistic ground state | supported | QE supports fully relativistic noncollinear/SOC calculations with suitable pseudopotentials. |
| Generic EPW spinor workflow | supported in code family | EPW release history and source contain spinor/SU(2) handling. This does not yet prove the complete WFPT AHC path. |
| `ph.x` AHC with nonmagnetic SOC | uncertain, promising | Current `phq_readin.f90` rejects AHC with `domag`; it does not visibly reject all nonmagnetic `noncolin+lspinorb` states in the same guard. A complete call-path audit is still required. |
| ABINIT EPH with SOC | unsupported | Current ABINIT EPH documentation explicitly lists spin–orbit coupling and noncollinear magnetism as unsupported. |
| Lower Fan contribution | implemented internally | EPW AHC/WFPT source distinguishes the lower-Fan part from the static upper-Fan/Debye–Waller part. User-facing export remains to be proven. |
| Upper Fan contribution | implemented internally | `wfpt.f90` contains Sternheimer/upper-Fan matrices and static AHC accumulation. |
| Debye–Waller contribution | implemented internally | `wfpt.f90` contains complex Debye–Waller matrices and separate self-energy arrays. |
| Complete complex band matrices | internal representation supported | Internal arrays are matrix-valued in band indices. A stable external export in the required gauge is not yet established. |
| Final user-facing full-matrix self-energy | uncertain | Standard documented outputs emphasize band-diagonal self-energies. A repository patch or dedicated extractor may be required. |
| Mode-resolved coupling | partially supported | `prtgkk` and verbose outputs expose mode-resolved coupling information, but documented output is often magnitudes or diagonal linewidth contributions rather than signed complex self-energy matrices. |
| Signed mode-resolved real self-energy | uncertain | Must be demonstrated from WFPT arrays or a minimal source patch before any material run. |
| Polar Wannier interpolation | supported | `lpolar=.true.` subtracts the analytic long-range contribution before interpolation and adds it back afterward. |
| Explicit long-range/short-range controls | present | EPW source/input contains `longrange` and `shortrange` controls in addition to `lpolar`. Exact behavior in the WFPT AHC path must be verified. |
| Long-range term without CdTe BECs | not established inside EPW | The safe baseline is repository-side generalized-Fröhlich post-processing using independent inputs. Direct injection of external tensors into EPW is not assumed. |
| Generalized-Fröhlich correction | established theory | ABINIT implements a generalized-Fröhlich ZPR task, and Miglio et al. validate the nonadiabatic model across infrared-active materials. R02 requires an independent implementation and benchmark. |
| Fixed smooth gauge | supported in principle | Wannier interpolation supplies a smooth gauge; R02 already has canonical Gamma-basis alignment machinery. The round trip between gauges remains to be tested. |
| Canonical eight-band projection | repository capability exists | The repo has completed Gamma double-group alignment and invariant projection infrastructure. It has not yet consumed an EPW WFPT matrix export. |
| Special-displacement total shift | supported as cross-check | EPW/ZG can provide finite-temperature displaced-supercell band structures. It does not replace explicit Fan/Debye–Waller matrix decomposition. |

## Source observations

### ABINIT

The current ABINIT EPH documentation states that the EPH code can compute electron self-energies with Fan–Migdal and Debye–Waller terms and can estimate polar ZPR corrections through a generalized Fröhlich model.

The same documentation states that EPH does not support:

```text
spin-orbit coupling
non-collinear magnetism / nspinor = 2
```

This is a hard incompatibility with the HgCdTe endpoint problem. ABINIT is therefore excluded as the primary computational backend unless that limitation changes in a future pinned release and is independently verified.

### QE/EPW AHC/WFPT

The EPW Wannier-function perturbation-theory implementation contains matrix-valued objects for:

```text
lower Fan electron-phonon vertices
upper Fan / Sternheimer contribution
Debye-Waller contribution
hopping/gauge corrections
```

The source-level design is closer to the R02 information target than the traditional EPW band-diagonal Fan-only path.

The critical uncertainty is not whether matrices exist internally. It is whether they can be exported and interpreted reproducibly under nonmagnetic SOC without a bespoke invasive code fork.

### SOC guard

Current QE source includes an AHC guard against `domag`, i.e. magnetic states. A separate historical guard disables an electron–phonon coefficient path for magnetic spin-orbit cases.

This suggests, but does not prove, that a nonmagnetic time-reversal-invariant SOC AHC state may be accepted. The audit must trace all downstream routines for assumptions about real wavefunctions, scalar bands, Kramers pairs, and spinor dimensions.

### Long-range separation

EPW's polar interpolation strategy is conceptually compatible with R02's decomposition: subtract the analytic long-range piece, interpolate the localized short-range remainder, and add the long-range piece back.

R02 cannot use that mechanism blindly because the analytic piece normally depends on dielectric and Born-charge inputs. The current CdTe response tensors failed raw neutrality and are prohibited.

The preferred implementation is therefore:

```text
EPW/WFPT output: short-range matrix object only
repository post-processing: independent generalized-Frohlich matrix correction
```

No claim is made yet that the existing flags emit exactly that object in the AHC path.

## Required source proofs

Before proposing a material run, B0 must identify exact source locations and produce a call graph for:

1. `electron_phonon='ahc'` parsing and guards in `ph.x`;
2. spinor dimensions through first-order wavefunctions;
3. `pw2wannier90` spinor gauge transfer;
4. EPW `lwfpt` matrix allocation and interpolation;
5. lower-Fan self-energy accumulation;
6. upper-Fan and Debye–Waller accumulation;
7. long-range subtraction/addition;
8. full-matrix output or the smallest required output patch;
9. mode and q-point decomposition;
10. temperature and zero-point separation.

Each proof must be attached to a pinned QE/EPW commit, not a floating `develop` branch.

## Minimal executable tests permitted after source review

No CdTe test is authorized by this file. If source review passes, the next issue may propose only:

1. an existing upstream nonpolar WFPT/AHC test reproduced byte-for-byte or tolerance-for-tolerance;
2. a nonmagnetic SOC compile/path test using an upstream or synthetic trivial system;
3. a matrix export round trip on test data;
4. a long-range-disabled versus long-range-only bookkeeping test using a published polar tutorial system.

These tests must not alter or rerun the terminated CdTe response state.

## Proposed short-range export schema

The immutable short-range object should contain one record per temperature, k point, q point or accumulated q set, and Kane-subspace matrix block:

```text
schema_version
backend, release, commit, build hash
pseudopotential hashes
ground-state hash
phonon/WFPT state hash
volume and lattice convention
k, q, mode, frequency
source gauge identifier
canonical-gauge transform identifier
Sigma_lower_Fan complex matrix
Sigma_upper_Fan complex matrix
Sigma_DW complex matrix
zero-point / thermal selector
broadening and denominator convention
long_range_included = false
units
convergence and resource metadata
```

A final scalar band shift without these provenance and decomposition fields does not satisfy the R02 target.

## Proposed generalized-Fröhlich input schema

```text
schema_version
material, phase, composition
reference volume and temperature
epsilon_infinity tensor + uncertainty
epsilon_static tensor or mode dielectric strengths + uncertainty
LO frequencies + uncertainty
mode eigenvector/branch provenance
effective-mass tensors for Gamma6/Gamma8/Gamma7 + uncertainty
degeneracy and symmetry representation
nonadiabatic denominator convention
integration/cutoff convention
source citations and file hashes
```

The output must preserve separate edge corrections and covariance:

```text
Sigma_LR_Gamma6(T)
Sigma_LR_Gamma8(T)
Sigma_LR_Gamma7(T)
Cov[Gamma6, Gamma8, Gamma7]
```

## No-double-counting test

The combined implementation must pass a synthetic closure test:

```text
full vertex = declared short-range vertex + declared long-range vertex
```

with the same analytic long-range term used on both sides. The test must fail if the long-range contribution is present twice or omitted.

For a real calculation, the metadata must state exactly which component was removed from the first-principles matrix before interpolation or accumulation.

## Initial decision

```text
ABINIT primary path: STOP
QE 7.6 / EPW 6.1 full R02 production: NOT AUTHORIZED
QE 7.6 / EPW 6.1 B0 source audit: GO
hybrid short-range + generalized-Frohlich architecture: RESTRICTED GO
special displacement as total-shift cross-check: DEFERRED
CdTe/HgTe/alloy material computation: CLOSED
```

## Primary references

- ABINIT EPH introduction: https://docs.abinit.org/tutorial/eph_intro/
- ABINIT ZPR tutorial: https://docs.abinit.org/tutorial/eph4zpr/
- ABINIT EPH variables: https://docs.abinit.org/variables/eph/
- QE releases: https://gitlab.com/QEF/q-e/-/releases
- EPW releases: https://docs.epw-code.org/Releases.html
- EPW theory: https://docs.epw-code.org/Theory.html
- EPW inputs: https://docs.epw-code.org/Inputs/Inputs.html
- EPW WFPT source: https://gitlab.com/QEF/q-e/-/blob/develop/EPW/src/wfpt.f90
- QE phonon input guards: https://gitlab.com/QEF/q-e/-/blob/develop/PHonon/PH/phq_readin.f90
- Miglio et al., nonadiabatic generalized-Fröhlich ZPR: https://doi.org/10.1038/s41524-020-00434-z
- Nery and Allen, polar correction: https://arxiv.org/abs/1603.04269
- Zacharias and Giustino, special displacement: https://doi.org/10.1103/PhysRevResearch.2.013357
