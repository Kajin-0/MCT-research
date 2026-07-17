# CdTe complete Gamma double-group validation

## Status

The selected CdTe bands 31--38 now have a wavefunction-level, complete-double-group canonical-basis validation at the static Kane smoke geometry.

This is a method and basis result. It is not a converged physical CdTe parameter result.

## Central-sign problem

A spatial orthogonal matrix determines a spinor transformation only up to the central sign

```text
D(g_tilde)  or  -D(g_tilde).
```

Choosing a principal SU(2) lift independently for every spatial operation produced order-one residuals for several twofold operations because those independent signs did not define one global double-group multiplication table.

The corrected construction uses only the already matched generators:

- `C3[111]`: IrRep operation 41;
- `S4z`: IrRep operation 23;
- pure time reversal: IrRep operation 2.

Their target matrices generate the complete 48-element double group by multiplication. Each IrRep operation is mapped using both its Cartesian spatial matrix and its recorded spinor lift. This identifies which member of each central pair is used by the IrRep convention.

## Canonical intertwiners

For each energy block, solve

```text
D_calc(g) W = W D_Kane(g)
```

for `C3[111]` and `S4z`, then use pure time reversal to remove the remaining continuous phase.

The generator-pair intertwiner has nullity exactly one in every block. The next singular value is approximately one, so the canonical solution is well separated from any additional continuous gauge freedom.

The validated assignments are:

| Bands | Irrep |
|---|---|
| 31--32 | Gamma7 |
| 33--36 | Gamma8 |
| 37--38 | Gamma6 |

The exact intertwiners are recorded in:

```text
first_principles/a0/cdte_kane_double_group_reference_result.json
```

## Complete runtime result

Workflow run `29592084036` rebuilt the pinned CdTe SOC calculation, reran the IrRep 3.0.1 wavefunction probe, generated all double-group lifts, and checked every matrix.

| Quantity | Result |
|---|---:|
| Generated double-group elements | 48 |
| Unitary operations checked | 24 |
| Antiunitary operations checked | 24 |
| Maximum spatial mapping residual | 3.47e-15 |
| Maximum spinor-lift mapping residual | 2.76e-15 |
| Maximum canonical matrix residual | 6.20e-12 |

Per-irrep maximum unitary and antiunitary residuals are:

| Irrep | Unitary | Antiunitary |
|---|---:|---:|
| Gamma7 | 4.18e-15 | 4.44e-15 |
| Gamma8 | 5.32e-12 | 6.20e-12 |
| Gamma6 | 1.68e-12 | 1.50e-12 |

The declared fail-closed threshold is `1e-8`.

## Evidence

- merged implementation: PR #78;
- workflow run: `29592084036`;
- artifact ID: `8411752451`;
- artifact SHA-256: `673860fcb5a37966ddca601ec7977b012bdf0e2e5389fc6ef8e3a806538f01b2`;
- full runtime-result SHA-256: `bf246392ee62062b7c2bc1e127f14e64cf626bba583fc6988eae340d0436b555`;
- raw probe JSON SHA-256: `d2da969d345e0173a119ff0d5417c35e6e839e154cc12786b99c882e8d933e8c`.

The committed result omits the 48 per-operation records to avoid duplicating the full artifact, but retains the canonical intertwiners, hashes, maximum residuals, and claim boundary.

## Remaining freedom

Symmetry and time reversal do not fix one discrete sign for each inequivalent irrep. Those relative signs must be fixed by a declared finite-k Kane convention.

The next gate is therefore:

1. rotate the existing finite-k fixed-basis matrices with the committed intertwiners;
2. choose the relative signs so one declared `Gamma6 <-> Gamma8` linear-k element gives real positive `P8`;
3. apply the published Gamma7 phase convention and record the corresponding sign of `P7`;
4. perform the paired `+/-k` extraction at radii `h` and `h/2`;
5. train on `[001]` and `[111]`;
6. require the unused `[110]` matrix and covariance holdout to pass;
7. report both one-`P` and two-`P` closure residuals.

No phonon, electron-phonon, HgTe, alloy, or converged physical CdTe claim is authorized by this result.
