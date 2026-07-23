# R06 supplied-source benchmark targets

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** analytical target specification; no production sweep authorized

## 1. Purpose

This document translates the user-supplied source papers into explicit verification targets for a later solver. The benchmark is considered passed only when the project convention is translated to the paper convention before comparison.

## 2. Convention precheck

Before source-specific comparisons:

1. identify whether the paper reports amplitude spectral density or PSD;
2. identify one-sided versus two-sided normalization;
3. identify hertz versus angular frequency;
4. reproduce the paper's variance integral;
5. apply geometry conversion between volume density and linear density;
6. match terminal ensemble exactly.

No numerical factor may be fitted after the comparison.

## 3. Shockley-Read four-channel kinetic benchmark

### State

Use local electron density `n`, hole density `p`, total trap density `N_t`, and occupied fraction `f_t`.

### Propensities

\[
a_{nc}=c_n nN_t(1-f_t),
\]

\[
a_{ne}=c_n n_1N_tf_t,
\]

\[
a_{pc}=c_p pN_tf_t,
\]

\[
a_{pe}=c_p p_1N_t(1-f_t).
\]

### Required steady occupancy

\[
f_t^*
=
\frac{c_nn+c_pp_1}
{c_n(n+n_1)+c_p(p+p_1)}.
\]

### Required net rate

\[
R_{SRH}
=
\frac{c_nc_pN_t(np-n_i^2)}
{c_n(n+n_1)+c_p(p+p_1)}.
\]

### Acceptance metrics

\[
\epsilon_f
=
\frac{|f_t^{num}-f_t^*|}{\max(f_t^*,10^{-30})}
<10^{-10},
\]

\[
\epsilon_R
=
\frac{|R^{num}-R_{SRH}|}
{\max(|R_{SRH}|,R_{scale}10^{-14})}
<10^{-10}.
\]

At equilibrium:

\[
np=n_i^2,
\qquad
R_{SRH}=0,
\]

but all permitted primitive rates remain nonnegative and generally nonzero.

The local stoichiometric covariance must be positive semidefinite to numerical precision.

## 4. Smith 1982 absorbing-contact benchmark

### Operator

\[
\mathcal L_S
=
\partial_t+\tau^{-1}+\mu E\partial_x-D\partial_x^2.
\]

### Boundary conditions

\[
\Delta P(-L,t)=\Delta P(L,t)=0.
\]

### Instantaneous covariance

