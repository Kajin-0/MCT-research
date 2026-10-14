# Measured cutoff sensitivity of the x=0.25 projected chemical response

**CALCULATED — completed, finite native experiment.** Starting from clean pushed
31e872e, ONE sequential two-rank stock QE 7.5 pair increased only the wave/density
cutoffs from 40/160 to 50/200 Ry. Both Hg4Te4 and CdHg3Te4 SCFs converge in
11 iterations. The W=2 eV response changes from +0.395351851152 to
**+0.393337031960 eV**, or **−2.014819 meV**. No native retry, NSCF, HSE,
16-atom run or additional grid calculation was performed.

This is the difference of two Gaussian projected Gamma6-minus-Gamma8 centroids
in a periodic 8-atom x=0.25 cell, with fixed physical host projectors. It is not
the bulk random-alloy signed gap, a sharp eigenvalue crossing or physical x_c.
Static ions and the fixed FD numerical smearing have not been extrapolated.

## Prospective protocol and measured native results

[Preregistration](preregistration.md), [frozen pins](frozen_protocol.json) and
[preflight](preflight.json) precede both runs. The cell is fixed at 6.46 Å,
SG15 fully relativistic NC potentials, 176 spinor bands/144 electrons,
PBE+SOC, FD sigma 0.001 Ry, conv_thr=1e-9 Ry and unshifted Gamma-containing
2x2x2 sampling. The same native Td symmetry reduces it to four weighted
representatives (1,3,3,1)/8. Inputs differ from the baseline only in the
declared cutoffs and private output paths; the independently checked host and
Cd cells, origins, spin axes and wave conventions agree.

| Measured quantity | Host | Cd substitution |
|---|---:|---:|
| Native SCF iterations | 11 | 11 |
| Native PWSCF wall, s | 226.27 | 212.73 |
| Owner elapsed, s | 227.606 | 213.939 |
| Total smeared energy, Ry | −1939.323093685065 | −1939.499979093468 |
| Native estimated SCF error, Ry | 3.048e-10 | 3.662e-10 |
| Independently reconstructed charge residual, electrons | −1.251e-12 | +1.251e-11 |
| Sampled family RSS, bytes | 1,037,570,048 | 1,031,184,384 |
| Kernel cgroup memory peak, bytes | 953,614,336 | 947,720,192 |

Both native science and terminal owner gates pass, with actual two-rank live
leases, kernel task exits, matching retained manager invocation/exit zero and
empty original cgroups. Peak RSS sums can overcount shared mappings. Kernel
12 GiB/swap-zero/tasks12 and 600 s/member caps were retained; sampled host RAM
stayed above 28,720,742,400 bytes and disk above 65,455,194,112 bytes. Final
independent retained output charge is **499,945,472 bytes** under the aggregate
14 GiB local contract. Disk/metadata accounting remains sampled, with explicit
producer/external-writer between-sample risk; it is not a quota or continuous
guarantee. No original host-wide MPI exclusion or network-isolation claim is made.

Full inputs, schemas, exact stdout, telemetry, rank/owner/terminal records and
ELF/PP/source/wave hashes are archived in [native_evidence](native_evidence)
and [evidence_manifest.json](evidence_manifest.json). Large complex spinors
remain in pinned private DFT storage. Stock QE and the protected dirty DFT
status/diff/files and old finished ledger are unchanged.

## Cutoff, finite-spectrum and physical-frame effects

**PROVEN UNDER ASSUMPTIONS / CHECKED ON ACTUAL WAVES:** the NC same-cell map
from the original 40-Ry host space to 50 Ry is an isometry matching physical
(G+k)B vectors. Every one of 7,809 source vectors is present in the 10,827-vector
target; 3,018 new vectors receive zero reference coefficients. No vector is
discarded, no state is renormalized and no native index overlap is used.
Maximum Gram change is 7.77e-16. All 24 Td operations intertwine under this
embedding; permutation, missing-source and wrong-cell counterchecks pass.
See [derivation](cross_cutoff_proof.md) and [complex overlaps](e50_complex_overlaps.npz).

