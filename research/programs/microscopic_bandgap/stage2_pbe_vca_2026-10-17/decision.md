# R07 Stage 2 — completed final PBE bridge (2026-10-17)

**Status:** ONE separately authorized xCd=0.25 stock-QE PBE+SOC primitive VCA calculation executed successfully. The existing 16-atom *shared* and *unshared* Cd configurations were reused unchanged. No HSE, R08, 32-atom campaign, retries, empirical fit or spending. The controlled **PBE bridge is now closed**.

## Method and provenance

- Primitive 2-atom zincblende Hg0.75Cd0.25Te virtual crystal at fixed a=6.46 Å; 46 spinor bands, 2x2x2 unshifted k-grid, PBE+SOC, SG15 fully relativistic norm-conserving Te, ecutwfc/rho 50/200 Ry, FD 0.001 Ry.
- Mixed cation PP generated once with stock QE7.5 `virtual_v2.x` from the pinned Hg and Cd parent SG15 PPs with Hg mixing weight 0.75. PP SHA256 `853d5873d257693c98cf5a8969cd7b78164eff32a0fdaaef22dfe678bbe7e51a`. It retains 24 radial beta projectors, 20 valence electrons, full relativistic SOC, PBE, zero interspecies D mixing. Nonlocal block equality to 0.75D_Hg / 0.25D_Cd is exact; local potential arithmetic mismatch 1.066e-14 Ry. This is valid source-formula qualification, **not** proof of mixed-atom pseudopotential transferability.
- First preparation root `r07s2_20261017` stopped **before** owner/native execution because PP was copied using generator filename; it remains an incomplete non-executed record. Fresh root `/home/User/opencode_workspace/DFT/.local/r07s2b_20261017` was generated instead and all pinned input/source/PP checks passed.
- Fresh dry non-QE owner test passed with MPI 2 rank exits/cgroup retirement; single native SCF `JOB DONE`/exit 0; 10.0489s owner elapsed, kernel memory peak 143790080 bytes (manager 146673664), sampled RSS peak 226996224, max sampled output 1802240 bytes; systemd inactive/success. Bounds: 12 GiB RAM, zero swap, 12 tasks, 900s, 10GiB disk and 4GiB host RAM reserves. **No native retry**.
- The fixed Γ projectors are the independently accepted 50Ry **native HgTe 16atom Γ6/Γ8** frame used in the accepted `pair_environment_2026-10-15` measurements, not Stage 1's different original 40Ry frame. Projected VCA Γ6 bands33–34 and Γ8 bands35–38 pass Td classification; frame-captured weights 0.999189054 (Γ6) and 0.999348335 (Γ8).

## Coherent reference location (all eV, own Fermi reference per specimen)

| Observable | VCA x=.25 | Unshared ordered | Shared ordered | Unshared−VCA | Shared−VCA |
|---|---:|---:|---:|---:|---:|
| Gaussian centroid Γ6−Γ8 W=2eV | −0.690173144 | −0.646231351 | −0.648308000 | +0.043941793 | +0.041865145 |
| Scalar inverse Γ ordering η=.05eV | −0.690797518 | −0.685188200 | −0.766662654 | +0.005609317 | −0.075865136 |

Algebraic closure (by independently reused own-Fermi source packet):
Gaussian `(shared−VCA)−(unshared−VCA) = −2.076648723 meV`;
inverse `=−81.474453652 meV` — equals original *shared−unshared* contrasts at computation precision. This identity validates consistent reuse, not a physical uncertainty envelope.

**Placement:** VCA lies **outside both** ordered values on the Gaussian W2 axis, below both. VCA lies **between** the two ordered scalar inverse-resolvent values, closer to the unshared response (5.609meV versus 75.865meV). The old 81.474meV environment contrast implies a purely algebraic minimum max deviation of 40.737meV for any common reference to these scalar central values; the actual max here is 75.865meV.

## Symmetry and qualification boundaries

The VCA Γ6/Γ8 pair/quartet remain well-defined symmetry multiplets in their own Td primitive lattice. Unshared 16atom ordered Γ8 is nearly quartet-degenerate. Shared 16atom Γ8 is **not** quartet-degenerate: two Kramers doublets lie at approximately −2.023970 and +2.023970 meV relative to the shared specimen's Fermi energy, giving **4.047940 meV** splitting; the ordered Γ6 pair lies at −712.120005meV. DO NOT report their artificial average as a sharp Γ8 level or common topological mass. The Gaussian/inverse observables retain their true split-state spectral weights.

All derived contrasts are **retained-spectrum numerical probes** using own-Fermi references, not an aligned cross-sample impurity potential, a material quasiparticle self-energy, a random-alloy variance, a thermodynamic enthalpy, or a physical critical x_c. Conditional original ordered pair error intervals persist; no full method/SCF/PP/disorder/finite-size uncertainty or material screening identified. Relative to Stage 1 x=.125, the Γ reference projector conventions differ; do NOT interpret cross-composition scalar numbers as a fitted composition law.

**Decision:** Stage 2 acquisition COMPLETE, native owner PASS, empirical controlled PBE bridge CLOSED. Future physics work requires independent first-principles screened, composition-dependent disorder parameters and a symmetry-consistent Γ inversion criterion, not automatic additional PBE/HSE or x=.25 jobs. Physical x_c remains UNPREDICTED. No other native authorization.
