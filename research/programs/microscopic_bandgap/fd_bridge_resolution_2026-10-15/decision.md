# Joint symmetry is constructive; FD/HSE state remains unqualified

2026-10-15 06:44 UTC. Continuing after the REAL same-composition PBE environment
milestone, not stopping after its PASS. This package uses retained native C1
states, exact physicalG and the already constructed new152space. No native
HSE job, old failed host iteration or old byte-replay test was rerun.

**CALCULATED:** six leading principal residuals outside ALL176old eigenstates
are.978224--.999999; at1e-8 the full residual has136directions, so no exact
six-direction containment theorem is asserted. Six auxiliary kinetic Ritz
values40.1023--40.3301Ry, versus occupied146maximum8.36158Ry. Their high-G
(kinetic>40Ry) probabilities89.28--91.61%, and occupied-density weights below
7.44e-17, identify normalized high-G reference/occupied differences rather than
six established low-energy bands. Kinetic is not totalH or a spectral bound.

**CALCULATED:** an explicitly NEW reduced-matrix Td/Theta/translation twirl
has charge144.0000000000045e and covariance residual3.4191e-15. Its change from
the projected OLD trial is9.9010e-8operator norm and9.9080e-7trace norm. Original
density omission has a conservative9.1243e-7operator bound; projection charge
loss1.59e-12e. Indicative entropy2.77258872229108kB versus OLD2.77258872223978kB.
These are floating trial-state diagnostics, NOT nativeFD/HSE stationarity.
Tiny rounded nonpositive/above-one natural eigenvalues preclude blindly using
their logarithms; clipping is only reported entropy evaluation, not a source
or occupation acceptance. Original source/reference preservation FAILS stand.

**PROVEN:** the constrained energy+FDentropy derivative requires the actual
same-trial H[D], not merely an invariant source space. At finite sigma the
Hilbert-Schmidt FD map is globally1/(4sigma)-Lipschitz; the elementary two-
eigenbasis proof needs no gap. In-space stationarity residual, off-space
Hamiltonian coupling and a complement occupied-tail bound give an explicit
full-space density-error budget. The latter complement input is still needed;
the observed kinetic levels cannot substitute for it. No nonlinear contraction,
global SCF convergence, material state or zero-smearing limit is inferred.

**PASS, independent finite-matrix checks:** energy+entropy directional
derivatives within7.31e-10; exact two-eigenbasis FD identities within floating
roundoff on twelve noncommuting pairs; block-coupling/tail bound and a fully
symmetry-compatible unknown-copy counterexample pass. These are mathematics
checks, not physical validation. Established variational/compression literature
is linked in theory.md; no novelty claim is made.

**HSE NATIVE RELEASE: NO-GO at a precise input/implementation boundary.**
Retained directFock actions refer to a DIFFERENT source density. local0/local1
are vloc on6probes; they omit complete kinetic/nonlocal-SOC/HSE action on the
new state. Native source review confirms this distinction. The rank1missing
input is a complete SAME-D native H[D] action/readback with natural-source,
charge/entropy, independent direct-exchange solved-state controls, off-space
and FD/eigenstate residuals. minimum_input.md specifies it without silently
turning compression auxiliaries into solved bands or assigning occupations.
No such integrated bridge is currently verified; no resource-safe native
release follows from its estimated export size or prior kernel timing.

The autonomous assignment has therefore produced real chemical data, a
discriminating spectral decomposition and a quantitative state-bridge result,
then reached a demonstrable missing-input boundary. No PBE-grid churn, defective
host rerun, arbitrary density relabeling, empirical gap fit, HSE convergence or
physicalxc. Stock/dirtyDFT/old failure evidence and all other sessions remain
untouched. The historical blockedgoal is unchanged.
