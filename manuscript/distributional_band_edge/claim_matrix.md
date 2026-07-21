# Claim and evidence matrix

## Status vocabulary

- **Exact theorem:** algebraic or analytical result under declared assumptions.
- **Numerical verification:** deterministic calculation verifying an exact statement or a bounded numerical consequence.
- **Source reproduction:** reproduction of a published source claim under source-aligned conventions.
- **Bounded synthetic sensitivity:** numerical result for declared illustrative parameters, not a specimen fit.
- **External material validation:** comparison against calibrated real specimen data with sufficient provenance.
- **Open:** not yet supported at the required level.

## Matrix

| ID | Manuscript claim | Claim class | Evidence and immutable record | Current status | Authorized wording | Prohibited overstatement |
|---|---|---|---|---|---|---|
| C01 | Composition variation produces a curvature bias in the mean gap and a first-order local gap width. | Exact asymptotic proposition | `src/mct_research/distributional_gap.py`; derivation 008 | Complete | “Under a narrow declared composition distribution…” | “All HgCdTe disorder is Gaussian” or “the result measures microscopic alloy disorder.” |
| C02 | Near a simple zero-gap root, composition variation is amplified into transition-temperature variation by `|Eg_x/Eg_T|`. | Exact local proposition plus exact bounded quadrature | `near_critical_transition_model_dependence.json`; `distributional_quadrature.py` | Complete | “The local sensitivity is amplified near the transition; exact bounded quadrature is required when roots are censored.” | “The computed opposite-sign probability is a topological phase fraction.” |
| C03 | At nominal `x=0.155`, the existing latent laws span `25.0803 K` in central transition temperature. | Numerical comparison of declared latent laws | `near_critical_transition_model_dependence.json` | Complete | “Within the declared latent-law set…” | “The true specimen transition is uncertain by exactly 25.0803 K.” |
| C04 | At `sigma_x=0.010`, `8.60-14.12%` of the declared composition model remains normal over `0-300 K`, and conditional-root moments are biased by censoring. | Bounded synthetic sensitivity | `near_critical_transition_model_dependence.json` | Complete | “For the declared conditioned Gaussian model…” | “This fraction is directly measured in the Teppe specimen.” |
| C05 | Herrmann’s gap-distribution convention has `sigma_G=sqrt(2)s`. | Source equation audit | Herrmann 1992, DOI `10.1016/0022-0248(92)90851-9`; `herrmann_gaussian_tail_reproduction.json` | Complete | State the convention exactly. | Equating `s`, `sigma_G`, `sigma_x`, and Urbach energy. |
| C06 | The source-aligned square-root convolution reproduces `W_fit/s=0.50504` over `1-100 cm^-1`. | Source-conditioned reproduction | `herrmann_gaussian_tail_reproduction.json`; `spectral_convolution.py` | Complete | “The repository independently reproduces the approximately-`s/2` scale under the declared source conditions.” | “The relation `W=s/2` is universal.” |
| C07 | Changing only the fit window from `1-100` to `100-500 cm^-1` increases inferred `W_fit` by `60.1%`. | Numerical observation-operator result | `herrmann_gaussian_tail_reproduction.json` | Complete | “The apparent tail energy is strongly fit-window dependent for the same synthetic spectrum.” | “The source’s experimental Urbach energy is wrong by 60.1%.” |
| C08 | An observed `W_fit=4 meV` maps to `sigma_G=6.995-12.661 meV` across the declared exponent/window family. | Bounded inverse-sensitivity result | `herrmann_gaussian_tail_reproduction.json` | Complete | “The declared operator family permits an inversion range factor of 1.81.” | “The specimen has this gap-distribution width.” |
| C09 | For an exponential tail, detector cutoff shifts exactly as `-W ln(d2/d1)`. | Exact theorem | `detector_cutoff.py`; derivation 011 | Complete | State as a forward-model theorem. | Applying it outside the tail branch or outside the declared optical model. |
| C10 | In the declared Chang case, changing effective thickness from 5 to 20 um shifts the 50% cutoff by `-16.636 meV` or `+2.494 um`. | Bounded synthetic sensitivity | `chang_2006_cutoff_identifiability.json` | Complete | “For the declared synthetic Chang parameters…” | “This is measured validation from Chang Figure 1; that figure is calculated.” |
| C11 | Any number of tail-only Chang cutoff observations has Jacobian rank at most two for `(Eg,W,ln A,ln b)`. | Exact structural theorem | derivation 011; `chang_2006_cutoff_identifiability.json` | Complete | “More tail-only observations improve precision in two combinations but cannot identify four parameters.” | “All multi-thickness measurements are uninformative.” |
| C12 | Mixed tail/intrinsic observations can restore local rank four but remain conditioned at about `199.81` in the declared design. | Numerical identifiability result | `chang_2006_cutoff_identifiability.json` | Complete | “Formal full rank does not imply a robust inversion.” | “The condition number is universal.” |
| C13 | The exact Kane-type nonparabolic energy is `2Epar/(1+sqrt(1+4 alpha Epar))`. | Exact proposition | `carrier_filling.py`; derivation 012 | Complete | State under the declared isotropic dispersion. | Claiming complete HgCdTe carrier physics. |
| C14 | At the declared Dingrong-density sensitivity point, the parabolic Burstein–Moss estimate exceeds the nonparabolic result by `147.323 meV`. | Bounded synthetic sensitivity | `dingrong_1985_carrier_filling_sensitivity.json` | Complete | “At the declared illustrative mass and nonparabolicity parameters…” | “The Dingrong specimen’s measured correction is 147.323 meV.” |
| C15 | A five-density edge series is locally rank five but has condition number `11034.75`. | Numerical identifiability result | `dingrong_1985_carrier_filling_sensitivity.json` | Complete | “Independent Hall, mass, low-density-gap, and renormalization information remain necessary.” | “Five density points can never identify the parameters.” |
| C16 | The unmarked unified single-state spectrum depends on five nominal parameters only through translated mean gap, gap width, and `A*d`. | Exact structural theorem | `unified_spectrum.py`; derivation 013 | Complete | “Under the declared Gaussian/power-law/single-pass model…” | Claiming the same rank for every possible microscopic spectrum. |
| C17 | The unmarked dense-spectrum Jacobian has structural rank at most three. | Exact theorem plus numerical verification | `unified_spectrum_structural_rank.json` | Complete | “No increase in SNR or point count can remove exact forward-model invariances.” | “Spectroscopy is generally incapable of measuring band structure.” |
| C18 | Two physically different parameter sets produce 281-point spectra equal to within `2.22e-16`. | Exact-invariance counterexample plus numerical verification | `unified_spectrum_structural_rank.json` | Complete | “The two parameterizations preserve the exact identifiable combinations.” | Presenting either parameter set as a real specimen. |
| C19 | An absolutely calibrated nontranslational carrier marker raises rank to four but leaves one combined null vector `(Delta,-Delta,0,-1,+1)`. | Exact marked-model invariance plus numerical verification | `unified_spectrum_structural_rank.json`; derivation 013 | Complete | “A calibrated carrier feature can add one independent direction while one external scale remains necessary.” | Calling the generic marker the Dingrong free-carrier law. |
| C20 | Independent carrier-state and effective-thickness information are necessary for latent-gap recovery under the base model. | Corollary of exact theorem | theorem index; derivation 013 | Complete | State as a model-conditioned measurement-design requirement. | Claiming these two measurements are sufficient for every real HgCdTe spectrum. |
| C21 | The combined framework is externally validated for a real specimen. | External material validation | `dingrong1985_table1_reproduction.json` supplies a real-specimen source-table carrier test; calibrated native spectrum and covariance remain absent | **Partial / submission blocker** | “The finite-temperature carrier branch has a qualified source-table test; complete specimen-spectrum validation remains pending.” | Calling four rounded table entries complete external spectrum validation. |
| C22 | One distributional state model jointly predicts PL displacement and FWHM across Ivanov-Omskii annealing states. | External/model validation | Ivanov-Omskii 2009, DOI `10.1016/j.physb.2009.08.210` | **Open** | Describe as a falsification target. | Treating the tabulated fluctuation parameter as `sigma_x` or `sigma_G`. |
| C23 | The physical Dingrong carrier physics breaks the unified gap/carrier degeneracy. | External/model validation | Dingrong 1985, DOI `10.1016/0038-1098(85)90315-1`; `dingrong1985_table1_reproduction.json` | **Partial** | “The source finite-temperature density integral reproduces the table structure only after exposing a printed-parameter inconsistency; the full below-gap carrier marker remains open.” | Presenting the diagnostic `E^-2` marker or the row-implied `P` as established source physics. |

## Manuscript-level claim hierarchy

### Primary claims

1. **Theorem 3:** structural rank at most three for the unmarked unified spectrum.
2. **Theorem 4:** a calibrated carrier marker raises rank but leaves one combined invariance.
3. **Theorem 2:** tail-only cutoff datasets have rank at most two.

### Supporting quantitative claims

1. `60.1%` fit-window dependence of the apparent tail energy.
2. `-16.636 meV` thickness-induced cutoff displacement in the declared case.
3. `147.323 meV` parabolic carrier-filling overestimate in the declared high-density case.
4. `25.0803 K` latent-law span in the near-critical transition calculation.
5. `11.297 meV` mismatch between Dingrong's printed Eq. 2/printed `P` and its Table 1 Fermi elevations.

### Submission boundary

Claims C01–C20 support an analytical and reproducible methods paper. C21 now has a qualified real-specimen source-table test but remains incomplete because native calibrated spectra and covariance are unavailable. C22 is optional. C23 is only partially supported until the complete physical carrier-dependent spectral branch is reconstructed.
