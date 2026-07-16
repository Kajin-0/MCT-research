# Krishnamurthy 1995 Table I channel decomposition

## Scope

This note reproduces the spin-averaged 300 K Hg0.78Cd0.22Te band-edge contributions printed in Krishnamurthy et al. Table I and closes them against Table II.

The source is historical HPTB plus valence-force-field theory. It is not experimental validation.

## Table definitions

Table I resolves the calculated electron-phonon changes in the valence edge `Ev` and conduction edge `Ec` by:

- intermediate electronic bands 1-8;
- TA, LA, LO, and TO phonon branches.

Bands 1-4 are valence bands and bands 5-8 are conduction bands. Spin is included in the calculation, but the table is spin averaged. Polar coupling is included in the LO contribution.

The gap contribution is defined consistently as

```text
Delta Eg = Delta Ec - Delta Ev.
```

## Reproduced 300 K edge and gap shifts

Summing the eight printed band contributions gives:

| Quantity | Shift |
|---|---:|
| `Delta Ev` | -207.02 meV |
| `Delta Ec` | -80.46 meV |
| `Delta Eg` | +126.56 meV |

Thus both edges move downward, but the valence edge moves farther, increasing the gap.

The four phonon-mode rows reproduce the total to printed rounding:

| Closure residual | Value |
|---|---:|
| mode sum minus total, `Ev` | -0.01 meV |
| mode sum minus total, `Ec` | +0.02 meV |
| mode sum minus total, `Eg` | +0.03 meV |

## Acoustic-phonon statement

The branch sums are:

| Branch | `Delta Ev` | `Delta Ec` | `Delta Eg` |
|---|---:|---:|---:|
| TA | -140.87 | -17.50 | +123.37 meV |
| LA | -30.79 | -22.93 | +7.86 meV |
| LO | -23.92 | -12.77 | +11.15 meV |
| TO | -11.45 | -27.24 | -15.79 meV |

Using the combined magnitude of both edge shifts,

```text
(|Delta Ev_ac| + |Delta Ec_ac|)
-------------------------------- = 0.73776.
(|Delta Ev|    + |Delta Ec|)
```

This numerically reproduces the paper's statement that acoustic phonons account for about 75% of the band-edge motion.

The same percentage should not be applied independently to each edge:

- acoustic share of `|Delta Ev|`: 82.92%;
- acoustic share of `|Delta Ec|`: 50.25%.

For the gap difference, acoustic branches contribute +131.23 meV, or 103.69% of the net +126.56 meV. Optical branches oppose them by -4.64 meV. TA alone supplies 97.48% of the net gap increase.

The 300 K gap result is therefore acoustic dominated, but it is a signed cancellation rather than an unsigned sum of branch strengths.

## Intermediate-band cancellation

Grouping the intermediate states gives:

| Intermediate states | `Delta Ev` | `Delta Ec` | `Delta Eg` |
|---|---:|---:|---:|
| valence bands 1-4 | +165.25 | +55.22 | -110.03 meV |
| conduction bands 5-8 | -372.27 | -135.68 | +236.59 meV |

The conduction-band-mediated gap increase is 186.94% of the final net shift. Valence-band intermediates cancel 86.94% of that net result.

A useful cancellation diagnostic is

```text
(|Delta Eg_VB| + |Delta Eg_CB|) / |Delta Eg_net| = 2.7388.
```

The final gap shift is therefore substantially smaller than the gross signed channel motion.

## Table I to Table II closure

Table II gives:

- `Eg(1 K) = 113.60 meV`;
- zero-point correction `= 13.6 meV`;
- `Eg(300 K) = 218.66 meV`.

The unrenormalized reference gap inferred from the printed low-temperature values is

```text
Eg,ref = 113.60 - 13.6 = 100.00 meV.
```

Adding the Table I 300 K electron-phonon shift gives the fixed-lattice reconstruction

```text
Eg,ref + Delta Eg_ep(300 K)
= 100.00 + 126.56
= 226.56 meV.
```

The difference from Table II is

```text
218.66 - 226.56 = -7.90 meV.
```

Equivalently, between 1 and 300 K:

```text
thermal electron-phonon shift = 126.56 - 13.6 = 112.96 meV
non-electron-phonon remainder = -7.90 meV
total shift                  = 105.06 meV.
```

This exactly reproduces `218.66 - 113.60 = 105.06 meV` at printed precision.

Under the paper's method, the -7.90 meV remainder is consistent with the separately described lattice-dilation contribution. It is an inferred decomposition; the paper does not print -7.90 meV as a standalone value.

The worst-case bound from printed decimal rounding is approximately 0.14 meV, far below the inferred remainder. This addresses transcription rounding, not historical model error.

## Scientific decision

The historical 300 K gap increase is:

- acoustic dominated;
- driven primarily by conduction-band intermediate states;
- strongly cancellation sensitive;
- partially opposed by optical branches and lattice dilation.

This supports a signed-channel microscopic picture. It does not identify a new oscillator family, because Table I contains only one temperature and no branch-resolved temperature dependence.

In particular, Table I cannot determine which branch competition produces the approximately 1 meV low-temperature turnover in Table II. That feature remains below the paper's 10-15 meV model/comparison floor.

## Limits and falsification

The result is limited by rounded historical calculated values with no covariance. It does not establish experimental phonon-channel weights or modern Fan/Debye-Waller separation.

The interpretation should be revised if:

1. a primary-source recheck changes any Table I value or row definition;
2. unrounded outputs fail branch-to-total closure;
3. source documentation shows Table II excludes dilation, in which case the -7.90 meV term must remain unlabeled;
4. temperature-resolved branch calculations show that the 300 K acoustic dominance does not persist over the range of interest.

## Reproduction

```bash
python tools/analyze_krishnamurthy1995_table1.py
```
