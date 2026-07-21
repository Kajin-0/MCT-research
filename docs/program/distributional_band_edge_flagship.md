# Distributional HgCdTe band-edge flagship program

## Status

**Activated:** 2026-07-21  
**Controlling issue:** #167  
**Execution mode:** independent, public-data-first, reproducible computation  
**Prior manuscript:** frozen as Paper I

## Publication objective

Develop a submission-quality theory and benchmark for how a latent HgCdTe signed band structure becomes a reported optical, photoluminescent, detector-cutoff, or magneto-optical gap observable.

The program extends the completed observation-model uncertainty manuscript. Paper I established that historical equation rankings are non-identifying at the few-meV scale. The flagship paper must now provide a positive forward model and significant quantitative results rather than another empirical gap equation.

## Central thesis

A reported HgCdTe gap is generally

$$
E_{\mathrm{reported}}^{(m)}
=
\mathcal O_m
\left[
\mathcal R_m
\left(
E_g^{\mathrm{local}},
A(\mathbf k,\omega),
\alpha(E),
n,p,
d,
T
\right)
\right],
$$

where $\mathcal R_m$ represents the modality-specific physical response and instrument model and $\mathcal O_m$ is the declared edge or parameter-extraction operator.

It is not generally true that

$$
E_{\mathrm{reported}}^{(m)}=E_g(\bar x,T).
$$

## Model ladder

### F0 — latent mean signed gap

$$
\bar E_g(x,T).
$$

This may be Hansen, Laurenti, a constrained thermal model, or a later physics-derived law. The flagship result must not depend on selecting one universal law prematurely.

### F1 — composition distribution

Let

$$
X=\bar x+\delta x,
\qquad
\mathbb E[\delta x]=0,
\qquad
\operatorname{Var}(X)=\sigma_x^2.
$$

To second order,

$$
\mathbb E[E_g(X,T)]
\approx
E_g(\bar x,T)
+
\frac12 E_{g,xx}(\bar x,T)\sigma_x^2,
$$

and

$$
\sigma_{E,x}
\approx
|E_{g,x}(\bar x,T)|\sigma_x.
$$

The curvature term is a systematic mean-gap bias. The width term is a local-gap statistic under a declared spatial or specimen-level interpretation. Neither is automatically an Urbach energy or quasiparticle linewidth.

### F2 — carrier and defect state

The latent optical transition model must admit

$$
E_{\mathrm{opt}}
=
E_g
+
\Delta E_{\mathrm{BM}}
+
\Delta E_{\mathrm{BGR}}
+
\Delta E_{\mathrm{defect}},
$$

with carrier density, polarity, compensation, and vacancy-related state retained as explicit covariates. Dingrong et al. provide a high-density Burstein-Moss validation regime; Chang et al. define a low-density LWIR regime where the shift is expected to be small.

### F3 — intrinsic and tail absorption

The above-gap branch will use a nonparabolic Kane response. The below-gap branch will be treated as an observation model whose width may contain static alloy disorder, structural disorder, dynamic disorder, defects, and instrumental effects.

The initial forward form is

$$
\alpha_{\mathrm{mix}}(E)
=
\int p(g)\,\alpha_{\mathrm{Kane}}(E\mid g,\theta_K)\,dg
+
\alpha_{\mathrm{tail}}(E\mid\theta_U)
+
\alpha_{\mathrm{FCA}}(E\mid n,T).
$$

No direct identity such as $W=\sigma_E$ is authorized. Herrmann's Gaussian-gap convolution and Chang's Urbach/Kane connection provide separate testable limits.

### F4 — geometry and instrument response

The measured transmission or detector response must include thickness, reflectivity, interference, effective collection thickness, spectral resolution, and calibration uncertainty where applicable.

Chang's thickness-dependent cutoff calculation is treated as a decisive warning: detector cutoff is a geometry-dependent response quantity, not a direct scalar material gap.

### F5 — observation operator

Every inferred edge must retain its operator, for example:

- fixed absorption threshold;
- derivative maximum;
- fitted Kane edge;
- Urbach/Kane intersection;
- transmission intercept;
- photoconductive half response;
- PL peak;
- magneto-optical Kane-mass fit.

Cross-modal agreement is a prediction to be tested, not an assumption.

## First significant result

At the Teppe sample-B transition regime, use the reconstructed Laurenti law at

$$
\bar x=0.155,
\qquad
T=77\ \mathrm K.
$$

The tested finite-difference propagation gives

$$
E_g(\bar x,T)=-0.0478\ \mathrm{meV},
$$

$$
\frac{\partial E_g}{\partial x}=1.71911\ \mathrm{eV},
$$

and

$$
\frac{\partial E_g}{\partial T}=0.38518\ \mathrm{meV/K}.
$$

For $\sigma_x=0.001$,

$$
\sigma_{E,x}=1.719\ \mathrm{meV},
\qquad
\sigma_{T_c}=4.46\ \mathrm K,
$$

