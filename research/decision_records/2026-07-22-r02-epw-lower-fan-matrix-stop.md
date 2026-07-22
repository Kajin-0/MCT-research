# Decision record: stop the QE 7.6 / EPW 6.1 observational full-matrix exporter path

**Date:** 2026-07-22  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #289  
**Parent:** #285  
**Status:** mandatory source-level gate failed before build

## Decision

Stop the proposed QE 7.6 / EPW 6.1 **observational full-matrix exporter** path before compiling or executing the combined SOC + WFPT fixture.

The reason is specific and predeclared: the standard lower-Fan path does not already compute a complete complex matrix that an exporter can merely observe. It contracts the complex electron--phonon vertex to a scalar modulus squared for one external band and accumulates a band-diagonal self-energy.

Creating the missing off-diagonal products would be a new scientific contraction algorithm, not an observational exporter. Issue #289 explicitly requires termination in that case.

## Pinned source state

The GitHub mirror tag `qe-7.6` resolves to:

```text
9f93ddec427d2b9a45bb72d828c6d324f62fcabd
```

Audited source blobs:

```text
EPW/src/selfen.f90
be4858854d1ab26d27b3acf52a9a30c21fa8b472

EPW/src/wfpt.f90
526405829090c4214eb87cff2af90bbd257efe3d
```

Candidate upstream nonpolar fixture assets were also identified:

```text
test-suite/ph_ahc_diam/diam.scf.in
5a895aacee9a0559de4c071be08c1fd54745b212

test-suite/ph_ahc_diam/diam.ph.in
11f358b98f789924022bbd16c7df589801475d98

atomic/pseudo_library/LDA/REL/C.rel-pz-rrkjus.in
61a17ceaac6ddba89566902972b2eea8bc99d579
```

The fixture itself was not executed because the exporter gate had already failed at source level.

## Lower-Fan finding

In `EPW/src/selfen.f90`, the lower-Fan loop uses the existing complex vertex through the scalar contraction

```text
g2 = |epf17(jbnd, ibnd, imode, ik)|^2 × scalar factors
```

and accumulates

```text
sigmar_all(ibnd, ik_global, itemp)
sigmai_all(ibnd, ik_global, itemp)
```

The loop has one external-band index `ibnd`. It does not construct or retain a second external-band index `ibnd2` and therefore does not form

```text
g*_(m,n) g_(m,n')
```

for `n != n'`.

A complete lower-Fan matrix cannot be recovered from `sigmar_all` after this contraction. Adding the missing contraction would change the computed scientific observable.

## Upper-Fan and Debye--Waller finding

`EPW/src/wfpt.f90` does contain complex matrix-valued intermediates:

```text
sthf17 / sthmat       upper Fan
dwf17 / dwmatf_trunc Debye--Waller
```

The standard AHC accumulation subsequently extracts only band-diagonal real values into

```text
sigma_ahc_uf
sigma_ahc_hdw
sigmar_dw_all
```

Those two components could support a disabled-by-default observational exporter. That is insufficient because issue #289 requires all three components, including lower Fan.

## Gate result

```text
pinned source                                         PASS
insulating nonpolar upstream fixture identified       PASS
upper-Fan complex matrix available                    PASS
Debye--Waller complex matrix available                PASS
lower-Fan complex matrix available                    FAIL
observational-only exporter possible for all terms    FAIL
combined build/run required after source failure      NO
```

The result is `STOP`, not a partial pass.

## Why no build was performed

A build could test whether nonmagnetic SOC survives the executable WFPT call chain, but it cannot change the source-level absence of an already-computed lower-Fan matrix.

Under the predeclared rules, spending the build budget after the mandatory exporter gate failed would not change the decision. No QE/EPW build, upstream test, combined fixture, pseudopotential generation, or material calculation was performed.

## Consequences

Terminated:

```text
QE 7.6 / EPW 6.1
+ disabled-by-default observational exporter only
+ complete lower-Fan, upper-Fan, and Debye--Waller matrices
```

Not terminated:

- the general hybrid short-range plus generalized-Fröhlich architecture;
- diagonal QE/EPW AHC as a possible later cross-check;
- a separately derived external matrix Fan contraction;
- another backend that natively retains the complete matrix;
- the existing static canonical Kane-basis infrastructure.

## Next admissible design

The most promising continuation is an explicit repository-side **matrix Fan contraction engine** that consumes complex electron--phonon vertices, electronic energies, phonon frequencies, occupations, gauge transforms, and q-point weights.

That path must be treated as a scientific implementation, not an exporter. Before execution it requires:

1. a derivation of the frequency-dependent matrix Fan self-energy;
2. a declared Hermitian quasiparticle reduction;
3. diagonal equivalence to the standard EPW result;
4. unitary covariance inside degenerate subspaces;
5. causality and denominator-sign tests;
6. independent synthetic and upstream scalar benchmarks;
7. an explicit short-/long-range separation;
8. a separate authorization issue.

## Authorization boundary

This decision does not authorize:

- an EPW source patch adding the missing lower-Fan contraction;
- a QE/EPW build under issue #289;
- CdTe, HgTe, HgCdTe, A1, A2, or A3 calculations;
- dense interpolation;
- generalized-Fröhlich material prediction;
- use of the failed CdTe Born tensors;
- automatic continuation into a new matrix algorithm.

## Claim boundary

This result does not establish that QE or EPW is incorrect, or that SOC electron--phonon calculations are unsupported. It establishes only that the standard QE 7.6 / EPW 6.1 lower-Fan path does not already retain the full matrix required by R02, so the observational-export strategy cannot satisfy its mandatory information contract.
