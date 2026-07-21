# Derivation 014: Chang thickness-pair validation design

## 1. Objective

The selected first external-validation route uses response-defined cutoff measurements at two effective absorber thicknesses. The purpose of this derivation is to determine:

1. the exact estimator for the exponential-tail energy `W`;
2. the uncertainty of that estimator when cutoff and thickness measurements are correlated;
3. the conditioning benefit of increasing the thickness ratio;
4. the maximum usable ratio imposed by tail-branch and source-energy limits;
5. the precision required for a quantitative external validation.

The result is a validation-design theorem. It is not a fit to Chang Figure 2.

## 2. Tail cutoff at one thickness

For a single-pass response

$$
R(E,d)=1-\exp[-\alpha(E)d],
$$

a fixed response criterion $R_t$ requires

$$
\alpha_t(d)=\frac{-\ln(1-R_t)}{d}.
$$

On an exponential tail,

$$
\alpha(E)=\alpha_j\exp\left(\frac{E-E_j}{W}\right),
$$

so the cutoff is

$$
E_c(d)=E_j+W\ln\left[\frac{-\ln(1-R_t)}{d\alpha_j}\right].
$$

The same material state, response criterion, and tail parameters must apply to both measurements.

## 3. Exact paired estimator

For effective thicknesses $d_1$ and $d_2$,

$$
\Delta E
=E_c(d_2)-E_c(d_1)
=-W\ln\left(\frac{d_2}{d_1}\right).
$$

Define

$$
L=\ln(d_2/d_1).
$$

Then

$$
\boxed{\hat W=-\frac{\Delta E}{L}}.
$$

The nuisance quantities $E_j$, $\alpha_j$, and the response criterion cancel from the paired difference. This cancellation is valid only when both cutoffs remain on the same exponential tail and share one material state.

## 4. Cutoff covariance

Let the two cutoff estimates have standard uncertainties $\sigma_{E_1}$ and $\sigma_{E_2}$ with correlation $\rho_E$. Then

$$
\operatorname{Var}(\Delta E)
=\sigma_{E_1}^2+\sigma_{E_2}^2
-2\rho_E\sigma_{E_1}\sigma_{E_2}.
$$

Positive correlation can be beneficial because a common energy calibration error cancels in the difference. It must be retained rather than assuming independence.

For equal uncertainties $\sigma_E$,

$$
\operatorname{Var}(\Delta E)
=2\sigma_E^2(1-\rho_E).
$$

## 5. Effective-thickness uncertainty

The relevant geometric variable is

$$
L=\ln d_2-\ln d_1.
$$

For effective-thickness uncertainties $\sigma_{d_1}$ and $\sigma_{d_2}$ with correlation $\rho_d$,

$$
\operatorname{Var}(L)
\approx
\left(\frac{\sigma_{d_1}}{d_1}\right)^2
+
\left(\frac{\sigma_{d_2}}{d_2}\right)^2
-2\rho_d
\frac{\sigma_{d_1}}{d_1}
\frac{\sigma_{d_2}}{d_2}.
$$

These uncertainties apply to effective optical thickness. Physical film thickness may be recorded separately but cannot replace effective thickness without a validated optical model.

## 6. General first-order uncertainty

With

$$
W=-\Delta E/L,
$$

the derivatives are

$$
\frac{\partial W}{\partial\Delta E}=-\frac{1}{L},
$$

and

$$
\frac{\partial W}{\partial L}
=\frac{\Delta E}{L^2}
=-\frac{W}{L}.
$$

Let

$$
C_{\Delta E,L}=\operatorname{Cov}(\Delta E,L).
$$

Then

$$
\boxed{
\operatorname{Var}(W)
=
\frac{\operatorname{Var}(\Delta E)}{L^2}
+
\frac{\Delta E^2}{L^4}\operatorname{Var}(L)
-
\frac{2\Delta E}{L^3}C_{\Delta E,L}
}.
$$

The covariance term is explicit because effective-thickness inference and energy calibration can share optical-model nuisance parameters.

When $C_{\Delta E,L}=0$, the relative variance is

$$
\boxed{
\left(\frac{\sigma_W}{W}\right)^2
=
\frac{\operatorname{Var}(\Delta E)}{W^2L^2}
+
\frac{\operatorname{Var}(L)}{L^2}
}.
$$

## 7. Conditioning versus thickness ratio

For fixed absolute cutoff uncertainty and fixed relative thickness uncertainty, every term above scales as

$$
\frac{1}{L^2}
=
\frac{1}{\ln^2(d_2/d_1)}.
$$

Therefore the relative uncertainty decreases monotonically with increasing

$$
|\ln(d_2/d_1)|.
$$

The formally best pair uses the largest thickness ratio allowed by:

- both cutoffs remaining on the exponential tail;
- the source-authorized energy interval;
- a declared margin from the source boundary;
- common material and carrier state;
- available effective-thickness calibration.

