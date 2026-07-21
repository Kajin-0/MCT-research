# Current research program state

**Last updated:** 2026-07-21  
**Controlling issue:** #167  
**Active milestone:** #179  
**Execution mode:** independent, public-data-first, reproducible computation

## Completed Paper I

The observation-model uncertainty manuscript is scientifically frozen:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

It establishes that historical composition uncertainty, specimen state, source lineage, carrier/defect state, and edge-definition choice dominate the sub-meV ordering among common empirical gap laws. Remaining work is submission administration, not scientific expansion.

## Active flagship manuscript

The active research product is:

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

The manuscript develops the constructive forward counterpart to Paper I:

```text
latent mean signed gap
-> composition/gap distribution
-> carrier and defect state
-> intrinsic, tail, and free-carrier response
-> thickness/instrument response
-> declared observation operator
-> reported gap observable
```

The analytical core is complete on branch:

```text
agent/flagship-manuscript-analytical-core
```

The controlling manuscript directory is:

```text
manuscript/distributional_band_edge/
```

## Principal theorem

For the declared Gaussian-gap, power-law local-edge, uniform carrier-translation, and single-pass Beer–Lambert model,

```text
parameters:
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

No improvement in signal-to-noise, spectral resolution, or point count can remove these exact forward-model null directions.

Two physically different parameter sets preserving the three identifiable combinations produce 281-point spectra with maximum absolute difference:

```text
2.22e-16
```

An absolutely calibrated nontranslational carrier marker raises rank to four but leaves one combined invariance with infinitesimal null vector:

```text
(Delta_carrier, -Delta_carrier, 0, -1, +1)
```

## Supporting results

### Distributional transition

At nominal `x=0.155`, the declared latent laws give:

```text
Laurenti reconstructed              77.1241 K
Hansen-Schmit-Casselman             52.0438 K
archived provisional Hansen-Pade    52.5937 K
central model span                  25.0803 K
```

At `sigma_x=0.010`, `8.60-14.12%` of the declared conditioned Gaussian model remains normal throughout `0-300 K`. Conditional-root censoring causes the local linearized transition-width estimate to overstate the exact conditional width by as much as `9.657 K`.

These are model-conditioned transition statistics, not bulk topological phase fractions or measured Teppe specimen distributions.

### Gaussian-gap tail

Herrmann’s convention is:

```text
sigma_G = sqrt(2)*s
```

The source-aligned square-root convolution over `1-100 cm^-1` gives:

```text
W_fit/s = 0.50504
R^2     = 0.99570
```

Changing only the fit window from `1-100` to `100-500 cm^-1` increases the apparent tail energy by `60.1%`, while both fits remain strongly log-linear.

For an observed `W_fit=4 meV`, the declared operator family permits:

```text
sigma_G = 6.995-12.661 meV
```

An Urbach-like tail is compatible with a Gaussian gap distribution but does not uniquely identify its width or microscopic origin.

### Thickness-defined detector cutoff

For an exponential tail:

```text
E_cut(d2)-E_cut(d1) = -W ln(d2/d1)
```

In the declared synthetic Chang case, changing effective thickness from 5 to 20 um shifts the 50% cutoff by:

```text
energy      -16.636 meV
wavelength   +2.494 um
```

without changing latent `Eg`.

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

At the declared Dingrong-density sensitivity point:

```text
n          = 7.0e17 cm^-3
m_edge     = 0.010 m0
alpha      = 7.5 eV^-1
m_valence  = 0.35 m0
```

the parabolic Burstein–Moss estimate exceeds the nonparabolic result by:

```text
147.323 meV
```

A five-density series is locally rank five but has condition number:

```text
11034.75
```

The parameters are illustrative and are not inferred for the Dingrong specimen.

## Manuscript asset state

Completed on the active branch:

```text
README.md
manuscript_draft.md
theorem_index.md
claim_matrix.md
figure_plan.md
figure_manifest.json
submission_gap.md
```

Controlling decision:

```text
research/decision_records/2026-07-21-flagship-manuscript-analytical-core.md
```

Every headline value is tied to an immutable record:

```text
data/validation/near_critical_transition_model_dependence.json
data/validation/herrmann_gaussian_tail_reproduction.json
data/validation/chang_2006_cutoff_identifiability.json
data/validation/dingrong_1985_carrier_filling_sensitivity.json
data/validation/unified_spectrum_structural_rank.json
```

## DOI-assisted acquisition queue

The user can search for full texts or supplements using exact DOIs. Highest priorities are:

```text
10.1016/0038-1098(85)90315-1   Dingrong carrier-filled absorption
10.1007/s11664-007-0162-0       Chang 2007 nonparabolic-Urbach/cutoff
10.1063/1.2245220                Chang 2006 short-form source
10.1016/0022-0248(92)90851-9    Herrmann multimodal broadening
10.1016/j.physb.2009.08.210     Ivanov-Omskii PL/annealing
10.1038/ncomms12576              Teppe near-critical Kane transition
10.1016/0020-0891(91)90110-2    Chu intrinsic absorption spectroscopy
```

Exact acquisition requirements and scientific payoff are recorded in:

```text
manuscript/distributional_band_edge/submission_gap.md
```

Retrieved papers must pass a source audit before changing an operator or claim.

## External validation boundary

No complete real-specimen unified-model validation is claimed.

Preferred independent validation routes are:

1. same-state multi-thickness absorption or detector response;
2. same-specimen Hall-measured carrier-state spectral series;
3. processing-conditioned PL displacement and FWHM test;
4. source-native recovery of the existing Paper I ellipsometry spectra.

External collaborators are not required. Public full texts, author manuscripts, supplements, permitted source data, auditable digitization, and reproducible computation remain the primary strategy.

## Static and finite-temperature first-principles boundary

The selected-band CdTe static post-processing result remains independently reproducible on the same immutable physical artifact. It is a mathematical and software component, not a converged HgCdTe material prediction.

The present CdTe polar response remains unsuitable for production AHC. New AHC, SQS, CPA, SCBA, or broad alloy calculations require:

- a decision-changing observable;
- a published validation target;
- a predeclared termination criterion;
- and evidence that the lower-cost observation model cannot resolve the decision.

## Authorized next work

1. open and validate the flagship analytical-core PR;
2. implement `scripts/build_distributional_band_edge_manuscript_assets.py` from `figure_manifest.json`;
3. execute the DOI acquisition queue and audit retrieved sources;
4. complete one external validation route or explicitly authorize theorem/methods-only submission;
5. generate final figures and tables from immutable data;
6. verify the complete bibliography and prior-art boundary;
7. package archive DOI, authorship, declarations, and journal submission files.

## Explicitly unauthorized

- reopening unconstrained empirical gap fitting;
- merging Paper I and the flagship manuscript as if they were one study;
- selecting one optical edge without an observation-operator declaration;
- identifying `sigma_x`, `sigma_G`, Herrmann `s`, Urbach energy, PL FWHM, and quasiparticle linewidth as equivalent;
- treating local gap-sign probability as a bulk topological invariant;
- reporting conditional transition moments without crossing probability;
- treating high log-linear `R^2` as proof of one tail mechanism;
- treating detector cutoff as a direct material gap;
- treating physical film thickness as effective absorbing thickness without validation;
- transferring Chang `b` or Dingrong carrier corrections between specimens without provenance;
- conflating Burstein–Moss filling with band-gap renormalization;
- treating the generic carrier marker as the Dingrong free-carrier law;
- assigning synthetic parameters to real specimens;
- claiming dense sampling removes exact forward-model invariances;
- requiring real collaborators before progress can continue;
- escalating to expensive first-principles or atomistic work without a decision-changing validation target.