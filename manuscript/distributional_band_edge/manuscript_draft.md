# From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability

## Abstract

The bandgap of Hg1-xCdxTe is commonly treated as a scalar function of alloy composition and temperature. Experimental observables, however, are produced by a sequence of additional operations: local composition and gap distributions, carrier filling and many-body shifts, intrinsic and tail absorption, optical thickness, detector response, and the selected edge or cutoff criterion. We develop a distributional forward framework that keeps these layers explicit and derive several identifiability limits relevant to HgCdTe band-edge metrology. First, composition uncertainty near the normal-to-inverted transition is amplified into critical-temperature uncertainty; at mean x=0.155, existing latent-gap laws differ by 25.08 K before any specimen-distribution uncertainty is introduced. Second, a Gaussian distribution of local gaps reproduces the Herrmann approximately-s/2 apparent tail scale under source-aligned conditions, but changing only the fitted absorption window changes the inferred tail energy by 60.1%. Third, a single-pass detector cutoff on an exponential tail shifts as -W ln(d2/d1), and any number of tail-only cutoff measurements has structural Jacobian rank at most two for four nominal absorption parameters. Fourth, at a declared high-density sensitivity point representative of the Dingrong regime, a parabolic Burstein-Moss estimate exceeds a nonparabolic calculation by 147 meV; a five-density edge series is formally full rank but has condition number 1.10x10^4. Finally, we prove that a dense single-state response spectrum with parameters (Eg0, carrier translation, gap width, absorption amplitude, effective thickness) has structural rank at most three because the spectrum depends only on the translated mean gap, gap width, and amplitude-thickness product. A calibrated nontranslational carrier feature raises rank to four but leaves one combined scaling/translation invariance. These results separate structural from statistical uncertainty and define the external measurements required to recover a latent HgCdTe gap from optical data.

## 1. Introduction

Hg1-xCdxTe occupies an unusual metrological regime. Its signed zone-center gap can be tuned through zero by composition and temperature, its bands are strongly nonparabolic, and its optical edge is sensitive to carrier state, disorder, processing, thickness, and the analysis operator. The same material can therefore be assigned different quantities called “the bandgap” depending on whether the measurement is absorption, photoconductivity, photoluminescence, magneto-optics, or detector cutoff.

Engineering equations such as the Hansen relation remain useful as latent mean-gap baselines. Their numerical precision should not be confused with the precision of an experimental observation. The previous study in this repository showed that historical composition uncertainty, source lineage, carrier and vacancy state, and edge-definition choice dominate the sub-meV ordering of common empirical laws. That result was intentionally negative: the available historical evidence did not identify a universal replacement equation.

The present work develops the constructive counterpart. Rather than asking which scalar gap equation is closest to a reported edge, we ask:

> Given a latent signed band structure, a specimen-state distribution, a carrier state, an optical geometry, and a measurement operator, what edge will the experiment report?

The framework is deliberately hierarchical. Low-cost analytical layers are activated before atomistic or first-principles calculations, and each layer has explicit claim boundaries. The resulting contribution is not one additional empirical correction. It is a set of exact and numerical identifiability results showing which physical parameters can, and cannot, be recovered from common HgCdTe observations.

The principal contributions are:

1. exact and bounded-Gaussian propagation from composition variation to local gap and critical-temperature distributions;
2. an independent reproduction of the Herrmann Gaussian-gap-to-apparent-tail scale and a quantitative fit-window non-uniqueness result;
3. a source-bounded Chang absorption-to-detector-cutoff operator and a rank-two theorem for tail-only cutoff datasets;
4. an exact nonparabolic carrier-filling model with a high-density parabolic-error criterion and density-series conditioning analysis;
5. a unified spectrum theorem proving structural rank at most three for five nominal single-state parameters;
6. a measurement-design prescription identifying the independent information required for latent-gap recovery.

The analytical theorems do not depend on fitting one historical spectrum. Material validation is treated separately and remains an explicit pre-submission requirement.

## 2. Definitions and forward hierarchy

### 2.1 Latent signed gap

Let

