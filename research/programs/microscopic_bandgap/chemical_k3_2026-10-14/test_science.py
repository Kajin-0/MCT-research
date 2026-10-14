"""Five focused native-data and independent functional checks; no job launch."""
from pathlib import Path
import hashlib
import json
import math
import re
import unittest
from xml.etree import ElementTree as ET
import numpy as np
from scipy.special import expit
import analyze_k3 as a
from preflight import prove_mesh

HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(Path(p).read_text())


class Science(unittest.TestCase):
    def test_actual_complex_physical_embedding_and_negative_cases(self):
        c,g,k,_,_,_=a.old.intake('host');prior=read(a.previous.OLD/'numerical_result.json')
        source=a.old.PAIR/'host/out/r07pbe.save/wfc1.hdf5'
        wave=a.PAIR/'host/out/r07pbe.save/wfc1.hdf5'
        target,gt,kt=a.read_spinors(wave);Bs=a.Bmatrix(source);Bt=a.Bmatrix(wave)
        kept=np.load(HERE/'k3_complex_overlaps.npz')
        for label in ['Gamma6','Gamma8']:
            frame=c[np.array(prior['host_sector_selection'][label]['native_host_bands_1based'])-1]
            embedded,index,p=a.embed_same_cell(frame,g,k,Bs,gt,kt,Bt)
            self.assertEqual((p['source_PW'],p['target_PW']),(7809,10827))
            np.testing.assert_array_equal(embedded[:,:,index],frame)
            reverse=np.arange(len(g))[::-1]
            reordered,_,_=a.embed_same_cell(frame[:,:,reverse],g[reverse],k,Bs,gt,kt,Bt)
            np.testing.assert_array_equal(reordered,embedded)
            direct=np.array([[np.vdot(f,psi[:,index]) for psi in target] for f in frame])
            np.testing.assert_allclose(direct,kept['host_'+label],rtol=0,atol=2e-14)
            with self.assertRaisesRegex(ValueError,'omits source'):
                a.embed_same_cell(frame,g,k,Bs,np.delete(gt,int(index[0]),axis=0),kt,Bt)
            with self.assertRaisesRegex(ValueError,'reciprocal cell'):
                a.embed_same_cell(frame,g,k,Bs,gt,kt,Bt*1.01)

    def test_native_mesh_symmetry_charge_and_identical_cutoff_inputs(self):
        proof=prove_mesh();self.assertEqual(proof['without_TR_star_sizes'],[1,4,4,6,12])
        expected_rot={tuple(op['spatial'].astype(int).ravel()) for op in a.old.td_operations()}
        for member in ['host','cd']:
            root=a.PAIR/member;t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml');b=t.find('.//output/band_structure');ks=b.findall('ks_energies')
            weights=np.array([float(v.find('k_point').attrib['weight']) for v in ks])
            np.testing.assert_allclose(weights,np.array([1,6,12,8])/27,rtol=0,atol=1e-12)
            self.assertEqual(int(t.findtext('.//output/symmetries/nsym')),24)
            actual=set()
            crystal=[v for v in t.findall('.//output/symmetries/symmetry') if v.findtext('info')=='crystal_symmetry']
            self.assertEqual(len(crystal),24)
            for s in crystal:
                rot=np.fromstring(s.findtext('rotation'),sep=' ').reshape(3,3)
                actual.add(tuple(rot.astype(int).ravel()))
                np.testing.assert_array_equal(np.fromstring(s.findtext('fractional_translation'),sep=' '),np.zeros(3))
            self.assertEqual(actual,expected_rot)
            e=np.array([np.fromstring(v.findtext('eigenvalues'),sep=' ') for v in ks]);occ=np.array([np.fromstring(v.findtext('occupations'),sep=' ') for v in ks]);ef=float(b.findtext('fermi_energy'))
            fd=expit((ef-e)/.0005);self.assertEqual(e.shape,(4,176))
            self.assertLess(abs(np.sum(weights[:,None]*fd)-144),1e-8)
            np.testing.assert_allclose(fd,occ,rtol=0,atol=1e-9)
            self.assertEqual(t.findtext('.//output/convergence_info/scf_conv/convergence_achieved'),'true')
            self.assertLessEqual(float(t.findtext('.//output/convergence_info/scf_conv/scf_error'))*2,1e-9)
            old=a.previous.DFT/'.local/qe75_lowram_20261011/chemical_pbe8_k2_e50_20261014'/member/'pw.in'
            normalize=lambda s:re.sub(r"(?:outdir|pseudo_dir)='[^']+'",'private_path',s)
            self.assertEqual(normalize((root/'pw.in').read_text()),normalize(old.read_text().replace('2 2 2 0 0 0','3 3 3 0 0 0')))

    def test_independent_scalar_functionals_and_summed_bounds(self):
        result=read(HERE/'grid_result.json');baseline=read(a.CUT/'cutoff_result.json');ov=np.load(HERE/'k3_complex_overlaps.npz')
        for row in result['rows']:
            means={}
            for member in ['host','cd']:
                values=[]
                for label,d in [('Gamma6',2),('Gamma8',4)]:
                    v=np.loadtxt(HERE/(member+'_'+label+'_k3_spectrum.csv'),delimiter=',',skiprows=1)
                    z=ov[member+'_'+label];p=np.sum(z.real*z.real+z.imag*z.imag,axis=0)/d
                    np.testing.assert_allclose(p,v[:,2],rtol=0,atol=2e-16)
                    x=v[:,1]-row['k3']['reference_offsets_from_own_Fermi_eV'][member]
                    phi=np.exp(-x*x/(2*row['W_eV']**2));mass=math.fsum(float(i*j) for i,j in zip(p,phi));moment=math.fsum(float(i*j*k) for i,j,k in zip(p,phi,x))
                    self.assertGreater(mass,.05);values.append(moment/mass)
                    self.assertGreater(row['k3']['members'][member]['branches'][label]['joint_denominator'],0)
                means[member]=values[0]-values[1]
            self.assertAlmostEqual(means['cd']-means['host'],row['k3']['delta_eV'],places=13)
            old=next(v for v in baseline['rows'] if v['W_eV']==row['W_eV'] and v['reference_kind']==row['reference_kind'])
            self.assertEqual(old['cutoff50']['delta_eV'],row['k2']['delta_eV'])
            change=row['k3']['delta_eV']-row['k2']['delta_eV'];radius=row['k3']['conditional_bound_eV']+row['k2']['conditional_bound_eV']
            np.testing.assert_allclose(row['conditional_grid_difference_interval_eV'],[change-radius,change+radius],rtol=0,atol=1e-15)

    def test_host_projectors_and_group_intertwining_are_preserved(self):
        j=read(HERE/'grid_result.json');_,gs,_,_,_,_=a.old.intake('host');_,gt,_=a.read_spinors(a.PAIR/'host/out/r07pbe.save/wfc1.hdf5')
        ls={tuple(v):i for i,v in enumerate(gs)};lt={tuple(v):i for i,v in enumerate(gt)};mapping=np.array([lt[tuple(v)] for v in gs])
        for op in a.old.td_operations():
            spatial=op['spatial'].T
            np.testing.assert_array_equal([lt[tuple(v)] for v in gs@spatial],mapping[[ls[tuple(v)] for v in gs@spatial]])
        for label,expected in [('Gamma6',[1,0,0]),('Gamma8',[0,0,1])]:
            c=j['host_frame_checks'][label]
            self.assertFalse(c['primary_original_frame_replaced'])
            self.assertEqual(c['Td_check']['rounded_Gamma6_Gamma7_Gamma8_multiplicities'],expected)
            self.assertTrue(c['Td_check']['nearest_integer_classification_admitted_under_model'])
            self.assertGreater(min(c['primitive_Gamma_probabilities']),1-1e-8)
            sv=c['native50K2_to_native50K3_host_overlap_singular_values']
            self.assertAlmostEqual(np.sqrt(1-min(sv)**2),c['native50K2_to_native50K3_host_projector_distance'],places=13)

    def test_frozen_sources_owners_resources_and_old_uncertainty(self):
        j=read(HERE/'grid_result.json');frozen=read(HERE/'frozen_protocol.json')
        for name,h in {**j['source_sha256'],**frozen['profile']['pins']}.items():self.assertEqual(hashlib.sha256(Path(name).read_bytes()).hexdigest(),h)
        for member in ['host','cd']:
            f=read(a.PAIR/member/'FINAL.json');t=read(a.PAIR/member/'TERMINAL.json');g=f['guard']
            self.assertTrue(f['accepted']);self.assertTrue(t['terminal'])
            self.assertEqual(t['manager']['InvocationID'],g['invocation']);self.assertEqual(t['manager']['ExecMainStatus'],'0')
            self.assertTrue(all(g['rank_kernel_exits'].values()));self.assertLess(g['elapsed_s'],600)
            self.assertLess(g['peak_sampled_RSS_B'],12*2**30);self.assertGreaterEqual(g['min_host_available_B'],4*2**30);self.assertGreaterEqual(g['min_free_disk_B'],10*2**30)
        original=read(a.previous.OLD/'host_native_result.json');self.assertFalse(original['accepted']);self.assertIsNone(original['terminal_pass'])


if __name__=='__main__':unittest.main()
