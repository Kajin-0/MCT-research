# R04/R05 matched spatial-covariance and spectroscopy evidence specification

**Controlling issue:** #395  
**Programs:** R04 primary; R05 dependent  
**Specification version:** `r04_r05_matched_evidence_v1`  
**Evidence state:** specification only; no qualifying specimen dataset is claimed

## 1. Purpose

This specification defines the minimum evidence package required to test whether a real near-critical HgCdTe specimen occupies a regime where the R05 matched correlated-random-mass benchmark could be experimentally distinguishable from the matched scalar local-gap mixture.

The controlling dimensionless parameters are

\[
g=\frac{\sigma_M\xi}{\hbar v_K},
\qquad
m=\frac{\overline M\xi}{\hbar v_K},
\qquad
M=\frac{E_g}{2}.
\]

R05 Phase 0 found that the declared synthetic effect threshold is bracketed by

\[
0.25<g_{\rm threshold}<0.30
\]

near zero mean mass for the frozen one-dimensional model and measurement convention. This bracket is a method-benchmark result, not a universal critical coupling or a measured HgCdTe threshold.

## 2. Decision contract

A dataset is decision capable only if it supports all of the following:

1. a local mass or composition variance with uncertainty;
2. an identifiable material correlation length after the complete spatial measurement kernel is applied;
3. a justified same-specimen or exchangeable-population link between spatial and spectroscopic observations;
4. a signed mean gap sufficiently near the R05 massless regime;
5. a measured spectroscopy resolution kernel;
6. a matched correlated-versus-scalar model comparison using the same one-point mass distribution;
7. uncertainty propagation that includes statistical and systematic components;
8. a result that would change whether a higher-dimensional or full-Kane calculation is warranted.

A code or document passing this schema does not imply that these scientific gates pass. It establishes only that the required fields and evidence classifications are present.

## 3. Evidence classes

Every quantitative input must carry one of these evidence classes:

- `measured_raw`: directly recorded instrument output with calibration metadata;
- `measured_derived`: derived from measured data through a documented transform;
- `source_established`: taken from a source that explicitly supports the quantity and specimen class;
- `empirical_model`: produced by an identified empirical relation with propagated uncertainty;
- `exploratory_assumption`: used only for design or sensitivity analysis;
- `unresolved`: required but not currently available.

`exploratory_assumption` and `unresolved` values cannot satisfy a material reopening gate.

## 4. Specimen identity and exchangeability

The record must include:

- persistent specimen identifier;
- source, growth method, substrate, crystallographic orientation, layer structure, and thickness;
- nominal composition and the method used to establish it;
- measurement temperature and relevant thermal history;
- conductivity type, carrier density, mobility, and surface/contact state when available;
- spatial-map specimen region and spectroscopy specimen region;
- one of `same_region`, `same_specimen_different_region`, `adjacent_lamella`, `same_growth_run`, or `unlinked`;
- a quantitative exchangeability argument whenever the relationship is not `same_region`.

A same-growth-run assertion by itself is not a quantitative exchangeability argument.

## 5. Spatial field record

### 5.1 Preferred latent quantities

Preference order:

1. signed mass map `M(x,y)`;
2. signed-gap map `Eg(x,y)` with `M=Eg/2`;
3. composition map `x(x,y)` with a temperature-specific gap model and uncertainty propagation;
4. a proxy field only when its forward relation to composition or gap is calibrated.

Wafer-average composition tolerance, nominal growth uniformity, or a manufacturer specification must not be encoded as a local fluctuation standard deviation.

### 5.2 Required raw geometry and transfer information

- coordinate system and units;
- map dimensions in pixels and physical length;
- pixel or scan-bin integration footprint;
- measured or calibrated point-spread function, modulation transfer function, or equivalent transfer description;
- depth weighting or lamella thickness where applicable;
- sample-center coordinates;
- missing-data mask;
- preprocessing history;
- noise and calibration covariance;
- repeated maps or independent regions where available.

Nominal pixel pitch is not a substitute for the point-spread function.

### 5.3 Required covariance inference

The analysis must report:

- local point-variance posterior or interval;
- filtered-variance likelihood;
- covariance function or power spectral density;
- correlation-length posterior or interval;
- identifiable spatial-frequency band;
- finite-window correction;
- pixel/PSF/depth-kernel correction;
- covariance-family sensitivity using at least Gaussian and one Matérn family;
- within-map effective information and cross-scale covariance when applicable.