$$
E_g^{(0)}(x,T)
=E_{\Gamma_6}(x,T)-E_{\Gamma_8}(x,T)
$$

be the latent signed zone-center gap of a declared mean material state. The superscript `(0)` distinguishes this latent reference from an observed optical edge.

The present framework does not select one universal equation for $E_g^{(0)}$. Hansen, reconstructed Laurenti, and archived constrained candidates are used as alternative latent laws when model dependence must be quantified.

### 2.2 Composition and local-gap distributions

Let the local Cd fraction be

$$
X=\bar x+\delta x,
$$

with declared mean $\bar x$ and standard deviation $\sigma_x$. For sufficiently narrow distributions,

$$
\mathbb E[E_g(X,T)]
\approx
E_g(\bar x,T)
+\frac12 E_{g,xx}(\bar x,T)\sigma_x^2,
$$

and

$$
\sigma_{E,x}
\approx
|E_{g,x}(\bar x,T)|\sigma_x.
$$

Near a zero-gap transition,

$$
\sigma_{T_c}
\approx
\left|\frac{E_{g,x}}{E_{g,T}}\right|\sigma_x.
$$

These local expressions are supplemented by exact deterministic quadrature over a Gaussian composition model conditioned on the physical alloy interval $0\le x\le1$.

### 2.3 Local absorption and spectral convolution

For a local gap $G$, use the controlled intrinsic-edge family

$$
\alpha_{\mathrm{loc}}(E\mid G)
=A(E-G)_+^p,
$$

where $(y)_+=\max(y,0)$ and $p$ is a declared edge exponent.

For

$$
G\sim\mathcal N(\mu_G,\sigma_G^2),
$$

the distributed absorption is

$$
\bar\alpha(E)
=A\sigma_G^p
F_p\left(\frac{E-\mu_G}{\sigma_G}\right),
$$

where

$$
F_p(z)=\int_{-\infty}^{z}(z-u)^p\phi(u)\,du.
$$

This model is a controlled observation basis. It is not assumed to be a complete microscopic absorption law.

### 2.4 Detector response and operational cutoff

For effective absorbing thickness $d$, the single-pass response is

$$
R(E,d)=1-\exp[-\alpha(E)d].
$$

A target response $R_t$ corresponds to

$$
\alpha_t=\frac{-\ln(1-R_t)}{d}.
$$

If the crossing lies on an exponential tail joined at $(E_j,\alpha_j)$,

$$
\alpha(E)=\alpha_j\exp\left(\frac{E-E_j}{W}\right),
$$

then

$$
E_c
=E_j+W\ln\left(\frac{\alpha_t}{\alpha_j}\right).
$$

### 2.5 Carrier-filled optical edge

For one spin-degenerate spherical valley,

$$
k_F=\left(\frac{3\pi^2 n}{g_v}\right)^{1/3}.
$$

Let

$$
E_{\mathrm{par}}
=\frac{\hbar^2k_F^2}{2m_e^*}.
$$

A declared Kane-type nonparabolic conduction branch satisfies

$$
E_c(1+\alpha E_c)=E_{\mathrm{par}},
$$

with solution

$$
E_c
=\frac{2E_{\mathrm{par}}}
{1+\sqrt{1+4\alpha E_{\mathrm{par}}}}.
$$

For a parabolic valence recoil,

$$
\Delta E_{\mathrm{BM}}
=E_c(k_F)+\frac{\hbar^2k_F^2}{2m_v^*}.
$$

The observed edge is kept decomposed:

$$
E_{\mathrm{opt}}
=E_g^{(0)}
+\Delta E_{\mathrm{BM}}
+\Delta E_{\mathrm{BGR}}
+\Delta E_{\mathrm{obs}}.
$$

## 3. Methods

### 3.1 Claim classes

Each result is assigned one of five states:

1. exact analytical theorem;
2. numerical verification of an exact theorem;
3. source reproduction under declared assumptions;
4. bounded synthetic sensitivity;
5. external material validation.

Only the fifth state supports direct specimen-level material claims. Synthetic parameter cases are never described as fitted material properties.

