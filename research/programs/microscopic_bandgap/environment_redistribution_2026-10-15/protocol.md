# Post-acquisition spectral decomposition — 2026-10-15

Startinga753cf5; no native rerun. This is an explicitly **post-acquisition**
diagnostic of the observed weak Gaussian/strong inverse contrast, not a new
prospective prediction of that observation or a retuned acceptance gate.

Keep the SAME frozen50Ryhost frame, full352complex overlaps and ownEF reference.
Use the already recorded largest2Gamma6/4Gamma8weight indices to decompose each
positive measure into selected and rest. The four sharing Gamma8states retain
their FOUR eigenvalues; never replace them by an averaged gap. Selected-only
measures have mass below1; they are diagnostic components, not complete physical
Hamiltonians. No fitted weights, normalization by retained mass or extraQEjob.

For GaussianW2 compute exactly

    c_full-c_selected = (N_rest-c_selected M_rest)/(M_selected+M_rest).

For the scalar inverse ateta.05eV compute exactly

    1/g_full-1/g_selected = -g_rest/(g_selected g_full).

Report selected contribution, remainder correction and their exact sum for
each sector/member and for the contrast. Independently reconstruct the saved
full results. To test dependence on energy probe rather than invent alignment,
freeze eta.05 and center displacements t=−.1,0,+.1eV relative to EACH ownEF.
Apply existing scalar positive-tail/frame/IEEE bounds; no new materialerrorbar.
No common absolute potential, local N2operator, gap or physicalxc is inferred.