The primary original projector stays fixed throughout this table. Own-Fermi
and independently defined dominant-Gamma8-quartet reference recipes agree
within 3e-12 eV for this dataset; this is not a general absolute band-alignment
theorem. Shading in [the figure](cutoff_comparison.png) includes conditional
completion/projector/arithmetic bounds, not material errors.

| W, eV | Response at 40/160, eV | Response at 50/200, eV | Measured change, meV | Conditional change interval, meV |
|---:|---:|---:|---:|---:|
| 1 | 0.377802665 | 0.375968165 | −1.83450 | [−6.83180, +3.16280] |
| 1.5 | 0.388136990 | 0.386207860 | −1.92913 | [−8.09595, +4.23769] |
| 2 | 0.395351851 | 0.393337032 | −2.01482 | [−9.57679, +5.54715] |
| 2.5 | 0.398119668 | 0.396066832 | −2.05284 | [−11.07615, +6.97048] |
| 3 | 0.398801432 | 0.396748057 | −2.05337 | [−12.56509, +8.45834] |

All new response intervals are positive under the conditional mathematical
model. At W=2 the new interval is [0.389515979249,0.397158084671] eV. The
cutoff-difference interval includes zero: the negative sign of the completed
cutoff correction is not certified by these conservative bounds. The
preregistered |change|>10 meV poor-input warning is not triggered. Two cutoffs
do not establish infinite-cutoff convergence or separate wave/density effects.

At W=2, omitted probability is host Gamma6/Gamma8 1.9252e-5/1.2709e-5 and
Cd 5.7705e-4/1.1063e-3; Gaussian masses are respectively
0.89018075/0.99997640 and 0.94137755/0.99396842, above the unchanged 0.05
floor. The positive-measure Gaussian tail bound uses the joint perturbed
denominator. Native eigenpair, functional, finite-cell, grid, ionic and
many-body errors are not controlled by that bound or by the total SCF error.

Independent native 50-Ry host sectors pass primitive-translation and complex
Td classification: Gamma6 bands139–140, Gamma8 bands143–146. The latter is
at the host Fermi energy; the Gamma6 doublet is about −0.964447 eV relative
to it. These host levels do not substitute for the chemical centroid observable.
Native 40K2→50 host projector distances are 0.00404253/0.00291057.
New-host high-G probabilities outside 40 Ry are about 1.3800e-5/7.5396e-6.
Following the new host frame instead changes the W2 response by only
**+0.087142 meV** at 50 Ry (baseline +0.062183 meV). Its cutoff change is
−1.989860 meV. This separate frame comparison never replaces the primary
fixed-projector result; small high-G norm alone does not bound an ordinary
unfiltered energy moment.

## Decision and next experiment

**ADVANCE the exploratory periodic PBE response as a measured sensitivity
result; STOP this finite native pair.** Seven focused independent checks pass.
The initial malformed mapping-test expectation is retained in
[source_test_correction.json](source_test_correction.json); no native admission
or physics was changed to repair it. Original host terminal uncertainty and
historical HSE occupation/neutrality/owner/RAM failures remain unchanged.

[The separate HSE assessment](hse_feasibility.md) gives source-conditioned
buffer subtotals and explicitly heuristic times. No HSE job is admitted or
launched: whole overhead and 8-atom timing/convergence data are missing, and
even a Gamma/q1 14-update comparison horizon projects to about 25 minutes/member.
Within the present 600-second budget, the best next chemistry uncertainty test
is matched PBE50/200 unshifted3x3x3 (four symmetry representatives; estimated
220–260 s/member). If functional accuracy takes priority instead, rank one
missing HSE input as actual 8-atom Gamma/q1 first-ACE timing/whole peak/native
descriptor under a separate bounded authorization. Neither proposal is executed
here; no queue, altered target, converged HSE or physical x_c claim is created.
