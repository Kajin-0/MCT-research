# Cross-material audit: Gaussian tails, apparent Urbach behavior, and finite-window identifiability

## Scope

This note audits claim-level prior art relevant to the R03 operator

$$
\alpha_p(E)=A\,\mathbb{E}[(E-G)_+^p],
\qquad
G\sim\mathcal{N}(\mu_G,\sigma_G^2),
\qquad p\ge 0.
$$

The audit asks which parts of the current R03 result are already established outside HgCdTe and which, if any, remain a defensible operator-specific contribution.

The audit does **not** infer one microscopic origin for measured absorption tails. Spatial random potentials, local-gap distributions, density-of-states distributions, and thermally weighted transition distributions are different models and are not interchangeable merely because their plotted tails can look similar.

## Evidence-status convention

| status | meaning |
|---|---|
| full text inspected | equations, model boundary, and stated asymptotics were inspected in the primary article |
| primary abstract inspected | only the publisher or institutional primary abstract was available; absence of a theorem cannot be inferred |
| primary abstract plus thesis record | article abstracts and a first-party thesis record were inspected; exact equation-level exclusion remains open |
| accessible primary text inspected | a publisher, repository, or author-hosted primary text was inspected |

A statement that an equivalent theorem was **not located** means only that it was not found in the inspected material. It is not a universal novelty determination.

## Source matrix

| source | evidence status | random object | local operator or observable | tail/asymptotic statement | inverse-log-slope or fit-window statement | relation to R03 |
|---|---|---|---|---|---|---|
| John, Soukoulis, Cohen, and Economou, *Phys. Rev. Lett.* **57**, 1777 (1986), DOI `10.1103/PhysRevLett.57.1777` | primary abstract inspected | correlated Gaussian spatial random potential | electronic density of states | reports an experimentally broad approximately linear-exponential Urbach regime from a correlated Gaussian random potential | not an optical one-sided threshold calculation | establishes that a Gaussian-disorder model can generate a long apparently exponential interval |
| John, Chou, Cohen, and Soukoulis, *Phys. Rev. B* **37**, 6963 (1988), DOI `10.1103/PhysRevB.37.6963` | full text inspected | correlated Gaussian spatial random potential | electronic density of states | distinguishes a shallow Halperin-Lax-type tail, an intermediate approximately exponential regime, and a deep Gaussian tail of the form `exp[-E^2/(2 V_rms^2)]` up to algebraic factors | emphasizes that the experimentally relevant Urbach-like behavior occurs in a crossover rather than being identified with either limiting asymptote | establishes prior art for an intermediate Urbach-like interval followed by a deeper Gaussian asymptote; the operator is not the R03 local-gap convolution |
| O'Leary, Zukotynski, and Perz, *Phys. Rev. B* **51**, 4143 (1995), DOI `10.1103/PhysRevB.51.4143` | primary abstract plus thesis record | spatially fluctuating amorphous-semiconductor potentials | local density of states averaged over potential fluctuations | constructs a unified density of states spanning band-tail and extended states | exact logarithmic-curvature statements were not recoverable from the available source record | establishes Gaussian-potential averaging across tail and band regimes; exact theorem exclusion remains unresolved without the full text |
| O'Leary, Zukotynski, and Perz, *Phys. Rev. B* **52**, 7795 (1995), DOI `10.1103/PhysRevB.52.7795` | primary abstract plus thesis record | correlated Gaussian conduction- and valence-band potential fluctuations | local joint density of states averaged over the fluctuations | gives optical absorption from below to above the nominal gap | exact all-`p` partial-moment, log-concavity, and finite-window residual results were not recoverable from the available source record | close conceptual precedent for Gaussian averaging of optical thresholds; a positive novelty decision is not permitted until the full text is inspected or formally recorded unavailable |
| Gokmen et al., *Appl. Phys. Lett.* **103**, 103506 (2013), DOI `10.1063/1.4820250` | accessible primary text inspected | Gaussian distribution of local band gaps in kesterite | direct-gap local absorption proportional to `sqrt(hbar omega-E_g)/(hbar omega)`, averaged over the gap distribution | produces broadened subgap absorption and is fitted to IQE-derived absorption data | fit quality does not uniquely identify gap fluctuations; an electrostatic-fluctuation model also describes the data | decisive prior art for Gaussian local-gap averaging of a square-root direct-gap edge, corresponding closely to the R03 `p=1/2` branch with an additional photon-energy prefactor |
| Guerra et al., *J. Phys. D* **52**, 105303 (2019), DOI `10.1088/1361-6463/aaf963` | accessible primary text and primary abstract inspected | band-edge fluctuation distribution chosen with non-Gaussian tails | averaged direct- and indirect-gap absorption laws | obtains a true exponential asymptote by using a fluctuation kernel whose tail is not Gaussian | treats the Urbach region as an asymptotic model property | establishes that asymptotic class depends on the fluctuation kernel; R03 must not generalize its Gaussian deep-tail result to all disorder models |
| Kaiser et al., *Nat. Commun.* **12**, 3988 (2021), DOI `10.1038/s41467-021-24202-9` | full open primary text inspected | Gaussian energetic disorder combined with thermally weighted optical transitions in organic semiconductors | EQE and the local inverse logarithmic slope | Gaussian disorder produces a strongly energy-dependent apparent Urbach energy near the absorption onset; a thermal Boltzmann regime can yield a true constant tail energy farther below the gap | defines `E_U^app(E)=[d ln(EQE)/dE]^{-1}` and states that narrow fitting ranges can force arbitrary exponential fits | establishes prior art for energy-dependent local inverse slope and fit-window-dependent apparent Urbach energies; its transition operator is not the R03 sharp one-sided power threshold |
| Winkler, Roodman, and Britney, *Management Science* **19**, 290 (1972), DOI `10.1287/mnsc.19.3.290` | primary abstract inspected | probability distributions generally | partial moments and recurrences | provides formulas and recursive relationships for partial moments of common distributions | not an optical-tail paper | establishes that generic Gaussian partial moments and their recurrence machinery are standard mathematics |

