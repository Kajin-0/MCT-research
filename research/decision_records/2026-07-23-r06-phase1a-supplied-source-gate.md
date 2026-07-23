# R06 Phase 1A supplied-source gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Decision:** continue Phase 1A with one critical source outstanding; broad novelty rejected; production simulation remains unauthorized

## Evidence added

The user supplied full readable copies of:

- Shockley and Read 1952;
- Smith 1982;
- Smith 1984;
- Iverson and Smith 1985;
- Bulashenko et al. 1998;
- Zocchi 2006.

Equation-level source notes now record their state variables, operators, boundary conditions, covariance representation, terminal ensemble, spectral convention, asymptotes, assumptions, and overlap with R06.

## Bibliographic resolution

The previously unresolved Smith 1982 DOI is:

`10.1063/1.330006`.

## Scientific findings

### 1. Broad finite-device full-frequency theory is established

Zocchi 2006 already treats a finite unipolar electron-trap semiconductor with drift, diffusion, linearized Poisson coupling, dielectric relaxation, full-frequency current and voltage spectra, and separate fixed-voltage and open-circuit boundary ensembles.

Therefore the combination of finite length, traps, Poisson coupling, drift-diffusion, and terminal spectra is not a novelty basis.

### 2. Non-Lorentzian HgCdTe spatial noise is established

Smith 1982 includes drift, diffusion, absorbing contacts, spatial source-lifetime correlation, thermal and optical-background populations, and predicts distinct non-Lorentzian high-frequency asymptotes.

Therefore a terminal spectrum departing from a single Lorentzian is not, by itself, a new HgCdTe result.

### 3. Finite deterministic contact velocity is established

Smith 1984 uses exact finite-`S` Robin boundaries and establishes blocking and absorbing limits, terminal Dember terms, contact asymmetry, and finite-`S` changes to responsivity and GR-noise rolloff.

No explicit stochastic contact injection/extraction or contact covariance is included.

### 4. Dynamic trap populations and trap noise are established

Iverson and Smith 1985 include four deep-level transition rates, explicit trap dynamics, correlated free-carrier/trap populations, trap-modified mobility and diffusion, and a distinct bound/free thermal-noise component.

### 5. SRH noise must be event based

Shockley and Read 1952 derive the mean SRH law from four positive capture/emission channels. The algebraic net rate does not define stochastic intensity. The reference R06 covariance must remain the stoichiometric sum over primitive events.

### 6. Equilibrium transfer cross terms are mandatory

Bulashenko et al. 1998 show that electrostatic and sample-contact cross terms are necessary to recover equilibrium Nyquist noise in an impedance-field decomposition.

## Accepted model decisions

1. **Dynamic trap occupancy remains in the reference state.**
2. **Primitive four-channel SRH propensities are accepted as the kinetic basis.**
3. **Population-source and equivalent-current backends remain mutually exclusive.**
4. **Direct resolvent and adjoint/impedance-field terminal calculations are both required.**
5. **Smith 1982, Smith 1984, Iverson-Smith 1985, Zocchi 2006, Gomila-Reggiani 2002, and Bulashenko 1998 become mandatory analytical benchmarks.**
6. **The provisional forward/reverse contact-event closure remains a project hypothesis, not a validated HgCdTe model.**

## Revised candidate contribution

The strongest remaining candidate is:

> A thermodynamically complete finite stochastic-contact boundary, embedded in a bipolar HgCdTe drift-diffusion-Poisson-trap model, together with controlled error bounds for the Smith quasineutral/finite-`S` and conventional single-lifetime reductions.

This remains contingent on Park 2022.

## Remaining critical source

Park 2022 — DOI `10.1063/5.0111954`.

The Phase 1A finite-contact novelty gate cannot close until the full paper is inspected for:

- stochastic contact sources;
- detailed balance;
- covariance normalization;
- terminal cross covariance;
- FDT recovery;
- blocking and reservoir limits.

## Authorization

Authorized:

- acquire and audit Park 2022;
- transcribe analytical benchmark equations;
- implement algebraic convention/unit tests if isolated from production device sweeps;
- derive the large-exchange stochastic reservoir limit;
- specify quantitative Smith-to-full-model error metrics;
- prepare the final Phase 1 proceed/reframe decision.

Not authorized:

- production parameter sweeps;
- HgCdTe predictive claims;
- manuscript drafting;
- novelty claims;
- arbitrary fitted noise sources;
- replacing explicit traps with algebraic SRH without a stochastic reduction proof.

## Stop or reframe rule

Reframe the contact contribution as a benchmark/synthesis result if Park 2022 already provides a thermodynamically complete finite-contact stochastic closure. Reframe the overall project if no uncertainty-robust HgCdTe reduction boundary can be produced from public parameters.