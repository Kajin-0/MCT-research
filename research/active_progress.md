# Active research progress

**Last updated:** 2026-07-20  
**Controlling ref:** `main`

Detailed results live in `research/decision_records/` and `validation/*_reference_result.json`. This file records the program-level decisions that control new work.

## Controlling scientific state

- Static CdTe extraction uses the isospectral selected-band polar Hamiltonian. The complete linear space has four directions; the complete quadratic space has ten established Weiler directions.
- The conventional tied quadratic model fails matrix and spectral closure. Five established departure directions are sufficient at the declared gate; `N2` is negligible. The former `49%`, large-`N2`, all-six-required, and 120-band interpretation is superseded.
- An independent post-processing implementation on the immutable physical artifact reproduces the selected-band isospectral construction, the 4D linear and 10D quadratic invariant spaces, and the conventional quadratic failure on an untouched `[110]` holdout.
- This independent reproduction uses direct SVD polar transport and a separately implemented raw-symmetry projector. It is not a new electronic-structure calculation and does not establish PBE, pseudopotential, geometry, cutoff, or band-count convergence.
- The static post-processing reproducibility question is closed. Additional static replication on the same physical artifact is unauthorized; a genuinely independent electronic-structure setup would require separate scientific justification and authorization.
- The CdTe A0 point remains invalid for long-range polar response. Further threshold tightening and A1 execution are unauthorized.
- Finite-temperature matrix, Fan-vertex, and special-displacement reconstruction methods pass synthetic oracles, but no audited backend closes all SOC, Debye-Waller, polar, gauge, and export requirements.

## Independent static CdTe reproduction

The independent SVD-polar path reproduces:

```text
minimum selected overlap singular value       0.9998015324
maximum selected eigenvalue error              2.576e-14 eV
complete linear invariant dimension            4
complete quadratic invariant dimension         10
complete linear training residual              1.523e-7
complete linear [110] holdout residual          1.447e-7
complete quadratic training residual           1.255e-5
complete quadratic [110] holdout residual       7.956e-6
conventional quadratic training residual       0.287044
conventional quadratic [110] holdout residual   0.332112
P8                                              6.772222 eV A
P7                                              6.201826 eV A
```

The `[110]` direction is excluded from training. Coarse/fine/Richardson variation is `1.42e-4` for `P8` and `1.17e-4` for `P7`. Scalar differences from the controlling implementation are no larger than `1.88e-11` for residual diagnostics and `2.83e-13 eV A` for the two linear couplings.

Authorized conclusion: the controlling static post-processing result is independently reproducible on the same immutable physical input. Unauthorized conclusion: that the underlying physical calculation or fitted material parameters are independently validated.

## Matrix covariance and regenerated statistics

- Hermitian `8x8` Hamiltonians use 64 orthonormal real coordinates; general complex dynamical operators retain 128.
- Dataset schema `2.0` stores covariance dimension `0`, `64`, or `128`; schema `1.0` remains readable through explicit migration.
- Old-versus-new regeneration confirms fitted parameters and Frobenius SSE are unchanged to numerical precision.
- For six matrices and eight parameters, residual degrees of freedom change from `760` to `376`; variance-scaled standard errors increase by `1.4217160742`.
- No committed physical static record contains calibrated Hamiltonian covariance statistics requiring numerical replacement.

## HgCdTe gap program

The previously leading provisional temperature law is retained as an archived candidate:

```text
Eg(x,T) = Eg_Hansen(x,0) + 5.918273117836612e-4
          * (1-2*x) * T^3 / (T^2 + 18.059294367159467^2)
```

It is a constrained Seiler-family parameterization, not a new functional family or production equation.

- Chu 1991 provides an independent `x=0.276`, 6-300 K absorption-turning-point series. The observed same-specimen shift is `61 meV`; Hansen predicts `70.466 meV` and the provisional Padé law predicts `79.096 meV`.
- Anchored thermal-increment MAE is `7.215 meV` for Hansen and `11.725 meV` for the provisional Padé law. Across the conservative `x=0.276 +/- 0.005` interval, the minimum Padé MAE (`10.829 meV`) exceeds the maximum Hansen MAE (`8.011 meV`).
- The provisional Padé law therefore does not retain its previously claimed broad cross-source transfer advantage. It must not be described as the leading candidate without this qualification.
- The Chu 1991 eight-specimen 300 K composition series separates absolute turning-point agreement from composition shape. Raw non-circular MAE favors Schmit-Stelzer (`8.579 meV`), while leave-one-specimen-out transfer of one source-class offset favors Seiler (`4.186 meV`) and Hansen (`4.277 meV`).
- Seiler and Hansen differ by only `0.091 meV` in offset-transfer MAE and are not distinguishable. The provisional Padé value is `7.479 meV`.
- Across a shared `delta_x = +/-0.005` composition-bias sweep, the minimum Padé offset-transfer MAE (`7.424 meV`) exceeds the maximum Hansen MAE (`4.320 meV`) by `3.104 meV`.
- These Chu results do not select Hansen, Seiler, or another universal law because the source reports absorption turning points, printed figure labels, incomplete specimen-state metadata, and a circular Chu-equation lineage.
- No replacement for Hansen's zero-temperature composition polynomial is authorized.
- No production absorption-edge correction is authorized.

