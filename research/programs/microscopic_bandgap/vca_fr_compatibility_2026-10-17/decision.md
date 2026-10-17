# Fully relativistic Hg/Cd VCA: pseudo/reader compatibility GO

2026-10-17 06:38 UTC; baseline `242e042a3fb6ca351ec9ff72ed9cdcabe32ef6a2`.
**GO for this specific stock virtual_v2/SG15 pair's pseudo construction and
SOC reader compatibility, within the frozen endpoint tests. HSE launch NO-GO
pending separate approval/admission.** Zero spending. Five stock-QE dry checks
and four endpoint PBE+SOC SCFs completed; **no mixed-composition SCF or HSE**.
This does not reopen the permanently closed PBE static-operator diagnostic.

## What is actually compatible

The supplied earlier `virtual_v2.x` outputs are retained at
`/tmp/r07_vca_20261017_compatibility/{x_1_0,x_0_875,x_0_0}`. Their labels denote
**Hg weights**1,.875,0, hence Cd fractions0,.125,1. Generation was not rerun;
we pin the supplied files/logs and current stock executable, not a nonexistent
original launch receipt. The truncated UPF comment omits the weight, so
external provenance and the actual D blocks are essential.

**CALCULATED / source-verified:** all parents and generated files have
`relativistic=full`, `has_so=true`, NC type, PBE,20-electron cation valence,
no NLCC/PAW/US augmentation. The Te parent has16 valence electrons. The virtual
potential retains **24 radial projectors:14Hg+10Cd**, maximum l=3, all correct
concatenated l/j values; it does not drop SOC. Its1246-point grid equals the
Hg grid and first1246 Cd points. Native beta support ends at indices332Hg,
308Cd, well inside this common grid; no Cd beta tail is lost.

For y=Hg fraction the defined external one-body operator is
`V_y=y V_Hg+(1-y)V_Cd`. Stock construction implements its local part linearly
and its separable nonlocal part with **unscaled concatenated projectors** and
`D_y=diag(y D_Hg,(1-y)D_Cd)`. Cross blocks vanish. The native angular SOC
mapping is linear in those D entries. For these files, both D blocks match
exactly as doubles, beta functions match exactly on the common grid, and the
mixed local average differs by at most1.066e-14Ry from direct arithmetic.
No artificial mixed-beta cross terms are introduced.

This is a valid **specified VCA approximation**, not a theorem equating VCA
with an alloy-averaged self-consistent Hamiltonian, norm conservation at a new
fractional atomic reference, ghost-free transferability at all energies, or
random-alloy disorder. Endpoint checks do not prove those properties.

### Real limitations: Cd radial truncation and inherited metadata

Cd extends to13.67bohr; the generated grid stops at12.45. Its local potential
on retained points is exact at the Cd endpoint, but the discarded interval
has `max|V_Cd+40/r|=6.611e-8Ry`, so **global endpoint operator equality is not
asserted**. The discarded atomic-density array is also nonzero (maximum
1.339e-5 in its radial convention). Initial atomic densities/orbitals can
therefore differ. Both potentials are used through QE's normal radial and
Fourier conventions; finite-grid native agreement below is a test, not a
universal operator bound.

Generated Cd-endpoint CHI labels remain Hg names5S/5P/6S/5D rather than
4S/4P/5S/4D, and some atomic reference metadata is inherited. For this pair,
the six l/j sequences and starting occupations agree; radial CHI arrays are
averaged by matching channel. `read_pp_spinorb` reads jchi/jjj (nn is obsolete),
and `atomic_wfc_so` uses radial CHI,l,j and occupation, **not the printed
principal-shell name**. Both native endpoint families actually initialized
**38 randomized atomic spinors+6 random spinors**, without source changes.
This establishes no label-induced failure in these tests, not absence of
initialization/basin sensitivity in HSE. Do not use inherited atomic-energy
metadata to invent meaningful cohesive/reference energies.

For the mixed file, independent Simpson integration of radial CHI products
gives squared norms0.99830–0.99999 and minimum same-l/j radial Gram eigenvalue
0.99830: no radial cancellation or dependent S pair is detected. This is a
radial initialization check, **not** a finite-plane-wave Gram certificate;
the mixed nstep0 test did not execute native atomic-wave initialization.
See [mixed initialization audit](mixed_initialization_audit.json).

## Native endpoint experiment and frozen acceptance

Fresh outputs are private under
`/home/User/opencode_workspace/DFT/.local/r07_vca_qual_20261017`.
Unmodified stock QE7.5,2 local MPI ranks, primitive2atom fcc cell at6.46Å,
identical origin/sites/spin convention and Te PP; PBE+SOC,50/200Ry,44spinors,
36e,unshifted Gamma-containing1³ mesh,FD.001Ry,conv_thr1e-12Ry,
Davidson/full accuracy,mixing.3,atomic+random,from_scratch. Cd uses the **Hg
lattice**, deliberately: this is an endpoint implementation test, not a CdTe
equilibrium structure prediction. Mass is held fixed within each pair and
has no effect on this clamped-ion electronic SCF.

Before any service, [preregistration](preregistration.json) froze0.1meV for
absolute total-energy and all44 raw/mu-aligned eigenvalue differences, plus
relative rhoG L2≤1e-5 and maximum Fourier-charge difference≤1e-5e. This is5%
of the old prospective2meV contrast budget, not an achieved material bound.
Each state separately requires charge error≤1e-8e and FD formula error≤1e-10.
Occupations are checked against the global FD conditioning bound
`|df_i|≤(|d epsilon_i|+|d mu|)/(4 sigma)` plus2e-12 rounding allowance;
no historical occupation or symmetry threshold is changed.

All five nstep0 checks (originalHg,virtualHg,originalCd,virtualCd,mixed) passed
the native fully relativistic reader. All four ensuing SCFs converged:

