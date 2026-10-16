"""One prospective FD trial from retained H[D0]; never writes/runs in DFT."""
from pathlib import Path
from itertools import permutations, product
import hashlib
import json
import numpy as np
from scipy.special import expit, xlogy
from scipy.spatial.transform import Rotation

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PRIVATE = Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8u_20261015')
RYEV = 13.605693122994
SIGMA = .001


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def op(a):
    return float(np.linalg.norm(a, 2))


def native_fd(x):
    # QE7.5 Modules/wgauss.f90 n=-99, including its numerical saturation.
    x = np.asarray(x)
    return np.where(x < -200, 0., np.where(x > 200, 1., expit(x)))


def fd(e, count):
    lo, hi = float(e[0]-1), float(e[-1]+1)
    for _ in range(100):
        mid = (lo+hi)/2
        if native_fd((mid-e)/SIGMA).sum() < count:
            lo = mid
        else:
            hi = mid
    mu = (lo+hi)/2
    return mu, native_fd((mu-e)/SIGMA)


def operations(species, positions):
    """Exact integer quarter-cell enumeration, no imported symmetry labels."""
    wanted = set((s, *p) for s, p in zip(species, positions))
    found = []
    for perm in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            R = np.diag(signs) @ np.eye(3, dtype=int)[list(perm)]
            # Image of atom0 must be another atom of the SAME species.
            ts = {tuple((p-R@positions[0]) % 4) for s, p in zip(species, positions)
                  if s == species[0]}
            for t in sorted(ts):
                image = (positions @ R.T + t) % 4
                if set((s, *p) for s, p in zip(species, image)) == wanted:
                    found.append((R, np.array(t)))
    return found


def spin(R):
    # Spin is axial under improper spatial operations; arbitrary lift sign
    # cancels in the density conjugation.
    d = round(np.linalg.det(R))
    q = Rotation.from_matrix(d*R).as_quat()
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]], complex)
    sz = np.diag([1, -1])
    return q[3]*np.eye(2)-1j*(q[0]*sx+q[1]*sy+q[2]*sz)


def density_bound(X, weights, image):
    """Stable full-space bound, avoiding subtraction of two ~144 traces.

    Y=XK+R; expand Y w Ydag-X w Xdag. Triangle inequality gives the
    displayed F bound, hence also an operator bound. No omitted-space gap.
    """
    gram = X.conj().T @ X
    K = np.linalg.solve(gram, X.conj().T @ image)
    residual = image-X@K
    inside = (K*weights)@K.conj().T-np.diag(weights)
    xn = np.sqrt(max(np.linalg.eigvalsh(gram)))
    cross = 2*xn*op(K)*np.linalg.norm(residual*weights, 'fro')
    last = np.linalg.norm(residual*np.sqrt(weights), 'fro')**2
    return float(xn*xn*np.linalg.norm(inside, 'fro')+cross+last)


