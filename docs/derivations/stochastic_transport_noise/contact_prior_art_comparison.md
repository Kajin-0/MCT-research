# R06 contact-boundary prior-art comparison

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** Smith and Zocchi comparison complete; Park 2022 pending

## 1. Purpose

The phrase “contact recombination velocity” does not uniquely define a stochastic boundary. This document compares the exact mean and fluctuation treatments in the acquired source papers with the provisional R06 forward/reverse event closure.

## 2. Smith (1982): absorbing contact

Smith 1982 uses the quasineutral ambipolar equation

\[
(\partial_t+\tau^{-1}+\mu E\partial_x-D\partial_x^2)\Delta P=f
\]

with

\[
\Delta P(-L,t)=\Delta P(L,t)=0.
\]

The contact is an ideal high-recombination sink. Fluctuations are introduced through the instantaneous bulk population covariance

\[
\langle\Delta P(x,0)\Delta P(x',0)\rangle
=\frac{p_0+P_B(x)}{Wd}\delta(x-x').
\]

There is no separate stochastic contact event.

### Interpretation

The absorbing boundary removes excess population deterministically. It is a reduced reservoir limit, not an explicit thermodynamic contact model.

## 3. Smith (1984): finite deterministic Robin contact

Smith 1984 uses

\[
(D\partial_x-\mu E)\Delta P=S'\Delta P
\quad(x=-L),
\]

\[
-(D\partial_x-\mu E)\Delta P=S\Delta P
\quad(x=+L).
\]

These equations interpolate between:

\[
S\rightarrow0
\quad\text{blocking},
\]

and

\[
S\rightarrow\infty
\quad\text{absorbing/ohmic}.
\]

The Green function obeys the corresponding Robin conditions. The terminal voltage contains both a spatial-average term and a boundary Dember term.

The noise remains based on thermal and background bulk population fluctuations propagated by the finite-`S` Green function. No independent injection, extraction, interfacial recombination, or contact shot-noise process is specified.

### Interpretation

Smith 1984 establishes the deterministic finite-`S` benchmark. It does not determine the equilibrium contact covariance associated with that dissipation.

## 4. Iverson and Smith (1985): dynamic bulk trap, ideal contact

Iverson and Smith retain explicit bulk deep-level dynamics but impose that all excess populations vanish at the contacts. Their additional covariance is a bulk free/bound population covariance, not a contact covariance.

### Interpretation

Dynamic traps and contact exchange are distinct physical source families. The Iverson-Smith trap source cannot be reused as a contact source.

## 5. Zocchi (2006): terminal ensemble boundaries

For fixed-voltage current noise, Zocchi imposes

\[
n(0,t)=n(L,t)=0,
\qquad
\int_0^LE_i(x,t)dx=0.
\]

For zero-field open-circuit voltage noise, the boundary current vanishes and the reduced carrier transfer problem has Neumann conditions.

The only primitive stochastic input is the bulk generation-minus-recombination process. No independent contact-event source is included.

### Interpretation

Zocchi rigorously distinguishes terminal ensembles, but the ideal boundaries do not supply finite-contact detailed balance.

## 6. Bulashenko et al. (1998): interface transfer cross terms

Bulashenko's “sample-contact” or junction cross terms arise from the electrostatic transfer field of an inhomogeneous junction. They are required to recover Nyquist noise, but they are not particle exchange propensities at a finite-recombination boundary.

### Interpretation

R06 must retain both:

1. contact-event state/terminal cross covariance;
2. electrostatic transfer cross terms.

They represent different correlations and must not be conflated.

## 7. R06 provisional event closure

For species `s` at contact `c`, define positive injection and extraction propensities per area:

\[
a_{s,c}^{in},
\qquad
a_{s,c}^{out}.
\]

The mean outward particle flux is

\[
\overline\Gamma_{s,c}^{out}
=a_{s,c}^{out}-a_{s,c}^{in},
\]

and the primitive flux covariance is

\[
Q_{s,c}^{\Gamma}
=\frac{a_{s,c}^{out}+a_{s,c}^{in}}{A_c}.
\]

For the classical reference model,

\[
a^{out}=Sc,
\qquad
a^{in}=Sc_{eq},
\]

so

\[
\overline\Gamma^{out}=S(c-c_{eq}),
\]

and at equilibrium

\[
Q_{eq}^{\Gamma}=\frac{2Sc_{eq}}{A_c}.
\]

The same event must enter:

- the boundary population state;
- terminal transferred charge;
- state-terminal cross covariance.

The closure is a project derivation, not yet a validated HgCdTe contact model.

## 8. Comparison table

| Source/model | Mean boundary | Fluctuation source | Contact detailed balance | Terminal cross covariance |
|---|---|---|---:|---:|
| Smith 1982 | absorbing Dirichlet | bulk population covariance | no | no explicit event channel |
| Smith 1984 | finite Robin `S` | bulk population covariance through finite-`S` Green function | no | Dember observation term, but no contact event covariance |
| Iverson-Smith 1985 | absorbing Dirichlet | bulk band, background, and trap population covariance | no | no contact event channel |
| Zocchi 2006 | ideal absorbing or zero-current ensemble | bulk Poisson GR process | no | conduction/displacement terminal observation only |
| Bulashenko 1998 | embedded inhomogeneous junction | local diffusion source plus transfer cross terms | not a finite-`S` exchange model | yes, electrostatic transfer cross terms |
| R06 provisional | forward/reverse exchange yielding Robin mean | sum of exchange propensities | yes by construction | required from the same primitive event |
| Park 2022 | pending full text | unresolved | unresolved | unresolved |

## 9. Benchmark implications

### B6a: deterministic Smith boundary

Recover Smith's Robin Green function and terminal Dember term with contact noise disabled.

### B6b: equilibrium event closure

Enable forward/reverse exchange and verify:

\[
\epsilon_{FDT}(\omega)
=
\frac{|S_I-4k_BT\operatorname{Re}Y|}
{4k_BT\operatorname{Re}Y}
\rightarrow0
\]

under refinement.

### B6c: model difference

Define

\[
\Delta_S(\omega)
=\frac{S_{terminal}^{event}(\omega)-S_{terminal}^{Smith}(\omega)}
{S_{terminal}^{event}(\omega)}.
\]

Map `Delta_S` against:

- contact Biot number;
- screening ratio;
- carrier density;
- contact area;
- terminal ensemble;
- frequency;
- contact asymmetry.

### B6d: fast-reservoir limit

Demonstrate convergence of a large finite exchange rate or derive stochastic elimination. Imposing a Dirichlet density and simply deleting the reservoir source is not accepted without proof.

## 10. Remaining prior-art gate

Park 2022, DOI `10.1063/5.0111954`, is the decisive remaining source. The candidate contact contribution survives only if Park does not already provide a thermodynamically complete stochastic finite-velocity boundary with the same limiting and FDT properties.