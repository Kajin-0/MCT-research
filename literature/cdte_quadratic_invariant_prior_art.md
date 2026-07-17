# Prior-art audit: complete quadratic eight-band invariants

## Status

**Conclusion:** the ten-dimensional homogeneous, time-reversal-even quadratic space found for the fixed

```text
Gamma6 + Gamma8 + Gamma7
```

basis is established prior art at the level of zincblende double-group invariant theory.

The repository must not claim discovery of six new quadratic invariants.

The narrower result that remains potentially publishable is material- and method-specific:

> A wavefunction-gauge-fixed static CdTe calculation rejects the conventional four-dimensional Kane quadratic reduction, while the complete ten-dimensional Weiler/Trebin quadratic space closes both fitted directions and an unused `[110]` matrix direction.

Novelty of that narrower claim remains unconfirmed.

## Closest prior art

### Weiler, Aggarwal, and Lax (1978)

M. H. Weiler, R. L. Aggarwal, and B. Lax, *Physical Review B* **17**, 3269 (1978), DOI `10.1103/PhysRevB.17.3269`.

Weiler generalized the eight-band Pidgeon-Brown zincblende Hamiltonian using double-group invariants and inversion-asymmetry terms. The parameter table is reproduced and discussed in L. C. Lew Yan Voon and M. Willatzen, *The k.p Method: Electronic Properties of Semiconductors* (Springer, 2009), Sec. 5.7, DOI `10.1007/978-3-540-92872-0`.

For the even, zero-field quadratic sector, the Weiler parameter count is:

| Block | Weiler parameters | Dimension |
|---|---|---:|
| `Gamma6-Gamma6` | `F` | 1 |
| `Gamma6-Gamma8` | `N2`, `G` | 2 |
| `Gamma6-Gamma7` | `G'` | 1 |
| `Gamma8-Gamma8` | `gamma1`, `gamma2`, `gamma3` | 3 |
| `Gamma8-Gamma7` | `gamma2'`, `gamma3'` | 2 |
| `Gamma7-Gamma7` | `gamma1'` | 1 |
| **Total** |  | **10** |

This dimension table is identical to the independently generated repository projector:

```text
1 + 2 + 1 + 3 + 2 + 1 = 10.
```

The Weiler model also contains odd-in-`k`, magnetic-field, and inversion-asymmetry parameters outside the present even-`k^2`, zero-field audit. They must not be conflated with the ten-dimensional quadratic subspace.

### Trebin, Roessler, and Ranvaud (1979)

H.-R. Trebin, U. Roessler, and R. Ranvaud, “Quantum resonances in the valence bands of zinc-blende semiconductors. I. Theoretical aspects,” *Physical Review B* **20**, 686–700 (1979), DOI `10.1103/PhysRevB.20.686`.

Trebin et al. construct an effective eight-state zincblende Hamiltonian by the method of invariants. Their work is a direct prior-art boundary for claims involving a symmetry-complete `Gamma6 + Gamma8 + Gamma7` Hamiltonian.

### Later complete-invariant and multiband work

- T. B. Bahder, *Physical Review B* **41**, 11992 (1990), DOI `10.1103/PhysRevB.41.11992`, derives an eight-band `Gamma6/Gamma8/Gamma7` Hamiltonian by second-order Loewdin perturbation, including strain.
- B. A. Foreman, *Physical Review B* **48**, R4964 (1993), DOI `10.1103/PhysRevB.48.R4964`, emphasizes that remote-band elimination and basis construction can invalidate commonly imposed parameter relations.
- M. Ostromek, *Physical Review B* **54**, 14467 (1996), DOI `10.1103/PhysRevB.54.14467`, analyzes a general eight-band Hamiltonian including inversion asymmetry and momentum-dependent spin-orbit effects.
- K. Gawarecki et al., *Physical Review B* **105**, 045202 (2022), DOI `10.1103/PhysRevB.105.045202`, provide a modern invariant expansion for a 30-band zincblende model and further establish symmetry-invariant construction as prior art.

These works reinforce that a complete invariant basis is not itself novel.

## Exact relationship to the repository model

The repository’s conventional homogeneous Novik Hamiltonian uses four independent even-quadratic parameters:

