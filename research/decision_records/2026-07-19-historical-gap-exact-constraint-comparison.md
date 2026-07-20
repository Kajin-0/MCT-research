# Historical exact-constraint comparison

Date: 2026-07-19  
Controlling issue: #132

## Question

Do the exact, non-digitized historical observations recovered in tranche 1 identify one preferred HgCdTe material-gap equation?

## Inputs

The comparison keeps four observation classes separate:

- 56 Schmit-Stelzer half-peak detector cutoffs;
- the McCombe combined-resonance gap fit;
- the Groves same-specimen 4 K and 77 K sign constraints;
- the Groves HgTe magnetoreflectance endpoint observations.

Candidate equations are Schmit-Stelzer 1969, Hansen 1982, published Seiler 1990, reconstructed Laurenti, provisional Hansen-Pade, and Chu 1983.

## Results

### Detector-cutoff class

Using the fit-adjusted compositions reported by Schmit and Stelzer, their own equation has a mean absolute residual of 1.778 meV over the 56 half-peak detector cutoffs. This is a reconstruction of the observation class on the compositions adjusted during the original fit and is not independent material-law validation.

Among the other comparators, Chu 1983 has the smallest adjusted-composition mean absolute residual, 5.094 meV. This result applies only to the historical half-peak detector-cutoff observation class.

Using nominal rather than adjusted compositions increases the Schmit-Stelzer equation's mean absolute residual from 1.778 to 7.008 meV. The composition adjustment is therefore a material part of the historical fit.

### Same-specimen sign change

For the Groves specimen interval `0.158 <= x <= 0.164`:

- Schmit-Stelzer predicts a positive gap throughout the interval at 4 K and therefore violates the reported negative sign;
- Chu crosses zero inside the composition interval and is composition-ambiguous;
- Hansen, Seiler, Laurenti, and provisional Hansen-Pade predict a negative gap throughout the interval at 4 K;
- all six equations predict a positive gap throughout the interval at 77 K.

The same-specimen sign constraint is more discriminating than a pooled mean residual because it tests a qualitative temperature-induced crossing while propagating the reported composition interval.

### McCombe point

At the reported `x=0.203` and 77 K, every equation predicts a gap above the McCombe value `64 +/- 3 meV`. The smallest absolute residual is 19.004 meV for reconstructed Laurenti.

Matching the reported value requires composition shifts of approximately `-0.011` to `-0.023`, depending on the equation. Because the pointwise absolute composition uncertainty is not reported and the gap is itself a model-conditioned combined-resonance fit, this point does not authorize a material-law ranking.

### HgTe endpoint

For the approximately 30 K HgTe magnetoreflectance result `-283 +/- 1 meV`, Hansen is the closest comparator with a residual of `-2.950 meV`. Schmit-Stelzer misses by `+48.699 meV`, demonstrating that its detector-cutoff equation should not be extrapolated to the HgTe endpoint.

The approximate 1.5 K value remains a separate low-precision endpoint record and is not averaged with the 30 K result.

## Decision

The exact historical constraints reject inappropriate equation use and distinguish observation classes, but they do not identify one universal HgCdTe material-gap law.

Authorized conclusions:

- reject Schmit-Stelzer as a 4 K sign model over the full reported Groves composition interval;
- classify Chu 1983 as composition-ambiguous for that 4 K sign constraint;
- report detector-cutoff residuals only with the fit-adjusted-composition and observation-class caveats;
- report the composition shifts required to reconcile each equation with McCombe;
- report temperature-qualified HgTe endpoint residuals;
- retain source-lineage and measurement-class separation.

Not authorized:

- pool detector cutoff, resonance, magnetoreflectance, and sign constraints as interchangeable gap points;
- select Chu globally from its detector-cutoff residual;
- select Laurenti globally from the McCombe residual;
- fit a new universal empirical coefficient set;
- promote any comparator to a production reference equation.
