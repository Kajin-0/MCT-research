# SAME-D complete native HSE host action — 2026-10-15

Startingb799d28. ONE new fixed-trial HOST acquisition, not SCF, ACE, restart or
Cd. Retain8atom/176source capacity/144e/50-200-200Ry/SG15FR/a6.46/Gamma-q1/
HSE.25,.106Bohr^-1/FDsigma.001Ry. No old job/source/failure modified. Native
direct Fock arithmetic unchanged. Never interpret six auxiliary directions as
solved low-energy bands. Only source natural orbitals carry occupation.

Construct the trial from spectral projectors of the retained jointly twirled
152matrix D: upper cluster(>.75)rank142, middle(.25,.75)rank4, lowcluster rank6.
Define D_trial=P_upper+.5P_middle. This is an explicit NEW nonmagnetic ensemble,
NOT FD of HSE or a preservation of the old source. Trace144,0<=D<=1 and entropy
4log2 are algebraic; qualify actual Gram, charge, all24Td,Theta,translations
to1e-8 independently. Trial weights1/.5 derive from the measured native
142full+fourhalf spectrum and symmetry-separated projectors; no fictitious
orbital eigenvalues or adjustable occupations are inserted. The complement
within152has zero trial weight. A strict0<D<I/logit claim is excluded.

Native source review: `sum_band` unconditionally calls `weights`; use the
existing `tfixed_occ/f_inp` path ONLY during trial density construction, restoring
it immediately. No fake energy is used to force FDweights. et/ef/eband from
this diagnostic fixed-occupation call are NOT eigenstate or energy evidence.
Use native sum_band -> exxinit(direct) -> v_of_rho(HSE active) -> set_vrs ->
newd. Capture source wg/phi, real/reciprocal rho and grids. Independently
reconstruct density via physicalG/FFT; sym_rho must not hide a failed source.

Return T,Vlocal,Vnonlocal_SOC and DIRECT Fock on joint152 plus ORIGINAL6frame
and itsTheta images (164trials). Native h_psi(ace=false) independently checks
complete component sum on the original6. No oldACE action. Native call m<=176.
Capture all full vectors for offspace residuals and byte source readback; actual
Gamma/q1 maps, physicalG/B,60^3FFT, source146,HSEparameters must agree. Source,
charge1e-8e, Gram/action/Hermiticity/TR/crystal1e-8 and owner/resource gates are
frozen BEFORE launch. FDstationarity is an OUTCOME, not an admission fiction.
Report projected FD charge root, entropy, density mismatch, commutator and full
eigenstate/offspace residual. Full-space upper bound requires its own complement
tail; report if uninformative. A full-space commutator lower bound can instead
prove a trial is not stationary without that tail. No SCF convergence claim.

Admission: separately versioned short root/socket<=107bytes, exact source/input/
PP/ELF/backend/reference hashes, known-family exclusion/lock, live rank leases,
12GiB/swap0/tasks12,600s hard wall, host4GiB/disk10GiB floors, sampled14GiB
owned aggregate including fixed prepared artifacts, one local2rankfamily.
No retry after an admitted failed unit. Prior real direct rate~.875s/trial,
170actions forecasts~149s; it is not a bound. Explicit allocation/output inventory
and conservative forecast must qualify before launch. Owner may abort on any
cap, mismatch or instability. Hostwide exclusion/private-network claim unpassed.

After native capture, independently verify component sum/readback/normalization/
symmetry. A failed scientific gate stays FAILED; retain numeric evidence without
relaxing thresholds. A nonzero FDresidual may be a successful diagnostic while
blocking SCF release. Commit/push qualified facts, then continue a distinct
causal/identifiability question; no empirical xc or arbitrary bowing fit.