| Native endpoint quantity | OriginalHg / virtualHg1 | OriginalCd / virtualCd0 |
|---|---:|---:|
| Inner iterations |15 /15|23 /23|
| Final free energy, Ry |−483.990872146922 /−483.990872146873|−484.1387894802164 /−484.138789497249|
| Final native SCF error estimate, Ry |5.25e-14 /5.36e-14|1.9235e-13 /1.9236e-13|
| Virtual−original free energy, meV |+6.67e-7|−2.3174e-4|
| All44 raw eigenvalue max difference, meV |4.0273e-5|2.0813e-4|
| All44 mu-aligned max difference, meV |4.3856e-5|2.7500e-4|
| Occupation max difference |1.77e-11|1.83e-7|
| rhoG relative L2 difference |5.20e-10|4.71e-9|
| Max G-labelled Fourier-charge difference, e |1.24e-8|7.84e-8|

**Both endpoints PASS the prospective compatibility criteria.** Largest
absolute state charge error7.16e-11e; FD formula error≤5.56e-14. Cell and
physical density-G labels match exactly; density comparison uses labels,
not presumed index ordering. Native geometries report24 operations, but
no new full-density Theta/Td certificate is claimed. No Gamma gap is inferred
from sorted bands. SCF convergence is not a rebuilt full-H residual proof.
Eigenvalues alone are not the operator argument: the independent radial,
SOC and separable-D audit is indispensable, and Cd truncation remains explicit.

## Actual resources, provenance and stop

Nine fresh transient systemd units, sequentially, no retries. Actual kernel
limits read back:12GiB memory,swap max0,tasks12; dry hard60s and SCF hard300s,
with native save deadlines45/240s. Maximum permitted sum1500s,below30min.
**Measured elapsed sum29.730s, kernel peak123,658,240B, maximum sampled tasks7.**
Minimum sampled host available29.733GB/free disk49.251GB; maximum sampled
owned blocks+metadata27.828MB versus14GiB gate. This is sampled output
accounting, not a continuous aggregate quota or deleted-open guarantee.
All units exited0 and were stopped/unloaded; no active pw.x/mpirun or temporary
MPI files remain. Outside `/tmp/r07vq_20261017_0640` was a fresh explicitly
scoped short runtime directory; no other temporary files were modified.
Owned cgroups do not prove absence of foreign MPI. Old Gate A stays REFUSED.

Post-run summary checks initially mishandled terminal `TasksCurrent=[not set]`
and the empty terminal `ControlGroup` field. Native units had already completed;
verification retains unavailable terminal data, uses observed live task samples
and checks each unique **prior nonempty live cgroup path** is now absent.
No calculation rerun or scientific gate change followed.

See [UPF audit](upf_audit.json), [native verification/raw hashes](verification.json),
[endpoint reader](analyze_endpoints.py), endpoint JSONs and committed native
inputs/stdout/XML. Raw saved HDF5 and UPFs remain private at manifest paths,
not publicly exported. `audit_upf.py` and `analyze_endpoints.py` independently
rerun read-only checks using existing DFT/.venv with bytecode/BLAS threads off.
All822 protected pins,76 historical files,DFT dirty status/diff,stock source/
ELFs,previous HSE/PBE failures and primitive k4 decision remain unchanged.

## Conditional HSE feasibility and one next physical input — NOT authorized

The virtual cation increases expanded angular beta count62→96; including Te,
the cell count is96→130. `vkb(npwx,nkb)` adds `34*npwx*16` bytes per rank;
becp and quadratic nhm-dependent SOC arrays/tables also grow. The actual PBE
kernel peaks were116.56MB→123.51MB for Hg and111.31MB→123.66MB for Cd.
These are measurements, not an HSE peak bound.

For a prospective primitive VCA k4/q4/44 HSE model, the retained40³ source
buffer formula remains **5,767,168,000B**, independent of projector count.
The old stock pure-host kernel peak6.226GB makes a12GiB local candidate
plausible, not admitted; new tables/layout/state/output/runtime still need
specific acceptance and fresh explicit approval. No HSE command is issued.

The smallest scientifically useful next input would be a **stationary
primitive VCA x=.125 HSE+SOC state at the matched k4/q4/e50/200/f200/FD law**,
with a properly qualified same-model Hg control, physical Γ6/Γ8 projector
tracking and full occupation/symmetry checks. It would measure the coherent
fractional-external-potential response without supercell band-folding cost.
It would **not** supply a local Cd impurity, Te mixed-environment operator,
configuration covariance or disorder self-energy. Nonlinear HSE self-consistency
is not replaced by interpolating binary eigenvalues.

The existing host ordering−.289586504823eV, dexx2.3e-10Ry and strict1e-8
density symmetry FAIL are unchanged. PBE compatibility cannot make that gate
PASS or admit a nonmagnetic HSE VCA state. No physical x_c, fitted bowing,
2meV HSE/material error, or novelty claim. **Finite assignment complete; STOP.**

Primary source: stock [virtual_v2.f90](https://github.com/QEF/q-e/blob/qe-7.5/upflib/virtual_v2.f90),
[SOC reader](https://github.com/QEF/q-e/blob/qe-7.5/upflib/read_upf_new.f90#L680-L730),
[SOC nonlocal construction](https://github.com/QEF/q-e/blob/qe-7.5/upflib/init_us_1.f90),
[atomic spinors](https://github.com/QEF/q-e/blob/qe-7.5/Modules/atomic_wfc_mod.f90),
and [QE input specification](https://www.quantum-espresso.org/Doc/INPUT_PW.html).
Local immutable qe-7.5 source hashes match inspected working files; stock
executables and PP hashes are recorded, not rebuilt.