def main():
    # Immutable original native provenance, then the derived common-state data.
    original = json.loads((BASE/'single_state304_2026-10-15/native_result.json').read_text())
    assert original['accepted'] and original['scientific_pass'] and original['terminal_pass']
    pins = original['source_hashes'].copy()
    build = json.loads((BASE/'single_state304_2026-10-15/build_results.json').read_text())
    frozen = json.loads((BASE/'single_state304_2026-10-15/frozen_protocol.json').read_text())
    for p in [PRIVATE/'trial.npz', PRIVATE/'expected_density.npz']:
        pins[str(p)] = frozen['profile']['pins'][str(p)]
    pins[str(PRIVATE/'full_actions.npz')] = json.loads(
        (BASE/'hse_residual_response_2026-10-15/result.json').read_text())['source_full_action_sha256']
    pins.update(build['source_pins'])
    pins[build['binary']] = build['binary_sha256']
    protected = json.loads((BASE/'screening_feasibility_2026-10-16/source_and_budget.json').read_text())
    # Locate the existing reviewed PP/ELF/source pin mapping without running
    # old driver modules or creating Python bytecode in protected directories.
    def mappings(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str) and k.startswith('/') and isinstance(v, str) and len(v) == 64:
                    yield k, v
                yield from mappings(v)
        elif isinstance(x, list):
            for v in x:
                yield from mappings(v)
    pins.update(dict(mappings(protected)))
    for p, h in pins.items():
        assert sha(p) == h, p
    for name in ['trial.npz', 'full_actions.npz']:
        pins[str(PRIVATE/name)] = sha(PRIVATE/name)
    f = np.load(PRIVATE/'trial.npz')
    a = np.load(PRIVATE/'full_actions.npz')
    V, G, D0 = f['Q'], f['G'], f['D_Q']
    Hraw = a['H']
    A = (Hraw+Hraw.conj().T)/2
    HV = a['HV']
    assert np.max(abs(V.conj().T@HV-Hraw)) < 1e-10
    assert op(V.conj().T@V-np.eye(304)) < 1e-10
    e, U = np.linalg.eigh(A)
    mu, w = fd(e, 144)
    F = (U*w)@U.conj().T
    # Keep the original 176 trial capacity, with discarded Galerkin tail
    # explicitly distinguished from the UNKNOWN whole-space occupied tail.
    source = V@U[:, :176]
    nonzero = int(np.count_nonzero(w[:176] > 1e-8))
    X, weights = source[:, :nonzero], w[:nonzero]
    assert nonzero == 146 and abs(w[:176].sum()-144) < 1e-8
    assert op(source.conj().T@source-np.eye(176)) < 1e-10
    N = len(G)
    lookup = {tuple(g): i for i, g in enumerate(G)}
    minus = np.array([lookup[tuple(-g)] for g in G])
    def theta(Y):
        return np.r_[Y[N+minus].conj(), -Y[minus].conj()]
    theta_error = density_bound(X, weights, theta(X))
    positions = np.array([[0, 0, 0], [0, 2, 2], [2, 0, 2], [2, 2, 0],
                          [1, 1, 1], [1, 3, 3], [3, 1, 3], [3, 3, 1]])
    host = operations(['Hg']*4+['Te']*4, positions)
    cd = operations(['Cd']+['Hg']*3+['Te']*4, positions)
    assert len(host) == 96 and len(cd) == 24
    errors = []
    for R, t in host:
        dest = np.array([lookup[tuple(g)] for g in G@R.T])
        Y = np.empty_like(X).reshape(2, N, nonzero)
        phase = np.exp(-2j*np.pi*((G@R.T)@(t/4)))
        Y[:, dest] = np.einsum('ab,bgn->agn', spin(R), X.reshape(2, N, nonzero))*phase[None, :, None]
        errors.append(density_bound(X, weights, Y.reshape(X.shape)))
    assert max(errors+[theta_error]) < 1e-8
    # True H[D0] action on D1 orbitals; not projected eigen-residual alone.
    Y = HV@U[:, :176]
    residual = Y-source*e[:176]
    R = HV-V@A
    RF = R@F
    comm_op = float(np.sqrt(max(np.linalg.eigvalsh(RF.conj().T@RF))))
    inspace = op(A@F-F@A)
    # For [H+E,D1]=0, ||E|| >= ||[H,D1]|| / diam(spec D1).
    # The full commutator norm is >= ||R F||-||[A,F]||.
    diameter = float(max(w))  # full space includes zero outside V
    min_change = max(0., comm_op-inspace)/diameter
    S = float(-sum(xlogy(w, w)+xlogy(1-w, 1-w)))
    free_linear = float(np.trace(A@(F-D0)).real-SIGMA*(S-4*np.log(2)))
    delta_F2 = float(np.linalg.norm(F-D0, 'fro')**2)
    # This threshold is a derived requirement, NOT a measured HSE Hessian.
    L_descent = -2*free_linear/delta_F2
    native_source = PRIVATE/'build1/source/exx.f90'
    text = native_source.read_text()
    guard = ('IF(ANY(wg(1:142,1)/=1._DP).OR.ANY(wg(143:146,1)/=.5_DP).OR.ANY(wg(147:176,1)/=0._DP))')
    assert guard in text
    refused = bool(np.any(w[:142] != 1) or np.any(w[142:146] != .5) or np.any(w[146:176] != 0))
    assert refused
    # Native ±200 saturation has at most M exp(-200) missing mathematical
    # charge; it is not an unknown low-lying-complement certificate.
    charge_saturation_upper = 2*N*np.exp(-200.)
    out = dict(status='CALCULATED_VALID_NEW_TRIAL; NATIVE_BRIDGE_REFUSED',
        native_jobs=0, builds=0, DFT_writes=0,
        charge_e=float(w.sum()), mu_Ry=mu,
        charge_derivative_e_per_Ry=float(sum(w*(1-w))/SIGMA),
        entropy_kB=S, source176_Gram_op=op(source.conj().T@source-np.eye(176)),
        native_source_active_rank=nonzero,
        discarded_304_tail_charge_e=float(w[176:].sum()),
        discarded_176_below_native_EXX_cut_charge_e=float(w[:176][w[:176] <= 1e-8].sum()),
        native_FD_saturation_whole_finite_dimension_charge_upper_e=float(charge_saturation_upper),
        full_nonlocal_density_Theta_F_upper=theta_error,
        full_nonlocal_density_all_host_space_ops_F_upper=errors,
        actual_host_space_operation_count=len(host), actual_Cd_space_operation_count=len(cd),
        Cd_reference_translations_NOT_inherited=True,
        source_natural_weights=w[:176].tolist(),
        FD304_delta_density_op=op(F-D0), FD304_delta_density_F=float(np.sqrt(delta_F2)),
        fixed_H_linearized_free_energy_change_Ry=free_linear,
        nonlinear_HSE_energy_change_UNKNOWN=True,
        sufficient_nonlinear_Hessian_upper_for_full_step_descent_Ry=L_descent,
        that_Hessian_bound_available=False,
        source_eigenstate_full_H0_residuals_Ry=np.linalg.norm(residual, axis=0).tolist(),
        Fermi_quartet_full_H0_residual_max_Ry=float(max(np.linalg.norm(residual[:, 142:146], axis=0))),
        full_H0_commutator_op_lower_Ry=max(0., comm_op-inspace),
        minimum_uniform_H_change_if_this_D1_becomes_stationary_Ry=min_change,
        minimum_uniform_H_change_if_this_D1_becomes_stationary_meV=min_change*RYEV*1000,
        lower_is_NOT_projected_chemical_error=True,
        old_D0_reader_rejects_new_D1=True,
        new_H_of_D1_and_full_FD_residual_available=False,
        whole_space_occupied_tail_certified=False,
        source_state_admission=False, owner_admission='NOT_ATTEMPTED_AFTER_SOURCE_REFUSAL',
        numeric_chemical_2meV_certified=False, HSE_converged=False, physical_xc=None,
        source_pins=pins,
        spatial_operations=dict(host=[dict(R=R.tolist(),t_quarters=t.tolist()) for R,t in host],
                                Cd=[dict(R=R.tolist(),t_quarters=t.tolist()) for R,t in cd]))
    np.savez(HERE/'trial_coordinates.npz',coordinate=U[:, :176],e_Ry=e,mu_Ry=mu,
             occupations=w,FD_Q=F,host_quarter_positions=positions)
    (HERE/'result.json').write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k: out[k] for k in ['status','charge_e','full_nonlocal_density_Theta_F_upper',
          'actual_host_space_operation_count','actual_Cd_space_operation_count',
          'minimum_uniform_H_change_if_this_D1_becomes_stationary_meV',
          'sufficient_nonlinear_Hessian_upper_for_full_step_descent_Ry','source_state_admission']}, indent=2))


if __name__ == '__main__':
    main()
