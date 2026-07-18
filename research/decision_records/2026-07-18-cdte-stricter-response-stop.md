# CdTe stricter-response diagnostic: stop numerical tightening

**Date:** 2026-07-18  
**Scope:** one same-geometry response diagnostic authorized after the first CdTe A0 physical audit failed.

## Controlled change

Only two numerical controls changed relative to the first A0 point:

```text
ecutrho: 456 -> 570 Ry
PH tr2_ph: 1e-10 -> 1e-14
```

The lattice, `ecutwfc`, k grid, band count, SCF threshold, pseudopotential bytes, Quantum ESPRESSO source, PBE functional, SOC setup and Gamma response target remained fixed.

## Evidence

```text
workflow run: 29642078177
artifact:     8429313337
digest:       sha256:9d179462706990c94376cff2499a42bb89af27d297afe1f514e8da9ff171c227
head:         2121442f648c2c66b14cf12196bdb9478ef68aad
```

The SCF completed in `1:11.95`; the Gamma PH response completed in `43:11.28`.

## Result

| Diagnostic | Baseline | Stricter point | Ratio |
|---|---:|---:|---:|
| Maximum raw acoustic magnitude | 183.63 cm^-1 | 20.55 cm^-1 | 0.11191 |
| ASR optical relative shift | 26.9853% | 0.94898% | 0.03517 |
| Absolute Born-charge sum | 0.51611 e | 1.25251 e | 2.42683 |

The raw optical triplet changed from `223.27 cm^-1` to `148.58 cm^-1`; the simple-ASR optical triplet changed from `283.52 cm^-1` to `147.17 cm^-1`. The dielectric tensor remained cubic and nearly unchanged. The static pressure remained `31.20 kbar`.

The raw output confirms that the Born-charge result is not a parser artifact:

```text
baseline: Cd +3.60434, Te -4.12045, sum -0.51611
stricter: Cd +2.90543, Te -4.15794, sum -1.25251
```

## Decision

The acoustic and ASR diagnostics materially collapsed, but the Born-charge neutrality error worsened by a factor of approximately `2.43`. Therefore the declared all-three collapse gate fails.

- A1 electron-phonon work remains unauthorized.
- No additional cutoff, threshold, k-grid, volume, functional, pseudopotential, HgTe or alloy calculation is automatically authorized.
- Numerical tightening stops here.
- The next task is an analytical root-cause review of the fixed-volume stress, pseudopotential/DFPT response formulation, and the meaning of the unconstrained raw effective charges.

## Interpretation boundary

This comparison shows that the initial large acoustic and ASR violations were strongly numerical, but it does not validate the resulting optical frequency because the raw Born-charge sum remains severely non-neutral and the fixed cell remains under approximately `3.12 GPa` pressure. Neither point is a physical CdTe reference.