## Paired HgCdTe acquisition protocol

The audit-grade acquisition target is now frozen as an executable collaboration contract:

```text
2 measured composition levels
x 2 achieved carrier-density levels
x 2 achieved vacancy-proxy levels
= 8 physical specimens

8 specimens x 2 paired modalities x 2 temperature blocks
= 32 primary gap observations
```

The same physical specimens and co-registered areas receive magneto-optical and absorption measurements at target `6 K` and `300 K`. Nominal low/high labels are planning metadata only; analysis covariates are calculated from measured continuous composition, carrier-density, and vacancy-proxy values.

For each temperature block, the balanced planning design gives:

```text
observation count             16
parameter count               5
design rank                   5
residual degrees of freedom   11
condition number              2.6180339887
maximum leverage              0.4375
carrier-vacancy correlation   0.0
```

The completed-package gates require:

```text
composition sigma_x target             <= 0.0010
composition sigma_x hard maximum       <= 0.0015
carrier low/high separation            >= 3 combined sigma
vacancy low/high separation            >= 3 combined sigma
abs(carrier-vacancy correlation)       <= 0.5
one carrier polarity per core block    required
processing between paired modalities   forbidden
pre/post state drift                    <= predeclared limit
technical replicates                    target 3, hard minimum 2
co-registered paired measurement area  required
```

Every observation must preserve native raw-data identity, calibration, sample temperature and uncertainty, extraction method, software commit, covariance, and analysis-record provenance. Witness-coupon state assignment requires an explicit witness ID and quantified transfer uncertainty.

Authorized conclusion: the repository now contains a collaboration-ready method for acquiring observation-class-controlled evidence under an identifiable local five-parameter model. Unauthorized conclusion: that this model is physically complete, that one vacancy observable is universal, that one absorption edge is corrected, or that the eight-specimen single-lineage core establishes external transfer.

## Primary evidence state

The centralized recovery ledger contains:

```text
all sources                         9
primary sources                     8
authorized primary fit sources      0
conditional primary sources         2
blocked primary sources             6
screen-only sources                 1
```

Conditional primary sources are Seiler 1990 and Orlita 2014.

Orlita 2014 adds a carrier-coupled near-critical constraint at approximately `1.8 K`: a graded plateau near `x approximately 0.17`, a low-field model improved by `Eg=4 meV`, `EF approximately 15-17 meV`, and `n approximately (2-3)e14 cm^-3`.

At nominal `x=0.17`, Laurenti is the closest local comparator, but model-equivalent composition offsets span from `+0.000573` to `-0.006608`. The record is composition-sensitive, carrier-coupled, and not an exact homogeneous calibration point.

Orlita and Teppe share the Mikhailov/Dvoretskii MBE and magneto-optical lineage. They are not independent cross-laboratory validation sets. The static-law reopening gate remains closed.

### Guldner-Weiler 1977 primary magneto-optical core

- The recovered Guldner Part I/II papers contribute seven exact 4.2 K composition/interaction-gap anchors from primary text or captions: `x=0.025/-261 meV`, `0.050/-207`, `0.115/-90`, `0.150/-30`, `0.185/+35`, `0.250/+161`, and `0.280/+208`. The complete Figure 11 trend remains figure-only.
- Guldner reports density and electron-microprobe composition methods and a zero-gap crossing `x0=0.165+/-0.005`, but no specimen-level `sigma_x` for the individual anchors. The interaction gaps remain Pidgeon-Brown/VCA model-conditioned observations.
- Weiler reports approximately `3 meV` fitted-gap uncertainty for ten magnetoreflectance specimens at 24 and 91 K, while composition uncertainty is `0.005-0.015`. Its own `dEg/dx=1.88-0.001*T` relation propagates this to `8.945-27.840 meV`, so composition uncertainty dominates the nominal gap-fit precision.
- Weiler also reports an interband/intraband discrepancy up to about `4 meV` near `60 kG`; Guldner parameters better describe the intraband result but fit Weiler interband data more poorly. This is retained as observable/model-class dependence, not as a universal correction.
- Independent-laboratory qualitative comparison is authorized. Few-meV cross-laboratory ranking, default pooling, trend-point digitization, and universal material-law fitting remain blocked.

