# Candidate-facility contact questions for paired HgCdTe acquisition

Version: 1.0  
Parent feasibility package: `hgcdte_paired_gap_feasibility_v1`  
Candidate landscape: `hgcdte_paired_gap_public_candidates_2026-07-20`

## 1. Use of this document

These questions convert public capability evidence into the documentary evidence required by the feasibility audit.

A public webpage can identify a plausible facility. It cannot establish:

- willingness to accept HgCdTe specimens;
- actual access or schedule;
- specimen geometry compatibility;
- uncertainty on the requested measurement;
- native-data and covariance release;
- data or publication rights;
- absence of state-altering processing;
- project cost.

Responses should be stored under stable evidence identifiers. A verbal answer without a dated written record remains conditional.

## 2. Common questions for every organization

1. Are you currently accepting external academic or independent-research projects involving HgCdTe?
2. Are mercury-bearing semiconductor specimens permitted under your safety and shipping procedures?
3. What specimen dimensions, thicknesses, substrates, mounts, surface conditions, and contact patterns are accepted?
4. What preparation, coating, polishing, contacting, annealing, cleaning, or remounting is required?
5. Which steps are destructive or may change carrier density, vacancy state, optical response, surface chemistry, or strain?
6. Can the same physical specimen and registered area be returned for the second optical modality?
7. What quantity is measured directly, and what quantity is inferred through a model or calibration?
8. What calibration standards, traceability, uncertainty budget, and quality-control measurements are available?
9. Can at least two native technical repeats be delivered before averaging or background correction?
10. Which native files, calibration files, instrument logs, environmental logs, processing scripts, residuals, and covariance products can be released?
11. Can every delivered file be included in a project-side SHA-256 manifest?
12. What metadata identify sample temperature rather than controller setpoint?
13. What is the practical throughput, queue, and turnaround for a two-specimen pilot and an eight-specimen experiment?
14. What are the assisted academic rates, required deposits, proposal requirements, travel costs, and cancellation terms?
15. What raw-data, intellectual-property, confidentiality, embargo, acknowledgment, and publication restrictions apply?
16. Who is the accountable technical owner and who is the administrative contact?
17. Which publicly described capability does not apply to this exact specimen or experiment?
18. What single unresolved assumption is most likely to prevent the experiment?

## 3. Material-provider questions

1. Can two Hg-rich composition levels near the intended experimental range be supplied with at least four candidate carrier/vacancy states per level?
2. Are the specimens bulk, LPE, MBE, or another growth class, and can one growth class be retained across the core design?
3. What are the parent wafer, growth run, substrate, thickness, orientation, doping, anneal, and processing histories?
4. Is independent composition available for each specimen, with a demonstrated standard uncertainty and method that does not reuse the gap model under test?
5. Can the candidate pool remain one carrier polarity at 6 K and 300 K?
6. What carrier-density range and Hg-vacancy-state range have actually been achieved, rather than nominally targeted?
7. Are unused witness coupons available, and what quantified transfer uncertainty connects them to the optical specimens?
8. Can specimens be provided without device passivation, contacts, coatings, or irreversible processing that would confound paired optical measurements?
9. Are material transfer, publication, and raw-data rights compatible with an open provenance record?

## 4. Composition and thickness metrology questions

1. Has the method been validated specifically on HgCdTe or closely matched Hg-Cd-Te standards?
2. What certified standards, matrix corrections, line selections, background models, and drift corrections are used for Hg, Cd, and Te?
3. What is the demonstrated specimen-level standard uncertainty in composition fraction `x`, including spatial inhomogeneity and between-session reproducibility?
4. Can `sigma_x <= 0.0015` be demonstrated on the actual specimen geometry?
5. How many locations and what mapped area are required to distinguish analytical precision from real composition nonuniformity?
6. What beam energy, current, dwell, spot size, and dose are used?
7. Has beam-induced Hg loss or composition drift been measured under those conditions?
8. Is polishing or conductive coating required, and can it be performed on a sacrificial coupon rather than the paired optical area?
9. Can composition and thickness be measured on the same registered area used optically?
10. What thickness method is used, what is its uncertainty, and how are substrate and interference effects handled?
11. Are raw count data, standards, calibration files, maps, point coordinates, correction factors, and covariance available?

## 5. Hall and carrier-state metrology questions

