# Conservative frozen-operator bound, source conditioned

This bounds the finite matched ACTIVATION, not a material error, full HSE
Hamiltonian or stationary screened impurity. The actual native kernel multiplier
array was not recorded in the accepted pair. Thus every numerical parity interval
is explicitly conditioned on the reviewed pinned QE7.5 NC CPU Gamma/q1 kernel,
FFT normalization and archived inputs. No original kernel readback is invented.
The original source/ELF/PP hashes and local snapshots are rechecked in
result.json. The additionally inspected exx_base source is newly pinned here;
this is not retroactive original multiplier provenance or binary disassembly.

Primary [QE7.5 exx_base.f90](https://raw.githubusercontent.com/QEF/q-e/qe-7.5/PW/src/exx_base.f90),
g2_convolution and exx_divergence, was read directly, together with the original
private vexx_k. Frozen data: a=12.2076307651Bohr>12,60³ FFT, q=k=0, e50Ry,
alpha_x=.25, erfc screening.106Bohr^-1, Gygi–Baldereschi, extrapolation=true,
no US/PAW or Coulomb truncation. Native FD weights lie in[0,1]; source Gram
defect is below the unchanged1e-8. Local potential magnetic components are
exactly zero. No new state, FFT, operator or source reconstruction is run.

## Proof of the deliberately loose bound

On the unitary FFT grid, a finite Coulomb convolution exchange map has the form

    X[D] = −alpha_x/Volume * sum_G v_G U_G D U_G†,

compressed into the NC wave basis; U_G multiplies both spin components by a
phase. Native rho products include1/Volume and FFT forward/inverse factors
give this normalization. Hence

    ||X[D]|| <= alpha_x * (sum_G |v_G|/Volume) * ||D||.

This triangle-inequality proof does NOT require v_G>=0 (the zero correction
can be signed). A wave-to-grid isometry and compression cannot increase norm.
No assumption about locality or small source-odd density is used.

Every FFT mode has integer components of absolute value<=30. For nonzero modes
the erfc factor is<=1 and extrapolation multiplier is0 or8/7. In Ry units e²=2,
G=(2pi/a)n. The full cubic box overbounds the active sphere:

    sum_{0<|n|inf<=30} 1/|n|²
       <= sum_{m=1}^30 (24m²+2)/m² < 724,
    sum_{G!=0}|v_G|/Volume
       < [16/(7*pi*a)]*724 < 46Ry.

Here pi>3 and a>12 suffice. Source density-grid G and EXX G lie within this
same box; extra unused modes only enlarge the bound.

For the zero mode, QE's regularization is a Gaussian-weighted reciprocal sum
minus e²*Volume*aa. The reciprocal term divided by Volume is bounded by46Ry.
The Gaussian physical parameter is gamma=10/ecutwfc=.2Bohr². Source aa is

    1/sqrt(gamma*pi) − (2/pi)*h*sum_{i=0}^{100000}
                          exp(−beta*((i+.5)*h)²),
    beta=gamma+1/(4*screen²)>16,  h=5/(sqrt(gamma)*100000)<.0002.

For the decreasing positive Gaussian, its finite midpoint sum times h is at
most h+integral_0^infinity exp(−beta*q²)dq <.2502. With pi>3, sqrt(pi)<2 and
1/sqrt(.2*pi)<1.3, this gives |aa|<2. Therefore the absolute zero coefficient
divided by Volume is<46+4=50Ry. The noncollinear branch has no gamma-only
factor2; nqs=1. This also covers the finite native quadrature rather than
replacing it with an asserted exact continuum integral.

The kernel L1 bound is consequently<96Ry and

    ||X[D]|| < 24*(1+1e-8)Ry.

For each activation let a_m=tr(P A_m P)/6. Actual local differences have max
operator bound.589291Ry; adding |a_m| still stays below7Ry, independently
checked for every rank/member/state. Thus ||A_m−a_m I||<32Ry with substantial
slack. Chemical subtraction gives ||C_j−a_j I||<64Ry; taking the difference
of two chemical responses gives128Ry. These constants were derived from source
and finite-grid inequalities; they are not fitted to the95.54meV leakage.

In particular ||Q(C−aI)Q|| obeys the same bound. It gives the stated.056008meV
chemical action radius and1.00163e-8meV trace radius despite nonzero reference
closure. Conditional mathematical intervals are evaluated in ordinary floating
arithmetic, with separate reconstruction/gauge residuals ~1e-12meV; no
directed-rounding or material uncertainty certificate is asserted.

## Literature / novelty boundary

Antiunitary averaging, Kramers sewing, Hermitian block completion, trace duality
and singular-value perturbation are established mathematics. Fock linearity
and ACE source-span exactness are established in
[Lin2016, sections2–3](https://math.berkeley.edu/~linlin/publications/ACE.pdf).
Native source exactness does not certify stationary density or off-span ACE.
No general new ACE, HSE, disorder mass or symmetry theory is claimed. The NEW
contribution is the actual matched response decomposition intervals, full
native-density defect norms and the precise imperfect-frame ambiguity. Historical
novelty remains UNVERIFIED; no broad or optical search is repeated.
