# Relativistic hybrid host gate

**CALCULATED:** a real static-lattice HSE+SOC CdTe calculation now converges
in the companion DFT repository. Independent double-group symmetry and
orbital projections identify the signed Gamma6-Gamma8 gap as **1.7048135 eV**
on the declared coarse grid. Hybrid spinors expand to the full reciprocal
grid without changing any original eigenvalue. This establishes a working
host-Hamiltonian route after the bare-vertex falsification; it is not yet a
validated material prediction or a replacement gap equation.

## Actual calculation and assignment

Quantum ESPRESSO 7.5, six OpenMPI ranks, one thread per rank; CdTe lattice
6.48 A, wavefunction cutoff 90 Ry, charge/exchange cutoff 360 Ry, Gamma-centered
k4 grid and q2 exchange grid. HSE fraction 0.25 and screening 0.106 bohr^-1
remain fixed. The input has 36 valence electrons and 44 spinor bands, with
fixed occupations. The geometry follows the parent convention of
[Nicklas and Wilkins (2011)](https://link.aps.org/accepted/10.1103/PhysRevB.84.121308).
No empirical alloy-gap point enters this calculation.

The previous ultrasoft pseudopotentials fail an actual HSE+SOC dry run with
`Noncolinear hybrid XC for USPP not implemented`. Fully relativistic NC
PseudoDojo potentials pass. They include Cd 20 and Te 16 valence electrons.
The new potentials and input are pinned by hashes rather than filenames alone.

The first NC SCF stops cleanly after 941 seconds at the declared 900-second
exit request. Its inner PBE/hybrid loops do not qualify it as an accepted HSE
result. A copied-checkpoint continuation, with unchanged physical settings,
converges in another 198 seconds. The final exchange error is 2.8e-9 Ry,
below the unchanged 1e-8 Ry criterion; full EXX self-consistency and successful
terminal status are present. Runtime provenance records the base git commit
and hashes of the working driver, input, potentials and native outputs.

| Sector | Reviewed bands | QE double-group label | Dominant mean orbital weight |
|---|---:|---|---:|
| Gamma6 | 37-38 | G6 | total s: 0.992416 |
| Gamma8 | 33-36 | G8 | Te p, j=3/2: 0.946609 |
| Gamma7 | 31-32 | G7 | Te p, j=1/2: 0.936716 |

The resulting Gamma8-Gamma7 splitting is **0.9442885 eV**. The parser uses
full-precision complex atomic projections and averages traces across each
degenerate space. It checks the different Hartree and Ry conventions in
the SCF and projection XML against each other. Explicit band choices must
pass both the independent symmetry-label and orbital-character checks;
occupied versus empty band count alone is not used for a signed gap.

open_grid.x completes with 64 k points. All eight original irreducible
points occur in that expanded grid, and their complete eigenvalue arrays
are unchanged (maximum difference 0 eV). Expanded weights sum to one.
This avoids assuming that standard hybrid NSCF/bands is implemented.
Wannier interpolation and a common host/impurity gauge remain to be tested.

## Core approximation is a separate gate

The successful NC calculation emits QE's warning that nonlinear core
correction is inconsistent with hybrid exchange. Its pseudopotentials were
generated with PBE and include NLCC. Successful convergence does not establish
the accuracy of that core approximation. Cutoff, k/q-grid and many-body errors
are also unresolved. The displayed gap is a diagnostic, not a few-meV input.

**HYPOTHESIS:** a separately generated potential set may change the hybrid
binary result materially. A controlled comparison is running with the same
geometry, grids, cutoffs and hybrid parameters. It uses SG15 v1.2 inputs
regenerated fully relativistically by
[Meng Wu's ONCVPseudoPack](https://github.com/MarioAndWario/ONCVPseudoPack),
at pinned commit `83b20795f8f7f0cb1bc3d9c08c944cb60580232f`.
Actual UPF headers confirm NC, full relativity, SOC, PBE, no NLCC and the same
Cd/Hg/Te valence counts 20/20/16. Its CdTe dry run succeeds. It is not obtained
by deleting the core density from a PseudoDojo potential. Because the sets
differ in other generator choices too, a difference cannot be attributed to
NLCC alone. The running comparison is not yet an accepted scientific result.

## Why matching a crossing alone is insufficient

**CALCULATED source diagnostic, validation only:** the 2011 HSE paper lists
binary gaps -0.27 and +1.34 eV, whose straight chord crosses at x=0.167702.
The experimental binary numbers listed there, -0.29 and +1.60 eV, give
0.153439. The paper's alloy crossing near 0.17 comes from a cubic fit to
five calculated compositions; it does not supply endpoint-impurity data.
The closeness of its HSE chord to its fitted crossing cannot by itself
identify the alloy correction or establish the requested material accuracy.

**PROVEN within the reciprocal numerator closure:** for

\[
N=(1-x)E_H+xE_C+C x(1-x),\qquad N(x_c)=0,
\]

first-order input sensitivity is

\[
\delta x_c=-\frac{(1-x_c)\delta E_H+x_c\delta E_C+k_c\delta C}
 {E_C-E_H+C(1-2x_c)}.
\]

This is a conditional error-propagation identity, not a general estimate of
the full self-consistent DFT error. It demonstrates why independent binary
and impurity tests are required alongside a successful crossing prediction.

## Reproducibility and continuation

Completed DFT code and native records are committed as **12bde47** on
`research/hgcdte-analytical-gap-20261010`. The companion repository resides
at `/home/User/opencode_workspace/DFT`. Its
[gate protocol](/home/User/opencode_workspace/DFT/docs/r07_static_binary_gate.md)
contains the declared assumptions, stopping rule and reproduction commands.
Raw scratch and UPF files are excluded from git; separate fetch manifests
recreate both source-qualified potential sets. The original user-edited
HgCdTe output was preserved. No thermal or R02 gate was changed.

The [portable result record](../../../data/calculated/static_hse_binary_gate_20261010.json)
captures the completed signed-gap/projection result, grid checks, input
hashes and the pending comparison separately. DFT's QE-free suite has
**45 passed, 1 deselected**, including degenerate-space unitary invariance
and rejection of the Hartree/Ry mismatch. Real QE runs verify capability,
SCF convergence, symmetry, projection and spinor grid expansion.

Next: finish the no-NLCC comparison; classify its sectors; then select and
check binary references before computing the physical Cd-in-HgTe potential.
The reciprocal HgTe host remains necessary. The corrected full/residual T
conventions and threshold/observable checks from the prior results still apply.
No alloy-gap coefficient will be tuned to repair a failed prediction.

**NOVELTY CANDIDATE:** none established by this capability gate. HSE, atomic
projections, double-group classification and grid expansion are established.
The research objective remains unresolved and active; temperature is deferred.
