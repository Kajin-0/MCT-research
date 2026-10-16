"""Read existing HSE files only; no DFT modules, native calls or protected writes.

Run from MCT using the existing h5py-equipped interpreter, bytecode disabled.
Only new MCT artifacts are written. Densities are low-rank occupation kernels,
not local spin densities; matrix residuals below are not full-H residuals.
"""
from pathlib import Path
import hashlib
import itertools
import json
import resource
import time
import xml.etree.ElementTree as ET

import h5py
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf, expit
from scipy.spatial.transform import Rotation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PRIOR = ROOT / 'research/programs/microscopic_bandgap/physical_input_qualification_2026-10-11/existing_audit.json'
HA = 27.211386245988


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(p):
    with h5py.File(p, 'r') as h:
        g = h['MillerIndices'][:].astype(int)
        b = np.array([h['MillerIndices'].attrs[f'bg{i}'] for i in [1, 2, 3]])
        k = h.attrs['xk'] @ np.linalg.inv(b)
        assert h.attrs['npol'] == 2 and h.attrs['scale_factor'] == 1
        c = np.ascontiguousarray(h['evc'][:]).view(complex).reshape(-1, 2, len(g))
    return c, g, k, b


def ops():
    sigma = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]])
    result = []
    for perm in itertools.permutations(range(3)):
        for sign in itertools.product([-1, 1], repeat=3):
            if np.prod(sign) != 1:
                continue
            r = np.diag(sign) @ np.eye(3)[list(perm)]
            det = round(np.linalg.det(r))
            q = Rotation.from_matrix(det * r).as_quat()
            s = q[3] * np.eye(2) - 1j * np.einsum('a,aij->ij', q[:3], sigma)
            result.append((r, s, det))
    return result


def transform(c, g, k, b, target_g, target_k, r=None, s=None):
    if r is None:  # Theta = i sigma_y K; an overall minus sign is immaterial.
        mapped = -g - k - target_k
        values = np.stack([c[:, 1].conj(), -c[:, 0].conj()], axis=1)
    else:
        mapped = (g + k) @ b @ r.T @ np.linalg.inv(b) - target_k
        values = np.einsum('st,atg->asg', s, c)
    assert np.max(abs(mapped - np.rint(mapped))) < 1e-9
    lookup = {tuple(x): i for i, x in enumerate(target_g)}
    assert len(lookup) == len(g)
    idx = np.array([lookup[tuple(x)] for x in np.rint(mapped).astype(int)])
    ans = np.empty_like(c)
    ans[:, :, idx] = values
    return ans


def kernel_test(c, d, f, g):
    """Stable compressed witness and full Frobenius upper bound.

    U=c.T, V=d.T; V=U O+R. The compression U†(D-U')U is a
    lower witness up to measured Gram error. The explicit R gives a stable
    upper bound without subtracting two almost equal density norms.
    """
    u = c.reshape(len(c), -1).T
    v = d.reshape(len(d), -1).T
    o = u.conj().T @ v
    residual = v - u @ o
    a = np.diag(f) - (o * g) @ o.conj().T
    gram = np.linalg.norm(u.conj().T @ u - np.eye(len(f)), 2)
    rf = np.linalg.norm(residual, 'fro')
    bound = ((1+gram)*np.linalg.norm(a, 'fro')
             + 2*np.sqrt(1+gram)*np.linalg.norm(o*g, 2)*rf + max(abs(g))*rf**2)
    lower = max(0., (np.linalg.norm(a,2)-max(abs(f))*gram*(2+gram))/(1+gram))
    return dict(compressed_operator_witness=float(lower),
                full_F_upper_arithmetic=float(bound), span_residual_F=float(rf),
                source_Gram_defect=float(gram))


