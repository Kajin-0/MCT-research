# Insight 0019 — Laurenti’s finite-temperature mass table is model propagation, not independent validation

**Status:** primary-source interpretation; mathematical dependency established; independent mass validation not supplied by the table

## Observation

Laurenti et al. publish both:

1. an empirical temperature- and composition-dependent gap equation; and
2. a table of conduction-band-edge effective masses $m^*(x,T)$.

The paper derives the mass through a five-band $k\cdot p$ expression using the empirical gap and additional band parameters. The Table V values are therefore downstream predictions of the same analytical closure, not independent effective-mass measurements.

## Dependency structure

A reduced multiband mass law has the schematic form

$$
\frac{m_0}{m^*(x,T)}
=
1+
\sum_r
\frac{W_r(x,T)}{E_{\Gamma_6}(x,T)-E_r(x,T)},
$$

where $W_r$ contains momentum-matrix-element information and the denominators contain the empirical gap and remote-band separations.

If the matrix elements and remote-band rules are fixed or composition interpolated, much of the reported temperature dependence of $m^*$ is inherited from $E_g(x,T)$ itself.

Consequently,

$$
E_g(x,T)\longrightarrow m^*_{\mathrm{model}}(x,T)
$$

is one prediction chain, not two statistically independent observations.

## Prior-art consequence

The following is established prior art:

> propagate an empirical HgCdTe gap law through a multiband $k\cdot p$ expression to obtain a temperature-dependent effective mass.

Therefore, a future claim that “the new gap equation also predicts $m^*(T)$” is not novel by itself.

## What remains scientifically differentiating

A matrix electron–phonon calculation could add new information by independently resolving

$$
P(T),\quad \Delta(T),\quad F(T),\quad \gamma_i(T),
$$

rather than assuming that mass changes arise only through $E_g(T)$.

The relevant comparison is

$$
m^*_{\mathrm{full}}(T)
\quad\text{versus}\quad
m^*_{E_g\text{-only}}(T),
$$

where the second curve freezes all non-gap Kane parameters.

Define

$$
\Delta m^*_{\mathrm{non-gap}}(T)
=
m^*_{\mathrm{full}}(T)-m^*_{E_g\text{-only}}(T).
$$

A statistically resolved nonzero value would demonstrate finite-temperature information not contained in a scalar bandgap equation.

## Falsification test

The stronger program fails to add mass information if, within numerical and experimental uncertainty,

$$
\Delta m^*_{\mathrm{non-gap}}(T)=0
$$

throughout the tested composition and temperature domain.

In that case, a scalar $E_g(x,T)$ law plus established multiband parameters would be sufficient for the mass observable, and complete matrix renormalization would not be justified by effective-mass prediction alone.

## Data rule

`data/laurenti/laurenti1990_table5_effective_mass_grid.csv` must be classified as `model_derived_kp_effective_mass`. It must not be scored as an independent experimental holdout against the Laurenti gap equation that generated it.
