# Decision memo: first CdTe fixed-volume thermal-moment pilot

**Decision status:** authorize a syntax-checked, timed coarse-grid pilot only.  
**Production AHC status:** not authorized.  
**HgTe, VCA, SQS, CPA, SCBA and dense EPW status:** gated.

## 1. Unresolved physical quantity

The total experimental CdTe gap curve is not the target. Existing measurements should determine that more cheaply than first-principles computation.

The unresolved quantity is the fixed-volume electron-phonon contribution resolved by band edge and phonon mode:

$$
\Delta_T E_n^{\mathrm{ep}}(T)
=
\sum_{\mathbf q\nu}
A_{n,\mathbf q\nu}
\left[
\coth\left(\frac{\Theta_{\mathbf q\nu}}{2T}\right)-1
\right],
$$

where

$$
\Theta_{\mathbf q\nu}=\frac{\hbar\omega_{\mathbf q\nu}}{k_B}.
$$

The fixed-volume gap contribution is

$$
\Delta_T E_g^{\mathrm{ep}}(T)
=
\Delta_T E_c^{\mathrm{ep}}(T)
-
\Delta_T E_v^{\mathrm{ep}}(T).
$$

The calculation must retain separate conduction- and valence-edge shifts because a small total gap change may result from cancellation of much larger edge shifts.

The mode-resolved gap weights are

$$
A_{g,\mathbf q\nu}
=
A_{c,\mathbf q\nu}-A_{v,\mathbf q\nu}.
$$

They define signed thermal moments

$$
\mu_p^{(g)}
=
\sum_{\mathbf q\nu}
A_{g,\mathbf q\nu}\Theta_{\mathbf q\nu}^{p}.
$$

The leading high-temperature slope is

$$
\boxed{
\lim_{T\rightarrow\infty}
\frac{d\Delta_T E_g^{\mathrm{ep}}}{dT}
=
2\mu_{-1}^{(g)}
}
$$

and is the first analytical quantity to compare with a compact thermal model.

## 2. Competing hypotheses

### H0: one leading thermal moment is sufficient

A one-scale or one-moment representation predicts the fixed-volume curve to within the combined numerical target over 0--300 K:

$$
\max_T
\left|
\Delta_T E_g^{\mathrm{ep}}(T)
-
\Delta_T E_{g,1}^{\mathrm{model}}(T)
\right|
\le 1.5\ \mathrm{meV}.
$$

If H0 survives held-out temperature tests, do not promote a two-oscillator physical interpretation.

### H1: a second stable moment is required

A two-moment representation improves held-out temperature prediction by at least

$$
2\ \mathrm{meV}
$$

and by more than three times the numerical comparison uncertainty. The inferred moment region must remain stable under q-grid refinement, broadening changes and an independent implementation.

### H2: signed edge cancellation produces nonmonotonic structure

The conduction and valence shifts have competing signed components that generate a resolved turnover or change in slope in the total fixed-volume gap contribution. The feature must exceed the propagated numerical uncertainty and persist under all convergence checks.

A shallow feature below the convergence floor is reported as an unresolved bound, not as a physical turnover.

## 3. Minimum outputs

The pilot must export, at minimum:

1. static SOC band-edge energies and irreducible representations;
2. phonon frequencies and stability diagnostics;
3. Fan contribution to the conduction edge;
4. Fan contribution to the valence edge;
5. Debye--Waller contribution to each edge;
6. total fixed-volume edge and gap shifts;
7. zero-point renormalization separately from finite-temperature increments;
8. mode- or frequency-binned gap-coupling weights sufficient to calculate $\mu_{-1}$ and higher moments;
9. numerical settings, pseudopotential hashes and code versions;
10. wall time, core count, memory high-water mark, scratch use and output size.

A temperature-only table without mode-resolved or frequency-binned information cannot identify spectral moments uniquely and does not satisfy the scientific objective.

## 4. Temperature set

Once the mode-resolved couplings are available, evaluating additional temperatures is inexpensive. The minimum reporting grid is

$$
T=0,\ 20,\ 50,\ 100,\ 200,\ 300\ \mathrm K.
$$

Use 0 K for zero-point separation, 20--50 K for low-temperature curvature, 100 K for the crossover region and 200--300 K for the leading thermal moment.

Additional temperatures may be evaluated from the same converged coupling data, but they do not substitute for q-grid convergence.

## 5. Required accuracy

The minimum decision accuracy is:

| Quantity | Required numerical uncertainty |
|---|---:|
| conduction-edge thermal shift at each reported temperature | $\le1.0$ meV |
| valence-edge thermal shift at each reported temperature | $\le1.0$ meV |
| total fixed-volume gap shift | $\le1.5$ meV |
| leading high-temperature slope $2\mu_{-1}^{(g)}$ | $\le0.01$ meV/K |
| independent-code total-gap difference | $\le2.0$ meV or explained |
| independent-code individual-edge difference | $\le3.0$ meV or explained |

The slope target corresponds to approximately 2 meV accumulated over a 200 K interval. A model distinction smaller than this is below the intended information scale of the pilot.

The numerical budget must include sensitivity to:

- q-grid;
- electronic k-grid;
- empty-band count or Sternheimer settings;
- nonadiabatic denominator treatment;
- polar long-range correction and cutoff;
- broadening or regularization;
- pseudopotential family and semicore partition;
- volume;
- Fan/Debye--Waller consistency.

