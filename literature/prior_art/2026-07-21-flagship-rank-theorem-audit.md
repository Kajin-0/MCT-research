# Flagship rank-theorem prior-art audit

## Scope

This audit fixes the novelty boundary for the manuscript:

> From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability.

It addresses two model-specific results:

1. the unmarked distributed spectrum depends on five nominal parameters through only `Eg0+Delta`, `sigma_G`, and `A*d`, so `rank(J)<=3`;
2. any number of tail-only Chang cutoff observations has rank at most two for `(Eg,W,ln A,ln b)`.

The audit is targeted, not a legal novelty opinion. A closer source can revise any yellow or green classification.

## General mathematical prior art

### Structural identifiability is established

Bellman and Astrom introduced structural identifiability as the question of whether a model's internal parameters can be recovered uniquely from ideal input-output observations.

- DOI: `10.1016/0025-5564(70)90132-X`

The manuscript must therefore say that it **applies** structural-identifiability analysis. It must not claim to introduce the concept.

### Parameter symmetries are established

Output-preserving transformations are an established route to diagnosing structural non-identifiability.

- Yates, Evans, and Chappell: `10.1016/j.automatica.2009.07.009`

The project's explicit scaling and translation transformations are model-specific instances of established symmetry logic.

### Identifiable parameter combinations are established

Recovering combinations rather than individual parameters is established identifiability methodology.

- Eisenberg and Hayashi: `10.1016/j.mbs.2014.08.008`

The specific combinations in the HgCdTe model can be a contribution. The general idea cannot.

## Optical inverse-problem prior art

### Beer-Lambert product structure

Beer-Lambert attenuation depends on an absorption scale and optical path length through a product.

- IUPAC definition: `10.1351/goldbook.B00626`

Therefore the `A*d` invariance is not new physics. Its role inside the complete distributed HgCdTe model remains useful and should be stated as an inherited optical-depth degeneracy.

### Thin-film optical inversion

Prior optical-metrology studies recover refractive index, extinction coefficient, and thickness only after adding constraints or additional observables such as reflectance, interference structure, angle, and polarization.

- transmission inversion with constraints: `10.1364/AO.36.008238`;
- measurement-combination error analysis: `10.1364/AO.40.002675`;
- criteria for precise and unambiguous `n,k,d`: `10.1364/AO.40.002682`;
- effective absorption and effective thickness in ATR: `10.1364/OL.418277`.

These sources support the manuscript's measurement-design logic. They do not state the same reduced HgCdTe parameter combinations.

## HgCdTe prior art

### Herrmann tail mechanism

Herrmann et al. established that a distribution of local gaps can generate a near-exponential apparent tail.

- DOI: `10.1016/0022-0248(92)90851-9`

Prior art includes the mechanism and approximately-`s/2` source scale. It does not include the repository's `60.1%` fit-window result or the stated inversion interval across the declared operator family.

### Chang nonparabolic-Urbach model and cutoff thickness

Chang 2006 and 2007 establish:

- a nonparabolic intrinsic absorption branch joined to an Urbach tail;
- the importance of effective absorber thickness for detector cutoff;
- the distinction between effective and physical absorber thickness.

DOIs:

- `10.1063/1.2245220`;
- `10.1007/s11664-007-0162-0`.

Chang does not state a Jacobian-rank theorem for tail-only cutoff data. Figure 1 in the 2007 paper is calculated and is not an independent multi-thickness experimental validation series.

The exact logarithmic shift follows directly from the source tail plus single-pass response and is not presented as a new physical discovery. The formal rank-two consequence is retained as a model-specific analytical result.

### Dingrong carrier-filled edge

Dingrong et al. establish finite-temperature carrier filling and free-carrier absorption in a real degenerate specimen.

- DOI: `10.1016/0038-1098(85)90315-1`

The repository's source-table consistency result is separate prior-art-free work: the printed equation and printed `P=8.0e-8 eV cm` miss the four Table 1 Fermi elevations by `11.297 meV` RMS, while the rounded rows imply a clustered diagnostic value near `8.51e-8 eV cm`.

That value is not a replacement material constant.

## Claim-level novelty decision

### Red: established ingredients

Do not claim novelty for:

- structural identifiability as a concept;
- parameter symmetries;
- identifiable parameter combinations;
- the Beer-Lambert absorption/path-length product;
- thickness-dependent detector cutoff;
- the logarithmic tail shift as standalone physics;
- Gaussian-gap distributions producing near-exponential tails.

### Yellow: application-specific analytical synthesis

Use cautious novelty language for:

- the explicit HgCdTe combination `Eg0+Delta_carrier`;
- the combined rank-three bound for `(Eg0,Delta,ln sigma_G,ln A,ln d)`;
- the marked-model combined null vector;
- the tail-only Chang rank-two bound;
- transition-root censoring in the declared near-inversion model.

These results were not found at comparable HgCdTe specificity in the audited corpus, but their mathematics uses established identifiability and symmetry principles.

### Green: project-specific quantitative findings

The strongest defensible project-specific findings are:

- the machine-precision five-parameter spectral counterexample;
- the `60.1%` fit-window displacement of apparent tail energy;
- mixed-branch rank restoration with condition number `199.81` in the declared design;
- the Dingrong printed-parameter/Table 1 inconsistency;
- the source-conditioned measurement requirements implied by the exact combinations.

Green does not mean exhaustive global novelty has been proven.

## Publication framing decision

The paper should be framed as:

> an HgCdTe-specific semiconductor optical-metrology and inverse-problem methods paper.

It should not be framed as:

- new general mathematical theory of structural identifiability;
- a new universal HgCdTe bandgap equation;
- a complete microscopic absorption theory;
- a fully externally validated detector model.

The central contribution is the combination of source-grounded HgCdTe operators into one forward hierarchy, followed by exact identification of the parameter combinations and external measurements required for latent-gap recovery.

## Manuscript-safe language

Preferred:

> We derive model-specific structural-identifiability bounds for a distributional HgCdTe band-edge operator and connect them to source-grounded absorption, carrier, and detector-cutoff examples.

Avoid:

> We introduce a new structural-identifiability theory for optical spectroscopy.

Preferred:

> The reduced single-pass model inherits the standard optical-depth product degeneracy, while the HgCdTe-specific gap/carrier translation and combined rank bound determine which additional measurements are required.

Avoid:

> We discover that amplitude and thickness cannot be separated.

Preferred:

> No audited HgCdTe source states the tail-only rank-two bound at comparable specificity; we therefore present it as an application-specific analytical result rather than unprecedented general mathematics.

## Submission consequence

The manuscript can support a methods-paper submission after:

1. integrating the Dingrong source-table result;
2. updating the bibliography with the general identifiability and optical-inversion sources;
3. preserving the audited claim language in abstract, introduction, discussion, and conclusions;
4. deciding whether a digitized real spectrum is required by the selected journal.
