# Completed k4/q4 control: converged SCF, conditional HgTe host reference

2026-10-17; post-run qualification from53b638a. **CALCULATED: conventional
numerical SCF PASS; frozen1e-8 full-density symmetry FAIL.** Retain a useful
conditional primitive host reference, not a strictly certified nonmagnetic
state or physical alloy x_c. No new native job, restart, direct Fock query,
postprocessor, source edit or Cd run occurred during this qualification.

The [prelaunch protocol](preregistration.md), [RUNNING checkpoint](active_checkpoint.json),
prefixes and original verification remain immutable historical records. This
decision supersedes their RUNNING status, not their contents. Terminal evidence
and rerunnable read-only code are in [final_qualification](final_qualification/verification.json).

## Actual completed control

| Measured native quantity | Result |
|---|---:|
| Source builds |6|
| Outer dexx series, Ry |8.3406e-4,1.66e-5,3.9e-7,1.0e-8,2.3e-10|
| EXX reached / XML convergence |yes /true|
| Final inner energy-error estimate, Ry |3.27448395e-10|
| Final total free energy, Ry |−484.161000956768|
| Displayed Fock energy(half), Ry |−8.96862706|
| Occupation charge error / saved rhoG error, e |+1.3841e-11 /+1.3856e-11|
| FD formula maximum error |2.78e-14|
| Reconstructed/native −TS, Ry |−4.33216991824e-5 /same|
| Fermi energy, eV |8.954506459252|
| OS wall / native termination |6622.739s /2026-10-17 03:24:51UTC|
| Kernel memory peak / swap |6,225,952,768B /0|
| Sampled family RSS peak(shared-page overcount) |6,289,747,968B|
| Sampled host available / disk minima |23.674GB /49.293GB|
| Sampled owned-output maximum / tasks |65.069MB /7|

Same frozen stockQE7.5/ACE,SG15 FR NC,6.46Å primitive2atom,36e/44spinors,
50/200/Fock200Ry,HSE(.25,.106),FD.001Ry,SOC. Native8irreducible fibers,
64distinct q-source coordinates,Γ weight1/64 and24crystal operations are
verified. The **effective output XML** has Fock200Ry; its input placeholder0
is not read as the effective cutoff. FD width.001Ry=.0136057eV is a finite
electronic-occupation regularization, not a demonstrated zero-smearing limit.

The original invocation8dee58502fd048e4bf30a09bd9053a1f exited0 and saved all,
without restart, EXIT request, resource refusal or observed OOM/limit events.
Original launcher/rank/observer identities and both cgroups are gone; units
are unloaded. Terminal manager evidence was captured before unload. The
12GiB/swap0/tasks12/24h bounds held; actual termination was convergence.
Thirty-second floor/output sampling is not a hard quota or continuous external-
writer guarantee. Stderr preserves native underflow/denormal notes.

## Γ labels and signed ordering

True G-labelled overlaps embed the accepted e90/f120 physical Γ6/Γ8 spinors
into e50 with identical cell/origin/axes/UPFs. The reference is **not** imported
as an e50 stationary state, and its discarded high-G probability is not
renormalized away:2.0382e-6 perΓ6 probe,1.2778e-7 perΓ8 probe. Projection and
actual24-operation spinor characters, rather than indices alone, identify:

| Native quantity | Γ6-like doublet | Γ8-like quartet |
|---|---:|---:|
| Bands |33–34|35–38|
| Energy center, eV(internal potential zero) |8.664919954402|8.954506459224|
| Energy spread, eV |2.16e-12|7.75e-9|
| Original frame weight per native state |≥.9999978843|≥.9999998564|
| Maximum double-group character error |1.45e-13|6.68e-15|
| Maximum Td amplitude span leakage |5.13e-7|1.75e-7|
| Θ amplitude span leakage |3.54e-7|1.48e-7|

