# P1 — existing physical-input qualification

**CALCULATED, 2026-10-11:** one read-only native audit in 0.83 seconds and
94,452 KiB RSS independently reproduces the completed f360/f120 Gamma kernel
norm **4.205828324256838 micro-eV**. Its six source eigenspinors have NC Gram
defect **1.656e-15**. The native target-sector overlap singular values match
the pinned prior report within 3e-15; all supplied target-state weights and
eigenvalues are now saved in [existing_audit.json](existing_audit.json).
No band prefix is renormalized. These are physical NC frame comparisons for
specified numerical reference operators, not a material error certificate.

| Existing object | Admission | Missing qualification / useful role |
|---|---|---|
| HgTe SG15 HSE+SOC k4/q4, 90-Ry wavefunctions, f360 and f120 | Accepted native numerical SCF references; native Td Gamma6/8 assignments | Model/core/GW/zero-point, residual/grid and physical impurity errors remain unknown |
| Their native Gamma eigenvectors and common-frame cross-overlaps | Fixed physical-projector numerical comparison passes; source Gram near identity | Gamma comparison does not bound finite-q exchange or alloy response |
| CdTe accurate-empty same-operator/folding controls | Valid extraction/embedding negative controls | Previously failed projected 1-meV and coarse-grid/material gates are unchanged |
| Existing x=.20 SOC SQS table | Existing PBE band-count edge 6.4 meV; not admitted as Gamma6/8 input | No retained Gamma measures, physical projector tracking or HSE/material budget; documented 27-meV smearing and finite SQS confounders |
| Matched n2/k2/q2 f120 16-atom Hg host/Cd substitution | Prepared inputs, successful native dry runs only | Both accepted SCF flags false; no self-consistent impurity spectrum/operator or dilute response |
| Archived reconstructed TB/CPA spectra | Reproducible diagnostic only | Physical predictor rejection retained; not a source of missing material contractions |
| Stage-0 magneto-optical raw/metrology/assay package | Unavailable at prior audited gate | No newly accessed empirical dataset or probe adapter |

The SQS file contains separate empirical benchmarks; the audit **does not copy
or use them**. An `ok` PBE parser status and an electron-count gap cannot stand
in for a signed projected Gamma ordering. Native `accepted_scf` is likewise an
execution/convergence gate, not exact material Hamiltonian acceptance.

Twenty-nine source hashes are saved, including 21 completed-reference sources
from the frozen review. The two historical supervisor state paths are skipped
even for hashing; no process/supervisor is inspected. Six prepared-input/SQS
sources, the native overlap module and the MCT review complete the 29 pins.
The DFT repository is read-only;
bytecode is disabled, and no DFT driver, environment setup script or native job
is invoked. A fresh MCT-only audit result is produced using the existing DFT
Python environment for its already installed h5py.

**Decision:** advance cheaply to P2. There is enough independently transported
reference spectral information to test a finite-window certificate, beyond a
single inverse-kernel point. There is **no** new accepted impurity or interior
alloy input. The present audit cannot supply a physical x_c, lower composition
modulus, or one-substitution amplitude. Investigate the numerical reference
window first, then reduce the indispensable acquisition without further native
calculation or repeated inventories.
