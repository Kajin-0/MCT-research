# Oriented Te p-tensor tomography and complementary scattering geometry

**PROVEN under stated assumptions:** a fixed ideal four-neighbor Te
environment, independent Bernoulli occupations, a common Cartesian
orbital frame, and a real symmetric spin-independent p-onsite response
covariant under all 24 operations of Td. This is a restricted sector of
the full relativistic impurity Hamiltonian. No HgCdTe coefficient is
assigned here. SOC changes, other orbitals, hopping matrices, long-range
response and background dependence require their actual operators.

The [general oriented covariance identity](oriented_tetrahedral_response.md)
shows why coherent composition derivatives miss directional disorder.
In this p sector the missing information has a finite, explicitly
extractable form.

## Representative matrices determine the orientation orbits

Use the bond signs (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1), unit
directions n_i, and A_i=n_i n_i^T-I/3. For a cation pair {i,j}, define

\[
 B_{ij}=A_i+A_j,\qquad
 E_{ij}=I/3-u_{ij}u_{ij}^T,\qquad
 u_{ij}=\frac{n_i+n_j}{\|n_i+n_j\|}.
\]

For {1,2}, u is the x axis, E=diag(-2,1,1)/3 and B has only yz and zy
entries, each 2/3. The scalar and two traceless tensors are orthogonal
in the Frobenius inner product.

After removing the pure-endpoint chord, H(empty)=H(all)=0. Every response
in this restricted covariant class has the unique form

\[
\begin{aligned}
 H(\{i\})&=h_1 I+a_1 A_i,\\
 H(\{i,j\})&=h_2 I+e_2 E_{ij}+b_2 B_{ij},\\
 H(\{1,2,3,4\}\setminus\{l\})&=h_3 I+a_3 A_l.
\end{aligned}
\]

For a singleton, its stabilizer permits two independent real symmetric
p tensors. For a pair, the stabilizer permits three; in the representative
frame its matrix is [[a,0,0],[0,b,c],[0,c,b]]. The complementary singleton
again permits two. The endpoint stabilizers permit only a scalar.
Consequently there are nine parameters before endpoint subtraction and
**seven after it: three coherent scalars and four directional parameters**.
The audit below computes the stabilizer dimensions by exact rational
linear algebra, rather than assuming an angular ansatz.

One oriented N=1 calculation, one oriented N=3 calculation and one
oriented N=2 pair calculation, with known orbital rotations, determine
this sector completely. Extract h_N=Tr(H_N)/3 and each directional
coefficient by its orthogonal tensor projection. For example,
a_1=Tr(A_i H({i}))/Tr(A_i^2). These are microscopic matrix extractions,
not fit parameters. Dilute calculations on opposite hosts supply those
representatives only if the fixed-background assumption is justified.

## Four parameters invisible to every coherent derivative

The orbit sums of A, E and B vanish. Hence

\[
 M(p)=\left[4p(1-p)^3h_1+6p^2(1-p)^2h_2
             +4p^3(1-p)h_3\right]I.
\]

No derivative of M contains a_1,a_3,e_2,b_2. Their absence does not imply
zero scattering. This distinction concerns configurational derivatives
of the coherent local matrix. Physical dilute T-matrix concentration
derivatives can already include scattering from these tensors.

Define the directional connected-triplet coefficient

\[
 c=a_3-a_1+2b_2.
\]

Möbius inversion gives the raw directional cluster increments

\[
 J_i=a_1 A_i,\qquad
 J_{ij}=e_2 E_{ij}+(b_2-a_1)B_{ij},\qquad
 J_{ijk}=c A_l,\qquad J_{1234}=0,
\]

where l is the missing bond. The zero four-body directional tensor
follows from Td covariance: its orbit is a singleton, so it must be
scalar. This statement applies to the specified real p-onsite sector;
it is not a theorem that the full SOC/Wannier Hamiltonian has no
four-body response.

