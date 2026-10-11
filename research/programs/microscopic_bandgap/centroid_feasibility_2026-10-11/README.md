# Bounded R07 centroid model feasibility

2026-10-11. **CALCULATED: finite-grid model NO-GO / material input unqualified.**
The existing exact causal continuum family qualifies as a synthetic benchmark.
It passes numerical and window-mass gates, but its endpoint/coherent-equivalent
alternatives fail the registered width-and-alternative sign gate. No physical
Gamma gap, x_c, topology, material sign bracket or intrinsic linewidth is inferred.

- [Decision and finite ledger](decision.md): results, limiting interpretation,
  and one missing physical input; stop after this finite task.
- [Pre-registration](preregistration.md) and [configuration](registration.json):
  frozen in `5347d3c` before the first scan; 135 rows, no tuning or root search.
- [Model and numerical certificate](model_and_certification.md): fixed projectors,
  continuum measure, exact primitive integrals and outward arithmetic conditions.
- [All rows](rows.csv), [enclosures/provenance](results.json),
  [machine-readable gate summary](summary.json).
- [Runner](run_study.py), [independent tests](test_feasibility.py),
  [verification](verification.md).

Reproduce using the existing repository environment, from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 .venv/bin/python \
  research/programs/microscopic_bandgap/centroid_feasibility_2026-10-11/run_study.py \
  --output /tmp/r07-centroid-reproduction
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q \
  research/programs/microscopic_bandgap/centroid_feasibility_2026-10-11/test_feasibility.py
```

Choose a fresh output directory. The runner refuses to overwrite results, checks
five pinned prior sources, uses deterministic arithmetic/configuration, and
records code/configuration/pre-registration hashes. This command documents
reproducibility; the authorized study ran the grid once. No dependencies were
installed, numerical jobs queued, old blocked goal changed, or detached
supervisor inspected or altered. The archived TB vertex remains rejected as
a physical predictor. Previous derivations/evidence packages are untouched.
