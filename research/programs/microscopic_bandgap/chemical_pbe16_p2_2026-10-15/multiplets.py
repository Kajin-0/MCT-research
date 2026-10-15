"""Separate actual ordered-cell Td multiplets from smoothed spectral observables."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json
import numpy as np
from science_units_v2 import cell,td_check,read_spinors,self_time_reversal_overlap,EV_HA
import cd_owner as r

HERE=Path(__file__).resolve().parent


def main():
    overlaps=np.load(HERE/'complex_overlaps.npz');out={}
    for member,root in [('host',r.HOST),('cd',r.PAIR/'cd')]:
        t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml')
        c,g,k=read_spinors(root/'out/r07pbe.save/wfc1.hdf5')
        e=np.fromstring(t.findtext('.//output/band_structure/ks_energies/eigenvalues'),sep=' ')*EV_HA
        ef=float(t.findtext('.//output/band_structure/fermi_energy'))*EV_HA
        out[member]={}
        for label,d,expected in [('Gamma6',2,[1,0,0]),('Gamma8',4,[0,0,1])]:
            weights=np.sum(abs(overlaps[member+'_'+label])**2,axis=0)/d
            indices=np.sort(np.argsort(weights)[-d:]);other=np.setdiff1d(np.arange(352),indices)
            gap=float(min(weights[indices])-max(weights[other]))
            assert gap>.1, 'ambiguous frame-dominant branch, no forced assignment'
            f=c[indices];sym=td_check(f,g,cell(t));sv,_=self_time_reversal_overlap(f,g,k)
            spread=float(np.ptp(e[indices]))
            assert sym['nearest_integer_classification_admitted_under_model'] and sym['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==expected
            assert spread<1e-5 and min(sv)>1-1e-8
            out[member][label]=dict(bands_1based=(indices+1).tolist(),energies_minus_own_Fermi_eV=(e[indices]-ef).tolist(),multiplet_spread_eV=spread,Td=sym,Theta_overlap_singular_values=sv.tolist(),primitive_Gamma_probabilities=np.sum(abs(f[:,:,np.all(g%2==0,axis=1)])**2,axis=(1,2)).tolist(),fixed_frame_weight_in_multiplet=float(sum(weights[indices])),other_retained_weight=float(sum(weights[other])),minimum_state_weight_dominance_margin=gap,mean_minus_own_Fermi_eV=float(np.mean(e[indices]-ef)),mean_taken_only_AFTER_symmetry_and_degeneracy_pass=True)
        out[member]['tracked_multiplet_ordering_eV']=out[member]['Gamma6']['mean_minus_own_Fermi_eV']-out[member]['Gamma8']['mean_minus_own_Fermi_eV']
    delta=out['cd']['tracked_multiplet_ordering_eV']-out['host']['tracked_multiplet_ordering_eV']
    r0=json.loads((HERE/'numerical_result.json').read_text())
    inverse=next(v for v in r0['scalar_causal_rows'] if v['eta_eV']==.05)['delta_eV']
    result=dict(status='CALCULATED independently Td/Theta-qualified frame-dominant ORDERED-CELL PBE multiplets',members=out,delta_tracked_multiplet_ordering_eV=delta,Gaussian_W2_delta_eV=r0['primary_W2_eV'],inverse_eta005_delta_eV=inverse,Gaussian_minus_tracked_eV=r0['primary_W2_eV']-delta,inverse_minus_tracked_eV=inverse-delta,not_a_disordered_quasiparticle_gap=True,not_a_material_error_bar=True,no_branch_tracking_claim_between_unsampled_configurations=True,physical_xc=None)
    (HERE/'multiplet_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['delta_tracked_multiplet_ordering_eV','Gaussian_W2_delta_eV','inverse_eta005_delta_eV','Gaussian_minus_tracked_eV','inverse_minus_tracked_eV']},indent=2))
    for member in out:
        print(member,out[member]['tracked_multiplet_ordering_eV'])
        for l in ['Gamma6','Gamma8']:print(l,out[member][l]['multiplet_spread_eV'],out[member][l]['fixed_frame_weight_in_multiplet'])


if __name__=='__main__':main()
