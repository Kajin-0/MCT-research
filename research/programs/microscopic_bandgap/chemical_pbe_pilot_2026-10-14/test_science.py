"""Focused independent mathematical/native-data checks; no QE launch."""
from pathlib import Path
import json
import hashlib
import unittest
import numpy as np
from scipy.special import expit
from xml.etree import ElementTree as ET

HERE=Path(__file__).resolve().parent
PAIR=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/chemical_pbe8_20261014_v2')


class Science(unittest.TestCase):
    def test_actual_charge_and_fixed_geometry(self):
        structures=[]
        for member in ['host','cd']:
            t=ET.parse(PAIR/member/'out/r07pbe.save/data-file-schema.xml')
            b=t.find('.//output/band_structure');e=np.fromstring(b.findtext('ks_energies/eigenvalues'),sep=' ')
            f=float(b.findtext('fermi_energy'));N=np.sum(expit((f-e)/.0005))
            self.assertLess(abs(N-144),1e-8)
            self.assertEqual(t.findtext('.//output/convergence_info/scf_conv/convergence_achieved'),'true')
            cell=t.find('.//output/atomic_structure/cell')
            pos=t.find('.//output/atomic_structure/atomic_positions')
            structures.append((ET.tostring(cell),[(v.attrib['name'],np.fromstring(v.text,sep=' ')) for v in pos]))
        self.assertEqual(structures[0][0],structures[1][0])
        self.assertEqual([a for a,_ in structures[0][1]].count('Cd'),0)
        self.assertEqual([a for a,_ in structures[1][1]].count('Cd'),1)
        for (_,a),(_,b) in zip(structures[0][1],structures[1][1]): np.testing.assert_array_equal(a,b)

    def test_actual_complex_weights_and_scalar_centroids(self):
        j=json.loads((HERE/'numerical_result.json').read_text());o=np.load(HERE/'complex_overlaps.npz')
        for m in ['host','cd']:
            cents=[]
            for lab,d in [('Gamma6',2),('Gamma8',4)]:
                v=np.loadtxt(HERE/(m+'_'+lab+'_spectrum.csv'),delimiter=',',skiprows=1)
                w=np.sum(o[m+'_'+lab].real**2+o[m+'_'+lab].imag**2,axis=0)/d
                np.testing.assert_allclose(w,v[:,2],rtol=0,atol=2e-16)
                # Scalar accumulation separate from vectorized production driver.
                phi=[float(np.exp(-float(t)**2/8)) for t in v[:,1]]
                M=sum(float(a)*b for a,b in zip(w,phi));N=sum(float(a)*float(t)*b for a,t,b in zip(w,v[:,1],phi));c=N/M
                self.assertGreater(M,.05)
                self.assertAlmostEqual(c,j['branches'][m][lab]['Gaussian_centroid_relative_Fermi_eV'],places=13)
                cents.append(c)
            self.assertAlmostEqual(cents[0]-cents[1],j['observables'][m]['Gaussian_projected_ordering_eV'],places=13)

    def test_actual_projector_labels_and_reference_loss(self):
        j=json.loads((HERE/'numerical_result.json').read_text())
        for lab,expected in [('Gamma6',[1,0,0]),('Gamma8',[0,0,1])]:
            s=j['host_sector_symmetry'][lab]
            self.assertTrue(s['nearest_integer_classification_admitted_under_model'])
            self.assertEqual(s['rounded_Gamma6_Gamma7_Gamma8_multiplicities'],expected)
            self.assertLess(j['host_sector_selection'][lab]['restricted_reference_max_missing_norm'],.0001)
        self.assertLess(max(j['actual_complex_invariance_checks'].values()),1e-12)

    def test_joint_bound_extremizers(self):
        # Independent scalar extremizers exercise the common-denominator bound,
        # including signed projector perturbation after positive tail addition.
        B=2/np.sqrt(np.e)
        for M,c,r,delta in [(.07,-1,.4,.01),(.8,-.6,.002,.0003),(1.,0,.001,.0004)]:
            den=M-delta;bound=(r+delta)*(B+abs(c))/den
            for a in [0,r]:
                for b in [-r*B,r*B]:
                    for dm in [-delta,delta]:
                        for dn in [-delta*B,delta*B]:
                            q=(M*c+b+dn)/(M+a+dm)
                            self.assertLessEqual(abs(q-c),bound+1e-14)

    def test_unbounded_full_moment_counterexample(self):
        # Fixed tiny missing norm does not bound the ordinary energy centroid.
        r=.001;E=np.array([1e3,1e6,1e9])
        unbounded=r*E
        self.assertGreater(unbounded[-1],1e5)
        filtered=r*E*np.exp(-E*E/8)
        self.assertTrue(np.all(abs(filtered)<=r*2/np.sqrt(np.e)))

    def test_native_hashes_and_old_failure_preservation(self):
        j=json.loads((HERE/'numerical_result.json').read_text())
        for m in ['host','cd']:
            for name,pin in j[m]['hashes'].items():
                self.assertEqual(hashlib.sha256(Path(name).read_bytes()).hexdigest(),pin)
        host=json.loads((HERE/'host_native_result.json').read_text())
        self.assertFalse(host['accepted']);self.assertIsNone(host['terminal_pass'])
        self.assertTrue(host['scientific_pass'])
        cd=json.loads((HERE/'cd_native_result.json').read_text())
        self.assertTrue(cd['accepted']);self.assertTrue(cd['terminal_pass'])
        frozen=json.loads((HERE/'host_frozen_protocol.json').read_text())
        source=HERE/'run_pilot.host_scope.py'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),frozen['profile']['pins'][str(HERE/'run_pilot.py')])


if __name__=='__main__': unittest.main()
