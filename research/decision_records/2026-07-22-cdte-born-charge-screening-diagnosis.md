# Decision record: CdTe A0 Born-charge and screening diagnosis

**Date:** 2026-07-22  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #261  
**Parent:** #4  
**Status:** analytical diagnosis; no calculation authorized by this record

## Decision

The present Quantum ESPRESSO PBE/SOC response setup is **not validated for polar CdTe response or A1 electron--phonon work**.

The existing evidence does not identify one proven root cause. It does establish that the Born effective charges and electronic dielectric response are not numerically trustworthy under the tested setup.

One and only one bounded follow-up may be proposed after separate authorization:

> At the same stricter-response SCF state, calculate Born charges independently through QE's dielectric-response (`zeu`) and phonon-density-response (`zue`) algorithms, while preserving the complete tensor output and checking the occupied--unoccupied separation at every sampled k point.

This is a diagnostic comparison, not another convergence point. It must stop without A1 authorization unless both charge routes agree within a predeclared tensor tolerance and the charge-neutrality residual is small.

## Existing calculations

The baseline and stricter-response points differ only in

```text
ecutrho        456 -> 570 Ry
ph tr2_ph      1e-10 -> 1e-14
```

while retaining

```text
a_ref          6.476035479332049 A
ecutwfc        114 Ry
k grid         4 x 4 x 4, unshifted
nbnd           40
SCF conv_thr    1e-8 Ry
occupations     fixed
noncollinear    true
spin orbit      true
functional      PBE
```

The stricter point reports

```text
pressure                           31.20 kbar
direct Gamma gap                   0.4973 eV
epsilon_infinity                   62.332890864
raw acoustic magnitude             20.55 cm^-1
raw optical triplet               148.58 cm^-1
simple-ASR optical triplet        147.17 cm^-1
Cd Born charge                     +2.90543 e
Te Born charge                     -4.15794 e
Born-charge sum                    -1.25251 e
```

Relative to the baseline:

```text
raw acoustic magnitude             0.11191 x
ASR optical relative shift         0.03517 x
absolute Born-charge sum           2.42683 x
```

The acoustic and optical-ASR symptoms improve strongly, but the charge-neutrality error worsens.

## Governing identities and code behavior

For a neutral insulating primitive cell, translational invariance requires the Born effective-charge tensors to satisfy the charge acoustic sum rule

```text
sum_kappa Z*_(kappa,alpha,beta) = 0
```

for every Cartesian tensor component, up to numerical error.

The current `ph.x` input uses

```text
q = Gamma
trans = true
epsil = true
```

so QE computes the dielectric tensor and effective charges. The default effective-charge algorithm is `zeu`, obtained from the dielectric response. QE also provides the alternative `zue` algorithm from phonon density responses; the official input documentation states that the two should agree within numerical noise.

The current record contains only the default route. Therefore it cannot distinguish a general response failure from a route-specific defect.

## Hypothesis assessment

### H1. Parser or scalar-reduction error

**Assessment:** strongly disfavored.

The raw output values quoted in PR #104 match the parsed reference record. Cubic symmetry also produces identical reported diagonal values. A future diagnostic must nevertheless retain all tensor components rather than only their mean.

### H2. Smearing or explicitly metallic calculation

**Assessment:** not supported by the input.

The SCF uses `occupations='fixed'`, and the run reports a positive direct Gamma gap. QE accepts `epsil=true` for the state as an insulator.

This does **not** prove a globally insulating spectrum. A coarse k grid and fixed occupations can conceal an indirect overlap or very small separation away from Gamma. The minimum follow-up must inspect the occupied--unoccupied separation at every sampled k point.

### H3. Fixed-volume stress

**Assessment:** physically important but insufficient to explain charge non-neutrality.

The fixed experimental-reference volume gives approximately `31.2 kbar` PBE pressure. That can shift phonons, dielectric response, and individual Born charges and prevents interpretation as an equilibrium PBE material prediction.

However, uniform stress does not remove translational invariance of a neutral insulating periodic cell. It cannot make a `-1.25251 e` charge sum acceptable. Structural stress is therefore a model-discrepancy contributor, not a complete explanation of the failed sum rule.