### 3.2 Numerical quadrature

Gaussian gap convolutions are evaluated using energy-dependent Gauss-Legendre quadrature restricted to $G\le E$. Splitting the integral at the moving local threshold removes the interior cusp that otherwise produces slow fixed-grid convergence. Linear and quadratic edge branches are verified against closed Gaussian moments.

Bounded composition distributions use deterministic Gaussian quadrature conditioned on $0\le x\le1$. Transition roots are classified as single crossing, always normal, always inverted, multiple crossing, or unresolved before conditional moments are reported.

### 3.3 Structural identifiability

For a vector of observables $y(\theta)$, local identifiability is evaluated from the singular values of

$$
J_{ij}=\frac{\partial y_i}{\partial\theta_j}.
$$

Exact invariances are derived analytically before numerical rank is interpreted. Relative singular values below the declared tolerance are treated as unresolved directions, but rank claims are not based solely on numerical thresholds when an exact proof is available.

### 3.4 Source boundaries

Herrmann et al. provide the Gaussian-gap distribution and the approximately-$s/2$ apparent tail claim. Chang et al. provide a nonparabolic-Urbach branch with a declared source domain. Dingrong et al. provide a high-density HgCdTe regime requiring carrier filling and free-carrier absorption. Teppe et al. provide a temperature-driven near-critical Kane-mass series.

Incomplete source parameters are not silently reconstructed. Chang Figure 2 and the full Dingrong spectrum remain outside quantitative material validation until native data and missing parameter provenance are recovered.

## 4. Results

### 4.1 Composition distributions broaden and censor the apparent transition

At nominal mean composition $\bar x=0.155$, the three existing latent laws predict central critical temperatures:

| Latent law | Central $T_c$ |
|---|---:|
| Reconstructed Laurenti | 77.1241 K |
| Hansen-Schmit-Casselman | 52.0438 K |
| Archived Hansen-Pade | 52.5937 K |

The central model span is

$$
25.0803\ \mathrm K.
$$

At $\sigma_x=0.001$, exact composition-induced critical-temperature widths are `3.804-4.560 K`; the latent-law choice dominates. At $\sigma_x=0.005$, conditional widths are `18.345-22.290 K`, and `0.36-1.30%` of the declared distribution remains normal throughout `0-300 K`. At $\sigma_x=0.010`, the always-normal fraction rises to `8.60-14.12%`.

The local derivative approximation becomes misleading in the broad regime because compositions with no transition inside the observation window are censored from the conditional root distribution. At $\sigma_x=0.010`, conditional means shift by `5.52-11.05 K`, while the local approximation overestimates conditional width by `6.68-9.66 K`.

This is not a topological phase-fraction calculation. It is a distributional observation result showing that an apparent transition temperature must be reported with the crossing probability and the assumed composition distribution.

### 4.2 A Gaussian gap distribution reproduces an apparent Urbach tail but not a unique width

Herrmann et al. define

$$
P(G)=
\frac{1}{2s\sqrt\pi}
\exp\left[-\frac{(G-\bar G)^2}{4s^2}\right],
$$

so

$$
\sigma_G=\sqrt2\,s.
$$

For a square-root local edge and the source-stated `1-100 cm^-1` fit range, the reproduced apparent exponential tail gives

$$
\frac{W_{\mathrm{fit}}}{s}=0.50504,
\qquad
R^2=0.99570.
$$

The approximately-$s/2$ source scale is therefore independently reproduced under source-aligned conditions.

The same convolved spectrum is not exactly exponential. Fitting different absorption intervals gives:

| Fit window ($\mathrm{cm^{-1}}$) | $W_{\mathrm{fit}}/s$ | $R^2$ |
|---|---:|---:|
| 0.1-100 | 0.46096 | 0.99307 |
| 1-100 | 0.50504 | 0.99570 |
| 10-100 | 0.56806 | 0.99836 |
| 10-500 | 0.66828 | 0.99190 |
| 100-500 | 0.80871 | 0.99738 |

Changing only the observation window from `1-100` to `100-500 cm^-1` increases the inferred tail energy by `60.1%`, although both fits appear strongly log-linear.

