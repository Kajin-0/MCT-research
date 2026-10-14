"""Focused native-data/functional checks. Never launches QE."""
from pathlib import Path
import unittest
import json
import hashlib
import numpy as np
from scipy.special import expit
from xml.etree import ElementTree as ET
import width_curve as w

HERE=Path(__file__).resolve().parent
PAIR=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/chemical_pbe8_k2_20261014')


class Science(unittest.TestCase):
    def test_retained_complex_width_reconstruction(self):
        D,env,rho,pins=w.old_data();j=json.loads((HERE/'width_result.json').read_text())
        for row in j['rows']:
            actual=w.response(D,row['W_eV'],row['reference_offsets_from_own_Fermi_eV'],env,rho)
            self.assertAlmostEqual(actual['delta_eV'],row['delta_eV'],places=14)
            self.assertAlmostEqual(actual['conditional_bound_eV'],row['conditional_bound_eV'],places=14)
            self.assertGreater(row['conditional_interval_eV'][0],0)
        for name,pin in pins.items():self.assertEqual(hashlib.sha256(Path(name).read_bytes()).hexdigest(),pin)

    def test_actual_weighted_charge_and_mesh(self):
        for member in ['host','cd']:
            b=ET.parse(PAIR/member/'out/r07pbe.save/data-file-schema.xml').find('.//output/band_structure')
            ks=b.findall('ks_energies');weights=np.array([float(v.find('k_point').attrib['weight']) for v in ks]);self.assertEqual(len(ks),4)
            np.testing.assert_allclose(sorted(weights),[.125,.125,.375,.375],rtol=0,atol=1e-12)
            e=np.array([np.fromstring(v.findtext('eigenvalues'),sep=' ') for v in ks]);ef=float(b.findtext('fermi_energy'));f=expit((ef-e)/.0005)
            self.assertLess(abs(np.sum(weights[:,None]*f)-144),1e-8)
            self.assertEqual(e.shape,(4,176))
            v=np.array([np.fromstring(k.findtext('k_point'),sep=' ') for k in ks]);self.assertEqual(np.count_nonzero(np.linalg.norm(v,axis=1)<1e-12),1)

    def test_actual_new_complex_scalar_centroids(self):
        j=json.loads((HERE/'grid_result.json').read_text());ov=np.load(HERE/'k2_complex_overlaps.npz')
        for row in j['rows']:
            means={}
            for member in ['host','cd']:
                vals=[];offset=row['new']['reference_offsets_from_own_Fermi_eV'][member]
                for label,d in [('Gamma6',2),('Gamma8',4)]:
                    v=np.loadtxt(HERE/(member+'_'+label+'_k2_spectrum.csv'),delimiter=',',skiprows=1)
                    prob=np.sum(ov[member+'_'+label].real**2+ov[member+'_'+label].imag**2,axis=0)/d
                    np.testing.assert_allclose(prob,v[:,2],rtol=0,atol=2e-16)
                    t=v[:,1]-offset;phi=np.exp(-t*t/(2*row['W_eV']**2));M=sum(float(x*y) for x,y in zip(prob,phi));N=sum(float(x*y*z) for x,y,z in zip(prob,phi,t))
                    self.assertGreater(M,.05);vals.append(N/M)
                means[member]=vals[0]-vals[1]
            self.assertAlmostEqual(means['cd']-means['host'],row['new']['delta_eV'],places=13)

    def test_actual_host_physical_frame_and_no_replacement(self):
        j=json.loads((HERE/'grid_result.json').read_text())
        for label,expected in [('Gamma6',[1,0,0]),('Gamma8',[0,0,1])]:
            c=j['newhost_physical_frame_checks'][label];s=c['physical_Td_check']
            self.assertTrue(s['nearest_integer_classification_admitted_under_model'])
            self.assertEqual(s['rounded_Gamma6_Gamma7_Gamma8_multiplicities'],expected)
            self.assertFalse(c['original_frame_replaced_in_primary_observable'])
            sv=c['original_to_newhost_frame_principal_overlap_singular_values']
            self.assertAlmostEqual(np.sqrt(1-min(sv)**2),c['projector_distance_comparison'],places=13)

    def test_proven_joint_bound_extremizers(self):
        for W in [1.,2.,3.]:
            B=W/np.sqrt(np.e);M=.3;c=-.8;r=.01;eps=.002;rho=1e-7;d=2*eps+rho
            bound=(r+d)*(B+abs(c))/(M-d)
            for a in [0,r]:
                for b in [-r*B,r*B]:
                    for dm in [-d,d]:
                        for dn in [-d*B,d*B]:self.assertLessEqual(abs((M*c+b+dn)/(M+a+dm)-c),bound+1e-14)

    def test_owners_pins_and_original_uncertainty(self):
        for member in ['host','cd']:
            f=json.loads((PAIR/member/'FINAL.json').read_text());t=json.loads((PAIR/member/'TERMINAL.json').read_text())
            self.assertTrue(f['accepted']);self.assertTrue(t['terminal'])
            self.assertEqual(t['manager']['InvocationID'],f['guard']['invocation'])
            self.assertEqual(t['manager']['ExecMainStatus'],'0')
            for name,pin in f['source_hashes'].items():self.assertEqual(hashlib.sha256(Path(name).read_bytes()).hexdigest(),pin)
        old=json.loads((w.OLD/'host_native_result.json').read_text());self.assertFalse(old['accepted']);self.assertIsNone(old['terminal_pass'])


if __name__=='__main__':unittest.main()
