# R05 Phase 0 claim-level prior-art matrix

**Controlling issue:** #390  
**Audit date:** 2026-07-31  
**Status:** bounded primary-source audit; several paywalled full texts still require line-by-line verification  
**Claim policy:** abstracts establish scope only; equation-level claims require full-text inspection

## Search boundary

The audit covered:

- random-mass Dirac Hamiltonians;
- short- and long-range correlated random mass;
- density of states and localization;
- SCBA and rare-region limitations;
- HgCdTe massless Kane experiments;
- HgCdTe disorder calculations;
- HgCdTe alloy/composition-fluctuation evidence;
- optical and magneto-optical observables.

The current audit does not support a broad novelty claim. It identifies only a narrow potentially distinct comparison: a finite-range HgCdTe/Kane calculation against an explicitly matched incoherent scalar local-gap mixture.

---

## Claim 1

**Claim:** Spatial correlation in a one-dimensional random Dirac mass can change the low-energy DOS and localization behavior relative to white-noise or less-correlated disorder.

**Closest prior result:** I. Ichinose and M. Kimura, “Non-locally correlated disorder and delocalization in one dimension (I): Density of states,” *Nuclear Physics B* (1999), DOI `10.1016/S0550-3213(99)00323-5`; K. Takeda and I. Ichinose, “Effects of Correlated Noise in Random-Mass Dirac Fermions,” *J. Phys. Soc. Jpn.* **71**, 2216–2223 (2002), DOI `10.1143/JPSJ.71.2216`.

**Hamiltonian used:** one-dimensional random-mass Dirac model.

**Spatial dimension:** 1D.

**Disorder type:** nonlocally correlated random mass; short- and long-range cases.

**Finite correlation length included:** yes.

**HgCdTe-specific:** no.

**Observable:** density of states, localization length, band-center behavior.

**Analytical or numerical:** supersymmetric, transfer-matrix, and numerical methods across the cited sequence.

**Experimental comparison:** no HgCdTe comparison.

**What remains distinct:** only material-specific mapping, finite-range covariance families relevant to HgCdTe, matched scalar-null comparison, and experimentally convolved observables.

**Novelty status:** `ESTABLISHED`.

---

## Claim 2

**Claim:** Correlated random mass can produce nontrivial low-energy DOS scaling in two-dimensional Dirac systems.

**Closest prior result:** A. A. Fedorenko, D. Carpentier, and E. Orignac, “Two-dimensional Dirac fermions in the presence of long-range correlated disorder,” *Phys. Rev. B* **85**, 125437 (2012), DOI `10.1103/PhysRevB.85.125437`.

**Hamiltonian used:** 2D Dirac fermions with scalar, gauge, and mass disorder channels.

**Spatial dimension:** 2D.

**Disorder type:** power-law long-range correlated disorder.

**Finite correlation length included:** not as the primary finite-range Gaussian/Matérn scale studied by R05; correlation is algebraic.

**HgCdTe-specific:** no.

**Observable:** DOS and transport/full counting statistics.

**Analytical or numerical:** SCBA, RG, Green-function, and bosonization methods.

**Experimental comparison:** no HgCdTe comparison.

**What remains distinct:** finite-range rather than algebraic covariance, 3D/HgCdTe Kane structure, and matched scalar local-gap null.

**Novelty status:** `ESTABLISHED` for correlated random-mass DOS physics; `INCREMENTAL_EXTENSION` for changing covariance class alone.

---

## Claim 3

**Claim:** Uncorrelated impurity and Cd-composition disorder can renormalize the Kane mass and DOS in bulk HgCdTe, with the heavy-hole band materially lowering a disorder-driven transition threshold.

**Closest prior result:** S. S. Krishtopenko, M. Antezza, and F. Teppe, “Disorder-induced topological phase transition in HgCdTe crystals,” *Phys. Rev. B* **106**, 115203 (2022), DOI `10.1103/PhysRevB.106.115203`.

**Hamiltonian used:** HgCdTe Kane model including heavy-hole effects.

**Spatial dimension:** bulk 3D.

**Disorder type:** uncorrelated randomly distributed impurities and Cd-composition fluctuations.

**Finite correlation length included:** no; the abstract identifies uncorrelated disorder.

**HgCdTe-specific:** yes.

**Observable:** disorder-renormalized mass and density of states; topological-transition interpretation.

**Analytical or numerical:** self-consistent Born approximation.

**Experimental comparison:** not established by the abstract as a direct specimen-level disorder fit.

**What remains distinct:** finite correlation length, matched scalar-mixture comparison, covariance-family robustness, and experimental-resolution survival.

