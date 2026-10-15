# Focused verification — theory/models only

Three scripts and a preservation verifier, no native program or broad test
suite. Exact proofs supply the general claims; small floating tests challenge
them independently. No synthetic number is material validation or x_c.

| Claim/test | Independent check | Result |
|---|---|---|
| 8-state SOC/HH/R02 convention | Angular matrices vs existing R02 coupled basis; all24Td and explicit antiunitary/TR | PASS; projector3.33e-16, Kane covariance2.37e-16 |
| Coherent-zero pair IR channel | All16Bernoulli configurations at three declared compositions, separate centered tensors; two tetrahedra sharing one site | PASS; covariance(8/3)k^2 I, nonzero HH weight, zero one-body cross/remote pair covariance |
| Dark/nonanalytic/flat/anisotropic limits | HH projector/current action, direct volume integration for qx^2+qy^2+qz^4, finite-curvature kernel limit | PASS; exponent formula assumptions enforced, no exact-alloy exponent inferred |
| Actual optical family | Small finite Kane oscillator matrix with actual jx+/-i jy; both M signs/zero | PASS; energies and oscillator strength, two-field signed extraction and held-out third field |
| Mass/third-field error budget | All16corners of independent synthetic energy/field errors against exact model values | PASS; no post hoc material tolerance |
| Zero-mean optical bias | Equal +/-m with equal weights, then independently computed actual Kane-current weights | PASS; positive M_opt in both, third-field discrepancies-.015699/-.043191 in synthetic units |
| Same G / different optics | Two exact finite ensembles plus common continuous scalar convolution; canonical current response | PASS; G difference0, finite transition2a versus no finite-frequency absorption |
| Liouvillian controlled closure | Three noncommuting centered perturbations, dense exact average vs quadratic Dyson prediction | PASS; error4.79278e-5 below.00132066, common scalar commutator exactly0 |
| Minimum source-only contraction | Independent complete Liouvillian resolvents and explicit source perturbations | PASS; scalar closure/error and source bound, not full tensor reconstruction |
| Weak-IR/no-atom resolution scale | Exact negative-energy denominator and independent complex quadrature vs analytic transform | PASS; arbitrarily pole-like finite-eta example with exact zero atom; no uniform limit exchange |
| Global phase norm premise | Tiny Hermitian gap perturbation bound only | PASS for gap; explicitly NOT TR/index/material validation |
| Protection/scope | Old frozen hashes, stock ELF, DFT tracked diff, R02source, research branch, local links/syntax | PASS in verification.json; no old package or R02/R05 state edit |

One initial binary Liouvillian example made second order exact; a declared
three-state noncommuting ensemble was used before publication to test a
nonzero remainder. In the final resolution check a reused eta output name was
corrected before acceptance; the verifier now asserts its recorded scale.
No native failure, old tolerance, physical data or accepted verdict was changed.

Common scalar cancellation assumes canonical filling, not arbitrary spatial
scalar disorder. Optical moments require the stated tail/window/line adapter;
a Lorentzian has no full absolute first moment. The3D/8-band material response,
finite-B disorder vertex, HSE stationarity and zero-T/strain/carrier corrections
remain uncertified. Primary comparison is bounded; novelty remains UNVERIFIED.
