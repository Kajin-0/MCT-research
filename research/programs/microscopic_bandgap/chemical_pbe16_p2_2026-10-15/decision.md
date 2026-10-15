# PBE16 x=0.125 physics decision — 2026-10-15

**CALCULATED: one real matched Hg8Te8/CdHg7Te8 PBE+SOC pair converged.**
No HSE run, old trajectory restart, empirical fit or physical xc claim.

| Quantity | Host | Cd | Cd minus host |
|---|---:|---:|---:|
| Dominant tracked Td Gamma6–Gamma8 multiplet separation, eV | -1.044386488 | -0.875353203 | **+0.169033285** |
| Fixed original-frame Gaussian W2 ordering, eV | -1.044391269 | -0.842933008 | **+0.201458261** |
| Fixed original-frame inverse-resolvent ordering, eta=.05eV | -1.044467700 | -0.909331232 | **+0.135136468** |

The first row is a well-resolved, frame-selected **periodic ordered-cell PBE
eigenvalue separation**: actual native Td multiplicities and Kramers pairs pass
for BOTH members before a mean is taken. It is not a disordered quasiparticle
gap, nor an adiabatic branch assignment between uncomputed configurations.
Host/Cd Gamma8 spreads2.15e-11/2.02e-12eV; Gamma6 spreads4.84e-12/1.21e-12eV.
These spreads are diagnostics, NOT eigenpair/material error bounds.

The Gaussian chemical response has conditional positive-tail/nearby-frame/IEEE
interval **[.197871355,.205045167]eV**. All five W1–3eV intervals are positive;
central values range.194777015–.201954562eV. Those are different probe widths,
not a PBE method or material uncertainty sweep. Original fixed physical
40Ry projectors are isometrically transported; they are not replaced by a
new fitted/renormalized frame. Independent real-space embedding and actual
block-unitary inverse-response errors are2.87e-15/2.22e-16.

At eta=.05eV the scalar inverse response interval is[.118253626,.152019310]eV.
The FULL6x6 inverse agrees in central value to3.1e-15eV and has the more
conservative fixed-frame tail/IEEE interval[.112706644,.157566292]eV.
Inversion margins are.999509/.988389; positive Stieltjes and causal effective
operator damping signs pass. Gamma6/8 mixing norm is1.53e-7/1.34e-7eV;
scalar-block defects are<=2.74e-10eV. No support-free domain D was used.
`matrix_causal_rows.mass_eV` means HALF this finite-resolution block-trace
ordering at each own EF+i eta. It is NOT the earlier exact common-mode crossing
mass mu(x), a real pole mass, or a topological Hamiltonian. Eta is analytical
resolution and not intrinsic linewidth. Common traces are relative to own EF,
not an absolute specimen band offset or an aligned impurity T-matrix.

## What changed microscopically in the captured spectra

Cd moves2.141% of captured Gamma6-frame probability outside its dominant pair
and.889% of Gamma8 probability outside its dominant quartet. Missing total
probabilities are.0583%/.0635%. Exact retained-spectrum centroid algebra gives
Gaussian-minus-tracked chemical change **+32.424976meV**; inverse-minus-tracked
is **-33.896817meV**. This quantifies spectral redistribution and probe
dependence, not a fitted static/dynamic self-energy decomposition.

Prior x=.25/k3 Gaussian response+.392177486eV differs from the new x=.125
response by-.190719225eV. Composition, cell and BZ sampling differ together:
new16Gamma folds conventional Gamma AND R. No dilute slope, bowing coefficient,
BZ convergence or alloy mass law is inferred. Both absolute orderings remain
negative; even the finite-resolution observables have no inversion bracket.
Do not add the old44.184/39.812meV HSE activation to these different observables.

## Native and source-state evidence

| Native diagnostic | Host | Cd |
|---|---:|---:|
| SCF steps | 11 | 12 |
| Final native residual, Ry | 9.01115e-10 | 4.90946e-10 |
| Total energy, Ry | -3877.902441281290 | -3878.083245590362 |
| Independently reconstructed charge error, electrons | -6.37e-11 | +1.33e-11 |
| Owned wall, seconds | 340.123 | 345.365 |
| Kernel memory peak, bytes | 2114387968 | 2105356288 |
| Native nonlocal density Theta relative HS defect | 4.530e-7 | 1.639e-7 |

The actual FD density audit includes occupied-space geometry and weights,
not just zero local spin. C3/S4 defects are4.45e-7(host)/1.61e-7(Cd).
This is six orders below the old broken HSE density, but does NOT pass a1e-8
HSE-source requirement. No source/occupation purification or HSE release follows.

Stock QE7.5, SG15 FR NC, fixeda6.46Angstrom,50/200Ry,352spinor bands/288e,
Gamma, FD.001Ry. Both real2rank leases/exit/manager/cgroup cleanup gates pass.
Maximum sampled pair output384159744B; host RAM floor>27.67GB and disk>56.87GB.
Post-exit recursive retained-file accounting charges503050240B for the complete
pair, including files finalized between live samples, below14GiB. Raw total
energies above are not formation energies across different pseudopotential species.
These are measured bounded PBE resources, not an HSE or streaming memory claim.
Sampling retains the documented between-sample burst/external-writer risk;
no host-wide MPI absence or private-net proof is claimed.

## Preserved refusals and interpretation boundary

The original p16 owner FAILED before QE lease due a socket-name defect. It was
not rerun. Fresh P2 host completed native SCF/owner but its first readback
assertion used wrong HDF5 reciprocal units and FAILED. That source/assertion
remains unchanged. Native write source plus independent actual HDF5/XML/cell
checks establish B_HDF5=2*pi*A^-T; separate read-only v2 qualification passes
ALL intended physical/charge/symmetry conditions at unchanged tolerances.
Only then a fresh Cd-only unit ran. Exactly TWO native SCFs, no host rerun;
old failures and all prior HSE/occupation/byte-replay failures are immutable.

PROVEN UNDER ASSUMPTIONS in the separate
[environment theorem](../ordered_environment_2026-10-15/theorem.md): neither
ordered specimen samples N2/N3 Te environments. Their independent operator
responses remain invisible even to complete measured Hamiltonians in the fixed
local model. First-principles state/functional/random-environment information
remains indispensable; physical xc is unidentifiable from these data.

**Decision:** retain the positive microscopic Cd response and its three distinct
observables. Stop native acquisition at this completed finite pair. Next useful
physical contrast is a same-cell/same-composition N2-sharing pair, after the
separately unresolved HSE state bridge if a hybrid prediction is sought; see
[ranked minimum input](../ordered_environment_2026-10-15/minimum_input.md).
No further grid churn, defective HSE iteration, empirical interpolation or xc.
