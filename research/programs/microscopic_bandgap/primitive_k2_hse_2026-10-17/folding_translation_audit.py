"""Read the immutable rejected stock8 state; no native call or state repair."""
import importlib.util
import json
from pathlib import Path
from xml.etree import ElementTree as ET

import h5py
import numpy as np

P = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    a = load('new_analysis', P / 'analyze_state.py')
    prior = load('prior_readonly', P.parent / 'stationary_reference_audit_2026-10-16/audit_native.py')
    old = P.parent / 'stock_hse_stationary_2026-10-16'
    freeze = json.loads((old / 'preregistration.json').read_text())
    original = json.loads((old / 'host_state_result.json').read_text())
    root = Path(freeze['members']['host']['root']) / 'out/r07hse8.save'
    paths = [root / 'wfc1.hdf5', root / 'data-file-schema.xml', root / 'charge-density.hdf5']
    for p in paths:
        assert a.sha(p) == original['raw_pins'][str(p)]
    c, g, k, b = prior.read(paths[0])
    f = np.fromstring(ET.parse(paths[1]).findtext(
        'output/band_structure/ks_energies/occupations'), sep=' ')
    assert np.linalg.norm(k) < 1e-12
    assert np.linalg.norm(b - np.eye(3)*b[0, 0]) < 1e-12
    with h5py.File(paths[2], 'r') as h:
        gr = h['MillerIndices'][:]
        rho = np.ascontiguousarray(h['rhotot_g'][:]).view(complex).reshape(-1)
    rows = []
    for t in [np.array([0, 1, 1]), np.array([1, 0, 1]), np.array([1, 1, 0])]:
        sign = 1 - 2*((g @ t) % 2)
        d = c * sign[None, None, :]
        n = a.density_norm(c, d, f, f)
        rho_sign = 1 - 2*((gr @ t) % 2)
        rel = float(np.linalg.norm(rho-rho_sign*rho) / np.linalg.norm(rho))
        rows.append(dict(translation_conventional_fraction=(t/2).tolist(),
                         density_operator=n, scalar_rhoG_relative_F=rel))
    twirl = sum(row['density_operator']['op'] for row in rows)/4
    tr = original['full_density_Theta_independent_QR_op']
    for p in paths:
        assert a.sha(p) == original['raw_pins'][str(p)]
    result = dict(status='CALCULATED old rejected state; no retropass',
                  old_state_translation_tests=rows,
                  primitive_translation_twirl_distance_upper_expression=twirl,
                  Theta_defect_after_translation_twirl_lower_expression=tr-2*twirl,
                  arithmetic='QR eigenvalues in ordinary double precision; theorem exact, numerical expressions not interval-certified',
                  old_raw_pins={str(p): a.sha(p) for p in paths},
                  native_runs=0, Theta_failure_unchanged=True,
                  limitation='No twirled H or FD state constructed. Not a causal separation of sampling and nonlinear self-consistency.')
    (P / 'folding_translation_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
