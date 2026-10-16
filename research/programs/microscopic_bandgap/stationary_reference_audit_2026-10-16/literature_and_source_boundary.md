# Primary-source comparison — no novelty claim

Accessed 2026-10-16. This is a native-reference qualification, not a new theory
of HSE, SCF, cold smearing, ACE, disorder or band inversion.

| Primary source | Established content used here | What it does NOT establish for these files |
|---|---|---|
| [QE7.5 open_grid.f90](https://raw.githubusercontent.com/QEF/q-e/qe-7.5/PP/src/open_grid.f90), especially restoration/punch around215–223 | Expands saved wavefunctions and restores EXX settings before export | New SCF convergence or full-H stationarity of the exported state |
| [QE7.5 wgauss.f90](https://raw.githubusercontent.com/QEF/q-e/qe-7.5/Modules/wgauss.f90), branches n=-1,-99; [input specification](https://www.quantum-espresso.org/Doc/INPUT_PW.html) | Distinct cold and FD occupation functions; numerical smearing conventions | A cold-SCF solution being FD at the same μ, a physical temperature or controlled zero-T extrapolation |
| [Marzari et al.1999 author manuscript](https://arxiv.org/abs/cond-mat/9903147), PRL82,3296 | Cold-smearing method is established numerical electronic-structure practice | Automatic microscopic HgCdTe material accuracy or FD entropy |
| [QE7.5 electrons.f90](https://raw.githubusercontent.com/QEF/q-e/qe-7.5/PW/src/electrons.f90), ~255–330 | Rebuild exchange, evaluate scalar dexx, take abs if negative, return on scalar tolerance | A whole-H eigenpair/FD residual or variational stability bound |
| [Lin2016 ACE, author PDF](https://math.berkeley.edu/~linlin/publications/ACE.pdf), JCTC12,2242, DOI10.1021/acs.jctc.6b00092 | Matching source-span action and adaptive rebuilding at self-consistency; oversampling for empty states | Global off-span accuracy, symmetry or exact replay of an incomplete source/state bundle |
| [QE7.5 exx.f90](https://raw.githubusercontent.com/QEF/q-e/qe-7.5/PW/src/exx.f90), ~435–552,3831; [memory_report.f90](https://raw.githubusercontent.com/QEF/q-e/qe-7.5/PW/src/memory_report.f90) | Source-buffer and ACE allocation dependencies | Total future RSS, guaranteed timing or a352-band streaming/native continuation proof |

The existing streaming `source_manifest.json` pins qe-7.5 commit
770a0b2d12928a67048e2f3da8d10d057e52179e and the upstream EXX file hash
9ce3e0fa836a11f6e3d8dda36ab92c1f39082fbf0587fc56a36fcc3f88b57bdf.
Numerical resource calculations use the ORIGINAL native FFT/band/q descriptors,
not webpage defaults or current QE release assumptions. Raw source was read on
the native web tool; no new source download/build in protected DFT occurred.

**Inherited scientific boundaries:** the repository's
[host-invariant kernel derivation](../../../../docs/derivations/host_invariant_reaction_kernel.md)
already distinguishes full/residual T and P-irreducible K. The prior
[physical-inversion identifiability result](../physical_inversion_2026-10-15/identifiability_and_root.md)
retains N3, configuration, material and root-modulus limitations. Earlier
Krishtopenko2022 SCBA and Wei–Zunger1991 comparisons remain unchanged; this
audit does not supersede them or propose a new microscopic alloy closure.

**Contribution here:** newly measured qualifications of the retained ORIGINAL
SCF sources (occupations, density symmetry, ACE probes, exact export lineage,
cutoff frame tail and resource incompatibility). This is distinct from P1's
cross-cutoff Γ spectral-kernel inventory. The transfer/fixed-point/error
inequalities are established mathematics or conditional derivations, not
unprecedented results. Material HgCdTe mass/x_c and scientific novelty remain
OPEN/UNVERIFIED. No optical search, data request or old synthetic test repeated.