**Novelty status:** `ESTABLISHED` for HgCdTe disorder-renormalized Kane DOS; `POTENTIALLY_DISTINCT` for the finite-range matched-null question.

**Required full-text check:** exact Hamiltonian, disorder vertices, ultraviolet regularization, composition-disorder mapping, DOS definition, and any implicit correlation assumptions.

---

## Claim 4

**Claim:** HgCdTe near the normal/inverted transition supports a simplified Kane rest-mass description with a velocity near `1e6 m/s`, and the signed mass changes through zero with composition or temperature.

**Closest prior results:** M. Orlita et al., “Observation of three-dimensional massless Kane fermions in a zinc-blende crystal,” *Nature Physics* **10**, 233–238 (2014), DOI `10.1038/nphys2857`; F. Teppe et al., “Temperature-driven massless Kane fermions in HgCdTe crystals,” *Nature Communications* **7**, 12576 (2016), DOI `10.1038/ncomms12576`.

**Hamiltonian used:** simplified Kane model with Gamma6/Gamma8 structure; full interpretation includes the heavy-hole/flat-band sector.

**Spatial dimension:** 3D bulk.

**Disorder type:** not the controlled variable.

**Finite correlation length included:** no.

**HgCdTe-specific:** yes.

**Observable:** dynamical conductivity, Landau-level/magneto-optical transitions, extracted gap/rest mass and velocity.

**Analytical or numerical:** model fitting to experiment.

**Experimental comparison:** direct far-infrared and magneto-optical measurements.

**What remains distinct:** disorder correlation and matched-null effects on DOS or optical response.

**Novelty status:** `ESTABLISHED`.

---

## Claim 5

**Claim:** The HgCdTe Kane velocity can be treated as composition- and temperature-independent over a useful near-transition range.

**Closest prior result:** Teppe et al. (2016), reporting `v_K = (1.07 +/- 0.05)e6 m/s` across the investigated compositions and temperatures.

**Hamiltonian used:** simplified Kane description.

**Spatial dimension:** 3D bulk.

**Disorder type:** not modeled.

**Finite correlation length included:** no.

**HgCdTe-specific:** yes.

**Observable:** magneto-optically inferred velocity.

**Analytical or numerical:** experimental fit.

**Experimental comparison:** yes.

**What remains distinct:** deriving the exact two-band velocity coefficient from the repository Novik-basis 8-band block and propagating its uncertainty into `m` and `g`.

**Novelty status:** `ESTABLISHED` physically; repository mapping remains a `METHOD_VALIDATION` task.

---

## Claim 6

**Claim:** HgCdTe exhibits composition-related optical disorder/band-tail phenomena.

**Closest prior result:** “Study of alloy disorder in (Hg,Cd)Te with the use of infrared photoluminescence,” *Physica B* **404**, 5035–5037 (2009), DOI `10.1016/j.physb.2009.08.210`.

**Hamiltonian used:** not a coherent random-mass Kane calculation.

**Spatial dimension:** bulk/epitaxial samples.

**Disorder type:** compositional fluctuations inferred through photoluminescence localization/red shift.

**Finite correlation length included:** no defensible spatial covariance length identified in the accessible record.

**HgCdTe-specific:** yes.

**Observable:** PL peak shift and temperature dependence; annealing sensitivity.

**Analytical or numerical:** phenomenological optical analysis.

**Experimental comparison:** yes, for `x=0.38` and `0.57`, not the near-critical `x approximately 0.15–0.17` regime.

**What remains distinct:** near-transition spatial correlation, coherent propagation, and direct DOS comparison.

**Novelty status:** `ESTABLISHED` for optical evidence of alloy disorder; `NOT_SUPPORTED` as a measured R05 correlation length.

---

## Claim 7

**Claim:** HgCdTe alloy occupations possess a directly measured finite spatial correlation length suitable for R05.

**Closest prior result:** R. S. Patrick, A.-B. Chen, A. Sher, and M. A. Berding, “Phase diagrams and microscopic structures of (Hg,Cd)Te, (Hg,Zn)Te, and (Cd,Zn)Te alloys,” *J. Vac. Sci. Technol. A* **6** (1988), DOI `10.1116/1.575524`, reports cluster-theory results consistent with nearly random distributions, with correlation signs sensitive to the alloy-medium model.

**Hamiltonian used:** alloy cluster/thermodynamic model, not Kane propagation.

**Spatial dimension:** atomistic alloy model.

**Disorder type:** local chemical/bond correlations.

**Finite correlation length included:** no source-qualified continuum `xi` identified.

**HgCdTe-specific:** yes.

**Observable:** calculated local correlations, bond lengths, and phase diagrams.

**Analytical or numerical:** cluster theory.

