# Decision record: hybrid short-range matrix AHC plus generalized-Fröhlich closure

**Date:** 2026-07-22  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #285  
**Parents:** #2, #4  
**Status:** restricted go for analytical capability audit only

## Decision

The preferred continuation of R02 is a hybrid decomposition:

1. obtain a symmetry-resolved first-principles **short-range** electron–phonon contribution;
2. construct the long-range polar contribution independently with a generalized Fröhlich model;
3. combine the two only under an explicit no-double-counting contract;
4. project the endpoint result into the existing canonical eight-band Kane basis;
5. use special-displacement finite-temperature calculations only as an independent total-shift cross-check, not as the source of Fan/Debye–Waller decomposition.

The current authorization is limited to source inspection, analytical derivation, schema design, parser prototypes on synthetic or upstream test data, and a written go/restricted-go/stop decision. No CdTe, HgTe, alloy, A1, dense EPW, altered pseudopotential, altered functional, or altered-grid calculation is authorized.

## Why this is the most promising path

The previous CdTe response work did not show a disagreement between Quantum ESPRESSO's two effective-charge algorithms. It showed that two independent routes agreed closely while sharing an order-unity raw neutrality failure. Reusing those tensors, or projecting them onto charge neutrality, would convert a failed validation into an unearned physical assumption.

Abandoning electron–phonon matrix work entirely would also discard the strongest candidate-novel part of R02: a symmetry-preserving finite-temperature self-energy projected into the complete Kane manifold with closure tests on more than the scalar gap.

The hybrid design isolates the failed observable instead of discarding the entire program:

```text
validated short-range matrix physics
+
independent long-range polar physics
=
controlled endpoint self-energy
```

## Architecture

At the accepted fixed reference volume, define

```text
Sigma_ep(k, omega, T)
  = Sigma_SR_lower_Fan(k, omega, T)
  + Sigma_SR_upper_Fan(k, T)
  + Sigma_SR_DW(k, T)
  + Sigma_LR_Frohlich(k, omega, T).
```

Thermal expansion remains separate:

```text
H_8(T)
  = H_8_static[V0]
  + Sigma_ep[T; V0]
  + {H_8_static[V(T)] - H_8_static[V0]}.
```

The short-range calculation must not contain the dipole Fröhlich contribution that is added analytically. The long-range model must not reuse the failed CdTe Born-charge tensors or any charge-ASR-repaired derivative of them.

## Primary computational candidate

The primary candidate for the short-range tranche is Quantum ESPRESSO 7.6 / EPW 6.1 using Wannier-function perturbation theory and the AHC path.

This is a candidate, not an authorization. Current source and documentation show promising ingredients:

- an AHC/WFPT implementation containing lower Fan, upper Fan, and Debye–Waller machinery;
- complex matrix-valued internal arrays rather than a purely scalar implementation;
- spinor/SOC infrastructure in the QE/EPW stack;
- explicit polar, long-range, and short-range controls in EPW;
- mode-resolved electron–phonon data pathways;
- a current release with active maintenance.

The complete nonmagnetic-SOC AHC path, user-facing matrix export, gauge behavior, and short-/long-range isolation remain unverified. Those are B0 questions, not assumptions.

## Rejected primary alternative: ABINIT EPH

ABINIT is not selected as the primary R02 endpoint backend because its current EPH documentation states that electron–phonon self-energy calculations do not support spin–orbit coupling or noncollinear spinors.

ABINIT remains useful as a theory and file-format reference because it provides:

- Fan–Migdal plus Debye–Waller self-energies;
- mode/frequency selection;
- generalized-Fröhlich ZPR correction;
- mature convergence and post-processing conventions.

Those strengths do not compensate for the missing SOC capability in HgCdTe endpoint work.

## Independent validation candidate

The EPW/ZG special-displacement method can evaluate finite-temperature band structures through displaced supercells and can retain SOC in the underlying electronic calculation.

Its role is limited to an independent check on total edge or gap shifts because it does not, by itself, provide the required explicit lower-Fan, upper-Fan, and Debye–Waller matrix decomposition.

A special-displacement result cannot satisfy the main R02 matrix-AHC objective and cannot be used to infer that the separate components are correct merely because their sum agrees with experiment.

