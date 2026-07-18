# Polar electron-phonon vertex decomposition decision

**Date:** 2026-07-18  
**Status:** synthetic Fan-vertex oracle passed

## Problem

The current CdTe PBE point cannot provide a physically consistent long-range polar response, but a replacement cannot be made by simply adding a corrected long-range self-energy to a retained short-range self-energy.

Fan self-energy is quadratic in the complete electron-phonon vertex. If

```text
g = g_SR + g_LR,
```

then

```text
Sigma_Fan[g] = Sigma_SR + Sigma_LR + Sigma_cross,
```

where the cross term contains `g_SR g_LR^dagger + g_LR g_SR^dagger` with the appropriate electronic and phonon denominators. Replacing self-energy components independently would generally lose this interference.

## Established architecture

The method follows the polar interpolation strategy implemented in EPW and derived by Verdi and Giustino, Phys. Rev. Lett. 115, 176401 (2015):

1. evaluate the complete source coarse-grid vertex;
2. evaluate the source long-range vertex in exactly the same conventions;
3. subtract the source long-range term;
4. localize/interpolate the short-range remainder;
5. evaluate the target long-range term in the same electronic gauge;
6. restore the target term at the vertex level;
7. recompute the complete Fan matrix from the restored vertex.

## Synthetic oracle

The oracle uses eight-band Hermitian matrix vertices, an exactly affine short-range component, anisotropic and distinct source/target long-range models, seven training q points, and three unused holdouts.

Evidence:

```text
workflow run: 29650741855
artifact:     8431388959
digest:       sha256:e75b7bb83a88ea06d174b14e45fd492877fca89ba72df1c863156fe3d42eec0d
```

Result:

```text
short-range training error                    = 4.68595e-16
maximum restored-vertex holdout error          = 1.31744e-16
maximum Fan closure error with cross term      = 1.90959e-16
minimum naive-addition error                   = 46.4029%
minimum error from omitting Fan cross term     = 33.9714%
minimum source/target LR model difference      = 34.1410%
```

The oracle therefore distinguishes all three operations:

- **correct:** subtract source LR, interpolate SR, restore target LR, form full Fan matrix;
- **incorrect:** add target LR to the uncorrected source full vertex;
- **incorrect:** add separately calculated SR and LR Fan matrices without their cross term.

## Real-input requirements

A real implementation must bind the following to one convention and provenance record:

- source full coarse-grid electron-phonon vertices;
- source dielectric tensor and Born tensors;
- source phonon frequencies, eigenvectors and q conventions;
- source electronic overlaps and selected-band polar gauge;
- target dielectric and Born tensors;
- target phonon-mode mapping;
- target electronic-energy denominator strategy;
- exact source and target long-range vertex formulas.

The source long-range model must be subtracted using the **source** response parameters. The target model is introduced only after the short-range remainder has been isolated. This is required even when the source response is physically inaccurate; otherwise the source long-range term remains embedded and is double counted.

## Decision

- The Fan vertex subtract/restore architecture is mathematically ready.
- Restoration must occur before Fan self-energy is formed.
- Direct replacement of self-energy components is forbidden.
- The current CdTe PBE vertex is not authorized as a real source input because its long-range response and raw Born neutrality fail.
- No target long-range model has been selected.
- A1 remains unauthorized.

## Remaining controlling blocker: Debye-Waller

The present oracle validates only the first-order electron-phonon vertex and Fan term. Debye-Waller depends on second derivatives or an explicitly justified rigid-ion/commutator reduction and has its own translational-invariance and double-counting requirements.

A real finite-temperature matrix calculation remains blocked until a separate Debye-Waller design:

1. states the exact second-order object;
2. defines any long-range subtraction/restoration;
3. enforces acoustic translational invariance;
4. demonstrates Fan plus Debye-Waller cancellation identities on synthetic truth;
5. preserves the selected-band matrix gauge;
6. rejects execution when the required second-order data are absent.

## Claim boundary

This decision validates method bookkeeping only. It does not establish a physical CdTe/HgCdTe vertex, identify a target dielectric/Born model, validate any scissor or hybrid correction, solve Debye-Waller, or authorize electron-phonon computation.
