"""Read-only contractions of the accepted two-state HSE chemical packets.

No legacy launch/analysis modules are imported. Native packets are opened rb,
checked against their ORIGINAL manifest, and embedded by physical integer G.
Only this new MCT directory receives output. No QE/MPI/build invocation.
"""
import hashlib
import json
import resource
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.special import expit

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'chemical_hse_relax_2026-10-15'
ROOT = Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8r_20261015/p1')
RY_MEV = 13605.693122994
MANIFEST = json.loads((OLD / 'evidence_manifest.json').read_text())
PINS = {}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


class Packet:
    def __init__(self, path, rank, stage, cycle):
        pin = MANIFEST['files'][str(path)]
        assert path.stat().st_size == pin['bytes'] and digest(path) == pin['sha256']
        PINS[str(path)] = pin
        self.data = path.read_bytes()
        self.pos = 0
        self.h = self.take('<i8', (16,))
        h = self.h
        assert tuple(h[:4]) == (7025101408, 1, stage, rank)
        assert tuple(h[7:14]) == (176, 2, 1, 1, 2, 144, cycle)
        self.p, self.n = map(int, h[5:7])
        assert 0 < self.n <= self.p <= 10827

    def take(self, dtype, shape):
        size = int(np.prod(shape)) * np.dtype(dtype).itemsize
        assert self.pos + size <= len(self.data)
        a = np.frombuffer(self.data, dtype, int(np.prod(shape)), self.pos).reshape(shape, order='F')
        self.pos += size
        assert np.isfinite(a).all()
        return a

    def matrix(self, cols):
        a = self.take('<c16', (2 * self.p, cols))
        assert np.linalg.norm(a[self.n:self.p]) < 1e-12
        assert np.linalg.norm(a[self.p + self.n:]) < 1e-12
        return np.r_[a[:self.n], a[self.p:self.p+self.n]]

    def end(self):
        assert self.pos == len(self.data)


def read(member, cycle, rank):
    path = ROOT / member / 'pilot'
    b = Packet(path / f'c{cycle}_before.rank{rank}', rank, 2, cycle)
    ext = b.take('<i8', (10,)); B = b.take('<f8', (3, 3)); k = b.take('<f8', (3,))
    scalars = b.take('<f8', (4,)); G = b.take('<i8', (3, b.n)).T
    et = b.take('<f8', (176,)); wg = b.take('<f8', (176,))
    phi = b.matrix(176)
    b.matrix(176)  # source direct columns are not needed for the six-probe test
    b.take('<c16', (176, 176)); b.end()
    a = Packet(path / f'c{cycle}_after.rank{rank}', rank, 3, cycle)
    a.take('<f8', (1,)); xi = a.matrix(176); a.matrix(176); a.take('<c16', (176, 176))
    probe = a.matrix(6); direct = a.matrix(6); a.end()
    local = []
    for stage in (0, 1):
        p = Packet(path / f'c{cycle}_local{stage}.rank{rank}', rank, stage, cycle)
        dims = p.take('<i8', (8,)); nr, ns, ng, nsg, nv = map(int, dims[:5])
        assert ns == nsg == 4 and tuple(dims[5:]) == (60, 60, 60)
        dg = p.take('<i8', (3, ng)); np.testing.assert_array_equal(p.matrix(6), probe)
        action = p.matrix(6)
        rhoR = p.take('<f8', (nr, ns)); rhoG = p.take('<c16', (ng, nsg)); p.take('<f8', (nv, 4)); p.end()
        local.append(dict(action=action, dg=dg, rhoR=rhoR, rhoG=rhoG))
    for field in ('dg', 'rhoR', 'rhoG'):
        assert local[0][field].tobytes() == local[1][field].tobytes()
    assert tuple(ext[:3]) == (60, 60, 60) and abs(scalars[1] - .25) < 1e-12
    assert abs(scalars[2] - 200) < 1e-12 and not np.any(k)
    return dict(G=G, B=B, et=et, wg=wg, phi=phi, xi=xi, probe=probe,
                direct=direct, local0=local[0]['action'], local1=local[1]['action'])


