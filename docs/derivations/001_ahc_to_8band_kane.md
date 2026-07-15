# Derivation 001 — From AHC self-energy to a finite-temperature 8-band Kane model

**Status:** derived framework; not yet numerically checked for HgCdTe  
**Claim level:** established theory assembled into a HgCdTe-specific research program  
**Novelty status:** unconfirmed

## 1. Target quantity

For bulk zincblende Hg\(_{1-x}\)Cd\(_x\)Te, define the signed zone-center gap

\[
E_g(x,T)=E_{\Gamma_6}(x,T)-E_{\Gamma_8}(x,T).
\]

The complete finite-temperature low-energy object is taken to be

\[
\overline{\mathbf G}_8^{-1}(\mathbf k,\omega;x,T)=
\hbar\omega\mathbf I
-\mathbf H_{8K}^{0}(\mathbf k;x)
-\boldsymbol\Sigma_{8}^{\mathrm{ep}}(\mathbf k,\omega;x,T)
-\boldsymbol\Sigma_{8}^{\mathrm{alloy}}(\mathbf k,\omega;x)
-\mathbf H_{8}^{\mathrm{QH}}(x,T).
\]

The scalar bandgap is one pole separation extracted from this Green function.

## 2. Eight-band basis

Use the ordered Kane basis

\[
\mathcal B_8=
\{|Γ_6,+1/2\rangle,|Γ_6,-1/2\rangle,
|Γ_8,+3/2\rangle,|Γ_8,+1/2\rangle,
|Γ_8,-1/2\rangle,|Γ_8,-3/2\rangle,
|Γ_7,+1/2\rangle,|Γ_7,-1/2\rangle\}.
\]

At \(\mathbf k=0\), with the \(\Gamma_8\) edge chosen as zero,

\[
\mathbf H_\Gamma^0=
\begin{pmatrix}
E_g^0\mathbf I_2&0&0\\
0&0\mathbf I_4&0\\
0&0&-\Delta^0\mathbf I_2
\end{pmatrix}.
\]

Here

\[
E_g^0=E_{\Gamma_6}-E_{\Gamma_8},
\qquad
\Delta^0=E_{\Gamma_8}-E_{\Gamma_7}.
\]

## 3. Static 8-band Kane Hamiltonian

Write

\[
\mathbf H_{8K}^{0}(\mathbf k)=
\mathbf H_\Gamma^0
+\mathbf H^{(1)}(\mathbf k)
+\mathbf H^{(2)}(\mathbf k)+\cdots.
\]

The linear term contains the Kane coupling

\[
\mathbf H^{(1)}(\mathbf k)=P\sum_i k_i\mathbf K_i,
\]

where \(\mathbf K_i\) are fixed basis-dependent invariant matrices.

The quadratic term contains the remote-conduction and valence-band parameters

\[
\mathbf H^{(2)}=
\mathbf H^{(2)}(F,\gamma_1,\gamma_2,\gamma_3).
\]

The standard parameter vector is

\[
\mathbf p=
\{E_g,\Delta,P,F,\gamma_1,\gamma_2,\gamma_3\}.
\]

## 4. Electron–phonon Hamiltonian

Expand the self-consistent electronic potential in atomic displacements:

\[
\hat V=\hat V^{(0)}+\hat V^{(1)}+\hat V^{(2)}+O(u^3).
\]

The linear electron–phonon interaction is

\[
\hat H_{\mathrm{ep}}^{(1)}=
\sum_{mn\mathbf k\mathbf q\nu}
 g_{mn\nu}(\mathbf k,\mathbf q)
 c_{m,\mathbf k+\mathbf q}^{\dagger}c_{n\mathbf k}
 \left(b_{\mathbf q\nu}+b_{-\mathbf q\nu}^{\dagger}\right),
\]

with

\[
g_{mn\nu}(\mathbf k,\mathbf q)=
\left\langle
\psi_{m,\mathbf k+\mathbf q}
\left|\Delta_{\mathbf q\nu}V_{\mathrm{SCF}}\right|
\psi_{n\mathbf k}
\right\rangle.
\]

The quadratic term produces the Debye–Waller contribution.

## 5. Dynamical Fan–Migdal self-energy

