"""Read-only analysis of the one stock-QE primitive control. No native calls.

Full-BZ states below are reconstructed from the three saved representatives,
not native full-BZ exports. Test all paths, not a forced symmetrized density.
"""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET

import h5py
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.special import expit, xlogy

P = Path(__file__).resolve().parent
RY = 13.605693122994


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def density_norm(c, d, f, h):
    """Exact finite-rank QR representation, no discarded singular directions.

    D-D' = Z diag(I,-I) Z†. QR retains every column, including null ones;
    eigenvalues of R diag(I,-I) R† give the finite-precision op/F norms.
    These are calculated IEEE values, not rigorous interval enclosures.
    """
    u = c.reshape(len(c), -1).T
    v = d.reshape(len(d), -1).T
    z = np.column_stack((u * np.sqrt(f), v * np.sqrt(h)))
    _, rr = np.linalg.qr(z, mode='reduced')
    a = rr[:, :len(f)] @ rr[:, :len(f)].conj().T
    a -= rr[:, len(f):] @ rr[:, len(f):].conj().T
    vals = np.linalg.eigvalsh(a)
    # An independently contracted scalar witness cannot exceed the QR norm.
    o = u.conj().T @ v
    gram = u.conj().T @ u
    comp = (gram * f) @ gram.conj().T - (o * h) @ o.conj().T
    w = np.linalg.eigh(comp)[1][:, np.argmax(abs(np.linalg.eigvalsh(comp)))]
    trial = u @ w
    scalar = float(np.dot(f, abs(u.conj().T @ trial)**2)
                   - np.dot(h, abs(v.conj().T @ trial)**2)) / float(np.vdot(trial, trial).real)
    return dict(op=float(max(abs(vals))), F=float(np.linalg.norm(vals)),
                scalar_witness=scalar,
                scalar_crosscheck_error=float(abs(w.conj() @ comp @ w
                    / np.vdot(trial, trial).real - scalar)))


def canonical(k):
    j = np.rint(2 * k).astype(int)
    assert np.max(abs(k - j / 2)) < 1e-10
    return tuple(j % 2)


def printed_gamma_history(lines, nbnd, selected):
    """Native displayed values; rounded to .0001eV, not full-precision packets.

    Provisional index tracking becomes a sector claim only after final physical
    association. It cannot certify that every intermediate subspace is the same.
    """
    history = []
    for i, line in enumerate(lines):
        if not re.search(r'k\s*=\s*0\.0000\s+0\.0000\s+0\.0000', line):
            continue
        energies = []
        for text in lines[i+2:]:
            if not text.strip():
                if energies:
                    break
                continue
            energies += list(map(float, re.findall(r'[-+]?\d+\.\d+', text)))
        if len(energies) != nbnd:
            continue
        chosen = np.array(energies)[selected]
        spread = float(np.ptp(chosen))
        history.append(dict(inner_block_1based=len(history)+1,
                            prior_ACE_builds=sum('ACE projected onto' in q for q in lines[:i]),
                            tracked_indices_1based=[j+1 for j in selected],
                            displayed_energies_eV=chosen.tolist(),
                            displayed_spread_eV=spread,
                            rounding_only_spread_interval_eV=[max(0,spread-.0001),spread+.0001]))
    return history