The target acquisition band is approximately `10–500 nm` where technically possible. The interval is a design target and not an assumed prior support for the material correlation length.

## 6. Spectroscopy record

### 6.1 Preferred observable

The preferred initial observable is local tunneling DOS from cryogenic STS because it can provide spatially resolved low-energy spectra. This preference is conditional: HgCdTe surface preparation, tip-induced band bending, surface states, pits, charging, and contact-induced broadening must be included as explicit systematic risks.

Alternative observables may be admitted only with a forward model showing that the correlated model and matched scalar null remain distinguishable after the modality-specific kernel is applied.

### 6.2 Required fields

- raw energy or bias axis;
- conductance or other observable and normalization convention;
- sample and effective electronic temperature;
- lock-in modulation amplitude and waveform, if used;
- measured effective energy-resolution kernel;
- tip or contact state;
- surface preparation and elapsed vacuum exposure;
- background model and fit range;
- spatial coordinates of spectra;
- repeated spectra and drift diagnostics;
- band-bending, charging, and surface-state assessment;
- calibration uncertainty and covariance.

The `1–2 meV` decision-scale resolution appearing in the R05 exploratory `sigma_x=0.002` mapping is not universal. It may be entered only as `exploratory_assumption` until replaced by a measured kernel and specimen-supported parameter mapping.

## 7. Joint inference

The joint record must predeclare:

- the one-point mass distribution used by both models;
- the spatial covariance family or model average;
- the conversion chain from measured field to `M`;
- priors for `Mbar`, `sigma_M`, and `xi`;
- the frozen value of `m_max` used for the near-critical gate;
- the spectroscopy forward kernel;
- likelihood definitions for the correlated and scalar models;
- treatment of nuisance backgrounds and calibration covariance;
- posterior predictive checks;
- sensitivity variants and exclusion criteria.

Primary reported quantities:

\[
P(g>0.25\mid D),
\qquad
P(|m|<m_{\max}\mid D),
\]

plus the convolved effect statistic and uncertainty under both models.

The value of `m_max` must be frozen before inspecting the final model-comparison statistic. It should be justified from the R05 detuning screen, not selected to improve the result.

## 8. Gate vocabulary

Each gate is one of:

- `PASS`;
- `FAIL`;
- `UNRESOLVED`;
- `NOT_APPLICABLE`.

Required gates:

- `local_variance_gate`;
- `correlation_length_gate`;
- `same_population_gate`;
- `near_critical_gate`;
- `resolution_gate`;
- `matched_null_gate`;
- `robustness_gate`;
- `decision_changing_gate`.

`R05_REACTIVATION_RECOMMENDED` is permitted only when every required gate is `PASS` and every gate-satisfying quantitative input is stronger than `exploratory_assumption`.

## 9. Stop rules

Stop and return `EVIDENCE_GATE_FAILED` or `EXTERNAL_DATA_BLOCKED` when any of the following is decisive:

- no local covariance data exist;
- the spatial transfer band cannot identify `xi`;
- spatial and spectroscopy records cannot be linked to the same specimen population;
- the gap-sign or mass conversion is unavailable;
- spectroscopy resolution removes the predicted effect;
- systematic uncertainty dominates the correlated-versus-scalar difference;
- the scalar null and correlated model are statistically indistinguishable;
- only macroscopic composition tolerance is available.

No larger R05 simulation is authorized merely to compensate for missing evidence.

## 10. Machine-readable records

The normative schema is

```text
data/schemas/r04_r05_matched_evidence_v1.json
```

A nonclaiming template is

```text
data/templates/r04_r05_matched_evidence_template.json
```

Repository validation is implemented in

```text
src/mct_research/r04_r05_evidence.py
```

and tested by

```text
tests/test_r04_r05_evidence.py
```

## 11. Claim boundaries

This specification does not establish:

- a measured random-mass field;
- a specimen-specific correlation length;
- a universal covariance family;
- topology, domain-wall transport, percolation, or mobility edges;
- specimen exchangeability without evidence;
- material validation from synthetic recovery;
- a new HgCdTe physical law;
- manuscript authorization.
