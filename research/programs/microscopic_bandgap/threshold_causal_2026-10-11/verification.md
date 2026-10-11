# Independent verification and reproducibility

Date: 2026-10-11. Tests are synthetic mathematical checks. There is no new DFT,
MPI/HSE job, supercell, parameter sweep, empirical gap fit or material validation.

| Claim | Independent check |
|---|---|
| T3 fractional coefficient/sign | Subtract the threshold value, evaluate the beta integral, and continue the specified branch from the gap side; both edge orientations have the retarded absorption sign |
| T4 analytic cutoff tail | Independently expand only the ε>=Λ integral; compare the square-root closed form with the bounded tail |
| T5 finite cutoff formula | Direct 180-node Gauss–Legendre integration after ε=u², at gap-side and complex energies for both edge orientations |
| T7 uniform density remainder | Exact partial fractions; beta/log/integral bounds; independent transformed quadrature for p=1.5, 2 and 2.5 |
| T8 positive complement | Pointwise lower-envelope inequalities; independent positive-density Cauchy integral and negative imaginary part |
| T13 joint secants | Difference of two Cauchy denominators before taking an endpoint limit; dense Hermitian two-level bath solves and an exact half-power endpoint |
| T16 root accuracy | A common scalar coherent shift of both branches changes the common energy; solve its candidate mass root independently; error/bound tends to one with an unbounded raw derivative |
| T17 mass-sign bracket | Direct nonnegative-weight consequence of T13; requires a separately established common root/domain, with no numerical inference that signs alone establish it |
| Failure in a continuum | Positive bounded constant-density bath, analytic logarithm and independent complex quadrature; real derivative ratio is 9 |
| Failure without transversality | Exact cubic mass root shifted by ε; ε^(1/3) displacement violates any uniform linear bound |
| IR plus regular moments do not identify x_c | Exact moment null vector inherited from I5, shared continuum bath, positive finite discrete baths and independent bracketed sharp-crossing solves |
| Resonance changes power | Earlier exactly integrable normalized quadratic host at v=1/g0; T√δ tends to -2/(3π) |
| Reference and dimensions | Shift all energies jointly; scale energy units, weights and density coefficients with their proper powers |

All numerical tests operate on at most small dense matrices, scalar closed
functions and short quadratures. Bisections have fixed iteration bounds.
Sampling supplements proofs; it is not presented as a uniform-bound proof.

The first moment-null witness was evaluated at E*=0. It was strengthened before
final freezing by translating the remote bath to E*=t_IR=0.3 eV. This aligns
both regular C,A values exactly with T9's reference, so the counterexample
preserves the actual proposed closure inputs, rather than moments at an
unrelated energy. Neither witness uses measured material parameters.

## Frozen audit

The [record](../../../../data/calculated/r07_threshold_causal_audit_20261011.json)
pins the helper, test and audit-script SHA256 values, NumPy version and source
parent commit. It labels every value as a synthetic mathematical audit.

- At gap detuning 10^-12 eV the normalized toy host susceptibility is
  2.35619149×10^6, while the root error is 5.89048248×10^-7 and the joint
  bound is 5.89049498×10^-7. Their ratio is 0.999997878. This tests a limiting
  certificate, not a physical HgCdTe sensitivity or precision requirement.
- The positive continuum bath has mass/common secant ratio 9.00003000 at
  E=0.001 eV, disproving a causal-continuum extension of the gap bound.
- The common IR bath contributes -0.0164179962 eV at the toy crossing energy.
  Regular C=0, A=0.2, S=0.08 eV² and d=0.5 eV at the *same IR threshold*
  agree in both worlds. Their sharp crossing roots are 0.2264536862 and
  0.2269701579. The separation is an identifiability witness, not a claimed
  physical uncertainty or error against a measured composition.

## Reproduction

From the repository root:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest tests/test_r07_threshold_causal_closure.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python tools/check_r07_threshold_causal.py --output /tmp/r07_threshold_causal_reproduction.json
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest
```

The audit refuses to overwrite an existing output, including a previous /tmp
reproduction. Use a new filename for another deliberate reproduction. No
supervisor or queue file is touched by these commands.

Focused verification: **37 passed in 0.73 s**, including the 15 new tests and
the prior analytical/threshold/CPA tests. Repository-wide verification gives
**1802 passed in 137.27 s**. All 13 local package/decision links and both the
new and previous audit source-hash records pass. `git diff --check` is clean.
The preceding analytical package, frozen evidence, derivations, portfolio
state and shared foundations have no changes; the registry diff touches R07
only. The current research branch is retained for commit and push.

Global causality of the local linearized-complement model does not imply its
high-frequency normalization or centroid is exact: the g_T coefficient is
1/(1+A_R). The proof explicitly restricts accuracy to its certified window.
No previous exact centroid or full-resolvent sum rule has been weakened.
The root certificate relies on the true positive measures, not on promoting
the approximate local model into a globally exact static Hamiltonian.

**Unverified physical quantities:** the actual projected alloy measure, weighted
threshold amplitude, common support-free domain, mixed-response bound,
composition modulus, pole/peak identification and global topology. No physical
x_c or replacement for Hansen is claimed. These omissions are the established
material-information boundary, not numerical convergence failures to be
hidden by another fitted coefficient.