**Experimental comparison:** bond-length and phase-diagram comparison reported.

**What remains distinct:** direct measurement of the electronic-mass covariance length near the band-inversion composition.

**Novelty status:** `NOT_SUPPORTED` for a measured continuum `xi`.

---

## Claim 8

**Claim:** A correlated random-mass DOS calculation is scientifically distinct merely because it uses finite correlation length.

**Closest prior result:** the 1D and 2D works above already establish correlation-dependent random-mass DOS behavior.

**Hamiltonian used:** Dirac.

**Spatial dimension:** 1D and 2D.

**Disorder type:** nonlocal short-range and long-range correlated mass.

**Finite correlation length included:** yes in the 1D literature; algebraic correlations in 2D.

**HgCdTe-specific:** no for those works.

**Observable:** DOS and localization/transport.

**Analytical or numerical:** both.

**Experimental comparison:** an integrated optical-platform emulation also exists: R. Keil et al., “The random mass Dirac model and long-range correlations on an integrated optical platform,” *Nature Communications* **4**, 1368 (2013), DOI `10.1038/ncomms2384`.

**What remains distinct:** only a tightly defined HgCdTe material mapping, full-Kane effect where necessary, matched scalar-mixture null, and experimentally resolvable prediction.

**Novelty status:** `NOT_SUPPORTED` as a broad claim.

---

## Claim 9

**Claim:** A difference between a finite-range correlated Kane/Dirac model and an incoherent scalar mixture with the identical one-point mass distribution has been established for near-critical HgCdTe.

**Closest prior result:** no directly matching result identified in the bounded audit. Generic correlated random-mass studies compare correlation classes or disorder strengths; the 2022 HgCdTe SCBA study treats uncorrelated disorder rather than the declared finite-range matched-null experiment.

**Hamiltonian used:** proposed minimal Dirac, conditionally full Kane.

**Spatial dimension:** initially 1D benchmark; physical question is bulk HgCdTe.

**Disorder type:** finite-range Gaussian/Matérn signed mass with matched marginal.

**Finite correlation length included:** proposed.

**HgCdTe-specific:** proposed through source-bounded mapping.

**Observable:** low-energy DOS first; optical/magneto-optical response only if DOS survives.

**Analytical or numerical:** proposed analytical limits and minimal numerical oracle.

**Experimental comparison:** not yet.

**What remains distinct:** the matched-null isolation of coherent spatial-correlation effects and its HgCdTe parameter/resolution gate.

**Novelty status:** `POTENTIALLY_DISTINCT` as a comparison protocol and material-specific screening question; not yet a supported physics claim.

---

## Claim 10

**Claim:** Rare-region or interface states automatically establish a measurable HgCdTe correlated-mass effect.

**Closest prior result:** rare configurations can lift nodal DOS in disordered 3D Dirac systems for finite-range scalar-potential disorder; random-mass domain walls are a known mechanism in lower-dimensional Dirac models.

**Hamiltonian used:** generic Dirac/Weyl models, often scalar disorder rather than HgCdTe mass disorder.

**Spatial dimension:** 1D–3D depending source.

**Disorder type:** model dependent.

**Finite correlation length included:** often yes for finite-range impurity potentials, but not the same as the R05 mass field.

**HgCdTe-specific:** no direct R05 validation.

**Observable:** low-energy DOS/localized resonances.

**Analytical or numerical:** both in the broader literature.

**Experimental comparison:** no direct R05 specimen comparison identified.

**What remains distinct:** proving the mechanism survives HgCdTe multiband structure, parameter bounds, and measurement convolution.

**Novelty status:** `NOT_SUPPORTED` as an HgCdTe claim.

---

## Audit decision

```text
Broad claim: finite correlation changes random-mass Dirac DOS
Decision: ESTABLISHED

Broad claim: disorder renormalizes HgCdTe Kane DOS/mass
Decision: ESTABLISHED for uncorrelated SCBA

Narrow claim: finite-range HgCdTe random mass differs measurably from a matched scalar local-gap mixture
Decision: POTENTIALLY_DISTINCT, UNVALIDATED
```

## Gate consequence

A minimal numerical oracle is scientifically defensible only as a bounded discrimination and parameter-threshold test. It must not be presented as discovery of correlated random-mass DOS physics.

The physical R05 claim remains blocked until:

1. full-text verification of the 2022 HgCdTe SCBA conventions;
2. a source-qualified near-transition spatial-correlation envelope or an explicit statement that none exists;
3. a converged matched-null effect above the predeclared threshold;
4. survival under plausible experimental resolution;
5. a clear reason full Kane structure changes the result, or a decision that it is unnecessary.