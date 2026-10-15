# Actual spectral observables and bounded dispersion

For each native source, amplitudes C_an=<a|phi_n> are summed across both ranks
using actual physical G and spin labels BEFORE absolute squares. The immutable
physical host projectors have dimensions2/4; no retained-weight renormalization
or naive array-index overlap is used. Positive branch weights are
w_(alpha,n)=sum_(a in alpha)|C_an|²/d_alpha. They define a subprobability measure
with measured omitted mass r=1-sum_n w_n, subject to the stated floating/frame
conditions. Each source eigenproblem is the previous frozen ACE plus converged
inner density, not exactly the just-rebuilt source Fock operator. This distinction
persists even when the native outer tolerance passes; report both residuals.

At reference mu (independently reconstructed FD root; separately native-XML
checked at final source) let t=E-mu, g=exp(-t²/(2W²)), widths1/1.5/2/2.5/3eV.
The centroid c=N/M has M=sum wg and N=sum wtg. The same previous positive-tail
bound is retained: |delta c| <=delta(B+|c|)/(M-delta), B=W/sqrt(e), with delta the
missing probability plus conditional frame/arithmetic budget. A sharper original
positive-tail denominator is used in spectral_evolution.py (only frame/roundoff
may reduce the retained M). These are bounds on a bounded probe, not material
or k/q/outer-convergence errors. Physical projectors and reference tracking are
assumptions distinct from native coefficient arithmetic.

**PROVEN UNDER ASSUMPTIONS:** with q=sum wt²g/M and v=q-c², the bounded second
moment obeys

    |delta q| <=delta(2W²/e+|q|)/(M-delta),
    |delta v| <= |delta q|+|delta c|(2|c|+|delta c|).

Here max |tg|=W/sqrt(e), max |t²g|=2W²/e; positivity supplies the mass bound.
Variance is nonnegative by Cauchy-Schwarz for the positive filtered measure.
The physical energy-origin shift cancels when mu shifts with E. Sector trace
weights are invariant under unitary rotations inside each original projector.
These elementary estimates hold inside a continuum at finite W and require no
support-free eliminated domain. The retained finite-cell spectrum is not itself
proof of a material continuum limit or correct many-body self-energy.

Also report the d_alpha bands of largest branch trace weight: their captured
weight, energy spread, separation from other retained eigenvalues and competing
weight gap. Call these **dominant-character clusters**, not an automatic sharp
signed Gamma gap. Their identity may fail with extra copies, mixed/multiple
peaks or symmetry splitting. Omitted high states and finite eigensolver residuals
are separate from the displayed cluster spreads. No spectral-peak crossing,
topological boundary, optical edge or random-alloyx_c follows from this selection.

**Negative result retained:** probability-tail control does NOT bound unweighted
first/second moments. Put omitted weight r at arbitrary energy L: its first and
second contributions are rL and rL². Thus filtered dispersion is not the exact
unbounded P H Q H P coupling norm. Full native H acting on the physical6 reference
columns, or independently bounded high-energy moments, would be needed for that
operator quantity. New notation for a filtered variance is not a novelty claim.
Observed Cd broadening here is spectral-character redistribution in an ordered
cell, not an intrinsic random-disorder linewidth.
