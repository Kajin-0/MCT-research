# Retained-data causal chemical response, no new material calculation

2026-10-15. Fixed existing accepted8atom ordered PBE+SOC host/Cd k3/50-200Ry
data and ORIGINAL physical Gamma6/8 projectors; no new QE, frame fit or spectrum
normalization. Physical x_c and HSE remain unqualified. This supplements the
existing bounded Gaussian response using a different bounded causal test.

Evaluate only t=-.05,0,+.05eV relative to EACH specimen's own native Fermi level
and eta=.025,.05,.1eV. Eta is analytic resolution, not an intrinsic linewidth.
Keep all176retained eigenstates and complex-overlap trace weights. Define

    g_a(t+i eta)=integral d mu_a(e)/(t+i eta-e),
    Omega_eta(t)=Re(1/g_8-1/g_6).

This equals signed ordering only for ideal single-pole measures. In the actual
multipeak case it is a specified inverse-resolvent functional, not a sharp gap,
spectral maximum, topological invariant or crossing-mass prediction. The chemical
response is Omega_Cd-Omega_host. Its own-Fermi convention is explicit and cannot
be substituted for a common electrostatic band-offset alignment.

Conditional bounds: if missing positive measure has mass r, frame projector
error<=epsilon under the existing Td/NC/IEEE model, and retained-weight roundoff
L1 error<=b, then |g-g_ret|<=delta=(r+2epsilon+b)/eta. If delta<|g_ret|,

    |1/g-1/g_ret| <= delta/[|g_ret|(|g_ret|-delta)].

Sum four bounds for chemical-response interval. If any denominator fails, mark
that row uncertified; do not change eta/window/data after observing results.
Preserve all old unconditional physical no-go theorems. These bounds address
only finite spectrum/frame/arithmetic under the fixed numerical Hamiltonian;
they do not bound SCF eigenpair, functional, BZ, supercell, disorder or material
errors. No empirical alloy data or missing-density assumption enters.
