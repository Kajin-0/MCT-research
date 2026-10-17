# R07 Stage 1 exploratory xCd=.125 PBE/VCA acquisition — 2026-10-17

**CALCULATED: one new stock-QE primitive PBE+SOC fully relativistic xCd=0.125 virtual crystal SCF, completed once and terminal-PASS.** The existing 16-atom ordered CdHg7Te8 PBE+SOC spectrum was reused without rerunning it. **No HSE, x=.25, R08, random-alloy ensemble or added spending.**

## Exact method and execution

- The separately authorized run used a **two-atom** primitive Hg0.875Cd0.125Te VCA model, 50/200 Ry plane-wave/charge cutoffs, 46 spinor bands, unshifted 2x2x2 sampling (Γ1/8, L4/8, X3/8), PBE+SOC, Fermi–Dirac smearing 0.001 Ry, fixed a=6.46 Å and unchanged fully relativistic SG15 Te pseudo.
- The cation virtual pseudo **VCA_HgCd_x0125.UPF** has SHA256 `4388cd23a07772037b6c4fdf7db72690478e6ae2e163025cfba1a6312dff11b4`, identical to the previously source-qualified HSE VCA file but used here under PBE. It is a specified coherent ionic operator, not a proven screened-disorder average or a test of norm conservation for the interpolated reference.
- Bounded fresh owner reuses the accepted PBE16 storage/cgroup/nonce/rank/terminal logic: 12 GiB, swap zero, 12 tasks, 900-second wall, 4 GiB system-RAM and 10 GiB disk reserves. Fresh isolated non-QE dry run passed before native release. Native owner elapsed **10.3023 seconds**; native QE exit 0 and SCF XML true, max kernel memory **145489920 B**, sampled RSS **226738176 B**, two rank exits true, output max **2785280 B**, systemd inactive/success. No retries. Raw wavefunctions, XML and scope records in `/home/User/opencode_workspace/DFT/.local/r07s1_20261017/primitive`.
- There was no retroactive qualification of Stage 0 strict high-energy gate; Stage 1 is a **separately authorized exploratory acquisition**.

## Direct first new physics: coherent versus periodically ordered Cd

The same original physical PBE Γ-sector HgTe reference frames are transported into the VCA primitive Γ plane-wave space and compared to the previously qualified ordered 16-atom Γ spectrum. The native VCA Γ6 bands31–32 and Γ8 bands35–38 pass Td Γ6/Γ8 subspace classification; fixed-reference captured weights are **0.99980813 Γ6** and **0.99984785 Γ8**, with negligible within-multiplet splitting. The ordered x=.125 Γ6/Γ8 bands were independently accepted in prior `chemical_pbe16_p2_2026-10-15/multiplet_result.json`.

| Observable (eV) | VCA x=.125 | Ordered x=.125 | Ordered − VCA |
|---|---:|---:|---:|
| Sharp tracked Γ6−Γ8 eigen-multiplet separation | −0.870480748 | −0.875353203 | **−0.004872454** |
| Fixed-frame Gaussian centroid ordering W=2eV, each own EF | −0.870493391 (from matched contrast) | −0.842933008 | **+0.027560383** |
| Fixed-frame scalar inverse-resolvent ordering η=.05eV, each own EF | −0.87058515 (from matched contrast) | −0.90933123 | **−0.038746081** |

Supplementary Gaussian ordered−VCA shifts for W=1,1.5,2,2.5,3 eV respectively: **+20.8713, +25.1743, +27.5604, +28.0361, +27.5841 meV**. Scalar inverse-resolvent shifts for eta=.025,.05,.1 eV: **−38.9070, −38.7461, −38.1113 meV**. These are *different* spectral observables. Contrasting signs are not an inconsistency in the eigensolver and MUST NOT be combined into a single static disorder mass.

## Explicit uncertainty boundaries

The retained-spectrum fixed-frame missing weights at VCA Γ6/Γ8 are **3.72e−5/9.01e−5**, and ordered Γ6/Γ8 are **5.83e−4/6.35e−4**. A separately recomputed **positive spectral tail-only** conservative bound for the W=2eV Gaussian contrast is about **±2.2971 meV** (conditional interval **[+25.2633,+29.8575] meV**). For scalar inverse-resolvent eta=.05eV the tail-only bound is **±10.3809 meV** (conditional interval **[−49.1270,−28.3652] meV**). These bounds **do not include** finite basis/SCF eigenpair error, fixed-frame projector uncertainty, pseudopotential transferability, disorder configuration statistics, method dependence, chemical relaxation, temperature and functional errors; they are not total numeric/material uncertainty certificates. No independent 2 meV-level Stage1 eigenpair convergence envelope was established.

The VCA Γ projection uses an exactly embedded even-G primitive sector. The Gaussian and scalar inverse-resolvent statistics are anchored to **each specimen's own Fermi reference** and are *not* common-absolute-energy matrix self-energies or material quasiparticle poles. The historical Gaussian/inverse ordered reference packets retain their own conditional bounds; this record does not replace them with the tail-only comparison. No matrix 6x6 causal inverse has been calculated for the new VCA.

## Stop decision

**Exploratory scientific outcome: a measurable model-dependent ordered−VCA contrast at x=.125, with method-specific sign and magnitude.** A real, matched first-principles comparison is now available; VCA versus one periodically ordered Cd specimen is not a random alloy statistical correction, does not fix HSE coherent Γ symmetry failure, cannot locate physical xc, and cannot be imported into HSE as a quantitative disorder shift. **Stage 1 acquisition COMPLETE; strict full physical acceptance NOT established.** Stage 2 x=.25 NOT AUTHORIZED. No new native jobs or retries.
