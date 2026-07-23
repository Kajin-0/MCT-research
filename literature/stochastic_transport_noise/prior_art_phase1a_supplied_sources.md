# R06 Phase 1A supplied-source conclusions

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Date:** 2026-07-23  
**Status:** equation-level audit increment; Park 2022 remains outstanding

## 1. Sources added at full-text level

The user supplied readable full papers for:

1. Shockley and Read (1952), DOI `10.1103/PhysRev.87.835`;
2. Smith (1982), DOI `10.1063/1.330006`;
3. Smith (1984), DOI `10.1063/1.334155`;
4. Iverson and Smith (1985), DOI `10.1063/1.335666`;
5. Bulashenko et al. (1998), DOI `10.1063/1.367023`;
6. Zocchi (2006), DOI `10.1103/PhysRevB.73.035203`.

The files themselves are not committed because redistribution rights are not established. Equation-level source notes and conclusions are committed.

## 2. Strongest novelty constraint: Zocchi (2006)

Zocchi treats a finite one-dimensional n-doped semiconductor with:

- electron drift and diffusion;
- dynamic ionized traps;
- linearized Poisson space-charge feedback;
- dielectric relaxation;
- independent Poisson generation and recombination processes;
- fixed-voltage current-noise boundary conditions;
- open-circuit voltage-noise boundary conditions;
- conduction plus displacement current in the terminal current;
- full-frequency finite-length spectra.

The paper obtains a long-sample Lorentzian as a limit, finite-size spectra controlled by diffusion and electrostatic time scales, and a high-frequency open-circuit voltage PSD proportional to `f^-7/2`.

### Consequence

The following broad claim is no longer defensible:

> A finite semiconductor with drift, diffusion, Poisson coupling, dynamic traps, and terminal current/voltage noise has not been treated at full frequency.

It has been treated in a unipolar uniform-material form. R06 must contribute a controlled extension or reduction-error result, not the governing-equation combination.

## 3. HgCdTe analytical lineage: Smith 1982-1985

### Smith (1982)

Smith establishes a quasineutral ambipolar model for finite intrinsic photoconductors with:

- drift and diffusion;
- absorbing contacts;
- thermal and optical-background populations;
- a spatial covariance proportional to local minority-carrier density;
- correlation between fluctuation probability and survival time;
- constant-current terminal voltage noise.

The paper predicts non-Lorentzian frequency behavior. Its high-frequency voltage-noise amplitudes scale as:

\[
V_{N,th}\propto\omega^{-3/4},
\qquad
V_{N,bg}\propto\omega^{-1},
\]

corresponding to PSD slopes `-3/2` and `-2`.

### Smith (1984)

Smith replaces absorbing contacts with finite deterministic Robin conditions:

\[
(D\partial_x-\mu E)\Delta P=S'\Delta P
\quad(x=-L),
\]

\[
-(D\partial_x-\mu E)\Delta P=S\Delta P
\quad(x=+L).
\]

The terminal-voltage observable also acquires a boundary Dember term. The paper establishes blocking and absorbing limits and shows that smaller `S` increases responsivity and noise while lowering rolloff frequency.

No explicit stochastic injection/extraction or contact-event source is included. The contact velocity modifies the deterministic operator and the propagated population covariance.

### Iverson and Smith (1985)

Iverson and Smith add explicit two-state deep-level dynamics to the quasineutral HgCdTe model. They verify:

- four capture/emission rates;
- correlated free-electron and charged-trap populations;
- a distinct bound/free thermal-noise contribution;
- trap-modified mobility, diffusion, lifetime, and sweepout;
- terminal rolloff that cannot be assigned to one bare microscopic lifetime.

### Consequence

R06 cannot claim novelty for:

- finite HgCdTe drift-diffusion GR-noise theory;
- finite deterministic contact recombination velocity;
- blocking-contact modification of responsivity and noise;
- non-Lorentzian spatial transport spectra;
- explicit deep-trap dynamics;
- correlated trap/carrier population fluctuations;
- a trap-generated thermal-noise component.

The Smith lineage becomes a mandatory controlled-reduction benchmark.

## 4. Shockley-Read kinetic consequence

Shockley and Read identify four primitive channels:

1. electron capture;
2. electron emission;
3. hole capture;
4. hole emission.

The algebraic SRH law follows only after solving the steady trap occupancy. At equilibrium, the net SRH rate vanishes while the primitive forward and reverse rates remain nonzero.

### Consequence

The R06 stochastic source cannot be based on `R_SRH`, `|R_SRH|`, or `2R_SRH`. It must be assembled as

\[
Q_{SRH}=\sum_r\nu_r\nu_r^Ta_r
\]

from the four positive propensities. Explicit trap occupancy remains the reference state until a stochastic adiabatic elimination is proven.

## 5. Bulashenko equilibrium-transfer consequence

Bulashenko et al. establish the impedance-field representation

\[
S_V=A\int|\nabla Z(x)|^2K(x)dx
\]

for an inhomogeneous drift-diffusion junction. In equilibrium, electrostatic and sample-contact cross terms are required to recover

\[
s_V^{eq}(x)=4k_BTR(x).
\]

### Consequence

A local source-intensity plot is not a terminal-noise contribution plot. R06 must preserve state-observation cross covariance and verify direct-versus-adjoint terminal spectra.

## 6. Revised contact comparison

| Model | Mean contact condition | Explicit stochastic contact source | FDT contact closure |
|---|---|---:|---:|
| Smith 1982 | absorbing Dirichlet | no | no |
| Smith 1984 | finite Robin `S` | no | no |
| Iverson-Smith 1985 | absorbing Dirichlet | no | no |
| Zocchi 2006 | ideal absorbing or open-current ensemble | no | no |
| R06 provisional closure | forward/reverse reservoir exchange giving Robin mean | yes | required |
| Park 2022 | pending full-text audit | unresolved | unresolved |

Smith 1984 therefore supports, but does not prove, the candidate gap: a finite stochastic contact boundary whose mean is a recombination-velocity condition and whose covariance follows detailed balance.

## 7. Revised spectral novelty boundary

Unusual non-Lorentzian slopes are not automatically new:

- Smith 1982 gives PSD slopes `-3/2` and `-2` in different components;
- Zocchi 2006 gives an open-circuit high-frequency PSD slope `-7/2`;
- Bulashenko shows junction-weighting and cross-term structure.

A proposed apparent `1/f^alpha` result must therefore specify:

1. the exact finite bandwidth;
2. local log-slope tolerance;
3. number and origin of modes;
4. distinction from known asymptotic diffusion laws;
5. exclusion of broad trap distributions, surface shunts, and circuit poles.

## 8. Remaining candidate outputs

After the supplied-source audit, the strongest viable outputs are:

1. a thermodynamically complete finite stochastic-contact boundary, if not already supplied by Park 2022;
2. a quantitative error map between full bipolar drift-diffusion-Poisson-trap dynamics and the Smith quasineutral ambipolar reductions;
3. a criterion for when a terminal corner differs from bulk, SRH, trap, transit, contact, or dielectric time scales by more than a declared tolerance;
4. an uncertainty-qualified HgCdTe regime map;
5. a rigorous finite-band result for apparent power-law behavior that is distinct from known diffusion asymptotes.

## 9. Gate status

The complete broad-theory novelty hypothesis is rejected with high confidence.

Phase 1A continues for one decisive source comparison:

- Park 2022, DOI `10.1063/5.0111954`.

Production sweeps remain unauthorized. Analytical benchmark transcription, contact comparison, and implementation test design remain authorized.