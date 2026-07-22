# Candidate source pin: QE 7.6 / EPW 6.1

**Date:** 2026-07-22  
**Program:** R02  
**Issue:** #285  
**Status:** candidate audit pin only; not an execution authorization

## Candidate release

```text
Quantum ESPRESSO release tag: qe-7.6
GitLab tag commit abbreviation: 9f93ddec
Bundled EPW release: 6.1
Release date: July 2026
```

The full immutable 40-character commit SHA and source-archive digest must be captured in the executable run contract before any build or test. The abbreviated tag commit is sufficient only to identify the current audit target.

## Tagged source paths under audit

```text
PHonon/PH/phq_readin.f90
EPW/src/wfpt.f90
EPW/src/longrange.f90
EPW/src/wan2bloch.f90
EPW/src/wan2bloch_wrap.f90
EPW/src/epw_readin.f90
PW/src/pw2wannier90.f90
```

The audit must cite the `qe-7.6` tag or the resolved full commit. Floating `develop` source is not admissible evidence for a material run.

## Initial tagged-source observation

The tagged `phq_readin.f90` path recognizes

```text
electron_phonon = 'ahc'
```

and applies AHC-specific validation. The visible input guard rejects magnetic `domag` states but does not, in that guard alone, reject every nonmagnetic `noncolin + lspinorb` state.

This is evidence only that the front-end parser does not immediately close the nonmagnetic-SOC path. It is not proof that the complete chain supports spinors:

```text
ph.x perturbation state
-> first-order wavefunctions
-> pw2wannier90 spinor gauge
-> EPW lwfpt interpolation
-> lower Fan / upper Fan / Debye-Waller accumulation
-> matrix export
```

Every stage remains subject to source tracing and a later upstream or synthetic executable test.

## Candidate-release changes relevant to R02

The current EPW release history records:

- EPW 6.1 bundled with the July 2026 QE release;
- WFPT/AHC real-self-energy and bandgap-renormalization capability introduced in the modern EPW line;
- prior spinor/SU(2) handling for SOC workflows;
- prior explicit `longrange` and `shortrange` controls;
- polar interpolation that separates an analytic long-range contribution from the localized Wannier remainder.

These are necessary ingredients, not a validated end-to-end capability claim.

## Fail-closed pin rule

Before any executable B0 test, record all of:

```text
full QE commit SHA
source archive SHA-256
EPW version string
compiler and linked-library versions
build configuration
executable SHA-256
upstream test identifiers
```

A later release, branch head, or locally patched source constitutes a different candidate and requires a new pin record.

## Current decision

```text
qe-7.6 / EPW 6.1 source audit: ACTIVE
qe-7.6 / EPW 6.1 executable validation: NOT YET AUTHORIZED
CdTe material calculation: CLOSED
HgTe and alloy calculations: CLOSED
```