## Absorption-edge uncertainty contract

- Every absorption-derived edge record must preserve source calibration, modality, temperature, thickness, composition provenance, carrier state, tail treatment, fit window, search bounds, model definitions, thresholds, and the raw spectrum.
- The exporter returns all valid candidates, exclusions, separate model/threshold envelopes, a combined envelope, and the SHA-256 of the complete input assumptions.
- The candidate ensemble includes fractional-power models and fixed thresholds. The prior-art Chu 1994 Kane-region model may be enabled within `0.170 <= x <= 0.443` and `77 <= T <= 300 K`.
- The Chang 2006 nonparabolic-Urbach operator may be enabled only within `0.21 <= x <= 0.23`, `77 <= T <= 80 K`, and `-0.020 <= E-Eg <= 0.300 eV`. It requires explicit provenance-bound `W` and `b`, continuity normalization at `E0=Eg+W/2`, and separate tail/intrinsic branch coverage.
- The Chang candidate is an observation-model sensitivity operator, not a material-gap law. Free joint fitting of `W`, `b`, and `Eg` is not authorized in the current tranche.
- Chang 2006 Figure 2 is not authorized as a quantitative operator validation dataset: the caption reports `80 K` while the body reports `77 K`, native numerical data and calibration are absent, and same-specimen `W` and `b` are not tabulated. The reported `b=103+/-2 meV` belongs to a separate `x=0.23`, `77 K` calculation and cannot be transferred as exact for the `x=0.21` figure.
- A declared synthetic Figure-2-like screen, with a `0.002 eV` upper source-domain margin, gives a weighted Jacobian condition number of `256.1`, `corr(Eg,ln W)=0.731`, and `corr(Eg,ln b)=0.801`. Fixed `W` errors of `+/-10-20%` move the recovered edge by approximately `0.8-1.7 meV` while retaining visually small residuals. These are sensitivity diagnostics, not real-specimen uncertainties.
- Finkman-Schacham 1984 is preserved as a source-bound operational-edge operator for `0.205 <= x <= 0.29`, `80 <= T <= 300 K`, and `20 <= alpha <= 1000 cm^-1`. Its source-labeled `Eg` is explicitly the `alpha=500 cm^-1` crossing selected to approximate the half-peak response of a 10 um photoconductive detector; it is not an identified latent gap.
- Across representative Hg-rich points, the `alpha=20` to `1000 cm^-1` edge span is `15.0-37.6 meV`. For a 500 um specimen, the transmission zero-intercept edge is about `20-21 meV` below the alpha-500 edge at 300 K. Eq. (13) uses cut-on wavenumber `Zi`, not absorption `e/d`; those coordinates are not interchangeable.
- Mroczkowski et al. 1983 provides publisher-abstract evidence at fixed nominal `x=0.3` that Hg-vacancy acceptor state changes the p-type exponential absorption-tail slope: `k=148 eV^-1` in high-purity material and `105 eV^-1` near `2e16 cm^-3` acceptors. The corresponding e-fold energy increases from `6.757` to `9.524 meV`, or `40.95%`.
- This source strengthens the paired protocol requirement for an achieved vacancy-state covariate. Full operator implementation, same-specimen causality, uncertainty-weighted fitting, latent-gap correction, and a universal vacancy coefficient remain blocked until the primary full text and complete specimen metadata are recovered.
- Yue et al. 2006 adds an exact five-specimen, `11-300 K` processing-conditioned anomaly table. Four samples show extrapolated `deltaE=9.7-11.3 meV`; the `240 C/24 h` Hg-vapor M17 condition alone is monotonic with `deltaE=0`. The source treats this anneal as optimized for removing Hg vacancies.
- The Yue compositions are inferred from the `11 K` absorption spectrum and are circular for material-law validation. Thick bulk and thin MBE specimens use different critical-point operators; carrier densities are reported at `77 K` and `300 K`, respectively. The result supports a conditional processing control, not direct vacancy metrology, same-specimen causality, or a universal approximately `10 meV` correction.
- The recovered Herrmann 1992/1993 chain does not define a complete executable model: the high-energy Anderson branch, explicit band-filling factors, carrier-density/quasi-Fermi mapping, and Kane parameter conventions remain external. Hybrid implementation is blocked.
- Herrmann 1993 Table I is preserved only as an eight-row secondary model-validation comparison. Its transition-offset MAE is `2.35 meV` with a maximum absolute error of `8.4 meV`; its transition-absorption comparison spans a maximum factor error of `2.865`. The table is not independent gap fit evidence.
- The exporter never selects a recommended or corrected material gap.
- Deterministic seven-candidate example: combined span `19.95223 meV`, model-family span `9.14375 meV`, threshold span `9.95726 meV`, and half-range `9.97612 meV`. This example remains unchanged because the new candidate is disabled by default.
- Research uncertainty export is authorized. Production correction and single-edge selection remain forbidden.

