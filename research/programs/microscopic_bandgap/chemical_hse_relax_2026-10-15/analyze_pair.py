"""Read-only before/after chemical projected operator from two accepted native updates."""
import json
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent
RY_EV=13.605693122994

def measures(h):
    return dict(Gamma6_Ry=float(np.trace(h[:2,:2]).real/2),Gamma8_Ry=float(np.trace(h[2:,2:]).real/4),
                ordering_eV=float((np.trace(h[:2,:2]).real/2-np.trace(h[2:,2:]).real/4)*RY_EV),
                antihermitian_opnorm_Ry=float(np.linalg.norm(h-h.conj().T,2)),
                intersector_opnorm_Ry=float(np.linalg.norm(h[:2,2:],2)))

def main():
    members={};matrices={}
    for m in ['host','cd']:
        _,_,root=r.load(m);f=json.loads((root/'FINAL.json').read_text())
        assert f['accepted'] and f['science']['scientific_pass'] and not r.cgroup_path(f['guard']['cgroup']).exists()
        d1=np.load(HERE/(m+'_c1_matrices.npz'));d2=np.load(HERE/(m+'_c2_matrices.npz'))
        first=dict(exchange=d1['exchange'],local=d1['local'])
        updated=dict(exchange=d2['exchange'],local=d1['local']+d2['local_total']-d1['local_total'])
        for v in [first,updated]:v['total']=v['exchange']+v['local']
        relaxation={k:updated[k]-first[k] for k in first}
        matrices[m]=dict(first=first,updated=updated,relaxation=relaxation)
        members[m]=dict(science=f['science'],guard=f['guard'],operators={stage:{k:measures(v) for k,v in d.items()} for stage,d in matrices[m].items()})
    chemistry={stage:{k:matrices['cd'][stage][k]-matrices['host'][stage][k] for k in ['exchange','local','total']} for stage in ['first','updated','relaxation']}
    old=json.loads((HERE.parent/'chemical_hse_firstace_p2_2026-10-14/numerical_result.json').read_text())
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='bce98cc',
                observable='fixed original Gamma6/Gamma8 normalized operator traces; updated HSE operator relative to each member preliminary PBE operator',
                chemical={stage:{k:measures(v) for k,v in d.items()} for stage,d in chemistry.items()},members=members,
                earlier_frozen_activation_eV=old['chemical_operator_change']['total']['difference_eV'],
                new_first_activation_difference_from_earlier_eV=measures(chemistry['first']['total'])['ordering_eV']-old['chemical_operator_change']['total']['difference_eV'],
                HSE_converged=False,physical_xc=None,final_eigenvalues_solve_old_frozen_ACE_not_second_rebuilt_operator=True,
                uncertainty='one HSE inner relaxation only; unknown further outer relaxation, finite-cell, Gamma/q1, projector, cutoff and material errors; numerical residuals are not material error bars')
    np.savez(HERE/'chemical_operator_matrices.npz',**{stage+'_'+k:v for stage,d in chemistry.items() for k,v in d.items()})
    (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result['chemical'],indent=2))

if __name__=='__main__':main()