The retarded Fan self-energy is

\[
\Sigma_{n\mathbf k}^{\mathrm{Fan}}(\omega,T)=
\frac{1}{N_q}\sum_{m\mathbf q\nu}|g_{mn\nu}|^2
\left[
\frac{n_{\mathbf q\nu}+1-f_{m,\mathbf k+\mathbf q}}
{\hbar\omega-\varepsilon_{m,\mathbf k+\mathbf q}-\hbar\omega_{\mathbf q\nu}+i\eta}
+
\frac{n_{\mathbf q\nu}+f_{m,\mathbf k+\mathbf q}}
{\hbar\omega-\varepsilon_{m,\mathbf k+\mathbf q}+\hbar\omega_{\mathbf q\nu}+i\eta}
\right].
\]

For narrow-gap polar HgCdTe, the nonadiabatic phonon denominators should be retained unless an explicit convergence study justifies the static approximation.

## 6. Debye–Waller term

The harmonic Debye–Waller shift is

\[
\Sigma_{n\mathbf k}^{\mathrm{DW}}(T)=
\frac{1}{2N_q}\sum_{\mathbf q\nu}
\Lambda_{nn}^{\nu\nu}(\mathbf k,\mathbf q,-\mathbf q)
\left[2n_{\mathbf q\nu}(T)+1\right].
\]

The complete electron–phonon self-energy is

\[
\boldsymbol\Sigma^{\mathrm{ep}}=
\boldsymbol\Sigma^{\mathrm{Fan}}+
\boldsymbol\Sigma^{\mathrm{DW}}.
\]

Both terms are required for a controlled second-order harmonic result.

## 7. Exact downfolding into the Kane subspace

Let \(\mathcal P\) project onto the eight Kane states and \(\mathcal Q=1-\mathcal P\). The exact projected Green function follows from the Schur complement:

\[
\mathbf G_8^{-1}=
 z-\mathbf H_{PP}-\boldsymbol\Sigma_{PP}
-(\mathbf H_{PQ}+\boldsymbol\Sigma_{PQ})
[z-\mathbf H_{QQ}-\boldsymbol\Sigma_{QQ}]^{-1}
(\mathbf H_{QP}+\boldsymbol\Sigma_{QP}).
\]

Therefore, the effective eight-band self-energy is not generally equal only to \(\mathcal P\Sigma\mathcal P\). Remote bands contribute through the second term and can renormalize \(F\), \(\gamma_i\), and the effective interband couplings.

## 8. Symmetry reduction at \(\Gamma\)

For an unstrained, macroscopically cubic alloy after configurational averaging,

\[
D(g)\boldsymbol\Sigma_8(0,\omega,T)D^{\dagger}(g)=
\boldsymbol\Sigma_8(0,\omega,T)
\qquad \forall g\in T_d.
\]

Schur's lemma then gives

\[
\boldsymbol\Sigma_8(0,\omega,T)=
\begin{pmatrix}
\sigma_6(\omega,T)\mathbf I_2&0&0\\
0&\sigma_8(\omega,T)\mathbf I_4&0\\
0&0&\sigma_7(\omega,T)\mathbf I_2
\end{pmatrix}.
\]

Hence

\[
\Sigma_{\Gamma_6,\Gamma_8}(0,\omega,T)=0
\]

under the average bulk symmetry. The \(\Gamma_6\)-\(\Gamma_8\) crossing is symmetry allowed and is not generically converted into an avoided crossing by the thermally averaged self-energy.

## 9. Renormalized band-edge parameters

The quasiparticle poles satisfy

\[
E_r=E_r^0+\operatorname{Re}\sigma_r(E_r,T),
\qquad r\in\{6,8,7\}.
\]

Therefore,

\[
E_g(T)=E_6(T)-E_8(T)
\]

and

\[
\Delta(T)=E_8(T)-E_7(T).
\]

At fixed reference volume,

\[
\Delta E_g^{\mathrm{ep}}(T)=
\operatorname{Re}
\left[
\sigma_6^{\mathrm{Fan}}-
\sigma_8^{\mathrm{Fan}}+
\sigma_6^{\mathrm{DW}}-
\sigma_8^{\mathrm{DW}}
\right].
\]

