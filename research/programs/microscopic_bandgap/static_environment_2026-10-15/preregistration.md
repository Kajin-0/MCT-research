# Independent static environment acquisition — 2026-10-15

Continue after strict HSEappend refusal c16f9af, without rerunning that job.
Exactly ONE sequential unshared then shared native PBE16operator query pair;
no SCF or new k grid. Use accepted x=.25Cd(0,7)/(0,1) final saved charges,
copied to NEW private roots; old state remains immutable. Same SG15FRNC,PBE+SOC,
16atoms/352capacity/288e,50/200Ry,Gamma,FD.001,cell/ions/spin conventions.

Question: what is the STATIC fixed-host Gamma6-8 trace of H at each actual saved
SCFcharge? This separates a measured static projection from a finite-eta
inverse kernel. It does not identify a complete localN2tensor/randomalloygap.
Use the accepted16atom50Ry original physical reference without renormalization
or index overlap. Import its complex six spinors with physical MillerG and B.

Private source: pristine run_pwscf calls init_run, then a new diagnostic and
returns BEFORE electrons/non_scf/punch. startingpot=file and startingwfc=file
read COPIES of accepted save metadata/charge/waves. Native potinit/read_scf->
rho_g2r/v_of_rho/set_vrs/newd construct the saved-charge Hamiltonian; no sum_band
or occupations update. Require actual full rhoG to match saved HDF5 charge
bitwise by physicalG and native stdout to certify file read/no fallback.
Import six physical probes AND six exact Theta-image control columns;
init_us_2/g2_kin then native h_psi, with independent
kinetic+vloc_psi_nc+calbec/add_vuspsi components. No EXX modification/call.

Frozen scientific gates: physical G/B/k/cell, NCGram and complex probe bytes,
charge<=1e-8e, rhoGreadback exact, finitearrays, fullH/component/Hermiticity and
Theta relative1e-8; native chemical group metadata must match retained cell.
No forced shared quartet. Input/save/source/ELF/PP/backend hashes pinned before
launch; stock routines except diagnostic run driver unchanged. Each unit once,
no retry; shared launched only if unshared passes and cleanup is verified.

Hard12GiB/swap0/tasks12/600s/member, one local2rankfamily, host4GiB/disk10GiB,
sampled14GiB aggregate including copies/build, short fresh socket<=107bytes,
live typed rank/ELF/owner/pidfd/terminal gates unchanged. Bounds cover small
native output; resource forecasts are not continuous guarantees. Original
hostwide exclusion/private-network claims stay unpassed. No unrelated scratch.

Report full static6matrix and component differences, trace mass/common with
energy-reference caveat, physical-probe leakage, and finite-eta minus STATIC
trace. The latter also contains any old SCFeigenpair/final-charge difference;
do not label it a pure exact Feshbach self-energy without an eigenpair bound.
Comparing native action with retained spectral firstmoment does not supply
missing eigenpair/completeness certificates. No fitted bowing/HSE/physicalxc.