## Completed manuscript milestone

PR #131 merged the submission-oriented manuscript:

> **Observation-model uncertainty and identifiability in HgCdTe band-gap extraction.**

Two Moazzami 2005 solid-IRSE traces pass the complete contract:

```text
x=0.226, T=300 K, d=15.40 um, 125 derived points
x=0.310, T=300 K, d=4.95 um, 115 derived points
```

- Fractional/Chu fitted-model spans are `6.414 meV` and `6.830 meV`.
- Coordinate perturbation moves every fitted-model edge by less than `0.891 meV`.
- Fixed thresholds through `4000 cm^-1` remain below the declared `5 meV` coordinate-sensitivity gate.
- The `5000 cm^-1` crossing for `x=0.310` shifts by `5.694 meV` and is excluded from precision claims.
- Operational threshold choice changes the nominal closest material comparator. No threshold is identified with the latent gap.
- Published Seiler 1990 is nominally closest for every fractional/Chu fitted edge, but its advantage over Hansen is only `0.177-0.255 meV`.
- Because specimen-level composition uncertainty is unreported and both spectra come from one study, the Seiler-Hansen ordering is descriptive only. Strict material-law ranking is not authorized.

Issue #129 is complete. Journal submission and author declarations are external administrative actions rather than active research-development work.

## Active research track

Issue #132 is complete under its non-identifiability stop rules. The historical evidence program established that composition uncertainty, observation definition, source lineage, carrier state, vacancy state, and model conditioning dominate the sub-meV empirical-law ordering. No universal HgCdTe gap law or production edge correction is identified.

Issue #141 and PR #142 provide the controlling paired acquisition contract:

> **Acquire co-registered magneto-optical and absorption evidence with independent composition, carrier-state, and vacancy-state measurements.**

Historical-source accumulation is closed. New work must secure protocol-compliant paired evidence or recover a native primary dataset whose information gain exceeds the current composition and observation-model uncertainty scales.

## Authorized next work

1. Use the paired protocol as the external collaboration handoff and obtain a documented feasibility review from candidate material, composition, Hall/defect, absorption, and magneto-optical partners.
2. Build a pre-screening pool large enough to achieve two separated carrier levels and two separated vacancy-proxy levels without changing carrier polarity or exceeding the carrier-vacancy correlation gate.
3. Recover native Chang 2006 Figure 2 absorption data, calibration, resolved temperature, and same-specimen `W` and `b` provenance before any quantitative operator validation or gap inference.
4. Prioritize existing paired or same-specimen cross-modality evidence only when specimen lineage, measured composition, carrier state, vacancy proxy, temperature, and extraction provenance are recoverable.
5. The Herrmann implementation path is blocked until Anderson 1977/1980, the full 1992 precursor, explicit `BFF_lh`/`BFF_hh`, carrier-density to quasi-Fermi mapping, and composition-dependent Kane conventions are recovered and jointly audited.
6. Reopen material-law development only after independent observation-class-controlled evidence exceeds propagated composition and measurement uncertainty and remains stable under leave-one-specimen-out analysis.

## Explicitly unauthorized

- treating Orlita as an exact homogeneous point or independent cross-laboratory validation;
- treating old redundant Hamiltonian degrees of freedom or variance-scaled standard errors as current;
- additional empirical gap coefficients from current or uncalibrated data;
- universal source, composition, carrier, defect, threshold, or model-family corrections from current metadata;
- treating a fitted Chu source offset as transferable outside that source and observation class;
- treating nominal processing labels as achieved carrier or vacancy covariates;
- substituting different specimens or unregistered measurement areas for the paired observations;
- irreversible processing between paired modalities;
- relaxing state-separation, correlation, composition-uncertainty, provenance, or drift gates after inspecting results;
- claiming the local five-parameter protocol model is physically complete or externally transferable before holdout evidence;
- additional static post-processing replication on the same physical artifact;
- claiming static electronic-structure convergence from the independent post-processing result;
- single-edge selection from the uncertainty ensemble;
- quantitative gap inference or operator validation from Chang 2006 Figure 2 without native data, resolved temperature, and same-specimen `W` and `b`;
- transferring the reported `x=0.23` Chang value of `b` as an exact input for the `x=0.21` Figure 2 specimen;
- broad source accumulation without a decision-changing target;
- additional micro-PRs that only restate an unchanged authorization boundary;
- A1 execution, further response-threshold tightening, 120-band static reruns, alloy production work, or unsupported novelty claims.
