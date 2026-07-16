# Pre-computation decision gate

**Status:** mandatory before any production AHC, dense EPW, VCA, SQS, or CPA campaign  
**Current gate:** closed

A calculation is authorized only when the memo below is completed for one narrow physical question. “Generate first-principles insight” is not a sufficiently specific question.

## Decision memo template

### 1. Unresolved physical quantity

State one quantity with units and operational definition, for example:

$$
\Delta E_g^{\mathrm{ep}}(x,T)
$$

at a specified $x$, $T$, volume, gap definition, and electronic starting point.

Do not combine gap shift, Kane velocity, disorder broadening, and thermal expansion into one pilot.

### 2. Competing hypotheses

List mutually discriminable hypotheses. Example:

- H0: the Hansen linear temperature term is adequate within experimental uncertainty over the target range;
- H1: one effective phonon scale produces resolvable low-temperature curvature;
- H2: two separated phonon scales are required;
- H3: measurement/source heterogeneity is larger than the functional-form difference.

### 3. Minimum required accuracy

Derive the accuracy from the difference between hypotheses, not from an aspirational round number:

$$
\sigma_{\mathrm{calc}}
\le
\frac{|Q_{H_i}-Q_{H_j}|}{K},
$$

with a declared discrimination factor $K$ such as 3.

The generic target of $1\ \mathrm{meV}$ is provisional. If competing analytical models differ by only $0.3\ \mathrm{meV}$, a $1\ \mathrm{meV}$ calculation is uninformative. If they differ by tens of meV, existing experiments may be sufficient and no calculation is justified.

### 4. Expected information gained

Specify which model parameter, Bayes factor, cross-validation error, or hypothesis decision will change after the calculation.

A valid answer has the form:

> The CdTe calculation estimates the sign and magnitude of the low-temperature fixed-volume curvature strongly enough to accept or reject the one-oscillator scale inferred from experiment.

An invalid answer is:

> It will improve our understanding of HgCdTe.

### 5. Smallest discriminating calculation

Declare:

- material;
- structure and volume;
- electronic method;
- pseudopotential identity;
- band and phonon quantities;
- smallest candidate $k/q$ grids;
- temperature points;
- adiabatic/nonadiabatic treatment;
- Fan/Debye–Waller scope;
- convergence sequence;
- observables exported.

The first justified material remains CdTe. HgTe is gated behind successful CdTe verification.

### 6. Approximate cost

Report ranges rather than false precision:

| Resource | Pilot estimate | Production estimate | Basis |
|---|---:|---:|---|
| CPU/GPU hours | pending | pending | timed static/DFPT pilot |
| peak memory | pending | pending | measured per rank/node |
| scratch storage | pending | pending | wavefunction/DDB/e-ph files |
| wall time | pending | pending | declared hardware |
| human analysis time | pending | pending | conversion and convergence review |

No production estimate is accepted before at least one timed pilot with the selected pseudopotentials and code release.

### 7. Stopping result

State the result that would terminate deeper computation. Examples:

- complete Fan + Debye–Waller corrections cannot be converged below the model-separation scale at feasible cost;
- CdTe cross-code results disagree beyond the declared tolerance with no identifiable convention difference;
- the experimental benchmark shows no resolvable low-temperature curvature;
- a one-oscillator model already saturates held-out error at the data uncertainty floor;
- the required full matrix self-energy is unavailable from the chosen stack;
- the electronic starting-point uncertainty exceeds the electron–phonon effect being tested.

A calculation with no stopping result is exploratory infrastructure, not a decision experiment.

## Current project decision

### Resolved model-separation fact

At the CdTe endpoint, the two executable historical equations predict thermal shifts from 0 to 77 K of

$$
\Delta E_g^{\mathrm H}=-41.20\ \mathrm{meV},
$$

and

$$
\Delta E_g^{\mathrm L}=-12.38\ \mathrm{meV}.
$$

Their predicted thermal shifts differ by

$$
\boxed{28.82\ \mathrm{meV}}
$$

at 77 K and by

$$
\boxed{83.26\ \mathrm{meV}}
$$

at 300 K.

These differences are large enough that a provenance-controlled bulk-CdTe experimental temperature series should decide which total-gap law is closer without first-principles computation.

### Question that does **not** justify AHC

> Is Hansen or Laurenti closer to the total experimental CdTe gap shift?

This is experimentally decidable and should be answered from primary data first.

### Candidate quantity that may justify AHC later

A narrower latent quantity unavailable from total-gap experiments may justify calculation:

$$
\Delta E_g^{\mathrm{ep,fixed\ volume}}(T),
$$

separated from

$$
\Delta E_g^{\mathrm{QH}}(T).
$$

The purpose would be to determine whether a compact one-effective-phonon or spectral-moment description reproduces the fixed-volume electron–phonon contribution, not merely to generate another total-gap curve.

### Missing prerequisites

- primary bulk-CdTe temperature-dependent gap data with observable definition and uncertainty;
- separation or accounting of excitonic transition energy versus fundamental quasiparticle gap;
- a fit of Hansen, Laurenti, and oscillator models to the same CdTe data;
- estimate of the remaining fixed-volume versus quasiharmonic ambiguity in meV;
- full-text audit of the 1995 HgCdTe electron–phonon method;
- exact pseudopotential files and timed pilot cost.

### Gate outcome

$$
\boxed{\text{Do not begin production AHC or dense EPW calculations yet.}}
$$

The first calculation memo may be opened only after endpoint experimental evidence identifies a microscopic decomposition question that survives model fitting. If experimental data alone saturate the analytical need, the CdTe AHC branch should stop.
