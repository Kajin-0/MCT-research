# Minimum additional physical input and N3 feasibility

## HSE takes priority

The same-density native query f249885 removed the missing complete H[D0]
barrier. It did NOT solve the FD state: measured density mismatch .0040404op,
whole-space Fermi-quartet Ritz residual .02625424Ry, and conditional global FD
error lower bound 1.2211e-7. The mathematically minimal full action-completion
space has dimension 304, with 152 new directions; both cubic and Theta leakage
are below 2.1e-11. Its unknown lower-right H block is the next input.

Query only H[D0] on the 152 new residual directions. Combining it with known
H[D0]Q requires a NEW typed profile and identical actual source, weights, G/k/q,
FFT/kernel, local/Hartree/XC/SOC and trial basis checks. It is not SCF restart or
old byte-replay acceptance. The present one native acquisition was used once;
no append query is admitted or queued by this read-only document. Measured
170 direct actions cost 185.3s and 4.25GB kernel peak. This is a useful forecast
for a bounded future query, not a theorem about new output/RAM/runtime or
subsequent self-consistency. All 12GiB/swap0/tasks12/600s, host4GiB/disk10GiB,
sampled14GiB, fresh-root/socket<=107byte and live-owner gates remain required.

At fixed D0 the appended matrix permits a real new Galerkin FD calculation.
It still needs full-space residual/tail checks, then a rebuilt H at any new D,
before HSE eigenstates or outer convergence can be released. Symmetry and
charge alone were already falsified as stationarity certificates.

## Static matrix versus spectral derivative

The accepted PBE inverse kernel mixes its static moment and virtual coupling.
A minimal direct static measurement is H on six orthonormal physical Gamma
probes for each of the two retained SCF densities, including all kinetic,
local, nonlocal SOC components. Native wave/charge frames must be read back at
those densities; a different prepared PBE or HSE state does not substitute.
Twelve actions would expose the static 6x6 contrast and energy-gauge-invariant
Gamma6-8 trace. Absolute common-channel shifts still require potential alignment.
Cost is likely dominated by native initialization/readback, not a new SCF;
no executable or resource certificate is currently frozen for that acquisition.
Static P H P is a projected operator, still not a full directional local N2
response nor a random-alloy covariance. Prior non-identifiability results stand.

For the finite-eta energy derivative alone, an independently justified omitted
support threshold >.20660eV (own EF for both cells), with eigenpair/frame error
accounting, would close the conditional sign uncertainty. Exact lowest-352
ordering would suffice by a wide margin, but has not been proved from native
printed bands. Additional precision of the same uncertified partial data does
not supply this missing premise. No extra native job is proposed solely to
reprint the same bands.

## One N3-bearing cell is feasible as a proposal, not yet admitted

Same 16-cell cation indices (0,1,2), Cd3Hg5Te8, x=.375. Fixed positions/lattice
and isovalent Hg/Cd valence imply 288 electrons and the existing 352 spinor-band
capacity. Retain 50/200Ry, SG15 fully relativistic NC, Gamma, FD sigma .001Ry,
conv_thr1e-9 and the accepted host physical projector frame. Te environments:
N=(3,2,2,2,1,1,1,0); histogram (N0,...,N4)=(1,3,3,1,0). Actual chemical point
group order 6; Kramers doublets, not a forced cubic Gamma8 quartet, are relevant.
This is a geometry proposal only; no native symmetry or convergence claim.

The actual two-Cd16 runs converged in 365.3/374.7s with kernel peaks about
2.095GB and about .25GB saved output/member. Same cell/cutoff/band/storage sizes
are favorable under 12GiB and 14GiB, but lower symmetry and different chemical
SCF conditioning do not guarantee convergence within 600s. A NEW exact input,
source/ELF/PP pin, fresh root/short socket, rank/query owner and real resource
admission are indispensable. Existing measured headroom is a forecast, not
that admission. No new service or work queue was made.

One such cell versus the accepted pure 16-host provides new ordered-cell x=.375
chemistry. It changes both concentration and environment. A same-x N3-free
triple, for example (0,1,7), is a second NEW SCF, not an existing control.
Thus isolating a same-composition N3-bearing contrast requires two new cells.
Even that contrast also changes longer-range ordering and does not isolate a
universal local triplet coefficient without a fixed-local-response theorem.

Under the hypothetical complete fixed-local operator assumptions only, adding
H0+3H1+3H2+H3 to the four independent endpoint/H1/H2 count rows closes the five
H_N linear problem. Present projected spectra do not supply those full rows;
global-background, gauge, strain, induced charge and directional bond response
cannot be silently dropped. No N3 random-alloy coefficient or physical x_c can
be reconstructed from the present finite ordered cells.
