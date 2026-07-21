# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #184  
**Execution mode:** independent, public-data-first, reproducible computation

## Completed Paper I

The observation-model uncertainty manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It establishes that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap laws. Remaining work is submission administration, not scientific expansion.

## Active flagship manuscript

The active research product is:

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

The analytical core was merged in PR #181. Deterministic manuscript figures and tables were merged in PR #183.

Controlling directory:

```text
manuscript/distributional_band_edge/
```

## Principal theorem

For the declared Gaussian-gap, power-law local-edge, uniform carrier-translation, and single-pass Beer-Lambert model, the nominal parameters

```text
Eg0
Delta_carrier
ln sigma_G
ln A
ln d
```

enter the dense single-state response spectrum only through:

```text
Eg0 + Delta_carrier
sigma_G
A*d
```

Therefore:

```text
dR/dEg0 = dR/dDelta_carrier
dR/dlnA = dR/dlnd
rank(J) <= 3
```

No increase in signal-to-noise, spectral resolution, or point count can remove these exact forward-model null directions.

Two physically different parameter sets preserving the three identifiable combinations produce 281-point spectra with committed numerical difference bounded by:

```text
2.22e-16
```

An absolutely calibrated nontranslational carrier marker raises rank to four but leaves one combined invariance with infinitesimal null vector:

```text
(Delta_carrier, -Delta_carrier, 0, -1, +1)
```

## Supporting quantitative results

### Distributional transition

At nominal `x=0.155`, the declared latent laws span:

```text
25.0803 K
```

in central critical temperature. At `sigma_x=0.010`, `8.60-14.12%` of the declared conditioned Gaussian model remains normal throughout `0-300 K`, and conditional-root censoring causes local linearization to overstate the exact width by as much as `9.657 K`.

These are model-conditioned transition statistics, not measured topological phase fractions.

### Gaussian-gap tail

Herrmann's convention is:

```text
sigma_G = sqrt(2)*s
```

The source-aligned square-root convolution over `1-100 cm^-1` gives:

```text
W_fit/s = 0.50504
R^2     = 0.99570
```

Changing only the fit window from `1-100` to `100-500 cm^-1` increases apparent tail energy by `60.1%`. For an observed `W_fit=4 meV`, the declared operator family permits:

```text
sigma_G = 6.995-12.661 meV
```

An Urbach-like tail does not uniquely identify gap-distribution width or microscopic origin.

### Thickness-defined cutoff

For an exponential tail:

```text
E_cut(d2)-E_cut(d1) = -W ln(d2/d1)
```

In the declared synthetic Chang case, changing effective thickness from 5 to 20 um shifts the 50% cutoff by:

```text
energy      -16.636 meV
wavelength   +2.494 um
```

Any number of tail-only cutoff observations has:

```text
rank(J_tail) <= 2
```

for `(Eg,W,ln A,ln b)`. Mixed intrinsic/tail observations restore local rank four in the declared design but retain condition number `199.81`.

### Nonparabolic carrier filling

For

```text
E_c*(1+alpha*E_c)=E_par
```

the exact positive solution is:

```text
E_c=2*E_par/(1+sqrt(1+4*alpha*E_par))
```

At the declared `7.0e17 cm^-3` sensitivity point, the parabolic Burstein-Moss estimate exceeds the nonparabolic result by:

```text
147.323 meV
```

A five-density series is locally rank five but has condition number:

```text
11034.75
```

The declared masses and nonparabolicity are illustrative and are not inferred for the Dingrong specimen.

## Manuscript analytical and generated assets

Merged analytical assets:

```text
README.md
manuscript_draft.md
theorem_index.md
claim_matrix.md
figure_plan.md
figure_manifest.json
submission_gap.md
```

Deterministic asset entry point:

```text
python -m tools.build_distributional_band_edge_manuscript_assets \
  --repository-root . \
  --output-dir distributional-generated
```

The merged pipeline generates:

```text
7 deterministic SVG figures
3 Markdown manuscript tables
1 machine-readable asset summary
```

It regenerates the Herrmann tail, carrier-density series, and unified exact-counterexample spectra through public functions; fails closed against immutable records; embeds claim/source/commit metadata; and remains byte-for-byte deterministic.

## DOI intake and external-validation gate

Issue #184 establishes the auditable paper-intake and route-selection layer.

Controlling files:

```text
literature/acquisition/distributional_band_edge_sources.json
literature/acquisition/source_intake_protocol.md
src/mct_research/validation_gate.py
tools/build_external_validation_gate.py
data/validation/external_validation_route_gate.json
research/decision_records/2026-07-21-external-validation-route-selection.md
```

