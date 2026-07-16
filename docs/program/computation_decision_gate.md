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

The current generic target of $1\ \mathrm{meV}$ is provisional. If competing analytical models differ by only $0.3\ \mathrm{meV}$, a $1\ \mathrm{meV}$ calculation is uninformative. If they differ by $10\ \mathrm{meV}$, sub-meV convergence may be unnecessary for the pilot.

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

### Unresolved quantity

Not yet sufficiently narrowed. Candidate quantities include the low-temperature curvature of $E_g(T)$ in CdTe and the fixed-volume electron–phonon contribution to the HgCdTe temperature coefficient.

### Missing prerequisites

- primary Hansen data reconstruction;
- later independent experimental datasets with compatible gap definitions;
- prior-art audit of analytical phonon-based HgCdTe equations;
- benchmark estimate of model separation in meV;
- exact pseudopotential files and pilot timing.

### Gate outcome

$$
\boxed{\text{Do not begin production AHC or dense EPW calculations yet.}}
$$

The next decision memo should be completed only after the analytical benchmark identifies where experimental models disagree enough for a CdTe calculation to be informative.
