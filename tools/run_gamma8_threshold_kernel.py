#!/usr/bin/env python3
"""Calculate a conditional Gamma8 infrared kernel from the published binary."""
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

import mct_research.gamma8_threshold as kernel_module
import mct_research.sp3d5 as binary_module
from mct_research.gamma8_threshold import angular_threshold_kernel,quadratic_gamma8_matrices
from mct_research.sp3d5 import BinaryModel


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


if __name__=='__main__':
    source=Path('data/materials/schindler2012_sp3d5.json')
    parameters=json.loads(source.read_text())
    model=BinaryModel(parameters['CdTe'])
    quadratic,linear_norm=quadratic_gamma8_matrices(model)
    def curvature(n):
        return -np.einsum('i,j,ijab->ab',n,n,quadratic)
    rows=[]
    for ntheta,nphi in [(16,32),(24,48),(32,64)]:
        kernel,minimum,maximum=angular_threshold_kernel(curvature,.25,ntheta,nphi)
        scalar=float(np.trace(kernel).real/4)
        row={'n_theta':ntheta,'n_phi':nphi,'scalar_kernel_eV_minus_three_halves':scalar,
             'kernel_real':kernel.real.tolist(),'kernel_imag':kernel.imag.tolist(),
             'cubic_irrep_scalar_defect_norm':float(np.linalg.norm(kernel-scalar*np.eye(4),ord=2)),
             'min_valence_curvature_eV_a_squared':minimum,
             'max_valence_curvature_eV_a_squared':maximum}
        rows.append(row)
        print({k:v for k,v in row.items() if k not in ['kernel_real','kernel_imag']},flush=True)
    report={'claim_status':'CALCULATED conditional quadratic-threshold diagnostic, not physical total A',
            'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'source':parameters['source'],'source_omissions':parameters['omissions'],
            'source_hashes':{str(p):sha(p) for p in [source,Path(__file__),Path(kernel_module.__file__),Path(binary_module.__file__)]},
            'Gamma8_linear_term_norm_eV_a':linear_norm,'dimensionless_fcc_cell_volume':.25,
            'momentum_units':'a^-1','numpy_version':np.__version__,'rows':rows,
            'last_quadrature_scalar_change':abs(rows[-1]['scalar_kernel_eV_minus_three_halves']-rows[-2]['scalar_kernel_eV_minus_three_halves']),
            'leading_single_impurity_derivative':'-T8_prime(E8+delta) ~ tau8(E8)^2 K8/sqrt(delta), if the quadratic threshold and finite nonzero forward amplitude assumptions hold',
            'applicability':'normal CdTe quadratic Gamma8 approximation; check physical linear BIA before taking delta to zero; no inverted-HgTe PSD claim',
            'empirical_alloy_gap_inputs':[]}
    target=Path('data/calculated/gamma8_quadratic_threshold_20261011.json')
    if target.exists():
        raise FileExistsError('Never overwrite a frozen kernel record')
    target.write_text(json.dumps(report,indent=2)+'\n')