Larger ratio is not universally better if it violates any of these conditions.

## 8. Source-domain ratio bound

For $d_2>d_1$,

$$
E_2=E_1-W\ln r,
\qquad
r=d_2/d_1.
$$

Let $E_{\min}$ be the lower authorized energy and let $m_E\ge0$ be a required margin. The second cutoff must satisfy

$$
E_1-W\ln r\ge E_{\min}+m_E.
$$

Therefore

$$
\boxed{
r_{\max}
=
\exp\left[
\frac{E_1-E_{\min}-m_E}{W}
\right]
}.
$$

The largest informative ratio is the minimum of this source-domain bound and any separately derived tail-branch bound.

## 9. Declared synthetic Chang result

Use the existing source-bounded synthetic record:

```text
Eg             0.100 eV
W              0.012 eV
baseline d1    5 um
baseline E1    0.0996292713 eV
source minimum 0.080 eV
```

### Absolute source bound

With zero margin,

$$
r_{\max}=5.13342.
$$

For $d_1=5\ \mu\mathrm{m}$,

$$
d_{2,\max}=25.6671\ \mu\mathrm{m}.
$$

### Two-meV margin

With $m_E=2$ meV,

$$
r_{\max}=4.34535,
$$

and

$$
d_{2,\max}=21.7267\ \mu\mathrm{m}.
$$

### Existing 5-to-20 micrometre pair

The existing pair has

$$
r=4,
$$

$$
\Delta E=-16.6355\ \mathrm{meV},
$$

and leaves

$$
2.99374\ \mathrm{meV}
$$

above the lower source bound.

It uses:

```text
77.9% of the absolute maximum ratio
92.1% of the maximum ratio with a 2 meV margin
```

Thus the pair is close to the largest well-conditioned ratio available under the declared source limits.

## 10. Width uncertainty for one-meV cutoff precision

Assume equal independent cutoff uncertainties of 1 meV and exact thickness ratio.

For $r=4$,

$$
\frac{\sigma_W}{W}
=
\frac{\sqrt{2}(1\ \mathrm{meV})}
{(12\ \mathrm{meV})\ln4}
=0.08501.
$$

Therefore

```text
sigma_W = 1.02014 meV
relative uncertainty = 8.50%
```

If the cutoff errors have correlation $\rho_E=0.8$,

```text
sigma_W = 0.45622 meV
relative uncertainty = 3.80%
```

The result demonstrates why covariance from common spectral calibration must be exported rather than discarded.

## 11. Thickness uncertainty

Add independent 2% effective-thickness uncertainties to the independent 1 meV cutoff errors.

For $r=4$,

```text
sigma_W = 1.04911 meV
relative uncertainty = 8.74%
```

At this precision level, cutoff-energy uncertainty dominates, but effective-thickness uncertainty is not negligible and remains a separate measurement requirement.

## 12. Required cutoff precision

For equal independent per-cutoff uncertainty and exact thickness ratio,

$$
\sigma_E
=
\frac{fW|\ln r|}{\sqrt{2}},
$$

where $f$ is the target relative uncertainty in $W$.

For $W=12$ meV and $r=4$:

| target relative `W` uncertainty | required equal per-cutoff sigma |
|---:|---:|
| 5% | 0.588 meV |
| 10% | 1.176 meV |
| 20% | 2.353 meV |

With independent 2% effective-thickness uncertainty, the corresponding cutoff-error budgets become:

| target relative `W` uncertainty | required equal per-cutoff sigma |
|---:|---:|
| 5% | 0.537 meV |
| 10% | 1.152 meV |
| 20% | 2.340 meV |

A dataset cannot meet a target when thickness uncertainty alone consumes the complete variance budget.

## 13. Future-source acceptance rules

A real-source pair is accepted for the paired-tail test only when:

1. both measurements share a declared specimen or defensible common material state;
2. response criteria are identical or transformed through a validated operator;
3. effective optical thickness and uncertainty are available;
4. cutoff energies and covariance are available or audibly estimated;
5. both crossings are classified as tail branch;
6. both crossings lie inside the source-authorized energy interval with a declared margin;
7. composition, temperature, carrier state, and parameter ownership are preserved;
8. physical thickness is recorded separately from effective thickness;
9. the source does not require transferring `W`, `b`, or amplitude between specimens.

Failure of any required condition produces a rejection record, not an imputed parameter.

## 14. Controlling conclusion

> For two same-state tail cutoffs, `W` is identified directly by the cutoff difference divided by the logarithmic effective-thickness ratio. Precision improves monotonically with thickness separation, but the optimal pair is the largest ratio that remains on the tail and inside the source-authorized energy domain. In the declared Chang sensitivity case, the 5-to-20 micrometre pair uses 92.1% of the ratio available with a 2 meV source-boundary margin and supports 10% `W` precision when independent per-cutoff uncertainty is approximately 1.18 meV or smaller.
