# R07/R08 retained-spectral observable gate — 2026-11-19

**Status:** Independent replay of *committed* finite-spectrum central quantities: **PASS**. Conditional estimator-dependence conclusion: **PASS within the archived model and error terms**. Physical HgCdTe random-alloy mass, broadenings, and publication novelty: **NO-GO**.

**Branch:** audit/r07-spectral-observable-gate-20261119, based exactly on R07 SHA 5135e16a9d22efa1b5535cd3a1612c8e2aeaad41. This tranche adds a read-only Python standard-library replay and isolated tests. No QE, MPI, network, HDF5, original result edit, branch merge, spending or new data acquisition.

## Scientific question and exact observables

Can the R07 xCd=0.25 *periodically ordered*, same-stoichiometry Cd pair be assigned one scalar, probe-independent "disorder correction" to an intrinsic bandgap or inversion mass?

Let s be the probe center measured relative to **each specimen's own Fermi level** and W a freely selected spectral width. Given the committed 352-band energies e_n and sector-normalized fixed-frame weights w_{nu,n}, define

    C_nu(W,s) = [sum_n w_{nu,n} (e_n-s) exp(-(e_n-s)^2/(2 W^2))]
                / [sum_n w_{nu,n} exp(-(e_n-s)^2/(2 W^2))].

The Gaussian ordering is C_6-C_8; the environment contrast is shared minus unshared at a common (W,s). This is a finite-spectrum *estimator*, not a quasiparticle gap.

For eta>0 use the scalar retarded Stieltjes projection

    g_nu(eta) = sum_n w_{nu,n}/(i eta-e_n),

and the **archived convention**

    Q(eta) = Re[g_8(eta)^(-1)-g_6(eta)^(-1)].

The contrast is Q_shared-Q_unshared. The scalar inverse is neither the full 6x6 matrix inverse nor an intrinsic linewidth. These two functions must not be treated as interchangeable definitions of physical mass.

The replay reads four original CSV files and recomputes all **15 Gaussian rows** and **three scalar inverse rows**. No stored central result is copied into the arithmetic. It separately reads the old JSON solely to compare the independent values and to preserve the authors' explicitly limited uncertainty envelopes.

## Independent numerical findings

Both central replay families agree with the archived report within 1e-11 eV, and the independent direct 352-band calculation agrees to approximately 1e-15 eV in the tested floating-point implementation.

### A. Scalar inverse contrast versus eta

| eta (meV) | shared minus unshared (meV) | archived conditional interval (meV) |
|---:|---:|---:|
| 25 | -81.625899 | [-142.343, -20.908] |
| 50 | -81.474454 | [-111.443, -51.506] |
| 100 | -80.463618 | [-95.753, -65.175] |

The tested central values span **1.162280 meV**, approximately **1.431%** of the mean absolute contrast. The three *conditional* intervals exclude zero. This is limited eta stability within a fixed, truncated PBE spectrum, **not** a certified physical 81 meV gap correction.

### B. Gaussian contrast changes sign as the probe center moves

| Gaussian W (eV) | s relative to own EF (eV) | shared minus unshared (meV) | archived conditional bound (meV) |
|---:|---:|---:|---:|
| 1.0 | -0.5 | -19.329932 | 6.127 |
| 1.0 | 0.0 | -1.488620 | 6.398 |
| 1.0 | +0.5 | +39.193422 | 13.544 |
| 2.0 | 0.0 | -2.076649 | 9.251 |
| 2.0 | +0.5 | +2.198875 | 13.215 |

The W=1 eV, s=-0.5 and +0.5 values have **opposite signs even after applying the original conditional bounds**. They do *not* have a common absolute electronic reference; each spectrum retains its own EF anchor, just as in the original study.

The independently calculated **central-value only** roots of the Gaussian contrast as a function of the *probe-center offset*, over [-0.5,+0.5] eV, are:

| W (eV) | central zero of probe-center offset s (eV) |
|---:|---:|
| 1.0 | +0.0266033623 |
| 1.5 | +0.0303476380 |
| 2.0 | +0.2471945593 |

These are mathematical zeros of the chosen spectral estimator. **They are not composition crossings x_c, topological transitions, uncertainty-certified roots, or experimental optical features.**

A common energy-origin translation applied consistently to both eigenenergies and the probe reference leaves the centroid invariant. Moving *only* the probe center relative to each EF changes the question being asked; the reversal is a sensitivity to the observation operator, not an energy-gauge inconsistency.

**Decision:** The committed ordered-cell evidence falsifies treating the measured central contrasts as one universal, probe-independent scalar environment correction. This is an estimator-level counterexample; it does **not** prove that every possible physical bandgap estimator is configuration-sensitive or that random HgCdTe has an 81 meV disorder shift.

### C. R08 remote-state domination blocks a near-edge scattering inference

The independently checked *committed summary identity* is

    S_total = S_local + S_nonlocal + S_interference.

At saved k-index 8, final states more than 5 eV from the initial Gamma-sector energy carry approximately **95.8%** of the all-band Γ6-like strength and **97.5%** of the Γ8-like strength. In the eight saved irreducible k points, the ±0.5 eV non-Gamma window has only two final bands at index 2 for Γ6-like initial states, and none for Γ8-like initial states.

