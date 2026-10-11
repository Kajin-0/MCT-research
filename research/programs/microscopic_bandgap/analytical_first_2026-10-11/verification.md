# Independent verification and limits

Date 2026-10-11. Everything in this report is a mathematical or synthetic-model
check. No DFT/native MPI calculation, empirical alloy fit, physical parameter
estimate or material validation is performed by this tranche.

## Analytic checks independent of the numerical helpers

| Claim | Independent verification |
|---|---|
| Two scalar Γ sectors | Apply group covariance to the compressed averaged resolvent; use the inequivalent irrep commutant; inspect the multiplicity exception |
| Positive Feshbach measures | Represent the ensemble by a self-adjoint multiplication operator; insert its Q spectral projections; compare against direct block elimination |
| Hidden endpoint data | Expand the balanced-event probability using exact integers/Fractions; independently enumerate configurations and their resolvents; inspect zero perturbation in either single-impurity host |
| Directional Γ8 correction | Contract the already proved angular projector norms; independently average all sixteen dense Hermitian resolvents and second moments |
| Same moments, different function/root | Exact rational null vector of the three-moment map; independent positive finite-bath realization and bracketed root solve |
| Spectral linearization bound | Exact partial fractions; triangle bound using support distance; compare with full Hermitian matrix inversion and energy intervals |
| Common/mass root certificate | Mean-value bound applied twice; independently solve a linear common/mass problem that saturates the stated bound |
| Weak-covariance error | Uniform Neumann-series tail plus a separate Born Dyson tail; independently invert a ±W ensemble |
| Spectral support | Two-sided finite-patch/Weyl argument; countable periodic approximants and Borel–Cantelli, rather than a finite-supercell spectrum used as proof |
| Atomic CPA limit | Substitute the exact binary mixture resolvent into both site T equations; account for floating cancellation |

All energy dimensions, pure endpoints, global energy shifts, retarded causality,
threshold/support failure guards and required symmetry hypotheses are explicitly
checked. Conditional bounds deliberately reject zero spectral separation,
nonpositive root-slope bounds, or w/d0≥1. No positivity theorem is transferred
to -Re T' inside a continuum. No global normalized Bloch-cloud overlap is used
to infer physical state rotation.

## Frozen small-model audit

The [audit](../../../../data/calculated/r07_analytical_first_audit.json) pins the
bound-module and audit-script SHA256 values, its parent commit and NumPy version.
It contains synthetic parameters identified as such, with no physical prediction.

At synthetic x=0.23 the coherent directional operator average is below
1.3e-17 eV in norm, but the Γ8 scattering response is nonzero. Halving λ reduces
the error of the second-order formula by factors **16.0281 and 16.0070**,
consistent with the next even fourth-order correction in this off-diagonal
atomic example. The general two-invariant trace agrees with independent matrix
contraction to **7.76e-18 eV**. These residuals verify algebra, not material
accuracy.

Two positive four-pole measures have identical C=0, A=0.2 and total weight
0.08 eV². Their synthetic real mass roots are **0.2322513975** and
**0.2323647721**. This is a non-uniqueness witness, not a HgCdTe prediction or
a test against the experimental inversion. The value bound over the declared
±0.2-eV interval is 0.026667 eV; sampled errors are below 0.008810 eV. An
interval sampling check supplements the analytic bound; it is not itself a
uniform-error proof.

## Reproduction

From the MCT repository root:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest tests/test_r07_analytical_first.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python tools/check_r07_analytical_first.py --output data/calculated/r07_analytical_first_reproduction.json
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest
```

The audit refuses to overwrite an existing output. The separate reproduction
filename avoids changing frozen evidence. Tests use only small matrices and
exact combinatorial identities; no new native work is invoked. The repository
test result and final scope checks are recorded below.

**CALCULATED:** the eleven new independent tests pass; the full MCT suite gives
**1787 passed in 152.04 s**. A first CPA residual assertion used an absolute
2e-15 tolerance despite subtracting larger nearly cancelling terms. Its
4.44e-15 roundoff residual was resolved by a machine-epsilon tolerance scaled
to those terms; no equation or physical acceptance gate was changed.
All package links and frozen audit source hashes pass, and `git diff --check`
is clean. The final change scope contains no DFT files, other program states,
portfolio-state changes or native work queues.

## Scope of validation

The package does not validate the physical Hamiltonian, actual material
threshold amplitudes, support distance, dilute limit, linewidth, global
topology, or a few-meV HgCdTe gap. Those remain the precise missing conditions.
No detached DFT process, supervisor, input, queue or numerical output is edited.
All other program state files and the portfolio state remain unchanged.
