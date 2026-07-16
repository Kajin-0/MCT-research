# Insight 0014 — Endpoint experiments should precede endpoint AHC

**Status:** exact comparison of the two executable historical equations.  
**Novelty status:** research-design result, not a new bandgap law.  
**Decision use:** identify questions that do not justify first-principles computation.

## 1. CdTe endpoint predictions

At $x=1$, Hansen becomes

$$
E_g^{\mathrm H}(1,T)=1.650-5.35\times10^{-4}T,
$$

while Laurenti becomes

$$
E_g^{\mathrm L}(1,T)=1.606
-3.25\times10^{-4}\frac{T^2}{T+78.7}.
$$

The two equations differ in both their zero-temperature intercept and thermal law.

| $T$ | Hansen $E_g$ | Laurenti $E_g$ | Laurenti − Hansen |
|---:|---:|---:|---:|
| 0 K | 1.6500 eV | 1.6060 eV | $-44.0$ meV |
| 20 K | 1.6393 eV | 1.6047 eV | $-34.6$ meV |
| 77 K | 1.6088 eV | 1.5936 eV | $-15.2$ meV |
| 120 K | 1.5858 eV | 1.5824 eV | $-3.4$ meV |
| 200 K | 1.5430 eV | 1.5594 eV | $+16.4$ meV |
| 300 K | 1.4895 eV | 1.5288 eV | $+39.3$ meV |

Absolute gap comparison mixes the zero-temperature intercept with the thermal dependence. The cleaner observable is the within-specimen thermal shift.

## 2. Within-specimen thermal shifts

Define

$$
\Delta_T E_g(T;T_0)=E_g(T)-E_g(T_0).
$$

With $T_0=0$:

| Interval | Hansen shift | Laurenti shift | Difference in predicted shift |
|---|---:|---:|---:|
| 0–20 K | $-10.70$ meV | $-1.32$ meV | $+9.38$ meV |
| 0–77 K | $-41.20$ meV | $-12.38$ meV | $+28.82$ meV |
| 0–120 K | $-64.20$ meV | $-23.55$ meV | $+40.65$ meV |
| 0–300 K | $-160.50$ meV | $-77.24$ meV | $+83.26$ meV |

These separations are far larger than the meV-scale accuracy sought for a future analytical HgCdTe equation.

Therefore:

> A first-principles calculation is not needed to decide whether the Hansen or Laurenti CdTe endpoint thermal law is closer to experiment. A provenance-controlled experimental CdTe temperature series should decide that first.

## 3. Why within-specimen differences are preferable

For one specimen, the thermal increment removes any temperature-independent calibration offset:

$$
[E_g^{\mathrm{obs}}(T)-E_g^{\mathrm{obs}}(T_0)]
=
[E_g^{\mathrm{true}}(T)-E_g^{\mathrm{true}}(T_0)]
+[\epsilon(T)-\epsilon(T_0)].
$$

It also reduces sensitivity to uncertain absolute composition at a binary endpoint. The remaining issues are:

- observable definition, such as excitonic transition versus fundamental quasiparticle gap;
- thermal expansion and strain;
- temperature calibration;
- sample-dependent defect or doping shifts;
- uncertainty correlation across the temperature series.

These are experimental-provenance questions, not reasons to begin AHC prematurely.

## 4. Consequence for the first CdTe calculation

The first CdTe AHC calculation must **not** ask:

> Which legacy equation gives the better total CdTe gap shift?

That question is already experimentally decidable with a coarse temperature series.

A justified calculation would instead ask a decomposition question unavailable from total-gap experiments, for example:

$$
\Delta E_g^{\mathrm{ep,fixed\ volume}}(T)
$$

versus

$$
\Delta E_g^{\mathrm{QH}}(T),
$$

or whether one effective phonon scale can reproduce the calculated fixed-volume curvature within a stated tolerance.

## 5. Computation gate

Before authorizing CdTe AHC:

1. acquire a primary bulk-CdTe temperature-dependent gap dataset;
2. separate exciton-transition energy from the fundamental gap where possible;
3. determine the experimental thermal shift and uncertainty;
4. fit Hansen, Laurenti, one-oscillator, and constrained empirical forms;
5. identify a remaining decomposition or curvature ambiguity that experiments alone cannot resolve;
6. set the calculation accuracy from that model separation.

If experimental data already determine the total thermal law and no microscopic decomposition is required for the analytical successor, endpoint AHC should be stopped.

## 6. Broader breadth-first rule

The same principle applies throughout this project:

- use equations to locate large, cheap experimental discriminants;
- use experiments to eliminate model branches;
- reserve first-principles calculations for latent physical quantities that experiments cannot isolate;
- stop computation when its uncertainty exceeds the separation between surviving hypotheses.

This is the intended breadth-first progression from evidence to analytical model to narrowly justified computation.