def herm(a):
    return (a + a.conj().T) / 2


def norm(a):
    return float(np.linalg.norm(a, 2))


def observable(a):
    return float((np.trace(a[:2, :2]).real/2 - np.trace(a[2:, 2:]).real/4) * RY_MEV)


def gather(member, cycle):
    ranks = [read(member, cycle, rank) for rank in (0, 1)]
    G = np.array(sorted(tuple(g) for r in ranks for g in r['G']))
    assert len(G) == len(set(map(tuple, G))) == 10827
    index = {tuple(g): i for i, g in enumerate(G)}
    N = len(G); minus = np.array([index[tuple(-g)] for g in G])
    fields = {}
    for name, ncol in [('phi', 176), ('xi', 176), ('probe', 6), ('direct', 6), ('local0', 6), ('local1', 6)]:
        v = np.empty((2*N, ncol), complex)
        for r in ranks:
            ix = np.array([index[tuple(g)] for g in r['G']])
            v[np.r_[ix, N+ix]] = r[name]
        fields[name] = v
    for key in ('B', 'et', 'wg'):
        np.testing.assert_array_equal(ranks[0][key], ranks[1][key])
    theta = lambda a: np.r_[a[N+minus].conj(), -a[minus].conj()]
    phi, F, xi = fields['phi'], fields['probe'], fields.pop('xi')
    np.testing.assert_array_equal(theta(theta(phi)), -phi)
    g = herm(phi.conj().T @ phi); w, v = np.linalg.eigh(g)
    assert np.max(abs(w - 1)) < 1e-8
    sqrtg = (v * np.sqrt(w)) @ v.conj().T
    U = phi @ ((v / np.sqrt(w)) @ v.conj().T)
    wg = ranks[0]['wg']; et = ranks[0]['et']
    overlap = U.conj().T @ theta(phi)
    # Exact compression lower witness in an orthonormal source frame (roundoff recorded).
    W = sqrtg @ np.diag(wg) @ sqrtg - (overlap*wg) @ overlap.conj().T
    witness = norm(herm(W))
    lo, hi = min(et)-1, max(et)+1
    for _ in range(100):
        mu = (lo+hi)/2
        if np.sum(expit((mu-et)/.001)) < 144: lo = mu
        else: hi = mu
    fd = expit(((lo+hi)/2-et)/.001)
    assert abs(sum(wg)-144) < 1e-8 and max(abs(fd-wg)) < 1e-9
    ace = -xi @ (xi.conj().T @ F)
    ace_error = ace-fields['direct']
    M = F.conj().T @ fields['direct']
    stored = np.load(OLD/f'{member}_c{cycle}_matrices.npz')
    reconstruction = float(np.max(abs(M-stored['exchange'])))
    assert reconstruction < 1e-12
    info = dict(source_Gram_error=norm(g-np.eye(176)),
                corrected_source_Gram_error=norm(U.conj().T@U-np.eye(176)),
                actual_density_Theta_compressed_lower_witness=witness,
                strict_1e_8_density_Theta_gate_falsified=witness > 1e-8,
                source_charge_e=float(sum(wg)), FD_occupation_max_error=float(max(abs(fd-wg))),
                recorded_source_mu_reconstructed_Ry=float((lo+hi)/2),
                direct_matrix_reconstruction_max_Ry=reconstruction,
                ACE_minus_direct_reference_action_opnorm_meV=norm(ace_error)*RY_MEV,
                ACE_minus_direct_reference_trace_meV=observable(F.conj().T@ace_error),
                reference_Gram_error=norm(F.conj().T@F-np.eye(6)))
    del fields['phi']
    fields['G'] = G
    return fields, info