\[
C_P(x,x')
=
\frac{p_0+P_B(x)}{Wd}\delta(x-x').
\]

### Required low-frequency spatial-correlation limits

Let `L_D=sqrt(D tau)`.

- diffusion length much greater than half-length:

\[
F(0)\rightarrow\frac65;
\]

- bulk-like long device:

\[
F(0)\rightarrow1;
\]

- high-field sweepout:

\[
F(0)\rightarrow\frac23.
\]

### Required high-frequency PSD slopes

Fit the local log slope over a converged asymptotic interval:

\[
\alpha_{th}
=-\frac{d\log S_{V,th}}{d\log\omega}
\rightarrow\frac32,
\]

\[
\alpha_{bg}
=-\frac{d\log S_{V,bg}}{d\log\omega}
\rightarrow2.
\]

Acceptance target:

\[
|\alpha_{num}-\alpha_{source}|<0.03
\]

over at least one decade after demonstrating mesh and frequency-window convergence.

### Drift-only zero removal

A diffusion-free reduced model contains exact spectral zeros. Any finite positive diffusion coefficient must remove those exact zeros. The numerical minimum must converge to a nonzero value rather than a mesh-dependent zero.

## 5. Smith 1984 finite-contact benchmark

### Mean boundary conditions

\[
(D\partial_x-\mu E)\Delta P=S'\Delta P
\quad(x=-L),
\]

\[
-(D\partial_x-\mu E)\Delta P=S\Delta P
\quad(x=+L).
\]

### Green-function boundary conditions

\[
\partial_xK
=\frac{S'+\mu E}{D}K
\quad(x=-L),
\]

\[
\partial_xK
=-\frac{S-\mu E}{D}K
\quad(x=+L).
\]

### Required limiting behavior

- `S,S' -> infinity`: Smith 1982 absorbing-contact spectrum;
- `S,S' -> 0`: zero minority-carrier particle flux;
- positive field in n-type material: sensitivity to `S` at `+L` exceeds sensitivity to `S'` at `-L` in the drift-dominated regime.

### Terminal observation

The constant-current voltage operator must include the finite-contact Dember boundary term proportional to

\[
\Delta P(L)-\Delta P(-L).
\]

Suppressing this term is permitted only for the exact symmetry or absorbing-contact limits in which it vanishes.

### Trend checks

For otherwise fixed parameters, decreasing symmetric `S` must produce:

1. increased low-frequency responsivity;
2. increased thermal GR noise;
3. a faster increase of background GR noise than thermal GR noise;
4. lower rolloff frequency;
5. approach toward background-limited detectivity when the background component dominates.

These are monotonic/trend benchmarks before exact figure reproduction.

## 6. Iverson-Smith dynamic-trap benchmark

### Quasineutral relation

\[
\Delta p+\Delta N^+=\Delta n.
\]

### Trap rates

\[
r_e=B_enN^+,
\qquad
r_h=B_hp(N_T-N^+),
\]

\[
g_h=B_hp_1N^+,
\qquad
 g_e=B_en_1(N_T-N^+).
\]

### Zero-time covariance targets

\[
\langle\Delta n(x)\Delta n(x')\rangle
=
\frac{\mathcal N^+(x)+p(x)}{Wd}\delta(x-x'),
\]

\[
\langle\Delta N^+(x)\Delta n(x')\rangle
=
\frac{\mathcal N^+(x)}{Wd}\delta(x-x'),
\]

\[
\langle\Delta n(x)\Delta p(x')\rangle
=
\frac{p(x)}{Wd}\delta(x-x'),
\]

\[
\langle\Delta N^+(x)\Delta p(x')\rangle=0,
\]

with

\[
\mathcal N^+=N^+\left(1-\frac{N^+}{N_T}\right).
\]

### Required source decomposition

The terminal spectrum must be decomposable into:

1. band-to-band thermal GR;
2. background photon generation;
3. bound/free trap exchange.

The event-level R06 covariance passes the reduced benchmark only if its equilibrium state covariance reproduces the equations above.

### Transport trend

When minority trapping is strengthened, effective mobility and diffusivity must decrease and sweepout-related rolloff must shift to lower frequency.

## 7. Zocchi full-frequency unipolar benchmark

### Linearized equations

\[
\partial_t n
=D\partial_x^2n+\mu E_e\partial_xn
+\mu N_0\partial_xE_i
-\frac{n}{\tau_N}-\frac{n_T}{\tau_T}+\Delta g_r,
\]

\[
\partial_t n_T
=-\frac{n_T}{\tau_T}-\frac{n}{\tau_N}+\Delta g_r,
\]

\[
\partial_xE_i=\frac{q}{A\varepsilon}(n_T-n).
\]

### Source

Generation and recombination are independent equilibrium Poisson processes with equal mean `g_0`. After convention translation, the difference source must reproduce the paper's `4g_0` spectrum.

### Fixed-voltage ensemble

\[
n(0,t)=n(L,t)=0,
\]

\[
\int_0^LE_i(x,t)dx=0.
\]

The terminal current is initially evaluated as

\[
i(t)=\frac1L\int_0^L
\left[-qj+A\varepsilon\partial_tE_i\right]dx,
\]

and must reduce numerically to

\[
i(t)=\frac{q\mu E_e}{L}\int_0^Ln(x,t)dx.
\]

Define

\[
\epsilon_{I,reduce}
=
\frac{|I_{full}-I_{reduced}|}
{\max(|I_{full}|,I_{scale}10^{-14})}.
\]

Target: `<1e-10` in the continuous-equation manufactured test and `<1e-7` after spatial discretization.

### Open-circuit zero-field ensemble

Use zero terminal current and the corresponding Neumann carrier conditions. This is a separate solve, not `S_V=R^2S_I`.

### Time scales

\[
\tau^{-1}=\tau_N^{-1}+\tau_T^{-1},
\]

\[
\tau_\varepsilon^{-1}=\frac{q\mu N_0}{A\varepsilon}.
\]

The finite-size transfer parameter is

\[
\xi^2(s)
=
\frac{L^2\tau_T}{D\tau_\varepsilon\tau}
\frac{(1+s\tau_\varepsilon)(1+s\tau)}{1+s\tau_T}.
\]

### Required limits

1. long sample current noise -> Lorentzian with `tau`;
2. low-field current PSD proportional to `V^2`;
3. high-field current PSD saturation;
4. finite-size curves collapse under the source dimensionless variables;
5. long-sample open-circuit voltage PSD high-frequency slope:

\[
-\frac{d\log S_V}{d\log f}
\rightarrow\frac72.
\]

Acceptance slope tolerance: `0.05` over at least one converged decade.

## 8. Bulashenko impedance-field benchmark

### Local source

After unit and convention translation:

\[
K(x)=4q^2n(x)D(x).
\]

### Terminal voltage PSD

\[
S_V=A\int|\nabla Z(x)|^2K(x)dx.
\]

### Equilibrium decomposition

Reproduce the separate local terms corresponding to `s_1`, `s_2`, and `s_3`. The sum must satisfy

\[
s_V^{eq}(x)=4k_BTR(x).
\]

Required test:

- with cross terms enabled: `epsilon_FDT < 1e-4` after convergence;
- with cross terms deliberately removed: the test must fail near the junction by an amount well above numerical tolerance.

This is a negative-control benchmark proving that the test can detect an incomplete observation covariance.

## 9. Contact-event extension benchmark

After reproducing Smith 1984 with contact-event noise disabled, enable the R06 forward/reverse contact closure while retaining the same mean Robin boundary.

Define

\[
\Delta_S(f)
=
\frac{S_{event}(f)-S_{Smith}(f)}
{S_{event}(f)}.
\]

Map `Delta_S` against:

- `Bi=SL/D`;
- `L/L_D`;
- terminal ensemble;
- contact asymmetry;
- carrier density;
- contact area;
- frequency.

The event closure must satisfy equilibrium FDT without an additive Johnson source.

## 10. Benchmark ordering

The implementation order is mandatory:

1. Shockley-Read local kinetics;
2. Smith 1982 absorbing quasineutral transport;
3. Smith 1984 deterministic finite contacts;
4. Iverson-Smith dynamic trap state;
5. Zocchi unipolar Poisson and terminal ensembles;
6. Bulashenko direct/adjoint and FDT cross terms;
7. R06 stochastic finite-contact extension;
8. full bipolar HgCdTe model.

A later stage is not accepted if an earlier source limit fails.