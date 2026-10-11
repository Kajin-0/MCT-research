# Relativistic Te p-onsite tensor closure

**PROVEN:** fixed ideal four-neighbor Td covariance, a common Cartesian
p basis with one spin axis convention, and a Hermitian nonmagnetic local
onsite operator. Background dependence, other orbitals and hoppings are
outside this classification. No material response amplitude is supplied.

The [real p-tensor classification](te_p_tensor_tomography.md) extends
without fitting to a spinful onsite Hamiltonian. Time reversal requires

\[
 H=D\otimes I_2+\sum_{ij}B_{ij}L_i\otimes\sigma_j,
 \qquad D=D^T\ \text{real},\quad B\ \text{real},
\]

where (L_i)_(jk)=-i epsilon_(ijk) and sigma are Pauli matrices. These
six plus nine real directions exhaust the 15-dimensional time-reversal
even Hermitian 6x6 space. Under a spatial operation Q, both L and spin
are axial, so D and B transform by Q D Q^T and Q B Q^T. The actual spin
rotation is det(Q) Q, including for improper Td operations.

For every four-bond binary environment, the stabilizer forces B to be
symmetric. Its allowed dimensions at N=0,1,2,3,4 are 1,2,3,2,1, the
same as D. Exact ranks therefore give **18 parameters before endpoint
subtraction and 14 afterward**. Six describe coherent composition
dependence and eight describe directional response invisible to every
coherent Bernstein derivative. No general four-body response is ruled
out: the fourth-order coefficient can contain I_6 and L.sigma.

## Extraction from the same three oriented representatives

Define Q(T)=sum_ij T_ij L_i tensor sigma_j and S=L.sigma. The traceless
A_i,E_ij,B_ij tensors have the definitions in the real classification.
After subtracting the pure endpoints, the unique form is

\[
\begin{aligned}
 H(\{i\})={}&h_1I_6+s_1 S+a_1 A_i\otimes I_2+\alpha_1 Q(A_i),\\
 H(\{i,j\})={}&h_2I_6+s_2 S+e_2 E_{ij}\otimes I_2
             +b_2 B_{ij}\otimes I_2
             +\epsilon_2 Q(E_{ij})+\beta_2 Q(B_{ij}),\\
 H(\mathrm{all}\setminus\{l\})={}&h_3I_6+s_3 S
                       +a_3 A_l\otimes I_2+\alpha_3 Q(A_l).
\end{aligned}
\]

All listed directions at each representative are mutually orthogonal
in the Frobenius inner product. Projection of the three actual matrices
onto these tensors extracts all 14 numbers. Known Td rotations generate
the remaining orientation orbits. The opposite-host dilute and pair
calculations still need a justified fixed-background correspondence;
group theory cannot supply that physical assumption.

The coherent average contains only h(p)I_6+s(p)S, with h and s each the
degree-four Bernstein polynomial of their three mixed-sector values.
At the atomic angular-projector level it shifts j=3/2 by h+s and j=1/2
by h-2s. These are local angular sectors, not a replacement for the full
Bloch Gamma6/Gamma8/Gamma7 projectors in a microscopic calculation.

The scalar-free directional orbital and SOC families follow the same
centered cluster polynomials and complementary one-body form factor
derived for the real tensor. Their Frobenius inner products satisfy

\[
 \|T\otimes I_2\|_F^2=2\|T\|_F^2,\qquad
 \|Q(T)\|_F^2=4\|T\|_F^2,\qquad
 (T\otimes I_2,Q(T'))_F=0.
\]

Thus their local configurational covariance traces are respectively
twice and four times the real-tensor formula, using their own extracted
coefficient sets. They remain ordinary occupation/cluster disorder;
no additional independent random field has been postulated.

## Exact redistribution between angular channels

S has eigenvalues +1 in j=3/2 and -2 in j=1/2. Set

\[
 P_{3/2}=(S+2I_6)/3,\qquad P_{1/2}=(I_6-S)/3.
\]

For a traceless real symmetric T, direct Cartesian angular algebra gives

\[
 \{S,T\otimes I_2\}=-Q(T),\qquad
 P_{1/2}(T\otimes I_2)P_{1/2}=0.
\]

Consequently a chemical plus directional-SOC tensor
D_T=a(T tensor I_2)+alpha Q(T) has

\[
\begin{aligned}
 P_{3/2}D_TP_{3/2}&=(a-2\alpha)
                   P_{3/2}(T\otimes I_2)P_{3/2},\\
 P_{3/2}D_TP_{1/2}&=(a+\alpha)
                   P_{3/2}(T\otimes I_2)P_{1/2},\\
 P_{1/2}D_TP_{1/2}&=0.
\end{aligned}
\]

The two projected squared norms of the bare orbital tensor are equal:

\[
 \|P_{3/2}(T\otimes I_2)P_{3/2}\|_F^2
 =\|P_{3/2}(T\otimes I_2)P_{1/2}\|_F^2
 =\frac23\|T\|_F^2.
\]

**PROVEN conditional example:** a=2alpha removes the j=3/2 intra-sector
tensor while retaining an inter-sector tensor of amplitude 3alpha.
A small local j=3/2 splitting therefore does not by itself bound the
directional coupling to the other angular sector. Conversely a=-alpha
removes the inter-sector tensor and leaves the intra-sector amplitude.
This is operator geometry, not evidence that HgCdTe chooses either ratio,
nor an identification of the exact Bloch impurity T-matrix channels.

## Audit and scientific status

The [independent frozen spinful audit](../../data/calculated/te_p_soc_tensor_audit.json)
checks exact rational stabilizer ranks, the 15 time-reversal-even matrix
directions, all 24 proper/improper spin rotations, representative
extraction and the angular projection identities above. It supplies no
gap, linewidth, susceptibility or inversion composition.

**HYPOTHESIS:** self-consistent Te chemistry and local SOC response could
redistribute directional impurity matrix elements between these angular
channels. That hypothesis requires the actual common-frame Cd-in-HgTe
operator. **NOVELTY CANDIDATE:** no priority established; angular momentum,
time-reversal constraints and site-symmetry tensor methods are established.
