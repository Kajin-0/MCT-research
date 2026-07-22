# Derivation 020: anchored published-tail validation

## Purpose

PR #237 established that a finite Gaussian-power tail can be made arbitrarily straight if its standardized position relative to the mean gap is unconstrained. The Chang 2004/2006 HgCdTe papers are a stronger external candidate than the Finkman figures because the experimental workflow includes photoconductive edge information or a tail-to-intrinsic join.

This derivation asks a narrower question:

> Even with the most favorable subgap placement, do the published Chang figures have enough geometric resolution to distinguish the controlled Gaussian-power curvature from a straight exponential?

No point digitization is performed before this gate.

## Controlled operator

The tested observation model is

$$
\alpha_p(E)=A\,\mathbb E[(E-G)_+^p],
\qquad
G\sim\mathcal N(\mu_G,\sigma_G^2),
\qquad p=\frac12.
$$

The source Urbach energy is used only to determine the horizontal length of an exponential trace displayed over a declared absorption interval. It is not identified with the latent Gaussian width.

## Mapping a source exponential interval into plot pixels

For a source-reported Urbach relation,

$$
\alpha(E)\propto \exp(E/W),
$$

the energy span between two absorption values is

$$
\Delta E
=W\ln\left(\frac{\alpha_{\max}}{\alpha_{\min}}\right).
$$

For panel energy width $E_{\rm panel}$ and raster width $N_x$,

$$
\Delta x_{\rm px}
=N_x\frac{\Delta E}{E_{\rm panel}}.
$$

For panel logarithmic absorption range $R_{\rm panel}$, raster height $N_y$, and trace dynamic range

$$
R=\log_{10}\left(\frac{\alpha_{\max}}{\alpha_{\min}}\right),
$$

the vertical trace span is

$$
\Delta y_{\rm px}=N_y\frac{R}{R_{\rm panel}}.
$$

The pixel coordinates are passed to the total-least-squares straightness metric implemented in `published_tail_recoverability.py`.

## Most favorable subgap placement

Within the declared Gaussian-power model, logarithmic curvature is largest near the latent mean gap. The source test therefore sets

$$
z_{\rm upper}
=\frac{E_{\rm upper}-\mu_G}{\sigma_G}=0.
$$

This is deliberately optimistic. Translating the same finite absorption interval to $z_{\rm upper}<0$ decreases its departure from the best straight line.

Failure at $z_{\rm upper}=0$ is therefore sufficient to reject publication-figure digitization as a curvature-validation path.

## Declared figure uncertainty

The calculation retains the source-conditioned convention from PR #237:

```text
trace-center uncertainty scenario       6 px
conservative three-uncertainty gate     18 px
```

Six pixels is not a measured standard deviation. It is a declared audit scenario intended to include raster quantization, line or marker width, trace overlap, and center-selection ambiguity. Source scatter, smoothing, absorption inversion, baseline uncertainty, and gap-anchor uncertainty are additional effects.

## Chang 2004 Figure 2(c)

Declared 300 dpi panel geometry:

```text
panel width                  590 px
panel height                 478 px
energy span                  0.30 eV
log absorption span          2 decades
low-temperature W            0.014 eV
```

### Optimistic broad interval

```text
alpha range                  100-4000 cm^-1
trace dynamic range          1.60206 decades
trace energy span            0.0516443 eV
horizontal trace span        101.567 px
vertical trace span          382.892 px
maximum departure at z=0     8.787 px
```

This interval exceeds the six-pixel scenario by only `1.465x` and fails the 18-pixel gate. It crosses six pixels only if

$$
z_{\rm upper}\gtrsim-0.713,
$$

which still requires a numerical standardized anchor.

### Representative interval

```text
alpha range                  100-1000 cm^-1
maximum departure at z=0     4.102 px
```

The representative interval does not reach even the one-uncertainty threshold.

## Chang 2006 Figure 2

Declared 300 dpi panel geometry:

```text
panel width                  649 px
panel height                 520 px
energy span                  0.50 eV
log absorption span          2 decades
low-temperature W            0.014 eV
```

### Optimistic broad interval

```text
alpha range                  200-4000 cm^-1
trace dynamic range          1.30103 decades
trace energy span            0.0419403 eV
horizontal trace span        54.438 px
vertical trace span          338.268 px
maximum departure at z=0     4.261 px
```

### Representative interval

```text
alpha range                  200-2000 cm^-1
maximum departure at z=0     2.769 px
```

Neither interval reaches the six-pixel scenario.

## Anchor status

Chang 2004 reports that transmissivity and photoconductivity were measured simultaneously at the same sample locations and that the photoconductive spectra were used to determine the gaps. This is experimentally valuable, but the article does not tabulate, for each Figure 2 trace:

- the numerical photoconductive gap;
- its uncertainty or covariance;
- the numerical alignment between that gap and each absorption trace.

Chang 2006/2007 provide a smooth fitted tail-to-intrinsic model and define a transition energy, but that fitted transition is not an independent measurement covariance for the latent mean gap.

Therefore the anchor requirement is not satisfied by the public article figures.

## Decision

All declared Chang traces satisfy

$$
\Delta_{\perp,\max}(z_{\rm upper}=0)<18\ \text{px}.
$$

The most favorable case reaches only `8.787 px`. Because moving deeper below the mean gap reduces curvature, no controlled subgap placement can pass the conservative gate.

**Manual digitization is not authorized.**

The validation path is simultaneously:

- figure-resolution limited;
- numerical-anchor limited;
- anchor-uncertainty limited.

## Reopening criterion

Reopen only if one of the following becomes available for the same specimen and temperature:

1. numerical absorption data with measurement covariance;
2. numerical photoconductive or independently measured gap with uncertainty;
3. sufficient raw above-gap data to fit the intrinsic branch and propagate the resulting mean-gap uncertainty;
4. a substantially higher-resolution source whose predicted departure exceeds the pre-declared uncertainty gate.

## Claim boundary

This calculation does not:

- establish Gaussian disorder as the tail mechanism;
- identify Urbach energy with `sigma_G`;
- estimate a specimen gap variance;
- convert photoconductive cutoff directly into a latent mean gap;
- treat six pixels as experimental covariance;
- authorize a manuscript.