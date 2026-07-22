# Decision record: Chang anchored-tail curvature validation

**Date:** 2026-07-22  
**Program:** R03 — distributional band-edge observables  
**Controlling issue:** #254  
**Parent data issue:** #22  
**Related work:** PR #226, PR #237, PR #253

## Decision

**Terminate the Chang publication-figure digitization path for logarithmic-curvature validation.**

The Chang 2004/2006 HgCdTe papers are stronger candidates than the Finkman figures because they connect absorption to photoconductive or tail-to-intrinsic edge information. They still fail the pre-digitization gate.

## Quantitative basis

The calculation places each Gaussian-power trace at the most favorable controlled subgap location,

$$
z_{\rm upper}=0,
$$

and maps a source Urbach interval into the published panel using

$$
\Delta E=W\ln(\alpha_{\max}/\alpha_{\min}).
$$

Declared 300 dpi results:

| source scenario | maximum orthogonal departure | six-pixel ratio | 18-pixel gate |
|---|---:|---:|---:|
| Chang 2004 Figure 2(c), optimistic `100-4000 cm^-1` | 8.787 px | 1.465 | fail |
| Chang 2004 Figure 2(c), representative `100-1000 cm^-1` | 4.102 px | 0.684 | fail |
| Chang 2006 Figure 2, optimistic `200-4000 cm^-1` | 4.261 px | 0.710 | fail |
| Chang 2006 Figure 2, representative `200-2000 cm^-1` | 2.769 px | 0.462 | fail |

The optimistic Chang 2004 case crosses six pixels only when

$$
z_{\rm upper}\gtrsim-0.713,
$$

but it never reaches the conservative 18-pixel threshold for any controlled subgap placement.

Moving the window below the latent mean gap decreases the predicted departure. The values above are therefore optimistic upper bounds within the declared model.

## Anchor audit

Chang 2004 states that transmissivity and photoconductivity were measured simultaneously at the same locations and that photoconductivity was used to determine the energy gaps. The public article does not tabulate, trace by trace:

- the numerical photoconductive gap;
- its uncertainty or covariance;
- the alignment between the gap determination and the plotted absorption trace.

Chang 2006/2007 define a smooth fitted transition between Urbach and intrinsic branches, but this fitted transition is not an independent numerical mean-gap measurement with covariance.

The validation path therefore fails both requirements:

1. publication-figure curvature exceeds the pre-declared uncertainty gate;
2. an independently recoverable numerical edge anchor with uncertainty exists for the same trace.

## Scientific interpretation

This is a data and recoverability limitation, not evidence for or against Gaussian disorder in the specimens.

The source Urbach energy is used only to map the displayed exponential interval into horizontal pixels. It is not equated to the Gaussian gap width.

## Consequence for Issue #22

The Chang papers remain valuable for:

- specimen and measurement metadata;
- temperature-dependent Urbach energies;
- tail-to-intrinsic model structure;
- the existence of simultaneous photoconductive edge measurements;
- source-conditioned bounds on what a publication figure can resolve.

They do not provide the raw or tabulated spectrum and edge covariance needed for the R03 logarithmic-curvature falsification test.

Issue #22 should remain open for numerical data acquisition. It should not be satisfied by digitizing these figures.

## Reopening conditions

Reopen the Chang path only if the following become available for the same specimen and temperature:

- raw or tabulated absorption values;
- numerical photoconductive or independent gap values;
- uncertainty or covariance for both;
- preprocessing and absorption-inversion details sufficient to propagate uncertainty.

An author-provided data file, thesis appendix, institutional repository deposit, or machine-readable supplement would satisfy the source form if the required metadata are present.

## Manuscript consequence

No manuscript is authorized.

The R03 theorem remains a bounded analytical result, but no audited historical HgCdTe spectrum currently supplies an externally anchored curvature test.

## Stop rule

Do not perform manual point extraction from Chang 2004/2006/2007 for this claim unless a new source changes the anchor or uncertainty information. Further synthetic enlargement of the same figure scenarios is not decision-changing.