### H4. Density-cutoff / pseudopotential response convergence

**Assessment:** strongly supported as a numerical-instability symptom; exact mechanism unresolved.

Both selected fully relativistic ONCV pseudopotentials include nonlinear core correction. The upstream cutoff hints constrain only the wavefunction cutoff; `ecutrho` must be converged independently. Raising `ecutrho` by 25% changes the Born-charge sum by a factor of `2.43` while leaving pressure and the direct Gamma gap unchanged.

This proves that the polar response is not stable with respect to the changed controls. It does not isolate whether the dominant source is density representation, nonlinear-core response, Sternheimer convergence, or interaction among them.

### H5. `tr2_ph` convergence alone

**Assessment:** not a sufficient control.

A tighter global phonon-response threshold materially improves acoustic and ASR diagnostics but does not constrain every electric-field and effective-charge response channel separately. The observed divergence between phonon and Born-charge diagnostics shows that `tr2_ph` cannot be used as a single convergence certificate.

### H6. Coarse Brillouin-zone sampling / anomalous screening

**Assessment:** high-priority surviving hypothesis.

The calculation uses a `4 x 4 x 4` grid. The electronic dielectric constant is `62.33`, indicating very strong interband screening in the declared PBE/SOC state. A small-gap polar semiconductor can have a large electronic dielectric response, but the value is not validated here and is especially sensitive to band separation and k-space integration.

The positive Gamma gap does not establish a robust insulating separation throughout the sampled Brillouin zone. The same-run occupied--unoccupied separation must be checked before interpreting the electric-field response.

### H7. Unsuitable setup for polar AHC

**Assessment:** current operational conclusion.

Regardless of the ultimate cause, a response setup that violates the Born-charge acoustic sum rule by order unity and whose charge sum worsens under tightening cannot support polar long-range electron--phonon terms. Stabilized optical frequencies alone are insufficient.

## Minimum discriminating follow-up

No broad convergence ladder is justified. A separate authorization may permit one same-state response diagnostic with no change to lattice, functional, pseudopotential bytes, wavefunction cutoff, density cutoff, k grid, occupations, bands, or SCF threshold.

Required outputs:

1. complete `zeu` Born tensors;
2. complete `zue` Born tensors;
3. tensor-by-tensor route difference;
4. tensor-by-tensor charge-neutrality residual before any imposed charge ASR;
5. dielectric tensor;
6. occupied--unoccupied separation at every sampled k point;
7. raw response convergence diagnostics and iteration history;
8. exact input/output hashes and resource use.

Predeclared pass conditions:

```text
maximum |sum_kappa Z*|                 <= 0.05 e
maximum |Z*_zeu - Z*_zue|              <= 0.05 e
all sampled occupied-unoccupied gaps    > 0.05 eV
all response channels report convergence
```

These are diagnostic acceptance thresholds for proceeding to a k-grid/cutoff design review, not material-accuracy claims.

Immediate stop conditions:

- either charge route violates neutrality above `0.05 e`;
- route disagreement exceeds `0.05 e`;
- any sampled occupied--unoccupied separation is `<=0.05 eV`;
- response convergence is incomplete or ambiguous;
- the full tensors cannot be exported reproducibly.

If any stop condition occurs, terminate this QE/PBE/pseudopotential polar-response path for A1. Do not repair the result by imposing a charge ASR and proceeding.

## Why charge-ASR projection is not a validation

QE post-processing can impose an acoustic sum rule on effective charges. That operation may be useful after a calculation is already converged. Here the raw violation is order unity and changes strongly with numerical controls. Projecting the tensors onto a neutral subspace would conceal the failed response rather than validate it.

## Authorization boundary

This record does not authorize:

- the proposed diagnostic run;
- additional cutoff or k-grid points;
- structural relaxation or equation-of-state work;
- A1, AHC, EPW, HgTe, or alloy calculations;
- interpretation of `epsilon_infinity`, phonons, or Born charges as converged CdTe properties.

A separate issue or decision must authorize the one bounded diagnostic and confirm available runtime cost.