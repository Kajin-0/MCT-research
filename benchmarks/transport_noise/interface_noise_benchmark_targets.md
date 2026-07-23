# R06 stochastic-interface benchmark targets

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Issues:** #341 and #343  
**Status:** source-derived analytical specification; executable implementation deferred to Phase 3

## 1. Purpose

These benchmarks translate the two full 1998 interface-noise papers into explicit acceptance tests for the R06 stochastic boundary implementation.

Primary sources:

1. G. Gomila and J. M. Rubí, *Physica A* **258**, 17–31 (1998), DOI `10.1016/S0378-4371(98)00199-X`.
2. G. Gomila, O. M. Bulashenko, and J. M. Rubí, *Journal of Applied Physics* **83**, 2619–2630 (1998), DOI `10.1063/1.367024`.

The tests separate primitive event covariance from cross terms generated after transfer to a terminal observable.

## 2. I0 — ideal activated interface event

### Model

Two reservoirs or material regions exchange one carrier through

\[
q_1\rightleftharpoons q_2.
\]

Define activities

\[
a_+=\lambda_{12}z_1,
\qquad
a_-=\lambda_{21}z_2.
\]

The reference mean and covariance are

\[
\bar J=a_+-a_-,
\]

\[
Q_J=\frac{a_++a_-}{A}.
\]

### Acceptance tests

1. The assembled covariance is nonnegative for all `a_+,a_- >= 0`.
2. At detailed balance `a_+=a_-`, mean current is zero and covariance remains finite.
3. In a one-way limit `a_-/a_+ -> 0`, the Fano ratio tends to the Poisson value after charge and PSD convention conversion.
4. Reversing interface orientation changes the mean sign but not the covariance.
5. State and terminal feed-through blocks generated from the same event are rank-one and positive semidefinite.

## 3. I1 — nonlinear generalized fluctuation relation

Let `[F]` be the electrochemical-potential discontinuity in the source convention. The ideal-interface source gives

\[
\bar J=-\frac{1}{T}M([F]),
\]

and

\[
Q_J
=
\frac{1}{A}
\frac{1}{T}M([F])
\coth\!\left(\frac{\beta[F]}{2}\right).
\]

### Acceptance tests

1. Direct event-sum and `coth` forms agree numerically.
2. The apparent `0/0` limit at `[F]=0` is evaluated analytically or with a stable series expansion.
3. The linear-response limit recovers

\[
Q_{J,eq}=\frac{2k_BL}{A},
\]

where `L` is the source Onsager coefficient.
4. Entropy production remains nonnegative under the selected force and flux orientation.

## 4. I2 — ideal metal-semiconductor interface

The source boundary is

\[
J_n
=
\frac{\lambda_{21}^{MS}}{N_C}(n_m-n)+\xi,
\]

with

\[
n_m=N_Ce^{-q\beta\phi_{bn}}.
\]

The source covariance is

\[
Q_\xi
=
\frac{1}{qA}
[-q\bar J_n+2I_s]
\]

in the source orientation.

### Acceptance tests

1. Translate this expression into the project outward-flux convention and recover the event sum.
2. At equilibrium recover zero mean and finite covariance.
3. At large forward or reverse bias recover the appropriate one-way shot-noise limit.
4. Under a Boltzmann density law, linearization reproduces the classical contact Onsager coefficient.
5. Under generalized statistics, replacing `n/(k_BT)` by `partial n/partial mu` preserves equilibrium FDT.

## 5. I3 — nonideal interface with one state population

Primitive processes are

\[
q_1\rightleftharpoons q_s,
\qquad
q_2\rightleftharpoons q_s,
\qquad
q_1\rightleftharpoons q_2.
\]

Each process has event activity

\[
Q_{ij}
=
\frac{\lambda_{ij}z_i+\lambda_{ji}z_j}{A}.
\]

Composite currents are assembled from the primitive event incidence matrix.

### Acceptance tests

1. Construct the full covariance as

\[
Q=B\,\mathrm{diag}(Q_{12},Q_{1s},Q_{2s})B^T.
\]

2. Recover the source composite cross covariance

\[
Q_{ns}
=
\frac{\lambda_{s2}z_s+\lambda_{2s}z_2}{A}.
\]

3. Verify that `Q` is positive semidefinite for random positive rates.
4. Verify exact charge/current conservation for every primitive event column of `B`.
5. Verify that deleting the off-diagonal covariance changes the terminal PSD and equilibrium covariance.
6. Recover the ideal-interface limit as interface-state coupling tends to zero.

## 6. I4 — dynamic interface-state elimination

Let the interface-state occupancy perturbation satisfy

\[
(i\omega C_s+G_s)\delta f_s
=B_s\delta u+\eta_s.
\]