def main():
    start = time.monotonic()
    prior = json.loads(PRIOR.read_text())
    pins = {str(PRIOR): sha(PRIOR)}
    for name, expected in prior['verified_sources_sha256'].items():
        p = Path(name) if name.startswith('/') else ROOT / name
        assert sha(p) == expected, str(p)
        pins[str(p)] = expected
    reports = []
    for ir, name in enumerate(prior['native_reference_runs']):
        run = Path(name)
        save = run / 'out/r07.save'
        expanded = run / 'out/r07_open.save'
        tree = ET.parse(save / 'data-file-schema.xml').getroot()
        xt = ET.parse(expanded / 'data-file-schema.xml').getroot()
        for directory in [save, expanded]:
            for p in directory.iterdir():
                if p.is_file() and (p.suffix in ['.hdf5', '.UPF'] or p.name == 'data-file-schema.xml'):
                    pins[str(p)] = sha(p)
        for p in [run / 'gamma/grid_expansion.json', run / 'gamma/open_grid_result.json']:
            pins[str(p)] = sha(p)
        expansion = json.loads((run / 'gamma/grid_expansion.json').read_text())
        assert pins[str(save / 'data-file-schema.xml')] == expansion['parent_schema_sha256']
        rows = tree.findall('output/band_structure/ks_energies')
        xr = xt.findall('output/band_structure/ks_energies')
        weights = np.array([float(r.find('k_point').attrib['weight']) for r in rows])
        energies = np.array([np.fromstring(r.findtext('eigenvalues'), sep=' ') for r in rows])
        occ = np.array([np.fromstring(r.findtext('occupations'), sep=' ') for r in rows])
        mu = float(tree.findtext('output/band_structure/fermi_energy'))
        sig = float(tree.find('input/bands/smearing').attrib['degauss'])
        x = (mu - energies) / sig - 1 / np.sqrt(2)
        mv = .5 * erf(x) + np.exp(-np.minimum(200, x*x)) / np.sqrt(2*np.pi) + .5
        fd_mu = brentq(lambda v: np.sum(weights[:, None] * expit((v - energies) / sig)) - 36,
                       float(energies.min()-1), float(energies.max()+1), xtol=1e-15)
        fd = expit((fd_mu - energies) / sig)
        c, g, k, b = read(save / 'wfc1.hdf5')
        ce, ge, ke, be = read(expanded / 'wfc1.hdf5')
        assert np.array_equal(g, ge)
        assert np.allclose(k, 0, atol=1e-12) and np.array_equal(b, be)
        f = occ[0]
        td, density_td, ace_td = [], [], []
        xi, gx, kx, bx = read(save / 'ace1.hdf5')
        assert np.array_equal(g, gx) and np.array_equal(b, bx)
        xf = xi.reshape(44, -1)
        def ace(v):
            vf = v.reshape(len(v), -1)
            return (-(vf @ xf.conj().T) @ xf).reshape(v.shape)
        probes = c[32:38]
        for r, s, det in ops():
            d = transform(c, g, k, b, g, k, r, s)
            density_td.append(kernel_test(c, d, f, f))
            row = []
            for sl in [slice(32, 34), slice(34, 38)]:
                o = c[sl].reshape(sl.stop-sl.start, -1).conj() @ d[sl].reshape(sl.stop-sl.start, -1).T
                row.append(float(np.linalg.norm(np.eye(len(o))-o.conj().T @ o, 2)))
            td.append(row)
            a = ace(transform(probes, g, k, b, g, k, r, s))
            other = transform(ace(probes), g, k, b, g, k, r, s)
            ace_td.append(float(np.linalg.norm(a-other)/np.linalg.norm(a)))
        theta = transform(c, g, k, b, g, k)
        trd = kernel_test(c, theta, f, f)
        at = ace(transform(probes, g, k, b, g, k))
        tr_ace = np.linalg.norm(at-transform(ace(probes), g, k, b, g, k))/np.linalg.norm(at)
        kinetic = np.sum((g @ b)**2, axis=1)  # Ry, reciprocal vectors in bohr^-1.
        tail50 = np.sum(abs(probes[:, :, kinetic > 50+1e-10])**2, axis=(1,2))
        with h5py.File(save / 'charge-density.hdf5', 'r') as h:
            rho = np.ascontiguousarray(h['rhotot_g'][:]).view(complex)
            gm = h['MillerIndices'][:]
            rho0 = rho[np.all(gm == 0, axis=1)][0]
        cell = np.array([np.fromstring(tree.findtext('output/atomic_structure/cell/'+key), sep=' ')
                         for key in ['a1','a2','a3']])
        record = json.loads((run / 'result.json').read_text())
        stdout = (run / 'pw.out').read_text()
        import re
        dim = tuple(map(int, re.findall(r'EXX grid:.*?FFT dimensions:\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\)', stdout)[-1]))
        rr = dict(run=str(run), SCF_schema_hash_matches_preexisting_expansion_parent=True,
                  accepted_scf=record['accepted_scf'], exx_converged=record['exx_converged'],
                  inner_SCF_error_Ry=2*float(tree.findtext('output/convergence_info/scf_conv/scf_error')),
                  original_nks=len(rows), expanded_nks=len(xr), nbnd=44,
                  electron_count=float(np.sum(weights[:, None]*occ)),
                  charge_from_saved_rhoG=float(rho0.real*abs(np.linalg.det(cell))),
                  smearing='mv (cold), not fd', sigma_Ry=2*sig,
                  occupation_formula_max_error=float(np.max(abs(mv-occ))),
                  FD_reinterpretation_mu_shift_eV=float((fd_mu-mu)*HA),
                  FD_reinterpretation_charge_residual_e=float(np.sum(weights[:,None]*fd)-36),
                  FD_vs_stored_max_occupation=float(np.max(abs(fd-occ))),
                  Gamma8_eigenvalue_spread_eV=float(np.ptp(energies[0,34:38])*HA),
                  Gamma8_occupation_spread=float(np.ptp(f[34:38])),
                  Gamma_Gram_error=float(np.linalg.norm(c.reshape(44,-1).conj()@c.reshape(44,-1).T-np.eye(44),2)),
                  Gamma_Td_sector_span_leakage2_max=np.max(td,axis=0).tolist(),
                  Gamma_density_Td_compressed_witness_max=max(d['compressed_operator_witness'] for d in density_td),
                  Gamma_density_Td_F_upper=max(d['full_F_upper_arithmetic'] for d in density_td),
                  Gamma_density_Theta=trd,
                  Gamma_ACE_Td_probe_defect=max(ace_td), Gamma_ACE_Theta_probe_defect=float(tr_ace),
                  Gamma6_Gamma8_loss_projecting_e90_to_e50=tail50.tolist(),
                  Gamma_original_equals_expanded_bytes=bool(np.array_equal(c,ce)),
                  Gamma_original_vs_expanded_max_coefficient_diff=float(np.max(abs(c-ce))),
                  Gamma_original_vs_expanded_frame_distance_F=float(np.linalg.norm(c-ce)),
                  EXX_grid=list(dim), nominal_exxbuff_B=int(np.prod(dim))*2*44*64*16,
                  historical_SCF_family_RSS_B=record['measured_peak_process_family_RSS_bytes'],
                  historical_wall_s=record['wall_seconds'])
        if ir == 1:
            # Full BZ Theta and two generators of Td; no whole-H claim.
            ks = np.array([read(expanded/f'wfc{i+1}.hdf5')[2] for i in range(64)])
            all_c = [read(expanded/f'wfc{i+1}.hdf5') for i in range(64)]
            fs = np.array([np.fromstring(r.findtext('occupations'), sep=' ') for r in xr])
            generators = [(np.array([[0,1,0],[0,0,1],[1,0,0]]), 'C3'),
                          (np.array([[0,-1,0],[1,0,0],[0,0,-1]]), 'S4')]
            full = {}
            for r, label in [(None, 'Theta'), *generators]:
                ss = next(s for rt,s,_ in ops() if np.array_equal(rt,r)) if r is not None else None
                metrics = []
                for j, (cj, gj, kj, bj) in enumerate(all_c):
                    wanted = -kj if r is None else kj @ bj @ r.T @ np.linalg.inv(bj)
                    distance = np.max(abs(wanted-ks-np.rint(wanted-ks)),axis=1)
                    found = np.where(distance < 1e-9)[0]; assert len(found)==1
                    m = found[0]; ct, gt, kt, bt = all_c[m]
                    d = transform(cj,gj,kj,bj,gt,kt,r,ss)
                    metrics.append(kernel_test(ct,d,fs[m],fs[j]))
                full[label] = dict(max_compressed_witness=max(v['compressed_operator_witness'] for v in metrics),
                    max_full_F_upper=max(v['full_F_upper_arithmetic'] for v in metrics),
                    max_span_residual_F=max(v['span_residual_F'] for v in metrics))
            rr['expanded_full_BZ_density_tests'] = full
            rr['full_BZ_occupation_vs_original_weighted_charge'] = float(np.mean(fs.sum(axis=1))-36)
        reports.append(rr)
    for p, expected in pins.items():
        assert sha(p) == expected, p
    report = dict(baseline='9a83424', native_jobs=0, records=reports,
                  preserved_source_hashes=pins, wall_s=time.monotonic()-start,
                  analysis_peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  limitations=['No fresh full-H actions, eigenpair residual or nonlinear SCF certificate.',
                              'FD reinterpretation uses stored eigenvalues only, not H[updated D].',
                              'Frobenius bounds assume measured NC Gram; floating rounding not interval certified.',
                              'ACE probes are not DIRECT Fock, and expanded symmetry may be imposed by open_grid.'])
    (HERE/'native_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='preserved_source_hashes'},indent=2))


if __name__ == '__main__':
    main()
