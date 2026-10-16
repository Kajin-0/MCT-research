"""Independent state/packet tests, one tiny nonlinear SCF; no native execution."""
from pathlib import Path
from itertools import product, permutations
import io
import json
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.special import expit, xlogy

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PRIVATE = Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8u_20261015')


def finite_fd(H, charge, sigma):
    e, U = eigh(H)
    mu = brentq(lambda m: expit((m-e)/sigma).sum()-charge,
                e[0]-1, e[-1]+1, xtol=5e-16)
    w = expit((mu-e)/sigma)
    return (U*w)@U.conj().T, mu, w, e, U


def main():
    r = json.loads((HERE/'result.json').read_text())
    a = np.load(HERE/'trial_coordinates.npz')
    old = np.load(BASE/'single_state304_2026-10-15/native_matrices.npz')
    H = (old['H_QQ']+old['H_QQ'].conj().T)/2
    F, mu, w, e, U = finite_fd(H, 144, .001)
    fd_difference = float(np.linalg.norm(F-a['FD_Q'], 2))
    assert fd_difference < 1e-9 and abs(mu-r['mu_Ry']) < 1e-12
    # Independent all64 quarter translations, not the atom0-image algorithm.
    positions = a['host_quarter_positions']
    groups = {}
    for name, species in [('host', ['Hg']*4+['Te']*4), ('Cd', ['Cd']+['Hg']*3+['Te']*4)]:
        keys = set()
        for perm in permutations(range(3)):
            for signs in product((-1, 1), repeat=3):
                R = np.eye(3, dtype=int)[list(perm)]*np.array(signs)[:, None]
                for t in product(range(4), repeat=3):
                    transformed = (positions@R.T+t) % 4
                    if all(any(s == z and np.array_equal(y, q) for z, q in zip(species, positions))
                           for s, y in zip(species, transformed)):
                        keys.add((tuple(R.ravel()), t))
        expected = {(tuple(np.array(k['R']).ravel()), tuple(k['t_quarters']))
                    for k in r['spatial_operations'][name]}
        assert keys == expected
        groups[name] = len(keys)
    # Canonical prospective rank transport: ORIGINAL accepted actual local G
    # maps, zero padded native 2*npwx layout. No files in DFT are created.
    b = np.load(PRIVATE/'trial.npz')
    V, G, P = b['Q'], b['G'], b['P']
    N = len(G)
    X = V@a['coordinate']
    lookup = {tuple(g): i for i, g in enumerate(G)}
    minus = np.array([lookup[tuple(-g)] for g in G])
    theta = lambda v: np.r_[v[N+minus].conj(), -v[minus].conj()]
    query = np.column_stack((X[:, :146], P, theta(P)))
    assert query.shape == (2*N, 158)
    seen = set()
    out = np.zeros_like(X)
    packet_sizes = []
    for rank in [0, 1]:
        path = PRIVATE/'p1/host/pilot'/f'H.rank{rank}'
        with path.open('rb') as src:
            h = np.fromfile(src, '<i8', 16)
            p, n = map(int, h[4:6])
            src.seek(848)  # fixed accepted v2 H packet header, verified here
            localG = np.fromfile(src, '<i8', 3*n).reshape(3, n, order='F').T
        assert h[0] == 70251541 and h[1] == 2 and h[2] == rank
        assert not (seen & set(map(tuple, localG)))
        seen.update(map(tuple, localG))
        ix = np.array([lookup[tuple(g)] for g in localG])
        global_ix = np.r_[ix, N+ix]
        native_ix = np.r_[np.arange(n), p+np.arange(n)]
        src = np.zeros((2*p, 176), complex)
        trials = np.zeros((2*p, 158), complex)
        src[native_ix], trials[native_ix] = X[global_ix], query[global_ix]
        fields = [np.array([70251601, 1, rank, p, n, 176, 146, 158, 144], '<i8'),
                  localG.T.astype('<i8'), a['occupations'][:176].astype('<f8'),
                  src.astype('<c16'), trials.astype('<c16')]
        stream = io.BytesIO(b''.join(k.tobytes(order='F') for k in fields))
        decoded = []
        for k in fields:
            value = np.frombuffer(stream.read(k.nbytes), dtype=k.dtype).reshape(k.shape, order='F')
            np.testing.assert_array_equal(value, k)
            decoded.append(value)
        assert not stream.read()
        out[global_ix] = decoded[3][native_ix]
        packet_sizes.append(len(stream.getvalue()))
    np.testing.assert_array_equal(out, X)
    assert len(seen) == N
    # An independent real-space view of the NEW trial, including spin that
    # domag=false would otherwise suppress. Native reciprocal/volume convention
    # is reused, without importing a protected driver or writing there.
    previous_density = np.load(PRIVATE/'expected_density.npz')
    omega = float(previous_density['omega'])
    density = np.zeros((60, 60, 60, 4))
    indices = tuple((G % 60).T)
    for j in range(146):
        z = np.zeros((2, 60, 60, 60), complex)
        for s in range(2):
            z[s][indices] = X[s*N:(s+1)*N, j]
        up, down = np.fft.ifftn(z, axes=(1, 2, 3))*60**3
        factor = float(a['occupations'][j])/omega
        density[..., 0] += factor*(abs(up)**2+abs(down)**2)
        density[..., 1] += factor*2*(up.conj()*down).real
        density[..., 2] += factor*2*(up.conj()*down).imag
        density[..., 3] += factor*(abs(up)**2-abs(down)**2)
    fft_charge = float(density[..., 0].sum()*omega/60**3)
    spin_abs = float(np.max(abs(density[..., 1:])))
    assert abs(fft_charge-144) < 1e-8 and spin_abs < 1e-10
    # This expected density is an OFFLINE prediction for future readback,
    # not a newly observed QE state or a rebuilt local XC potential.
    np.savez_compressed(HERE/'expected_trial_density.npz', rhoR=density, omega=omega)
    # Mathematical commutator/change bound, independently in an exact small
    # Hermitian block. This is an algebra check, not a material counterexample.
    h = np.array([[0., .3], [.3, 1.]])
    d = np.diag([1., 0.])
    comm = np.linalg.norm(h@d-d@h, 2)
    correction = np.array([[0., -.3], [-.3, 0.]])
    assert abs(comm-np.linalg.norm(correction, 2)) < 1e-14
    assert np.linalg.norm((h+correction)@d-d@(h+correction)) == 0
    # A closed-loop nonlinear state update in a COMPLETE 8dimensional model.
    # All spin blocks are present. It tests the residual logic; it does not
    # substitute its contraction constant for unknown HSE feedback.
    h0 = np.diag([-.3, -.1, .1, .3])
    h0[0, 1] = h0[1, 0] = .04
    h0[2, 3] = h0[3, 2] = .03
    h0 = np.kron(np.eye(2), h0)
    D = np.diag([1., 1., 0., 0.]*2).astype(complex)
    H_of_D = lambda d: h0+.04*d
    theta_d = lambda d: np.block([[d[4:, 4:].conj(), -d[4:, :4].conj()],
                                  [-d[:4, 4:].conj(), d[:4, :4].conj()]])
    first = finite_fd(H_of_D(D), 4, .05)[0]
    stale_residual = np.linalg.norm(first-finite_fd(H_of_D(D), 4, .05)[0], 2)
    rebuilt_residual = np.linalg.norm(first-finite_fd(H_of_D(first), 4, .05)[0], 2)
    assert stale_residual < 1e-12 and rebuilt_residual > 1e-6
    history = []
    for _ in range(60):
        HD = H_of_D(D)
        Fnext = finite_fd(HD, 4, .05)[0]
        error = float(np.linalg.norm(D-Fnext, 2))
        history.append(error)
        assert abs(np.trace(D).real-4) < 1e-10
        assert np.linalg.norm(D-theta_d(D), 2) < 1e-10
        if error < 1e-10:
            break
        D = Fnext
    assert history[-1] < 1e-10
    # Full-density symmetry alone also admits nonstationary initial D.
    assert history[0] > 1e-3
    result = dict(passed=True, actual_native_data_independent_FD_op_error=fd_difference,
        independent_species_group_counts=groups, actual_two_rank_packet_sizes_B=packet_sizes,
        canonical_source_and_158_query_roundtrip_bitwise=True,
        new_trial_independent_FFT=dict(charge_e=fft_charge, max_spin_density_Bohr_minus3=spin_abs,
            charge_density_change_max_Bohr_minus3=float(np.max(abs(density[...,0]-previous_density['rhoR'][...,0]))),
            charge_density_change_L2_Bohr_minus3_over2=float(np.sqrt(np.sum((density[...,0]-previous_density['rhoR'][...,0])**2)*omega/60**3)),
            rebuilt_native_H_of_new_density=False),
        native_reader_implemented_or_compiled=False,
        small_complete_nonlinear_model=dict(stale_H_FD_residual=stale_residual,
            rebuilt_H_FD_residual=rebuilt_residual, iterations=len(history),
            final_full_FD_residual=history[-1], TR_charge_checks=True,
            establishes_native_or_material_convergence=False),
        commutator_change_bound_saturated_in_small_block=True,
        numerical_chemical_2meV_certified=False, native_admission=False,
        native_jobs=0, DFT_writes=0)
    (HERE/'independent_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
