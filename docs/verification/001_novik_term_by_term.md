# Verification 001 — Term-by-term comparison with Novik et al.

**Status:** completed for the homogeneous, unstrained, zero-field bulk reduction  
**External source:** E. G. Novik et al., *Phys. Rev. B* **72**, 035321 (2005), Eqs. (4)–(6), arXiv:cond-mat/0409392  
**Scope:** fixed [001] basis; constant material parameters; no strain, magnetic field, bulk-inversion asymmetry, or heterostructure operator ordering

## 1. Declared basis

The implementation uses the same ordered basis as Novik Eq. (4):

$$
\Gamma_6\oplus\Gamma_8\oplus\Gamma_7
$$

with order

$$
\left(
|\Gamma_6,+\tfrac12\rangle,
|\Gamma_6,-\tfrac12\rangle,
|\Gamma_8,+\tfrac32\rangle,
|\Gamma_8,+\tfrac12\rangle,
|\Gamma_8,-\tfrac12\rangle,
|\Gamma_8,-\tfrac32\rangle,
|\Gamma_7,+\tfrac12\rangle,
|\Gamma_7,-\tfrac12\rangle
\right).
$$

The phase convention therefore matches the published matrix directly; no basis rephasing is used in this audit.

## 2. Homogeneous-bulk specialization

Novik defines position-dependent operators for a [001] heterostructure. For a homogeneous bulk material,

$$
[\kappa,k_z]=0,
\qquad
\{\gamma_3,k_z\}=2\gamma_3 k_z,
$$

so

$$
C=0,
\qquad
\bar S_\pm=\widetilde S_\pm
=-2\alpha\sqrt3\,\gamma_3 k_\pm k_z,
$$

where

$$
\alpha=\frac{\hbar^2}{2m_0}.
$$

The repository intentionally implements only this homogeneous reduction.

## 3. Scalar kernels

| Published Novik term | Repository term | Result |
|---|---|---|
| $T=E_c+\alpha(1+2F)k^2$ | `t = ev + eg + a*(1+2*f)*k2` | exact |
| $U=E_v-\alpha\gamma_1 k^2$ | `u = ev - a*gamma1*k2` | exact |
| $V=-\alpha\gamma_2(k_x^2+k_y^2-2k_z^2)$ | `v = -a*gamma2*(kx*kx+ky*ky-2*kz*kz)` | exact |
| $R=\alpha\sqrt3[\gamma_2(k_x^2-k_y^2)-2i\gamma_3k_xk_y]$ | `r = a*sqrt(3)*(...)` | exact after expanding Novik's $\mu,\bar\gamma$ form |
| $\bar S_\pm=\widetilde S_\pm=-2\alpha\sqrt3\gamma_3k_\pm k_z$ | `s_plus`, `s_minus` | exact |
| $C=0$ | omitted | exact for constant parameters |

The conversion

$$
E_P=\frac{2m_0P^2}{\hbar^2}
$$

is implemented as

$$
P=\sqrt{\alpha E_P},
$$

because $\alpha=\hbar^2/(2m_0)$.

## 4. Conduction and interband block

Every nonzero $\Gamma_6\leftrightarrow\Gamma_8$ and $\Gamma_6\leftrightarrow\Gamma_7$ entry in Novik Eq. (5) was compared directly. The signs and coefficients

$$
\frac1{\sqrt2},\qquad
\frac1{\sqrt6},\qquad
\sqrt{\frac23},\qquad
\frac1{\sqrt3}
$$

match the repository implementation term by term.

The conventional model uses one $P$. The repository's optional $P_8/P_7$ extension changes only the reduced coupling assigned to the two published interband blocks; setting

$$
P_8=P_7=P
$$

recovers Novik exactly.

## 5. Valence block audit

The diagonal $U\pm V$ and $U-\Delta$ terms, the $R$ and $R^\dagger$ terms, the $\sqrt2V$ terms, and the $\bar S_\pm/\widetilde S_\pm$ terms were compared against all upper-triangular entries of Eq. (5).

The visually dense $u_5$–$u_7$ entry was checked directly against the rendered primary-source matrix. It is

$$
\boxed{
H_{5,7}=-\sqrt{\frac32}\,\widetilde S_+
},
$$

while the Hermitian counterpart is

$$
H_{7,5}=-\sqrt{\frac32}\,\widetilde S_+^\dagger.
$$

In zero-based Python indices the upper-triangular entry is therefore

```python
h[4, 6] = -np.sqrt(3.0 / 2.0) * s_plus
```

which was already the repository's original implementation. An initial audit draft mistakenly moved the dagger into the upper-triangular entry; GitHub CI and the existing time-reversal test rejected that transcription. The mistaken branch change was reverted before merge.

This term vanishes whenever $k_y=0$ or $k_z=0$. The [111] external reference test is therefore retained because it exercises the complex mixed-$k$ structure that axis-only and [110] checks cannot expose.

## 6. Independent executable checks

`tests/test_novik_reference.py` contains a second explicit implementation constructed from Novik Eqs. (5)–(6), rather than calling repository matrix templates.

It checks:

1. full complex matrix equality along [100], [110], and [111];
2. eigenvalue equality along all three directions;
3. independent finite-difference band curvatures and effective masses;
4. the isotropic conduction-band mass against the Löwdin second-order formula

$$
A_c=
\alpha(1+2F)
+\frac{2P^2}{3E_g}
+\frac{P^2}{3(E_g+\Delta)},
$$

with

$$
\frac{m_c^*}{m_0}=\frac{\alpha}{A_c}.
$$

The effective-mass test uses the normal-gap CdTe parameters from Novik Table I so the nondegenerate conduction expansion is well posed.

## 7. Items deliberately outside this verification

This audit does not validate:

- position-dependent Burt–Foreman operator ordering;
- $C$, $\bar S_\pm\ne\widetilde S_\pm$ in heterostructures;
- strain or Bir–Pikus terms;
- magnetic-field and Zeeman terms;
- bulk-inversion-asymmetry terms;
- arbitrary growth-direction rotations.

Those extensions are deferred. They are not required for the current homogeneous bulk analytical-bandgap program.

## 8. Conclusion

The implemented one-$P$ homogeneous Hamiltonian is algebraically identical to the declared Novik convention within the stated scope. The verification is executable and includes directions that expose complex mixed-$k$ terms. The CI failure during the audit was useful evidence: it caught a human transcription error rather than a defect in the original implementation.