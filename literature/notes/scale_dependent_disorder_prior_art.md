# Targeted prior-art audit: probe-scale dependence of HgCdTe disorder observables

## Status

**Preliminary audit, not a novelty guarantee.**

The general filtered-covariance identity is established random-field and signal-processing mathematics. The novelty question is narrower:

> Has prior HgCdTe work explicitly connected a spatial composition covariance to a finite optical/device kernel, derived the resulting probe-scale band-edge variance, proved one-scale non-identifiability of disorder amplitude and correlation length, and given a constructive multi-scale inverse?

The sources reviewed so far do not establish that combined result.

## 1. General mathematical prior art

For a stationary random field and a linear normalized measurement kernel,

```text
Var(X_a) = int int w_a(r) w_a(r') C(r-r') dr dr'
```

or, spectrally,

```text
Var(X_a) = (2 pi)^(-D) int S(k) |W_a(k)|^2 dk.
```

This is standard covariance propagation. The Gaussian-covariance/Gaussian-kernel integral is also elementary Gaussian convolution. Neither should be presented as new probability theory.

The paper must therefore claim only the application-specific HgCdTe synthesis, exact inverse design, quantitative measurement consequences, and source-grounded distinction among observables.

## 2. HgCdTe wafer mapping already establishes finite spatial probes

### Chang et al., 2005

**DOI:** `10.1016/j.jcrysgro.2005.01.051`

**Title:** Composition and thickness distribution of HgCdTe molecular beam epitaxy wafers by infrared microscope mapping

The paper develops infrared-microscope mapping of HgCdTe composition and thickness. The reported instrument uses a variable beam aperture, with the accessible beam size extending down to approximately `25 um` at a `10 um` wavelength and a `100 um` aperture selected for large-area mapping.

This is directly relevant because the reported composition map is already a finite-aperture observable. The source demonstrates the experimental feasibility of varying measurement scale and the device importance of composition uniformity.

It does **not**, based on the material reviewed so far:

- derive a covariance-filter law for the reported map variance;
- separate microscopic variance from aperture-averaged variance;
- infer a spatial correlation length by an aperture sweep;
- prove one-scale non-identifiability;
- derive a two-scale inverse.

### Furstenberg, White, and Olson, 2005

**DOI:** `10.1007/s11664-005-0022-8`

**Title:** Spatially resolved photoluminescence and transmission spectra of HgCdTe

The paper reports high-resolution scanning mid-infrared photoluminescence and transmission measurements of HgCdTe epilayers, including macrodefect and annealing effects.

This establishes that spatially resolved optical observables can be compared on HgCdTe. It does not, based on the accessible record, establish the explicit probe-kernel covariance theorem or a scale-sweep inversion for microscopic disorder amplitude and correlation length.

## 3. HgCdTe optical disorder prior art estimates energy/composition fluctuation amplitude

### Herrmann et al., 1992

The source shows that convolving an intrinsic absorption edge with a Gaussian-like distribution of local gap energies can produce an approximately exponential absorption tail over a finite dynamic range. The project already reproduced the source-conditioned apparent `W ~= s/2` scale and showed strong fit-window dependence.

Herrmann supplies a distribution of local gap energies, not a spatial covariance or correlation-length measurement. The new spatial layer must not be read back into that source.

### Ivanov-Omskii et al., 2009

**DOI:** `10.1016/j.physb.2009.08.210`

The paper uses infrared photoluminescence to estimate alloy-disorder fluctuation measures in HgCdTe and attributes PL redshift to excitons localized at composition fluctuations. Annealing reduces the inferred fluctuation amplitude.

The source supports the physical importance of compositional disorder and the distinction between PL and a nominal gap. It does not identify a measurement-kernel-dependent spatial covariance or establish a correlation length from multiple probe scales.

### Ruzhevich et al., 2024

**DOIs:**

```text
10.1364/JOT.91.000077
10.17586/1023-5086-2024-91-02-23-33
```

The paper compares transmission, photoluminescence, scanning electron microscopy, and energy-dispersive X-ray spectroscopy. It reports that optical and microscopic interpretations depend strongly on composition regime and that PL can involve carriers localized on large-scale composition fluctuations.

This is important modern evidence that different observation operators sample different disorder structures. The accessible abstract does not provide the exact spatial-filter theorem, one-scale no-go result, or two-scale inverse developed here.

## 4. Existing detector-cutoff models do not close the spatial inverse

### Chang et al., 2006 and 2007

**DOIs:**

```text
10.1063/1.2245220
10.1007/s11664-007-0162-0
```

These sources establish a nonparabolic intrinsic absorption model with an Urbach branch and show that effective absorber thickness changes the detector cutoff. The existing repository result proves a model-specific rank bound for tail-only cutoff data.

Those works do not supply a spatial composition covariance, an optical point-spread function, or a multi-resolution map from which microscopic variance and correlation length can be recovered.

## 5. Microscopic alloy-correlation theory is adjacent but not equivalent

### Patrick et al., 1988

**DOI:** `10.1116/1.575524`

Cluster theory was applied to local correlations, bond-length distributions, and phase diagrams of HgCdTe and related alloys. This is microscopic alloy-structure prior art.

Local atomic correlation predictions are not automatically the mesoscopic covariance inferred by an optical or device kernel. Any connection between atomic cluster statistics and the continuum `C_x(h)` used here would require a separate coarse-graining model.

## 6. Preliminary novelty classification

| Claim | Classification | Reason |
|---|---|---|
| General covariance-filter identity | Established | Standard linear random-field propagation |
| Gaussian/Gaussian closed form | Established mathematics | Elementary convolution |
| HgCdTe composition and thickness maps use finite apertures | Established | Chang 2005 |
| HgCdTe spatial PL/transmission mapping | Established | Furstenberg 2005 |
| Gap-distribution-induced apparent absorption tail | Established | Herrmann 1992 |
| PL shifts from compositional fluctuations | Established | Ivanov-Omskii 2009 and later work |
| Effective-thickness-dependent detector cutoff | Established | Chang 2006/2007 |
| Explicit HgCdTe probe-scale variance law tied to optical/device kernels | Candidate contribution | Not found in reviewed sources |
| Exact one-scale no-go result for `sigma_x` versus `ell` in HgCdTe measurement | Candidate contribution | Not found in reviewed sources |
| Exact two-scale recovery and conditioning design | Candidate contribution | Not found in reviewed sources |
| Quantified change in apparent HgCdTe gap/cutoff width across realistic probe scales | Candidate contribution | Requires model-bounded presentation and source-scale audit |

## 7. Highest-value source acquisitions

Before a novelty claim is frozen, obtain or audit full text for:

```text
10.1016/j.jcrysgro.2005.01.051
10.1007/s11664-005-0022-8
10.1364/JOT.91.000077
```

The critical questions are:

1. Does any source vary aperture or resolution on the same specimen and report how composition or gap variance changes?
2. Is a spatial autocorrelation function or correlation length calculated?
3. Is the instrumental point-spread function deconvolved?
4. Are map variance and microscopic composition variance distinguished?
5. Are two or more probe scales used to infer a latent correlation length?

## 8. Current claim boundary

The defensible working claim is:

> Existing HgCdTe literature establishes spatial nonuniformity, finite-aperture optical mapping, disorder-induced optical shifts, and thickness-dependent cutoff. The present work adds an explicit spatial-covariance observation layer and derives the exact information content and scale design of multi-resolution disorder measurements under declared covariance and kernel models.

This wording remains provisional until the three high-value sources above are fully audited.
