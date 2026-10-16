# Focused independent verification, with limits

All commands execute from **MCT**, not DFT. No DFT project command, driver,
setup script or source module is invoked. The existing h5py-equipped Python
interpreter is borrowed read-only with bytecode disabled. Writes are restricted
to this new MCT package. No native executable, MPI, service, source build,
synthetic mass/optical example or public-data search.

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  /home/User/opencode_workspace/DFT/.venv/bin/python \
  research/programs/microscopic_bandgap/stationary_reference_audit_2026-10-16/audit_native.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 \
  /home/User/opencode_workspace/DFT/.venv/bin/python \
  research/programs/microscopic_bandgap/stationary_reference_audit_2026-10-16/metadata_audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 \
  /home/User/opencode_workspace/DFT/.venv/bin/python \
  research/programs/microscopic_bandgap/stationary_reference_audit_2026-10-16/independent_checks.py
```

Actual main audit39.13s, peak781316KiB (~763MiB). Full native-data analysis
performed once successfully; no broad test suite. A prior read-only assertion
that original/export coefficient bytes were equal FAILED before result output;
the completed assessment retains explicit false equality and numerical frame
distance. No scientific gate was changed, no old refusal or frozen file edited.
The HDF5 charge container hashes differ while both named numerical datasets
match exactly; do not call container inequality a measured charge difference.

- All29 prior P1 source pins verified before analysis. Original SCF schema
  hashes checked against the earlier expansion-parent pins. Original8wfc+8ACE
  and64exportedwfc files per run are freshly pinned for future audit, not
  claimed historically fingerprinted. All opened scientific sources rehashed
  unchanged after the main check; no supervisor state path opened.
- Exact cold formula reproduces native occupations. Decimal summation of the
  saved weights/occupations and independent saved rhoG×cell volume verify
  neutrality. Brent and independent bisection agree on a hypothetical FD root
  of the **stored spectra**, not a newly solved native state.
- All24Td Γ-frame/density/ACE probe comparisons and64-point f120 Θ/C3/S4
  density comparisons use full complex spinors. Low-rank compression gives
  a lower witness; the explicitly computed residual gives a conservative
  whole-kernel upper bound with measured-Gram factors. Bounds are arithmetic
  numerical estimates, not directed-rounding intervals. No global direct-H
  residual, whole-density symmetry PASS or full source-action equivalence
  is inferred. Different density and operator probe norms are not conflated.
- Independent Schur scalar-distance and per-component high-G tail sums confirm
  occupation and frame obstructions. No old projected prefix is renormalized.
- Exact integer source-buffer calculations check actual32³/54³/64³ descriptors,
 44/352bands and64/8q points. They are not a total runtime/RSS certificate.

The final offline verifier hashes protected MCT/DFT/stock inputs and resolves
new local links/allowed edit scope. It does not invoke Git or any other
project command inside protected DFT. The entire original SUCCESSOR_HANDOFF
content is retained beneath the new section. A passing verification admits
this **assessment**, not an SCF/physical-mass/job gate. All unknown material,
zero-T, finite-size, continuum and composition-transversality inputs stay OPEN.
