"""Read-only terminal k4 analysis. No QE, MPI, state repair or star expansion.

Use DFT/.venv/bin/python with PYTHONDONTWRITEBYTECODE=1 and BLAS threads=1.
Only this new MCT final_qualification directory is written. Native saves are
opened read-only; all 44 columns are retained in the 88-column density QR.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import resource
import time
import xml.etree.ElementTree as ET

import h5py
import numpy as np
from scipy.optimize import brentq
from scipy.special import expit, xlogy
from scipy.spatial.transform import Rotation

P = Path(__file__).resolve().parent
CASE = P.parent
B = CASE.parent
RY = 13.605693122994
OLD = Path('/home/User/opencode_workspace/DFT/calculations/r07/'
           'hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800')


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def load_prior():
    path = B/'stationary_reference_audit_2026-10-16/audit_native.py'
    spec = importlib.util.spec_from_file_location('pinned_read_only_helpers', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, path


def density_norm(c, d, f, h):
    """All-space finite-rank D-D' via QR; no rank threshold or column discard.

    Z=[U sqrt(f),V sqrt(h)]=QR, K=R diag(I,-I) R*. Nonzero
    eigenvalues of D-D' equal those of K. A direct matrix-free Rayleigh
    quotient and eigenvector residual independently check the extremal result.
    These are floating-point measurements, not interval-certified bounds.
    """
    u, v = c.reshape(len(c), -1).T, d.reshape(len(d), -1).T
    z = np.column_stack((u*np.sqrt(f), v*np.sqrt(h)))
    q, r = np.linalg.qr(z, mode='reduced')
    a = r[:, :len(f)] @ r[:, :len(f)].conj().T
    a -= r[:, len(f):] @ r[:, len(f):].conj().T
    ev, vec = np.linalg.eigh(a)
    j = np.argmax(abs(ev))
    w = q @ vec[:, j]
    actual = u @ (f*(u.conj().T @ w)) - v @ (h*(v.conj().T @ w))
    ray = np.vdot(w, actual).real/np.vdot(w, w).real
    o = u.conj().T @ v
    gram = u.conj().T @ u
    compressed = (gram*f) @ gram.conj().T - (o*h) @ o.conj().T
    return dict(op=float(max(abs(ev))), F=float(np.linalg.norm(ev)),
                direct_action_Rayleigh=float(ray),
                eigenvalue_Rayleigh_error=float(abs(ray-ev[j])),
                direct_action_eigenvector_residual=float(np.linalg.norm(actual-ev[j]*w)),
                compressed_witness=float(np.linalg.norm(compressed, 2)),
                columns_retained=z.shape[1], physical_dimension=z.shape[0])


def equivalent(k, j):
    return np.max(abs(k-j-np.rint(k-j))) < 1e-10


def main():
    start = time.monotonic()
    frozen = json.loads((CASE/'preregistration.json').read_text())
    root = Path(frozen['root'])
    save = root/'out/r07pk4.save'
    prior, helper = load_prior()
    tree = ET.parse(save/'data-file-schema.xml')
    out = tree.find('output')
    hybrid = out.find('dft/hybrid')
    assert hybrid.find('qpoint_grid').attrib == dict(nqx1='4', nqx2='4', nqx3='4')
    # Output effective Fock cutoff is authoritative; the input XML field is 0.
    assert float(hybrid.findtext('ecutfock'))*2 == 200
    assert float(hybrid.findtext('exx_fraction')) == .25
    assert float(hybrid.findtext('screening_parameter')) == .106
    assert float(out.findtext('basis_set/ecutwfc'))*2 == 50
    assert float(out.findtext('basis_set/ecutrho'))*2 == 200
    assert out.findtext('band_structure/smearing') == 'fd'
    sigma = 2*float(out.find('band_structure/smearing').attrib['degauss'])
    assert sigma == .001
    assert out.findtext('band_structure/spinorbit') == 'true'
    assert out.findtext('band_structure/noncolin') == 'true'
    assert int(out.findtext('band_structure/nbnd')) == 44
    assert float(out.findtext('band_structure/nelec')) == 36
    rows = out.findall('band_structure/ks_energies')
    assert len(rows) == 8
    cell = np.array([np.fromstring(out.findtext('atomic_structure/cell/'+a), sep=' ')
                     for a in ['a1', 'a2', 'a3']])
    xml_b = np.array([np.fromstring(out.findtext('basis_set/reciprocal_lattice/'+a), sep=' ')
                      for a in ['b1', 'b2', 'b3']])
    mu = 2*float(out.findtext('band_structure/fermi_energy'))
    states = []
    for i, row in enumerate(rows, 1):
        c, g, k, b = prior.read(save/f'wfc{i}.hdf5')
        e = 2*np.fromstring(row.findtext('eigenvalues'), sep=' ')
        f = np.fromstring(row.findtext('occupations'), sep=' ')
        w = float(row.find('k_point').attrib['weight'])
        xk = np.fromstring(row.findtext('k_point'), sep=' ') @ np.linalg.inv(xml_b)
        assert np.max(abs(xk-k)) < 1e-12
        assert len(c) == len(e) == len(f) == 44 and c.shape[2] == len(g)
        assert np.all((f >= 0) & (f <= 1))
        assert np.max(abs(b-states[0][3])) < 1e-12 if states else True
        states.append((c, g, k, b, f, e, w))
    assert abs(sum(s[6] for s in states)-1) < 1e-14
    assert states[0][6] == 1/64 and np.linalg.norm(states[0][2]) < 1e-12

    # Actual XML crystal operations (exclude the extra Bravais operations).
    crystal = [s for s in out.findall('symmetries/symmetry')
               if s.findtext('info') == 'crystal_symmetry']
    ops = prior.ops()
    xmlops = []
    for entry in crystal:
        rot = np.fromstring(entry.findtext('rotation'), sep=' ').reshape(3, 3)
        candidates = [cell.T @ a @ np.linalg.inv(cell.T) for a in [rot, rot.T]]
        cart = min(candidates, key=lambda a: min(np.linalg.norm(a-r) for r, _, _ in ops))
        index = int(np.argmin([np.linalg.norm(cart-r) for r, _, _ in ops]))
        assert np.linalg.norm(cart-ops[index][0]) < 1e-10
        assert np.linalg.norm(np.fromstring(entry.findtext('fractional_translation'), sep=' ')) < 1e-12
        xmlops.append((index, *ops[index], entry.find('info').attrib['name']))
    assert len(xmlops) == len({v[0] for v in xmlops}) == 24
    atom = out.findall('atomic_structure/atomic_positions/atom')
    assert [v.attrib['name'] for v in atom] == ['Hg', 'Te']
    assert np.linalg.norm(np.fromstring(atom[0].text, sep=' ')) < 1e-12
    assert np.linalg.norm(np.fromstring(atom[1].text, sep=' ')-.25*cell.sum(axis=0)) < 1e-12

    stored, spatial, tr_tests, missing_tr = [], [], [], []
    for i, (c, g, k, b, f, e, w) in enumerate(states):
        flat = c.reshape(44, -1)
        little = []
        for index, r, s, det, name in xmlops:
            wanted = k @ b @ r.T @ np.linalg.inv(b)
            if not equivalent(wanted, k):
                continue
            d = prior.transform(c, g, k, b, g, k, r, s)
            metric = density_norm(c, d, f, f)
            record = dict(source_k=i+1, target_k=i+1, operation=index,
                          operation_name=name, cart_rotation=r.tolist(), **metric)
            spatial.append(record)
            little.append(record)
        targets = [j for j, st in enumerate(states) if equivalent(-k, st[2])]
        assert len(targets) <= 1
        tr = None
        if targets:
            j = targets[0]
            ct, gt, kt, bt, ft, et, wt = states[j]
            d = prior.transform(c, g, k, b, gt, kt)
            d2 = prior.transform(d, gt, kt, bt, g, k)
            assert np.max(abs(d2+c)) < 1e-14
            tr = dict(source_k=i+1, target_k=j+1,
                      Theta_square_error=float(np.max(abs(d2+c))),
                      **density_norm(ct, d, ft, f))
            tr_tests.append(tr)
        else:
            missing_tr.append(dict(k_index=i+1, k_crystal=k.tolist(),
                                   missing_target_mod_G=(-k-np.floor(-k+1e-12)).tolist()))
        stored.append(dict(index=i+1, k_crystal=k.tolist(), weight=w, npw=len(g),
                           Gram_op=float(np.linalg.norm(flat.conj() @ flat.T-np.eye(44), 2)),
                           energies_eV=(e*RY).tolist(), occupations=f.tolist(),
                           electron_count_fiber=float(sum(f)),
                           FD_formula_error=float(max(abs(f-expit((mu-e)/sigma)))),
                           highest_band_f=float(f[-1]), highest_band_minus_mu_eV=float((e[-1]-mu)*RY),
                           native_little_group_count=len(little),
                           little_group_density_op_max=max(v['op'] for v in little),
                           actual_Theta_test=tr))

    # Real G-matched reference transport, without renormalizing lost e90 tails.
    c, g, k, b, f, e, w = states[0]
    oc, og, ok, ob = prior.read(OLD/'out/r07.save/wfc1.hdf5')
    old_tree = ET.parse(OLD/'out/r07.save/data-file-schema.xml')
    old_cell = np.array([np.fromstring(old_tree.findtext('output/atomic_structure/cell/'+a), sep=' ')
                         for a in ['a1', 'a2', 'a3']])
    assert np.max(abs(old_cell-cell)) < 1e-12 and np.max(abs(b-ob)) < 1e-12
    old_atom = old_tree.findall('output/atomic_structure/atomic_positions/atom')
    assert all(v.attrib['name'] == ov.attrib['name'] and
               np.max(abs(np.fromstring(v.text, sep=' ')-np.fromstring(ov.text, sep=' '))) < 1e-12
               for v, ov in zip(atom, old_atom))
    for pp in ['Hg_sg15_pbe_fr_v12.UPF', 'Te_sg15_pbe_fr_v12.UPF']:
        assert sha(save/pp) == sha(OLD/'out/r07.save'/pp)
    lookup = {tuple(x): j for j, x in enumerate(og)}
    idx = np.array([lookup[tuple(x)] for x in g])
    ref = oc[32:38][:, :, idx]
    overlap = ref.reshape(6, -1).conj() @ c.reshape(44, -1).T
    tail = np.sum(abs(oc[32:38])**2, axis=(1, 2))-np.sum(abs(ref)**2, axis=(1, 2))
    sectors = {}
    for label, sl, dim in [('Gamma6', slice(0, 2), 2), ('Gamma8', slice(2, 6), 4)]:
        weights = np.sum(abs(overlap[sl])**2, axis=0)
        selected = np.sort(np.argsort(weights)[-dim:])
        u = c[selected].reshape(dim, -1).T
        td, char, ideal = [], [], []
        for index, r, s, det, name in xmlops:
            d = prior.transform(c[selected], g, k, b, g, k, r, s).reshape(dim, -1).T
            a = u.conj().T @ d
            td.append(float(np.linalg.norm(d-u@a, 2)))
            char.append(complex(np.trace(a)))
            t = 2*Rotation.from_matrix(det*r).as_quat()[3]
            ideal.append(t if label == 'Gamma6' else det*(t**3-2*t))
        theta = prior.transform(c[selected], g, k, b, g, k).reshape(dim, -1).T
        o = u.conj().T @ theta
        sectors[label] = dict(bands_1based=(selected+1).tolist(),
                              energies_eV=(e[selected]*RY).tolist(), occupations=f[selected].tolist(),
                              energy_centroid_eV=float(np.mean(e[selected])*RY),
                              energy_spread_eV=float(np.ptp(e[selected])*RY),
                              occupation_spread=float(np.ptp(f[selected])),
                              e90_reference_weights=weights[selected].tolist(),
                              overlap_singular_values=np.linalg.svd(overlap[sl][:, selected], compute_uv=False).tolist(),
                              max_Td_amplitude_span_leakage=max(td),
                              max_Td_character_error=float(max(abs(np.array(char)-ideal))),
                              Td_characters=[[z.real, z.imag] for z in char],
                              Td_ideal_characters=ideal,
                              Theta_amplitude_span_leakage=float(np.linalg.norm(theta-u@o, 2)),
                              Theta_retained_singular_values=np.linalg.svd(o, compute_uv=False).tolist(),
                              Theta_sewing_skew_error=float(np.linalg.norm(o+o.T, 2)),
                              exact_irrep_under_frozen_amplitude_1e8=bool(max(td) <= 1e-8))
    tr = prior.transform(c, g, k, b, g, k)
    gamma_conservative = prior.kernel_test(c, tr, f, f)
    theta_overlap = c.reshape(44, -1).conj() @ tr.reshape(44, -1).T
    # Stable independent Frobenius evaluation using source/residual blocks.
    # QR only U (44 columns), instead of the weighted [U,V] (88 columns).
    u, v = c.reshape(44, -1).T, tr.reshape(44, -1).T
    uq, ur = np.linalg.qr(u, mode='reduced')
    o = uq.conj().T @ v
    residual = v-uq@o
    aa = (ur*f)@ur.conj().T-(o*f)@o.conj().T
    cross = residual@(f[:, None]*o.conj().T)
    rg = residual.conj().T@residual
    alternative_F = np.sqrt(np.linalg.norm(aa, 'fro')**2+2*np.linalg.norm(cross, 'fro')**2
                            +np.sum(f[:, None]*f[None, :]*abs(rg)**2).real)
    weighted_missing_span_op = np.linalg.norm(cross, 2)

    lines = (root/'pw.out').read_text().splitlines()
    trajectory = []
    for i, line in enumerate(lines):
        if 'est. exchange err (dexx)' not in line:
            continue
        energy = next(q for q in reversed(lines[:i]) if 'total energy' in q)
        fock = next(q for q in lines[i+1:i+8] if '+ Fock energy' in q)
        number = lambda q: float(q.split('=')[1].split()[0])
        trajectory.append(dict(source_build=len(trajectory)+2, dexx_Ry=number(line),
                               corrected_total_Ry=number(energy), Fock_half_Ry=number(fock)))
    with h5py.File(save/'charge-density.hdf5', 'r') as h:
        gm = h['MillerIndices'][:]
        rho = np.ascontiguousarray(h['rhotot_g'][:]).view(complex).reshape(-1)
        rho0 = rho[np.all(gm == 0, axis=1)][0]
    weights = np.array([s[6] for s in states])
    eig = np.array([s[5] for s in states])
    occ = np.array([s[4] for s in states])
    root_mu = brentq(lambda z: np.sum(weights[:, None]*expit((z-eig)/sigma))-36,
                     float(eig.min()-1), float(eig.max()+1), xtol=5e-16)
    charge = float(np.sum(weights[:, None]*occ))
    minus_ts = float(sigma*np.sum(weights[:, None]*(xlogy(occ, occ)+xlogy(1-occ, 1-occ))))
    delta = sectors['Gamma6']['energy_centroid_eV']-sectors['Gamma8']['energy_centroid_eV']
    interval = [min(sectors['Gamma6']['energies_eV'])-max(sectors['Gamma8']['energies_eV']),
                max(sectors['Gamma6']['energies_eV'])-min(sectors['Gamma8']['energies_eV'])]
    old_e = 2*np.fromstring(old_tree.findtext('output/band_structure/ks_energies/eigenvalues'), sep=' ')*RY
    old_delta = float(np.mean(old_e[32:34])-np.mean(old_e[34:38]))
    # Conditional only: omitted true eigenstates must all lie above E44.
    # This eigenvalue ordering/completeness is not certified by dexx.
    conditional_tail = [dict(k_index=i+1,
        omitted_dimension=2*len(st[1])-44,
        occupation_op_bound=float(expit((mu-st[5][-1])/sigma)),
        occupation_trace_bound=float((2*len(st[1])-44)*expit((mu-st[5][-1])/sigma)))
        for i, st in enumerate(states)]
    outer_ok = ('EXX self-consistency reached' in '\n'.join(lines)
                and out.findtext('convergence_info/scf_conv/convergence_achieved') == 'true'
                and trajectory[-1]['dexx_Ry'] <= 1e-9
                and 2*float(out.findtext('convergence_info/scf_conv/scf_error')) <= 1e-9)
    np.savez(P/'projected_native_state.npz', overlap=overlap, reference_lost_probability=tail,
             Gamma_energies_Ry=e, Gamma_occupations=f, Gamma_Theta_overlap=theta_overlap,
             all_eigenvalues_Ry=eig, all_occupations=occ, weights=weights)
    result = dict(status='CONVENTIONAL_NUMERICAL_SCF_PASS; STRICT_SYMMETRY_1e8_FAIL',
                  native_outer_converged=bool(outer_ok), XML_outer_convergence=out.findtext(
                      'convergence_info/scf_conv/convergence_achieved'),
                  completed_source_builds=len(trajectory)+1, trajectory=trajectory,
                  total_free_energy_Ry=2*float(out.findtext('total_energy/etot')),
                  last_inner_error_Ry=2*float(out.findtext('convergence_info/scf_conv/scf_error')),
                  Fock_half_Ry_displayed=trajectory[-1]['Fock_half_Ry'],
                  fermi_Ry=mu, fermi_eV=mu*RY, sigma_Ry=sigma,
                  electron_count=charge, weighted_charge_error_e=charge-36,
                  rhoG_charge_error_e=float(rho0.real*abs(np.linalg.det(cell))-36),
                  rhoG_zero_imag=float(rho0.imag), FD_formula_max_error=max(v['FD_formula_error'] for v in stored),
                  independent_FD_charge_root_shift_eV=float((root_mu-mu)*RY),
                  independent_FD_charge_root_residual_e=float(np.sum(weights[:, None]*expit((root_mu-eig)/sigma))-36),
                  minus_TS_Ry_reconstructed=minus_ts,
                  minus_TS_Ry_XML=2*float(out.findtext('total_energy/demet')),
                  weighted_entropy_over_kB=float(-minus_ts/sigma),
                  highest_band_occupation_max=float(max(occ[:, -1])),
                  min_highest_band_minus_mu_eV=min(v['highest_band_minus_mu_eV'] for v in stored),
                  conditional_empty_band_tail_bounds=conditional_tail,
                  empty_band_tail_hypothesis='All missing true eigenstates >= highest retained energy; no full-H/completeness certificate available',
                  stored_irreducible_states=stored, native_Gamma_weight=weights[0],
                  actual_Gamma_density_Theta_QR=tr_tests[0],
                  Gamma_density_Theta_conservative_bound=gamma_conservative,
                  Gamma_density_Theta_independent_block_F=float(alternative_F),
                  Gamma_density_Theta_weighted_out_of_44_span_op=float(weighted_missing_span_op),
                  actual_Gamma_density_Td_QR_max=max(v['op'] for v in spatial if v['source_k'] == 1),
                  native_Theta_tests=tr_tests, unavailable_native_minus_k_fibers=missing_tr,
                  all_native_little_group_density_tests=spatial,
                  native_64_fiber_Theta_or_Td_certificate=False,
                  generated_full_BZ_states=0, native_full_H_eigenpair_residual_available=False,
                  physical_frame_cell_origin_PP_G_compatible=True,
                  e90_reference_lost_probability_e50=tail.tolist(), sectors=sectors,
                  candidate_signed_Gamma_ordering_eV=delta, candidate_half_ordering_eV=delta/2,
                  pairwise_sector_level_difference_range_eV=interval,
                  ordering_status='projection/character-qualified approximate sectors; not strict1e-8 host mass or material gap bound',
                  old_e90_cold_f120_signed_ordering_eV=old_delta,
                  new_minus_old_ordering_eV=delta-old_delta,
                  old_reference_is_same_numerical_model=False,
                  strict_nonmagnetic_host_1e8_qualified=False,
                  actual_full_H_error_bound_eV=None, material_uncertainty_eV=None, physical_xc=None,
                  analysis_peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  analysis_wall_s=time.monotonic()-start,
                  analysis_source_pins={str(Path(__file__)): sha(__file__), str(helper): sha(helper)},
                  raw_pins={str(p): sha(p) for p in [root/'pw.in', root/'pw.out', root/'pw.err',
                      *sorted(save.glob('*')), OLD/'out/r07.save/wfc1.hdf5',
                      OLD/'out/r07.save/data-file-schema.xml'] if p.is_file()})
    (P/'state_result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'native_outer_converged',
          'total_free_energy_Ry', 'weighted_charge_error_e', 'FD_formula_max_error',
          'actual_Gamma_density_Theta_QR', 'actual_Gamma_density_Td_QR_max',
          'candidate_signed_Gamma_ordering_eV', 'new_minus_old_ordering_eV',
          'analysis_peak_RSS_KiB', 'analysis_wall_s']}, indent=2))


if __name__ == '__main__':
    main()
