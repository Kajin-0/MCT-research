# Measured k3 sampling sensitivity of the x=0.25 chemical response

**CALCULATED — finite native pair completed.** From clean pushed3fe5ef2,
ONE sequential stock QE7.5 PBE+SOC Hg4Te4/CdHg3Te4 pair changes only the
unshifted k mesh2x2x2→3x3x3 and private paths. The W2 Gaussian projected
response is **+0.392177486293 eV**, versus **+0.393337031960 eV** at k2:
measured grid change **−1.159546 meV**. Both native SCFs converge11 steps.
No retry,NSCF,HSE,other composition,source-arithmetic change or extra job.

This observable is a difference of specified projected centroid orderings
in an ordered periodic8atom x=.25 cell. It is not the real-alloy signed gap,
absorption edge, physical x_c or an experimental/material uncertainty bar.
An independent actual-schema nearest-neighbor check finds all four Te sites
have N=1 Cd neighbor in the substituted cell (N=0 in host). Thus it tests a
uniform Hg3Cd tetrahedral count in a periodic x=.25 background, not the
Bernoulli mixture of five environments or an isolated dilute impurity. It
does not extract a transferable F1 matrix or impurity T-matrix; see
[local_environment.json](local_environment.json).

## Prospective/native qualification

[Preregistration](preregistration.md),[source/input/PP/ELF freeze](frozen_protocol.json)
and[preflight](preflight.json) precede launch. Keep SG15FR NC,176spinor bands/
144e,50/200Ry,FDsigma.001Ry,6.46Angstrom fixed cell/origin/ionic positions/
global spin axes,PBE+SOC,native nosym=false,conv_thr1e-9 and all other solver
parameters. Independently normalized inputs differ from accepted k2 only in
mesh and private paths. No inherited aborted/restart density or wave state.

Native inputs/outputs confirm24 crystal Td operations and time-reversal
reduction to four k3 stars with weights(1,6,12,8)/27. Both actual XML rotation
sets equal the24 declared Td matrices, all crystal translations are explicit
zero, one unique Gamma is saved directly at the new SCF charge. The initial
read-only parser wrongly included24 extra lattice-only rotations; pinned QE
source distinguishes these by `info=crystal_symmetry` versus `lattice_symmetry`.
[Correction evidence](intake_correction.json) is retained; absent translations
were not replaced with zero and no scientific/resource threshold changed.
Host source/terminal/frame gates pass before Cd launch. Five focused checks pass.

| Actual native quantity | Host | Cd substitution |
|---|---:|---:|
| Native SCF iterations | 11 | 11 |
| Native PWSCF wall, s | 243.78 | 225.01 |
| Owner elapsed, s | 245.815 | 226.681 |
| Smeared total energy, Ry | −1939.342780123225 | −1939.520436638572 |
| Native estimated SCF error, Ry | 4.916e-10 | 3.718e-10 |
| All-k reconstructed charge residual, electrons | +3.888e-11 | −9.101e-11 |
| Sampled family RSS peak, bytes | 1,036,648,448 | 1,030,868,992 |
| Kernel cgroup peak, bytes | 952,119,296 | 946,941,952 |

Both actual typed two-rank leases, kernel task exits and retained manager
invocation/exit zero pass; owned groups are absent afterward. Kernel12GiB/
swap0/tasks12/600s and4GiB host/10GiB disk floors hold. Minimum sampled RAM
28,873,519,104B and disk64,770,048,000B; RSS can overcount shared mappings.
Final independent pair output charge is **500,674,560B**, below sampled14GiB.
This local output/metadata accounting retains between-sample producer/external
writer risk, not a quota or continuous theorem. Original host-wide exclusion
and private-network proofs remain unpassed and are not claimed by this pilot.

Actual inputs/schemas/stdout/telemetry/leases/manager records and all wave/source/
ELF/PP hashes are in[native_evidence](native_evidence) and[the manifest](evidence_manifest.json).
Large waves remain pinned privately. Protected stock,DFT HEAD/status/diff/files
and old finished ledger match before/after. Other sessions/supervisors/Calcura,
dirty DFT and historical goal receive no changes or signals.

## Fixed-frame response and uncertainty

