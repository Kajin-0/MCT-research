"""Read-only native stock HSE state qualification; no solver/launch/import side effects.

Run only after the owned host stops. Uses existing NC spinor/antiunitary
formulas, actual physical G labels and saved XML. Writes this new package only.
"""
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

import h5py
import numpy as np
from scipy.special import expit, xlogy

P = Path(__file__).resolve().parent
RY = 13.605693122994


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    frozen = json.loads((P / 'preregistration.json').read_text())
    root = Path(frozen['members']['host']['root'])
    terminal = json.loads((P / 'host_terminal_manager.json').read_text())
    assert terminal['manager']['SubState'] != 'running'
    source = P.parent / 'stationary_reference_audit_2026-10-16/audit_native.py'
    spec = importlib.util.spec_from_file_location('prior_readonly_symmetry', source)
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    save = root / 'out/r07hse8.save'
    xml = ET.parse(save / 'data-file-schema.xml')
    out = xml.find('output')
    band = out.find('band_structure')
    eig = 2 * np.fromstring(band.findtext('ks_energies/eigenvalues'), sep=' ')
    occ = np.fromstring(band.findtext('ks_energies/occupations'), sep=' ')
    ef = 2 * float(band.findtext('fermi_energy'))
    c, g, k, b = prior.read(save / 'wfc1.hdf5')
    assert c.shape == (176, 2, 10827) and len(eig) == len(occ) == 176
    assert np.linalg.norm(k) < 1e-12
    gram = c.reshape(176, -1).conj() @ c.reshape(176, -1).T
    assert np.linalg.norm(gram - np.eye(176), 2) < 1e-8
    theta = prior.transform(c, g, k, b, g, k)
    full_TR = prior.kernel_test(c, theta, occ, occ)
    # Independent exact low-rank reduction: D-Theta(D)=Z diag(I,-I) Z^dagger.
    # QR keeps all directions, with no chosen truncation or assumed Kramers span.
    z = np.column_stack((c.reshape(176, -1).T * np.sqrt(occ),
                         theta.reshape(176, -1).T * np.sqrt(occ)))
    q, rr = np.linalg.qr(z, mode='reduced')
    small = rr[:, :176] @ rr[:, :176].conj().T - rr[:, 176:] @ rr[:, 176:].conj().T
    theta_eigs = np.linalg.eigvalsh(small)
    full_TR_independent_QR_op = float(max(abs(theta_eigs)))
    full_TR_independent_QR_F = float(np.linalg.norm(theta_eigs))
    del q, rr, z, small

    # Original common physical frame. Do not overlap reciprocal array indices.
    with (root / 'reference.bin').open('rb') as f:
        h = np.fromfile(f, '<i8', 4)
        assert tuple(h) == (70251406, 7809, 6, 1)
        rb = np.fromfile(f, '<f8', 9).reshape(3, 3, order='F')
        rk = np.fromfile(f, '<f8', 3)
        rg = np.fromfile(f, '<i8', 3 * 7809).reshape(3, 7809, order='F').T
        ref = np.fromfile(f, '<c16', 15618 * 6).reshape(15618, 6, order='F')
        assert not f.read(1)
    assert np.linalg.norm(rb - b) < 1e-12 and np.linalg.norm(rk - k) < 1e-12
    index = {tuple(x): i for i, x in enumerate(g)}
    embedding = np.array([index[tuple(x)] for x in rg])
    frame = np.zeros((2 * len(g), 6), complex)
    frame[embedding] = ref[:7809]
    frame[len(g) + embedding] = ref[7809:]
    frame_states = frame.T.reshape(6, 2, len(g))
    frame_theta = prior.transform(frame_states, g, k, b, g, k).reshape(6, -1).T
    w = c.reshape(176, -1).T
    o = frame.conj().T @ w
    ot = frame_theta.conj().T @ w
    d = (o * occ) @ o.conj().T
    dt = ((ot * occ) @ ot.conj().T).conj()
    values, vectors = np.linalg.eigh(d - dt)
    vv = vectors[:, np.argmax(abs(values))]
    trial = frame @ vv
    native_flat = c.reshape(176, -1).T
    reversed_flat = theta.reshape(176, -1).T
    scalar_witness = float(np.dot(occ, abs(native_flat.conj().T @ trial)**2
                                  - abs(reversed_flat.conj().T @ trial)**2))
    scalar_check_error = float(abs(scalar_witness - vv.conj() @ (d - dt) @ vv))
    td_lower = []
    for r, s, det in prior.ops():
        inverse_frame = prior.transform(frame_states, g, k, b, g, k,
                                        r=r.T, s=s.conj().T).reshape(6, -1).T
        overlap = inverse_frame.conj().T @ w
        dr = (overlap * occ) @ overlap.conj().T
        td_lower.append(float(np.linalg.norm(d - dr, 2)))
    # A small compression is not an upper bound on whole-density symmetry.
    # Only attempt the full24 tests if the independently necessary Theta gate passes.
    full_Td = []
    if full_TR['full_F_upper_arithmetic'] < 1e-8:
        for r, s, det in prior.ops():
            rotated = prior.transform(c, g, k, b, g, k, r=r, s=s)
            full_Td.append(prior.kernel_test(c, rotated, occ, occ))
    sectors = {}
    for label, sl, dim in [('Gamma6_character', slice(0, 2), 2),
                           ('Gamma8_character', slice(2, 6), 4)]:
        weights = np.sum(abs(o[sl]) ** 2, axis=0)
        top = np.argsort(weights)[-dim:]
        sectors[label] = dict(native_bands_1based=(top + 1).tolist(),
                              eigenvalues_eV=(eig[top] * RY).tolist(),
                              sector_weights=weights[top].tolist(),
                              selected_spread_eV=float(np.ptp(eig[top]) * RY),
                              saved_total_weight=float(sum(weights)))
    text = (root / 'pw.out').read_text()
    lines = text.splitlines()
    trajectory = []
    for i, line in enumerate(lines):
        if 'est. exchange err (dexx)' not in line:
            continue
        energy_line = next(s for s in reversed(lines[:i]) if 'total energy' in s)
        fock_line = next(s for s in lines[i + 1:i + 8] if '+ Fock energy' in s)
        number = lambda s: float(s.split('=')[1].split()[0])
        trajectory.append(dict(source_build=len(trajectory) + 2,
                               dexx_Ry=number(line),
                               corrected_total_Ry=number(energy_line),
                               Fock_half_Ry=number(fock_line)))
    outer_ok = ('EXX self-consistency reached' in text and bool(trajectory)
                and trajectory[-1]['dexx_Ry'] < 1e-9)
    charge_error = float(sum(occ) - 144)
    fd_error = float(np.max(abs(occ - expit((ef - eig) / .001))))
    minus_TS = float(.001 * sum(xlogy(occ, occ) + xlogy(1 - occ, 1 - occ)))
    result = dict(status='CALCULATED saved stock-QE state, not material validation',
                  native_outer_converged=outer_ok, trajectory=trajectory,
                  XML_convergence=out.findtext('convergence_info/scf_conv/convergence_achieved'),
                  total_energy_Ry=2 * float(out.findtext('total_energy/etot')),
                  XML_scf_error_Ry=2 * float(out.findtext('convergence_info/scf_conv/scf_error')),
                  charge_error_e=charge_error, FD_max_error=fd_error,
                  FD_entropy_minus_TS_Ry=minus_TS, fermi_Ry=ef,
                  native_nsym=int(out.findtext('symmetries/nsym')),
                  Gram_op=float(np.linalg.norm(gram - np.eye(176), 2)),
                  full_density_Theta=full_TR,
                  full_density_Theta_independent_QR_op=full_TR_independent_QR_op,
                  full_density_Theta_independent_QR_F=full_TR_independent_QR_F,
                  independent_scalar_Theta_witness=scalar_witness,
                  independent_scalar_Theta_check_error=scalar_check_error,
                  reference_Theta_span_defect_op=float(np.linalg.norm(
                      frame_theta - frame @ (frame.conj().T @ frame_theta), 2)),
                  frame_density_Theta_lower_op=float(np.linalg.norm(d - dt, 2)),
                  all24_Td_frame_density_lower_op=td_lower,
                  all24_Td_whole_density=full_Td,
                  full_Td_withheld_if_Theta_gate_fails=True,
                  frame_Gamma8_density_eigenvalues=np.linalg.eigvalsh(d[2:, 2:]).tolist(),
                  sectors=sectors,
                  symmetry_certified=(full_TR['full_F_upper_arithmetic'] < 1e-8
                                      and len(full_Td) == 24 and all(
                                          q['full_F_upper_arithmetic'] < 1e-8
                                          for q in full_Td)),
                  actual_full_H_eigenpair_residual_packet_available=False,
                  full_H_residual_not_inferred_from_dexx=True,
                  stationary_nonmagnetic_host_accepted=False,
                  Cd_launched=False, physical_xc=None,
                  raw_pins={str(p): sha(p) for p in [root / 'pw.in', root / 'pw.out',
                            root / 'pw.err', root / 'reference.bin',
                            save / 'data-file-schema.xml', save / 'wfc1.hdf5',
                            save / 'charge-density.hdf5', *sorted(save.glob('ace*.hdf5'))]},
                  analysis_pins={str(p): sha(p) for p in [Path(__file__), source]})
    np.savez(P / 'host_projected_state.npz', overlap=o, Theta_overlap=ot,
             density=d, Theta_density=dt, eigen_Ry=eig, occupations=occ)
    (P / 'host_state_result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
