# R07 decision memo: pre-existing physical evidence does not close inversion

**Date:** 2026-10-11. **Contribution:** R07 only.
**Decision:** `MISSING_QUALIFIED_PHYSICAL_EVIDENCE — STOP`.
This independent evidence-acquisition investigation is complete at that decision;
the older analytical goal remains blocked and unresolved. This memo supplies
neither a physical zero-temperature composition prediction nor a new alloy
coefficient. The accompanying [matrix](source_evidence_matrix.md) gives precise
DOIs, primary links, inspected locations, input lineage and source-specific
limits; [sources.json](sources.json) pins retrieved binaries and inherited audits.

## 1. What would count as certification?

Fix the target: a bulk, nonmagnetic, declared lattice/strain and disorder ensemble,
with physical projectors continuously identifying one Γ6 doublet and one Γ8
quartet. A signed ordering gap is distinct from the positive excitation gap of a
semiconductor, a spectral maximum, a mobility edge and a topological invariant.
Composition means the Cd cation fraction, measured independently of an optical
gap law. Common energy references may be shifted together; assigning unrelated
zeros to separately computed operators does not supply a physical alignment.

R07's static zero-temperature Hamiltonian holds nuclei fixed. An experimental
physical zero-temperature quasiparticle observable also includes zero-point
motion and any residual many-body effects. The target must explicitly select
one, or bound their difference. A 2–4.2 K observation is not an exact 0 K input;
an empirical temperature equation is not an independent correction certificate.
This distinction adds no thermal calculation to the present scope.

For the static ensemble representation used in the existing theorem, write

```text
gα(z,x) = [z − eα(x) − Kα(z,x)]⁻¹,  α = 6,8,
Kα(z,x) = ∫ dνα(t;x)/(z−t),  να ≥ 0,
Dα = z−eα−Kα,
Fs = (D6+D8)/2,  M = (D8−D6)/2,
Fs(Ebar(x),x)=0,  μ(x)=M(Ebar(x),x).
```

The exact augmented-space K is the kernel of the configuration-averaged
resolvent. It is neither a single-impurity T, an average of individual Feshbach
kernels, nor automatically an interacting GW self-energy. In the latter case a
causal Dyson representation, reference and applicable hypotheses must first be
matched. A static hybrid potential called a self-energy correction is not by
that name a measured complex, frequency-dependent quasiparticle self-energy.

The [threshold-causal theorem T5–T7](../threshold_causal_2026-10-11/derivation.md)
requires the following inputs **for the same physical observable and ensemble**:

| Gate | Minimum qualified information | Audit decision |
|---|---|---|
| D: common support-free domain and existence | Continuous real segments Jx over a declared interior composition interval I; interiors disjoint from both supp να; finite one-sided threshold values where needed; opposite Fs boundary signs with error margins; true and approximate common roots lie in Jx | Not supplied |
| B: interior mass bracket | At two interior x values, opposite μ signs with margins exceeding uniform branch residual errors; or the T17 opposite D6/D8 sign patterns at certified trial energies in Jx | Finite-temperature, model-conditioned ordering signs exist; qualified μ/D signs on D do not |
| S: lower composition secant modulus | μ(x2)−μ(x1) ≥ m(x2−x1), m>0, for **every** x1<x2 in I, or a certified non-linear lower modulus | Not supplied |
| U: physical error budget | Uniform branch-denominator residual bounds ε6,ε8 including microscopic/model, composition, strain, projection/window, continuum and zero-temperature interpretation errors | Not supplied |

On D, positivity gives nonnegative finite energy secants bα and

```text
rsec = (b8−b6)/(2+b6+b8),  |rsec|<1,
|μ−μapp| ≤ max(ε6,ε8),
|xc−xc,app| ≤ max(ε6,ε8)/m       [D+B+S+U].
```