With xi_i=eta_i-x, the centered directional vertices are

\[
\begin{aligned}
 C_i&=\beta_1(x)A_i,&
 \beta_1&=a_1+2x(b_2-a_1)-c x^2,\\
 C_{ij}&=e_2 E_{ij}+\beta_2(x)B_{ij},&
 \beta_2&=b_2-a_1-cx,\\
 C_{ijk}&=c A_l,&C_{1234}&=0.
\end{aligned}
\]

Therefore the exact local squared Frobenius fluctuation is

\[
 V_{\rm dir}(x)=\frac83 k\beta_1^2
       +k^2\left(4e_2^2+\frac{16}{3}\beta_2^2\right)
       +\frac83 k^3 c^2,
 \qquad k=x(1-x).
\]

It is the trace of the vectorized directional covariance, not an
electronic linewidth, static shift or susceptibility. Tensoring with
the spin identity doubles this trace but supplies no SOC response.

## Complementary one-body form factor

Let F(q)=sum_i exp(i q.d_i), and define the three sign-weighted Fourier
sums F_alpha=sum_i s_(i,alpha) exp(i q.d_i). The four sign rows form a
Hadamard matrix, so exactly

\[
 |F|^2+|F_x|^2+|F_y|^2+|F_z|^2=16.
\]

The off-diagonal xy, xz, yz entries of sum_i exp(i q.d_i)A_i are
F_z/3,F_y/3,F_x/3. Thus

\[
 \left\|\sum_i e^{iq.d_i}A_i\right\|_F^2
       =\frac29\left(16-|F(q)|^2\right).
\]

**PROVEN:** the one-body directional tensor is zero at q=0 and its
Frobenius scattering strength is maximal at every scalar F zero. Its
geometry is complementary to the count-symmetric one-body filter.
This does not make the full electronic scattering isotropic: branch
spinors, hopping phases and the electronic Green function remain inside
each matrix bilinear.

Because distinct Te tetrahedra share at most one cation, the pair and
triplet channels remain spatially white at second configurational order.
For translationally identical orbital frames the directional covariance
trace is consequently

\[
 \operatorname{Tr}K_{\rm dir}(q,x)
 =\frac29 k\beta_1^2(16-|F(q)|^2)
  +k^2\left(4e_2^2+\frac{16}{3}\beta_2^2\right)
  +\frac83 k^3c^2.
\]

The simple endpoint-invisible one-body counterexample is the special
case a_1=b_2=lambda, a_3=-lambda, e_2=0. It has c=beta_2=0 and
beta_1=lambda. The equality above recovers its finite X-point vertex.

## Independent checks and consequence

[The frozen audit](../../data/calculated/te_p_tensor_tomography_audit.json)
enumerates all 16 environments and 24 Td operations, proves the
stabilizer ranks exactly, reconstructs all seven coefficients from three
representative matrices, and compares direct event averaging and Möbius
cluster coefficients with the formulas above. Arbitrary wavevectors
verify the complementary Fourier norm. No measured alloy quantity or
physical response amplitude enters these checks.

Angular p tensors have established precedent in
[Niquet et al., PRB 79, 245201 (2009), Eq. (10)](https://arxiv.org/pdf/0902.0491).
That paper is a strain/SiGe model and supplies no HgCdTe coefficient.
**HYPOTHESIS:** the four directional components may be significant in a
self-consistent Cd-in-HgTe potential. The next physical extraction must
retain them before averaging. **NOVELTY CANDIDATE:** no historical
priority is established for this classification or its application.

The [spinful onsite extension](te_p_soc_tensor_tomography.md) includes
all time-reversal-even p-sector SOC tensors: six coherent and eight
directional coefficients after endpoint subtraction. It also derives
the distinct chemical/SOC combinations seen within j=3/2 and between
j=3/2 and j=1/2, without assigning any physical amplitude.
