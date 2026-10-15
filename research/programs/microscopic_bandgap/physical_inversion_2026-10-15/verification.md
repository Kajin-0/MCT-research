# Verification scope and independent checks

Run the four commands in README, then `git diff --check`. Results/logs and
`verification.json` are retained. No numerical DFT/MPI invocation or external
material dataset is used. The proofs, not finite float samples, establish the
universal statements. None of the model results is called material validation.

| Check | Independent construction / falsification | Outcome |
|---|---|---|
| A1/A2 accounting | Average two dense Hermitian resolvents vs augmented-space formula and exact Fraction-polynomial coefficient identity; direct Schur inverse | PASS; full causal, projected chemical difference positive Im17.26886568 in synthetic energy units |
| A3 covariance | Exact two-realization ensemble with opposite common/mass cross correlation, same separate variances; arbitrary noncommuting6x6 coherent matrix | PASS; own-reference spectra identical, aligned mass kernels opposite; diagonal-contraction error<3e-17 |
| B1 constants | Exact rational worst-case3/4,1/3 constants; direct numerator identity vs inverse transform | PASS; a_min=1/18 and positive margin5/36 at eta1 |
| B1 continuum | Six Z/eta cases with actual continuum through the atom; analytic logs vs independent quadrature; causal perturbed measure | PASS; atom/root and propagated input-error bounds contain all tested errors |
| B1 nonanalytic background | Positive inverse-square-root spectral density at atom threshold | PASS; no common support gap needed. This is the spectral measure, not B2 coupling measure |
| Native-free Hermitian bath/reference | Three-state dense inverse vs spectral decomposition, common energy shift | PASS; finite floating tolerance; no physical Hamiltonian claim |
| Missing atom | Continuous Lorentzian sectors with different resonance widths and equal inverse centers; bounded uniform continuous measure too | Counterexamples PASS; a root alone does not establish a sharp branch |
| Common-energy proxy | Same atom energy, different causal background/residue | Counterexample PASS; finite-eta inverse difference is nonzero despite coincident atoms |
| Conditional composition | Explicit synthetic linear branch order and independent slope; inverse-root reconstruction | PASS; actual synthetic error5.13e-7 within conservative3.59e-3 bound. These fractions are NOT material x_c estimates |
| B2 normalization | Exact IR power integrals vs quadrature; explicit nonnegative Friedrichs thresholds with p=.5 and1.5 | PASS; real inverse zero and zero damping coexist with Z=0 for p=.5; p=1.5 allows Z5/6 |
| C1 actual geometry | Read accepted16cell neighbor indices; count host/oneCd/unshared/shared independently; exact Bernoulli fractions and causal mixture | PASS; N2 present, N3 absent; invisible term changes averaged Green function |
| Missing transversality | Cubic branch order under constant perturbation | Counterexample PASS; O(epsilon) root error cannot be presumed |
| Preservation | SHA256 old native/refused records, DFT tracked diff and stock QE; branch scope and package syntax/links | PASS as recorded in verification.json; no DFT write/native job, main/goal/session change |

The initial phase1 local test found SymPy unavailable; no dependency was
installed. Exact rational polynomial arithmetic replaced that optional tool.
No native numerical result was retried or relabeled. The old HSE/PBE failure
gates and acceptance thresholds are not altered by these new model examples.

The primary-literature audit is bounded: full Krishtopenko, Wei–Zunger and
Friedrichs author texts; Alowa publisher preview only. It is adequate to reject
broad method/environment novelty, insufficient for a historical originality
claim about specific B1 constants or this synthesis. Literature-access limits
are scientific limits, not grounds to speculate about a missing paper.
