# Focused native and independent validation

**Native pair:** one host and one sequential Cd first-ACE execution, no retry.
Both all-rank owner/resource/science gates passed. Actual logs, XML, typed leases,
manager status, native packet/wave hashes and telemetry are archived or retained
privately. No synthetic fixture is substituted for either native member.

Native pw.out archives retain their exact trailing whitespace. The default Git
whitespace check flags those original output lines; invocation-only
`-c core.whitespace=-blank-at-eol` passes without changing raw data or repository
configuration.

**Before services:** actual absolute host/Cd paths had 103/101 bytes (104/102
with NUL), bound at the fresh locations, and were closed and inode-checked before
removal. The fresh p2 root did not exist initially. No prior attempt state or
units existed. Reference/input equivalence was checked against old prepared
physics, permitting only private path changes. Reviewed owner patch applied with
zero fuzz. Native ELF/observer/source/arithmetic and PP pins remained identical.

**Source/readback:** byte-exact native source waves and activation rhoR/rhoG;
complete physical G coverage; fixed six-vector probe embedding; both ranks and
60³ FFT/extents; 176 bands, 144 electrons, actual Γ/q1/HSE/cutoffs, 24 symmetries,
preliminary 1e-9 SCF gates and explicit false HSE convergence passed. Original
source/ELF/readback tolerances were not changed after observation.

**Three independent read-only checks passed:**

1. FD neutrality from decimal XML strings at 70-digit precision, independent of
   the NumPy/SciPy native intake: −9.55e-12/+4.265e-11 electrons.
2. Per-column complex vdot contractions reproduce reference action matrices
   within 7.22e-16 Ry and native unhalved Fock energy within 2.85e-14 Ry.
3. Within-irrep unitary rotations preserve the projected ordering trace within
   3.47e-18 Ry, independently of its original basis coordinates.

The first offline check import failed because mpmath was unavailable. The failure
is recorded; the standard-library Decimal replacement then passed. No package
installation, native rerun, acceptance change, or frozen source alteration.

To reproduce only these read-only checks:

```bash
cd /home/User/opencode_workspace/DFT
source scripts/env.sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python /home/User/repos/MCT-research/research/programs/microscopic_bandgap/chemical_hse_firstace_p2_2026-10-14/independent_checks.py
```

Final checks passed all raw/archive and frozen-pin hashes, protected snapshot
identity, JSON/Python syntax and operator decomposition. Both own cgroups are
absent, lock free, old ledger exact; known native process names are empty. No
host-wide absence claim. Final member/prepared accounting remains below 14 GiB;
observed resource floors are far above the original limits. Stock/dirty DFT,
old failed acquisition and all protected prior evidence remain unchanged.

Do not rerun prepare/preflight/launch or old address helper main functions.
These accepted native states are retained evidence, not a qualified restart or
future relaxation authorization. Full HSE convergence, material uncertainty,
physical x_c and whole-SCF memory gain remain unestablished.
