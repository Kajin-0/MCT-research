# Decision record: finite-temperature Kane matrix oracle

**Date:** 2026-07-18  
**Status:** synthetic matrix pipeline validated; real A1 input still blocked  
**Scope:** finite-temperature Kane self-energy symmetry, quasiparticle reduction, parameter recovery, and analytical thermal reduction

## Decision summary

The deterministic finite-temperature matrix oracle passes every declared gate.

The repository can now distinguish failures in a future real electron-phonon calculation from failures in the downstream matrix machinery. The following components have been validated against known synthetic truth:

- `Td`-symmetric Gamma self-energy construction;
- positive-definite quasiparticle metric enforcement;
- matrix quasiparticle linearization;
- exact dynamical quasiparticle pole solution;
- bounded error of first-order dynamical linearization;
- recovery of `Eg`, `Delta`, `P8`, `P7`, `F`, and `gamma_i` from finite-k matrices;
- rejection of the one-`P` restriction when `P8 != P7`;
- held-out one-scale versus two-scale thermal reduction;
- signed thermal moments and turnover detection.

This result validates a method pipeline. It is not a CdTe or HgCdTe electron-phonon result and does not authorize A1.

## 1. Why the oracle was required

The static audit showed that an apparently reasonable overlap construction can target the wrong effective Hamiltonian while still preserving symmetry and producing small residuals. A finite-temperature workflow therefore cannot be trusted merely because it runs, preserves Hermiticity, or fits a parameter model.

Before spending A1 computational resources, the complete downstream path must recover a self-energy and thermal trajectory whose truth is known exactly.

The oracle is deliberately zero-compute:

1. construct a known two-`P` thermal Kane trajectory;
2. construct a linear matrix self-energy whose quasiparticle reduction equals that target exactly;
3. add a separate rational dynamical self-energy with a remote pole;
4. recover matrix parameters from finite-k matrices;
5. test one- and two-scale analytical thermal reductions on held-out temperatures.

## 2. Synthetic thermal target

The static reference point uses the corrected CdTe smoke values only as numerical scales:

```text
Eg     = 0.4972157232164524 eV
Delta  = 0.8592417011362832 eV
P8     = 6.772221951499152 eV A
P7     = 6.201825720178372 eV A
```

No physical meaning is assigned to the synthetic thermal amplitudes.

The gap trajectory is generated from two signed Bose scales:

```text
Theta1 = 70 K,  A1 = +0.004 eV
Theta2 = 240 K, A2 = -0.018 eV
```

The resulting relative gap shifts are:

```text
T (K)       0       20       50       100      200      300
Delta Eg   0.000   0.249    2.320    4.300    3.574    1.066 meV
```

The signed contributions produce a resolved maximum at `100 K`, followed by a decline.

## 3. Matrix quasiparticle result

For a linearized self-energy,

```text
A = I - Sigma'
B = H0 + Sigma(z0) - z0 Sigma'
H_QP = A^-1/2 B A^-1/2
```

the oracle constructs `Sigma(z0)` from a known target Hamiltonian and then independently reconstructs `H_QP`.

Result:

```text
maximum matrix relative error = 1.375089300405315e-16
minimum metric eigenvalue     = 0.92
maximum Gamma symmetry error  = 0.0
```

A nonpositive metric is rejected by test.

## 4. Dynamical pole result

Each Gamma irrep uses a rational self-energy:

```text
Sigma(z) = offset + slope*(z-z0) + g^2/(z-Eremote)
```

The target quasiparticle root is solved by fail-closed bisection without crossing the remote pole. The exact roots are compared against first-order quasiparticle linearization.

Result:

```text
maximum pole linearization error = 5.606447750494681e-09 eV
```

This is more than two orders of magnitude below the declared `1e-6 eV` method gate.

## 5. Matrix parameter recovery

The complete extended-Kane model is fitted by linear matrix regression over nine finite-k points.

Result:

```text
maximum absolute parameter error = 1.1461796789458134e-11
maximum two-P matrix residual     = 4.264895857130218e-16
minimum one-P matrix residual     = 2.266042026692118e-4
```

The two-`P` truth is recovered to numerical precision, while the nested one-`P` restriction is correctly rejected at the declared gate.

## 6. Held-out analytical reduction

Training temperatures are `20, 100, 300 K`; held-out temperatures are `50, 200 K`.

### One-scale model

The one-scale model is restricted to `Theta = 70 K`.

```text
training relative residual = 87.9311%
held-out errors             = 2.1438, 2.2908 meV
maximum held-out error      = 2.2908159401962296 meV
```

It fails the declared `2 meV` held-out threshold.

### Two-scale model

The two known scales are fixed at `70 K` and `240 K`, while amplitudes are fitted only on the training temperatures.

Recovered amplitudes:

```text
A1 = +0.00399999999999999 eV
A2 = -0.01799999999999993 eV
```

Result:

```text
maximum held-out error = 8.239936510889834e-14 meV
improvement             = 22.9082 declared numerical sigmas
```

The oracle therefore detects when a second signed thermal channel is genuinely required by held-out predictions.

The recovered signed moments are:

```text
mu_-1 = -1.7857142857142716e-05 eV/K
mu_0  = -0.01399999999999994 eV
mu_1  = -4.039999999999984 eV K
```

These are synthetic truth values, not material moments.

## 7. Evidence

```text
workflow run: 29641452536
artifact:     8428743550
digest:       sha256:3b5586418f649b5aa077527fae02de6a62ee1b4c42efaf3b8f929bdb6c7712c9
head:         77f5551a28349b79dfbcf45892d746cbd804ce2c
```

Controlling compact record:

```text
first_principles/matrix_oracle/finite_temperature_kane_oracle_reference_result.json
```

## 8. Scientific consequence

The downstream matrix pipeline is ready to accept real first-principles inputs.

This does not imply that the current CdTe A0 response is physically usable. The next real-input stage must specify exactly which quantities are exported from A1 and must reject inputs that fail phonon, acoustic-sum-rule, Born-charge, convergence, gauge, or provenance checks.

The next valid question is not “Can the code process a finite-temperature self-energy?” That is now answered.

The next question is:

> What is the smallest real electron-phonon export that can populate the validated matrix pipeline and falsify a scalar-only thermal model without committing to production AHC?

## 9. Authorization

Authorized:

- design the minimum real-input A1 export schema;
- define physical and numerical sanity gates;
- map mode-resolved Fan and Debye-Waller information into the validated matrix representation;
- preserve gauge-invariant observables separately from gauge-fixed matrix coefficients.

Not authorized:

- execute A1 from the current failed A0 physical-response state;
- production AHC;
- dense EPW;
- HgTe;
- VCA, SQS, CPA, or alloy electron-phonon work;
- physical claims from the synthetic amplitudes or moments.
