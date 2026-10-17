# R08 — bounded energy-resolved ionic interference audit (2026-10-17)

**Gate:** Frozen wavefunction re-evaluation PASS for bare scattering amplitudes only. Low-energy random-alloy coherence mechanism NOT established. No SCF/DFT, paid compute, or R07 changes.

## Reproducible evidence

- `finite_k_interference.py` extends the existing `finite_k_bare_probe.py` and reruns identical Hg/Cd local + relativistic nonlocal projections on the archived 8 irreducible k points and 44 final states, retaining per-final-band local, nonlocal, interference and combined squared matrix elements for each of two initial manifolds. `finite_k_energy_resolved_results.json` is a 277,311-byte local evidence packet retained off-repository; its SHA256 is in `finite_k_interference_summary.json`. Re-execution recreates the packet at zero incremental spending.
- `finite_k_interference_summary.json` is the compact committed sufficient statistic for energy bins: `near` (|ΔE|≤0.5 eV), `intermediate` (0.5<|ΔE|≤5 eV) and `remote` (|ΔE|>5 eV), plus `all`. Averages divide local, nonlocal, cross and total strengths by initial manifold dimensions: Γ6-like /2 and Γ8-like /4. The identity S_total=S_local+S_nonlocal+S_cross is checked per-band and for all bins (tolerance 1e-10 eV²). Entries in eV² *per initial state*. The source is a single-site bare ionic potential; no screened response or final-state distribution integration.

## What the numbers establish

- Γ6→Γ all-band: local 117.356, nonlocal 100.312, cross **−216.897**, total **0.771** eV² per initial state (99.65% destructive reduction of separate squared contributions). Γ8→Γ total **1.246** eV²/initial; 99.07% reduction.
- Γ6→k8 all-band: local 112.723, nonlocal 102.996, cross **−212.031**, total **3.687** eV²/initial (98.29% reduction). Γ8→k8: local 48.864, nonlocal 72.559, cross **−103.403**, total **18.020** eV²/initial (85.16% reduction).
- At Γ, the **near-energy six-band** Γ6 window has a combined **0.276118** eV²/initial and a cross term **−19.599554** eV²/initial; the Γ8 near window combined **0.312741**, cross **−21.572272**. The cancellation **also occurs in this energy-selected Γ subset**. But the window includes Γ itself and is not a scattering phase-space integral.
- The only non-Γ ±0.5 eV overlap in archived eight points is k2 for Γ6: two final bands, combined strength approximately **1.5474555e−14 eV²/initial** (total 3.0949110e−14 eV² over the doublet). All other non-Γ ±0.5 eV windows contain zero final bands. They are sparse sampling gaps, not proof of vanishing on-shell scattering.
- At k8, states with |ΔE|>5 eV contribute **3.533** out of **3.687** Γ6 strength (~95.8%) and **17.561** out of **18.020** Γ8 strength (~97.5%). This makes it especially inappropriate to interpret the all-band destructive interference as an actual low-energy linewidth suppression. The remote-bin cancellation cross terms are **−199.321** and **−99.654** eV²/initial respectively.
- Cancellation arises in both near/remote groupings, but the near-Γ *nonzero-momentum energy-conserving* question is still untested because the saved k mesh is too sparse. Within a fully relativistic norm-conserving pseudopotential, the local/nonlocal split is representation-dependent; the *sum* is the relevant bare observable.

## Integrity and stopping rule

Gamma regression remains 1.495e−16 eV (local) and 2.221e−15 eV (nonlocal); these are reused-formula checks, not native QE action qualification. Finite 44-band coverage may bias remote strength decomposition. No dense near-Γ states, screening, random alloy correlations, phase-space normalization, linewidth, lifetime, or physical critical composition. R07 frozen strict 1e−8 symmetry failures unchanged.

**Decision: bounded decomposition complete.** It confirms destructive local/nonlocal interference in the existing operator but rejects a physical scattering-rate or near-Γ coherence mechanism claim on current evidence. No further rerun or native computation justified solely by this result.
