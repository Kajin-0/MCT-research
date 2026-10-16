# Decision: the large frozen chemical leakage survives time reversal

2026-10-16, from clean/pushed **4cfc16b**. Distinct retained-data physics phase:
**NO native QE/HSE/MPI, build, SCF, source edit or DFT write.** The new answer is
not already contained in the previous95.541meV total-leakage measurement.

**PROVEN UNDER THE REVIEWED FROZEN-KERNEL ASSUMPTIONS / CALCULATED:** the updated
chemical response's time-reversal-EVEN Q-action norm lies in
**[95.4618,95.5739]meV**; the ODD norm lies in **[0.2198,0.3320]meV**.
Thus the95.541080meV total leakage is not predominantly an explicit odd
artifact. Every even-part leakage singular value stays above91.5138meV.
Norms are not additive percentages: the odd upper is less than0.35% of the
original total operator norm, not a decomposition of its energy or variance.

| Matched chemical activation | Original trace (meV) | Even Q norm interval (meV) | Odd Q norm interval (meV) |
|---|---:|---:|---:|
| First source | +44.184097247 | [120.0794,120.1915] | [0,0.0562] |
| After one relaxation | +39.811503589 | [95.4618,95.5739] | [0.2198,0.3320] |
| Second minus first | −4.372593659 | [32.3223,32.5465] | [0.1639,0.3880] |

All intervals are **conditional finite-grid operator bounds**, not material
uncertainties or directed-rounding enclosures. Endpoints in this table are
rounded outward. Source assumptions and the deliberately loose64Ry centred
chemical-operator bound are proved in [the source certificate](source_norm_certificate.md).
The raw native multiplier packet was not archived, so no new kernel-byte
certificate is claimed. Complete precision, six singular intervals, both
members and their differences appear in [result.json](result.json) and
[response_table.csv](response_table.csv).

## The original trace is effectively even, not an exact-closure claim

For EXACTLY Theta-even W=P6/2−P8/4 and Hermitian C, tr(W C_odd)=0. The actual
original reference is not exactly Kramers closed: its measured residual is
1.28639923e-7, failing the inherited1e-8 gate. **Exact six-column reconstruction
is therefore REFUSED.** No frame is silently repaired or closure tolerance changed.

Hermiticity supplies the known cross block, leaving only Q(C−aI)Q acting on
that small residual. It produces linear action ambiguity but quadratic trace
ambiguity. With the source-conditioned bound the updated odd trace is confined
to approximately **[−8.95e-9,+1.109e-8]meV**. The+39.8115meV original-frame trace
therefore survives explicit odd-part subtraction to the stated precision,
subject to the source assumptions and small recorded arithmetic residuals.
It is not asserted exactly unchanged for the imperfect numerical frame.
Without ANY completion bound the six columns alone do not identify even/odd
parts; the actual residual gives a constructive information NO-GO.

## Full native-density defects, not just lower witnesses

| Source | ||D−Theta D Theta^-1||op | Frobenius norm |
|---|---:|---:|
| Host preliminary | 5.19022e-7 | 2.31125e-6 |
| Host relaxed | **0.001428207982** | **0.004040264356** |
| Cd preliminary | 5.99595e-7 | 2.29729e-6 |
| Cd relaxed | 4.05907e-7 | 1.03192e-6 |

These use an explicit352-dimensional union of each source and its Theta
image, with weighted span/Gram error allowances. Independent actual unit-vector
contractions agree. The earlier0.001395756895 host witness was correctly a
LOWER witness; it is unchanged. The tiny old preliminary-Cd compressed witness
was not a full TR certificate: its newly computed full defect is much larger.
All four sources still fail a strict1e-8 nonmagnetic-state qualification.

## Physical consequence and stopping boundary

The positive finite activation and remote-sector coupling cannot be dismissed
as the explicit Theta-odd part of this frozen response. They may still include
Theta-EVEN bias from a nonstationary or unstable trajectory. Theta-even is not
cubic Td, a restored Gamma8 quartet or a solved FD state. Nonlinear local XC,
same-D local-density consistency and an unknown stationary-response Jacobian
prevent promoting the projected response to a repaired HSE solution. The
[theory](theory.md) states the special frozen-operator exception and the precise
missing Hessian/Jacobian bounds; it does not falsely forbid that exception.

The next genuinely physics-changing input remains a **qualified matched
same-state full-H response on the six physical probes, with independent FD/
eigenstate residual and symmetry/stability control**. No new native residual-
direction job is justified merely to narrow the small parity interval. Such
actions would remove the mathematical six-column ambiguity, not supply the
missing stationary chemical response. Original16atom memory/output restrictions,
all source/owner/byte-replay failures and old acquisition PASS records remain.

**STOP this finite phase.** No empirical fit, physical signed gap/mass/x_c,
new SCF admission, topology, convergence or ground-state magnetism claim.
