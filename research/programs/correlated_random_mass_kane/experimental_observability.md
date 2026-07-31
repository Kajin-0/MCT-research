# R05 Phase 0 experimental observability gate

**Controlling issue:** #390  
**Status:** experiment-design screening; no experimental feasibility claim  
**Current decision:** no candidate observable yet passes the quantitative addressability gate

## 1. Characteristic energy and length scales

The finite-correlation propagation scale is

\[
E_\xi=\frac{\hbar v_K}{\xi}.
\]

Using the source-bounded nominal velocity

```text
hbar v_K = 0.7042868 eV nm,
```

| `xi` | `E_xi` |
|---:|---:|
| `10 nm` | `70.4 meV` |
| `50 nm` | `14.1 meV` |
| `100 nm` | `7.04 meV` |
| `200 nm` | `3.52 meV` |
| `500 nm` | `1.41 meV` |
| `1000 nm` | `0.704 meV` |

A coherent random-mass feature cannot be assumed to have width `E_xi`; its actual width must come from the oracle. For screening, define

\[
E_{\rm feature}
=\min(E_\xi,\sigma_M,E_{\rm oracle}),
\]

where `E_oracle` is the numerically observed width after convergence but before experimental convolution.

The provisional resolution requirement is

\[
\delta E_{\rm exp}\le0.25E_{\rm feature}.
\]

This is a design criterion, not an established instrument law.

## 2. Thermal resolution

Boltzmann broadening is

\[
k_BT=0.0861733\,T\ \mathrm{meV}.
\]

Representative values:

| `T` | `k_B T` | `3.5 k_B T` |
|---:|---:|---:|
| `0.3 K` | `0.0259 meV` | `0.0905 meV` |
| `1 K` | `0.0862 meV` | `0.3016 meV` |
| `4 K` | `0.3447 meV` | `1.206 meV` |
| `20 K` | `1.723 meV` | `6.033 meV` |
| `77 K` | `6.635 meV` | `23.22 meV` |

For differential tunneling conductance, the Fermi-derivative width is of order `3.5 k_B T`; modulation voltage, lifetime broadening, and inhomogeneous contact potentials add further convolution.

Consequently:

- a `1 meV` DOS feature generally requires a sub-kelvin tunneling experiment;
- a `5–10 meV` feature may be thermally accessible at a few kelvin;
- a narrow low-energy feature is unlikely to remain distinct at `77 K` unless it is much wider than the exploratory mass-disorder scales.

## 3. Candidate observable table

| Observable | Required specimen regime | Required resolution | Candidate correlated signal | Matched scalar-null prediction | Principal confounders | Current gate |
|---|---|---|---|---|---|---|
| Planar tunneling DOS | homogeneous near-critical bulk or thick epilayer; low carrier density; controlled surface/contact | `delta_E_exp <= 0.25 E_feature`; usually `T <= 1–4 K` depending scale | excess or altered scaling of low-energy DOS relative to the scalar linear law | for smooth `P(M)`, `rho_scalar(E) ~ |E| P(0)/(hbar v_K)` | surface accumulation, band bending, contact barrier distribution, Coulomb gap, charged impurities, lifetime broadening | `POTENTIALLY_DISCRIMINATING`, no public qualifying dataset identified |
| Scanning tunneling spectroscopy | cleavable or stable HgCdTe surface representative of bulk; `xi` above lateral resolution | lateral resolution `<= xi/3`; field of view `>= 10 xi`; energy requirement as above | spatially correlated near-zero spectral weight tied to mass-sign or gradient structure | independent local spectra follow local homogeneous gap distribution without coherent interface excess | surface reconstruction, oxidation, tip-induced band bending, surface states, finite-depth sensitivity | `HIGH_RISK`; bulk representativeness unresolved |
| Far-infrared optical conductivity | near-critical specimen, low free-carrier absorption, known thickness and dielectric background | spectral resolution `<= 0.25 E_feature`; temperature low enough that phonon/free-carrier broadening is subordinate | modified low-frequency absorption or conductivity beyond scalar gap convolution | weighted incoherent average of homogeneous Kane optical responses | optical matrix elements, heavy-hole flat band, Drude response, phonons, thickness fringes, carrier filling | `REQUIRES_FULL_KANE_RESPONSE`; DOS alone is insufficient |
| Magneto-optical Landau spectroscopy | established massless-Kane specimen regime; field and temperature sweep | line-position/shape uncertainty below `0.25 E_feature`; field inhomogeneity below predicted disorder effect | non-scalar line-shape, transition-dependent broadening, or low-field spectral weight | scalar mixture of homogeneous Landau-transition spectra | field inhomogeneity, carrier-density distribution, strain, conventional lifetime broadening, unresolved transitions | `MOST_ESTABLISHED_PLATFORM`, but requires magnetic full-Kane disorder theory |
| Low-temperature transport | near charge neutrality; multiple geometries and lengths | energy/temperature scale below feature; geometry sufficient for finite-size scaling | nonlocal or length-dependent response associated with coherent mass structure | effective-medium/local-gap transport without coherent interface contribution | charged impurities, mobility disorder, contacts, puddles, phonons, parallel surface conduction | `NOT_PRIMARY`; inverse problem too nonunique for Phase 0 |
| Spatially resolved optical spectroscopy | epilayer with `xi` above optical/near-field resolution | lateral resolution `<= xi/2`; calibrated depth kernel; energy requirement as above | cross-correlation between local spectral feature and independently mapped composition/mass proxy | local spectrum predicted only by local gap and measurement kernel | probe convolution, depth averaging, strain, defects, carrier-density variation | `CONCEPTUALLY_STRONG`, no qualifying public dataset identified |

