"""Actual stored density/source-occupation changes; no material error inference."""
import json
from pathlib import Path
import numpy as np
from packets import packet
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main():
    out={}
    for m in ['host','cd']:
        root=r.PAIR/m;assert json.loads((root/'FINAL.json').read_text())['accepted']
        change=0.;norm=0.;real_change=0.;real_norm=0.;seen=set();occupation=0.
        for rank in [0,1]:
            a=packet(root,'local1',rank,1);b=packet(root,'local1',rank,2)
            np.testing.assert_array_equal(a['density_G'],b['density_G'])
            labels=set(map(tuple,a['density_G']));assert len(labels)==len(a['density_G']) and not labels.intersection(seen);seen.update(labels)
            change+=float(np.linalg.norm(b['rhoG'][:,0]-a['rhoG'][:,0])**2);norm+=float(np.linalg.norm(a['rhoG'][:,0])**2)
            real_change+=float(np.linalg.norm(b['rhoR'][:,0]-a['rhoR'][:,0])**2);real_norm+=float(np.linalg.norm(a['rhoR'][:,0])**2)
            old=packet(root,'before',rank,1);new=packet(root,'before',rank,2)
            occupation=max(occupation,float(np.max(abs(new['wg']-old['wg']))))
        out[m]=dict(relative_charge_density_G_coefficient_norm=float(np.sqrt(change/norm)),relative_stored_charge_density_R_array_norm=float(np.sqrt(real_change/real_norm)),unique_density_G_labels=len(seen),max_source_occupation_change=occupation,interpretation='native stored-array/coefficient relative changes, not gap error bounds or a physical linewidth')
    (HERE/'density_change.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
