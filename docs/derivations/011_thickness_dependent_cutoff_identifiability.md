# Derivation 011: thickness-dependent detector cutoff and identifiability

## 1. Scope

This derivation connects a declared absorption coefficient to a single-pass detector response and then to an operational cutoff. It uses the source-bounded Chang nonparabolic-Urbach shape as one forward model, but the core tail-branch results apply to any exponential absorption tail.

The model excludes reflection, interference, collection-efficiency variation, carrier transport, and multiple passes. The thickness variable is an effective absorbing thickness.

## 2. Single-pass response

For absorption coefficient $\alpha(E)$ and effective thickness $d$,

$$
R(E,d)=1-\exp[-\alpha(E)d].
$$

A target response $0<R_t<1$ requires

$$
\boxed{
\alpha_t(d,R_t)=\frac{-\ln(1-R_t)}{d}
}.
$$

Thus a response-defined cutoff is an absorption-threshold crossing whose threshold changes inversely with thickness.

For $R_t=1/2$,

$$
\alpha_{50}=\frac{\ln2}{d}.
$$

## 3. Exponential tail crossing

Let the tail join the intrinsic branch at $(E_j,\alpha_j)$ and obey

$$
\alpha(E)=\alpha_j
\exp\left(\frac{E-E_j}{W}\right),
\qquad E<E_j.
$$

Solving $\alpha(E_c)=\alpha_t$ gives

$$
\boxed{
E_c
=E_j+W\ln\left(\frac{\alpha_t}{\alpha_j}\right)
}.
$$

Substituting the single-pass threshold,

$$
E_c
=E_j+W\left[
\ln[-\ln(1-R_t)]-\ln d-\ln\alpha_j
\right].
$$

This equation establishes that detector cutoff is not a direct scalar bandgap measurement.

## 4. Thickness sensitivity

For two thicknesses at the same response criterion,

$$
\boxed{
E_c(d_2)-E_c(d_1)
=-W\ln\left(\frac{d_2}{d_1}\right)
}.
$$

One decade of thickness changes the cutoff by

$$
\boxed{
\Delta E_{\mathrm{decade}}=-W\ln10
}.
$$

For the declared synthetic width

$$
W=12\ \mathrm{meV},
$$

this becomes

$$
\Delta E_{\mathrm{decade}}=-27.631\ \mathrm{meV}.
$$

This is an observation-operator scale, not a change in the latent material gap.

## 5. Response-criterion sensitivity

At fixed thickness,

$$
E_c(R_2)-E_c(R_1)
=W\ln\left[
\frac{-\ln(1-R_2)}{-\ln(1-R_1)}
\right].
$$

Therefore changing a reported cutoff from 10% response to 50% or 90% response moves the cutoff even when the specimen and latent band structure are unchanged.

## 6. Chang branch

The continuity-normalized Chang operator uses

$$
E_j=E_g+\frac{W}{2}
$$

and

$$
\alpha_j=A\,S_j(E_g,W,b),
$$

where $S_j$ is the intrinsic nonparabolic shape evaluated at the join and $A$ is a positive amplitude.

For a tail crossing,

$$
E_c
=E_g+\frac{W}{2}
+W\left[
\ln q-\ln d-\ln A-\ln S_j(E_g,W,b)
\right],
$$

with

$$
q=-\ln(1-R_t).
$$

Define

$$
C(\theta)
=E_g+\frac{W}{2}
-W\ln A
-W\ln S_j(E_g,W,b),
$$

where

$$
\theta=(E_g,W,\ln A,\ln b).
$$

Then every tail observation has the form

$$
\boxed{
E_{c,i}=C(\theta)+W L_i
}
$$

with

$$
L_i=\ln q_i-\ln d_i.
$$

## 7. Structural rank theorem for tail-only cutoffs

Differentiate:

$$
\frac{\partial E_{c,i}}{\partial\theta}
=
\nabla_\theta C
+L_i\nabla_\theta W.
$$

Every Jacobian row is a linear combination of only two vectors:

$$
\nabla_\theta C
\quad\text{and}\quad
\nabla_\theta W.
$$

Therefore

$$
\boxed{
\operatorname{rank}(J_{\mathrm{tail}})\le2
}.
$$

This remains true for any number of thicknesses and response criteria, provided every crossing remains on the same exponential tail.

Consequences:

- $W$ can be identified from the slope against $\ln(q/d)$;
- one intercept combination can be identified;
- $E_g$, amplitude, and $b$ cannot be separated from tail cutoffs alone;
- collecting more tail-only cutoff points improves precision but does not remove structural non-identifiability.

## 8. Synthetic Chang reference

The declared synthetic parameters are

```text
Eg       = 0.100 eV
W        = 0.012 eV
b        = 0.100 eV
amplitude= 50000 cm^-1
E_join   = 0.106 eV
alpha_join = 2357.327 cm^-1
```

For 50% single-pass response:

| effective thickness | cutoff energy | cutoff wavelength | branch |
|---:|---:|---:|---|
| 1 um | 147.269 meV | 8.419 um | intrinsic |
| 2 um | 112.794 meV | 10.992 um | intrinsic |
| 5 um | 99.629 meV | 12.445 um | tail |
| 10 um | 91.312 meV | 13.578 um | tail |
| 20 um | 82.994 meV | 14.939 um | tail |

The 5-to-20 um change is a thickness ratio of four. The analytical prediction is

$$
-W\ln4=-16.636\ \mathrm{meV},
$$

which agrees with the numerical Chang crossing. The corresponding wavelength shift is approximately

$$
2.494\ \mu\mathrm m.
$$

At 50 um, the 50% crossing falls below the authorized Chang relative-energy domain $E-E_g=-20$ meV. It is therefore rejected rather than extrapolated.

## 9. Tail-only numerical rank

For nine source-valid tail crossings spanning multiple thicknesses and response criteria, the numerical singular values for parameters

$$
(E_g,W,\ln A,\ln b)
$$

are

```text
4.7561439
1.0049619
1.92e-12
9.75e-13
```

The numerical rank is exactly two at the declared tolerance, confirming the analytical structural-rank result.

## 10. Mixed-branch design

A design including both tail and intrinsic crossings gives singular values

```text
4.5297860
0.7024186
0.1983685
0.0226704
```

and local rank four. However,

$$
\kappa(J)=199.81.
$$

Thus intrinsic observations can restore local identifiability, but the weakest parameter direction remains approximately 200 times smaller than the strongest.

Full rank is not equivalent to a robust inversion.

## 11. Experimental-design consequences

A cutoff campaign intended to infer material parameters should:

1. include cutoffs on both tail and intrinsic branches;
2. vary thickness and response level sufficiently to move the crossing across the join;
3. independently constrain effective thickness;
4. retain the absolute absorption amplitude or an equivalent calibration;
5. report the response criterion explicitly;
6. avoid treating repeated tail-only cutoffs as independent identification of $E_g$, $A$, and $b$.

A calibrated full spectrum is substantially more informative than one cutoff per specimen.

## 12. Claim boundaries

The result does not establish that:

- the synthetic parameters describe Chang Figure 2;
- physical film thickness equals effective absorbing thickness;
- the single-pass model captures reflection, interference, transport, or collection efficiency;
- one response cutoff determines the latent material gap;
- the external $x=0.23$ value of $b$ is transferable to another specimen.

The authorized result is:

> Detector cutoff is a thickness- and criterion-dependent observation operator. Tail-only cutoff measurements have structural rank at most two, regardless of how many are collected.
