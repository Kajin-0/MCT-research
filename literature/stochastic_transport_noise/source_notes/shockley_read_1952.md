# Shockley and Read (1952) equation-level audit

**Source:** W. Shockley and W. T. Read, Jr., “Statistics of the Recombinations of Holes and Electrons,” *Physical Review* **87**, 835–842 (1952).  
**DOI:** `10.1103/PhysRev.87.835`  
**Verification status:** user-supplied journal PDF inspected in full; four transition channels, detailed-balance relations, nondegenerate reduction, steady trap occupancy, and net recombination law verified.

## 1. Physical state model

The paper assumes one trap family whose charge can occupy two states differing by one electronic charge. Figure 1 identifies four primitive processes:

1. electron capture from the conduction band;
2. electron emission to the conduction band;
3. hole capture, equivalently annihilation of a trapped electron with a valence-band hole;
4. hole emission, equivalently capture of a valence-band electron and creation of a hole.

The paper assumes that internal relaxation inside a trapped excited state is fast compared with capture and emission. Thus a single trap-occupancy state is sufficient.

This is the authoritative kinetic basis for the R06 four-channel trap event model.

## 2. Detailed balance before the nondegenerate approximation

For electron exchange, the paper writes the energy-resolved capture and emission rates in Eqs. (2.5)-(2.8). Equilibrium detailed balance gives Eq. (2.9), relating the emission and capture constants through the trap and band energies.

The important structural result is:

- capture and emission remain distinct nonzero processes at equilibrium;
- their **difference** determines mean net transfer;
- their **sum** determines event activity and therefore stochastic covariance in an event-level extension.

The last statement is an R06 derivation from the verified kinetic channels; the 1952 paper itself is a mean-rate theory and does not derive a noise covariance.

## 3. Nondegenerate transition rates

In the paper's nondegenerate notation, Eqs. (3.8)-(3.9) can be written in modern volumetric form as four positive propensities:

\[
a_{nc}=c_n n N_t(1-f_t),
\]

\[
a_{ne}=c_n n_1 N_t f_t,
\]

\[
a_{pc}=c_p p N_t f_t,
\]

\[
a_{pe}=c_p p_1 N_t(1-f_t),
\]

where:

- `f_t` is the electron-occupied trap fraction;
- `c_n`, `c_p` are electron and hole capture coefficients;
- `n_1`, `p_1` are the equilibrium band densities associated with the trap energy.

The net trap-occupancy equation is therefore

\[
N_t\partial_t f_t
=a_{nc}+a_{pe}-a_{ne}-a_{pc}.
\]

The electron and hole continuity reaction terms must use the same primitive channels and stoichiometry.

## 4. Steady trap occupancy

Equating the net electron and hole capture rates gives the steady occupied and empty fractions in Eqs. (4.2)-(4.3). In modern notation,

\[
f_t
=
\frac{c_n n+c_p p_1}
{c_n(n+n_1)+c_p(p+p_1)},
\]

\[
1-f_t
=
\frac{c_n n_1+c_p p}
{c_n(n+n_1)+c_p(p+p_1)}.
\]

These formulas are derived from the four forward/reverse channels, not postulated from a lifetime.

## 5. Net SRH recombination law

Substitution of the steady occupancy into the transition rates yields Eq. (4.4). In modern notation,

\[
R_{SRH}
=
\frac{c_n c_p N_t(np-n_1p_1)}
{c_n(n+n_1)+c_p(p+p_1)}.
\]

Since

\[
n_1p_1=n_i^2,
\]

this is equivalent to the conventional lifetime form

\[
R_{SRH}
=
\frac{np-n_i^2}
{\tau_p(n+n_1)+\tau_n(p+p_1)},
\]

with

\[
\tau_n=(c_nN_t)^{-1},
\qquad
\tau_p=(c_pN_t)^{-1}.
\]

The net rate vanishes at equilibrium even though all four primitive event rates can remain finite.

## 6. Stochastic consequence

The paper does **not** justify using any of the following as a white-noise intensity:

- `R_SRH`;
- `abs(R_SRH)`;
- `2 R_SRH`.

An event-level stochastic extension must instead use the four propensities separately. For a state vector containing electron number, hole number, and occupied traps, a consistent stoichiometry is:

| Event | State change `(Delta n, Delta p, Delta N_t^occ)` |
|---|---|
| electron capture | `(-1, 0, +1)` |
| electron emission | `(+1, 0, -1)` |
| hole capture | `(0, -1, -1)` |
| hole emission | `(0, +1, +1)` |

The local reaction covariance is then the project derivation

\[
Q_{SRH}
=
\sum_{r\in\{nc,ne,pc,pe\}}
\nu_r\nu_r^T a_r.
\]

This automatically includes carrier-trap cross correlations and remains nonzero at thermal equilibrium.

## 7. Adiabatic elimination warning

Shockley and Read solve the steady trap occupancy to obtain the algebraic net recombination law. That operation does not prove that trap occupancy can be removed from a frequency-dependent stochastic model.

Eliminating `f_t(t)` dynamically generally creates:

- a memory kernel;
- colored effective carrier noise;
- carrier-carrier and carrier-trap cross correlations;
- an additional relaxation pole.

R06 must retain explicit trap occupancy in the reference model until a controlled stochastic elimination is derived.

## 8. Statistics regime

The paper begins with Fermi-Dirac occupation factors and then specializes to nondegenerate conduction- and valence-band populations in Section 3.

Therefore the common SRH formula above is source-supported for the nondegenerate carrier approximation. Quantitative use in degenerate or strongly nonparabolic HgCdTe requires revised band-state integrals and generalized emission/capture relations.

## 9. Limitations

- spatially local mean kinetics only;
- no drift, diffusion, Poisson equation, contacts, or terminal observable;
- no stochastic Langevin covariance;
- one trap family with two charge states;
- fast internal trap relaxation;
- the closed algebraic SRH law assumes steady trap occupancy.

## 10. R06 acceptance rule

The stochastic SRH module is accepted only if it:

1. implements all four positive propensities;
2. recovers the Shockley-Read steady occupancy;
3. recovers Eq. (4.4) in steady state;
4. satisfies detailed balance at equilibrium;
5. produces a positive-semidefinite stoichiometric covariance;
6. retains nonzero equilibrium reaction activity;
7. reduces to algebraic SRH only under a quantified time-scale separation.

## 11. Novelty consequence

Neither the algebraic SRH law nor explicit four-channel trap kinetics is novel. A possible R06 contribution lies in embedding those verified kinetics into a finite bipolar drift-diffusion-Poisson/contact model and quantifying the failure of steady algebraic lifetime interpretations in terminal noise.