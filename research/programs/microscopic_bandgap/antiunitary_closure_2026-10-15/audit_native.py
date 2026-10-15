"""Read-only physical-G antiunitary and weighted-density audit (no QE execution)."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
from scipy.linalg import svd, eigh

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'hybrid_convergence_2026-10-15'
sys.path.insert(0, str(OLD))
from packets import packet

ROOT = Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8c_20261015/p1/host')
THRESHOLDS = [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def gather(cycle):
    records = [packet(ROOT, 'before', rank, cycle) for rank in [0, 1]]
    G = np.array(sorted(tuple(g) for b in records for g in b['G']))
    N = len(G)
    assert N == len(set(map(tuple, G))) == 10827
    lookup = {tuple(g): i for i, g in enumerate(G)}
    minus = np.array([lookup[tuple(-g)] for g in G])
    np.testing.assert_array_equal(minus[minus], np.arange(N))
    phi = np.empty((2*N, 176), complex)
    direct = np.empty_like(phi)
    for b in records:
        n, p = b['nnpw'], b['npwx']
        ix = np.r_[np.arange(n), np.arange(p, p+n)]
        target = np.array([lookup[tuple(g)] for g in b['G']])
        glob = np.r_[target, N+target]
        phi[glob] = b['phi'][ix]
        direct[glob] = b['direct'][ix]
        for key in ['et', 'wg', 'B', 'k', 'scalars']:
            np.testing.assert_array_equal(b[key], records[0][key])
    theta = lambda x: np.r_[x[N+minus].conj(), -x[minus].conj()]
    np.testing.assert_array_equal(theta(theta(phi)), -phi)
    return phi, direct, theta, records[0]['et'], records[0]['wg']


def orthonormal(phi):
    g = phi.conj().T @ phi
    w, v = eigh((g + g.conj().T)/2)
    assert min(w) > .9999999
    U = phi @ ((v / np.sqrt(w)) @ v.conj().T)
    return U, float(np.linalg.norm(g-np.eye(g.shape[0]), 2))


def inspect(cycle):
    phi, direct, theta, et, wg = gather(cycle)
    U, gerr = orthonormal(phi)
    TU = theta(U)
    cross = U.conj().T @ TU
    R = TU - U @ cross
    # Direct residual SVD has absolute precision O(eps), unlike sqrt(1-s^2).
    L, singular, _ = svd(R, full_matrices=False, lapack_driver='gesvd')
    ranks = {str(t): int(sum(singular > t)) for t in THRESHOLDS}
    r = int(sum(singular > 1e-11))
    Q, _ = np.linalg.qr(np.column_stack((U, L[:, :r])), mode='reduced')
    qerr = float(np.linalg.norm(Q.conj().T @ Q-np.eye(Q.shape[1]), 2))
    C = Q.conj().T @ phi
    TP = theta(phi)
    CT = Q.conj().T @ TP
    D = (C*wg) @ C.conj().T - (CT*wg) @ CT.conj().T
    D = (D+D.conj().T)/2
    compressed = float(np.max(np.abs(eigh(D, eigvals_only=True))))
    # A posteriori bound for omitted density: ||BB†-PBB†P|| <= 2||B||||(I-P)B||.
    B = phi*np.sqrt(wg)
    BT = TP*np.sqrt(wg)
    eB = float(np.linalg.norm(B-Q@(Q.conj().T@B), 2))
    eBT = float(np.linalg.norm(BT-Q@(Q.conj().T@BT), 2))
    normB = float(np.linalg.norm(B, 2))
    remainder = 2*normB*(eB+eBT)
    # Q is floating orthonormal; explicitly bound its Gram correction scale.
    gram_allowance = 16*qerr*normB**2
    lower = max(0., compressed-gram_allowance)
    upper = compressed+remainder+gram_allowance
    H = -(phi.conj().T @ direct)
    hherm = float(np.linalg.norm(H-H.conj().T, 2))
    he = eigh((H+H.conj().T)/2, eigvals_only=True)
    shells = []
    for start, stop in [(0, 142), (142, 146), (0, 146), (146, 176)]:
        A = phi[:, start:stop]
        QA, ge = orthonormal(A)
        RA = theta(QA)-QA@(QA.conj().T@theta(QA))
        ls = svd(RA, compute_uv=False, lapack_driver='gesvd')
        shells.append(dict(bands_1_based=[start+1, stop], occupation_min=float(min(wg[start:stop])),
                           occupation_max=float(max(wg[start:stop])), gram_error=ge,
                           leakage_max=float(max(ls)), leakage_ranks={str(t):int(sum(ls>t)) for t in THRESHOLDS},
                           leakage_singular_values=ls.tolist()))
    weights = []
    for cutoff in [1e-2, 1e-4, 1e-8, 1e-12]:
        discard = wg < cutoff
        # Orthogonal native orbitals up to measured Gram: tail operator, not sum.
        tail_op = float(max(wg[discard], default=0.) * np.linalg.norm(phi.conj().T@phi, 2))
        weights.append(dict(occupation_cutoff=cutoff, kept=int(sum(~discard)),
                            omitted_charge_e=float(sum(wg[discard])), density_tail_op_upper=tail_op))
    result = dict(cycle=cycle, source_Gram_error=gerr, orthonormal_Gram_error=float(np.linalg.norm(U.conj().T@U-np.eye(176),2)),
                  residual_method='direct ThetaU-U(Udagger ThetaU), positive-Gram correction',
                  residual_singular_values=singular.tolist(), leakage_ranks=ranks,
                  numerical_closure_dimension_at_threshold={k:176+v for k,v in ranks.items()},
                  exact_rank_not_identified_below_floating_resolution=True,
                  reduced_density_basis_dimension=Q.shape[1], reduced_basis_Gram_error=qerr,
                  density_TR_compressed_op=compressed, density_TR_op_interval=[lower, upper],
                  density_omission_bound=remainder, floating_Gram_allowance=gram_allowance,
                  nearest_TR_invariant_density_op_distance_interval=[lower/2, upper/2],
                  source_charge_e=float(sum(wg)), source_et_Ry=et.tolist(), source_wg=wg.tolist(),
                  exchange_positive_Gram_min_Ry=float(min(he)), exchange_positive_Gram_max_Ry=float(max(he)),
                  exchange_Gram_condition=float(max(he)/min(he)), exchange_Gram_Hermiticity_defect_Ry=hherm,
                  native_unhalved_exchange_Ry=float(wg@np.diag(-H).real), shells=shells, tails=weights)
    print(json.dumps({k:v for k,v in result.items() if k in ['cycle','leakage_ranks','density_TR_op_interval','exchange_positive_Gram_min_Ry','exchange_Gram_condition'] }), flush=True)
    return result


def main():
    rows = [inspect(c) for c in [1, 2, 3, 8]]
    provenance = {str(p):sha(p) for c in [1, 2, 3, 8] for rank in [0,1]
                  for p in [ROOT/'pilot'/f'c{c}_before.rank{rank}']}
    out = dict(status='CALCULATED retained native spectra only', parent='d6b95cc', thresholds=THRESHOLDS,
               rows=rows, raw_sha256=provenance, code_sha256=sha(Path(__file__)), new_native_jobs=0,
               no_occupation_or_source_change=True, physical_xc=None)
    (HERE/'native_audit.json').write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')


if __name__=='__main__':
    main()