## 10. Quasiparticle linearization

Linearize the matrix self-energy near \(z_0\):

\[
\Sigma_8(z)\approx\Sigma_8(z_0)+(z-z_0)\Sigma_8'(z_0).
\]

Define

\[
\mathbf A=\mathbf I-\operatorname{Re}\Sigma_8'(z_0),
\]

\[
\mathbf B=\mathbf H_{8K}^{0}+\operatorname{Re}\Sigma_8(z_0)
-z_0\operatorname{Re}\Sigma_8'(z_0).
\]

The generalized eigenvalue problem is

\[
\mathbf B|\psi\rangle=E\mathbf A|\psi\rangle.
\]

A static Hermitian quasiparticle Hamiltonian is

\[
\boxed{\mathbf H_8^{\mathrm{QP}}=\mathbf A^{-1/2}\mathbf B\mathbf A^{-1/2}}.
\]

This reduction should be rejected if the self-energy varies too strongly over the target energy window.

## 11. Thermal expansion

Two non-double-counting choices are available.

### Fixed-volume decomposition

\[
\mathbf H_8(T)=\mathbf H_8^{\mathrm{stat}}[V_0]
+\Sigma_8^{\mathrm{ep}}[T;V_0]
+\left(\mathbf H_8^{\mathrm{stat}}[V(T)]-\mathbf H_8^{\mathrm{stat}}[V_0]\right).
\]

### Volume-consistent calculation

\[
\mathbf H_8(T)=\mathbf H_8^{\mathrm{stat}}[V(T)]
+\Sigma_8^{\mathrm{ep}}[T;V(T)].
\]

The second expression must not receive an additional thermal-expansion correction.

## 12. Parameter extraction by invariant projection

Write the Kane model as

\[
\mathbf H_{8K}(\mathbf k;\mathbf p)=
\sum_a p_a\mathbf M_a(\mathbf k),
\]

where \(\mathbf M_a=\partial \mathbf H_{8K}/\partial p_a\).

Given projected first-principles matrices \(\mathbf H_8^{\mathrm{QP}}(\mathbf k,T)\), minimize

\[
\chi^2=\sum_{\mathbf k}w_{\mathbf k}
\left\|\mathbf H_8^{\mathrm{QP}}(\mathbf k,T)
-\sum_a p_a(T)\mathbf M_a(\mathbf k)\right\|_F^2.
\]

Define

\[
G_{ab}=\sum_{\mathbf k}w_{\mathbf k}
\operatorname{Re}\operatorname{Tr}
[\mathbf M_a^{\dagger}\mathbf M_b],
\]

\[
b_a=\sum_{\mathbf k}w_{\mathbf k}
\operatorname{Re}\operatorname{Tr}
[\mathbf M_a^{\dagger}\mathbf H_8^{\mathrm{QP}}].
\]

Then

\[
\boxed{\mathbf p(T)=\mathbf G^{-1}\mathbf b(T)}.
\]

This matrix fit preserves eigenvector character and interband couplings that are lost in an eigenvalue-only fit.

## 13. Test of one-\(P\) closure

The finite-temperature Hamiltonian can be allowed to contain separate couplings

\[
P_8(T):\Gamma_6\leftrightarrow\Gamma_8,
\qquad
P_7(T):\Gamma_6\leftrightarrow\Gamma_7.
\]

Define

\[
\eta_P(T)=
\frac{2|P_8-P_7|}{|P_8|+|P_7|}.
\]

The conventional one-\(P\) Kane model is supported only if \(\eta_P\) remains below the combined numerical, gauge, and experimental uncertainty.

## 14. Model-closure residual

After extracting the standard parameters, define

\[
\mathbf R(\mathbf k,T)=
\mathbf H_8^{\mathrm{QP}}(\mathbf k,T)
-\mathbf H_{8K}(\mathbf k;\mathbf p(T)).
\]

Use the normalized residual

\[
\rho(T)=
\sqrt{
\frac{\sum_{\mathbf k}w_{\mathbf k}\|\mathbf R(\mathbf k,T)\|_F^2}
{\sum_{\mathbf k}w_{\mathbf k}
\|\mathbf H_8^{\mathrm{QP}}(\mathbf k,T)-\mathbf H_8^{\mathrm{QP}}(0,T)\|_F^2}
}.
\]