Across local-edge exponents $p=0.5$, 1, and 2, the source-window ratio changes only from `0.48375` to `0.50504`. Thus high $R^2$ weakly identifies the intrinsic branch.

For an observed $W_{\mathrm{fit}}=4$ meV, the declared exponent/window family permits

$$
6.995\ \mathrm{meV}
\le\sigma_G\le
12.661\ \mathrm{meV}.
$$

An Urbach-like slope is therefore compatible with a Gaussian gap distribution but does not uniquely identify it or its width.

### 4.3 Detector cutoff is a thickness-dependent observation operator

On an exponential tail,

$$
E_c(d_2)-E_c(d_1)
=-W\ln(d_2/d_1).
$$

For a declared synthetic Chang case with $W=12$ meV, changing effective thickness from 5 to 20 $\mu$m shifts the 50% response cutoff by

$$
-16.636\ \mathrm{meV},
$$

or from `12.445 um` to `14.939 um`, without changing the latent $E_g$.

A tail-only Chang cutoff can be written

$$
E_{c,i}=C(E_g,W,A,b)+WL_i,
$$

where $L_i$ depends only on thickness and response criterion. Every Jacobian row lies in the span of $\nabla C$ and $\nabla W$, so

$$
\boxed{
\operatorname{rank}(J_{\mathrm{tail}})\le2.
}
$$

Nine tail-only observations produce two finite singular values and two values near `10^-12`. Adding intrinsic-branch observations restores local rank four, but the condition number remains `199.81`.

Collecting more tail-only cutoffs improves precision in two combinations; it does not identify $E_g$, $W$, amplitude, and nonparabolicity separately.

### 4.4 Nonparabolic carrier filling is not a small correction at high density

Define

$$
q=\alpha E_{\mathrm{par}}.
$$

The exact relative error from using the parabolic conduction energy is

$$
\boxed{
\frac{E_{\mathrm{par}}-E_c}{E_c}
=
\frac{\sqrt{1+4q}-1}{2}.
}
$$

At the declared high-density sensitivity point

```text
n          = 7.0e17 cm^-3
m_edge     = 0.010 m0
alpha      = 7.5 eV^-1
m_valence  = 0.35 m0
```

we obtain:

| Quantity | Value |
|---|---:|
| $k_F$ | 0.0274688 $\mathrm{\AA^{-1}}$ |
| Parabolic conduction energy | 287.476 meV |
| Nonparabolic conduction energy | 140.154 meV |
| Valence recoil | 8.214 meV |
| Nonparabolic BM shift | 148.367 meV |
| Parabolic BM shift | 295.690 meV |
| Parabolic overestimate | 147.323 meV |
| $q$ | 2.1561 |

The parabolic filling shift is `1.993` times the nonparabolic result. For the same declared parameters, the conduction-energy error grows from `0.0046 meV` at `10^14 cm^-3` to `147.323 meV` at `7x10^17 cm^-3`.

One optical edge at one density has rank one for five declared parameters. A five-density series restores local rank five, but its condition number is

$$
1.1035\times10^4.
$$

Formal full rank is therefore insufficient for a stable unconstrained inversion.

These values are bounded sensitivity results in the Dingrong density regime, not a fit to the Dingrong specimen.

### 4.5 Unified spectrum theorem: dense sampling cannot remove exact invariances

For

$$
G\sim\mathcal N(E_g^{(0)}+\Delta_c,\sigma_G^2)
$$

and

$$
R(E)=1-
\exp\left\{
-Ad\,\sigma_G^p
F_p\left[
\frac{E-E_g^{(0)}-\Delta_c}{\sigma_G}
\right]
\right\},
$$

the five nominal parameters

$$
(E_g^{(0)},\Delta_c,\ln\sigma_G,\ln A,\ln d)
$$

enter through only

$$
E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
Ad.
$$

Therefore

$$
\frac{\partial R}{\partial E_g^{(0)}}
=
\frac{\partial R}{\partial\Delta_c},
$$