with a Gaussian local opposite-sign fraction of approximately $0.489$ because the mean gap is nearly zero.

For $\sigma_x=0.005$,

$$
\sigma_{E,x}=8.596\ \mathrm{meV},
\qquad
\sigma_{T_c}=22.32\ \mathrm K.
$$

This is an observation-scale and local-sign result, not a claim that Teppe's specimen has either declared $\sigma_x$, not an optical linewidth, and not a bulk topological invariant. It establishes the precision scale that any composition-tuned transition claim must resolve.

## Primary-source roles

### Wu 1983

Supports a microscopic alloy-fluctuation contribution to composition-dependent bowing beyond the virtual-crystal approximation. It does not supply a modern, uniquely transferable disorder width or an observation operator.

### Dingrong et al. 1985

Provides a degenerate $x=0.19$, $n\approx7\times10^{17}\ \mathrm{cm^{-3}}$, 77–300 K regime in which the absorption edge is explicitly carrier-filled and below-gap free-carrier absorption is material to the spectrum.

### Herrmann et al. 1992

Provides a unified semi-empirical treatment of absorption, photoconductivity, and luminescence and shows that convolving an intrinsic edge with a Gaussian-like gap distribution yields a near-exponential tail over a relevant absorption range. It also separates alloy disorder, temperature-dependent broadening, and shallow-level contributions.

### Chang et al. 2007

Provides a nonparabolic Kane plus Urbach absorption model over the tail and intrinsic region, same-point transmissivity/photoconductivity methodology, and a thickness-dependent detector-cutoff consequence.

### Teppe et al. 2016

Provides the near-critical magneto-optical target: a temperature-driven sign change near 77 K for nominal $x=0.155$ and an approximately universal Kane velocity of $(1.07\pm0.05)\times10^6\ \mathrm{m\,s^{-1}}$.

### Ivanov-Omskii et al. 2009

Provides processing-conditioned PL red shifts and linewidths interpreted through composition fluctuations. Annealing reduces the inferred fluctuation measure, but the inference remains model- and PL-operator-dependent.

## Validation sequence

1. **Analytical propagation:** verify linear and quadratic limiting cases and derivative-step stability.
2. **Teppe transition screen:** quantify $\sigma_E$, $\sigma_{T_c}$, and local sign fractions across declared $\sigma_x$ values and competing latent gap laws.
3. **Herrmann convolution reproduction:** reconstruct the Gaussian-gap-to-tail relation without identifying the resulting tail parameter with a universal disorder width.
4. **Chang operator reproduction:** reproduce the intrinsic/tail transition and thickness-dependent cutoff under source-declared limits.
5. **Dingrong carrier branch:** reproduce the qualitative and quantitative edge shift in the degenerate regime.
6. **Ivanov-Omskii PL branch:** test whether one distributional parameter can jointly account for PL displacement and FWHM across annealing states.
7. **Cross-modal benchmark:** predict and compare absorption, PL, photoconductive, cutoff, and magneto-optical reported gaps.
8. **Holdout tests:** leave one specimen, source, modality, and processing class out.

## Publication-level target results

The final paper must contain at least three of the following:

1. a quantitative recoverability map for latent $E_g$ in $(x,T,\sigma_x,n,d,W)$ space;
2. a demonstrated equation-rank reversal caused by a declared observation operator;
3. a disorder- and metrology-broadened transition band in the $x$-$T$ plane;
4. a successful cross-modal prediction using one latent specimen-state model;
5. a falsified direct identification between an Urbach/PL width and composition variance;
6. a reusable provenance-controlled benchmark dataset and software package.

## Computation gate

The default methods are analytical derivation, numerical quadrature, parameter sensitivity, and published-data reconstruction. SQS, CPA, SCBA, or new first-principles work is authorized only if:

- a low-cost forward model isolates a decision-changing observable;
- the required microscopic quantity cannot be bounded from existing data;
- a specific published result can validate the calculation;
- the computational branch has a predeclared termination criterion.

## Claim boundaries

The program must not claim:

- that the local Gaussian composition model is microscopically complete;
- that a local opposite-sign fraction is a topological invariant;
- that one optical edge definition is the latent material gap;
- that $W$, PL FWHM, $\sigma_x$, and quasiparticle linewidth are interchangeable;
- that nominal composition uncertainty equals microscopic alloy fluctuation;
- that the completed Paper I selected a universal gap equation;
- that external collaboration is required for the independent program to proceed.

## Completion criterion

The flagship manuscript is ready when the repository contains:

- a frozen Paper I submission package;
- the tested F0–F5 forward model or explicit bounded subset;
- source-native or auditable validation records from at least three independent experimental lineages;
- analytical and numerical uncertainty propagation;
- group-preserving validation and falsification results;
- manuscript figures generated from committed data and code;
- a claim-by-claim novelty audit.
