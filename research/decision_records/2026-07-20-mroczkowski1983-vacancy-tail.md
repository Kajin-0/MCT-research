# Mroczkowski 1983 vacancy-conditioned absorption-tail constraint

**Date:** 2026-07-20  
**Source:** DOI `10.1116/1.572210`

## Question

Does the 1983 fixed-composition experiment provide evidence that Hg-vacancy acceptor state changes the optical absorption-edge tail, and what authority can be assigned without the primary full text?

## Verified source identity

The AIP issue record verifies:

```text
J. A. Mroczkowski
D. A. Nelson
R. Murosako
P. H. Zimmermann
Optical absorption edge in Hg0.7Cd0.3Te
Journal of Vacuum Science & Technology A 1, 1756-1760 (1983)
DOI 10.1116/1.572210
```

The publisher abstract is recovered. The primary full text is not.

## Exact abstract-level observations

The source studies high-purity and stoichiometrically doped p-type material at fixed nominal composition `x=0.3`. It reports an exponential edge form:

```text
alpha_e = alpha_0 exp[k(E-E_0)]
```

and attributes the broadening to valence-band tailing associated with native Hg-vacancy acceptor defects.

Exact reported values available from the publisher abstract are:

```text
high-purity ambient-temperature slope k      148 eV^-1
vacancy-rich/doped slope k                    105 eV^-1
reported acceptor concentration               approximately 2e16 cm^-3
```

The accessible abstract does not provide numerical temperature in kelvin, composition uncertainty, specimen count, fit window, slope uncertainty, or same-specimen lineage.

## Derived diagnostics

The characteristic exponential e-fold energy is `1/k`:

```text
high-purity state           6.7567568 meV
vacancy-rich state          9.5238095 meV
difference                  2.7670528 meV
width ratio                 1.4095238
width increase              40.95238%
slope decrease              29.05405%
```

These are exact transformations of the reported slopes. `1/k` is not a band-gap shift and carries no independently reported measurement uncertainty.

## Decision

Authorized:

- classify the source as `vacancy_conditioned_exponential_tail_slope` evidence;
- preserve the sign and reported magnitude of vacancy-conditioned tail broadening at fixed nominal composition;
- strengthen the priority of an achieved, continuously measured vacancy-state covariate in the paired acquisition protocol;
- prioritize recovery of the primary full text.

Unauthorized:

- implement a complete absorption operator from the abstract;
- convert `1/k` into a latent-gap correction;
- fit a universal vacancy coefficient;
- assign uncertainty absent from the publisher abstract;
- claim same-specimen, matched-specimen, or independently controlled causality;
- pool these slopes with magneto-optical or fixed-threshold gap observations;
- use the abstract endpoints in uncertainty-weighted fitting.

## Reopening gate

A quantitative state-effect model requires recovery of:

1. specimen inventory and lineage;
2. measurement temperature for each endpoint;
3. acceptor-density assignment for each state;
4. growth, anneal, or stoichiometric-processing history;
5. composition method and uncertainty;
6. spectral fit windows and slope uncertainties;
7. comparison design identifying same, matched, or independent specimens.

## Program consequence

The historical evidence now supports the paired protocol's vacancy-state factor independently of the modern synthetic identifiability calculation. The appropriate response is to measure vacancy state directly and preserve its covariance with carrier density and composition—not to apply a literature-derived universal correction.