The gate ranks expected decision value under the current acquisition state. It is not a probability that a source or model is correct.

### Selected first route

```text
Chang multi-thickness / cutoff validation
score      24
readiness  ready_after_retrieval
```

Required source pair:

```text
10.1007/s11664-007-0162-0
10.1063/1.2245220
```

Blocking evidence:

```text
native or calibrated spectra
same-specimen W and b
effective-thickness provenance
carrier state and response construction
```

The Chang route is selected because a tested source-bounded operator already exists and a successful retrieval can directly test a merged theorem and observation operator.

### Ranked routes

```text
1  Chang thickness/cutoff                 24
2  Dingrong carrier spectrum              20
3  Chu intrinsic absorption               19
4  Herrmann multimodal tail               18
5  Teppe transition series                18
6  Moazzami source-native recovery         16
7  Ivanov-Omskii PL joint closure          15
8  Finkman independent tail                14
9  Krishtopenko prior-art audit             2
```

### Highest-value single physics source

Dingrong remains the highest-value single paper for replacing the generic carrier marker with a physical carrier-dependent spectrum:

```text
10.1016/0038-1098(85)90315-1
```

It is ranked second as an implementation route because complete equations, calibrated spectra, specimen thickness, optical geometry, and nuisance-state separation remain missing.

### User request order

Request first:

```text
10.1007/s11664-007-0162-0
10.1063/1.2245220
10.1016/0038-1098(85)90315-1
```

Supplements, author manuscripts, source data, parameter tables, and high-resolution figures are more valuable than duplicate publisher PDFs.

## Source-intake boundary

A retrieved paper does not authorize an operator change.

Every source must pass:

1. DOI and version verification;
2. rights classification;
3. cryptographic hashing;
4. specimen and parameter ownership audit;
5. equation, unit, convention, and valid-domain audit;
6. figure/data calibration audit;
7. route re-scoring;
8. a separate issue and PR before any scientific operator changes.

Publisher PDFs are not committed to the public repository merely because the user supplied them. Citations, hashes, permitted notes, equations, digitizations, and derived data remain the default public artifacts.

## External validation boundary

No complete real-specimen unified-model validation is claimed.

The selected Chang route remains `ready_after_retrieval`, not ready now. If the source pair fails its calibration, parameter-ownership, or effective-thickness gates, the route is rejected and the deterministic ranking is recomputed.

External collaborators are not required. Public full texts, author manuscripts, supplements, permitted source data, auditable digitization, and reproducible computation remain the primary strategy.

## Static and finite-temperature first-principles boundary

The selected-band CdTe static post-processing result remains independently reproducible on the same immutable physical artifact. It is a mathematical and software component, not a converged HgCdTe material prediction.

The present CdTe polar response remains unsuitable for production AHC. New AHC, SQS, CPA, SCBA, or broad alloy calculations require:

- a decision-changing observable;
- a published validation target;
- a predeclared termination criterion;
- evidence that the lower-cost observation model cannot resolve the decision.

## Authorized next work

1. complete CI and merge Issue #184;
2. intake and audit any retrieved Chang or Dingrong source;
3. recompute the validation-route gate after each source audit;
4. open a route-specific implementation issue only after a source passes its rejection gates;
5. integrate one real-spectrum validation without changing exact theorem claims;
6. convert approved SVG assets to journal PDF format;
7. verify bibliography, archive DOI, authorship, declarations, and journal packaging.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- merging Paper I and the flagship manuscript as if they were one study;
- selecting one optical edge without an observation-operator declaration;
- identifying `sigma_x`, `sigma_G`, Herrmann `s`, Urbach energy, PL FWHM, and quasiparticle linewidth as equivalent;
- treating local gap-sign probability as a bulk topological invariant;
- treating detector cutoff as a direct material gap;
- treating physical film thickness as effective absorbing thickness without validation;
- transferring Chang `b` or Dingrong carrier corrections between specimens without provenance;
- conflating Burstein-Moss filling with band-gap renormalization;
- treating the generic carrier marker as the Dingrong free-carrier law;
- assigning synthetic parameters to real specimens;
- interpreting route score as truth probability;
- changing an operator merely because a paper was obtained;
- committing restricted source PDFs without verified rights;
- requiring real collaborators before progress can continue;
- escalating to expensive first-principles or atomistic work without a decision-changing validation target.
