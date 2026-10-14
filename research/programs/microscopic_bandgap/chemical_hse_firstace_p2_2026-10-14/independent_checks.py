"""Three read-only scientific checks on actual native records; never runs QE."""
import json,math
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from decimal import Decimal, getcontext
from packets import packet
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main():
    getcontext().prec=70;result={}
    for member in ['host','cd']:
        root=r.PAIR/member
        final=json.loads((root/'FINAL.json').read_text());assert final['accepted']
        t=ET.parse(root/'out/r07hse8.save/data-file-schema.xml')
        b=t.find('.//output/band_structure');ks=b.findall('ks_energies');assert len(ks)==1
        ef=2*Decimal(b.findtext('fermi_energy'))
        eps=[2*Decimal(v) for v in ks[0].findtext('eigenvalues').split()]
        sigma=Decimal('0.001')
        n=sum(Decimal(1)/(Decimal(1)+((e-ef)/sigma).exp()) for e in eps)
        assert abs(n-144)<=Decimal('1e-8')
        # Independent vdot per reference column instead of the intake's GEMM.
        exchange=np.zeros((6,6),complex);local=exchange.copy();energy_terms=[]
        for rank in [0,1]:
            before=packet(root,'before',rank);after=packet(root,'after',rank)
            low=packet(root,'local0',rank);high=packet(root,'local1',rank)
            npw=before['nnpw'];p=before['npwx'];active=np.r_[np.arange(npw),np.arange(p,p+npw)]
            for i in range(6):
                for j in range(6):
                    exchange[i,j]+=np.vdot(after['probe'][active,i],after['direct_probe'][active,j])
                    local[i,j]+=np.vdot(low['probe'][active,i],high['action'][active,j]-low['action'][active,j])
            energy_terms.extend(float(before['wg'][i])*np.vdot(before['phi'][active,i],before['direct'][active,i]).real for i in range(176))
        fock=math.fsum(energy_terms)
        stored=np.load(HERE/(member+'_matrices.npz'))
        residual=max(float(np.max(abs(exchange-stored['exchange']))),float(np.max(abs(local-stored['local']))))
        assert residual<1e-12 and abs(fock-final['science']['native_unhalved_Fock_Ry'])<1e-10
        h=exchange+local
        # Unitary rotations within each irrep leave the normalized trace invariant.
        U=np.zeros((6,6),complex)
        for start,d in [(0,2),(2,4)]:
            j=np.arange(d);U[start:start+d,start:start+d]=np.exp(2j*np.pi*j[:,None]*j[None,:]/d)/np.sqrt(d)
        hh=U.conj().T@h@U
        shift=lambda v:float((np.trace(v[:2,:2]).real/2-np.trace(v[2:,2:]).real/4))
        gauge_residual=abs(shift(h)-shift(hh));assert gauge_residual<1e-12
        result[member]=dict(high_precision_FD_charge_e=str(n),charge_residual_e=str(n-144),
                            independent_column_action_matrix_max_Ry=residual,
                            independent_Fock_contraction_Ry=fock,
                            Fock_disagreement_Ry=fock-final['science']['native_unhalved_Fock_Ry'],
                            block_unitary_trace_difference_Ry=gauge_residual)
    (HERE/'independent_check_results.json').write_text(json.dumps(dict(checks=3,passed=True,native_invocations=0,scope='actual-record FD neutrality; independent complex column contractions; irrep trace basis invariance',members=result),indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
