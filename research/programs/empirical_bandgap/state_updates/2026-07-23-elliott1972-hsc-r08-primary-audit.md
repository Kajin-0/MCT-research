# R01 state addendum: Elliott et al. 1972 HSC_R08 primary-source audit

**Date:** 2026-07-23  
**Program:** R01 - empirical bandgap reconstruction  
**Issue:** #336  
**Hansen graph identity:** HSC_R08

## Primary-source result

The complete Elliott et al. article was recovered and audited. Its primary measurement class is hydrostatic-pressure magnetotransport, not magneto-optics.

```text
source PDF SHA256
509bbcfd3c4b72312ab49ee2460e56561a9324e4e96af56dd29e8612b0b2b328

article pages
2985-2997
```

The source binary is not committed.

## Reconstructed evidence

```text
named sample identities                      3
physical specimen count lower bound          4
Table I carrier rows                         11
Table II gap/Fermi rows                       5
source-native 7B temperature pairings         2
figure digitization                           none
```

The named identities are 7B, 7B1, and 8B at `x=0.149`, `0.149`, and `0.138`, each with source-reported electron-microprobe accuracy `+/-0.005`.

## Measurement and model boundary

The signed zero-pressure gaps in Table II are Kane-model outputs inferred from pressure-dependent carrier concentrations. They are not direct optical gaps.

```text
dEg/dP = 7.0e-6 eV/bar
```

The 77 K 7B result has two alternatives because the source evaluates heavy-hole masses `0.3 m0` and `0.7 m0`.

## Hansen result

Hansen's generic `magneto_optical_gap` source classification is corrected to pressure-dependent magnetotransport. Source-native candidate points are now explicit, but Hansen does not identify its HSC_R08 markers or the selected 77 K heavy-hole-mass branch.

```text
controlling decision
primary_source_recovered_source_native_gap_candidates_reconstructed_hansen_marker_mapping_unresolved
```

## Authorization state

```text
primary source identity and hash                 validated
measurement-class correction                    validated
Table I and Table II transcription               validated
source-native Hansen candidates                  validated
pointwise covariance                             not authorized
figure-curve digitization                        not authorized
exact Hansen marker mapping                      unresolved
independent Hansen validation                    not authorized
production equation or manuscript claim          not authorized
```
