# R07 Stage 1 — Γ overlap-reference reconciliation (2026-10-17)

Read-only re-evaluation of archived QE HDF5 spinors. No new QE, no parameter adjustment, no change to numerical contrasts or frozen acceptance rules.

The two reported overlap pairs are **both correct but refer to different projector subspaces**:

| Projector onto VCA selected Γ bands | Γ6 (31–32) | Γ8 (35–38) |
|---|---:|---:|
| Original fixed HgTe Γ6/Γ8 frame, transported into primitive VCA basis (used for Gaussian and scalar inverse spectra) | 0.9998891897936594 | 0.9996082772145374 |
| Native, self-consistent 16-atom HgTe Γ6/Γ8 host eigenspace projected into the same primitive basis | 0.9998081304674815 | 0.9998478497435468 |

**Reporting correction:** `stage1_contrasts.json:VCA_Td.{Gamma6,Gamma8}.VCA_frame_weight_in_selected` names the **first**, original fixed-frame value. `decision.md` inadvertently described the **second**, native-host-frame overlaps as if they were fixed-reference captured weights. Interpret those reported numbers as native-host-frame overlaps. Do **not** overwrite the committed data or substitute one projector for the other. The original fixed frame remains the spectral-statistic definition; the native frame is supplementary classification/transport diagnostics.

Projection computation: original fixed spinors in `chemical_pbe16_p2_2026-10-15/science.py:frames()`, native HgTe host band indices from `multiplet_result.json` (Γ6=275–276, Γ8=287–290), primitive Γ embedding by even reciprocal vectors `G_super=2G_primitive`. Projection is `sum_{frame eigenstates a, chosen VCA bands n} |<frame_a|VCA_n>|^2/d` for d=2 or 4. Both saved-wave calculations yield the numbers above, not spectral values inferred from rounded eigenenergies.

**Stage 2 decision:** At xCd=.25 the independently accepted environment difference for the scalar inverse response is approximately −81.474454 meV, so any single identical VCA reference must differ from at least one ordered scalar result by ≥40.737227 meV on the central measured values (triangle inequality). A new x=.25 PBE VCA would allocate that mismatch across the two selected ordered cells and check same-reference algebraic closure, not produce random-alloy variance, screening or physical xc. Retain the split Γ8 in the shared configuration. A single Stage 2 acquisition is scientifically defensible but **NOT authorized** here. Stop the PBE bridge after separately authorized Stage 2, if it occurs, and reassess the physical disorder-aware inversion criterion. R08/HSE remain unchanged.
