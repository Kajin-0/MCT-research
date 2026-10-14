# Physics-forward recommendation — future experiment only

Recommend the **smallest matched 8-atom HSE+SOC Gamma/q1 first-ACE timing and
resource pilot**, not another PBE composition or full HSE SCF. The measured
same-cutoff k2→k3 W2 sensitivity is only −1.160 meV; functional and finite-cell
errors remain unconstrained. A further x=.5 PBE spectrum would add composition
information and new symmetry effects but would not test functional adequacy.

The future pilot keeps the same Hg/Cd cell, origin, SG15 FR NC potentials,
176 spinor bands/144 electrons, FD0.001Ry,50/200Ry. Use HSE fraction.25,
screening.106Bohr^-1 and explicit Fock cutoff200Ry. Gamma/q1 sampling is a
separate coarse k/q approximation, not the accepted k3 quadrature. Avoid the
48-band cold-smearing private solver and the old16atom352band target entirely.
No pilot is launched or admitted by this recommendation.

**SOURCE-CONDITIONED:** pinned QE7.5 needs a complex spinor EXX buffer even
at Gamma. If its real-space descriptor is60^3, one unique k+q buffer costs
1,216,512,000B; the xi-only source upper bound is60,977,664B. Adding the
current measured PBE kernel peak gives2,229,608,960B. This subtotal is NOT a
complete RSS or native FFT certificate; other EXX/backend/MPI workspaces,
plans and output require actual qualification. No streaming memory gain is
inferred or needed for this small proposed domain.

**MEASURED versus HYPOTHESIS:** the old actual2atom48band HSE timing gives
25.19s per whole ACE rebuild; that run was unconverged and used different
cutoffs/cold occupations. Scaling trial/source band pairs and FFT volume,
plus one-quarter of the measured current four-k PBE startup time, gives
rough first-ACE costs162–185s host and158–180s Cd, total320–365s. Treat
144–176 contributing source bands as a heuristic range, not an error bound.
Changing SCF histories, FFT/kernel work and conditioning can violate it.
The current PBE measurements do not certify HSE completion below600s.

The discriminating pilot should capture **one complete native first ACE** for
each species, with direct action, Gram, contracted/Fock energy, actual source
Gamma spinors, charge, descriptor, stage timings and whole-family peaks. A
projected chemical exchange response requires independently covered action
and the same physical host frame; scalar Fock energy alone is insufficient.
Even a successful firstACE is not a self-consistent HSE spectrum or physical
gap. No arbitrary occupation tolerance, gap fit or empirical bowing enters.

Before any launch, separately freeze and verify the176-band observer/stop path
without altering exchange arithmetic, qualify the actual Gamma/q1 state/FFT/
disk/RAM/typed-rank domain and obtain explicit pilot authorization. Preserve
the existing12GiB/swap0/tasks12/600s/member,4GiB host/10GiB disk floors and
sampled14GiB local output contract. Stop on first mismatch/refusal; do not
continue into full SCF, retry, queue or reinterpret partial data as success.

[next_experiment.json](next_experiment.json) contains exact source-conditioned
bytes, measured anchors, assumptions and acceptance boundaries. The remaining
minimum HSE information is actual8atom firstACE timing/wholepeak/descriptor;
analytical subtotals cannot replace it. Material x_c remains OPEN.
