"""Bounded first-ACE comparison. Reading packets never grants a native lease.

Corresponding direct/ACE actions are compared BETWEEN implementations. There
is deliberately no direct=ACE assertion for an arbitrary off-span probe.
"""
from pathlib import Path
import hashlib
import os
import stat
import struct
import numpy as np

MAX_FILE = 128*2**20
RTOL = 1e-12
ATOL = 1e-13
ENERGY_ATOL_RY = 1e-12


class Refusal(ValueError):
    pass


def read_regular(path, limit=MAX_FILE):
    # Pin the opened inode, enforce size before allocation, refuse aliases.
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        s = os.fstat(fd)
        if not stat.S_ISREG(s.st_mode) or not 96 <= s.st_size <= limit or s.st_nlink != 1:
            raise Refusal('bounded unaliased regular evidence required')
        with os.fdopen(os.dup(fd), 'rb') as f:
            raw = f.read(s.st_size+1)
        after = os.fstat(fd)
        identity = lambda v: (v.st_dev, v.st_ino, v.st_size, v.st_nlink, v.st_mtime_ns, v.st_ctime_ns)
        if len(raw) != s.st_size or identity(after) != identity(s):
            raise Refusal('packet changed during read')
        return raw
    finally:
        os.close(fd)


def decode(path):
    raw = read_regular(path)
    if raw[:16] != b'QE75-ACE-DIAG01 ':
        raise Refusal('diagnostic magic')
    h = struct.unpack_from('=9q', raw, 16)
    version, rank, k, stage, padded, active, spin, bands, nl = h
    if (version, spin, bands) != (1, 2, 48) or rank not in [0, 1] or not 1 <= k <= 8:
        raise Refusal('exact 48-band/two-rank fixture required')
    if stage not in [1, 2] or not 1 <= active <= padded <= 19683 or not 1 <= nl <= 2_000_000:
        raise Refusal('bounded diagnostic shape')
    pos = 96
    def take(n):
        nonlocal pos
        if n < 0 or pos+n > len(raw):
            raise Refusal('truncated diagnostic')
        result = raw[pos:pos+n]
        pos += n
        return result
    energy = struct.unpack_from('=d', raw, 88)[0]
    layout = np.frombuffer(take(8*nl), dtype='=i8').copy()
    labels = np.frombuffer(take(8*active), dtype='=i8').copy()
    if np.min(labels) < 1 or len(set(labels.tolist())) != active:
        raise Refusal('duplicate/invalid reciprocal ownership')
    physical = np.r_[np.arange(active), padded+np.arange(active)]
    rows = padded*spin
    def matrix(nrows, cols):
        return np.frombuffer(take(16*nrows*cols), dtype='=c16').copy().reshape((nrows, cols), order='F')
    def waves(cols, field):
        # Only native unused padding is excluded; never phase align, rescale,
        # rotate bands or omit any active plane wave/spinor component.
        full = matrix(rows, cols)
        if field != 'phi':
            padding = np.r_[np.arange(active, padded), padded+np.arange(active, padded)]
            if np.any(full[padding, :]):
                raise Refusal('native operator/probe padding must be zero: '+field)
        return full[physical, :]
    d = dict(header=h, rank=rank, k=k, stage=stage, energy=energy, layout=layout,
             global_g=labels, packet_sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    if stage == 1:
        n1, n2 = struct.unpack('=2q', take(16))
        if n1 != 48 or not 1 <= n2 <= 8:
            raise Refusal('exact source occupation shape')
        d['occupation'] = np.frombuffer(take(8*n1*n2), dtype='=f8').copy().reshape((n1, n2), order='F')
        phi, vphi = [], []
        for _ in range(48):
            phi.append(waves(1, 'phi')[:, 0]); vphi.append(waves(1, 'vphi')[:, 0])
        d.update(phi=np.array(phi).T, vphi=np.array(vphi).T,
                 gram=matrix(48, 48), probe=waves(1, 'probe'), action=waves(1, 'direct action'))
    else:
        d.update(xi=waves(48, 'xi'), factor=matrix(48, 48), action=waves(1, 'ACE action'))
    if pos != len(raw):
        raise Refusal('extended diagnostic')
    for name, value in d.items():
        if isinstance(value, (np.ndarray, float)) and not np.all(np.isfinite(value)):
            raise Refusal('nonfinite active diagnostic: '+name)
    return d


def defect(a, b):
    delta = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    scale = float(max(np.max(np.abs(a)), np.max(np.abs(b))))
    bound = max(ATOL, RTOL*scale)
    return dict(absolute_max=delta, scale_max=scale,
                relative_max=delta/max(scale, ATOL), acceptance_bound=bound,
                passed=delta <= bound)


def compare(control, streamed, ks):
    if not ks or list(ks) != sorted(set(ks)) or not all(1 <= k <= 8 for k in ks):
        raise Refusal('explicit actual k coverage required')
    wanted = {(r, k, s) for r in [0, 1] for k in ks for s in [1, 2]}
    if set(control) != wanted or set(streamed) != wanted:
        raise Refusal('complete two-rank/k/stage coverage required')
    modes = {}
    consistency = {}
    for name, group in [('control', control), ('stream', streamed)]:
        modes[name] = {key: decode(path) for key, path in group.items()}
        for key, d in modes[name].items():
            if (d['rank'], d['k'], d['stage']) != key:
                raise Refusal('packet mislabeled')
        for k in ks:
            for stage in [1, 2]:
                a, b = [modes[name][(r, k, stage)] for r in [0, 1]]
                if set(a['global_g']).intersection(b['global_g']):
                    raise Refusal('duplicated reciprocal rows across ranks')
                if a['energy'] != b['energy']:
                    raise Refusal('replicated native energy differs across ranks')
            for r in [0, 1]:
                before, after = [modes[name][(r, k, s)] for s in [1, 2]]
                if before['header'][:3]+before['header'][4:] != after['header'][:3]+after['header'][4:]:
                    raise Refusal('within-member stage descriptor changed')
                for key in ['layout', 'global_g']:
                    if not np.array_equal(before[key], after[key]):
                        raise Refusal('within-member stage maps changed')
                if before['energy'] != after['energy']:
                    raise Refusal('within-member energy identity lost')
            # Gram/factor and occupations are native globally reduced/shared
            # records. NEVER sum their duplicate rank copies as energies.
            for stage, keys in [(1, ['gram', 'occupation']), (2, ['factor'])]:
                a, b = [modes[name][(r, k, stage)] for r in [0, 1]]
                if any(not np.array_equal(a[key], b[key]) for key in keys):
                    raise Refusal('replicated native contraction differs across ranks')
            initial = [modes[name][(r, k, 1)] for r in [0, 1]]
            final = [modes[name][(r, k, 2)] for r in [0, 1]]
            # Independent contractions on the complete physical basis detect
            # a COMMON wrong diagnostic, not just differences between modes.
            nc = sum(d['phi'].conj().T @ d['phi'] for d in initial)
            gram = sum(d['phi'].conj().T @ d['vphi'] for d in initial)
            overlap = sum(z['xi'].conj().T @ d['probe'] for z, d in zip(final, initial))
            c = dict(NC_Gram=defect(nc, np.eye(48)),
                     direct_Gram=defect(gram, initial[0]['gram']),
                     probe_norm=defect(np.array([sum(np.vdot(d['probe'], d['probe']).real for d in initial)]), np.array([1.])))
            for rank, z in enumerate(final):
                c['ACE_action_rank'+str(rank)] = defect(-(z['xi'] @ overlap), z['action'])
            if not all(v['passed'] for v in c.values()):
                raise Refusal('independent native contraction/action inconsistency: '+str(c))
            consistency[name+'.k'+str(k)] = c
    errors, exact = {}, []
    for key in sorted(wanted):
        a, b = [modes[m][key] for m in ['control', 'stream']]
        if a['header'] != b['header']:
            raise Refusal('paired descriptor changed')
        for field in ['layout', 'global_g'] + (['phi', 'occupation', 'probe'] if key[2] == 1 else []):
            if not np.array_equal(a[field], b[field]):
                raise Refusal('actual paired input/maps differ: '+field)
        exact.append(dict(rank=key[0], k=key[1], stage=key[2],
                          control_sha256=a['packet_sha256'], stream_sha256=b['packet_sha256']))
    energy_delta = 0.
    for k in ks:
        per_k = modes['control'][(0, k, 1)]['energy']-modes['stream'][(0, k, 1)]['energy']
        if abs(per_k) > ENERGY_ATOL_RY:
            raise Refusal('per-k native exchange-energy mismatch')
        energy_delta += modes['control'][(0, k, 1)]['energy']-modes['stream'][(0, k, 1)]['energy']
        for stage, keys in [(1, ['vphi', 'gram', 'action']), (2, ['xi', 'factor', 'action'])]:
            for field in keys:
                # Concatenation spans all rank-owned physical rows. Duplicated
                # global contractions can instead use the unique root copy.
                ranks = [0] if field in ['gram', 'factor'] else [0, 1]
                a, b = [np.concatenate([modes[m][(r, k, stage)][field].ravel() for r in ranks])
                        for m in ['control', 'stream']]
                errors[f'k{k}.stage{stage}.{field}'] = defect(a, b)
    if any(not d['passed'] for d in errors.values()) or abs(energy_delta) > ENERGY_ATOL_RY:
        raise Refusal('quantitative EXX/ACE mismatch: '+str(dict(errors=errors, energy_delta_Ry=energy_delta)))
    return dict(passed=True, quantitative_errors=errors, summed_unique_k_energy_delta_Ry=energy_delta,
                energy_abs_tolerance_Ry=ENERGY_ATOL_RY, rtol=RTOL, atol=ATOL,
                exact_active_input_and_map_records=exact,
                independent_contraction_checks=consistency,
                comparison='control-direct vs stream-direct; control-ACE vs stream-ACE',
                padding_only_excluded=True, direct_equals_ACE_not_assumed=True,
                native_provenance_and_lease_must_be_supplied_separately=True,
                SCF_restart_or_physical_HgCdTe_validation=False)