A residual larger than the numerical projection error indicates that temperature generates structure not captured by the conventional parameter manifold.

## 15. Alloy configurational averaging

For alloy configuration \(C\), calculate \(\mathbf G_{8,C}\). The rigorous average is

\[
\overline{\mathbf G}_8=
\left\langle\mathbf G_{8,C}\right\rangle_C,
\]

not simply the resolvent of the averaged Hamiltonian.

The spectral function is

\[
A_8(\mathbf k,\omega,T)=
-\frac{1}{\pi}\operatorname{Im}
\operatorname{Tr}\overline{\mathbf G}_8.
\]

For finite SQS sampling, restore the average cubic symmetry using

\[
\overline{\mathbf H}_8^{\mathrm{sym}}(\mathbf k)=
\frac{1}{N_C|T_d|}\sum_C\sum_{g\in T_d}
D^{\dagger}(g)\mathbf H_{8,C}(g\mathbf k)D(g).
\]

The removed configuration-dependent splittings are retained as disorder statistics rather than discarded as numerical noise.

## 16. Analytical reduction

After calculating the mode-resolved gap coupling, define a spectral density

\[
\mathcal F_g(x,\omega)=
\frac{1}{N_q}\sum_{\mathbf q\nu}
\mathcal G_{\mathbf q\nu}(x)
\delta(\omega-\omega_{\mathbf q\nu}).
\]

Then the thermal electron–phonon gap shift relative to zero temperature is

\[
\Delta_T E_g^{\mathrm{ep}}(x,T)=
2\int_0^{\infty}d\omega\,
\mathcal F_g(x,\omega)n_B(\omega,T).
\]

A compact surrogate can be generated by approximating the spectral density with a small number of signed effective oscillators:

\[
\Delta_T E_g^{\mathrm{ep}}(x,T)\approx
\sum_j A_j(x)
\left[\coth\left(\frac{\Theta_j(x)}{2T}\right)-1\right].
\]

This is a reduced model, not the exact AHC expression. Its adequacy must be assessed against the full spectral integral.

## 17. Immediate falsifiable predictions

1. \(v_K(T)\) changes much less than \(E_g(T)\).
2. Low-temperature \(E_g(T)\) departs from exact linearity.
3. The standard one-\(P\) Kane model may acquire a measurable closure residual.
4. Near the zero-gap composition, disorder broadening may exceed the mean signed gap.
5. The critical composition obeys

   \[
   \frac{dx_c}{dT}=-
   \frac{\partial E_g/\partial T}
   {\partial E_g/\partial x}.
   \]

## 18. Required checks before use

- reproduce static HgTe and CdTe ordering;
- converge the gap to below 1 meV numerical uncertainty;
- verify gauge stability of projected matrix elements;
- verify symmetry-restored degeneracies;
- test the dependence on \(k\)-fit window;
- compare on-shell and dynamical quasiparticle solutions;
- separate electron–phonon and thermal-expansion terms;
- benchmark against held-out magneto-optical transitions.

## 19. Current conclusion

The defensible research target is not merely

\[
E_g=E_g^0+\Sigma_c-\Sigma_v.
\]

It is a symmetry-preserving, frequency-aware, disorder-resolved finite-temperature 8-band model from which a compact analytical bandgap equation can be reduced and independently validated.

## Literature anchors

- P. B. Allen and V. Heine, theory of temperature-dependent electronic band structures.
- J. P. Nery and P. B. Allen, generalized treatment of electron–phonon band renormalization.
- E. G. Novik et al., *Band structure of semimagnetic Hg\(_{1-y}\)Mn\(_y\)Te quantum wells*, standard 8-band Kane conventions: https://arxiv.org/abs/cond-mat/0409392
- F. Teppe et al., *Temperature-driven massless Kane fermions in HgCdTe crystals*: https://arxiv.org/abs/1602.05999
- W. Chen et al., dielectric-dependent hybrid-functional/SOC treatment of HgCdTe alloys and defects: https://arxiv.org/abs/2311.05283
