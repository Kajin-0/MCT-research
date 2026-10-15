"""Actual charge, scalar exchange and distributed old-ACE/new-source checks."""
import json,math,sys
from decimal import Decimal,getcontext
from pathlib import Path
import numpy as np
from packets import packet
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main(members=('host','cd')):
    getcontext().prec=60;results={}
    for m in members:
        root=r.PAIR/m;f=json.loads((root/'FINAL.json').read_text());assert f['accepted']
        phases={}
        for cycle in range(1,f['science']['last_cycle']+1):
            matrix=np.zeros((6,6),complex);terms=[];cross=np.zeros((176,176),complex)
            for rank in [0,1]:
                b=packet(root,'before',rank,cycle);a=packet(root,'after',rank,cycle)
                n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
                for i in range(6):
                    for j in range(6):matrix[i,j]+=np.vdot(a['probe'][ix,i],a['direct_probe'][ix,j])
                terms.extend(float(b['wg'][j])*np.vdot(b['phi'][ix,j],b['direct'][ix,j]).real for j in range(176))
                if cycle>1:
                    old=packet(root,'after',rank,cycle-1);prev=packet(root,'before',rank,cycle-1)
                    np.testing.assert_array_equal(b['G'],prev['G']);np.testing.assert_array_equal(b['B'],prev['B'])
                    cross+=old['xi'][ix].conj().T@b['phi'][ix]
            stored=np.load(HERE/(m+'_c'+str(cycle)+'_matrices.npz'))
            matrix_err=float(max(abs(matrix-stored['exchange']).ravel()));assert matrix_err<1e-12
            fock=math.fsum(terms);native=f['science']['source_cycles'][str(cycle)]['native_unhalved_Fock_Ry'];assert abs(fock-native)<1e-10
            charge=sum(Decimal(str(v)) for v in b['wg']);assert abs(charge-144)<=Decimal('1e-8')
            row=dict(independent_Fock_Ry=fock,Fock_difference_Ry=fock-native,reference_matrix_max_Ry=matrix_err,charge_from_actual_occupations_e=str(charge))
            if cycle>1:
                f1=-float(np.dot(b['wg'],np.sum(abs(cross)**2,axis=0)))
                native_f1=f['science']['residuals'][str(cycle)]['fock1_Ry'];assert abs(f1-native_f1)<1e-10
                raw=f1-.5*(phases[str(cycle-1)]['independent_Fock_Ry']+fock)
                assert abs(raw-f['science']['residuals'][str(cycle)]['raw_Ry'])<1e-10
                row.update(old_ACE_new_orbitals_contraction_Ry=f1,old_ACE_bridge_residual_Ry=f1-native_f1,reconstructed_signed_dexx_Ry=raw)
            phases[str(cycle)]=row
        results[m]=phases
    tag='' if len(members)==2 else members[0]+'_'
    (HERE/(tag+'independent_check_results.json')).write_text(json.dumps(dict(passed=True,checks=3,native_invocations=0,members=results),indent=2)+'\n')
    print(json.dumps(dict(passed=True,cycles={m:len(v) for m,v in results.items()},max_bridge_error_Ry=max(abs(v.get('old_ACE_bridge_residual_Ry',0)) for m in results.values() for v in m.values())),indent=2))

if __name__=='__main__':main(tuple(sys.argv[1:]) or ('host','cd'))
