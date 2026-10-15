# PASS: one HSE relaxation changes chemical operator trace by −4.373 meV

**CALCULATED:** the matched Cd-minus-host fixed-reference Γ6–Γ8 projected
operator correction changes from **+44.184097247 meV** at first activation to
**+39.811503589 meV** after one hybrid orbital/density relaxation and second ACE
rebuild. The additional change is **−4.372593659 meV**. Its exchange contribution
is +1.239720012 meV; the local-potential contribution is −5.612313671 meV. The
local contribution now includes density/Hartree response, not just fixed-density
XC replacement. [Methods](methods_and_limits.md) define the three observables.

| Chemical projected contribution (meV) | First activation | After one relaxation | Change |
|---|---:|---:|---:|
| Direct exchange | +55.956326907 | +57.196046919 | +1.239720012 |
| Local potential | −11.772229659 | −17.384543330 | −5.612313671 |
| Total | +44.184097247 | +39.811503589 | −4.372593659 |

The first activation reproduces the earlier independent +44.184097193 meV
within 5.42e-11 eV. The positive projected correction persists for this finite
update; it is not a certified limiting sign, converged HSE bandgap, or physical
x_c. The measured step is not a bound on the uncomputed outer remainder.
Do not add either number to the earlier k3 PBE Gaussian response.

## Actual native execution

Exactly ONE fresh two-rank Hg4Te4 member followed by ONE CdHg3Te4 member, with
no retries or restarts. Both accepted owner/source/science/resource/readback
gates. Each performs preliminary semilocal SCF (11 steps), first ACE, one HSE
inner SCF (9 steps), second ACE, native Fock/dexx and post-punch publication.
It then deliberately saves outer convergence=false before a third update or
QE's potentially misleading outer-budget convergence branch.

| Measurement | Host | Cd substituted |
|---|---:|---:|
| Guard wall (s) | 410.332676 | 409.314651 |
| QE wall (s) | 408.54 | 407.63 |
| Kernel MemoryPeak (bytes) | 4,548,526,080 | 4,541,669,376 |
| Sampled family RSS, shared overcount (bytes) | 4,290,301,952 | 4,284,145,664 |
| Hybrid inner SCF error (Ry) | 7.76670e-11 | 4.42052e-10 |
| Final charge residual (electrons) | +5.81508e-11 | −1.60298e-11 |
| Second half-Fock (Ry) | −35.798735450445 | −35.849732444501 |
| Second corrected native total (Ry) | −1936.319184664065 | −1936.463322257280 |
| Native dexx (Ry) | 0.002518748847 | 0.002548968880 |

All four source direct/ACE action and Gram comparisons are below the frozen
1e-8 tolerances (actual residuals are approximately6e-16). Final source wave is
bitwise verified against HDF5; both source stages preserve rhoR/rhoG/G/probe
bytes within each rebuild. Actual stored charge-density coefficients change
by relative norms0.00421477/0.00426263, with86791 distinct physical density G
labels. These are observed density changes, not a material error estimate.

Independent actual-data checks passed charge sums, per-column complex/Fock
contractions and distributed old-xi/new-Phi ACE contractions. Old-ACE fock1
matches native within2.85e-14Ry (host) /1.43e-14Ry (Cd); signed dexx is independently
reconstructed. This validates the native old/new operator dependency used here
without claiming old ACE equals old direct Fock on arbitrary new orbitals.

Both actual 84/82-byte socket paths bound before services. Fresh roots/jobs/
nonces and all physical/source/ELF/PP/backend pins passed. The numerical and
resource gates were frozen before launch and unchanged after observation. Same
8 atoms/176 spinor bands/144 electrons, SG15FR NC/a6.46Å, HSE .25/.106,
50/200/Fock200Ry, Γ/q1, FD.001Ry and native solver. Only the diagnostic outer
budget changes from1 to2. The three-object private observer/stop leaves exchange,
compression, local-XC and occupation/solver arithmetic unchanged.

12GiB/swap0/tasks12/600s caps held, host available RAM stayed above25.239GB and
free disk above62.094GB. Final pair output charge is1,465,839,616bytes, below
14GiB. Output remains a sampled guarantee with explicit burst/external-writer
risk; no hard aggregate quota, host-wide MPI absence or private-network proof.
Both own cgroups are absent, lock free, old ledger exact. Kernel peak includes
charged file pages; sampled RSS can overcount shared maps. Neither is evidence
of whole-SCF memory saving against stock or an unmatched task.

## Scope and decision

**PASS for this finite physics acquisition; STOP native work.** The first
chemical HSE activation is not erased by the measured relaxation. Local density
response reduces its projected trace by several meV. Further hybrid outer
relaxation remains indispensable before self-consistent HSE spectral inference:
dexx is still roughly2.5e-3Ry versus1e-9Ry target, and final eigenvalues solve
first ACE, not the rebuilt second operator. Native dexx is extensive and is not
a Γ-gap error bar. Full convergence within600s remains unproved.

Raw packets/waves and compiled source/ELF are retained privately with hashes;
logs, XML, ranks/manager/telemetry and complete complex projected matrices are
archived here. Three focused independent scientific checks passed. No empirical
fit, full-HSE/physical-x_c/restart claim. All earlier failures and accepted data,
stock/dirtyDFT, original16atom352band, Calcura/sessions/supervisors/goal/main are
untouched. Commit/push only existing MCT research branch, then stop this scope.