## Claims that must be treated as established prior art

The cross-material audit removes the following from any novelty claim:

1. **Gaussian or correlated-disorder models can generate long apparently exponential spectral intervals.**
2. **A deeper Gaussian asymptote can coexist with an intermediate Urbach-like crossover regime.**
3. **Gaussian averaging of a local direct-gap square-root absorption edge is established.** The R03 `p=1/2` convolution is therefore not new as a model class.
4. **The inverse logarithmic slope can be energy dependent.** Calling it a local or apparent Urbach energy is established practice.
5. **Narrow-window exponential fits can be arbitrary and fit-window dependent.**
6. **Generic partial-moment identities and recurrences are established probability theory.**
7. **The asymptotic tail class is kernel dependent.** A non-Gaussian fluctuation distribution can produce a true exponential asymptote, so the Gaussian result is not universal across disorder models.

## What the inspected sources do not establish as one result

No equivalent statement was located in the inspected full texts and accessible primary records that combines, for the declared one-sided Gaussian-power threshold operator and arbitrary `p>=0`, all of the following:

$$
F_p'(z)=F_{p+1}(z)-zF_p(z),
$$

$$
F_p''(z)=F_{p+2}(z)-2zF_{p+1}(z)+(z^2-1)F_p(z),
$$

log-concavity of the resulting absorption,

$$
\frac{d^2\log\alpha_p}{dE^2}\le 0,
$$

monotonic increase of

$$
W_{\rm loc}(E)=\left[\frac{d\log\alpha_p}{dE}\right]^{-1},
$$

the normalized deep-tail limit

$$
\sigma_G^2\frac{d^2\log\alpha_p}{dE^2}\to -1,
$$

and the fixed-dynamic-range recoverability result

$$
\epsilon_{\rm affine}=O(|z_{\rm upper}|^{-2})\to0.
$$

This absence is **not** sufficient for a broad novelty claim. The O'Leary article full texts remain a material audit gap, and standard partial-moment mathematics owns the recurrence machinery itself.

## Retained candidate distinction

The narrow candidate R03 contribution is the **assembled operator-specific theorem and measurement consequence**, not any individual ingredient:

- specialization of standard partial-moment machinery to the full one-sided Gaussian-power optical operator for arbitrary `p>=0`;
- proof of log-concavity and monotone local inverse slope for that operator;
- explicit normalized deep-tail logarithmic-curvature limit;
- explicit finite-window best-affine residual scaling;
- source-conditioned demonstration that historical HgCdTe figures cannot validate the curvature without an independent standardized window-location anchor.

The defensible wording is:

> For the declared Gaussian-distributed one-sided power-threshold observation operator, the combined differential, asymptotic, and finite-window recoverability consequences were not located in the audited literature.

The following wording is not defensible:

> Gaussian disorder has not previously been connected to Urbach-like absorption, energy-dependent apparent Urbach energies, square-root edge convolution, or deeper Gaussian tails.

## Decision

**Narrow the claim; do not terminate the theorem.**

The cross-material audit does not invalidate the analytical results in PR #226 or the recoverability result in PR #237. It removes broad novelty language and leaves only a compact operator-specific theorem package as a candidate contribution.

No new numerical implementation is justified by this audit. The next decision-changing work is external:

1. retrieve and inspect the two O'Leary 1995 full texts, or record a formal source-unavailable boundary;
2. locate numerical absorption data with covariance or a defensible above-gap/mean-gap anchor;
3. test whether such data can resolve logarithmic curvature under the recoverability theorem.

Until those gates are satisfied, manuscript writing remains unauthorized.

## Claim-boundary summary

### Supported

- broad cross-material prior art materially narrows R03;
- the `p=1/2` Gaussian local-gap convolution is prior art;
- apparent Urbach energy and fit-window dependence are prior art;
- the R03 deep-tail class is specific to the Gaussian threshold-distribution model;
- the combined all-`p` curvature and recoverability package was not located in the inspected material.

### Not supported

- universal novelty of Gaussian-disorder absorption tails;
- novelty of partial-moment recurrence relations;
- novelty of energy-dependent inverse logarithmic slope;
- novelty of square-root edge convolution over a Gaussian gap distribution;
- a universal Gaussian deep tail for all disorder kernels;
- a positive novelty determination without the unresolved full-text audit;
- manuscript or submission authorization.