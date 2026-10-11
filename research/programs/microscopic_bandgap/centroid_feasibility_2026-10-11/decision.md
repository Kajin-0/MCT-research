# Finite decision: synthetic model NO-GO; physical input still missing

2026-10-11. **STOP.** The registered study is completed without changing any
scientific parameter or gate. The existing continuum family is a qualified
**synthetic causal benchmark**, not a qualified HgCdTe TB/CPA Hamiltonian.
One 135-row scan takes 2.31 seconds and 38,684 KiB maximum process RSS.
No material gap fitting, root search, new native calculation, acquisition or
supervisor action follows this decision.

## Registered gate outcome

| Gate | Result | Evidence |
|---|---|---|
| Positive normalized model; fixed projections; common endpoints/coherent control | PASS, synthetic only | Exact rational, parity and independent dense-resolvent tests |
| Numerical radius <=0.1 meV; independent moment discrepancy tolerances | PASS, all 135 rows | Maximum enclosed centroid radius 7.574e-26 eV; moment checks below 2.357e-11 in mass and 1.073e-11 eV in first moment |
| Every lower retained mass >=0.05 | PASS | Minimum m6 >=0.0694186; minimum m8 >=0.1247973 |
| All nine width/eta choices keep one >=1-meV sign for each (x,alternative) | FAIL, 5 of 15 groups | Positive alternative fails at x=0.20,0.25; negative alternative fails at x=0.30,0.35,0.40 |
| All alternatives share that stable sign at every registered x | FAIL, all five x | Endpoint/coherent-equivalent spectra yield opposite signs |

All individual row signs are resolved; the smallest enclosed distance from zero
exceeds **5.408 meV**. Thus the rejection is not caused by a numerically ambiguous
near-zero row. All reported error bounds are conditional on the documented
Decimal arithmetic contract, independently checked by fixed positive-kernel
quadrature. The extremely small rounding enclosure reflects inexpensive scalar
guard precision, not any claimed material accuracy.

The following centroid ranges span the **nine registered widths/resolutions**,
rounded outward to 0.01 meV. They are changes of model/observable, not error bars
on one observable. Signs refer to Omega=C6-C8 of synthetic projected measures.

| x | balanced range (meV) | positive range (meV) | negative range (meV) | Alternative-robust? |
|---|---:|---:|---:|---|
| 0.20 | [-66.26,-37.57] | [-65.80,214.82] | [-317.23,-40.03] | No |
| 0.25 | [-20.60,-11.47] | [-19.78,367.46] | [-392.13,-15.76] | No |
| 0.30 | [9.76,24.28] | [20.46,505.25] | [-484.56,22.78] | No |
| 0.35 | [16.68,65.73] | [45.52,618.54] | [-583.15,62.71] | No |
| 0.40 | [12.84,95.06] | [63.08,700.36] | [-673.09,87.87] | No |

At fixed width none of the 45 (x,alternative,W) groups changes sign across the
three eta values. Width changes flip signs in 6 of 15 (x,eta) groups for the
positive alternative and 9 of 15 for the negative alternative; balanced flips
none. The largest fixed-eta width span is 0.760943 eV; the largest fixed-width
eta span is 0.141066 eV. These effects dwarf arithmetic uncertainty.

The registered narrow half-width W=0.5 happens to preserve a common sign for all
three alternatives and eta values at each x. This **slice observation** is not
the preregistered all-width acceptance gate, an optimized replacement window,
or a bound on arbitrary material spectra. The fixed witnesses place their main
mixed weight outside that narrow window. Widths W=1.5 and 5 each permit opposing
alternative signs at every x/eta. Even W=5 is a tapered, finite-resolution
observable, not the full first moment of an unbroadened probability measure.
No window is promoted to a physical probe on the basis of this scan.

## Why precise centroids remain underdetermined

**PROVEN UNDER ASSUMPTIONS; elementary parity identity.** With the even window
and Cauchy kernel, m_atom(t)=m_atom(-t), n_atom(t)=-n_atom(-t), and n8=0.
Consequently the total m6 is independent of a and

```text
Omega_a = Omega_0 + a R,
R = h(1-b)[0.8 n_atom(1)-0.2 n_atom(4)]/m6.
```

The exact full centroids, endpoint projected spectra and first endpoint
spectral jets are identical for all three alternatives. Retained masses also
coincide. Their differing windowed odd moments alone produce the sign ambiguity.
For example at x=0.25, W=1.5 eV, eta=0.10 eV, Omega is approximately -16.195 meV
(balanced), +189.910 meV (positive), and -222.300 meV (negative), with separate certified
rounding enclosures in [the complete results](results.json).

The balanced sign can also be checked without numerics: its symmetric mixed
sector contributes zero n6; for t>0 and E>0,
P_eta(E-t)>P_eta(E+t), so the remaining atom's tapered n6 has the sign of e(x).
This validates the balanced scan and demonstrates how an imposed symmetry can
give stable model signs. The equality of endpoint/coherent controls does not
justify that symmetry in an actual alloy. No a value is fitted or preferred.

**FALSIFIED in this finite model:** agreement of endpoint projected spectra,
first endpoint jets, full coherent centroids and even retained masses suffices
to certify a width-and-alternative-independent continuum ordering. This is a
quantitative feasibility witness for the earlier N3 non-identifiability result,
not a new material theorem or a historical priority claim. Existing sharp-gap,
threshold, directional SOC, host-frame and TB rejection gates remain in force.

## One ranked missing physical input and stopping boundary

**Rank 1 — OPEN:** independently bounded interior Gamma6/Gamma8 spectral-window
contractions `(m6,n6,m8,n8)` for a **predetermined physical projector, state,
window and analytical eta**. Equivalently, for ordering alone, a certified sign
of `K=n6*m8-n8*m6` with positive mass floors suffices; K has units eV. This avoids
requiring full spectral tomography when a physical operator/observation adapter
can bound the contractions directly. In the present witnesses the indispensable
information is the unresolved odd window moment, not additional endpoint
precision or a more accurate integral.

Physical projector transport, composition statistics/assays, lattice/strain
path, carrier and many-body/zero-point convention, spectral coverage and
observation residuals must belong to that input's definition. No existing
accepted repository or Stage-0 archival object provides it. The synthetic
alternatives are not a probability distribution for material error or an
admissible uncertainty range established for HgCdTe. Only independent physical
restrictions on their unresolved spectral contractions could remove this
obstruction; a gap fit cannot do so.

**Decision ledger:** qualification and numerical feasibility PASS; registered
robust-ordering feasibility FAIL; physical identification NO-GO. Keep the
continuum-compatible centroid as a conditional observable with its mass/error
gates. Stop at this bounded evidence result. No additional scan, resolution
optimization, old-goal resumption or calculation queue is authorized by this
decision. A sharp physical Gamma6/Gamma8 inversion remains **OPEN**; no physical
x_c, operational material sign bracket, spectral-peak crossing, absorption edge
or bulk topology is claimed.
