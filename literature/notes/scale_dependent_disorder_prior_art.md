# Prior-art audit: measurement-scale dependence of HgCdTe disorder observables

## Status

Preliminary audit. It constrains claims; it is not a novelty guarantee.

The general covariance-filter identity and Gaussian convolution are established mathematics. The relevant novelty question is narrower:

> Has HgCdTe literature explicitly linked a spatial composition covariance to a finite optical or device kernel, derived the probe-scale band-edge variance, proved the one-scale ambiguity between disorder amplitude and correlation length, and supplied a constructive multi-scale inverse?

No reviewed source presently establishes that full chain.

## Finite-aperture HgCdTe mapping

### Chang et al., 2005

**DOI:** `10.1016/j.jcrysgro.2005.01.051`

The paper maps HgCdTe composition and thickness with an infrared microscope and a variable specimen-plane aperture. It establishes that reported wafer uniformity is already a finite-resolution observable and that probe scale is experimentally adjustable.

The accessible record does not establish:

- a covariance-filter law for map variance;
- separation of point variance from aperture-averaged variance;
- recovery of correlation length from an aperture sweep;
- a one-scale no-go theorem;
- a two-scale inverse with conditioning analysis.

### Furstenberg, White, and Olson, 2005

**DOI:** `10.1007/s11664-005-0022-8`

This work reports spatially resolved photoluminescence and transmission spectra of HgCdTe and demonstrates that local optical response varies across defects and processing states. It does not, based on the accessible record, derive the explicit spatial covariance/kernel inverse.

## Optical disorder and local-gap distributions

### Herrmann et al., 1992

Herrmann shows that convolution of an intrinsic absorption edge with a Gaussian-like distribution of local gap energies can generate an approximately exponential tail. The repository reproduces the source-conditioned apparent tail scale and demonstrates fit-window dependence.

Herrmann supplies a distribution of local gap energies, not a measured spatial covariance. The fitted tail width must not be reinterpreted as a correlation length or point composition variance.

### Ivanov-Omskii et al., 2009

**DOI:** `10.1016/j.physb.2009.08.210`

The paper attributes photoluminescence redshift to excitons localized at composition fluctuations and reports processing-dependent fluctuation amplitudes. It supports the physical relevance of disorder but does not close the spatial inverse between microscopic covariance and finite-resolution measurement.

### Ruzhevich et al., 2024

**DOIs:**

```text
10.1364/JOT.91.000077
10.17586/1023-5086-2024-91-02-23-33
```

The work compares transmission, photoluminescence, scanning electron microscopy, and energy-dispersive X-ray spectroscopy and discusses carriers localized on large-scale composition fluctuations. It reinforces the need to distinguish observation operators. The accessible abstract does not present the scale-dependent covariance theorem or multi-scale recovery used here.

## Detector-cutoff prior art

### Chang et al., 2006 and 2007

**DOIs:**

```text
10.1063/1.2245220
10.1007/s11664-007-0162-0
```

These papers establish nonparabolic intrinsic absorption, an Urbach branch, and effective-thickness dependence of detector cutoff. They do not supply a spatial composition covariance or infer its correlation length from multi-resolution maps.

## Microscopic alloy correlations

### Patrick et al., 1988

**DOI:** `10.1116/1.575524`

Cluster theory addresses local alloy correlations and bond distributions. Atomic-scale cluster correlations are not automatically the mesoscopic covariance sampled by an optical aperture, carrier diffusion volume, pixel, or electrical weighting field. A coarse-graining model would be required.

## Claim classification

| Claim | Status |
|---|---|
| General covariance filtering | Established mathematics |
| Gaussian covariance/Gaussian probe closed form | Established mathematics |
| HgCdTe mapping uses finite apertures | Established experimentally |
| HgCdTe disorder shifts optical response | Established experimentally |
| Effective thickness changes detector cutoff | Established |
| Explicit HgCdTe probe-scale variance operator | Candidate application-specific contribution |
| One-scale ambiguity between point variance and correlation length | Candidate application-specific theorem statement |
| Exact multi-scale recovery and conditioning prescription | Candidate application-specific contribution |
| Quantified gap/cutoff-width change across realistic probe scales | Candidate result; presently a declared sensitivity case |

## Full-text audit priorities

Before freezing novelty language, audit:

```text
10.1016/j.jcrysgro.2005.01.051
10.1007/s11664-005-0022-8
10.1364/JOT.91.000077
```

The decisive questions are whether any source:

1. varies resolution on the same specimen;
2. reports variance as a function of aperture or point-spread function;
3. computes a spatial autocorrelation or correlation length;
4. deconvolves the measurement kernel;
5. uses two or more scales to recover a latent covariance parameter.

## Working claim boundary

Existing literature establishes finite-resolution HgCdTe mapping, spatial nonuniformity, disorder-induced optical shifts, and thickness-dependent detector cutoff. The present program adds an explicit spatial-covariance observation layer and derives the exact information content and scale design of multi-resolution disorder measurements under declared covariance and kernel models.
