# R06 Phase 1A initial prior-art and novelty boundary

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Date:** 2026-07-23  
**Status:** Initial verified-source audit; novelty unresolved; simulation not authorized

## 1. Decision reached

The broad provisional novelty hypothesis is rejected.

It is not defensible to claim novelty merely for combining finite length, drift and diffusion, Poisson electrostatics, carrier/trap fluctuations, contact recombination, or a terminal current/voltage spectrum. Prior literature already covers these elements in overlapping combinations.

The scientifically viable question is narrower:

> Does a thermodynamically closed, bipolar, HgCdTe-specific photoconductor model with explicit trap kinetics, stochastic finite-contact exchange, optical generation, a conserved terminal observable, and dimensionless error bounds expose practically relevant regimes not already resolved by established finite-device noise theory?

This is a research question, not a novelty claim.

## 2. Highest-overlap prior art

### 2.1 Finite size, diffusion, Poisson correlation, and terminal current

Gomila and Reggiani developed an analytical finite-size GR-noise theory for a one-dimensional, uniformly doped resistor with drift-diffusion transport, trap dynamics, Poisson electrostatics, ohmic contacts, and conduction plus displacement current.

Source:

- G. Gomila and L. Reggiani, “Size effects on generation-recombination noise,” *Applied Physics Letters* 81, 4380-4382 (2002).
- DOI: `10.1063/1.1526915`.
- Author preprint: `arXiv:cond-mat/0210365`.

Verified implications:

- finite size modifies low-frequency current noise;
- diffusion cannot be discarded generally;
- long-range Coulomb correlation changes the high-field behavior;
- the terminal current must be constructed from conduction and displacement contributions;
- the infinite-device lumped expression is a limit of a more general spatial result.

R06 consequence:

- finite-size Poisson-coupled GR noise is not a novel premise;
- this paper becomes an analytical benchmark;
- a later solver must reproduce the reported limiting behavior before any HgCdTe result is trusted.

### 2.2 Coupled carriers, traps, Poisson, and full frequency spectra

Zocchi reports current and voltage GR-noise spectra for finite-length semiconductors using coupled drift-diffusion continuity equations for both carriers and traps with Poisson space-charge interaction.

Source:

- F. E. Zocchi, “Current and voltage noise spectrum due to generation and recombination fluctuations in semiconductors,” *Physical Review B* 73, 035203 (2006).
- DOI: `10.1103/PhysRevB.73.035203`.

Verified from the publisher abstract:

- finite sample length is explicit;
- both charge carriers and trap levels are dynamic;
- Poisson interaction is included;
- current and voltage PSDs are computed over frequency;
- finite-length carrier boundary conditions are included.

R06 consequence:

- the general frequency-domain coupled-carrier/trap problem is already strongly occupied;
- full-text equation and boundary-condition comparison is mandatory before solver design;
- novelty, if any, must arise from a more specific combination or a new controlled result, not from the governing-equation list.

### 2.3 Bipolar fundamental sources versus approximate equivalent sources

Bonani and Ghione compare a fundamental Langevin treatment using electron, hole, and trap population fluctuations against approximate equivalent current-density sources in a bipolar drift-diffusion model.

Source:

- F. Bonani and G. Ghione, “Generation-recombination noise modelling in semiconductor devices through population or approximate equivalent current density fluctuations,” *Solid-State Electronics* 43, 285-295 (1999).
- DOI: `10.1016/S0038-1101(98)00253-6`.

Verified implications:

- homogeneous equivalent sources can fail when ohmic boundary conditions matter;
- a monopolar model can fail when minority-carrier transfer is non-negligible;
- direct and deep-trap-assisted processes can require correlated bipolar treatment;
- empirical lifetime or source corrections can hide structural model error.

R06 consequence:

- the baseline must retain bipolar primitive event sources;
- equivalent current sources may be used only after an equivalence proof for the selected geometry and operating regime;
- a comparison between fundamental and reduced source models could be useful, but is not inherently novel.

### 2.4 Established impedance-field and Green-function transfer methods

Bulashenko, Gomila, Rubi, and Kochelap extend impedance-field analysis to inhomogeneous semiconductor junctions with both drift and diffusion.

Source:

- O. M. Bulashenko, G. Gomila, J. M. Rubi, and V. A. Kochelap, “Extension of the impedance field method to the noise analysis of a semiconductor junction: Analytical approach,” *Journal of Applied Physics* 83, 2610-2618 (1998).
- DOI: `10.1063/1.367023`.

R06 consequence:

- a matrix-frequency, Green-function, transfer-field, or adjoint terminal-noise solver is established methodology;
- numerical efficiency or software architecture does not establish physics novelty;
- an adjoint/impedance-field solution can provide the second independent method required for selected cases.

### 2.5 Finite contact recombination velocity

Park treats finite contact surface recombination velocities in GR-noise spectra of uniformly doped semiconductors.

Source:

- C. H. Park, “Generation-recombination noise in uniformly doped semiconductors with contacts of finite surface recombination velocities,” *Journal of Applied Physics* 132, 214501 (2022).
- DOI: `10.1063/5.0111954`.