## Long-range generalized-Fröhlich tranche

The long-range model must be nonadiabatic and capable of handling:

- multiple infrared-active LO branches;
- degenerate or quasidegenerate band extrema;
- anisotropic effective masses where required;
- separate Gamma6, Gamma8, and Gamma7 edge corrections;
- zero-point and finite-temperature contributions;
- uncertainty in every external input.

The first input contract should contain, at minimum:

```text
material and phase
reference volume and temperature convention
epsilon_infinity tensor
epsilon_static tensor or mode-effective dielectric increments
LO frequencies and branch labels
band-edge effective-mass tensors
band degeneracies and symmetry labels
source identifiers
measurement/calculation conditions
central values, covariance or conservative bounds
unit declarations
```

The primary theoretical anchor is the generalized Fröhlich treatment used to explain why nonadiabatic effects are essential for infrared-active materials. The long-range term is therefore not a fitted residual polynomial.

## First scientific target

The first target is the fixed-volume Gamma-block temperature dependence:

```text
Delta E_Gamma6(T)
Delta E_Gamma8(T)
Delta E_Gamma7(T)
Delta Eg(T)       = Delta E_Gamma6 - Delta E_Gamma8
Delta DeltaSO(T)  = Delta E_Gamma8 - Delta E_Gamma7.
```

Only after these quantities pass component-wise validation may the program extend to finite-k closure of

```text
Eg, Delta, P8, P7, F, gamma1, gamma2, gamma3.
```

This ordering is deliberate. It tests the physically identifiable band-edge structure before paying for a complete finite-k matrix dataset.

## Validation hierarchy

The result must be tested in the following order:

1. source-level capability and incompatibility checks;
2. upstream nonpolar AHC/WFPT reference reproduction;
3. upstream or synthetic nonmagnetic-SOC path test;
4. matrix export and gauge round-trip test;
5. explicit short-/long-range bookkeeping test;
6. generalized-Fröhlich implementation against a published benchmark;
7. CdTe external-input consistency review;
8. one separately authorized bounded CdTe short-range smoke test;
9. total-shift comparison against independent experimental or historical HgCdTe/CdTe evidence;
10. eight-band projection and closure residual.

Failure at an earlier level blocks later levels.

## B0 decision gates

B0 returns one of three decisions.

### Go

All required SOC, component-separation, matrix-export, gauge, and short-/long-range capabilities are explicitly supported and reproducible from pinned source or upstream tests.

### Restricted go

The code can produce a decision-changing subset, such as Gamma-block short-range component matrices, but not the complete finite-k production object. A bounded smoke test may then be proposed only for that subset.

### Stop

Any of the following terminates the EPW/LWFPT route before a material run:

- nonmagnetic SOC fails in a required AHC/WFPT stage;
- lower Fan, upper Fan, and Debye–Waller cannot be separated;
- only final diagonal scalar shifts are accessible;
- no stable map exists from the internal smooth gauge to the canonical Kane basis;
- the short-/long-range split cannot be made explicit;
- external long-range inputs cannot be combined without double counting;
- output volume or cost is disproportionate to the first decision-changing observable.

## Claim boundary

This decision does not establish that the hybrid method works numerically for CdTe or HgCdTe. It selects the architecture that best preserves R02's scientific objective while respecting the failed polar-response gate.

No new HgCdTe bandgap equation should be fitted until the component model is validated on held-out data and shown to provide either improved prediction or new physically identifiable information beyond Hansen, Laurenti, and the 1995 electron–phonon treatment.

## Sources to pin in the capability audit

- ABINIT EPH introduction and ZPR documentation, current 2026 version;
- Quantum ESPRESSO 7.6 release notes;
- EPW 6.1 release and input documentation;
- QE `PHonon/PH/phq_readin.f90` AHC/SOC guards;
- EPW `wfpt.f90` AHC implementation;
- EPW long-range/short-range interpolation controls;
- Miglio et al., 2020 generalized-Fröhlich/nonadiabatic ZPR work;
- Nery and Allen polar correction work;
- Zacharias and Giustino special-displacement theory;
- Krishnamurthy et al., 1995 HgCdTe electron–phonon calculation;
- Teppe et al., 2016 temperature-dependent Kane-fermion validation.
