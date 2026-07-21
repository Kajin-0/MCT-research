# Decision record: Chang thickness-dependent cutoff identifiability

**Date:** 2026-07-21  
**Issue:** #173  
**Status:** candidate controlling result pending PR validation

## Decision

Promote the source-bounded Chang 2006 nonparabolic-Urbach shape from an edge-fit sensitivity candidate to a forward single-pass detector-cutoff operator.

Authorize the operator for:

1. analytical thickness and response-criterion sensitivity;
2. synthetic identifiability analysis;
3. comparison of latent edge, absorption threshold, and detector cutoff definitions;
4. experimental-design guidance.

Do not authorize it as quantitative validation of Chang Figure 2 or as a production detector model.

## Forward response model

Use

$$
R(E,d)=1-\exp[-\alpha(E)d]
$$

with declared effective absorbing thickness $d$.

A target response requires

$$
\alpha_t=\frac{-\ln(1-R_t)}{d}.
$$

On an exponential tail,

$$
E_c=E_j+W\ln(\alpha_t/\alpha_j).
$$

Therefore

$$
E_c(d_2)-E_c(d_1)=-W\ln(d_2/d_1).
$$

## Significant analytical result

For the Chang tail branch, write

$$
E_{c,i}=C(\theta)+W L_i,
$$

where

$$
\theta=(E_g,W,\ln A,\ln b)
$$

and

$$
L_i=\ln[-\ln(1-R_i)]-\ln d_i.
$$

Every Jacobian row is a linear combination of $\nabla C$ and $\nabla W$. Hence

$$
\boxed{\operatorname{rank}(J_{\mathrm{tail}})\le2}.
$$

No number of tail-only thickness or response measurements can separately identify $E_g$, $W$, amplitude, and $b$.

## Synthetic reference

Declared parameters:

```text
Eg         0.100 eV
W          0.012 eV
b          0.100 eV
amplitude  50000 cm^-1
E_join     0.106 eV
alpha_join 2357.327 cm^-1
```

At 50% single-pass response:

```text
thickness   energy       wavelength   branch
1 um        147.269 meV   8.419 um     intrinsic
2 um        112.794 meV  10.992 um     intrinsic
5 um         99.629 meV  12.445 um     tail
10 um        91.312 meV  13.578 um     tail
20 um        82.994 meV  14.939 um     tail
```

The source-valid 5-to-20 um change shifts the apparent cutoff by

```text
-16.636 meV
+2.494 um
```

without changing the latent `Eg`.

A full thickness decade on a 12 meV tail corresponds to

```text
-W ln(10) = -27.631 meV
```

although such a decade may leave the source-authorized relative-energy domain.

## Identifiability calculations

### Tail-only design

Nine source-valid tail cutoffs give singular values

```text
4.7561439
1.0049619
1.92e-12
9.75e-13
```

and numerical rank two, matching the structural proof.

### Mixed tail/intrinsic design

Ten cutoffs spanning both branches give

```text
4.5297860
0.7024186
0.1983685
0.0226704
```

with rank four but condition number

```text
199.81
```

Intrinsic observations restore local rank, but the inversion remains weak in one parameter direction.

## Authorized conclusions

- Detector cutoff is a thickness- and criterion-dependent observation operator.
- Tail-only cutoff datasets identify at most two combinations of `Eg`, `W`, amplitude, and `b`.
- More tail-only points improve precision but do not remove structural non-identifiability.
- Intrinsic-branch measurements are necessary for local full rank.
- Full rank does not imply a robust inversion.
- Effective thickness and response criterion must be preserved as measurement provenance.

## Unauthorized conclusions

- The synthetic parameters are not inferred for Chang Figure 2 or another real specimen.
- The `x=0.23`, `b=103+/-2 meV` source value is not transferred to the `x=0.21` figure.
- Effective absorbing thickness is not automatically physical film thickness.
- Reflection, interference, multiple passes, collection efficiency, and carrier transport are not included.
- No universal material-gap or detector-cutoff correction is identified.

## Validation gates

Merge requires:

- exact inversion of the single-pass Beer-Lambert response;
- analytical and numerical tail-cutoff agreement;
- exact logarithmic thickness shift;
- source-domain fail-closed behavior;
- tail/intrinsic branch classification;
- numerical confirmation of tail-only rank two;
- numerical confirmation of mixed-design rank four and conditioning;
- public API and complete CI success on Python 3.11 and 3.13.

## Next decision

After merge, use the result to design a real-spectrum or multi-thickness validation target. If no source supplies calibrated spectra and effective-thickness provenance, retain the Chang result as a synthetic structural-identifiability theorem and proceed to the Dingrong carrier-filled branch.