Eliminating it gives a reduced boundary admittance and effective source:

\[
Y_{eff}(\omega)
=Y_0-B_{us}(i\omega C_s+G_s)^{-1}B_{su},
\]

\[
\eta_{eff}(\omega)
=
\eta_u-B_{us}(i\omega C_s+G_s)^{-1}\eta_s.
\]

### Acceptance tests

1. The reduced covariance includes the induced colored term and cross terms.
2. Direct explicit-state and eliminated-state terminal spectra agree to relative error `<1e-8` for a small analytical system.
3. In the fast-state limit, the colored covariance approaches the correct white reduced limit over fixed finite frequency.
4. In the slow-state limit, an additional interface pole appears explicitly.
5. A deterministic `S` boundary is accepted only where the reduced covariance and admittance errors are both below the declared tolerance.

## 7. S0 — Schottky thermionic source

For the source paper’s current orientation,

\[
S_{I_c}=2q(I+2I_c),
\qquad
I_c=qn_0^{eq}v_rA.
\]

### Acceptance tests

1. At equilibrium recover `S_Ic=4qI_c`.
2. At one-way high current recover `S_Ic/(2q|I|) -> 1`.
3. With

\[
R_c=\frac{k_BT}{qI_c},
\]

recover

\[
R_c^2S_{I_c}=4k_BTR_c.
\]

4. Confirm that the result is obtained from the stochastic boundary, not by adding terminal shot noise after solving the device.

## 8. S1 — Schottky bulk transfer and cross term

At equilibrium define

\[
a(x)=\frac{r(x)}{r(0)}.
\]

The source gives

\[
s_{Vdep}=4k_BT a^2R,
\]

\[
s_{Vser}=4k_BT(1-a)^2R,
\]

\[
s_{Vcros}=8k_BT a(1-a)R.
\]

### Acceptance tests

1. Verify pointwise

\[
s_{Vdep}+s_{Vser}+s_{Vcros}=4k_BTR.
\]

2. Delete `s_Vcros` deliberately and confirm a nonzero pointwise FDT defect

\[
\Delta s_V=-8k_BT a(1-a)R.
\]

3. Confirm that the cross term arises from a shared distributed bulk source and two transfer components, not from primitive thermionic-bulk source covariance.
4. Recover total equilibrium terminal noise

\[
S_V=4k_BT(R_c+R_{dep}+R_{ser}).
\]

## 9. S2 — thermionic versus diffusion control

Define

\[
\beta_c=\frac{\mu E_{th}}{v_r},
\qquad
E_{th}=\frac{k_BT}{qL_D}.
\]

### Acceptance tests

1. `beta_c <= 10^-2`: diffusion-limited benchmark.
2. `beta_c >= 10^2`: thermionic-emission-limited benchmark.
3. `0.1 <= beta_c <= 10`: mixed benchmark.
4. Verify that similar I-V shapes can coexist with distinct local impedance/noise decompositions.
5. Report the fraction

\[
\eta_{cross}=\frac{S_{Vcros}}{S_V}
\]

as a function of bias and `beta_c`.

The numerical thresholds above are benchmark sampling choices, not source-defined phase boundaries.

## 10. S3 — frequency limitation

The Schottky source model is intended for the low-frequency plateau above `1/f` noise and below dielectric relaxation.

### Acceptance tests

1. Reproduce the quasistatic source benchmark when `omega tau_dr << 1`.
2. Demonstrate departure from the quasistatic formula as `omega tau_dr` approaches unity in the full R06 solver.
3. Do not treat the Schottky formula as a full-frequency contact PSD without deriving the frequency-dependent interface model.

## 11. R0 — deterministic finite-velocity reduction error

Compare:

1. explicit interface-event model;
2. explicit interface-state model;
3. stochastic reduced boundary after elimination;
4. deterministic Robin boundary with no contact covariance.

For observable `Y`, define

\[
\epsilon_Y(\omega)
=
\frac{|Y_{reduced}(\omega)-Y_{reference}(\omega)|}
{\max(|Y_{reference}(\omega)|,Y_{floor})}.
\]

Required observables:

- DC current;
- differential resistance;
- responsivity;
- terminal current PSD;
- terminal voltage PSD;
- dominant pole or fitted corner;
- inferred lifetime.

Regime boundaries should be reported for at least `epsilon_Y=0.01`, `0.05`, and `0.10`.

## 12. Novelty gate

Passing these benchmarks does not establish novelty. It establishes correct implementation of prior interface-noise theory.

A paper-level R06 contribution requires at least one new quantitative reduction boundary or asymptotic error result that remains robust under HgCdTe parameter uncertainty.