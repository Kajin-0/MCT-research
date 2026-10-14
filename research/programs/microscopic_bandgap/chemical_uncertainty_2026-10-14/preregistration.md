# Finite probe sensitivity and ONE k-sampling refinement

2026-10-14; clean parent b776a9e, original research session/branch. User authorizes
this new finite experiment; no repeat of the original Gamma-only pair.

## Step1: immediate retained-data analysis (before new native work)

Use original176band actual complex overlaps/energies only. Gaussian widths
W=[1,1.5,2,2.5,3]eV. Energy references: each member's native Fermi energy with
common offsets[-.5,-.25,0,.25,.5]eV; separately each member's own dominant
host-Gamma8 quartet mean (top4 trace weights). No absolute cross-species energy
zero comparison. Compute DeltaOmega as difference of within-member sector
centroid differences; require existing normalized Gaussian massfloor.05.
Keep omitted probability, same-rank host-projector envelope and conditional
arithmetic budget, all using joint denominator M-2epsilon-rho_round. Tail
|t phi_W|<=W/sqrt(e). Report the whole curve and envelope; no posthoc best width.
These variations are choices of spectral probe/reference, not physical errors
or a PBE k-convergence estimate. Primary original W2/Fermi value stays unchanged.

## Step2: one matched new native SCF pair

Smallest cubic-symmetric distinct uniform Gamma-containing mesh is unshifted
2x2x2 in conventional cubic reciprocal axes: eight points with coordinates0 or
1/2 modulo integers. Td signed permutations preserving tetrahedral bonds map
them to stars by number of half components, with sizes1,3,3,1. Both pure Hg4Te4
and ordered CdHg3Te4(at origin) preserve the same24 spatial Td operations.
Enable QE native crystal symmetrization (nosym=false) so representative density
is rotated/averaged correctly; merely listing four stars with nosym=true would
not integrate the full density. Native automatic mesh must independently match
expected stars/weights(1,3,3,1)/8 and preserve unique Gamma. Source/code/frame
and density symmetry gates must pass. This confines the result to the same
nonmagnetic Td branch; it cannot test a lower-symmetry/metastable solution.

Same8atom geometry,a6.46A,SG15FR NC,176bands144e,PBE+SOC,40/160Ry,FDsigma.001Ry,
SCF1e-9Ry,full-accuracy Davidson,beta.3,max100SCF,max_seconds500. Only mesh and
legitimate symmetry reduction change computational settings. Fresh independent
states/private outputs. No changes to stock, old HSE16/352, dirty DFT, old raw
data, existing failures, supervisors/sessions or historical blocked goal.

Budget assessment before launch: original actual native wall42.16/43.35s and
kernel peaks.511/.508GB. Four representative k states suggest~169/174s; a2.5x
cost margin~422/434s fits500 native softstop/600 hard wall, an estimate rather
than convergence guarantee. Conservative8x original measured memory <4.1GB
and wave output <1GB/pair, well within kernel12GiB and sampled14GiB aggregate.
Use actual ext4/quota, availableRAM>=16GiB at admission, disk>=24GiB at admission;
runtime4GiB RAM/10GiB disk floors,12GiB familyRSS/kernel,zero swap/tasks12,
600s/member,one family,typed kernel rank leases/strict output accounting.
No native retry on refusal/mismatch/time failure; Cd only if host fully passes.
All source/ELF/PP/input hashes frozen before the first new launch.

## Comparability / acceptance

Native weighted FD charge at ALL k: sum_k wk sum_b f((ef-ebk)/sigma)=144,
residual<=1e-8electron, each XMLoccupation agrees<=1e-9; sum weights1 for NC
spinors. SCF converged and JOBDONE, strict terminal owner evidence. Independently
locate native Gamma index by XML k vector; HDF xk/reciprocal normalization and
PW Miller space must match ORIGINAL physical host frame. No extra Gamma NSCF
is needed if native SCF mesh saves Gamma. No separate NSCF is pre-issued.

PRIMARY P6/P8 are the ORIGINAL qualified full40Ry Gamma-only host sectors,
transported through exact PW/Bloch mapping. Apply identical frames to both new
host and Cd. Check native new-host primitive-Gamma/Td labels and principal angles
to original frame; do not quietly replace the frame and call the observables
identical. Report optional new-host-frame result separately if useful.

Compare original and refined DeltaOmega(W2) for BOTH recipes: native own EF,
and native own dominant projected-Gamma8 quartet center. Report actual shifts
EF-minus-Gamma8-center; smoothed spectral shape depends on this reference even
though each ordering is invariant to global energy zero. No incompatible Fermi
alignment, BZ convergence from two grids, physical gap/x_c or HSE claim. Two-grid
change is numeric method/grid sensitivity; still unknown cutoff/finite-cell/
functional/ionic and eigenpair error. Stop after the finite measured result.
