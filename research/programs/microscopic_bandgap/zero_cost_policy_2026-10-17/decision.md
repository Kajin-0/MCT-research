# R07 current operating policy — zero additional spending

Decision date: 2026-10-17. This decision records the user's explicit $0 additional-spending constraint after the former compute-acquisition proposal. It supersedes procurement and spending proposals, but does not rewrite or reclassify their historical evidence.

## Financial and execution boundaries

- Additional spending allowed: **$0**. No cloud rentals, paid CPU/GPU, storage purchases, hardware upgrades, software purchases, or automatic acquisitions. Do not provision paid resources or recommend expenditure unless the user explicitly changes this constraint.
- Work only with existing computing, stock Quantum ESPRESSO and retained scientific data, plus free resources. Preserve main, dirty DFT, protected raw sources and failed cases.
- The earlier [128 GiB cloud acquisition plan](../compute_acquisition_plan_2026-10-17/decision.md) remains a historical, unexecuted feasibility study. Its conditional PLAN GO is **superseded for acquisition**; purchase and native job authorization were never given.
- The PBE static Hamiltonian diagnostic remains closed; do not reopen source/owner/streaming engineering without a specific new scientific reason and explicit approval.
- One scientific run is never authorized by this policy alone. Any new native HSE execution requires its own science and resource checks plus express user authorization; no automatic composition scan.

## Scientific status at policy adoption

- [Completed primitive HgTe HSE+SOC reference](../primitive_k4_hse_2026-10-17/decision.md): conventional EXX SCF converged with dexx 2.3e-10 Ry and projection-labelled E_Gamma6-E_Gamma8 about -289.586505 meV. Its strict 1e-8 full-density time-reversal and spatial-symmetry gates **FAIL**. This remains a conditional endpoint reference, not an error-certified material inversion mass.
- [Fully relativistic Hg/Cd VCA compatibility](../vca_fr_compatibility_2026-10-17/decision.md): specific stock virtual_v2.x, SG15 projector/SOC reader combination **GO within endpoint criteria**, five native dry tests and four PBE+SOC endpoint SCFs passed. Largest raw 44-level endpoint differences: Hg 0.0000403 meV; Cd 0.000208 meV versus frozen 0.1 meV threshold. Cd radial truncation and inherited metadata are documented. No mixed-composition SCF or VCA HSE exists.
- Existing Cd-substituted PBE results inform chemistry but cannot be spliced into the HSE endpoint as an HSE alloy coefficient. The critical random-alloy composition x_c remains unknown.

## Next decision-changing scientific result

The first useful new HSE output is an independently converged two-atom Hg0.875Cd0.125Te VCA HSE+SOC state at physically matched primitive k4/q4, 50/200/Fock200 Ry, FD 0.001 Ry, with independently tracked Gamma6/8 character, charge/occupation checks, and measured full-density symmetry defects. An increase from 14 Hg beta projectors to 24 VCA cation projectors needs fresh resource qualification before any run. Endpoint PBE reader compatibility does NOT admit HSE accuracy, convergence, or a physical alloy x_c.

If the VCA pseudo ceases to be valid under a tested physical criterion or its native HSE workload cannot be admitted on the current hardware, stop and use the retained negative result to select a different established low-cost method. Do not create another custom exchange/owner framework.

No native calculation, cloud action, purchase, new pseudopotential generation, or change to old scientific data is part of this policy recording.
