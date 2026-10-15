# R07 analytical physical-inversion phase — 2026-10-15

Start with [decision](decision.md) and [claim registry](discovery_registry.md).
No native DFT/HSE/MPI jobs, empirical fitting or new physical x_c in this phase.

- [Observable definitions](observables.md): periodic signed order, Kane mass,
  sharp atoms, real inverse roots, broadened peaks, Green zeros and topology.
- [Chemical/disorder accounting](chemical_disorder.md): exact mean, projection,
  causal total kernel, full/residualT and the missing common/mass correlation.
- [Continuum-to-sharp sufficient certificate](sharp_atom_certificate.md): atom,
  resolution, independent input error and conditional composition interval.
- [Threshold eligibility obstruction](threshold_eligibility.md): even zero
  linewidth/real inverse zero can lack an atom.
- [Identifiability and root conditions](identifiability_and_root.md),
  [actual-input matrix](input_matrix.md), [ONE next input](one_next_input.md).
- [Claim-level literature boundary](prior_art_matrix.md),
  [phase decisions](decision_ledger.md), [reset handoff](handoff_ledger.md),
  [verification](verification.md).

Small checks use the existing environment, not native QE:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_bandgap/physical_inversion_2026-10-15/check_accounting.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_bandgap/physical_inversion_2026-10-15/check_sharp_atoms.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/User/opencode_workspace/DFT/.venv/bin/python research/programs/microscopic_bandgap/physical_inversion_2026-10-15/check_identifiability.py
python3 research/programs/microscopic_bandgap/physical_inversion_2026-10-15/verify_package.py
```

Proofs provide the theorems; float checks are independent falsification tests,
not interval arithmetic or material validation. No new dependencies installed.
