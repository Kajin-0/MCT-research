# Actual evidence versus the minimum physical information

All numerical entries below are carried from accepted records; none is a new
DFT result. Source links identify their exact observable/uncertainty domains.

| Evidence | What it constrains | What it does not identify |
|---|---|---|
| [PBE8 ordered x=.25 k3](../chemical_k3_2026-10-14/decision.md): W2 response +.392177486eV | Fixed-frame Gaussian chemical response at specified cell/BZ/PBE/FD settings; small-grid/cutoff sensitivity | Sharp random-alloy poles, aligned impurity kernel, HSE correction or composition law |
| [PBE16 ordered x=.125](../chemical_pbe16_p2_2026-10-15/decision.md): periodic signed order change +.169033285eV; W2 +.201458261eV; inverse eta.05 +.135136468eV | Actual Td/Kramers-compatible periodic PBE branch order and separately defined spectral redistribution | No dilute slope from one16cell, no cross-composition gap fit; different cell/BZ from PBE8. Own-EF inverse response does not preserve arbitrary aligned common-mode correlations |
| [PBE16 same x=.25 environment contrast](../matrix_environment_2026-10-15/decision.md): inverse-matrix norm82.917971meV, conditional lower57.679585meV | Same-cell configuration dependence and positive-measure finite-window bounds. N2 is now sampled; shared Gamma8 splits into Kramers pairs | Static N2 operator, N3 response, full configuration law, quartets in broken symmetry, or real mass. Gaussian sign remains unresolved |
| [One-state HSE H304+12](../single_state304_2026-10-15/decision.md): native329.21s, peak5.56GB; symmetry/Hermiticity pass | Full-action information for one explicitly frozen144e trialD0, not a cross-run splice | Physical stationary HSE host, nonlinear H[D1], Cd self-consistency or zero-T bulk limit. FD residual .023784678Ry and conditional FD-distance lower1.3115e-7 rule out the claimed1e-8 closure |
| [HSE residual response](../hse_residual_response_2026-10-15/decision.md): eta.5 inverseordering-.729914eV; conditional interval[-1.232296,-.227533]eV | Query-action/positive-eta error mechanism without D, conditional on an unproved whole-action allowance | Thermodynamic sharp-atom weight Z, a real-axis mass, physical linewidth, common-mode energy, or x_c. Tested artificial complements did NOT reverse the sign; they were not complete316-query alternatives |
| [Stage0 archived spectroscopy](../evidence_acquisition_2026-10-11/decision_memo.md) | Availability/independent-assay/raw-calibration audit; published evidence retains its own scope | No accepted raw/metrology-complete specimen pair to certify the proposed zero-T operational sign bracket; no outreach authorized here |

## Minimal sufficient input sets depend on the claim

| Intended claim | Irreducible information (possibly supplied through an equivalent adapter) | Error/decision gate |
|---|---|---|
| Finite-eta response of the fixed HSE trial | Specified physical projectors and certified whole-query action/tail error | Existing residual theorem; inverse denominator discs exclude0. Not a material gap |
| Periodic model's signed Gamma order | Stationary chosen Hamiltonian, physical irrep tracking, full-space eigenstate errors and lattice/BZ/occupation convention | Isolated single-copy multiplets; no forced quartet when symmetry is broken |
| Random-alloy sharp signed order | Independently controlled g6,g8 on a composition interval, physical frame/reference, nonzero tracked thermodynamic atom weights/background bounds | B1, or an independently valid sharp-pole theorem. Current finite spectra cannot establish the atom hypothesis |
| Controlled weak-contrast approximation to those functions | Aligned mean and full required covariance contractions, including common/mass and directional terms, plus contrast/omitted-cluster bound | C3.1. Within the scalar/mass vertex class S_+,S_- suffice for diagonal traces at second order; no universal two-number closure |
| Unique sharp-order x_c interval | Previous row's spectral eligibility, certified sign margins, uniform ordering error and nonzero composition transversality | epsilon_Delta/s or C4.1. No such material margins/slope are present |
| Bulk topology or mobility boundary | Global physical occupied/Green/localization structure and its hypotheses | Gamma-only data are insufficient even if exact. A scalar inverse zero is not an index |

An input is indispensable only up to equivalent information: one can determine
an exact averaged propagator without separately reconstructing each local
tensor, and one can certify an atom by other means than B2's measure. We do
not claim that a particular code, supercell or impurity calculation is the
unique route. No finite list of free fitted constants can replace these
unbounded unknown operator/function classes without a controlled restriction.
