# Insight 0015 — A low-temperature turnover requires competing signed thermal channels

**Status:** exact structural result plus one historical microscopic-model diagnostic  
**Novelty status:** the monotonicity proof is elementary; the HgCdTe research implication is candidate and unconfirmed experimentally  
**Primary source:** Krishnamurthy et al. (1995), Table II, Hg$_{0.78}$Cd$_{0.22}$Te

## 1. Published microscopic-model behavior

Krishnamurthy et al. tabulate a calculated finite-temperature gap for Hg$_{0.78}$Cd$_{0.22}$Te:

| $T$ | Calculated $E_g$ |
|---:|---:|
| 1 K | 113.60 meV |
| 10 K | 112.67 meV |
| 20 K | 112.56 meV |
| 30 K | 114.44 meV |
| 100 K | 139.17 meV |
| 300 K | 218.66 meV |

The tabulated curve falls by

$$
E_g(20)-E_g(1)=-1.04\ \mathrm{meV}
$$

and then rises, crossing above the 1 K value by 30 K. The table therefore contains a shallow minimum near 20 K.

This is a prediction of the historical HPTB electron–phonon treatment, not a resolved experimental result. The paper’s broader gap agreement is at approximately the 10–15 meV level, much larger than the 1.04 meV turnover. The feature must therefore be treated as a **model-generated hypothesis**, not established HgCdTe physics.

## 2. Hansen cannot represent a turnover

For Hansen,

$$
E_g^{\mathrm H}(x,T)=P_3(x)+aT(1-2x),
$$

so

$$
\frac{\partial E_g^{\mathrm H}}{\partial T}=a(1-2x)
$$

has one fixed sign at each composition. At $x=0.22$, the gap is strictly increasing with temperature.

Relative to 1 K, Hansen predicts

| $T$ | $\Delta E_g^{\mathrm H}(T;1\ \mathrm K)$ |
|---:|---:|
| 10 K | +2.70 meV |
| 20 K | +5.69 meV |
| 30 K | +8.69 meV |
| 100 K | +29.66 meV |
| 300 K | +89.58 meV |

At 20 K, this differs from the historical microscopic table by 6.73 meV in thermal shift.

## 3. Laurenti cannot represent a turnover either

Laurenti has the thermal term

$$
\Delta E_g^{\mathrm L}(x,T)
=C(x)\frac{T^2}{T+B(x)},
$$

where $B(x)>0$. Its derivative is

$$
\frac{\partial \Delta E_g^{\mathrm L}}{\partial T}
=C(x)\frac{T(T+2B)}{(T+B)^2}.
$$

For every $T>0$, its sign is exactly the sign of $C(x)$. Thus the Laurenti curve is also monotonic at each fixed composition unless $C(x)=0$ identically.

At $x=0.22$, Laurenti predicts

| $T$ | $\Delta E_g^{\mathrm L}(T;1\ \mathrm K)$ |
|---:|---:|
| 10 K | +0.87 meV |
| 20 K | +2.76 meV |
| 30 K | +5.11 meV |
| 100 K | +25.27 meV |
| 300 K | +87.89 meV |

At 20 K, this differs from the historical microscopic table by 3.80 meV in thermal shift.

## 4. One effective oscillator is also monotonic

For a single Bose–Einstein channel,

$$
\Delta E_g(T)
=A\left[
\coth\left(\frac{\Theta}{2T}\right)-1
\right]
=2A n_B(\Theta,T),
$$

where $n_B$ is the Bose occupation. Since $n_B$ increases monotonically with $T$, the sign of

$$
\frac{d\Delta E_g}{dT}
$$

is fixed by $A$. One oscillator cannot generate a finite-temperature minimum or maximum.

## 5. Minimum analytical structure for a turnover

A turnover requires at least two temperature-dependent contributions with opposite signed derivatives over some range. A physically interpretable form is

$$
E_g(x,T)=E_g(x,0)
+\sum_j 2A_j(x)n_B\!\left(\Theta_j(x),T\right)
+\Delta E_g^{\mathrm{QH}}(x,T),
$$

with either

$$
A_iA_j<0
$$

for two phonon channels, or an electron–phonon contribution opposed by the quasiharmonic term.

An extremum at $T_*$ satisfies

$$
\sum_j 2A_j(x)
\frac{\partial n_B(\Theta_j,T_*)}{\partial T}
+rac{\partial \Delta E_g^{\mathrm{QH}}}{\partial T}(x,T_*)=0.
$$

This equation gives a direct connection between an observed turnover and a cancellation of signed spectral moments.

## 6. Why this matters for the proposed analytical successor

The first nontrivial question is no longer merely whether HgCdTe exhibits low-temperature curvature. Laurenti already establishes curvature as prior art. The stronger question is:

> Does a provenance-controlled HgCdTe temperature series exhibit a statistically resolved change in the sign of $dE_g/dT$ at fixed composition?

If yes, all single-sign one-scale equations—including Hansen, Laurenti, and a one-effective-oscillator model—are structurally inadequate. A two-channel or explicitly separated electron–phonon/quasiharmonic model becomes necessary rather than merely more flexible.

If no experimentally resolved turnover exists, the 1 meV dip in the 1995 table should be treated as below the historical model’s accuracy and should not motivate a more complicated equation.

## 7. Falsification requirements

A credible turnover claim requires:

1. repeated measurements on one specimen below approximately 40 K;
2. independently calibrated composition and strain;
3. one consistent gap observable across temperature;
4. energy uncertainty comfortably below 1 meV, or a larger observed reversal;
5. temperature calibration fine enough to locate the extremum;
6. evidence that an excitonic or edge-fitting artifact does not change sign over the same range;
7. comparison with a constant-composition latent-variable model.

The current result is therefore a **high-value experimental target**, not yet a new HgCdTe bandgap law.
