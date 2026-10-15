# Source dependency proof:316trials,176source capacity

Norm-conserving noncollinear CPU, one EXX/band/task group, Gamma/q1 only.

1. In native Modules/mp_exx, exxinit calls init_index_over_band(176,176), which
   fixes max_ibands/nibands176 and ibands1..176, all_start1/all_end176. Native
   vexx wrapper does not rebuild those tables at negrp1. A call m316 would not
   process its last140columns. Recalling the general initializer with m>nbnd
   would overrun its square pair_bands array. Neither route is admitted.
2. Native vexx_k accepts m158<=176: loops over cached176 and skips ibnd>m,
   allocates big_result(n*npol,m), and final writes im1..m. In one group no
   exchangebuffer circulation, remapping or result_sum communication occurs.
   Inner source bands remain176 with zero weights beyond146. The fixed .25HSE
   source/kernel is the same for two158calls; query columns carry no occupations.
3. calbec_nc explicitly accepts m<=size(becp%nc,3). Allocate capacity316; its
   GEMM and MPI sum slice1:m are valid. add_vuspsi_nc uses ps(nkb,npol,m) and
   loops/GEMM dimensionm; no wvfct%nbnd limit. The local spinor action also
   accepts explicitm. Native h_psi6 recalculates its own projector overlaps;
   becp is query workspace, not part of H[D0].
4. Source imports and native sum_band/exxinit/v_of_rho/set_vrs/newd occur ONCE.
   Native g2_convolution_all primes the fixed cache before capture; subsequent
   q1 calls return the cached factor. Streamed before/after snapshots include
   ALL active real EXXsource and occupations, actual kernel, rho/local/SOC data
   and qmaps. Equality is checked, not assumed from common physics parameters.
5. The modified driver only sizes trial/workspace/IO, applies two legal linear
   blocks, and captures fixed state. Bodies vexx/vexx_k/exxinit/ACE are unchanged.
   No source Hamiltonian arithmetic, density symmetrization rule, functional,
   cutoffs, native nbnd, smearing or ion geometry is modified.

This is one native state and one304column acquisition, not a cross-run splice.
The snapshots distinguish the native floating state from the mathematical D0;
they do not retroactively pass any previous byte-identity failure. Before/after
equality and independent controls complement source review; no claim about
material accuracy, whole omitted spectrum or nonlinear convergence follows.
