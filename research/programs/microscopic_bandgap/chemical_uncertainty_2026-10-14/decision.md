# Decision — probe curve and one real k-refinement completed

2026-10-14 18:24 UTC, clean parent b776a9e. **CALCULATED / FINITE EXPERIMENT
COMPLETE.** Stop native acquisition at the stated one-pair limit. No rerun of
original Gamma-only pair, separate NSCF, retry, physics-parameter downgrade or
extra campaign. Original HSE16/352 target, historical failures and blocked goal
remain unchanged. This is exploratory periodic x=.25 PBE+SOC materials input.

## Step1: true retained-data probe uncertainty

All30 preregistered width/reference combinations use actual retained176band
complex overlaps. At each member's own Fermi reference:

| W eV | Original Gamma-only DeltaOmega eV | Conditional bound meV |
|---:|---:|---:|
| 1 | .3845942490 | 2.533 |
| 1.5 | .3942522821 | 3.126 |
| 2 | .4010050707 | 3.835 |
| 2.5 | .4035423888 | 4.577 |
| 3 | .4040711964 | 5.332 |

Across all widths and common[-.5,-.25,0,.25,.5]eV offsets from EACH member's
own Fermi reference, calculated response spans **.3823211179–.4111676987eV**,
a28.8466meV probe range. Union of conditional completion/projector/arithmetic
intervals **[.3795185850,.4174176506]eV** is strictly positive. Minimum Gaussian
mass.334882 exceeds unchanged.05 floor. Dominant own-Gamma8 reference gives
the same curve at stored precision in this old packet. This is spectral-probe
sensitivity, NOT a physical error bar or a k-convergence result. No best width
was selected after inspecting data. [Curve](width_curve.png), CSV/JSON and
underlying complex coefficients/source hashes are retained.

## Step2: actual matched Gamma-containing 2x2x2 refinement

One sequential fresh stockQE7.5 pair,8atom176band144e,40/160Ry,FDsigma.001Ry,
PBE+SOC/SG15FR NC,identical fixed a6.46A/cell/origin/spin axes. Exact atomic
Td proof and mesh stars allowed native symmetrization/reduction of8 points to
4 representatives with weights(1,3,3,1)/8. Both native schemas confirm this.
All-k weighted charge is checked independently; Gamma normalization is kept
separate. No arbitrary representative-density substitution and no Gamma NSCF.

| Actual native outcome | Pure host K2 | Cd-in-host K2 |
|---|---:|---:|
| Native SCF iterations/convergence | 11 / true | 11 / true |
| Native PWSCF wall seconds | 162.92 | 158.32 |
| Total energy Ry (species differ; no formation-energy inference) | -1939.2511335858035 | -1939.4383635152817 |
| Estimated SCF error Ry | 1.2975e-10 | 3.7473e-10 |
| Weighted charge residual electrons | -1.4154e-11 | +2.6688e-11 |
| Sampled RSS bytes (shared overcount) | 778702848 | 774737920 |
| Measured kernel memory peak bytes | 693432320 | 689721344 |
| Terminal manager/lease/kernel exit/cleanup | PASS | PASS |

With the **same original physical host Gamma6/8 projectors**:

| W eV | Original DeltaOmega eV | Refined DeltaOmega eV | Measured new-minus-old meV |
|---:|---:|---:|---:|
| 1 | .3845942490 | .3778026646 | -6.792 |
| 1.5 | .3942522821 | .3881369898 | -6.115 |
| 2 | .4010050707 | .3953518512 | -5.653 |
| 2.5 | .4035423888 | .3981196681 | -5.423 |
| 3 | .4040711964 | .3988014317 | -5.270 |

AtW2: **DeltaOmega_K2=+.3953518511520109eV**, conditional completion/projector/
arithmetic envelope ±.003740918367205293eV. Measured method/grid difference
**−5.653219558meV** has conservative conditional interval
**[−13.228988113,+1.922548997]meV**, including zero. Positive chemical response
persists on both tested meshes/widths under the stated model. Neither BZ
convergence nor the true physical sign of grid error is certified. Old run used
nosym=true/new nosym=false, so this comparison includes the legitimate Td
symmetrization route; a separate symmetry-toggle control was not run.

At W=1, the conditional difference interval is **[−11.78872,−1.79445] meV**,
which excludes zero under the same spectral assumptions. The narrower probe
therefore resolves a negative method/grid change within this model, whereas
the broader W=2 bound does not. This is not a material-error or convergence claim.

Own-Fermi and own dominant-Gamma8 recipes differ in refined DeltaOmega by
<5e-14eV at stored precision; actual reference offsets<3e-12eV are independently
recorded. This numerical coincidence is not physical pico-eV accuracy, a
cross-species potential alignment or a general theorem about Fermi references.

Both native Gamma matrices have matching7809PW spaces. New-host Gamma6/8
multiplicities(1,0,0)/(0,0,1) pass independent complex character/translation
checks. Original-to-newhost principal overlaps>.99998; projector distances
.005656/.004392. Primary frame stays fixed. Separately replacing it with the
new-host frame changes refined DeltaOmega by only **+.06218meV**. Actual
complex coefficients, every retained trace weight/energy and frame conditions
are retained. [Comparison plot](grid_comparison.png), [numerical record](grid_result.json).

## Acceptance, uncertainty boundary and ranked next information

Safety caps held12GiB/swap0/tasks12/600s/member,one actual local MPI family,
host4GiB/disk10GiB floors and sampled14GiB aggregate output. Sampled host
availability stayed>27GiB; disk>61GiB. Independent final retained aggregate
360718336B (<.34GiB) passes. Kernel groups absent/lock available. Source,
PPs,ELFs,inputs,all-wave hashes and raw logs/schema/leases/telemetry are archived.
Stock/dirty DFT/old ledger/old native results/Calcura/other sessions and projects
are unchanged. No host-wide foreign-MPI exclusion or private-network proof.
Original host terminal-recording uncertainty stays false/null; the new host
terminal PASS does not retrospectively repair it.

Six focused independent native-data/mathematical tests PASS in.525s. Exact scalar
positive-tail/derivative arguments and counterexample limitations are in
[methods](methods_and_bounds.md). No novel-method priority or manuscript claim.

The remaining highest-information accuracy input is **a matched cutoff
qualification of this same chemistry/frame/grid**, before extending cell size
or substituting HSE-quality claims. Current40/160Ry cutoff error is unbounded;
one additional k mesh does not fix it. Functional/dilution/ionic/many-body and
random-alloy errors also remain open. No additional native job is issued here.
Original HSE memory/cold-root/full-state gates remain necessary in their own
domain. No physical x_c, detector cutoff, fully converged HSE or streaming
whole-SCF RAM-gain claim.
