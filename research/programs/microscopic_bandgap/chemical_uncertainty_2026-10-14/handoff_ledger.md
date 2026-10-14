# Context-reset handoff — 2026-10-14 18:24 UTC

Parent b776a9e; original research branch and session. The user authorized a
retained-data width/reference curve and ONE matched native k refinement. Both
are complete. Stop native runs: no original-pair rerun, NSCF capture or retry.

The 30 retained-spectrum probes use W=1,1.5,2,2.5,3 eV, each member's Fermi
reference with common offsets -0.5,-0.25,0,0.25,0.5 eV, and its dominant Γ8
quartet centre. DeltaOmega spans 0.382321–0.411168 eV; the conditional interval
union [0.379519,0.417418] eV is positive. The 28.85 meV probe range is separate
from material and grid errors. CSV/JSON/PNG/PDF and an independent variance
reference-derivative check are retained.

New raw root: DFT .local/qe75_lowram_20261011/chemical_pbe8_k2_20261014, host/
and cd/. Both native SCFs converge in 11 iterations, 162.92/158.32 seconds.
Weighted FD charge errors are below 2.7e-11 electron. The unchanged setup is
8 atoms, x=0.25, a=6.46 Angstrom, SG15 FR NC, PBE+SOC, 40/160 Ry, 176 spinor
bands, 144 electrons and FD width 0.001 Ry. The new unshifted 2x2x2 mesh uses
native Td symmetrization: four stars with weights (1,3,3,1)/8, Gamma index1,
and four saved HDF waves. No NSCF. The old nosym=true/new nosym=false route
change is explicit; this is method/grid sensitivity, not a pure certified
BZ error. Original HSE16/352 and all historical failures are unchanged.

The ORIGINAL physical host Γ6/Γ8 frames remain primary across grids. New-host
characters and primitive-Γ probabilities pass; principal overlaps exceed
0.99998. The separately labelled new-host frame changes refined DeltaOmega by
only +0.06218 meV. Primary W2 response is +0.395351851152 eV versus the original
+0.401005070710 eV, a measured -5.65322 meV change. New conditional bound is
±3.74092 meV; the difference interval [-13.22899,+1.92255] meV includes zero.
No BZ convergence, material error bar or physical x_c. Fermi and dominant-Γ8
recipes agree at schema precision; offsets below 3e-12 eV do not imply physical
pico-eV accuracy or absolute cross-species alignment.

Both NEW owners pass typed rank/kernel/ELF leases, retained manager invocation
and exit0, kernel rank exits and empty-group/exclusive-lock checks. Caps:
12 GiB, swap0, tasks12, 600 s; observed RSS below0.78 GB, kernel memory below
0.70 GB, host available above27 GiB and free disk above61 GiB. Independently
checked retained aggregate is360718336 B under the sampled14 GiB budget.
Original host terminal-record uncertainty remains accepted=false/terminal=null.
The new host PASS does not repair the old result. No host-wide MPI absence or
private-network proof is claimed.

Six focused tests pass. Archives retain inputs, schemas, exact compressed logs,
leases, managers and telemetry; all native wave hashes remain pinned privately.
Complex Γ overlaps and trace spectra are retained. Protected-before/after checks
show stock, dirty DFT, HEAD/status/diff and old ledger unchanged; both new groups
are gone and the lock is free. No Calcura, session, supervisor, other-program
or historical-goal action. Publish with the existing id_ed25519_kajin identity.

The next accuracy input is matched cutoff qualification at the same grid and
frame before costlier functional/cell/ionic changes. No further native queue is
authorized by this finite protocol. Used run_grid.py roots refuse reruns. Read
decision.md and methods_and_bounds.md before a new request.