$$
\frac{\partial R}{\partial\ln A}
=
\frac{\partial R}{\partial\ln d},
$$

and

$$
\boxed{
\operatorname{rank}(J)\le3.
}
$$

Two parameter sets with different latent gaps, carrier shifts, amplitudes, and thicknesses produce response spectra equal to machine precision when the translated mean gap and amplitude-thickness product are preserved. Across 281 spectral points, their maximum absolute difference is `2.22x10^-16`.

The numerical singular values are

```text
2.10943527e2
3.12774161e0
3.79499126e-1
3.36022167e-11
4.59184616e-14
```

and the numerical rank is three.

Known carrier shift alone leaves the amplitude/thickness null. Known thickness alone leaves the gap/carrier null. Both must be constrained to recover $(E_g^{(0)},\sigma_G,A)$ in the base model.

### 4.6 A carrier-dependent spectral marker raises rank but leaves one combined invariance

Add an absolutely calibrated diagnostic carrier feature

$$
\alpha_m(E)
=B\Delta_c(E_r/E)^2.
$$

The marked spectrum depends on four combinations:

$$
E_g^{(0)}+\Delta_c,
\qquad
\sigma_G,
\qquad
Ad,
\qquad
\Delta_cd.
$$

The two simple pairwise invariances no longer hold, but one combined transformation remains:

$$
d\rightarrow cd,
$$

$$
A\rightarrow A/c,
$$

$$
\Delta_c\rightarrow\Delta_c/c,
$$

$$
E_g^{(0)}
\rightarrow
E_g^{(0)}+\Delta_c(1-1/c).
$$

The infinitesimal null vector is

$$
(\Delta_c,-\Delta_c,0,-1,1).
$$

The marked-spectrum numerical rank is four, with one relative singular value near `10^-13`. Independently known effective thickness removes the remaining null and leaves the other four parameters locally full rank.

The marker is a structural diagnostic, not the Dingrong free-carrier absorption law.

## 5. Discussion

### 5.1 Structural uncertainty is not reduced by better instruments

Noise reduction improves estimation only within identifiable parameter combinations. It cannot resolve exact invariances of the forward operator. This distinction matters because HgCdTe experiments often report small numerical fitting errors while omitting composition, carrier, thickness, or observation-model uncertainty that lies in a structurally unresolved direction.

The unified theorem provides a strict example. An ideal, continuum, noise-free spectrum still cannot separate $E_g^{(0)}$ from a rigid carrier shift or absorption amplitude from effective thickness in the base model.

### 5.2 A reported edge is a property of specimen and operator

The results establish four distinct mechanisms by which a reported edge can move without a corresponding change in the latent mean gap:

1. composition distributions alter local gap and critical-temperature statistics;
2. fit-window choice changes an apparent Urbach energy;
3. thickness and response criterion move detector cutoff;
4. carrier filling and many-body terms translate the interband threshold.

A scalar edge coordinate is therefore incomplete unless the observation operator and specimen state are declared.

### 5.3 Minimum experimental information

Under the base unified model, latent-gap recovery requires at least:

- independent carrier density and a validated carrier-shift model;
- independently calibrated effective thickness or absorption amplitude;
- a full calibrated spectrum;
- sufficient spectral range to resolve gap width and intrinsic-edge shape.

A carrier-dependent spectral background can add an independent direction only if its shape and absolute calibration are retained. Subtracting such a background without joint uncertainty can remove precisely the information needed to separate carrier state from latent gap.

### 5.4 Relation to prior work

Herrmann et al. established that gap distributions can produce apparent exponential tails. The present work reproduces that scale and shows quantitatively that the inverse width depends strongly on the fit window.

Chang et al. developed a nonparabolic-Urbach absorption model and connected absorption to thickness-dependent detector response. The present work isolates an exact logarithmic thickness law and proves the structural rank limit of tail-only cutoff datasets.

Dingrong et al. demonstrated a degenerate HgCdTe regime requiring Burstein-Moss and free-carrier physics. The present work quantifies the potential parabolic error and shows why a density series remains poorly conditioned without independent mass and renormalization constraints.