R06 consequence:

- replacing ideal ohmic contacts with a finite deterministic recombination velocity is not novel;
- the unresolved question is whether a thermodynamically complete stochastic injection/extraction boundary was included;
- R06 must not assume that a Robin mean boundary alone provides contact noise.

## 3. HgCdTe-specific prior art

### 3.1 Blocking contacts already modify HgCdTe GR noise and responsivity

D. L. Smith studied blocking-contact effects on GR noise, responsivity, and detectivity in intrinsic photoconductors, including HgCdTe examples near 77 K.

Source:

- D. L. Smith, “Effects of blocking contacts on generation-recombination noise and responsivity in intrinsic photoconductors,” *Journal of Applied Physics* 56, 1663 (1984).
- DOI: `10.1063/1.334155`.

R06 consequence:

- contact-controlled changes to HgCdTe noise corner and responsivity are established;
- a later model must reproduce the applicable Smith limit;
- the possible contribution is a more complete electrostatic and stochastic contact closure plus quantified regime boundaries.

### 3.2 Deep-trap effects on HgCdTe GR noise are established

Iverson and Smith developed an HgCdTe photoconductor theory in which deep levels modify lifetime, mobility, diffusivity, sweepout, and the free/bound carrier noise.

Source:

- A. Evan Iverson and D. L. Smith, “Theory of deep level trap effects on generation-recombination noise in HgCdTe photoconductors,” *Journal of Applied Physics* 58, 579-587 (1985).
- DOI: `10.1063/1.335666`.

R06 consequence:

- explicit trap dynamics cannot be advertised as an unexplored HgCdTe concept;
- the exact state variables and covariance in this source must be compared with an event-level SRH closure;
- the measured corner frequency must not be assumed equal to one microscopic lifetime.

### 3.3 Practical planar-contact geometry can invalidate a 1D effective contact parameter

Smith, Musca, and Faraone compared ideal one-dimensional end contacts with practical two-dimensional planar contacts in HgCdTe photoconductors.

Source:

- E. P. G. Smith, C. A. Musca, and L. Faraone, “Two-dimensional modelling of HgCdTe photoconductive detectors,” *Infrared Physics & Technology* 41, 175-186 (2000).
- DOI: `10.1016/S1350-4495(99)00054-7`.

Verified implications:

- practical planar contact geometry changes electric-field and minority-carrier distributions;
- a two-dimensional n+/n contact model fit experimental responsivity without using contact recombination velocity as an adjustable parameter;
- a one-dimensional contact velocity can act as an effective proxy rather than a unique material/interface constant.

R06 consequence:

- the 1D theory is an idealized end-contact benchmark and similarity map;
- direct prediction of practical planar detectors is outside the baseline claim;
- any inferred contact velocity must be labeled geometry conditioned;
- a future 2D verification is required before transferring quantitative contact boundaries to production devices.

### 3.4 Surface shunt noise is an alternative explanation

Bhan, Gopal, Saxena, and Singh found that standard bulk GR expressions did not fit measured noise in an n-HgCdTe overlap array and introduced passivant-induced surface accumulation shunts.

Source:

- R. K. Bhan, V. Gopal, R. S. Saxena, and J. P. Singh, “Noise modeling of shunt resistance in HgCdTe photoconductor detectors,” *Infrared Physics & Technology* 45, 81-92 (2004).
- DOI: `10.1016/j.infrared.2003.06.001`.

R06 consequence:

- excess or multimode terminal spectra are not unique evidence of spatial bulk GR modes;
- surface accumulation, distributed shunts, contact resistance, and measurement loading must be alternative hypotheses;
- a future experimental comparison needs independent surface/shunt information.

## 4. Material parameter evidence

Sarusi et al. extracted mobility, diffusion length, bulk lifetime, absorption, and front/back surface recombination velocities in p-Hg0.77Cd0.23Te layers as functions of temperature.

Source:

- G. Sarusi, A. Zemel, D. Eger, S. Ron, and Y. Shapira, “Investigation of the bulk and surface electronic properties of HgCdTe epitaxial layers using photoelectromagnetic, Hall, and photoconductivity measurements,” *Journal of Applied Physics* 72, 2312-2321 (1992).
- DOI: `10.1063/1.351573`.

The institutional abstract reports a CdTe-capped surface recombination velocity below \(5000\ \mathrm{cm\,s^{-1}}\) at 77 K for the studied p-type material.

R06 consequence:

- this value is a specimen- and interface-specific range anchor, not a universal metal-contact velocity;
- bulk lifetime, diffusion length, and mobility extracted from the same experiment are correlated;
- the parameter schema must distinguish passivated surface recombination from contact exchange.

## 5. Novelty matrix

