# Smith (1984) equation-level audit

**Source:** D. L. Smith, “Effects of blocking contacts on generation-recombination noise and responsivity in intrinsic photoconductors,” *Journal of Applied Physics* **56**, 1663–1669 (1984).  
**DOI:** `10.1063/1.334155`  
**Verification status:** user-supplied publisher PDF inspected in full; finite-contact boundary equations, Green-function conditions, terminal-voltage observable, noise formulation, limiting behavior, and HgCdTe calculations verified.

## 1. Model class

The paper extends Smith's 1982 quasineutral ambipolar photoconductor model from perfectly recombining contacts to finite contact recombination velocities.

Geometry:

- one-dimensional detector;
- contacts at `x=-L` and `x=+L`;
- length `2L`, width `W`, thickness `d`;
- optional displaced optical aperture;
- n-type intrinsic photoconductor in the explicit derivation.

The excess electron and hole densities are constrained to be equal and are represented by one ambipolar population `Delta P(x,t)`. No Poisson equation or separate bipolar transport is solved.

## 2. Mean transport and finite-contact boundary conditions

Equation (1a) is

\[
\left(
\partial_t+\tau^{-1}+\mu E\partial_x-D\partial_x^2
\right)\Delta P(x,t)=f.
\]

The finite-contact boundary conditions are Eqs. (1b)-(1c):

\[
\left(D\partial_x-\mu E\right)\Delta P
=S'\Delta P
\qquad (x=-L),
\]

\[
-\left(D\partial_x-\mu E\right)\Delta P
=S\Delta P
\qquad (x=+L).
\]

Here `S'` and `S` are recombination velocities at the left and right contacts.

The paper explicitly identifies the limits:

- `S,S' -> 0`: perfectly blocking minority-carrier contacts;
- `S,S' -> infinity`: ohmic/high-recombination contacts, for which `Delta P(+-L)->0`.

Under positive field in n-type material, the negative contact at `+L` dominates minority-carrier loss; left-right contact asymmetry is therefore physically important.

## 3. Green-function boundary conditions

The Green function satisfies Eq. (4a) with Robin conditions Eqs. (4b)-(4c):

\[
\partial_xK
=\frac{S'+\mu E}{D}K
\qquad(x=-L),
\]

\[
\partial_xK
=-\frac{S-\mu E}{D}K
\qquad(x=+L).
\]

The paper gives the closed frequency-domain Green function in Eqs. (6a)-(6h). These equations are a direct analytical benchmark for a finite-volume or finite-element implementation of deterministic ambipolar Robin boundaries.

## 4. Terminal-voltage observable and Dember term

The device is treated under constant current. Integrating the current-density equation yields Eq. (3):

\[
\Delta V(t)=
-\frac{V(b+1)}{p_0+bn_0}
\left[
\frac{1}{2L}\int_{-L}^{L}\Delta P(x,t)dx
+
\frac{k_BT}{qV}\frac{b-1}{b+1}
\left(\Delta P(L,t)-\Delta P(-L,t)\right)
\right].
\]

The second term is a Dember/diffusion contribution. It vanishes for absorbing ohmic contacts and for equal electron and hole mobilities, but remains for finite blocking contacts.

This demonstrates that finite-contact terminal voltage is not determined only by the spatially averaged excess density.

## 5. Noise representation

The paper carries forward the Smith 1982 population-covariance and Green-function treatment. The terminal noise is expressed through:

- the finite-contact Green function;
- thermal equilibrium minority population `p_0`;
- background-generated carrier profile `P_B(x)`;
- spatial response functions `Q(omega)`, `theta(omega)`, `Z(x,omega)`, and `F(omega)`;
- additional boundary-density terms caused by the Dember contribution.

Crucially, the paper introduces **no independent stochastic contact injection, extraction, or interfacial-trap source**. Contact recombination velocity modifies the deterministic operator and observation kernel only.

Therefore Smith 1984 establishes finite deterministic contact velocity in HgCdTe GR-noise theory, but it does not close the stochastic contact covariance required by R06 equilibrium fluctuation-dissipation consistency.

## 6. Physical results

For decreasing contact recombination velocity:

- minority-carrier sweepout decreases;
- effective carrier survival increases;
- responsivity increases;
- thermal GR noise increases;
- background GR noise increases faster than thermal noise;
- both responsivity and GR noise roll off at lower frequency;
- detectivity moves toward the background-limited value when background noise dominates.

The paper emphasizes that blocking is far more consequential at the downstream/negative contact under bias.

## 7. HgCdTe specialization

The numerical example uses approximately:

- `x approximately 0.20` HgCdTe;
- `T=77 K`;
- detector length `34 micrometers`;
- width `50 micrometers`;
- thickness `10 micrometers`;
- `mu_n approximately 2e5 cm^2/(V s)`;
- `mu_p approximately 500 cm^2/(V s)`;
- background flux `1e17 photons/(cm^2 s)`.

The calculations show strong response changes once `S` falls below several thousand `cm/s`, with example highly blocking cases near `100 cm/s`.

The reported doping and composition windows are model-conditioned engineering examples, not universal HgCdTe limits.

## 8. Limitations

- quasineutral ambipolar state;
- low-level excess population;
- no self-consistent Poisson electrostatics;
- no separate electron and hole continuity equations;
- no explicit bulk trap state;
- constant current and voltage-noise observable;
- deterministic Robin contacts only;
- no contact shot/exchange noise;
- no equilibrium terminal FDT demonstration;
- one-dimensional end contacts; lateral planar-contact transport is represented only effectively through `S`.

## 9. Required R06 benchmark

R06 must reproduce:

1. Eqs. (1a)-(1c);
2. the Green-function Robin conditions Eqs. (4b)-(4c);
3. the `S->0` blocking and `S->infinity` absorbing limits;
4. the Dember boundary contribution to terminal voltage;
5. the stronger influence of the negative contact under drift;
6. the trend toward lower rolloff frequency as `S` decreases;
7. the relative scaling of thermal and background components.

The benchmark must then show what changes when the same finite mean boundary is supplemented by a thermodynamically consistent forward/reverse contact-event covariance.

## 10. Contact-novelty consequence

Smith 1984 resolves a key question from the initial audit:

> The paper uses a deterministic contact recombination velocity but does not include an explicit stochastic contact exchange source.

Accordingly:

- finite deterministic `S` is not a novelty basis;
- blocking-contact effects on HgCdTe noise and responsivity are not new;
- a stochastic finite-contact closure recovering equilibrium FDT remains a candidate contribution, subject to comparison with Park 2022 and broader contact-noise literature.

## 11. Revised R06 position

The paper's most important role is as the finite-`S`, quasineutral HgCdTe benchmark. R06 should quantify the error introduced by this reduction when Poisson screening, separate bipolar transport, explicit trap kinetics, stochastic contact exchange, and the external circuit are restored.