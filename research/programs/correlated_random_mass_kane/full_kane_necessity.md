# R05 Phase 0 full-Kane necessity gate

**Controlling issue:** #390  
**Decision:** `DEFER_FULL_KANE`  
**Meaning:** the 8-band spatial-disorder calculation is unnecessary for the first mechanism/null test and necessary for any later quantitative HgCdTe optical or magneto-optical prediction

## 1. Decision question

Does the Phase 0 decision change if the first numerical oracle uses the full 8-band HgCdTe Kane Hamiltonian rather than the minimal random-mass Dirac model?

For the initial question

\[
\rho_{\rm corr}(E)
\stackrel{?}{=}
\int dM\,P(M)\rho_{\rm hom}(E;M),
\]

the required mechanism is coherent propagation through a finite-range signed mass field while matching the one-point mass distribution. A two-component model is sufficient to test whether the implementation and comparison protocol can detect such a nonlocal distinction.

## 2. Why full Kane is unnecessary for the first oracle

The minimal model already contains:

- a signed mass;
- a controlled correlation length;
- coherent spatial propagation;
- sign-changing interfaces;
- exact homogeneous and scalar-null references;
- particle-hole symmetry and domain-wall mechanism tests;
- a low-cost finite-size and ultraviolet convergence ladder.

A full 8-band calculation would add many parameters and operator-ordering choices before the central matched-null method is validated. It would make failures harder to diagnose and would not repair the absent HgCdTe correlation-length evidence.

Therefore PR 2, if authorized, should implement only the minimal oracle.

## 3. Why full Kane is likely necessary for a quantitative HgCdTe prediction

### 3.1 Heavy-hole flat-band participation

The HgCdTe massless-Kane regime contains a heavy-hole/flat-band sector absent from a two-component symmetric Dirac model. Existing HgCdTe SCBA work reports that the heavy-hole band materially changes the disorder-renormalized DOS and lowers the disorder-driven transition threshold.

A quantitative bulk DOS amplitude or transition threshold therefore cannot be transferred from the two-component oracle without a heavy-hole sensitivity test.

### 3.2 Optical matrix elements

Far-infrared conductivity and absorption require:

- multiband eigenvectors;
- occupation factors;
- transition matrix elements;
- heavy-hole and split-off contributions;
- realistic degeneracy;
- thickness and dielectric response.

A DOS difference alone does not determine an optical signal.

### 3.3 Magnetic-field response

Magneto-optical discrimination requires:

- Kane Landau levels;
- band-dependent optical selection rules;
- oscillator strengths;
- Zeeman terms where relevant;
- disorder broadening in a magnetic basis.

The minimal zero-field 1D oracle cannot provide these.

### 3.4 Electron-hole asymmetry and multiple velocities

The repository 8-band Hamiltonian includes quadratic terms and separate one-`P`/two-`P` closures. Near the energy range of an experiment, electron-hole asymmetry or distinct couplings may change both the scalar null and the correlated spectrum.

### 3.5 Noncommuting spatial parameter variations

A real alloy fluctuation may alter more than `Eg`:

```text
Ev
Eg
Delta
P or P8/P7
F
gamma1, gamma2, gamma3
```

Spatially varying coefficients multiplying derivatives require a Hermitian operator-ordering derivation. These disorder vertices may not commute and cannot be represented by a scalar random mass.

This is a reason for a later full-Kane study only if source evidence shows that non-mass parameter fluctuations materially affect the selected observable.

## 4. Full-Kane implementation hazards

A spatial 8-band Hamiltonian must resolve before coding:

1. Novik basis and phase convention;
2. relation between local composition and every spatial parameter;
3. Hermitian ordering for position-dependent linear and quadratic momentum terms;
4. boundary conditions and spurious-state control;
5. ultraviolet regularization;
6. physical degeneracy and DOS normalization;
7. heavy-hole flat-band regularization;
8. split-off-band truncation error;
9. scalar-null definition with the same multivariate local parameter distribution;
10. validation against the homogeneous `kane8.py` spectrum and symmetry tests.

A model with only spatial `Eg` variation but homogeneous `P`, `Delta`, and Luttinger parameters must be labeled a random-gap Kane sensitivity model, not a complete alloy-disorder Hamiltonian.

## 5. Decision-changing full-Kane criteria

Authorize a full-Kane calculation only if all are satisfied:

```text
minimal oracle passes analytical and convergence gates
matched non-scalar effect exceeds 10% before material mapping
a source-bounded HgCdTe parameter region overlaps the effect region
a candidate experiment remains after realistic convolution
heavy-hole, optical, magnetic, or asymmetry physics can change the activation decision
all required spatial parameter and operator-ordering conventions are explicit
an independent homogeneous and limiting-case reference exists
```

At least one specific prediction must be named, such as:

- heavy-hole sector suppresses or enhances the convolved DOS effect by more than the decision margin;
- multiband optical matrix elements convert the DOS distinction into a resolvable conductivity feature;
- Landau-transition line shapes retain a covariance-sensitive component not reproduced by scalar averaging.

“More realistic” is not a sufficient authorization reason.

## 6. Recommended hierarchy after a successful minimal oracle

```text
Stage 1: homogeneous 8-band scalar-mixture null using kane8.py
Stage 2: two-band versus reduced Kane block comparison at matched homogeneous parameters
Stage 3: heavy-hole-inclusive minimal 3-band or 6-band sensitivity model
Stage 4: spatial 8-band random-gap model with derived Hermitian ordering
Stage 5: multivariate alloy-disorder vertices only if source evidence supports them
Stage 6: magnetic or optical response only for a selected experiment
```

Every stage requires a stop rule and must demonstrate that the previous lower-cost model is inadequate for the decision.

## 7. Current decision

```text
minimal random-mass Dirac oracle: JUSTIFIED_AS_METHOD_AND_THRESHOLD_TEST
full 8-band spatial oracle: NOT_AUTHORIZED
homogeneous 8-band null audit: AUTHORIZED_LATER_IF_MINIMAL_ORACLE_PASSES
quantitative optical/magneto-optical prediction: REQUIRES_FULL_KANE_OR_VALIDATED_REDUCTION
```

The full-Kane gate does not block the minimal oracle. It blocks promotion of a minimal-model result into a quantitative HgCdTe experimental claim.