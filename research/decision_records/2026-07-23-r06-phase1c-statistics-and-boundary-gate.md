# R06 Phase 1C statistics and deterministic-boundary gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** accept Fermi–Dirac/nonparabolic reference statistics and the deterministic contact/circuit hierarchy; continue Phase 1C because material parameter provenance remains incomplete

## Evidence considered

The Phase 1 literature and interface audit established that:

- electrochemical potential is the natural transport and interface variable;
- the generalized Einstein relation depends on carrier compressibility;
- stochastic interface FDT depends on the same susceptibility;
- narrow-gap HgCdTe carrier concentration has been modeled using Kane k.p and Fermi–Dirac statistics;
- public intrinsic-density relations differ materially in low-temperature narrow-gap regimes.

## Statistics decision

The reference architecture will evaluate carrier density and compressibility from one source-controlled Fermi–Dirac/nonparabolic density-of-states model.

The generalized Einstein relation is

\[
\frac{D_s}{\mu_s}
=
\frac{n_s}{q(\partial n_s/\partial\mu_s)_T}.
\]

Screening uses total differential charge susceptibility rather than an automatically imposed Boltzmann Debye length.

Boltzmann transport is retained as a reduced model. Preliminary parabolic-band checks indicate that `eta <= -3` is a candidate two-percent domain and `eta <= -4` a candidate one-percent domain, but the actual decision for HgCdTe must be made by direct comparison against the chosen nonparabolic closure.

## Boundary and circuit decision

The deterministic implementation must separate:

1. blocking carrier flux;
2. ideal electrochemical-potential reservoirs;
3. finite nonlinear direct exchange;
4. dynamic interface-state storage;
5. pair surface recombination;
6. Smith-type effective finite-`S` boundaries;
7. asymmetric left/right contacts.

The external circuit must separately support:

- fixed voltage;
- fixed current;
- open circuit;
- finite Thevenin or Norton loading;
- explicit capacitive states where used.

The label “ohmic” is not a complete boundary or circuit specification.

## Parameter provenance decision

A machine-readable source ledger is accepted. It records source role, verification depth, validity context, uncertainty state, and the remaining audit action.

No numerical value may enter a predictive parameter set merely because it appears frequently in secondary literature.

## Remaining blockers

1. Equation-level selection of the Kane/nonparabolic density-of-states model.
2. Full intrinsic-density model comparison.
3. Low-temperature electron and hole mobility ranges with specimen context.
4. Static permittivity relation and uncertainty.
5. Contact barrier/rate parameter provenance.
6. Optional absorption relation for Beer-Lambert generation.
7. A parameter-correlation policy translated into executable configurations.
8. Final demonstration that at least one reduction-error boundary is likely to remain stable under these uncertainties.

## Authorization

Authorized next:

- full-text material-relation audits;
- numerical statistics prototypes limited to model-comparison and threshold verification;
- completion of the deterministic finite-volume architecture;
- creation of Phase 2 test specifications;
- final Phase 1 decision preparation.

Still unauthorized:

- production detector simulations;
- broad material sweeps;
- stochastic production code;
- predictive HgCdTe contact or noise claims;
- manuscript drafting;
- novelty claims.

## Stop rule

Reframe the project as a benchmark/synthesis package if no parameter model can support a stable reduction-error boundary or if the full reference and all reduced models agree within the declared tolerance throughout the plausible HgCdTe domain.