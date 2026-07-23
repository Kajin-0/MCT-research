# R06 deterministic boundary and external-circuit hierarchy

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** Phase 1C specification; implementation deferred

## 1. Purpose

This document separates material boundary physics from the external electrical ensemble. A contact model and a terminal circuit are independent choices and must not be encoded by one ambiguous label such as “ohmic.”

## 2. Orientation

The device occupies `0 <= x <= L` with outward normals

\[
\nu_L=-1,
\qquad
\nu_R=+1.
\]

Carrier conditions are written in outward particle flux,

\[
\nu_c\Gamma_s=\mathcal B_{s,c},
\]

before converting to conventional current.

The terminal voltage is

\[
V=\phi(0)-\phi(L).
\]

## 3. Electrostatic boundary hierarchy

### E0 — fixed-voltage gauge

\[
\phi(0)=0,
\qquad
\phi(L)=-V_b.
\]

Use for deterministic voltage continuation and fixed-voltage current calculations.

### E1 — unknown terminal voltage

Fix one potential as the gauge,

\[
\phi(0)=0,
\]

and treat `V=-phi(L)` as an unknown constrained by the circuit equation.

Use for fixed-current and finite-load formulations.

### E2 — interface charge or capacitance

Where a contact or interface stores areal charge, impose the displacement jump and surface balance explicitly. A fitted voltage drop may not be inserted simultaneously unless an equivalence derivation prevents double counting.

## 4. Carrier-contact hierarchy

### C0 — blocking particle boundary

\[
\nu\Gamma_n=0,
\qquad
\nu\Gamma_p=0.
\]

Electrostatic displacement and terminal current may remain nonzero. A blocking carrier boundary is not an electrically open terminal by itself.

### C1 — ideal equilibrium reservoir

Pin carrier electrochemical potentials to reservoir values,

\[
\mu_n=\mu_{n,c}^{res},
\qquad
\mu_p=\mu_{p,c}^{res}.
\]

The corresponding boundary densities are derived from the same Fermi–Dirac/nonparabolic statistics used in the bulk. They are not independent input constants.

### C2 — finite direct exchange

Use source-supported nonlinear flux-force laws

\[
\nu\Gamma_s
=\mathcal F_{s,c}(\mu_s-\mu_{s,c}^{res}).
\]

The classical density-Robin reduction

\[
\nu\Gamma_s=S_{s,c}(c_s-c_{s,c}^{eq})
\]

is a special model and must be labeled as such.

### C3 — dynamic interface state

Add areal occupancy variables and surface balance equations. Bulk flux discontinuities are coupled to the interface-state rates and surface charge. This is the reference model when interface storage or trap mediation is active.

### C4 — pair surface recombination

Represent electron-hole pair recombination and reverse generation as shared primitive processes. A pair boundary is not equivalent to two independent carrier-exchange Robin laws.

### C5 — Smith effective finite-`S` boundary

Use the quasineutral ambipolar finite-recombination boundary from Smith 1984 only as a reduced analytical benchmark. It is not the reference bipolar contact closure.

### C6 — asymmetric contacts

Left and right contacts have independent reservoir electrochemical potentials, barrier parameters, interface states, and rate coefficients. Symmetry may be imposed only as an explicit test case.

## 5. External-circuit hierarchy

### T0 — ideal voltage bias

At the deterministic operating point,

\[
V=V_b.
\]

At small signal,

\[
\delta V=0.
\]

The terminal current is solved and includes conduction plus displacement current.

### T1 — ideal current bias

At the operating point,

\[
I=I_b.
\]

At small signal,

\[
\delta I=0.
\]

The terminal voltage is solved. This is the relevant ensemble for the Smith voltage-noise benchmarks.

### T2 — open circuit

Open circuit is the zero-applied-terminal-current specialization of T1. It does not imply zero local carrier flux everywhere.

### T3 — finite Thevenin source

For source voltage `V_s` and series impedance `Z_s`, choose the current orientation so that

\[
V_s=V+Z_s I.
\]

At small signal,

\[
\delta V_s
=\delta V+Z_s(\omega)\delta I.
\]

For deterministic AC response with a noiseless source, set `delta V_s=0`. During stochastic equilibrium testing, the physical source impedance and its thermal fluctuations belong to the assembled circuit model.

### T4 — finite Norton source or load

A Norton representation must be algebraically equivalent to T3 after source transformation. Code must verify the equivalence rather than implement unrelated terminal conventions.

### T5 — capacitive and readout loading

Contact, cable, input, or transimpedance capacitance enters through explicit dynamic circuit states or impedances. A circuit pole must not be misidentified as a detector recombination mode.

## 6. Allowed contact/circuit combinations

| Carrier boundary | Voltage bias | Current bias | Finite load | Required note |
|---|---:|---:|---:|---|
| Blocking | yes | yes | yes | Check conserved-population null modes |
| Ideal reservoir | yes | yes | yes | Reservoir covariance required later for stochastic solve |
| Finite direct exchange | yes | yes | yes | Use same statistics on both sides |
| Dynamic interface state | yes | yes | yes | Surface charge and circuit current must remain conserved |
| Pair recombination | yes | yes | yes | Electron-hole event correlation mandatory later |
| Smith effective `S` | reduced benchmark | source benchmark | reduced benchmark | Quasineutral ambipolar model only |

## 7. Deterministic acceptance tests

1. Equal reservoir electrochemical potentials and zero applied source produce zero mean terminal current.
2. Fixed-voltage and finite-Thevenin formulations agree as `Z_s -> 0`.
3. Fixed-current and finite-Thevenin formulations agree as `|Z_s| -> infinity` under a controlled limit.
4. Blocking contacts give zero particle flux while allowing electrostatic displacement response.
5. Ideal reservoir densities agree with the selected carrier-statistics module.
6. Finite direct exchange approaches blocking as all exchange rates vanish.
7. Finite direct exchange approaches the ideal reservoir through a controlled fast-boundary limit.
8. Interface-state surface charge satisfies Gauss-law and surface-balance identities.
9. The assembled steady conduction current is spatially constant.
10. The later AC/stochastic total current is conduction plus displacement and is spatially constant.
11. Smith 1984 boundaries and Dember observation are recovered only in the declared quasineutral reduction.
12. Thevenin and Norton terminal representations produce identical device observables.

## 8. Configuration requirements

Every simulation configuration must state:

- left and right electrostatic conditions;
- left and right electron and hole contact models;
- contact statistics and reservoir temperature;
- terminal ensemble;
- external source/load impedance;
- sign of positive terminal current;
- whether interface storage is dynamic or eliminated;
- whether a boundary is a reference physics model or a reduced benchmark.

The label “ohmic contact” without these fields is insufficient.

## 9. Current decision

Accepted as the deterministic hierarchy:

- Fermi-level-pinned reservoir;
- nonlinear finite exchange;
- explicit dynamic interface state;
- blocking flux;
- pair surface recombination;
- Smith effective finite-`S` benchmark;
- voltage, current, open-circuit, and finite-load terminal ensembles.

Material-specific HgCdTe barrier and interface-rate parameters remain unresolved and are not authorized for predictive calculations.