"""Independent read-only native cycle contractions and old-ACE lifetime bridge."""
import json,math
from decimal import Decimal,getcontext
from pathlib import Path
import numpy as np
from packets import packet
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main(members=('host','cd')):
    getcontext().prec=60;results={}
    for m in members:
        _,_,root=r.load(m);final=json.loads((root/'FINAL.json').read_text());assert final['accepted']
        phases={};cross=np.zeros((176,176),complex)
        for cycle in [1,2]:
            matrix=np.zeros((6,6),complex);terms=[];gram=np.zeros((176,176),complex)
            for rank in [0,1]:
                before=packet(root,'before',rank,cycle);after=packet(root,'after',rank,cycle)
                n,p=before['nnpw'],before['npwx'];active=np.r_[np.arange(n),np.arange(p,p+n)]
                for i in range(6):
                    for j in range(6):matrix[i,j]+=np.vdot(after['probe'][active,i],after['direct_probe'][active,j])
                terms.extend(float(before['wg'][j])*np.vdot(before['phi'][active,j],before['direct'][active,j]).real for j in range(176))
                gram+=before['phi'][active].conj().T@before['phi'][active]
                if cycle==2:
                    old=packet(root,'after',rank,1)
                    before1=packet(root,'before',rank,1)
                    np.testing.assert_array_equal(before1['G'],before['G'])
                    np.testing.assert_array_equal(before1['B'],before['B'])
                    assert old['npwx']==p and old['nnpw']==n
                    cross+=old['xi'][active].conj().T@before['phi'][active]
            stored=np.load(HERE/(m+'_c'+str(cycle)+'_matrices.npz'))
            matrix_err=float(np.max(abs(matrix-stored['exchange'])));assert matrix_err<1e-12
            fock=math.fsum(terms);native=final['science']['source_cycles'][str(cycle)]['native_unhalved_Fock_Ry'];assert abs(fock-native)<1e-10
            # Recorded actual occupations, independently summed at high precision.
            charge=sum(Decimal(str(v)) for v in before['wg']);assert abs(charge-144)<=Decimal('1e-8')
            phases[str(cycle)]=dict(independent_Fock_Ry=fock,Fock_difference_Ry=fock-native,reference_matrix_max_Ry=matrix_err,charge_from_actual_occupations_e=str(charge),source_Gram_opnorm=float(np.linalg.norm(gram-np.eye(176),2)))
        f1=-float(np.dot(before['wg'],np.sum(abs(cross)**2,axis=0)))
        native_f1=final['science']['Fock_old_new_Ry'];assert abs(f1-native_f1)<1e-10
        raw=f1-.5*(phases['1']['independent_Fock_Ry']+phases['2']['independent_Fock_Ry'])
        assert abs(raw-final['science']['raw_dexx_Ry'])<1e-10
        results[m]=dict(cycles=phases,old_ACE_new_orbitals_contraction_Ry=f1,old_ACE_bridge_residual_Ry=f1-native_f1,reconstructed_signed_dexx_Ry=raw)
    (HERE/('independent_check_results.json' if len(members)==2 else members[0]+'_independent_check_results.json')).write_text(json.dumps(dict(passed=True,checks=3,native_invocations=0,scope='actual source charge; per-column direct reference/Fock contractions; distributed old-xi/new-Phi ACE bridge and dexx',members=results),indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    import sys
    main(tuple(sys.argv[1:]) or ('host','cd'))