## 6. Smallest calculation ladder

### Stage A0 -- syntax and static/phonon sanity

- one fully relativistic norm-conserving PBE pseudopotential family;
- Cd $4d$ and Te valence partition recorded explicitly;
- converged static SOC calculation;
- coarse phonons sufficient to detect instability or gross interpolation errors;
- no scientific AHC claim.

### Stage A1 -- timed coarse AHC pilot

- $4\times4\times4$ q-grid;
- one declared electronic k-grid and one denser check;
- two denominator/broadening settings;
- Fan and Debye--Waller retained separately;
- mode-resolved or frequency-binned export verified;
- purpose: measure cost, data availability and gross signal scale.

### Stage A2 -- intermediate convergence

Proceed only if A1 is physically and numerically coherent:

- $6\times6\times6$ q-grid;
- one pseudopotential/semicore sensitivity calculation;
- repeat the temperature and moment analysis;
- compare changes in each edge, total gap and $\mu_{-1}^{(g)}$.

### Stage A3 -- decision grid

Proceed only if the 4-to-6 trend is stable:

- $8\times8\times8$ q-grid;
- independent-code total correction;
- held-out one- versus two-moment comparison;
- complete uncertainty ledger.

A $10\times10\times10$ grid or dense interpolation is not automatic. It requires a stable extrapolation trend and a declared unresolved difference larger than the remaining uncertainty.

## 7. Approximate computational cost

The following values are planning priors, not allocation commitments. They must be replaced by measured A1 timing.

Let $C_4$ be the measured cost of the complete $4^3$ q-grid pilot. The first scaling prior is

$$
C_n\approx C_4\left(\frac{n}{4}\right)^3,
$$

before accounting for empty bands, parallel efficiency, polar interpolation and I/O.

For planning only, take

$$
C_4\sim500\text{--}2000\ \text{core-hours}.
$$

This gives:

| Stage | q-grid | Relative q count | Planning cost |
|---|---:|---:|---:|
| A0 | static/coarse phonons | n/a | 100--500 core-hours |
| A1 | $4^3$ | 1.00 | 500--2,000 core-hours |
| A2 | $6^3$ | 3.375 | 1,700--6,800 core-hours |
| A3 | $8^3$ | 8.00 | 4,000--16,000 core-hours |
| optional | $10^3$ | 15.625 | 8,000--31,000 core-hours |

An independent-code confirmation approximately doubles the production-stage cost. Dense EPW or equivalent interpolation is provisionally estimated at $2\times10^4$--$10^5$ core-hours depending on Wannierization, grids and convergence requirements, and is **not authorized by this memo**.

Initial resource planning should allow roughly 32--128 GB aggregate memory and 20--200 GB scratch/output per run family. These are deliberately broad priors. The A1 run must replace them with measured values.

## 8. Expected information gained

A successful pilot will determine:

1. whether the direct Fan + Debye--Waller workflow is numerically coherent for normal-gap CdTe;
2. whether the separate edge shifts are much larger than their difference;
3. the sign and magnitude of the leading fixed-volume thermal moment;
4. whether one moment is sufficient or a second stable moment is required;
5. whether a mode-resolved export exists that can constrain an analytical phonon model;
6. whether the same implementation is credible enough to approach inverted HgTe.

It will not determine the complete experimental CdTe gap curve, quasiharmonic expansion contribution, exciton binding shift or alloy disorder.

## 9. Stop conditions

Stop deeper computation and document the failure if any of the following occurs:

1. CdTe phonons are unstable or the static band ordering is incorrect under the declared setup.
2. Fan and Debye--Waller terms are not both available consistently.
3. The mode-resolved or frequency-binned export required for moments cannot be produced.
4. The $4^3\rightarrow6^3\rightarrow8^3$ sequence changes the total gap by more than 3 meV without a stable trend.
5. The individual edge shifts vary by more than 5 meV without a stable trend even when the total happens to cancel.
6. Independent implementations disagree by more than 2 meV in the total gap or 3 meV per edge after controlled settings, with no identified cause.
7. A second moment improves held-out predictions by less than 2 meV or is unstable across grids/codes. In that case retain the one-moment model or report bounds.
8. A claimed turnover is smaller than three times its propagated numerical uncertainty.
9. The scientific result reduces to reproducing the experimentally available total CdTe $E_g(T)$ curve without resolving a latent component.
10. The predicted non-gap or moment effect is smaller than the experimental/model-discrepancy floor of the intended downstream observable.

Do not respond to a failed stop condition by launching a denser calculation automatically.

## 10. HgTe gate

HgTe remains blocked until all of the following are true:

- CdTe total fixed-volume correction is converged to the stated target;
- separate edge shifts are stable;
- Fan and Debye--Waller are cross-checked;
- nonadiabatic and polar treatments are understood;
- the moment export is reproducible;
- the cost and data-volume estimates are measured;
- the independent-code comparison passes or the discrepancy is physically explained.

Only then may the project write a separate HgTe decision memo for matrix-valued AHC near inversion.

## 11. Decision

$$
\boxed{
\text{Authorize A0 and one timed A1 smoke test only.}
}
$$

Do not begin A2, A3, dense EPW, HgTe or alloy calculations until A1 results are reviewed against the stop conditions above.
