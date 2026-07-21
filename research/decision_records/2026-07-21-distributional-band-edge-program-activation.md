# Decision: activate the independent distributional band-edge program

**Date:** 2026-07-21  
**Issue:** #167  
**Decision status:** controlling

## Decision

Freeze the completed observation-model uncertainty manuscript as Paper I and replace the collaboration-first continuation plan with an independent flagship program:

> Develop a distributional, observation-aware theory of HgCdTe band-edge observables.

The paired acquisition protocol remains available as a future validation design, but partner outreach and laboratory collaboration are no longer active dependencies.

## Evidence motivating the decision

Paper I established that historical equation differences are smaller than or comparable to composition uncertainty, specimen-state uncertainty, and observation-operator spread. Additional universal-law fitting is therefore not expected to produce a defensible high-significance result from the current historical scalar data.

The newly recovered full-text source set supplies a coherent constructive route:

- Wu 1983: alloy-fluctuation physics contributes to bowing beyond a virtual-crystal mean;
- Herrmann 1992: a distribution of local gaps can generate an apparent exponential absorption tail;
- Dingrong 1985: carrier filling moves the observed optical edge and contributes below-gap absorption;
- Ivanov-Omskii 2009: processing changes PL displacement, linewidth, and inferred disorder measures;
- Chang 2007: nonparabolic intrinsic absorption, Urbach tails, and effective thickness jointly determine the reported cutoff;
- Teppe 2016: the near-critical Kane mass changes sign with temperature, while composition fluctuations impede fine composition tuning.

## New scientific question

Instead of asking only

```text
Which equation best predicts Eg(x,T)?
```

ask

```text
Given a latent band structure and a specimen-state distribution,
what gap will each measurement modality and edge operator report?
```

## First quantitative result

A tested second-order propagation model was implemented for a Gaussian composition distribution. At nominal `x=0.155`, `T=77 K`, using the reconstructed Laurenti law:

```text
Eg                         -0.0478 meV
dEg/dx                      1.71911 eV
dEg/dT                      0.38518 meV/K

sigma_x=0.001 -> sigma_E=1.719 meV, sigma_Tc=4.463 K
sigma_x=0.005 -> sigma_E=8.596 meV, sigma_Tc=22.316 K
```

Near the nominal transition, the corresponding Gaussian local opposite-sign fractions are close to one half. This is a local sign statistic and precision requirement, not a topological invariant or a claim about the actual Teppe specimen composition distribution.

## Why this is the preferred route

- It builds directly on Paper I rather than abandoning it.
- It produces positive predictions and falsifiable cross-modal relations.
- It can be executed independently from public papers and reproducible computation.
- It preserves the repository's strongest assets: provenance, observation operators, uncertainty propagation, Kane modeling, and group-aware validation.
- It does not require speculative production first-principles calculations.
- It can remain scientifically useful even if no universal latent gap law is selected.

## Publication target

The flagship manuscript must contain:

1. a new forward model from latent gap to reported observable;
2. analytical results with limiting-case checks;
3. at least one significant quantitative HgCdTe result;
4. validation against at least three independent published experimental lineages;
5. recoverability or identifiability maps;
6. group-preserving holdout tests;
7. public code, data, and provenance;
8. a claim-by-claim novelty audit.

## Authorized work

- composition-to-gap distribution propagation;
- source-bounded absorption, PL, detector-cutoff, and magneto-optical operators;
- carrier filling and free-carrier absorption;
- Gaussian and non-Gaussian quadrature with explicit distribution provenance;
- transition-width and recoverability maps;
- auditable digitization and published-data reproduction;
- manuscript development after independent reproduction gates pass.

## Deferred work

- partner outreach and facility access;
- new sample acquisition;
- SQS, CPA, SCBA, and production alloy first-principles calculations;
- full AHC calculations;
- universal gap-law fitting.

Deferred work may be reopened only if a low-cost model identifies a decision-changing observable that cannot be resolved from public evidence.

## Claim restrictions

Do not:

- equate composition uncertainty with microscopic composition fluctuation;
- equate a local gap distribution with an Urbach, PL, or quasiparticle width;
- treat detector cutoff as a direct material gap;
- treat PL peak, absorption edge, and Kane mass as interchangeable;
- infer a bulk topological invariant from local sign probability;
- describe the reconstructed Laurenti law as universally selected;
- expand Paper I in a way that obscures its completed non-identifiability result.

## Superseded continuation instruction

The previous instruction to prioritize external partner feasibility, outreach approval, and paired specimen acquisition is superseded as the active research path. The protocol and outreach records remain archived and valid for future use.
