# Preferred native construction and scientific contract

**PROVEN UNDER THE DECLARED NC-PBE MODEL:** at fixed scalar valence rho and
ionic/PP/cell state, the finite50Ry spinor operator is determined without an
occupied density matrix:

    H_m = T + v_ion,m + v_H[rho_m] + v_PBE[rho_m] + V_NL,SOC,m.

This is H of the accepted saved density, not a newly certified stationary
ground state. FD width.001Ry/electron288 are source metadata, not occupations
to be recomputed. The fixed cell, a6.46Angstrom, origins/spin axes, SG15 FR NC
potentials,50/200Ry and Gamma remain unchanged for both16atom arrangements.

## Exact routine chain — a NEW driver, not a restart

Source line numbers/hashes are in audit_result.json and additional_sources.json.
The following is a design outline, **not executable source or a build recipe**:

1. New program uses QE `mp_global:mp_startup()` and `environment_start` as a
   postprocessor, with one image/pool/band group/task group and CPU backend.
   Actual world size/rank MUST be1/0. This does not prove MPI singleton works.
   Explicitly initialize/check operational globals including report0,
   qcutz0, noGPU, no extra fields/corrections/plugins; do not rely on
   uninitialized SAVE/BSS values. Pin the actual linked archive/module closure.
2. Set only the staged input prefix/root. Call `read_file_new` with a fresh
   LOGICAL variable false. `read_xml_file` imports geometry, species, physical
   cutoffs,80^3 grids, noncolin/SOC/domag, chemical operations, k/nelec/smearing
   and352-band et/wg metadata. XML energies/cutoffs are Hartree; QE multiplies
   by e2=2 to Ry. Preserve original XML bytes; never reset nbnd/nelec to12.
   needwf is OUTPUT-overwritten to wf_collected, so do not accidentally reuse
   its returned true value to request wave initialization.
3. `post_xml_init`: readpp (staged pseudo_dir_cur first); pre_init determines
   nkb712; data_structure/allocate_fft/ggen/ggens/gshells rebuild rank-local
   descriptors; allocate_uspp sets internal is_spinorbit=lspinorb. read_scf
   imports rhoG, zeroing magnetization components for domag=false; rho_g2r
   reconstructs all4 local arrays. init_vloc/init_us_1/init_tab_beta/struc_fact/
   setlocal/set_rhoc/v_of_rho/newd construct the ionic+PBE+FR state. Retain
   ordinary initialization helpers such as init_tab_atwfc even though unused
   by the query; removing them would enlarge the equivalence proof.
4. Explicitly call `set_vrs(vrs,vltot,v%of_r,kedtau,v%kin_r,dfftp%nnr,nspin,
   doublegrid)`. It is absent from post_xml_init. No potential is inferred
   from own EF or copied from an incompatible FFT layout.
5. Compute npwx with n_plane_waves, call klist:init_igk ONCE, allocate ONLY
   vkb(npwx,nkb), g2kin(npwx), explicit trial/action buffers and becp(nkb,12).
   Do NOT call allocate_wfc_k (it allocates evc352), wfcinit, openfil,
   read_collected_wfc, electrons, non_scf, Fermi solve or punch. current_k=1;
   g2_kin and init_us_2 use actual k=0/native igk. Populate Phi by integer G.
6. Apply unchanged native h_psi(npwx,n,12,Phi,Y). Independently record native
   kinetic, vloc_psi_nc_acc, calbec+add_vuspsi components, local/rho/G/FFT
   snapshots and bare SOC coefficients as needed by acceptance. This is
   exactly12 full-H probe applications/member,24 total, not352 eigen-solves.
7. Checked packet write/flush/size/close, live authenticated one-rank final and
   explicit read-only postprocessor shutdown. Do NOT call PW stop_run: it
   creates/deletes restart/update/para files and invokes close_files. Check
   the actual HDF5 initialization/finalization macro path; the pinned
   environment_end uses `_HDF5` while initialization uses `__HDF5`.
   Explicitly close/finalize once if required; no hidden restart output.

## Physical conventions that cannot be dropped

- **Density transport:** read_rhog normally uses ig_l2g; it does not always
  read/check MillerIndices when both gamma_only flags agree. ggen's default
  global sort is source-conditioned rank-independent; do not assume this for
  memory=small or changed cutoff/cell/backend. Independently compare every
  native rhoG coefficient against the accepted HDF5 by integer Miller label
  BEFORE trusting vrs. Failure means stop, not zero-padding/remapping by index.
