# Bond orientation in the Te tetrahedral Hamiltonian

Status: **PROVEN** identities and counterexample under independent Bernoulli
occupation and a fixed four-neighbor Hamiltonian in one physical orbital
frame. No HgCdTe response amplitude is calculated or fitted here.

The count-symmetric Bernstein closure in the handoff assumes that every
configuration with N Cd neighbors has the same matrix H_N in that frame.
Physical tetrahedral covariance is a weaker condition:

\[
 H(gS)=U_g H(S)U_g^\dagger.
\]

It relates oriented configurations by orbital rotations. It does not make
their common-frame matrices equal. This distinction matters for Te p/d
onsite tensors, SOC matrices and bond-resolved hopping operators. Retain
those directions in the self-consistent impurity extraction before any
environment or sector average.

## Exact oriented cluster expansion

Let S be a subset of the four specified cation bonds. For an arbitrary
fixed local matrix response, its unique multilinear expansion is

\[
 H(\eta)=\sum_{S\subseteq\{1,2,3,4\}}J_S\prod_{i\in S}\eta_i.
\]

With xi_i=eta_i-x, define

\[
 C_S(x)=\sum_{T\supseteq S}J_T x^{|T|-|S|},\qquad
 M(p)=\sum_S J_S p^{|S|}.
\]

Then H=M(x)+sum_(S nonempty) C_S prod_(i in S) xi_i. Bernoulli
orthogonality still holds for every distinct subset. The local covariance,
written as a positive operator on vectorized Hamiltonian matrices, is

\[
 K_{\rm local}=\sum_{m=1}^4 k^m\sum_{|S|=m}|C_S)(C_S|.
\]

Here |C)(C| denotes vec(C) vec(C)^dagger, and k=x(1-x). Equivalently,
any fixed Hermitian scalar probe has variance sum_S k^|S| [Tr(O C_S)]^2.
No configurational cross-order channel has been added.

The auxiliary-probability derivative now determines the **order average**:

\[
 \overline C_m=\binom4m^{-1}\sum_{|S|=m}C_S
 =\frac{(4-m)!}{4!}M^{(m)}(x).
\]

Set delta C_S=C_S-overline C_m. Their sum at fixed m vanishes, giving

\[
 K_{\rm local}
 =\sum_m\binom4m k^m|\overline C_m)(\overline C_m|
 +\sum_m k^m\sum_{|S|=m}|\delta C_S)(\delta C_S|.
\]

**PROVEN:** the former Bernstein covariance formula is a positive lower
contribution to the general local covariance. It is an equality exactly
when all C_S of a given order coincide. The coherent M(p) cannot determine
the additional orientation covariance. Two Hamiltonians with identical
M(p), including identical endpoint derivatives of every order, can have
different finite-q scattering.

## Endpoint-invisible one-body counterexample

Use the unit tetrahedral directions n_mu=(+,+,+),(+,-,-),(-,+,-),(-,-,+)
divided by sqrt(3). In a common Cartesian Te (p_x,p_y,p_z) basis define

\[
 A_\mu=n_\mu n_\mu^T-I_3/3,\qquad
 H_{\rm dir}(\eta)=\lambda\sum_\mu\eta_\mu A_\mu.
\]

The local response is Hermitian and tetrahedrally covariant. It is zero
for all-Hg and all-Cd configurations because sum_mu A_mu=0. Its Bernoulli
coherent average **M(p)=0 for every p**, so all configurational derivatives
vanish. Nevertheless,

\[
 \langle\|H_{\rm dir}\|_F^2\rangle
 =\frac83\lambda^2 k>0
\]

for a mixed random alloy and nonzero lambda. The centered response is
ordinary one-body occupation disorder, lambda sum_mu xi_mu A_mu. It
does not define another independent random field. Spin can be included
as A_mu tensor I_2 without breaking nonmagnetic time reversal.

This angular tensor has established tight-binding precedents. The p-orbital
onsite expression in [Niquet et al., PRB 79, 245201 (2009), Eq. (10)](https://arxiv.org/pdf/0902.0491)
contains neighbor-weighted angular matrices of this form. That work studies
strain and Si/Ge; it does **not** provide a Hg/Cd chemical-response lambda
or validate this counterexample as HgCdTe's actual impurity potential.

## Form-factor zeros do not remove the directional one-body part

With d_mu=a n_mu sqrt(3)/4, the actual configurational matrix vertex is

\[
 \Gamma_1(q)=\sum_\mu e^{iq\cdot d_\mu}C_{\{\mu\}}
 =F(q)\overline C_1+
 \sum_\mu e^{iq\cdot d_\mu}\delta C_{\{\mu\}}.
\]

Only the first term is fixed by M'(x)/4 and the scalar tetrahedral form
factor. At q_X=(2 pi/a)(0,0,1), F(q_X)=0, but the counterexample gives

\[
 \Gamma_{\rm dir}(q_X)
 =\frac{4i\lambda}{3}
 (|p_x\rangle\langle p_y|+|p_y\rangle\langle p_x|),
 \qquad
 \operatorname{Tr}K_1(q_X)=\frac{32}{9}\lambda^2 k.
\]

**PROVEN:** a one-body Te response can survive an F(q) zero when its
orbital matrix depends on the bond direction. Vanishing at those zeros
requires the additional count-symmetric/equal-vertex assumption. Extra
Wannier hopping phase factors are a further electronic issue.

## Results retained and the extraction consequence

The centered-subset orthogonality and zincblende overlap geometry are
unchanged. All m>=2 channels remain white at second configurational order:
distinct Te tetrahedra cannot share a cation subset of size two or larger.
Their local covariance is now k^m sum_(|S|=m) |C_S)(C_S|. At a scalar
form-factor zero, orientation contributions are positive additions to
the former higher-cluster floor; they cannot invalidate its lower bound.

For independent occupations the coherent average still has degree at
most four. Five H_N can represent **orientation-averaged** matrices.
Endpoint-Hermite and Bernstein identities retain that coherent meaning.
Endpoint averaged derivatives reconstruct those five averages; they do
not reconstruct the common-frame oriented matrices from those derivatives
alone. Actual single/pair impurity calculations retain more information.
Under fixed Td covariance, representative N=1,2,3 matrices and the known
orbital rotations can generate their orientation orbits.

The physical effective one-body substitution vertex already includes
the induced Te directional response. No new phenomenological coefficient
should be inserted into the gap law. Extract and test the full oriented
operator from Cd-in-HgTe first; preserve its p/d tensors and bond-resolved
hoppings. Only then evaluate coherent sector averages and finite-q
spectral moments. **HYPOTHESIS:** such directional components may matter
numerically in HgCdTe. This document supplies no amplitude or gap shift.
**NOVELTY CANDIDATE:** none established; angular crystal-field operators,
cluster orthogonality and covariance decompositions are established tools.

The restricted real p-onsite sector admits a sharper
[seven-parameter oriented tomography](te_p_tensor_tomography.md): three
coherent scalars and four directional components, with an exact
complementary one-body Fourier norm proportional to 16-|F(q)|^2.