```text
F, gamma1, gamma2, gamma3.
```

It contains:

- the single `Gamma6-Gamma6` curvature `F`;
- the three `Gamma8-Gamma8` Luttinger structures;
- fixed split-off and `Gamma8-Gamma7` matrix structures generated from the same `gamma1`, `gamma2`, and `gamma3`.

Relative to the complete double-group space, that reduction makes two distinct restrictions.

### 1. It omits three conduction-valence quadratic channels

```text
Gamma6-Gamma8: N2, G
Gamma6-Gamma7: G'
```

The standard reduced Kane Hamiltonian retains the linear couplings `P8/P7` but no independent even-quadratic couplings in these blocks.

### 2. It ties the split-off quadratic parameters to the Gamma8 parameters

The complete double-group model allows

```text
gamma1', gamma2', gamma3'
```

independently of

```text
gamma1, gamma2, gamma3.
```

The conventional reduction imposes the single-group-derived identifications

```text
gamma1' = gamma1
gamma2' = gamma2
gamma3' = gamma3
```

up to the declared basis, sign, and normalization convention.

Therefore the six additional dimensions found by the repository are not unnamed new objects. They are the established independent directions

```text
N2, G, G',
gamma1' - gamma1,
gamma2' - gamma2,
gamma3' - gamma3
```

where the last three expressions describe the dimensions relative to the conventional tied subspace, not literal universal parameter differences across notation systems.

## What the repository result does establish

At the existing static CdTe planning point:

1. the conventional four-dimensional quadratic span gives approximately `48%` training and unused-`[110]` residual;
2. the complete ten-dimensional span gives approximately `1.4e-5` training residual and `8.6e-6` unused-`[110]` residual;
3. the ten-dimensional fit has rank 10 and condition number approximately `1.73`;
4. all three omitted channel groups are required for held-out closure;
5. finite-radius contamination is approximately `0.125%` of the failed residual and is therefore strongly disfavored as the explanation.

This supports the statement:

> The single-group-style parameter ties used by the conventional homogeneous Kane reduction do not close the projected static CdTe matrix Hamiltonian, whereas the established complete Weiler double-group quadratic space does.

It does not yet establish:

- converged CdTe values of `N2`, `G`, `G'`, or the primed `gamma` parameters;
- that the discrepancy persists with converged cutoffs, lattice constant, band count, or exchange-correlation treatment;
- that the effect is unique to CdTe or HgCdTe;
- a new invariant or a new Hamiltonian form;
- finite-temperature behavior;
- experimental improvement.

## Candidate novelty after this audit

### Established

- the ten-dimensional symmetry-allowed quadratic space;
- the Weiler parameter classes and their sector dimensions;
- independent double-group parameters versus single-group-derived parameter relations;
- invariant generation and multiband downfolding as general methodology.

### Candidate methodological/material result, unconfirmed

- direct extraction from physical CdTe wavefunctions after complete double-group gauge fixing;
- matrix-level demonstration that the conventional four-dimensional reduction fails while the complete Weiler space closes an unused crystal direction;
- quantitative identification of which established Weiler channel groups are necessary for CdTe closure;
- a reproducible route for testing those channel relations across temperature and HgCdTe composition.

### Not currently supportable

- “six new quadratic parameters”;
- “first complete eight-band zincblende Hamiltonian”;
- “new symmetry invariants”;
- converged CdTe or HgCdTe parameter values;
- a new analytical bandgap equation derived from this static result alone.

## Next authorized gate

The next step should remain analytical and use the existing matrices:

1. construct explicit Weiler-normalized templates for `N2`, `G`, `G'`, `gamma1'`, `gamma2'`, and `gamma3'` in the exact Novik basis;
2. verify that those ten named templates reproduce the projector basis exactly;
3. fit named coefficients and report covariance/correlation under `[001]/[111]` training with `[110]` holdout;
4. test nested physically motivated reductions rather than arbitrary orthonormal invariant directions;
5. freeze the static model before any new electronic-structure calculation.

No phonon, AHC, HgTe, alloy, denser-`k`, additional-band, or higher-level-functional calculation is authorized by this audit.