- **One-rank layout:** expected physicalN21595 and densityNg173631, but runtime
  descriptors/padding are NEW and must be captured. Old rank0/1 npwx10799/10796,
  offsets, FFT slabs and fixed two-packet headers/reader are invalid here.
  Gamma is a k point; `gamma_only` real-wave trick MUST remain false for SOC.
- **Normalization:** NC overlap is the identity in normalized plane waves,
  phi_G=e^(iG.r)/sqrt(Omega), and sum_Gspin|c|²=1. rhoG has charge Omega*rho0.
  QE FFTW3 forward is normalized, inverse unnormalized. Physical B and k,
  spinor ordering and explicit Theta(G):(down*(-G),-up*(-G)) must match.
- **PBE:** v_of_rho calls v_xc/gradcorr plus v_h. gradcorr uses reciprocal
  gradients, xc_gcx and fft_graddot divergence, actual density cutoffs/branches
  and Ry factors. It is NOT a pointwise LDA or bare n^(1/3) replacement.
  For these UPFs set_rhoc produces zero core arrays. A different NLCC, US/PAW,
  Hubbard, meta-GGA or magnetic source invalidates this minimal contract.
- **SOC/PP:** init_tab_beta uses4pi/sqrt(Omega) with radial Simpson/Bessel
  tables; init_us_2_acc adds actual (-i)^l and exp(-i(G+k).tau) phases.
  A nearby code comment says4pi/Omega and i^l; follow executed code, not that
  shorthand. init_us_1 forms dvan_so with fcoef/spinor angular algebra;
  newd_nous copies it to deeq_nc. Nonlocal action is beta D beta† on both
  spin components, not a scalar species offset. The ordinary h_psi m argument
  is independent of nbnd, with no occupied-wave dependency in this domain.
- **Gauge:** v_h sets HartreeG0=0. Same cell/composition/PP counts fix ionicG0;
  retain each PBE-XC mean. No isolated-boundary/electric/gate/QMMM/plugin terms.
  This is the periodic numerical model's energy gauge, not a vacuum band
  offset. If gauge cannot be checked, publish only scalar-shift invariants.

## Observable and strict limits

Keep exact original6 columns F, S=F†F, Pi=F S^-1F†, Q=1-Pi and sector
projectors Pi_a=F_a S_a^-1F_a†, d6=2,d8=4. No reorthogonalized/replaced probes:

    A_m=F†H_mF, B_m=QH_mF,
    Omega_m=Tr[(Pi6/2-Pi8/4)H_m], deltaOmega=Omega_sh-Omega_unsh.

The original Theta leakage1.65485e-6 is NOT silently ignored: include all6
explicit Theta images/member. Report QHP singular values and component-resolved
contrasts. Kinetic difference must cancel. Omega and QHP are invariant to
independent scalar shifts H_m+c_m I; full scalar A contrast needs the numerical
alignment just specified. Do not substitute the prior own-EF inverses.

Full Phi actions determine these static quantities without a352-band tail
closure in the declared50Ry Hilbert space. They do not determine QHQ or
A+B†(z-QHQ)^-1B, infinite-cutoff error, a local N2 vertex, random-alloy
self-energy/linewidth or physical mass/gap/x_c. No stationary spectral claim
is gained from accepted SCF flags alone. Six native member eigenpair checks,
if demanded separately, need12 EXTRA actions/pair and selected saved-wave
columns; full352 residuals are not certified by the primary24 actions.

The actual24/4 spatial groups constrain ionic/density/local fields. Do not
impose a host quartet on sharing or infer whole-H numerical covariance solely
from6 probes. Full crystal covariance requires a full-source/low-rank bound
or separately counted rotated-probe actions; no hidden additional queries.

Numerical response budget2meV remains prospective. For action error E_ma on a
sector, its contribution is bounded by

    e_ma <= ||E_ma S_a^-1/2||_F / sqrt(d_a).

This follows from the Frobenius norm sqrt(d_a) of F_a S_a^-1/2. Sum both
sectors and both configurations, plus independently bounded potential/transport
errors. Native actions/errors are Ry; multiply by13.605693122994 before an
eV budget (then1000 for meV). An a-priori allocation is1meV pair action/contraction error,0.5meV
potential reconstruction and0.5meV frame/input transport. It is NOT achieved
by Hermiticity/Theta1e-8 or agreement of two shared-code paths. Functional,
finite-cell, disorder/statistical and material uncertainty remain unknown.
