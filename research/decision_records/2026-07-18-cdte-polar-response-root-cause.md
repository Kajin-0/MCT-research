# CdTe polar-response root-cause decision

**Date:** 2026-07-18  
**Status:** zero-compute consistency audit completed

## Question

After the stricter response point reduced the raw acoustic and ASR optical diagnostics, can the same PBE/DFPT point support the long-range polar response required by CdTe electron-phonon calculations?

## Inputs

Calculated stricter-response point:

```text
Eg = 0.4973 eV
epsilon_infinity = 62.332890864
TO(simple ASR) = 147.17 cm^-1
|Z*(ASR)| = 3.53169
raw Born sum = -1.25251 e
pressure = 31.20 kbar
```

Bounded room-temperature consistency anchors:

```text
Eg = 1.529 eV
epsilon_infinity = 7.05
TO = 141 cm^-1
LO = 167 cm^-1
```

The phonon anchor is associated with M. Schall, M. Walther and P. U. Jepsen, Phys. Rev. B 64, 094301 (2001), DOI `10.1103/PhysRevB.64.094301`. The dielectric and optical-gap source chain is preserved in `first_principles/a0/cdte_polar_response_consistency_contract.json`.

## Consistency relation

For the two-atom zincblende primitive cell,

```text
omega_LO^2 - omega_TO^2 = e^2 Z*^2 / (epsilon0 epsilon_infinity Omega mu)
```

where `Omega = a^3/4` and `mu` is the Cd-Te reduced mass.

The anchor values imply

```text
|Z*|_anchor = 2.157728341
Z*^2/epsilon_infinity = 0.660395971
```

The stricter-response quantities imply

```text
LO_predicted = 155.194838 cm^-1
Z*^2/epsilon_infinity = 0.200100366
```

## Result

```text
TO relative error = 4.3759%          -> planning gate passes
gap ratio = 0.32525                  -> fails
dielectric ratio = 8.84154           -> fails
LO relative error = 7.0690%          -> fails
polar-strength ratio = 0.30300       -> fails
raw Born sum = -1.25251 e            -> fails
pressure = 31.20 kbar                -> fails reference interpretation
```

The short-range Gamma TO frequency is close enough to the bounded anchor to remain useful for planning. This does not make it a reference phonon because the point is unconverged and highly stressed.

The long-range polar quantities are mutually inconsistent. The current electronic gap is approximately one third of the optical anchor, while the macroscopic electronic dielectric response is approximately `8.84` times the anchor. Even after ASR adjustment of the effective charge, the resulting long-range factor `Z*^2/epsilon_infinity` is only approximately `30.3%` of the anchored value.

The combination is consistent with severe semilocal overscreening, but this single audit does not prove that the band-gap error is the sole cause. Fixed-volume stress, pseudopotential transferability and the DFPT electric-field response remain entangled.

## Quantum ESPRESSO interpretation

The pinned QE source explicitly labels the reported first effective charges as values "without acoustic sum rule applied". It then constructs the displayed ASR-adjusted charges by subtracting the per-cell charge sum divided by the number of atoms. The adjusted `+/-3.53169` values are therefore a translational-sum-rule projection, not independent evidence that the raw Born response is converged.

## Decision

- Preserve the tightened TO result only as a planning-level short-range diagnostic.
- Reject `epsilon_infinity`, raw Born charges, LO response and the present long-range Fröhlich input as physical CdTe references.
- Keep A1 and production polar AHC unauthorized.
- Stop automatic numerical tightening.
- Authorize design, but not execution, of a separately validated short-range/long-range decomposition.

## Requirements for the replacement design

The next design must:

1. define the long-range nonanalytic and Fröhlich terms explicitly in terms of provenance-bound `epsilon_infinity`, `Z*`, phonon frequencies and eigenvectors;
2. keep the short-range matrix response separate from the macroscopic correction;
3. prevent double counting when the long-range contribution is subtracted and restored;
4. state how corrected electronic energies enter Fan denominators and dielectric screening;
5. preserve the fixed selected-band polar gauge and finite-temperature matrix export contract;
6. include a synthetic subtraction/restoration oracle before any real calculation;
7. remain blocked until one independently defensible electronic and polar reference strategy is selected.

## Claim boundary

This decision establishes an internal-consistency failure and a method-design requirement. It does not validate an empirical replacement, endorse a specific hybrid functional or scissor correction, or establish converged CdTe phonons, dielectric tensors, Born charges or electron-phonon self-energies.
