# R06 Phase 1A stochastic-contact closure gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Decision:** accept a forward/reverse reservoir-exchange model as the provisional thermodynamic reference; quantitative HgCdTe contact use remains unauthorized

## Accepted project derivation

For carrier species `s` at contact `c`, define forward injection and reverse extraction propensities per unit area,

\[
a_{s,c}^{in},
\qquad
a_{s,c}^{out}.
\]

The mean outward particle flux is

\[
\overline{\Gamma}_{s,c}^{out}
=a_{s,c}^{out}-a_{s,c}^{in},
\]

while the area-averaged primitive flux covariance is proportional to their sum,

\[
Q_{s,c}^{\Gamma}
=
\frac{a_{s,c}^{out}+a_{s,c}^{in}}{A_c}.
\]

For the classical finite-velocity reference closure,

\[
a_{s,c}^{out}=S_{s,c}c_s,
\qquad
a_{s,c}^{in}=S_{s,c}c_{s,c}^{eq}.
\]

This gives

\[
\overline{\Gamma}_{s,c}^{out}
=S_{s,c}(c_s-c_{s,c}^{eq}),
\]

and at equilibrium,

\[
Q_{s,c,eq}^{\Gamma}
=
\frac{2S_{s,c}c_{s,c}^{eq}}{A_c}.
\]

The equilibrium factor of two arises from equal forward and reverse event activity and is distinct from PSD convention factors.

## Required implementation rule

The same primitive boundary event must generate:

- the boundary-cell population source;
- the direct terminal transferred-charge contribution;
- their cross covariance.

Independent contact-density and contact-current noise sources would double count the same event.

## Physical distinctions retained

The project must distinguish:

1. independent electron and hole exchange with a reservoir;
2. electron-hole pair recombination/generation at an interface;
3. exchange mediated by a dynamic interface trap;
4. displacement current at a particle-blocking contact.

A single deterministic surface-recombination velocity does not determine which stochastic closure applies.

## Limiting decisions

- `S -> 0`: particle-exchange mean and primitive exchange noise vanish, but displacement-current coupling may remain.
- `S -> infinity`: the fast reservoir limit requires finite-rate convergence or stochastic adiabatic elimination; setting Dirichlet density and deleting contact noise is not accepted.
- equilibrium: terminal FDT must emerge from the complete bulk/contact/circuit covariance without a post hoc Johnson source.

## Authorization

Authorized:

- use this closure to design finite-volume and finite-element boundary source assembly;
- derive the fast-reservoir elimination;
- test blocking, finite-exchange, and reservoir limits analytically;
- compare with Park 2022 and Smith 1984 once full papers are supplied.

Not authorized:

- treat `S c` exchange as a validated HgCdTe metal-contact model;
- claim the closure is novel;
- begin production sweeps;
- omit interface-state dynamics where source evidence requires them.

## Falsification rule

Revise or reject the closure if full prior art supplies a different thermodynamically complete boundary, if equilibrium FDT cannot be recovered without an added source, or if an energy-resolved degenerate contact model produces material changes over the intended HgCdTe regime.