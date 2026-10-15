# Focused verification and scientific status

- CALCULATED: three private QE objects compile/link; original direct/ACE kernels,
  occupation/SCF equations and matcalc arithmetic unchanged. Frozen hashes pass.
- CALCULATED: one real two-rank host;8sources, original finite-acquisition gates
  PASS, final HDF5 bit-exact, XML/export/FD charge checks and clean kernel owner.
  Native convergence=false. Cd unit not loaded, no native Cd files or packets.
- CALCULATED: independent scalar Fock/reference contractions, Decimal charge and
  old-xi/new-Phi bridge on all8sources; max cross-energy residual8.53e-14Ry.
- CALCULATED: G/spin overlaps before squaring, gauge/sector-unitary checks and
  positive-tail Gaussian probes at5widths. Conditional filtered-variance estimates
  do not control unbounded moments or material uncertainty.
- PROVEN/CALCULATED: exact antiunitary compression identity independently checked
  on a nonclosed synthetic reference AND native scalar witness; error2.89e-15.
  The first invariant-reference shortcut REFUSED; its log and correction retained.
- CALCULATED: actual first ACE -xi xi† source action reconstructs5.44e-16; its
  antiunitary commutator is nonzero. No direct off-span equality claim.
- CALCULATED: native density Fourier reconstruction, charge sums and positive
  periodic window partition; local spin density is zero while nonlocal D failsTR.
  These are pseudovalence/grid observables, not unique atomic/Bader charges.
- PROVEN UNDER ASSUMPTIONS: exchange residual decomposition/bounds; exact rational
  counterexample rejects the stronger positivity inference.3tiny analytic checks;
  no synthetic material validation or novelty claim.
- CALCULATED: exact preservation/owned closure/output accounting and Python/JSON
  checks pass. Original host-wide proof absent, sampled-output caveat retained.

No extra MPI/SCF tests, native retry, stock modification, empirical fit, matched
full-HSE result, restart certification, whole-SCF RAM improvement or physicalx_c.
Deferred analyze_pair.py is unexecuted because no new Cd run exists. It is not
used to claim a matched chemical result.

Git whitespace check excludes raw native pw.out and the exact upstream-source
patch context; their original whitespace is deliberately preserved and hashed.
Derived CSV line endings are LF; edited code/docs pass the focused check.
