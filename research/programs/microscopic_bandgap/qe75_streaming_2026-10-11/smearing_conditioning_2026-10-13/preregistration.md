# Prospective cold-smearing-conditioned full-SCF pair

Frozen 2026-10-13 before any new native launch. Historical `full_scf_2026-10-13`
step4 FAIL and 1e-8 occupation policy are immutable. This is a NEW experiment,
not retrospective qualification of that failed run.

Same tiny HgTe HSE+SOC/SG15/48 bands/90-360-120 Ry/k2-q2/sigma0.001 Ry,
solver, original 48-band file seed, and existing fresh local-owned scope5.
No restart/import, successful fixed-operator rerun, Cd or 16-atom calculation.
Both private binaries differ from executed build3 only by observation of native
`ener::ef` in the existing scalar packet. Exchange arithmetic is unchanged.
One fresh control then stream; no retry. Maximum600s/member, native480s softstop,
12GiB cgroup/swap0/tasks12, actual authenticated two local ranks,4GiB host
MemAvailable/10GiB disk floor,14GiB AGGREGATE sampled retained output across BOTH members plus escrow and exact
stream extents. Producer bursts/external writers between samples remain a risk;
no global foreign-MPI/network isolation/continuous quota claim.

## Independent numerical budgets, chosen from existing energy target

Keep existing total/Harris/Fock/dexx energy tolerance1e-8 Ry; initial byte-exact
waves/rhoG/et/wg/maps and reconstructed rhoR5e-14/vrs5e-12 Ry; later charge
fields1e-9 and local potential1e-8 Ry; Gram defect1e-10; independent weighted
one-body-density relative Frobenius1e-7. These are engineering reproducibility
budgets, not certified errors relative to converged or experimental material.

Cold-smearing f has maximum<1.1. With48 bands and sum k weights1, total absolute
occupation weight<=52.8. Allocate HALF the old1e-8 Ry energy budget to the
fixed-occupation eigenvalue contribution, so epsilon_budget=5e-9/52.8 Ry
=9.469696969696970e-11 Ry. Independently require EACH native eigenvalue delta
and native chemical-potential delta<=this budget (the latter is a separate
conservative acceptance gate, not inferred from charge neutrality). For fixed
occupations this bounds the eigenvalue contribution to band-energy drift by
5e-9 Ry. It does NOT bound other SCF/Fock/density terms: direct energy and
independent density gates remain mandatory. No threshold is derived from the
failed1.469e-8 occupation number.

Native ef must be directly captured on both ranks and replicated bitwise.
Native full all-k weighted occupations must reconstruct bitwise using unedited
QE gweights_only at captured ef, sigma and weights. Neutrality error<=1e-8
ELECTRONS independently on each member; no generic guarantee from QE efermig's
relaxed0.01 electron cold-smearing fallback. All inputs finite.

For each band require |delta f| <= (L/sigma)(|delta epsilon|+|delta ef|)+2eta_f,
L=0.7541710171545021, eta_f=64*binary64 machine epsilon. Each actual evaluation
must independently satisfy eta_f against a high-precision analytic cold formula
including the source exponential tail clamp. Decimal evaluation is a bounded
pointwise check, not a universal libm theorem. The mathematical Lipschitz theorem
is exact for real unclipped f; tail clamp adds at most exp(-200)/sqrt(2pi) per
member. Rounding/evaluation allowances are separately stated and checked. The
worst-case occupation ceiling from the independently fixed energy budgets is
about1.429e-7; actual bandwise gates use the measured energy/ef deltas and are
usually much tighter. The independent density gate is never replaced by this
conditioning test. Degenerate phases/rotations cannot rescue wrong weighted
density. Native ef is NOT inferred by fitting its own occupations.

Use the stable QR block identity for gamma=A diag(f) A^dagger; compare all active
spinor coefficients in identical actual reciprocal bases, across both ranks,
without forming a large real-space density matrix. Gauge invariance concerns
same gamma (phases, rotations with co-transformed occupation matrix), not any
arbitrary rotation keeping unequal diagonal occupations fixed.

PASS denotes corresponding completed outer steps satisfying ALL gates.
Converged HSE additionally requires native EXX convergence, final dexx<1e-10 Ry
and schema convergence; inner convergence/exit0 do not suffice. Stop immediately
on mismatch/resource/refusal; partial trajectories are not qualified restart.
No matched-work performance or whole-SCF memory claim if outer counts differ.
