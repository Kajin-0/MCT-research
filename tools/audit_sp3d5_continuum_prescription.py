#!/usr/bin/env python3
"""Audit distinct continuum prescriptions in the archived diagnostic model.

The model is rejected as a physical impurity predictor. This calculation
tests a mathematical prescription; it does not generate a new alloy root.
At finite eta, T[Herm(g)] is not a principal-value thermodynamic limit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

from mct_research.impurity_tmatrix import branch_trace, t_matrix
from mct_research.sp3d5 import BinaryModel, host_embedding, star_embedding, star_potential
import mct_research.impurity_tmatrix as t_module
import mct_research.sp3d5 as binary_module


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args):
    if args.output.exists():
        raise FileExistsError('Do not overwrite a frozen prescription audit')
    if any(m < 2 or m % 2 for m in args.mesh) or any(e <= 0 for e in args.eta):
        raise ValueError('Positive eta and even midpoint grids are required')
    path = Path('data/materials/schindler2012_sp3d5.json')
    parameters = json.loads(path.read_text())
    raw = {name:BinaryModel(parameters[name]) for name in ['HgTe','CdTe']}
    models = {name:BinaryModel(parameters[name],-raw[name].gamma_sectors()['E8']-(.4 if name=='CdTe' else 0))
              for name in raw}
    rows = []
    for host, guest in [('HgTe','CdTe'),('CdTe','HgTe')]:
        sec = models[host].gamma_sectors()
        states = {str(a):star_embedding(np.zeros(3)) @ sec[f'states{a}'] for a in [6,8]}
        v = star_potential(models[host],models[guest],.25)
        energy = (sec['E6']+sec['E8'])/2
        for mesh in args.mesh:
            embedded = host_embedding(models[host],mesh)
            for eta in args.eta+([0.] if host=='CdTe' else []):
                g = embedded.resolvent(energy+1j*eta)
                h = (g+g.conj().T)/2
                gamma = -(g-g.conj().T)/(2j)
                tr = t_matrix(v,g)
                kh = t_matrix(v,h)
                from_k = np.linalg.solve(np.eye(len(v))+1j*kh @ gamma,kh)
                conversion_error = float(np.linalg.norm(tr-from_k,2)/max(np.linalg.norm(tr,2),1))
                if conversion_error > 1e-10:
                    raise ValueError('Ordered reactance-to-retarded conversion failed')
                th = (tr+tr.conj().T)/2
                branches = {a:dict(retarded_real_eV=branch_trace(th,states[a]).real,
                    retarded_imag_eV=branch_trace(tr,states[a]).imag,
                    hermitian_resolvent_reactance_eV=branch_trace(kh,states[a]).real)
                    for a in ['6','8']}
                mass_r = (branches['6']['retarded_real_eV']-branches['8']['retarded_real_eV'])/2
                mass_h = (branches['6']['hermitian_resolvent_reactance_eV']-branches['8']['hermitian_resolvent_reactance_eV'])/2
                row = dict(host=host,guest=guest,mesh=mesh,eta_eV=eta,energy_eV=energy,
                    retarded_vs_conversion_relative_error=conversion_error,
                    reactance_hermiticity_relative_error=float(np.linalg.norm(kh-kh.conj().T,2)/max(np.linalg.norm(kh,2),1)),
                    retarded_vs_hermitian_resolvent_operator_difference_eV=float(np.linalg.norm(th-kh,2)),
                    hermitian_resolvent_denominator_min_singular=float(np.linalg.svd(np.eye(len(v))-v @ h,compute_uv=False).min()),
                    minimum_absorptive_resolvent_eigenvalue_eV_inverse=float(np.linalg.eigvalsh(gamma).min()),
                    branches=branches,retarded_full_mass_projection_eV=mass_r,
                    hermitian_resolvent_full_mass_projection_eV=mass_h,
                    mass_prescription_difference_eV=mass_h-mass_r)
                rows.append(row)
                print(f'{host} mesh={mesh} eta={eta:g}: mass difference {1000*(mass_h-mass_r):.6g} meV; conversion error {conversion_error:.2g}',flush=True)
            del embedded
    record = dict(
        claim_status='CALCULATED mathematical prescription audit in an archived, rejected binary-derived impurity model; no physical alloy coefficient',
        git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        driver_sha256=digest(__file__),module_sha256={m.__name__:digest(m.__file__) for m in [t_module,binary_module]},
        parameter_file_sha256=digest(path),source=parameters['source'],offset_eV=.4,te_share=.25,
        quadrature='Even midpoint primitive reciprocal grid, no discrete Gamma pole',
        identities={'g':'h-i gamma','retarded_conversion':'T[g]=(I+i K_h gamma)^(-1) K_h, K_h=T[h]',
                    'scalar_hermitian_part':'Herm(T)=k_h/(1+(gamma k_h)^2)'},
        rows=rows,empirical_alloy_gap_inputs=[],
        limits=['Finite-eta T[Herm(g)] is not an established principal-value eta-to-zero limit',
                'No physical impurity vertex or inversion composition is inferred',
                'K_h is a support-space reactance, distinct from the host-edge P-irreducible K_P',
                'The CdTe real mid-gap row is an off-continuum control',
                'Continuum prescriptions must be tied to the requested physical observable'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh',type=int,nargs='+',default=[14,22,30])
    parser.add_argument('--eta',type=float,nargs='+',default=[.01,.02,.05])
    parser.add_argument('--output',type=Path,default=Path('data/calculated/sp3d5_continuum_prescription.json'))
    run(parser.parse_args())