## 4. Tunneling-DOS discrimination protocol

The scalar Gaussian null has the exact low-energy form

\[
\rho_{\rm scalar}(E)
=\frac{|E|P(0)}{\hbar v_K}+O(|E|^3).
\]

A tunneling experiment would be discriminating only if the correlated model predicts, after all convolution:

1. a statistically stable departure from this linear law over a finite energy interval;
2. an integrated effect `Delta_1 > 0.10`;
3. an effect larger than uncertainty in contact background subtraction and local carrier density;
4. a feature reproducible across at least two specimen regions or specimens;
5. a null comparison using the independently characterized one-point gap distribution.

A finite zero-bias conductance alone is not decisive because contacts, surface states, thermal broadening, and charged-disorder puddles can produce the same qualitative observation.

## 5. Magneto-optical discrimination protocol

Magneto-optics is experimentally established for massless Kane HgCdTe, but the R05 calculation would need to predict more than generic line broadening.

A useful signature must be one of:

- transition-index-dependent broadening not reproducible by a scalar mass distribution;
- correlated transfer of oscillator strength among transitions;
- low-field spectral weight from coherent mass structure with a fixed field scaling;
- a covariance-sensitive line-shape asymmetry surviving thickness, carrier, and instrument convolution.

Required null:

\[
S_{\rm scalar}(\omega,B)
=\int dM\,P(M)S_{\rm hom}(\omega,B;M),
\]

with identical temperature, carrier filling, linewidth model, thickness, and optical kernel.

This observable cannot be computed from DOS alone. It requires Landau quantization, multiband wavefunctions, optical matrix elements, and a disorder treatment compatible with the magnetic field.

## 6. Spatial discrimination protocol

A direct spatial experiment is scientifically strongest because it can compare local mass proxies and local spectroscopy while preserving correlation information.

Minimum design:

```text
lateral point-spread width <= xi/2
field of view >= 10 xi in each mapped direction
sample spacing <= xi/3
at least 3 independently calibrated effective spatial scales
measured depth sensitivity
full same-raster covariance
independent composition/strain/carrier-density covariates
```

The R04 finite-kernel and correlated-map machinery should be used to determine whether `xi` is identifiable before R05 interprets any spectrum.

## 7. Public-data boundary

The bounded audit identified:

- direct HgCdTe massless-Kane optical and magneto-optical experiments;
- HgCdTe alloy-disorder photoluminescence evidence away from the critical composition;
- no public near-critical dataset containing both a calibrated spatial covariance length and a low-energy DOS or equivalent local spectral observable.

Therefore no existing public dataset presently supports direct R05 validation.

## 8. Experimental convolution requirement

For every candidate model spectrum, save:

```text
unbroadened converged model
numerical-estimator kernel and width
thermal kernel
instrument kernel
lifetime/background model
fully convolved correlated spectrum
fully convolved matched scalar spectrum
Delta_1 and Delta_infinity before and after each convolution
```

The activation statistic is evaluated only after all plausible experimental kernels are applied.

## 9. Addressability decision

```text
tunneling DOS: potentially discriminating, no qualified dataset or specimen protocol
magneto-optics: established platform, but full-Kane magnetic response required
optical conductivity: potentially useful, DOS-only oracle insufficient
spatial spectroscopy: conceptually strongest, source and instrument specification absent
transport: too confounded for the first activation claim
```

Current experimental-addressability gate:

```text
FAIL_NOT_YET_QUANTIFIED
```

The minimal numerical oracle may proceed only to determine whether any feature is large enough to justify a concrete experimental design. It does not presently support `ACTIVATE_R05`.