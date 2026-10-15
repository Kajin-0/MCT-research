"""Measured full fixed-frame operator trajectory; never add it to PBE centroids."""
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
    members={};matrices={};flat={}
    for m in ['host','cd']:
        root=r.PAIR/m;f=json.loads((root/'FINAL.json').read_text())
        assert f['accepted'] and not r.cgroup_path(f['guard']['cgroup']).exists()
        first=np.load(HERE/(m+'_c1_matrices.npz'))
        members[m]=dict(science=f['science'],guard=f['guard'],operators={})
        matrices[m]={}
        for c in range(1,f['science']['last_cycle']+1):
            a=np.load(HERE/(m+'_c'+str(c)+'_matrices.npz'))
            op=dict(exchange=a['exchange'],local=first['local']+a['local_total']-first['local_total'])
            op['total']=op['exchange']+op['local'];matrices[m][c]=op
            members[m]['operators'][str(c)]={k:measures(v) for k,v in op.items()}
            for k,v in op.items():flat[m+'_c'+str(c)+'_'+k]=v
    chemical=[]
    for c in range(1,min(map(len,matrices.values()))+1):
        delta={k:matrices['cd'][c][k]-matrices['host'][c][k] for k in ['exchange','local','total']}
        chemical.append(dict(source_cycle=c,contributions={k:measures(v) for k,v in delta.items()},
                             step_from_previous_eV=None if c==1 else measures(delta['total'])['ordering_eV']-chemical[-1]['contributions']['total']['ordering_eV']))
        for k,v in delta.items():flat['chemical_c'+str(c)+'_'+k]=v
    # True final-final comparison remains defined if the native convergence counts differ.
    final={k:matrices['cd'][max(matrices['cd'])][k]-matrices['host'][max(matrices['host'])][k] for k in ['exchange','local','total']}
    old=json.loads((HERE.parent/'chemical_hse_relax_2026-10-15/numerical_result.json').read_text())
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='04d767c',
                observable='normalized fixed original Gamma6/Gamma8 trace of current direct HSE exchange plus local potential relative to each member preliminary PBE local potential',
                chemical_trajectory=chemical,final_chemical={k:measures(v) for k,v in final.items()},members=members,
                numerical_HSE_outer_converged=all(v['science']['outer_converged'] for v in members.values()),
                earlier_c2_eV=old['chemical']['updated']['total']['ordering_eV'],
                independent_fresh_c2_difference_eV=chemical[1]['contributions']['total']['ordering_eV']-old['chemical']['updated']['total']['ordering_eV'],
                final_eigenvalues_solve_previous_ACE=True,physical_xc=None,
                uncertainty='finite outer trajectory and numerical residuals are reported; no certified infinite-tail, finite-cell/BZ/functional/quasiparticle/material error')
    np.savez(HERE/'chemical_operator_matrices.npz',**flat)
    (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    with (HERE/'operator_trajectory.csv').open('w') as f:
        f.write('source_cycle,exchange_chemical_eV,local_chemical_eV,total_chemical_eV,step_eV\n')
        for row in chemical:
            f.write(','.join(map(str,[row['source_cycle'],*[row['contributions'][k]['ordering_eV'] for k in ['exchange','local','total']],row['step_from_previous_eV']]))+'\n')
    print(json.dumps(dict(chemical_trajectory=chemical,final_chemical=result['final_chemical'],numerical_HSE_outer_converged=result['numerical_HSE_outer_converged']),indent=2))

if __name__=='__main__':main()