def main():
    freeze = json.loads((P / 'preregistration.json').read_text())
    terminal = json.loads((P / 'terminal_manager.json').read_text())
    assert terminal['manager']['SubState'] != 'running'
    root = Path(freeze['root'])
    save = root / 'out/r07pk2.save'
    source = P.parent / 'stationary_reference_audit_2026-10-16/audit_native.py'
    spec = importlib.util.spec_from_file_location('read_only_prior', source)
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    tree = ET.parse(save / 'data-file-schema.xml')
    out = tree.find('output')
    rows = out.findall('band_structure/ks_energies')
    assert len(rows) == 3
    hybrid = out.find('dft/hybrid')
    assert hybrid.find('qpoint_grid').attrib == dict(nqx1='2', nqx2='2', nqx3='2')
    assert abs(float(hybrid.findtext('ecutfock'))*2-200) < 1e-12
    assert abs(float(hybrid.findtext('exx_fraction'))-.25) < 1e-12
    assert abs(float(hybrid.findtext('screening_parameter'))-.106) < 1e-12
    xml_b = np.array([np.fromstring(out.findtext('basis_set/reciprocal_lattice/'+a),sep=' ')
                      for a in ['b1','b2','b3']])
    fermi = 2 * float(out.findtext('band_structure/fermi_energy'))
    states, stored = [], []
    weights = []
    for i, row in enumerate(rows, 1):
        c, g, k, b = prior.read(save / f'wfc{i}.hdf5')
        f = np.fromstring(row.findtext('occupations'), sep=' ')
        e = 2 * np.fromstring(row.findtext('eigenvalues'), sep=' ')
        weight = float(row.find('k_point').attrib['weight'])
        xml_k = np.fromstring(row.findtext('k_point'), sep=' ') @ np.linalg.inv(xml_b)
        assert np.max(abs(xml_k-k)) < 1e-12
        assert len(c) == len(f) == len(e) == 44
        assert np.max(abs(2 * k - np.rint(2 * k))) < 1e-10
        assert min(f) >= 0 and max(f) <= 1
        assert np.max(abs(b - states[0][3])) < 1e-12 if states else True
        flat = c.reshape(44, -1)
        gram = float(np.linalg.norm(flat.conj() @ flat.T - np.eye(44), 2))
        tr = prior.transform(c, g, k, b, g, k)
        tr2 = prior.transform(tr, g, k, b, g, k)
        assert np.max(abs(tr2+c)) < 1e-14
        trnorm = density_norm(c, tr, f, f)
        theta_overlap = flat.conj() @ tr.reshape(44,-1).T
        partners = np.argmax(abs(theta_overlap)**2, axis=0)
        theta_rows = []
        for j in range(44):
            partner = partners[j]
            theta_rows.append(dict(band_1based=j+1, largest_Theta_overlap_band_1based=int(partner+1),
                                   largest_Theta_overlap_probability=float(abs(theta_overlap[partner,j])**2),
                                   occupation=float(f[j]), partner_occupation=float(f[partner]),
                                   energy_difference_eV=float(abs(e[j]-e[partner])*RY),
                                   retained_Theta_probability=float(sum(abs(theta_overlap[:,j])**2))))
        states.append((c, g, k, b, f, e))
        weights.append(weight)
        stored.append(dict(k_index=i, k_crystal=k.tolist(), weight=weight,
                           npw=len(g), Gram_op=gram, occupations=f.tolist(),
                           eigenvalues_eV=(e * RY).tolist(),
                           FD_max_error=float(max(abs(f - expit((fermi-e) / .001)))),
                           Theta=trnorm,
                           Theta_squared_error=float(np.max(abs(tr2+c))),
                           Theta_overlap_partner_diagnostics=theta_rows,
                           partner_note='Largest overlap is descriptive; a degenerate manifold need not have a unique native-band partner. Full density norm is basis independent.',
                           retained_Theta_energy_commutator_op_eV=float(np.linalg.norm(
                               (e[:,None]-e[None,:])*theta_overlap,2)*RY),
                           energy_commutator_not_full_H_residual=True,
                           adjacent_pair_energy_max_eV=float(max(abs(e[::2]-e[1::2]))*RY),
                           adjacent_pair_occupation_max=float(max(abs(f[::2]-f[1::2])))))
    assert abs(sum(weights) - 1) < 1e-12
    assert np.max(abs(np.array(weights) - [1/8, 4/8, 3/8])) < 1e-12

    # No density averaging. Choose one star path, then test ALL other paths.
    ops = prior.ops()
    full = {}
    for key in itertools.product([0, 1], repeat=3):
        kt = np.array(key) / 2
        found = False
        for i, (c, g, k, b, f, e) in enumerate(states):
            for ir, (r, s, det) in enumerate(ops):
                kr = k @ b @ r.T @ np.linalg.inv(b)
                if np.max(abs(kr - kt - np.rint(kr-kt))) > 1e-10:
                    continue
                gr = (g+k) @ b @ r.T @ np.linalg.inv(b) - kt
                assert np.max(abs(gr-np.rint(gr))) < 1e-9
                cr = np.einsum('st,atg->asg', s, c)
                full[key] = (cr, np.rint(gr).astype(int), kt, b, f, e, i, ir)
                found = True
                break
            if found:
                break
        assert found, key
    full_TR, covariance = [], []
    for key, (c, g, k, b, f, e, origin, path) in full.items():
        tr = prior.transform(c, g, k, b, g, k)
        full_TR.append(dict(k=list(k), source_index=origin+1,
                            rotation_index=path, **density_norm(c, tr, f, f)))
        for ir, (r, s, det) in enumerate(ops):
            target = canonical(k @ b @ r.T @ np.linalg.inv(b))
            d, gd, kd, bd, fd, *_ = full[target]
            rotated = prior.transform(c, g, k, b, gd, kd, r=r, s=s)
            covariance.append(dict(k=list(k), target_k=list(kd), rotation_index=ir,
                                    **density_norm(d, rotated, fd, f)))

    # Identify through the old physical frame but do NOT renormalize lost e90 tails.
    old = Path('/home/User/opencode_workspace/DFT/calculations/r07/'
               'hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800/'
               'out/r07.save/wfc1.hdf5')
    oldc, oldg, oldk, oldb = prior.read(old)
    c, g, k, b, f, e = states[0]
    assert np.linalg.norm(k) < 1e-12 and np.max(abs(b-oldb)) < 1e-12
    lookup = {tuple(x): j for j, x in enumerate(oldg)}
    indices = np.array([lookup[tuple(x)] for x in g])
    reference = oldc[32:38, :, indices]
    overlap = reference.reshape(6, -1).conj() @ c.reshape(44, -1).T
    tail = 1 - np.sum(abs(reference)**2, axis=(1, 2))
    sectors = {}
    for label, sl, dim in [('Gamma6', slice(0, 2), 2), ('Gamma8', slice(2, 6), 4)]:
        wgt = np.sum(abs(overlap[sl])**2, axis=0)
        selected = np.sort(np.argsort(wgt)[-dim:])
        u = c[selected].reshape(dim, -1).T
        characters, ideal, leakage = [], [], []
        for r, s, det in ops:
            rot = prior.transform(c[selected], g, k, b, g, k, r=r, s=s).reshape(dim,-1).T
            a = u.conj().T @ rot
            characters.append(complex(np.trace(a)))
            t = 2 * Rotation.from_matrix(det * r).as_quat()[3]
            ideal.append(t if label == 'Gamma6' else det*(t**3-2*t))
            leakage.append(float(np.linalg.norm(rot-u@a, 2)))
        sectors[label] = dict(native_bands_1based=(selected+1).tolist(),
                              energies_eV=(e[selected]*RY).tolist(),
                              weights=wgt[selected].tolist(),
                              spread_eV=float(np.ptp(e[selected])*RY),
                              occupation_spread=float(np.ptp(f[selected])),
                              max_Td_span_leakage_op=max(leakage),
                              max_character_error=float(max(abs(np.array(characters)-ideal))),
                              characters=[[v.real,v.imag] for v in characters])
    lines = (root / 'pw.out').read_text().splitlines()
    # Final irrep association does not itself prove continuity of earlier bands.
    history = printed_gamma_history(lines, 44,
              [j-1 for j in sectors['Gamma8']['native_bands_1based']])
    trajectory = []
    for i, line in enumerate(lines):
        if 'est. exchange err (dexx)' in line:
            energy = next(q for q in reversed(lines[:i]) if 'total energy' in q)
            fock = next(q for q in lines[i+1:i+8] if '+ Fock energy' in q)
            num = lambda q: float(q.split('=')[1].split()[0])
            trajectory.append(dict(source_build=len(trajectory)+2, dexx_Ry=num(line),
                                   corrected_total_Ry=num(energy), Fock_half_Ry=num(fock)))
    with h5py.File(save / 'charge-density.hdf5', 'r') as h:
        gm = h['MillerIndices'][:]
        rho = np.ascontiguousarray(h['rhotot_g'][:]).view(complex).reshape(-1)
        rho0 = rho[np.all(gm == 0, axis=1)][0]
    cell = np.array([np.fromstring(out.findtext('atomic_structure/cell/'+a), sep=' ')
                     for a in ['a1','a2','a3']])
    # Verify actual XML space operations against the physical Cartesian Td group.
    xml_crystal = [s for s in out.findall('symmetries/symmetry')
                   if s.findtext('info')=='crystal_symmetry']
    xml_rot = [np.fromstring(s.findtext('rotation'),sep=' ').reshape(3,3)
               for s in xml_crystal]
    assert all(np.linalg.norm(np.fromstring(s.findtext('fractional_translation'),sep=' '))
               < 1e-12 for s in xml_crystal)
    cart_candidates = []
    for transpose in [False, True]:
        rr = [cell.T @ (s.T if transpose else s) @ np.linalg.inv(cell.T) for s in xml_rot]
        orth = max(float(np.linalg.norm(r.T@r-np.eye(3))) for r in rr)
        cart_candidates.append((orth,transpose,rr))
    orth, xml_transposed, xml_cart = min(cart_candidates,key=lambda q:q[0])
    assert len(xml_cart)==24 and orth<1e-10
    assert all(min(np.linalg.norm(r-op[0]) for op in ops)<1e-10 for r in xml_cart)
    pos = out.findall('atomic_structure/atomic_positions/atom')
    assert [a.attrib['name'] for a in pos]==['Hg','Te']
    actual_positions=np.array([np.fromstring(a.text,sep=' ') for a in pos])
    assert np.linalg.norm(actual_positions[0])<1e-12
    assert np.linalg.norm(actual_positions[1]-.25*cell.sum(axis=0))<1e-12
    oldtree=ET.parse(old.parent/'data-file-schema.xml')
    oldcell=np.array([np.fromstring(oldtree.findtext('output/atomic_structure/cell/'+a),sep=' ')
                      for a in ['a1','a2','a3']])
    assert np.max(abs(cell-oldcell))<1e-12
    charge = sum(weights[i] * sum(q[4]) for i,q in enumerate(states))
    totaltext = '\n'.join(lines)
    start = next(i for i,s in enumerate(lines) if '(k+q)-points:' in s)
    qtable = []
    for line in lines[start+1:]:
        if not line.strip():
            break
        values = line.split()
        assert len(values) == 5
        cart = np.array(list(map(float, values[:3])))
        frac = cart @ np.linalg.inv(xml_b)
        assert np.max(abs(2*frac-np.rint(2*frac))) < 3e-7
        qtable.append(dict(cart_2pi_over_alat=cart.tolist(),
                           crystal_rounded=(np.rint(2*frac)/2).tolist(),
                           irreducible_index=int(values[3]), symmetry_index=int(values[4])))
    assert len(qtable)==8
    assert {canonical(np.array(q['crystal_rounded'])) for q in qtable} == set(full)
    outer_ok = bool(trajectory and 'EXX self-consistency reached' in totaltext
                    and trajectory[-1]['dexx_Ry'] <= 1e-9
                    and out.findtext('convergence_info/scf_conv/convergence_achieved')=='true')
    maxtr = max(q['op'] for q in full_TR)
    maxtd = max(q['op'] for q in covariance)
    result = dict(status='CALCULATED finite-smearing primitive k2/q2 HSE control',
                  native_outer_converged=outer_ok, trajectory=trajectory,
                  displayed_Gamma8_index_history=history,
                  XML_convergence=out.findtext('convergence_info/scf_conv/convergence_achieved'),
                  total_energy_Ry=2*float(out.findtext('total_energy/etot')),
                  inner_scf_error_Ry=2*float(out.findtext('convergence_info/scf_conv/scf_error')),
                  fermi_Ry=fermi, charge_error_e=float(charge-36),
                  independent_rhoG_charge_error_e=float(rho0.real*abs(np.linalg.det(cell))-36),
                  FD_entropy_minus_TS_Ry=float(.001*sum(weights[i]*sum(
                      xlogy(q[4],q[4])+xlogy(1-q[4],1-q[4])) for i,q in enumerate(states))),
                  stored_irreducible_states=stored,
                  native_qpoint_grid_XML=hybrid.find('qpoint_grid').attrib,
                  actual_q_source_coordinates_stdout=qtable,
                  explicit_q_coordinates_in_XML=False,
                  q_coordinate_evidence='XML stores q-grid dimensions; stdout stores actual8 k+q source coordinates. At Gamma these are the q mesh. Not mislabelled as explicit XML coordinates.',
                  full_BZ_reconstructed_Theta=full_TR,
                  full_BZ_Td_covariance=covariance,
                  full_BZ_direct_sum_Theta_op=maxtr,
                  full_BZ_direct_sum_Td_op=maxtd,
                  reconstruction='8 symmetry-transported fibers; NOT native full-BZ readback or bitwise EXX source replay; covariance checks all24x8 paths without averaging',
                  reference_e90_lost_probability_e50=tail.tolist(),
                  sectors=sectors,
                  native_nsym=int(out.findtext('symmetries/nsym')),
                  native_nrot=int(out.findtext('symmetries/nrot')),
                  XML_cartesian_Td_group_verified=True,
                  XML_rotation_array_transposed_for_cartesian=xml_transposed,
                  XML_rotation_cartesian_orthogonality_error=orth,
                  original_primitive_cell_origin_compatible=True,
                  symmetry_1e8_qualified=(maxtr<=1e-8 and maxtd<=1e-8),
                  actual_full_H_eigenpair_residual_available=False,
                  stationary_nonmagnetic_host_accepted=False,
                  final_interpretation_record='decision.md', Cd_runs=0, physical_xc=None,
                  raw_pins={str(q):sha(q) for q in [root/'pw.in',root/'pw.out',root/'pw.err',
                       *sorted(save.glob('*.xml')),*sorted(save.glob('*.hdf5')),old]},
                  analysis_pins={str(q):sha(q) for q in [Path(__file__),source]})
    np.savez(P/'projected_state.npz', overlap=overlap, reference_tail=tail,
             energies_Ry=states[0][5], occupations=states[0][4])
    (P/'state_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in
                     ['raw_pins','analysis_pins','full_BZ_Td_covariance','stored_irreducible_states','sectors']},indent=2))


if __name__ == '__main__':
    main()
