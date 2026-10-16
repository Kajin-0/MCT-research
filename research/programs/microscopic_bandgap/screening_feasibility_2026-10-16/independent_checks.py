"""Independent scalar native-density witnesses and QR/action checks; no jobs."""
import json
import math
from pathlib import Path
import numpy as np
from audit_retained import Packet, ROOT, HERE, RY_MEV, herm, norm


def density_check(member, cycle):
    rows = []
    for rank in (0, 1):
        b = Packet(ROOT/member/'pilot'/f'c{cycle}_before.rank{rank}', rank, 2, cycle)
        b.take('<i8', (10,)); b.take('<f8', (3, 3)); b.take('<f8', (3,)); b.take('<f8', (4,))
        G = b.take('<i8', (3, b.n)).T.copy(); b.take('<f8', (176,)); f = b.take('<f8', (176,)).copy()
        rows.append((G, b.matrix(176), f))
    G = np.array(sorted(tuple(g) for gs, _, _ in rows for g in gs)); N = len(G)
    index = {tuple(g): i for i, g in enumerate(G)}
    phi = np.empty((2*N, 176), complex)
    for gs, ps, f in rows:
        ix = np.array([index[tuple(g)] for g in gs]); phi[np.r_[ix, N+ix]] = ps
    minus = np.array([index[tuple(-g)] for g in G])
    Tphi = np.r_[phi[N+minus].conj(), -phi[minus].conj()]
    O = phi.conj().T @ Tphi
    # Select a witness using the uncorrected native compression, independently of
    # the main audit's positive-Gram normalization. The final scalar uses the
    # original vectors themselves, and is a lower witness with no Gram assumption.
    A = herm(np.diag(f)-(O*f)@O.conj().T)
    ev, v = np.linalg.eigh(A); j = int(np.argmax(abs(ev)))
    u = phi@v[:, j]; u /= np.linalg.norm(u)
    scalar = math.fsum(float(f[k])*(abs(np.vdot(phi[:, k], u))**2-abs(np.vdot(Tphi[:, k], u))**2) for k in range(176))
    main = json.loads((HERE/'retained_result.json').read_text())['phases'][f'{member}_{cycle}']['actual_density_Theta_compressed_lower_witness']
    assert abs(abs(scalar)-main) < 2e-13
    return dict(actual_scalar_witness=scalar, absolute_witness=abs(scalar),
                difference_from_main_witness=abs(abs(scalar)-main),
                unit_witness_norm=float(np.linalg.norm(u)), strict_gate_falsified=abs(scalar)>1e-8)


def main():
    result = json.loads((HERE/'retained_result.json').read_text())
    states = {f'{m}_{c}':density_check(m, c) for m in ('host', 'cd') for c in (1, 2)}
    data = np.load(HERE/'contracted_actions.npz'); F = data['reference']; Q, _ = np.linalg.qr(F)
    actions = {}
    for k in ('c1', 'c2', 'change'):
        Y = data[f'{k}_action_Ry']
        R = Y-Q@(Q.conj().T@Y)
        sv = np.linalg.svd(R, compute_uv=False)*RY_MEV
        main_sv = np.array(result['chemical'][k]['action_Q_leakage_singular_meV'])
        assert max(abs(sv-main_sv)) < 1e-9
        # Independent compensated real+imaginary diagonal contraction, no BLAS trace.
        diag = [math.fsum((F[:, j].real*Y[:, j].real+F[:, j].imag*Y[:, j].imag).tolist()) for j in range(6)]
        g = (math.fsum(diag[:2])/2-math.fsum(diag[2:])/4)*RY_MEV
        assert abs(g-result['chemical'][k]['trace_meV']) < 1e-9
        actions[k] = dict(QR_residual_singular_meV=sv.tolist(), compensated_trace_meV=g)
    # Exact dual-norm extremizer on the REAL measured six-by-six matrix. This
    # tests a numerical-error theorem, not a synthetic material or new spectrum.
    A = data['c2_P_Ry']*RY_MEV
    radius = result['chemical']['c2']['sharp_unseen_P_block_error_sign_radius_meV']
    W = np.diag([.5, .5, -.25, -.25, -.25, -.25])
    extremizer = np.diag([-radius, -radius, radius, radius, radius, radius])
    sharp_zero = float(np.trace(W@(A+extremizer)).real)
    assert abs(sharp_zero) < 1e-9 and abs(norm(extremizer)-radius) < 1e-12
    output = dict(passed=True, native_invocations=0, density_scalar_checks=states,
                  actions=actions, sharp_trace_radius_extremizer_meV=radius,
                  perturbed_actual_compression_trace_meV=sharp_zero,
                  claims='finite-array checks, no directed-rounding/material error enclosure')
    (HERE/'independent_results.json').write_text(json.dumps(output, indent=2, allow_nan=False)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
