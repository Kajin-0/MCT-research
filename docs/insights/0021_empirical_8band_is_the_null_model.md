# Insight 0021: empirical temperature-dependent 8-band Kane is the null model

## Statement

A calculation that inserts empirical temperature-dependent gaps and structural parameters into an 8-band Kane Hamiltonian is already established for HgTe/CdHgTe quantum wells.

Therefore, the relevant null hypothesis for the AHC-to-Kane program is not a completely temperature-independent Hamiltonian.

It is

$$
\mathcal M_0:
\begin{cases}
E_g(T),\ \Omega_{\mathrm{VBO}}(T),\ a_L(T),\ c_{ij}(T)
&\text{temperature dependent},\\
\Delta,\ E_P,\ F,\gamma_1,\gamma_2,\gamma_3,\kappa,
\text{deformation potentials}
&\text{fixed}.
\end{cases}
$$

This model class already reproduces temperature-driven HgTe quantum-well phase transitions and magneto-optical spectra at a useful level.

## Nested alternatives

Microscopic calculations should be evaluated through nested hypotheses:

$$
\mathcal M_1=\mathcal M_0+\Delta(T),
$$

$$
\mathcal M_2=\mathcal M_1+P(T),
$$

$$
\mathcal M_{2b}=\mathcal M_1+P_8(T)+P_7(T),
$$

$$
\mathcal M_3=\mathcal M_{2b}+F(T)+\gamma_1(T)+\gamma_2(T)+\gamma_3(T).
$$

The question is not whether $\mathcal M_3$ is formally more complete. It is whether the additional parameters produce a resolved improvement in held-out observables.

## Observable tests

Candidate observables include:

1. bulk signed gap $E_g(T)$;
2. Kane velocity from bulk magnetospectroscopy;
3. conduction mass after subtracting the $E_g$-only prediction;
4. quantum-well critical temperature;
5. zero-mode Landau-level crossing field;
6. nonlocal side-maxima energies;
7. spin polarization or wavefunction character near inversion;
8. anisotropic valence-band curvature along multiple crystal directions.

The strongest comparison is not an absolute band calculation but

$$
\Delta O_j(T)
=
O_j^{\mathcal M_n}(T)
-
O_j^{\mathcal M_0}(T),
$$

with the same structural and empirical-gap inputs in both models.

## Minimum claim threshold

A non-gap temperature dependence should be called physically resolved only if:

$$
|\Delta O_j|
>
\max\left(
3\sigma_{O_j},
\epsilon_{\mathrm{num}},
\epsilon_{\mathrm{model\ discrepancy}}
\right)
$$

on a held-out observable or temperature range.

Parameter motion alone is insufficient if it lies along a poorly identifiable covariance direction or leaves all observables unchanged.

## Computation gate

Before running production AHC, the decision memo must identify:

- which nested model is being tested;
- the observable most sensitive to the added invariant;
- the expected effect size;
- the required meV or percent accuracy;
- the empirical-null uncertainty;
- the result that would stop deeper computation.

Examples:

- If $P(T)$ changes the best available transition energies by less than experimental and composition uncertainty, do not deepen the $P$ branch.
- If $P_8/P_7$ splitting produces no held-out improvement over one $P$, retain the conventional closure.
- If $\gamma_i(T)$ are not identifiable over a stable $k$ window, report bounds rather than fitted curves.

## Consequence

The candidate novelty is not “temperature-dependent 8-band Kane.”

It is a demonstrated, uncertainty-qualified rejection of $\mathcal M_0$ for at least one HgCdTe observable, with the rejection traced to a specific microscopic self-energy component.
