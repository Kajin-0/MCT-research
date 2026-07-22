# QE 7.6 / EPW 6.1 raw-vertex fixture selection

**Date:** 2026-07-22  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #300  
**Status:** source qualification only; no build or scientific execution authorized

## Decision

Select the upstream `test-suite/epw_base` diamond fixture for the first raw complex-vertex normalization test.

The fixture is selected because it is:

- upstream and release-pinned;
- nonpolar;
- insulating in its intended role;
- already configured for four electronic bands;
- already configured to calculate the electron self-energy;
- small enough to remain inside the declared resource ceiling;
- independent of CdTe, HgTe and HgCdTe;
- sufficient to expose `epf17` before the standard modulus-square contraction.

The upstream `epw_wfpt` BAs fixture is rejected for this gate because its EPW input enables `lpolar=.true.`. The first normalization fixture must not require a long-range polar decomposition.

## Pinned source state

```text
repository   QEF/q-e
release tag  qe-7.6
commit       9f93ddec427d2b9a45bb72d828c6d324f62fcabd
EPW version  6.1
```

The following Git object identities are predeclared:

| Path | Git blob SHA |
|---|---|
| `EPW/src/selfen.f90` | `be4858854d1ab26d27b3acf52a9a30c21fa8b472` |
| `test-suite/epw_base/scf.in` | `aa6e84ee470749bceb22e43ae0f18396e34490b3` |
| `test-suite/epw_base/ph.in` | `37450ee9680c455b75195787e05dca78e2e2c671` |
| `test-suite/epw_base/scf_epw.in` | `1bdb39f7567c30cffafe38cebe9e6443f2d025f7` |
| `test-suite/epw_base/nscf_epw.in` | `50542d302a8772f24d46e1d98e194cff51cb3f54` |
| `test-suite/epw_base/epw1.in` | `624b4f8a47b003443a131f15afb7815b33a3398e` |
| `pseudo/C_3.98148.UPF` | `368260443c8341d971fe9da5690f6697f0f8864c` |

Git blob identities do not replace SHA-256 provenance. Phase 1 must clone the exact commit, verify every blob identity and calculate SHA-256 values before any compilation or executable run.

## Upstream fixture properties

### Ground state

The upstream SCF input defines diamond with:

```text
prefix      diam
nat         2
ntyp        1
nbnd        4
pseudo      C_3.98148.UPF
k grid      6 x 6 x 6
```

### Phonons

The upstream phonon input declares:

```text
epsil       false
q grid      3 x 3 x 3
```

The absence of dielectric response is the controlling nonpolar property for this fixture.

### EPW electron self-energy

The upstream `epw1.in` declares:

```text
elph          true
elecselfen    true
nbndsub       4
coarse k      3 x 3 x 3
coarse q      3 x 3 x 3
fine k        6 x 6 x 6
fine q        6 x 6 x 6
temperature   300 K
degaussw      1 eV
```

No `lpolar` setting is enabled.

## Bounded export window

Writing every scalar loop row would create unnecessary evidence volume. The observational exporter will retain a complete matrix block for one external fine-grid k point while covering all q points:

```text
ik_global          1
external bands     all 4
intermediate bands all 4
phonon modes       all
q points           all
temperatures       all
```

This window preserves:

- a complete `4 x 4` complex vertex block for every selected `(q,nu)` contribution;
- full q-weight coverage and a q-weight sum test;
- all phonon branches, including explicit acoustic-mask behavior;
- per-band and summed scalar diagonal reconstruction;
- a synthetic external rotation test.

The backend continues calculating its original full fixture. The exporter only filters what it writes.

## Exact backend normalization

The pinned source uses

```text
g2 = |epf17|^2 * inv_wq * g2_tmp
inv_wq = 1 / (2 omega_qnu)
```

where `g2_tmp` is one above the acoustic threshold and zero below it. The source comments state that the phonon zero-point displacement is included by this factor and that the resulting `g2` has squared-energy units.

The repository adapter must therefore construct

```text
G_normalized_eV
  = epf17 * sqrt(inv_wq * g2_tmp) * ryd2ev
```

and pass `wqf_loc` separately to the matrix-Fan kernel.

For one external state, the real diagonal reconstructed at the backend on-shell energy must equal the exported full-precision scalar increment after conversion from Rydberg to electronvolts.

The non-WFPT fixture uses Gaussian broadening for the positive linewidth accumulator. Therefore the first fixture compares the real self-energy exactly and checks the retarded imaginary sign independently; it does not claim equality between Gaussian linewidth magnitude and the Lorentzian imaginary part of the retarded denominator.

## Two-phase execution gate

### Phase 1 — authorized now

- clone exact source commit;
- verify Git blob identities;
- calculate SHA-256 for every required source, input and pseudopotential file;
- preserve a source manifest and artifact digest;
- run focused repository tests only.

### Phase 2 — closed until a new commit

- build QE/EPW;
- apply the observational patch;
- run `epw_base` with the exporter disabled and enabled;
- analyze vertices and scalar equivalence.

Phase 2 may be enabled only after the Phase 1 SHA-256 values and artifact digest are committed to the contract. The workflow cannot transition automatically.

## Claim boundary

Selecting and hashing the fixture does not establish:

- that QE 7.6 / EPW 6.1 builds in the intended environment;
- that the exporter compiles or is observational;
- that raw vertices are complete or correctly normalized;
- that the external matrix-Fan kernel matches a backend result;
- that SOC spinor vertices work;
- that any material lower-Fan matrix is valid.