B and continuity alone establish existence of at least one root in a bracket,
not uniqueness or a linear error bound. D is a condition on eliminated
**weighted kernel support**, not merely the band gap or weak plotted spectral
broadening. A finite-broadening calculation, finite-resolution null signal,
DOS gap, or finite list of eigenvalues does not prove D. Roots at a merging
threshold can lose the finite boundary margins or simple-pole interpretation.
It is permissible that no useful physical D exists near an inverted continuum;
the outcome here is absence of certification, not an assertion that D must exist.

## 2. What the primary sources actually make available

The strongest candidates are kept, with their different evidence classes:

- **Published static alloy states and weights:** Nicklas–Wilkins HSE,
  Rubel et al. unfolding, and Chen et al. dielectric-dependent hybrid calculations.
  Calculated composition samples and effective bands supply material precedent.
  None of the inspected papers supplies a uniform physical branch residual or
  the projected support/domain and all-pairs composition modulus required above.
  [Primary HSE](https://doi.org/10.1103/PhysRevB.84.121308),
  [unfolding](https://doi.org/10.1103/PhysRevB.90.115202),
  [dielectric-dependent hybrid](https://doi.org/10.1063/5.0187006).
- **Actual disorder propagators in approximations:** Hass et al. provide
  tight-binding CPA spectral densities and self-energy corrections; Krishtopenko
  et al. give explicit matrix Green functions, SCBA disorder kernels and spectral
  functions. These are substantial prior art. Their physical-input and
  approximation-error limitations are specified in matrix rows P01 and P05;
  they are not exact alloy-kernel certificates.
  [CPA](https://doi.org/10.1103/PhysRevB.27.1088),
  [SCBA](https://doi.org/10.1103/PhysRevB.106.115203).
- **Quasiparticle many-body calculations:** Svane et al., Sakuma et al. and
  Fleszar–Hanke establish GW-based binary electronic-structure work. Binary
  quasiparticle calculations do not determine a composition-resolved alloy
  disorder self-energy. Their distinctions are retained in P07–P09.
  [QSGW](https://doi.org/10.1103/PhysRevB.84.205205),
  [spin-dependent GW](https://doi.org/10.1103/PhysRevB.84.085144),
  [earlier GW](https://doi.org/10.1103/PhysRevB.71.045207).
- **Independent observation:** binary magnetoreflection and photoemission
  establish inverted HgTe ordering, while historical alloy magneto-optics and
  modern Kane spectroscopy provide finite-temperature signed ordering evidence.
  Observation of inversion is not evidence for the complete D+B+S+U package.
  P10–P15 separate laboratories, fitted lineages, carrier states and metrology.
  [Binary magnetoreflection](https://doi.org/10.1103/PhysRev.161.779),
  [binary photoemission](https://doi.org/10.1103/PhysRevB.61.R5058),
  [modern alloy experiment](https://doi.org/10.1038/ncomms12576).

**Input independence is not equivalent to absence of all empirical information.**
Measured composition, lattice constants, dielectric response and raw photon/field
energies are admissible independent physical inputs when their uncertainties and
state are retained. An empirical nongap dielectric x relation is distinct from
an empirical alloy-gap x relation, but still needs its own provenance and errors.
Binary-fitted tight-binding constants are approximate operator inputs, not
absolute self-consistent alloy potentials. Standard HSE or mBJ is an approximation,
not a bounded exact Hamiltonian even when no HgCdTe gap coefficient is tuned.

In particular, the HSE crossover is obtained from a cubic fit to **calculated**
gaps at endpoints and x=0.25,0.50,0.75. That is distinct from fitting the operator
to measured alloy gaps, but it still cannot certify an unsampled interior mass
or remainder. The 2022 SCBA baseline traces through its Ref. 8 to an explicitly
empirical Laurenti gap relationship; using its mass table as independent absolute
input would import the barred alloy-gap law. Chen's dielectric/lattice inputs
are nongap empirical relationships, and its comparison with Hansen is validation,
not evidence that its DD-CAM parameters were fitted to Hansen. These distinctions
prevent both false acceptance and false accusations of circular fitting.

The current-date primary search also located a 2026 shell DFT correction paper,
[DOI 10.1016/j.cocom.2026.e01374](https://www.sciencedirect.com/science/article/pii/S2352214326001711).
The accessible abstract/introduction and results snippet identify an adjustable
parameter capable of reproducing an experimental gap, but do not expose the
complete calibration of its composition rule or an independent error bound.
Its use is quarantined as
`UNVERIFIED_INPUT_LINEAGE`; no parameter is imported. Missing full text is an
access limitation, not proof of how every parameter was obtained. A 2025
[composition-tuned quantum-well experiment](https://doi.org/10.1103/PhysRevMaterials.9.054602)
is also retained as P23, with its confinement and CdTe strain qualifications.
Its Appendix fits a bulk-gap cubic constrained to Laurenti; that relationship
is excluded as a coefficient or modulus input. Its subband phase diagram is
not the requested bulk physical certificate.

## 3. Existing project evidence, including negative results

The [inventory](local_evidence_inventory.json) hashes every tracked text,
JSON, CSV and source record in the local literature and numerical/evidence
corpora named there, and records
scope metadata for all frozen R07 calculation JSON. This is corpus triage plus
focused scientific review, not a claim to have rederived every unrelated program
result. All R07 result memos, both analytical packages, their audits and the
relevant empirical-source/observable audits were reviewed. No numerical data are
regenerated. The completed-reference record's 23 external hashes are inherited,
not claimed as a fresh native-wavefunction extraction.

| Existing evidence | Retained scientific consequence |
|---|---|
| [Bare-vertex audit](../result_2026-10-10.md) and [direct-alloy follow-up](../result_2026-10-10_self_consistency.md) | Quarter-share binary-derived Te substitution remains rejected as a physical predictor. Frozen n=8/12 spectra give −138 meV near x=0.18 and a peak meeting near x=0.30; these are model diagnostics, not physical material values. Exact resummation did not repair this vertex. |
| [HSE host gate](../result_2026-10-10_hybrid_gate.md), [projected-frame failure](../result_2026-10-10_projected_host.md), [repair/control ledger](../result_2026-10-11.md) | Potential-set sensitivity, incomplete projected spaces, coarse exchange quartet failure, orbital-frame mismatch and finite-window limits remain explicit. Zero-substitution and transport controls test infrastructure, not a physical impurity response. |
| [Completed-reference review](../result_2026-10-11_completed_reference_review.md) | Numerically accepted HgTe f360/f120 references differ by 6.7014 μeV in Γ gap; the pointwise Γ kernel comparison is 4.2058 μeV at Im z=25 meV. Neither is ε for a physical real-energy alloy. No accepted alloy impurity amplitude or interior μ is supplied. |
| [I1/I3/I5/I6 identifiability results](../analytical_first_2026-10-11/identifiability.md) | Fixed local mixed interactions can hide from finite endpoint data; coherent-invisible directional/SOC response can alter Γ8; positive equal finite moments need not identify roots; full-support fixed-interaction Bernoulli support is composition independent under its stated assumptions. The last result concerns operator support and does not by itself prove a chosen projected measure fills a particular energy window. |
| [Threshold negative results](../threshold_causal_2026-10-11/cycles_and_boundary.md) | Finite T does not guarantee finite T′; p=1 defeats a finite regular slope; a positive bath defeats the continuum contraction; cubic tangency defeats a universal linear root bound; equal IR channels and regular moments still permit distinct roots. |
| [Reference/threshold rules](../../../../docs/derivations/impurity_reference_and_threshold.md), [volume path](../../../../docs/derivations/endpoint_volume_path.md), [continuum rule](../../../../docs/derivations/continuum_prescription_and_crossing.md) | Subtract coherent contrast once; embedded g′≠−g² generally; fixed-volume and homogeneous strain differ; Herm T[gR]≠T[Herm gR]; broadened pole, inverse-denominator and peak crossings differ. |
| [Scalar CPA and centroid result](../../../../docs/derivations/self_consistent_threshold_and_centroid.md) | Independent-host x^(3/2) versus CPA x² is approximation-specific; different observables have different corrections; the omitted-cluster indicator is order one and is not a rigorous material error bound. Exact centroid closure does not locate peaks. |

All 22 frozen `data/calculated/*.json` records are included, including mesh,
offset, scattering-geometry, alloy seed/box/broadening, continuum, threshold,
tomography, analytical and native-reference controls. The theory/experimental,
first-principles, validation and literature corpora also contain empirical gap
laws, finite-temperature/matrix capability results and instrument-conditioned
edges. Their existing scoped claims do not become physical alloy-kernel bounds.

For historical inversion evidence, use the later direct Part I/II audits,
not the earlier condensed seven-anchor description: x≈0.150 and its −30 meV
value are approximate; Part I does not print a composition metrology method;
Part II reports density/microprobe. The source-reported x0=0.165±0.005 is a
4.2 K, model-assisted crossover uncertainty, not individual specimen errors,
an all-pairs modulus, or a confidence interval for physical 0 K xc.
The secondary Camassel transcription is preserved as secondary. No correction
to R01 data or its old audits is made in this R07-only tranche.

## 4. Exact missing-information disposition

1. **Observable/state adapter:** an independently bounded link from the
   measured/frozen-ion quantity to the intended physical 0 K Γ ordering,
   including strain, carrier filling, zero-point effects and branch identity.
   An independently specified disorder law is also required; a measured
   macroscopic composition uncertainty is not automatically atomic disorder.
2. **D:** sector-weighted eliminated spectral support or an equivalent rigorous
   analyticity/separation certificate, uniform in composition, with common-root
   existence margins. Neither numerical η nor a resolution-limited linewidth
   upper bound certifies zero support. Spectrum outside a measured window can
   change Re K through dispersion relations; optical transitions alone do not
   reconstruct both single-particle gα.
3. **B:** bounded interior Γ6/Γ8 denominators or μ on the certified common
   trajectory. Binary gaps, an interpolated cubic zero and a threshold DOS
   coefficient are insufficient. A qualified pair of signs could suffice for
   existence without reconstructing all local tensor coefficients.
4. **S:** a lower composition modulus across the entire interval, with
   uncertainty. Finite measured/calculated secants do not establish it.
   Even at three exact sample points, adding
   `λ(x−x1)(x−x2)(x−x3)` preserves all observations and can change the interior
   derivative arbitrarily. This is an information counterexample, not a
   proposed material correction; the fixed-local I1 theorem is stronger.
5. **U:** joint uniform branch residual bounds against the physical operator,
   not internal convergence differences. Their correlation and composition
   metrology must be retained. No finite number can currently be inserted as
   `max(ε6,ε8)/m`; neither ε nor positive m is qualified.

Thus there is **no certified physical 0 K xc interval from this package**.
Reported experimental and model intervals remain valid only with their original
qualifications. If continuity of a particular experimental ordering observable
is independently established, its robust opposite signs can bracket at least
one finite-temperature ordering reversal. That weaker statement neither proves
D nor specifies a unique 0 K root. No interval is narrowed by averaging published
crossovers with incompatible state, lineage or error semantics.

## 5. One next action, and why stop here

The [single proposed pilot](next_pilot.md) is a bounded reanalysis of existing
low-temperature, polarization-resolved magnetotransmission on independently
assayed interior specimens, initially two compositions and conditionally a
third. It targets a specimen-level signed ordering bracket, the cheapest useful
portion of missing B, without claiming to recover D, S or U. It has explicit
data/fidelity gates, deterministic resource caps and acceptance/rejection rules.
No new growth, high-cost native calculation, outreach or numerical queue is
created. If the existing raw data/metrology do not exist, reject the pilot at
intake rather than digitize fitted curves into artificial evidence.

Further symbolic variations cannot supply an unknown physical measure, and a
larger numerical reference precision cannot supply an unknown interior mass.
The missing-evidence conclusion is substantiated by inspected primary material
work plus preserved counterexamples. Stop this investigation now. Reopening
requires new qualified evidence or a separately authorized scoped acquisition;
it does not change the older goal's status, controls or budget.
