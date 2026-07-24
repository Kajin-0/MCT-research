# Lowney-Madarasz nonparabolic statistics source audit

**Program:** R06 - stochastic transport and finite-size noise  
**Phase:** 1C material-source gate  
**Controlling issue:** #346  
**Decision:** `ARCHITECTURE_RECOVERED_IMPLEMENTATION_BLOCKED_ON_SYMBOL_EXACT_TRANSCRIPTION`

## Source result

An official open NIST copy of the 1991 Seiler-Lowney-Littler-Yoon proceedings paper was recovered. It is a primary precursor to the 1992 Lowney journal paper and explicitly follows the general calculation of Madarasz and Szmulowicz.

The source fixes the following calculation architecture:

- Kane three-band `k.p` conduction-band model;
- full Fermi-Dirac statistics for conduction electrons;
- nondegenerate heavy-hole statistics;
- interactions with light-hole and split-off valence bands;
- split-off energy `Delta = 1 eV`;
- momentum matrix element `P = 8.49e-8 eV cm`;
- heavy-hole mass `m_hh = 0.55 m0`;
- Newton iteration for the reduced Fermi energy;
- integration by parts to remove a derivative from the electron-density integrand;
- direct inversion of Kane's cubic secular equation for `gamma = k^2`.

The source calculation spans approximately `0.17 <= x <= 0.30` and `4 <= T <= 300 K`.

## Verified nonlinear gap relation

The proceedings paper prints

```text
Eg = -0.302
     + 1.93*x
     - 0.810*x^2
     + 0.832*x^3
     + 5.35e-4*(1-2*x)*((-1822+T^3)/(255.2+T^2))
```

with `Eg` in eV and `T` in kelvin.

## Remaining equation-level block

The official PDF prints the charge-neutrality, integration-by-parts, and intrinsic-density equations as Eqs. (2)-(4). Automated text extraction corrupts their mathematical typography. Those equations are therefore not transcribed into executable code in this gate.

The following remain false:

```text
equation_2_charge_neutrality_symbol_level_verified  false
equation_3_integration_by_parts_symbol_level_verified false
equation_4_intrinsic_density_symbol_level_verified false
madarasz_equations_symbol_level_verified            false
lowney_1992_fit_coefficients_verified                false
source_exact_statistics_implementation_authorized   false
```

No missing symbol, prefactor, degeneracy, integration limit, or unit conversion is inferred from general Kane theory and attributed to either historical source.

## Consequence

The source gap is narrowed from an architectural gap to a transcription-and-reference-data gap. The repository now has enough primary evidence to specify the intended model, but not enough to claim a source-exact implementation.

Before implementation, the project requires:

1. visual symbol-by-symbol transcription of Eqs. (2)-(4);
2. a complete Ry/atomic-unit conversion contract;
3. independent numerical reference points for the neutrality solution and intrinsic density;
4. the verified 1992 fitted relation if the Lowney fit itself is implemented.

## Claim boundary

Supported:

- source identities and lineage;
- model architecture;
- printed parameter values;
- composition and temperature ranges;
- exact nonlinear gap equation;
- statistics and neutrality algorithm choices.

Not supported:

- source-exact Madarasz equations;
- source-exact Lowney 1992 fit;
- an intrinsic-density model comparison;
- a material-accurate HgCdTe transport closure;
- predictive detector claims.