Teppe et al. demonstrated a temperature-driven sign change of the Kane mass. The present distributional calculation shows that composition variation and latent-law choice can broaden and displace an apparent transition even before a specific disorder self-energy is introduced.

The unified rank theorem is the new synthesis: these mechanisms are not merely additive error bars. They create exact or near-exact parameter combinations that determine what a spectrum can identify.

### 5.5 Implications for model validation

A bandgap law should not be validated against an optical edge until the forward observation operator is sufficiently specified. Conversely, the inability to recover a unique latent gap does not imply that the spectrum is useless. Dense spectra can identify translated mean edge, gap width, and optical-depth scale, and can falsify inadequate lineshape models.

The correct goal is not to force every experiment to report one corrected scalar gap. It is to fit a forward model whose identifiable combinations and external constraints are explicit.

## 6. Limitations

The analytical results use controlled model layers rather than a complete microscopic HgCdTe calculation. Principal limitations are:

1. Gaussian local-gap distributions may not represent clustering, gradients, or correlated disorder.
2. The power-law local edge is a sensitivity basis, not a complete Kane absorption model.
3. Carrier translation is spatially uniform in the unified theorem.
4. The generic carrier marker is not a physical free-carrier absorption model.
5. Single-pass response excludes reflection, interference, multiple paths, transport, and energy-dependent collection efficiency.
6. The Dingrong sensitivity calculation is zero-temperature and does not reproduce the full source spectra.
7. Chang Figure 2 lacks the native data and parameter provenance required for external validation.
8. Local opposite-sign fractions are not bulk topological invariants.
9. Structural rank does not determine practical posterior uncertainty after external constraints are introduced.
10. At least one calibrated real-spectrum validation case is still required before submission.

These limitations are activation gates for future model layers, not justification for collapsing the current distinctions.

## 7. Conclusions

We developed a distributional observation framework for HgCdTe band-edge measurements and established several quantitative identifiability limits.

Composition variation near inversion produces critical-temperature distributions whose width and censoring can exceed local derivative estimates. Gaussian gap distributions can reproduce highly exponential-looking tails, but the inferred tail energy changes substantially with the fitting window. Detector cutoff depends logarithmically on effective thickness, and tail-only cutoff datasets have structural rank at most two. Degenerate carrier filling requires nonparabolic treatment; at the declared high-density sensitivity point, the parabolic estimate is wrong by 147 meV. Most importantly, a dense single-state response spectrum with five nominal parameters has structural rank at most three under the base model. A calibrated carrier-dependent spectral feature raises rank to four but leaves one combined invariance until an external scale is supplied.

The central result is methodological:

> The precision of an extracted edge is not the precision of a latent bandgap. Recovering the latent HgCdTe gap requires a forward observation model and independent constraints on the exact parameter combinations that spectroscopy cannot separate.

## 8. Reproducibility and data availability

Every quantitative result in this draft is generated from version-controlled code and immutable repository records:

- `data/validation/near_critical_transition_model_dependence.json`;
- `data/validation/herrmann_gaussian_tail_reproduction.json`;
- `data/validation/chang_2006_cutoff_identifiability.json`;
- `data/validation/dingrong_1985_carrier_filling_sensitivity.json`;
- `data/validation/unified_spectrum_structural_rank.json`.

The executable implementations are in:

- `src/mct_research/distributional_gap.py`;
- `src/mct_research/distributional_quadrature.py`;
- `src/mct_research/spectral_convolution.py`;
- `src/mct_research/detector_cutoff.py`;
- `src/mct_research/carrier_filling.py`;
- `src/mct_research/unified_spectrum.py`.

The analytical derivations are in `docs/derivations/008` through `013`.

## 9. Submission status

The analytical core is complete enough for manuscript development. Submission remains blocked by:

1. one external calibrated spectrum or same-specimen multi-state validation case;
2. complete bibliography verification;
3. final figure generation from immutable data;
4. journal-specific formatting and word limits;
5. author, affiliation, declarations, and archive metadata;
6. independent review of theorem wording and prior-art boundaries.
