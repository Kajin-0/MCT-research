# Hansen and successor-equation primary-source acquisition log

## A. Hansen 1982

**Target:** G. L. Hansen, J. L. Schmit, and T. N. Casselman, “Energy gap versus alloy composition and temperature in HgCdTe,” *Journal of Applied Physics* **53**(10), 7099-7101 (1982), DOI `10.1063/1.330018`.

**Acquisition date:** 2026-07-16  
**Current outcome:** primary full text acquired from a repository-owner upload and audited; exact source hash recorded in `literature/papers/README.md`.  
**SHA-256:** `aa8017a8f3e136a0b893619e836e8808002b9889119c8e809536e94ebd557357`.

### Primary-source facts now verified

- The paper compiles optical-absorption and magneto-optical results and states that data from 22 studies were used.
- The fit-support region is stated as approximately `0 <= x <= 0.6`, plus the CdTe endpoint `x=1`, over `4.2 <= T <= 300 K`.
- The published expression is

  $$
  E_g(x,T)=-0.302+1.93x-0.810x^2+0.832x^3
  +5.35\times10^{-4}T(1-2x).
  $$

- The reported standard error of estimate is `0.013 eV`, at least 15% better than the earlier expressions compared by the authors.
- The fitting sequence is explicit:
  1. regress $E_g$ versus $T$ for each temperature-dependent sample;
  2. fit $\partial E_g/\partial T$ linearly versus composition;
  3. normalize each sample to 80 K;
  4. perform a nonlinear least-squares fit of the 80 K composition dependence.
- Optical data used nonuniform operational edges, including approximately `alpha=500 cm^-1`, `alpha=1000 cm^-1`, detector half-peak cutoff, and 50% detector cutoff criteria.
- Composition was not measured by one common method: the source studies used density, vendor-reported composition tied to optical cutoff and destructive chemistry, and revised transmission-cutoff estimates.
- Four low-composition Schmit-Stelzer samples were excluded because of mercury inclusions.
- The authors explicitly caution that the true composition dependence above approximately `x=0.6` is conjectural even though the equation spans the full nominal alloy range.

### Remaining reconstruction work

- transcribe every source study and specimen into a provenance-controlled table;
- separate optical cutoff energy from magneto-optical bandgap measurements;
- recover source-specific composition uncertainties and corrections;
- reproduce the stated `0.013 eV` standard error from the reconstructed data;
- determine implicit weighting and leverage of the HgTe and CdTe endpoints;
- quantify coefficient covariance, which is not reported in a modern uncertainty format;
- evaluate residuals by measurement class, composition, and temperature.

## B. Laurenti 1990

**Target:** J. P. Laurenti, J. Camassel, A. Bouhemadou, B. Toulouse, R. Legros, and A. Lusson, “Temperature dependence of the fundamental absorption edge of mercury cadmium telluride,” *Journal of Applied Physics* **67**(10), 6454-6460 (1990), DOI `10.1063/1.345119`.

**Acquisition date:** 2026-07-16  
**Current outcome:** primary full text acquired from a repository-owner upload and audited; exact source hash recorded in `literature/papers/README.md`.  
**SHA-256:** `1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea`.

### Primary-source facts now verified

- The authors measured cadmium-rich LPE HgCdTe samples with `0.5 <= x <= 1` from approximately 2 to 300 K and combined them with selected Hg-rich and endpoint literature data.
- Temperature-dependent measurements used transmission, often analyzed through the first derivative of absorption.
- The fundamental nonexcitonic edge was extracted with a three-dimensional direct-allowed exciton model.
- The authors report transition-energy accuracy better than approximately `3 meV` despite temperature-dependent broadening.
- For one inherited Scott dataset, nominal compositions were adjusted to account for about 2% composition uncertainty; the reported best overall correction was about 2.3%.
- The primary typeset equation directly verifies the nonlinear composition-dependent Varshni form currently implemented in the repository.
- The authors state a nominal validity range `0 <= x <= 1` and `0 <= T <= 500 K`.
- The equation predicts a temperature-independent gap near `x=0.505`.
- The paper also uses a simplified three-band $k\cdot p$ model to derive composition- and temperature-dependent effective masses.

### Remaining reconstruction work

- recover the complete numerical dataset behind every plotted composition and temperature series;
- trace the Hg-rich and endpoint values to their original papers and measurement definitions;
- reconstruct the least-mean-squares objective, effective weighting, and residual distribution;
- distinguish directly measured LPE specimens from literature-compiled values;
- propagate composition uncertainty rather than applying only deterministic composition corrections;
- determine whether the nominal `0-500 K` validity claim is supported by data or partly extrapolative.

## C. Krishnamurthy et al. 1995

The closest historical electron-phonon calculation has also been acquired and audited; its exact source hash is recorded in `literature/papers/README.md`. Its method and novelty implications are audited in `literature/notes/krishnamurthy_1995.md`.

## Research rule

Primary-source acquisition resolves bibliographic and methodological uncertainty, but it does not by itself reconstruct the underlying data or reproduce the published fits. All later claims must distinguish:

1. visually verified statements from the papers;
2. newly reconstructed datasets;
3. repository calculations;
4. inferences not stated by the original authors.