Thus even a large all-band local/nonlocal cancellation does not identify a physical near-edge on-shell scattering rate. The archived raw 277,311-byte energy-binned evidence packet is **not** reconstructed or independently replayed here; only the committed 16-record summary identities and phase-space counts are checked. Operator-screening, random statistics, full-BZ integration, native QE action parity and physical linewidth remain outstanding.

## Scientific synthesis and proposed target

The useful high-impact question is narrower than "the alloy configuration changes the gap":

> **When is a coherence-preserving, averaged HgCdTe electronic structure sufficient to predict a *specified* inversion or absorption observable within a defensible uncertainty?**

The R07 ordered-cell results make observable dependence a decisive issue. R08 could eventually explain small incoherent near-edge weight, but the present bare ionic calculation cannot supply the missing screened physical self-energy. R01/R03 can eventually supply measurement operators only after independently justified source and parameter contracts.

A strong contribution would jointly establish:

1. A matched same-Hamiltonian, same-geometry *ensemble* spectral observable (configuration uncertainty and finite-size convergence).
2. A defined physical energy alignment, Γ-sector projector validity, symmetry resolution and full-H/eigenpair uncertainty.
3. A screened microscopic scattering calculation **or a rigorous bound** on the relevant self-energy contribution, without double counting coherent chemistry.
4. A held-out experimentally specified observable, or a theorem with materially new conditions compared with the literature.
5. A sensitivity/uncertainty gate that distinguishes VCA error from finite spectral-window, algorithmic and specimen effects.

A *negative* result (a rigorous small VCA-bias bound) could be publishable if it is genuinely stronger and more predictive than existing prior art; the current results do not yet establish that bound.

## Existing prior-art novelty boundary

- Nicklas and Wilkins, *Phys. Rev. B* 84, 121308 (2011), DOI 10.1103/PhysRevB.84.121308, already predicted HSE/SQS alloy inversion near x~0.17.
- Camassel et al., *Phys. Rev. B* 38, 3948 (1988), DOI 10.1103/PhysRevB.38.3948, already reported near-cancellation of disorder effects at the band edge.
- Wang, Luo and Zunger, *Phys. Rev. Materials* 3, 044605 (2019), DOI 10.1103/PhysRevMaterials.3.044605, reported negligible incoherent weight in HgCdTe under their atomistic unfolding model.
- Krishtopenko, Antezza and Teppe, *Phys. Rev. B* 106, 115203 (2022), DOI 10.1103/PhysRevB.106.115203, already treated disorder-renormalized Kane masses.
- Alowa et al. (2025), DOI 10.1088/1361-6463/adb2a0, considered configuration and strain effects in HgCdTe.

**Novelty gate remains OPEN/NO-GO:** resolution-dependent spectral estimators, alloy-configuration-dependent bandstructure, disorder mass renormalization and weak near-edge scattering are not independently novel claims. Any material-specific theorem or new mechanism needs targeted prior-art exclusion and a demonstrated discriminating physical prediction.

## Next decision — do not launch expensive HSE

**G2 replay:** PASS. **Interpretation as one scalar gap correction:** REJECT. **R08 physical weak-scattering mechanism:** NOT ESTABLISHED. **HSE virtual-crystal reference:** still fails the frozen 1e-8 full-density symmetry gate. **Random-alloy x_c:** UNPREDICTED. **Manuscript:** NO-GO.

Next minimum useful science:
- Requalify the archived HSE sector/density/full-H error budget through read-only independent analyses of actual preserved wavefunctions if accessible, without silently moving numerical acceptance criteria.
- Obtain matching same-Hamiltonian unfolded spectral data for at least two distinguishable x=0.125 configurations or a controlled validated physical bound; preserve model/geometry/functional/projector equivalence.
- Require genuine finite-k, near-energy, screened scattering information before asserting a cancellation mechanism.
- If none is obtainable without expensive new calculations, stop at this evidence boundary rather than fitting a new gap equation.

## Reproduce and limitations

    python tools/audit_r07_retained_spectral.py
    python -m unittest discover -s tests -p 'test_r07_retained_spectral_gate.py'

Uses Python standard library only; reads archived committed spectra and numerical summaries. It neither mutates the previous evidence nor fetches private VPS data. The replay validates *internal algebra and reported central values*, not native DFT correctness. Existing conditional bounds omit functional error, BZ mesh, configuration statistics, lattice relaxation, pseudopotential transfer, full-H/eigenpair and experimental measurement uncertainty. The original R07/R08 refusal decisions remain authoritative for these missing inputs.

Source records:
- research/programs/microscopic_bandgap/pair_environment_2026-10-15/decision.md
- research/programs/microscopic_bandgap/pair_environment_2026-10-15/numerical_result.json
- research/programs/microscopic_bandgap/pair_environment_2026-10-15/{shared,unshared}_Gamma{6,8}_spectrum.csv
- research/programs/microscopic_bandgap/stage1_pbe_vca_2026-10-17/decision.md
- research/programs/microscopic_bandgap/stage2_pbe_vca_2026-10-17/decision.md
- research/programs/microscopic_bandgap/vca_x0125_hse_2026-10-17/decision.md
- research/programs/microscopic_ionic_scattering/finite_k_interference_decision.md
- research/programs/microscopic_ionic_scattering/finite_k_interference_summary.json
