"""Read-only first-activation operator comparison; requires two accepted pilots."""
import json
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent
RY_EV=13.605693122994

def sectors(h):
    h=np.asarray(h)
    return dict(Gamma6_Ry=float(np.trace(h[:2,:2]).real/2),
                Gamma8_Ry=float(np.trace(h[2:,2:]).real/4),
                difference_eV=float((np.trace(h[:2,:2]).real/2-np.trace(h[2:,2:]).real/4)*RY_EV),
                antihermitian_opnorm_Ry=float(np.linalg.norm(h-h.conj().T,2)),
                Gamma6_spread_Ry=float(np.ptp(np.linalg.eigvalsh((h[:2,:2]+h[:2,:2].conj().T)/2))),
                Gamma8_spread_Ry=float(np.ptp(np.linalg.eigvalsh((h[2:,2:]+h[2:,2:].conj().T)/2))),
                intersector_opnorm_Ry=float(np.linalg.norm(h[:2,2:],2)))

def main():
    results={}; matrices={}
    for member in ['host','cd']:
        profile,job,root=r.load(member)
        result=json.loads((root/'FINAL.json').read_text())
        assert result['accepted'] and result['terminal_pass'] and result['science']['scientific_pass']
        assert not r.cgroup_path(result['guard']['cgroup']).exists()
        for path,pin in result['source_hashes'].items(): assert r.sha(path)==pin
        data=np.load(HERE/(member+'_matrices.npz'))
        matrices[member]={k:data[k].copy() for k in ['exchange','local']}
        matrices[member]['total']=matrices[member]['exchange']+matrices[member]['local']
        results[member]=dict(operators={k:sectors(v) for k,v in matrices[member].items()},
                            science=result['science'],guard=result['guard'],HSE_converged=False)
    delta={k:matrices['cd'][k]-matrices['host'][k] for k in ['exchange','local','total']}
    out=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='c50f466',
             scope='FIRST-ACE HSE activation on separately converged Gamma-only semilocal densities; periodic x=.25',
             quantity='difference of fixed physical Gamma6/Gamma8 normalized traces of delta-H activation, Cd minus host',
             members=results,chemical_operator_change={k:sectors(v) for k,v in delta.items()},
             Rydberg_eV=RY_EV,projector='same retained original 40Ry six-vector frame embedded exactly into 50Ry G-space',
             source_HSE_quasiparticle_spectrum=False,converged_HSE_gap=False,physical_xc=None,
             not_additive_correction_to_PBE_k3_Gaussian_response=True,
             uncertainty='reported numerical consistency residuals do not bound material, functional, k/q, cutoff, finite-cell or eigenpair errors')
    np.savez(HERE/'chemical_operator_matrices.npz',**{k:v for k,v in delta.items()})
    (HERE/'numerical_result.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(out['chemical_operator_change'],indent=2))

if __name__=='__main__':main()
