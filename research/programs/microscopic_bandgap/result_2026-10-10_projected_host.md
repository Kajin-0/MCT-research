# Two hybrid host calculations and a failed finite-q matrix gate

**CALCULATED:** the source-qualified no-NLCC SG15 CdTe HSE+SOC calculation
converged, with independently assigned signed Gamma6-Gamma8 gap
**1.5753656 eV**. The previous PseudoDojo calculation gives **1.7048135 eV**
with identical physical settings. Their **129.4479-meV** difference is a
potential-set sensitivity, not a fitted correction or an isolated NLCC effect.
Neither supplies a validated few-meV binary reference yet.

**CALCULATED:** both calculations yield full-rank projected 26-spinor
matrices across the complete 64-point grid. However, both fail an independent
matrix time-reversal check. Native wavefunction inspection traces the tested
failure to the retained empty-state space at X, before grid expansion. A
controlled calculation with tighter empty-state diagonalization is running.
The physical impurity T-matrix remains unresolved; these matrices are not
accepted as scattering hosts.

## Completed binary comparison

Both calculations use QE 7.5, six MPI ranks, HSE fraction 0.25, screening
0.106 bohr^-1, CdTe lattice 6.48 Angstrom, k4/q2 grids, wavefunction cutoff
90 Ry and density/exchange cutoff 360 Ry, 36 electrons and 44 spinor bands.
The potential files and all inputs have pinned checksums. No experimental
alloy-gap data or coefficient enters either SCF.

The SG15 run stopped cleanly at its runtime limit, with exchange error
5e-8 Ry, and was continued from a copied checkpoint with unchanged physical
settings. The continuation converged in 178 seconds with exchange error
1.1e-9 Ry, below the unchanged 1e-8 criterion. Its reviewed G6, G8 and G7
sectors have bands 37–38, 33–36 and 31–32 respectively. Symmetry labels and
dominant orbital traces agree. The Gamma8-Gamma7 splitting is 0.9565300 eV.
Its full-grid expansion preserves all eight original eigenvalue arrays.

The SG15 potentials were generated without NLCC, unlike the previous set,
but their other generator choices also differ. The comparison therefore
cannot attribute the entire gap difference to core correction. Both use
PBE-generated relativistic norm-conserving potentials with HSE; cutoff,
exchange-grid and electronic-structure accuracy still require validation.

## Rank is necessary but insufficient

The declared trial functions are cation s,p,d plus Te s,p, with both spin
components, fixed Cartesian axes and identical hydrogenic radial choices.
They span the 26 retained bands 19–44 after exclusion of 18 deep semicore
spinors. No spread minimization or independent Wannier gauge optimization
is performed.

For A_mn=<psi_m|g_n>, the full-rank polar frame Q=A(A* A)^(-1/2) gives
H_g=Q* H_band Q. **PROVEN:** a consistent unitary change of Bloch-state
gauge leaves this trial-frame Hamiltonian invariant. This does not establish
that separately projected host and impurity orbitals share a physical basis.

| Diagnostic | PseudoDojo | SG15 |
|---|---:|---:|
| Smallest projection singular value | 0.114182 | 0.0124843 |
| Worst projection condition number | 9.07791 | 82.4386 |
| Maximum time-reversal matrix defect | 0.0782256 eV | 6.37827 eV |
| Smallest native X time-reversal span overlap | 0.9998679 | 0.0946768 |
| Native X occupied-span overlap deficit | <2e-14 | <1.5e-11 |

The matrix test compares H(-k) with J H(k)* J*, including reciprocal
folding. The real trial orbitals have adjacent up/down spin pairs, with
J=I_13 tensor i sigma_y. Both matrices fail the declared 1-meV diagnostic
tolerance. The eigenvalue-preservation error of a square polar transform
is below 5e-14 eV; that algebraic identity cannot certify its physical frame.

**PROVEN:** equality of paired eigenvalues alone does not establish
time-reversal covariance of a matrix or invariance of a retained physical
subspace. A numerical test explicitly supplies equal energy spectra but
inconsistent time-reversal eigenvectors.

## Native wavefunctions identify the tested failure

For the orthonormal native spinor columns C, the singular values of
C* Theta C measure the overlap between the retained span and its time
reverse. A complete invariant subspace has all singular values equal to one.
The reader maps plane waves at a reciprocal boundary by G -> -G-2k,
and checks the norm-conserving Euclidean Gram matrix. Observed Gram errors
are below 4e-15 for both hosts.

At X the SG15 retained space has a time-reversal principal-angle sine
of 0.995508, even though its occupied space is invariant within numerical
tolerance. The largest paired eigenvalue splitting among the retained empty
states is 32.176 meV. The original and expanded X coefficients agree to
1.6e-16: the tested defect already occurs in the native SCF states. This
does not implicate physical time-reversal breaking in nonmagnetic CdTe.

**HYPOTHESIS:** the default loose empty-state diagonalization is inadequate
for this higher-band representation. A retained window that cuts an
unresolved multiplet is another possibility. The controlled next run sets
`diago_full_acc=true`, which converges empty states at the occupied-state
accuracy, with all physical settings fixed. The interpretation follows
the [official QE input reference](https://www.quantum-espresso.org/Doc/INPUT_PW.html).
No symmetrization or altered gap coefficient conceals the defect.

## Reproducibility and current action

The completed code, native SCF evidence, projected-frame inputs, checksums
and wavefunction audits are saved in DFT commit **a0c91cc** on
`research/hgcdte-analytical-gap-20261010`. Its
[projection protocol](/home/User/opencode_workspace/DFT/docs/r07_projected_host_frame.md)
documents the assumptions and commands. The source HDF5 layout is checked
against [QE 7.5 io_base](https://github.com/QEF/q-e/blob/qe-7.5/Modules/io_base.f90).
The common-basis extraction requirement is established in
[Berlijn, Volja and Ku (2011)](https://link.aps.org/accepted/10.1103/PhysRevLett.106.077005).

The portable [hybrid result record](../../../data/calculated/static_hse_binary_gate_20261010.json)
now separates the two completed gaps, the failed matrix gates and the live
numerical control. QE-free tests give **52 passed, 1 deselected**. New tests
cover Bloch-gauge invariance, rank loss, reciprocal-boundary spinor mapping
and a symmetry defect invisible to an energy list. Original user edits
and the R02 thermal/first-principles gates are unchanged.

The six-rank bounded control started as
`calculations/r07/cdte_hse_sg15_k4_q2_e90_fullacc`, launched from commit
a0c91cc. It stopped cleanly after 922 seconds at its runtime limit without
full EXX convergence. On October 11 the unchanged copied continuation
`cdte_hse_sg15_k4_q2_e90_fullacc_restart_4b7c5f97` resumed; it retains
`diago_full_acc=true`. It is not an accepted result until full EXX convergence
and terminal status are checked. Repeat the projection and native-wavefunction audits
after convergence. If the defect persists, inspect the retained band window
and spinor solver before computing a physical impurity potential. HgTe and
the actual Cd-in-HgTe impurity are still required.

**NOVELTY CANDIDATE:** none established by this numerical host audit. The
research contribution is a reproducible failed gate and a concrete control,
not a replacement for Hansen. Temperature remains deferred.