**PROVEN UNDER ASSUMPTIONS / VERIFIED ON ACTUAL SPINORS:** every original
40Ry source vector is embedded by physical(G+k)B into the50Ry Gamma basis:
7809→10827PW with3018new-only zero reference coefficients. No missing source
vectors,discarded source norm,renormalization or naive native-index overlaps.
All24 symmetry maps intertwine; independent complex contractions and wrong-cell/
missing-source/permutation counterchecks pass. Native Gamma NC Gram defects
are3.41e-14/5.47e-15. Primary original physical host projectors never change.

| W, eV | k2 response, eV | k3 response, eV | Measured change, meV | Conditional change interval, meV |
|---:|---:|---:|---:|---:|
| 1 | 0.375968165 | 0.374624221 | −1.34394 | [−6.39666,+3.70877] |
| 1.5 | 0.386207860 | 0.384964595 | −1.24326 | [−7.46838,+4.98185] |
| 2 | 0.393337032 | 0.392177486 | −1.15955 | [−8.78763,+6.46854] |
| 2.5 | 0.396066832 | 0.394951709 | −1.11512 | [−10.21368,+7.98344] |
| 3 | 0.396748057 | 0.395661486 | −1.08657 | [−11.68336,+9.51021] |

At W2 the primary host/Cd orderings are−0.958711634231/−0.566534147938eV;
the positive response is their DIFFERENCE. It must not be read as a positive
absolute semiconductor gap. Own-Fermi versus own dominant projected-Gamma8
references agree within6e-13eV in W2 response for this dataset; this numerical
coincidence is not general reference or band-offset invariance.

W2 new response interval[0.388370450922,0.395984521665]eV uses conditional
positive-tail/projector/IEEE bounds. All ten tested width/reference response
intervals remain positive. Every conservative grid-difference interval includes
zero: the sign of the completed grid correction is not certified. Native SCF
total-energy tolerance is not an individual eigenpair/operator error bound.
Cutoff,finite-cell,functional,ionic/zero-point,BZ-continuum and material errors
remain unknown. Two same-cutoff meshes do not establish BZ convergence or
permit an extrapolation law. Preregistered10meV poor-sampling warning is not
triggered; the phase stops without another mesh.

At W2, retained Gaussian masses are hostGamma6/8 .89139340/.99996923 and
Cd .94178922/.99401223, above the unchanged.05floor. Omitted probabilities
are host2.1346e-5/1.4979e-5 andCd5.7447e-4/1.0974e-3. The joint denominator
bound is derived in[methods_and_bounds.md](methods_and_bounds.md), with no
renormalization of incomplete retained probability. Arithmetic uses actual
50Ry component count for BOTH k2 and k3.

Native new-host sectors retain primitive-Gamma and complexTd6/8 character
(bands139–140 and143–146). Native k2→k3 host projector distances are
.00119284/.00083708. Using the new k3 host frame separately changes W2
response by+.099038meV (k2+.087142meV); its grid change is−1.147649meV.
Primary frames stay fixed. These are geometric/probe effects, not material
error bars. See[complex overlaps](k3_complex_overlaps.npz),[full result](grid_result.json)
and[the response figure](grid_comparison.png).

## Decision and next physics

**ADVANCE this periodic PBE response as measured sampling sensitivity;
STOP the finite native assignment.** Both science/owner/resource gates pass,
five focused tests pass and protected-state/archival checks pass. All original
host terminal uncertainty and HSE occupation/neutrality/owner/RAM failures
remain unchanged; no HSE convergence,physical x_c or whole-SCF RAM-gain claim.

Recommend a separately scoped **matched8atom HSE Gamma/q1 first-ACE timing/
resource pilot** before another composition at the same unqualified functional.
The present k sensitivity is ~1.16meV, while functional uncertainty is unresolved.
Source-conditioned complex EXX+xi+current PBE peak subtotal is2.230GB, NOT
an RSS admission bound; heuristic first-ACE pair time320–365s, NOT completion
or convergence assurance. Need the actual176-band stop/diagnostic path,
native descriptor/state/output/resource admission and separate authorization.
It would measure one exchange build, not a self-consistent HSE chemical gap.
[Exact next-input assessment](next_experiment.json) and[recommendation](next_experiment.md)
create no job,queue,source build or launch. Original16atom352band remains untouched.
