# First-principles execution assets

This directory contains provisional, parameterized assets for the staged

$$
\mathrm{CdTe}\rightarrow\mathrm{HgTe}\rightarrow\mathrm{Hg}_{1-x}\mathrm{Cd}_x\mathrm{Te}
$$

campaign. They are research templates, not validated production inputs.

## Scientific rules

1. Use fully relativistic pseudopotentials and explicit SOC for the electronic states.
2. Converge static electronic structure, phonons, dielectric response, and Born charges before electron–phonon work.
3. Compare nonadiabatic and adiabatic Fan calculations, but use the nonadiabatic result as the primary polar-material result.
4. Keep Fan and Debye–Waller terms separate and report their sum.
5. Do not use EPW's diagonal electron self-energy output as a substitute for a full matrix-valued AHC result.
6. Do not convert a diagonal self-energy table into `MatrixDataset`; the export must contain an explicit complex $8\times8$ matrix.
7. Record pseudopotential hashes, input hashes, code versions, meshes, broadening, band windows, and convergence deltas.

## Directory contents

- `templates/qe/` — Quantum ESPRESSO ground-state, DFPT, and EPW templates.
- `templates/abinit/` — ABINIT EPH/AHC driver fragment to attach to a validated GS/DFPT workflow.
- `pseudopotential_matrix.csv` — candidate-pseudopotential comparison ledger.
- `convergence_ledger.csv` — run-level convergence and uncertainty ledger.
- `matrix_export_mapping.example.json` — example explicit NetCDF variable mapping.
- `provenance.example.json` — minimum provenance record for dataset conversion.

## Temperature protocol

The target temperatures are

$$
T=0,\ 77,\ 150,\ 225,\ 300\ \mathrm{K}.
$$

ABINIT's `tmesh` defines a linear grid by initial temperature, step, and number
of points. Because the target list is not uniformly spaced, use one EPH run per
temperature with

```text
tmesh @TEMPERATURE_K@ 1 1
```

rather than changing the requested 77 K point or interpolating it without a
separate error analysis.

EPW accepts an explicit `temps` list, so the complete list can be supplied in
one input when the selected task supports it.

## Conversion workflow

A code-specific extraction step must export full matrices either as JSONL or as
NetCDF variables with an explicit mapping. Convert the result with

```bash
python tools/convert_matrix_export.py raw.jsonl matrices.npz \
  --format jsonl \
  --composition 1.0 \
  --temperature-k 77 \
  --volume-a3 100.0 \
  --matrix-kind self_energy_total \
  --provenance-json provenance.json \
  --sha256-output matrices.npz.sha256
```

For NetCDF, add

```bash
--mapping-json first_principles/matrix_export_mapping.example.json
```

The converter intentionally refuses to guess variable names or reconstruct
off-diagonal information from eigenvalue-only output.

## Primary documentation anchors

- ABINIT electron–phonon variables: <https://docs.abinit.org/variables/eph/>
- ABINIT zero-point-renormalization tutorial: <https://docs.abinit.org/tutorial/eph4zpr/>
- Quantum ESPRESSO `pw.x`: <https://www.quantum-espresso.org/Doc/INPUT_PW.html>
- Quantum ESPRESSO `ph.x`: <https://www.quantum-espresso.org/Doc/INPUT_PH.html>
- EPW inputs: <https://docs.epw-code.org/Inputs/Inputs.html>

Every template must be rechecked against the exact installed code release before execution.