1. Is van der Pauw or Hall-bar measurement available at actual sample temperatures near 6 K and 300 K?
2. What is the sample-temperature uncertainty and equilibration criterion at both blocks?
3. What magnetic-field range and polarity reversal sequence are used?
4. What resistance, mobility, carrier-density, and contact-resistance ranges can be measured reliably for HgCdTe?
5. What contact metallurgy and anneal are required, and can contacts be removed without altering the optical area or state?
6. Can low excitation current, voltage, and power limits be predeclared to avoid heating or injection?
7. Are I-V linearity, field antisymmetrization, geometric correction, and repeatability diagnostics delivered?
8. Can carrier polarity, density, mobility, covariance, and uncertainty be reported for every specimen at both temperature blocks?
9. Can carrier state be measured before and after the paired optical sequence to quantify drift?
10. Are native voltage/current/field/temperature time series and processing code available?

## 6. Vacancy-sensitive metrology questions

1. Which PAS observable is proposed as the quantitative vacancy proxy: lifetime, Doppler broadening, coincident Doppler, depth profile, or a joint fit?
2. What evidence connects that observable specifically to Hg vacancies in HgCdTe rather than generic open volume, substrate defects, dislocations, or surface damage?
3. Are HgCdTe reference states with independently altered vacancy concentration available for calibration?
4. What is the detection limit, dynamic range, depth resolution, lateral resolution, and standard uncertainty for the proposed proxy?
5. How do epilayer thickness, substrate, surface oxide, contacts, passivation, and composition affect the signal?
6. Can the same specimen geometry be measured without destructive preparation?
7. Can the vacancy proxy be measured at 6 K and 300 K, or what validated transfer model connects a room-temperature measurement to both optical states?
8. Can at least two technical repeats and full raw spectra be delivered?
9. Are background, source, detector-response, depth-profile, and model-parameter covariance records available?
10. Can pre/post optical-sequence measurements detect state drift at the declared threshold?

## 7. Absorption-laboratory questions

1. Can transmission and/or reflectance cover the expected HgCdTe edge at both 6 K and 300 K with the same specimen and registered area?
2. What source, beamsplitter, detector, purge/vacuum path, spectral range, resolution, spot size, and polarization are available?
3. Is the reported temperature measured at the sample, and what is its uncertainty and stability?
4. What reference, substrate, reflection, interference, and stray-light corrections are applied?
5. Can native interferograms or equivalent minimally processed spectra be released?
6. Are calibration scans, background scans, detector linearity, instrument-response records, and covariance available?
7. Can multiple edge definitions and observation models be applied after acquisition without losing information?
8. Can the exact optical area be photographed or registered for transfer to magneto-optical measurement?
9. Are two or more native repeats available at each temperature without changing sample state?
10. What mounting or window changes occur between 6 K and 300 K?

## 8. Magneto-optical-laboratory questions

1. Can the relevant interband transitions be measured at both 6 K and 300 K, or is the useful temperature range restricted?
2. What maximum steady field, field homogeneity, sweep protocol, Faraday/Voigt geometry, and polarization control are available?
3. What spectral range, resolution, detector chain, source stability, and signal-to-noise are expected for the supplied thickness and area?
4. Can zero-field absorption and high-field spectra use the same mounting and registered area?
5. How are field, temperature, polarization, substrate, window, and background calibrations recorded?
6. Which transition model and band parameters are needed to infer an interaction gap?
7. Can raw spectra, field traces, temperature traces, transition assignments, fit residuals, covariance, and software versions be released?
8. Can model-conditioned outputs be clearly separated from directly observed transition energies?
9. What sample geometry, orientation, thickness, and substrate restrictions apply?
10. Is a technical pre-proposal review available before a formal user proposal?

## 9. Data-archive questions

1. Who is the accountable owner of the complete raw-data package?
2. Which repository will hold raw files, calibration files, processing code, manifests, and derived results?
3. Are restricted-access or embargoed records compatible with partner rights while preserving a stable identifier?
4. How are versions, corrections, withdrawals, and superseded files represented?
5. Is a DOI or equivalent persistent identifier assigned?
6. Does the archive preserve original bytes, and what checksum algorithm does it use?
7. Will the project additionally publish an independent SHA-256 manifest?
8. What file-size, format, retention, preservation, backup, and access limits apply?
9. How are proprietary instrument formats documented so future users can interpret them?
10. What repository-independent backup exists?

## 10. Evidence-to-status rule

A candidate remains `public_evidence_only` until a dated response and supporting documentation are stored.

A role may become `conditional` when:

- an accountable owner is identified;
- the organization confirms interest or access in writing;
- unresolved assumptions are explicit.

A role may become `confirmed` only when all role documentation in the PR #162 feasibility template is complete and no blocking assumption remains.

The same rule applies to every cross-cutting pilot gate. A candidate shortlist is not a readiness decision.
