"""Read-only diagnosis of ORIGINAL strict refusal; never releases a splice."""
from pathlib import Path
import json
import numpy as np
from accepted import HERE,PRIVATE,OLD,decode,frames,global_indices,sha


def main():
    target=HERE/'strict_refusal.json'
    if target.exists():raise FileExistsError('retain original strict refusal')
    root=PRIVATE/'p2/host';stderr=(root/'launch_stderr.json').read_text();assert 'SAME-D BYTE REFUSAL: energies' in stderr
    fields=['dims','fft','B','k','scalars','bounds','energies','G','density_G','wg','source','rhoG','rhoR','vrs'];rows=[]
    for rank in [0,1]:
        a=decode(PRIVATE/'p1/host/pilot'/f'H.rank{rank}');b=decode(root/'pilot'/f'H.rank{rank}');out={}
        for key in fields:
            mask=a[key]!=b[key];out[key]=dict(bitwise=a[key].tobytes()==b[key].tobytes(),different_entries=int(sum(mask.ravel())),max_abs_delta=float(np.max(abs(a[key]-b[key]))))
            if key=='energies':out[key].update(old_ehart_etxc_vtxc_Ry=a[key].tolist(),new_ehart_etxc_vtxc_Ry=b[key].tolist(),delta_Ry=(b[key]-a[key]).tolist())
        control={k:dict(bitwise=a[k][:,152:].tobytes()==b[k][:,152:].tobytes(),max_abs_delta=float(np.max(abs(a[k][:,152:]-b[k][:,152:])))) for k in ['trial','kin','loc','nl','fock']}
        control['h_psi']=dict(bitwise=a['control'].tobytes()==b['control'].tobytes(),max_abs_delta=float(np.max(abs(a['control']-b['control']))))
        rows.append(dict(rank=rank,state_fields=out,original_physical_controls=control))
    guard=json.loads((root/'GUARD_RESULT.json').read_text());term=json.loads((root/'TERMINAL.json').read_text());assert guard['pass_guard'] and term['terminal']
    result=dict(status='REFUSED original strict same-D energy-byte gate; NO304SPLICE/FD result',original_error='SAME-D BYTE REFUSAL: energies',ranks=rows,native_execution_terminal_and_owner_PASS=True,strict_append_science_PASS=False,no_native_retry=True,no_splice_performed=True,no_HSE_or_xc_claim=True,resources=guard,raw={str(p):sha(p) for p in [root/'launch_stderr.json',root/'GUARD_RESULT.json',root/'TERMINAL.json',*list((root/'pilot').iterdir()),HERE/'frozen_protocol.json',HERE/'readback.py',Path(__file__)]})
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='raw'},indent=2))


if __name__=='__main__':main()