The useful **conditional signed Γ level ordering** is therefore
**EΓ6−EΓ8≈−0.289586504823eV**, with nominal half-ordering
**−0.144793252411eV** under a valid Kane-model identification. All doublet-
quartet differences span[−.289586508700,−.289586500945]eV. This range reflects
only retained level splitting, not SCF/eigenpair/material error. Character
agreement does not override amplitude leakage above1e-8. The labels are
excellent approximate irreps, not exact certified irreps of the saved state.
Negative Γ ordering in inverted HgTe is not a positive fundamental/optical gap.

## Full density: small defects, but strict acceptance still FAILS

Γ source Gram defect is2.81e-15. Keeping **all44states and88weighted QR
columns**, over the entire5466-dimensional native spinor basis, gives:

- ||DΓ−ΘDΓΘ⁻¹||op = **3.615172826e-7**, Frobenius8.710744260e-7.
- Compressed witness4.0554e-11, conservative Frobenius upper2.1690e-6.
- Independent residual-block Frobenius agrees within1.7e-16; matrix-free
  extremal Rayleigh/eigenvector checks agree around1e-15.
- Maximum actual24-operation Γ density Td defect **5.196448527e-7**.

These IEEE measurements **FAIL frozen1e-8**. Neither the small compressed
witness nor Γ weight1/64 is used to force PASS. Γ8 occupations are
.5000000717,.5000000717,.4999999293,.4999999293; their1.4246e-7 spread
is retained. No averaging, source symmetrization or relaxed old gate occurs.

OnlyΓ,L,X(nativefibers1,3,7) have actually saved−k partners modulo G. Their
Θ norms are3.6152e-7,2.8340e-7,3.1618e-7. Each other native little group is
tested without imposing Kramers degeneracy at generic k. Five−k partners are
missing. **No64native-fiber Θ/Td certificate or manufactured unique-star
extension.** Exact algebra and finite-band limitations are in the
[scientific report](final_qualification/scientific_result.md).

## Scientific inference and next physical input

The same-e50/FD k2 trajectory had Γ density-Θ norm.9037 and315meV quartet
splitting; this run converged rapidly with3.6e-7 and7.75neV respectively.
This supports the quadrature/near-Fermi feedback hypothesis for the tested
trajectories. It does not prove unique causality, a global fixed-point theorem
or a universal ACE fault/cure: k andq changed together, and atomic+random
initial states are not byte-identical. Old k2/HSE8 failures remain rejected.

The old e90/cold/f120 ordering−.289770113778eV differs by+.183609meV.
That is a cross-model observation, not a cutoff/smearing/functional error bar.
Rebuilt DIRECT full-H eigenpair/occupied residuals and a quantitative operator
error bound are unavailable; dexx, quartet splitting and saved ACE cannot
replace them. Conventional numerical SCF is accepted in its stated domain
without pretending a universal stationarity/material certificate.

**Next indispensable input:** a separately authorized, sampling-compatible
self-consistent Cd-bearing HSE state **and its matched host**, physical frame
transport and explicit state tests. This primitive reference cannot be spliced
onto old8atomΓ/q1 Cd data. A direct8atom k4/q4 copy is **resource-NO-GO under
12GiB**: retained native60³/176 extents imply **77,856,768,000B(72.51GiB)
nominal source buffer alone**. Primitive4³ folds to16conventional fibers;
even a hypothetical supported16-source layout needs19.46GB before other
arrays. This folding lower-cost comparison is **not an admitted stock16-source
input**. See [sampling/cost evidence](final_qualification/next_sampling_cost.json).
No Cd run, cap increase, new streamer/owner or infrastructure phase is admitted.
Random-alloy x_c still requires composition/configuration and observable-
eligibility information. No fitted bowing or endpoint x_c is supplied.

All822protected pins,76historical originals,old failures,stock/backends,
DFTdirty bytes and historical BLOCKED goal are unchanged. Raw HDF5 remains
private at manifest paths; Git carries hashes,stdout/XML,analysis and resource
records, not a public raw export. **STOP after this completed qualification.**