def inspect_action(F, Y):
    S = herm(F.conj().T@F); w, v = np.linalg.eigh(S)
    inv = (v/np.sqrt(w))@v.conj().T
    V = F@inv; YV = Y@inv
    A = herm(V.conj().T@YV)
    residual = YV-V@A
    e6 = np.linalg.eigvalsh(A[:2, :2]); e8 = np.linalg.eigvalsh(A[2:, 2:])
    scalar = np.zeros((6, 6), complex)
    scalar[:2, :2] = np.eye(2)*np.trace(A[:2, :2])/2
    scalar[2:, 2:] = np.eye(4)*np.trace(A[2:, 2:])/4
    return dict(trace_meV=observable(F.conj().T@Y),
                all_sector_Rayleigh_difference_interval_meV=[float((e6[0]-e8[-1])*RY_MEV), float((e6[-1]-e8[0])*RY_MEV)],
                scalar_free_compression_opnorm_meV=norm(A-scalar)*RY_MEV,
                action_Q_leakage_opnorm_meV=norm(residual)*RY_MEV,
                action_Q_leakage_Gamma6_opnorm_meV=norm(residual[:, :2])*RY_MEV,
                action_Q_leakage_Gamma8_opnorm_meV=norm(residual[:, 2:])*RY_MEV,
                action_Q_leakage_singular_meV=(np.linalg.svd(residual, compute_uv=False)*RY_MEV).tolist(),
                reference_normalization_change_meV=norm(A-herm(F.conj().T@Y))*RY_MEV,
                compression_antihermitian_meV=norm(F.conj().T@Y-Y.conj().T@F)*RY_MEV,
                Gram_error=norm(S-np.eye(6))), A, residual


def main():
    start = time.monotonic(); states = {}; information = {}
    for m in ('host', 'cd'):
        states[m] = {}
        for c in (1, 2):
            states[m][c], information[f'{m}_{c}'] = gather(m, c)
    F = states['host'][1]['probe']
    for s in states.values():
        for d in s.values(): np.testing.assert_array_equal(d['probe'], F)
    actions = {}; matrices = {}; results = {}
    for c in (1, 2):
        per_member = {}
        for m in ('host', 'cd'):
            d = states[m][c]
            # Kinetic and species nonlocal/SOC cancel only INSIDE each member's activation.
            per_member[m] = d['direct'] + d['local1'] - states[m][1]['local0']
        actions[f'c{c}'] = per_member['cd']-per_member['host']
    actions['change'] = actions['c2']-actions['c1']
    old = np.load(OLD/'chemical_operator_matrices.npz')
    for key, Y in actions.items():
        results[key], matrices[key], _ = inspect_action(F, Y)
        past = old[{'c1':'first_total', 'c2':'updated_total', 'change':'relaxation_total'}[key]]
        error = norm(F.conj().T@Y-past)
        assert error < 2e-12
        results[key]['old_complex_matrix_reconstruction_error_Ry'] = error
    g = results['c2']['trace_meV']
    results['c2']['sharp_unseen_P_block_error_sign_radius_meV'] = g/2
    np.savez(HERE/'contracted_actions.npz', G=states['host'][1]['G'], reference=F,
             **{f'{k}_action_Ry':a for k,a in actions.items()}, **{f'{k}_P_Ry':a for k,a in matrices.items()})
    out = dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(), baseline='5dc77a9',
               native_invocations=0, new_source_edits=0, state_status='old finite acquisitions retained; NOT HSE stationary',
               observable='Cd-minus-host HSE activation relative to each preliminary PBE operator; NOT total screened substitution',
               phases=information, chemical=results, native_packet_pins=PINS,
               wall_s=time.monotonic()-start, audit_peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               interval_rounding_enclosure=False, material_gap_or_xc=None)
    (HERE/'retained_result.json').write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
    print(json.dumps(dict(phases=information, chemical=results, wall_s=out['wall_s']), indent=2))


if __name__ == '__main__':
    main()