| Proposed element | Prior-art status | R06 position |
|---|---|---|
| Finite 1D sample | Established | Benchmark only |
| Drift plus diffusion | Established | Required baseline |
| Poisson space-charge coupling | Established | Required baseline |
| Displacement current in terminal observable | Established | Conservation requirement |
| Full frequency current/voltage GR PSD | Established in general semiconductor theory | Reproduce and specialize |
| Both carrier populations and traps | Established | Required baseline |
| Bipolar population-source Langevin model | Established | Required source representation |
| Impedance-field/Green-function terminal transfer | Established | Independent solver method |
| Finite deterministic contact recombination velocity | Established | Not a novelty basis |
| HgCdTe blocking-contact effect on GR noise | Established | Required material-specific limit |
| HgCdTe deep-trap noise effects | Established | Required comparison |
| 1D end-contact geometry as practical planar-detector model | Known to be limited | Treat as idealized similarity model |
| Event-level stochastic contact detailed balance in bipolar HgCdTe PC | Not yet established by this audit | Candidate gap; full-text search required |
| Unified optical generation, explicit traps, contact exchange, Poisson, and terminal FDT | Not yet established by this audit | Candidate integration gap, not yet novelty |
| Dimensionless quantitative error map for the lumped Lorentzian in HgCdTe | Not yet established by this audit | Candidate result |
| Demonstration that terminal corner differs from microscopic lifetime across identified regimes | Partly anticipated by trap/contact theory | Candidate quantitative synthesis |
| Controlled apparent \(1/f^\alpha\) interval from discrete spatial modes | Not established by current source set | Candidate result requiring strict discrimination from surface/trap distributions |

## 6. Revised working contribution

The provisional contribution is narrowed to:

> R06 will test a bipolar, finite one-dimensional HgCdTe photoconductor model in which drift, diffusion, Poisson electrostatics, explicit trap kinetics, finite stochastic contact exchange, optical generation, and the external terminal circuit are closed under one covariance convention. The intended contribution is not the existence of finite-size GR modes, but quantified dimensionless error bounds for common lumped interpretations and a verified map of when a terminal noise corner, amplitude, or apparent spectral slope ceases to represent one bulk lifetime.

This statement remains provisional.

## 7. Falsifiable outputs that could still be valuable without strong novelty

Even if the full formulation is an integration of established theory, R06 can remain scientifically useful if it produces at least one of the following nontrivial results:

1. a controlled asymptotic correction to the lumped HgCdTe GR amplitude or corner;
2. an explicit inequality defining when \(\tau_{\mathrm{inferred}}=(2\pi f_c)^{-1}\) differs from the microscopic trap or recombination time by more than a declared tolerance;
3. a similarity map separating bulk, diffusion, contact, screening, and sweepout regimes;
4. a verified contact-noise boundary formulation that recovers both blocking and reservoir limits;
5. a proof or counterexample concerning apparent \(1/f^\alpha\) behavior from a finite set of spatial modes;
6. a practical criterion for when the 1D contact-velocity model ceases to approximate a planar HgCdTe detector.

## 8. Immediate full-text priorities

The next audit must obtain and compare the complete equations in:

1. Zocchi 2006 — DOI `10.1103/PhysRevB.73.035203`;
2. Park 2022 — DOI `10.1063/5.0111954`;
3. Smith 1984 — DOI `10.1063/1.334155`;
4. Iverson and Smith 1985 — DOI `10.1063/1.335666`;
5. Bonani and Ghione 1999 — DOI `10.1016/S0038-1101(98)00253-6`;
6. Bulashenko et al. 1998 — DOI `10.1063/1.367023`.

For each source, the audit must extract:

- state variables;
- deterministic residual;
- contact and terminal ensembles;
- primitive noise sources;
- source covariance;
- PSD convention;
- role of displacement current;
- limiting cases;
- exact overlap with R06.

## 9. Confidence and unresolved risks

| Finding | Confidence | Main uncertainty |
|---|---:|---|
| Broad finite-size Poisson-GR novelty is invalid | High | None material to the decision |
| Full frequency carrier/trap spectra already exist | High from abstract; medium on exact closure | Zocchi full equations unavailable |
| Bipolar fundamental source treatment is established | High | Exact electrostatic implementation still to audit |
| Finite contact velocity effects are established | High from abstract | Contact fluctuation covariance unknown |
| HgCdTe blocking-contact and deep-trap effects are established | High from abstracts | Exact equations and assumptions pending |
| 1D contact velocity may be geometry-effective | High | Quantitative reduction error not yet mapped |
| Unified event-level stochastic contact closure may be a gap | Low-to-medium | Literature search incomplete |
| Dimensionless HgCdTe lumped-model error map may be new | Low-to-medium | Adjacent analytical literature incomplete |

## 10. Gate decision

Continue Phase 1A. Do not begin production simulations.

The next positive gate requires:

1. full-text source comparison for the six priority papers;
2. a finalized primitive covariance representation;
3. a thermodynamically complete contact boundary;
4. an explicit decision on dynamic trap occupancy;
5. a reduced dimensionless parameter set;
6. a statement of which output is expected to be new rather than merely implemented.

If these conditions cannot be met, R06 should be reframed as a reproducible benchmark and synthesis study rather than an original theoretical paper.
