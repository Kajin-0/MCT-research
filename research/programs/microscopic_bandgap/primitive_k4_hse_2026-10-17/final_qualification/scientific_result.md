# Density-norm derivation and numerical reference boundaries

2026-10-17. **CALCULATED conventional SCF PASS / strict1e-8 symmetry FAIL.**
Read-only qualification of the completed sole case; no new native execution.
The [decision](../decision.md) gives all measured physics and resource values.
No novelty or new manuscript is claimed.

## Full finite-rank operator, not a compressed witness

In the actual NC plane-wave spinor basis, U contains all44saved columns and
F their native FD occupations. Θ=iσ_yK maps coefficients as
(c↑(G),c↓(G))→(c↓*(G),−c↑*(G)) at target−G−k−k_target. Target labels must
exist and the reciprocal difference be integral. Θ²=−I is checked exactly
on every available pair. Actual24XML crystal operations act on physical G,
with the axial SU(2) rotation det(R)R for improper R; fractional shifts vanish.

For V=ΘU(or a spatial transform), with occupation matrix F′:

    D−D′=Z J Z†, Z=[U sqrt(F),V sqrt(F′)], J=diag(I₄₄,−I₄₄).
    Z=QR => nonzero spectrum(D−D′)=nonzero spectrum(R J R†).

**PROVEN UNDER ASSUMPTIONS:** exact finite-basis linear algebra. All88QR
columns remain, including small/null directions; no44-state closure is
assumed. Norms refer to the whole5466-dimensional Γ basis, not the original
column-space compression. No small Γ integration weight is inserted into the
frozen per-fiber acceptance test.

**CALCULATED:** Γ op3.615172826e-7,F8.710744260e-7. The extremal physical
vector is independently applied to U F U†−V F V†: Rayleigh agreement6.2e-16,
eigenvector residual1.5e-15. A second algorithm orthogonalizes only U and
splits V=U₀O+R⊥; Frobenius² is the diagonal-block norm² plus twice the cross-
block norm² plus the residual Gram contraction. It gives8.710744262e-7.
Deterministic phase changes of all actual44spinors change the op norm by
2.4e-16. These are IEEE observations, not interval-arithmetic bounds.

The weighted cross block outside the44-state span has norm3.615172382e-7.
It explains why the4.05e-11 compressed witness misses the dominant defect.
The earlier2.17e-6 conservative upper remains valid but cannot certify1e-8.
No physical state is averaged or repaired by these diagnostics.

## Finite bands and the incomplete native Brillouin zone

All44coefficients/occupations enter D. Adding empty columns without changing
D cannot remove the measured occupied-kernel defect. Conditional on a complete
ordered finite-basis spectrum with every omitted eigenvalue≥E₄₄,

    ||D_tail||≤f(E₄₄), Tr D_tail≤(2 npw−44) f(E₄₄).

Computed highest levels lie≥5.305eV aboveμ; the conditional largest missing
trace bound is2.49e-166. The hypothesis is NOT certified by dexx or native
energy ordering alone: full-H/eigenpair/completeness residuals are missing.
Increasing bands could change ACE/SCF, which would be a new numerical experiment.

Only8irreducible wave packets were saved, not64. DirectΘ is possible on
nativeTRIMfibers1,3,7; the five generic−k partners are absent. Actual native
little-group counts in order are24,6,6,4,2,2,8,4. No fullTd is imposed at
generic k. No reconstructed stars, native64export or full-BZ symmetryPASS
is manufactured. A little-group test cannot replace the missing−k comparison.

## Physical Γ association and what its energies mean

The original f120 reference recorded Γ6 s weight.996596 andΓ8 Te-p,j=3/2
weight.903912, with reviewed double-group labels. Original frame/XML/UPF/
signed-gap pins are checked against the pre-existing audit. Integer G-labelled
transport embeds the e90probes into e50 with identical primitive cell,origin,
species and spin axes; no lost-tail renormalization or stationary-state transfer.
New frame weights and all24characters support the approximate sectors.
Character traces can be insensitive to amplitude errors at first order:
excellent traces do not override5.13e-7/1.75e-7sector span leakages.

The Γ6-like doublet is.289586505eV below the Γ8-like quartet. The within-
state difference is invariant under a scalar potential-zero shift. In cubic
inverted HgTe it is not a positive fundamental/absorption gap. Half-ordering
is a Kane convention under a justified effective model, not a disorder mass,
topological boundary or physical x_c. The tiny retained level range is not
an eigenpair, functional or material error interval.

Independent weighted occupations and saved rhoG give36e within1.39e-11e.
FD formula error is2.78e-14; an independent charge root shiftsμ by−1.21e-11eV.
Reconstructed entropy matches native−TS. The7.75neV quartet splitting yields
FD occupation spread1.4246e-7 atσ=.0136057eV; neither is rounded away.
Γ6 Θ-sewing singular values differ from1 by≤6.3e-14,Γ8 by≤1.2e-14,
yet amplitude off-span norms remain3.54e-7/1.48e-7. Probability deficits and
amplitudes are different tests; no unique native partner is imposed in a
degenerate quartet. Local/scalar density or small charge error alone cannot
certify the nonlocal occupied kernel.

## Reproduction and evidence

From MCT-research with existing DFT/.venv Python, bytecode disabled and
OPENBLAS_NUM_THREADS=1, run this directory's `analyze_final.py`, then
`verify_final.py`. They read native files and write only this new MCT result
directory. Raw HDF5 must remain accessible at the pinned paths; their hashes
in Git are not a public dataset. `capture_terminal.py` records the already-
completed read-only resource capture; it does not recreate historical manager
state. The original observer saved true exit0/invocation/peak before unload.

The first offline verifier completed scientific/protection checks but failed
JSON serialization of a NumPy int64 in the prospective folding-cost table.
It was corrected to Python int; native extents were independently checked
and the verifier then passed. No native rerun, new physical result or
threshold relaxation occurred. That code-only failure did not alter evidence.

No fresh full-H action, DIRECT-vs-ACE error or universal stationarity bound
exists here. This does not erase useful conventional convergence, nor permit
strict1e-8 symmetry or material claims. Old failures remain immutable. Stop
after the bounded terminal qualification; no new scientific job is authorized.
