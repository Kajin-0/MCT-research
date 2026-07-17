# CdTe complete Gamma double-group validation

## Status

The selected CdTe bands 31--38 have a wavefunction-level, complete-double-group canonical-basis validation at the static Kane smoke geometry.

This is a method and basis result. It is not a converged physical CdTe parameter result.

## Two distinct convention gates

### Global double-group signs

A spatial orthogonal matrix determines a spinor transformation only up to the central sign

```text
D(g_tilde)  or  -D(g_tilde).
```

Choosing a principal SU(2) lift independently for every spatial operation produced order-one residuals for several twofold operations because those signs did not define one global multiplication table.

The resolved construction uses only the matched generators:

- `C3[111]`: IrRep operation 41;
- `S4z`: IrRep operation 23;
- pure time reversal: IrRep operation 2.

Their matrices generate the complete 48-element double group. Each IrRep operation is mapped using both its Cartesian spatial matrix and recorded spinor lift, selecting one globally consistent member of every central pair.

### Exact Kane basis phases

A valid `Gamma6 + Gamma8 + Gamma7` representation is still insufficient for extracting conventional Kane parameters unless its internal phases match the Hamiltonian definition.

PR #80 aligned the target states explicitly with Novik et al. Eq. (4). It corrected:

- the sign of the second `Gamma7` basis vector;
- the relative time-reversal phase of the p-like sector.

These changes do not alter characters or irrep assignments. They are detected only by the stronger requirements

```text
D(g) H(k) D(g)^dagger = H(g k)
```

and exact agreement with the executable Kane time-reversal matrix.

## Canonical intertwiners

For each energy block, solve

```text
D_calc(g) W = W D_Kane(g)
```

for `C3[111]` and `S4z`, then use pure time reversal to remove the remaining continuous phase.

The generator-pair intertwiner has nullity exactly one in every block. The next singular value is approximately one, so the solution is well separated from additional continuous gauge freedom.

| Bands | Irrep |
|---|---|
| 31--32 | Gamma7 |
| 33--36 | Gamma8 |
| 37--38 | Gamma6 |

The corrected Novik-convention intertwiners are recorded in:

```text
first_principles/a0/cdte_kane_double_group_reference_result.json
```

## Corrected runtime result

Workflow run `29594001046` rebuilt the pinned CdTe SOC calculation, reran the IrRep 3.0.1 wavefunction probe, generated all double-group lifts, and checked every matrix in the exact Novik basis.

| Quantity | Result |
|---|---:|
| Generated double-group elements | 48 |
| Unitary operations checked | 24 |
| Antiunitary operations checked | 24 |
| Maximum spatial mapping residual | 3.47e-15 |
| Maximum spinor-lift mapping residual | 2.76e-15 |
| Maximum canonical matrix residual | 6.20e-12 |

| Irrep | Maximum unitary residual | Maximum antiunitary residual |
|---|---:|---:|
| Gamma7 | 6.48e-15 | 6.69e-15 |
| Gamma8 | 5.33e-12 | 6.20e-12 |
| Gamma6 | 1.70e-12 | 1.52e-12 |

The declared fail-closed threshold is `1e-8`.

## Evidence

- central-sign implementation: PR #78;
- exact Novik phase correction: PR #80;
- corrected workflow run: `29594001046`;
- artifact ID: `8412517215`;
- artifact SHA-256: `92b4a8cf56f0fa9983ccfea2a7b10c58920eb116895896e0dd767a45d49e4e08`;
- full runtime-result SHA-256: `13fb8be6833d102a615c7af9d71485a8c205e63838315ce109832e265dfdadf7`;
- raw probe JSON SHA-256: `ec8d0e0da40fcfe44fa0b629040be55dba8dcc803e090413564825128be663f0`;
- QE schema SHA-256: `27ddf2a2c8e236a392047ecf32460a4ccb82886c12491b5f579b3fabe72c26d1`.

The committed result omits the 48 per-operation records to avoid duplicating the full artifact, but retains the physical intertwiners, hashes, maximum residuals, and claim boundary.

## Remaining freedom and next gate

Symmetry and time reversal leave one discrete sign for each inequivalent irrep. The finite-k gate must:

1. reconstruct the fixed-reference Hamiltonian from the Gamma-star overlaps and exact QE eigenvalues;
2. rotate it with the corrected Novik-convention intertwiners;
3. fix the relative signs by requiring the declared `P8` and `P7` matrix elements to be real and positive;
4. perform paired `+/-k` extraction at `h` and `h/2`;
5. train on `[001]` and `[111]`;
6. require the unused `[110]` matrix and covariance holdout to pass;
7. compare one-`P` and two-`P` closure.

No phonon, electron-phonon, HgTe, alloy, or converged physical CdTe claim is authorized by this result.
