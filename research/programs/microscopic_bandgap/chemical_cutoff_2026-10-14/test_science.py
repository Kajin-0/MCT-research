"""Focused actual-spectrum and physical-basis checks; never launches QE."""
from pathlib import Path
import hashlib
import json
import math
import re
import unittest
from xml.etree import ElementTree as ET
import numpy as np
from scipy.special import expit
import analyze_cutoff as a
from embedding import embed_same_cell

HERE=Path(__file__).resolve().parent
PAIR=a.PAIR
read=lambda p:json.loads(Path(p).read_text())


class Science(unittest.TestCase):
    def test_actual_physical_isometry_and_refusals(self):
        c,g,k,_,_,_=a.old.intake('host')
        prior=read(a.previous.OLD/'numerical_result.json')
        frame=c[np.array(prior['host_sector_selection']['Gamma6']['native_host_bands_1based'])-1]
        source=a.old.PAIR/'host/out/r07pbe.save/wfc1.hdf5'
        wave=PAIR/'host/out/r07pbe.save/wfc1.hdf5'
        target,gt,kt=a.read_spinors(wave);Bs=a.Bmatrix(source);Bt=a.Bmatrix(wave)
        embedded,index,p=embed_same_cell(frame,g,k,Bs,gt,kt,Bt)
        self.assertEqual((p['source_PW'],p['target_PW'],p['new_only_PW']),(7809,10827,3018))
        np.testing.assert_array_equal(embedded[:,:,index],frame)
        self.assertEqual(p['source_norm_discarded'],0)
        self.assertFalse(p['renormalization_used'])
        permutation=np.arange(len(g))[::-1]
        reordered,_,_=embed_same_cell(frame[:,:,permutation],g[permutation],k,Bs,gt,kt,Bt)
        np.testing.assert_array_equal(reordered,embedded)
        with self.assertRaisesRegex(ValueError,'omits source'):
            embed_same_cell(frame,g,k,Bs,np.delete(gt,int(index[0]),axis=0),kt,Bt)
        with self.assertRaisesRegex(ValueError,'reciprocal cell'):
            embed_same_cell(frame,g,k,Bs,gt,kt,Bt*1.01)
        # Independent contraction from the native target at mapped physical G.
        scalar=np.array([[np.vdot(f,target[b][:,index]) for b in range(176)] for f in frame])
        retained=np.load(HERE/'e50_complex_overlaps.npz')['host_Gamma6']
        np.testing.assert_allclose(scalar,retained,rtol=0,atol=2e-14)

    def test_all24_actual_label_intertwining_and_host_irreps(self):
        _,gs,_,_,_,_=a.old.intake('host')
        _,gt,_=a.read_spinors(PAIR/'host/out/r07pbe.save/wfc1.hdf5')
        ls={tuple(v):i for i,v in enumerate(gs)};lt={tuple(v):i for i,v in enumerate(gt)}
        mapping=np.array([lt[tuple(v)] for v in gs])
        for op in a.old.td_operations():
            r=op['spatial'].T
            np.testing.assert_array_equal([lt[tuple(v)] for v in gs@r],mapping[[ls[tuple(v)] for v in gs@r]])
        result=read(HERE/'cutoff_result.json')
        for label,expected in [('Gamma6',[1,0,0]),('Gamma8',[0,0,1])]:
            v=result['host_frame_checks'][label]
            self.assertFalse(v['primary_original_frame_replaced'])
            self.assertEqual(v['Td_check']['rounded_Gamma6_Gamma7_Gamma8_multiplicities'],expected)
            self.assertTrue(v['Td_check']['nearest_integer_classification_admitted_under_model'])
            self.assertGreater(min(v['primitive_Gamma_probabilities']),1-1e-8)
            self.assertLess(max(v['native50_highG_probability_outside40_by_state']),1e-4)
            self.assertAlmostEqual(np.sqrt(1-min(v['original40_to_native50_overlap_singular_values'])**2),v['principal_projector_distance'],places=13)

    def test_allk_native_charge_convergence_and_same_settings(self):
        for member in ['host','cd']:
            root=PAIR/member;t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml')
            b=t.find('.//output/band_structure');ks=b.findall('ks_energies')
            weights=np.array([float(v.find('k_point').attrib['weight']) for v in ks])
            e=np.array([np.fromstring(v.findtext('eigenvalues'),sep=' ') for v in ks])
            occ=np.array([np.fromstring(v.findtext('occupations'),sep=' ') for v in ks])
            ef=float(b.findtext('fermi_energy'));fd=expit((ef-e)/.0005)
            self.assertEqual(e.shape,(4,176));np.testing.assert_allclose(weights,[.125,.375,.375,.125],rtol=0,atol=1e-12)
            self.assertLess(abs(np.sum(weights[:,None]*fd)-144),1e-8)
            np.testing.assert_allclose(fd,occ,rtol=0,atol=1e-9)
            self.assertEqual(t.findtext('.//output/convergence_info/scf_conv/convergence_achieved'),'true')
            self.assertEqual(int(t.findtext('.//output/convergence_info/scf_conv/n_scf_steps')),11)
            self.assertLess(float(t.findtext('.//output/convergence_info/scf_conv/scf_error'))*2,1e-9)
            old=(a.previous.DFT/'.local/qe75_lowram_20261011/chemical_pbe8_k2_20261014'/member/'pw.in').read_text()
            new=(root/'pw.in').read_text()
            # Only private paths and the preregistered cutoff pair differ.
            normalize=lambda s:re.sub(r"(?:outdir|pseudo_dir)='[^']+'",'private_path',s)
            self.assertEqual(normalize(old),normalize(new.replace('ecutwfc=50, ecutrho=200','ecutwfc=40, ecutrho=160')))

    def test_scalar_complex_centroids_and_cutoff_difference(self):
        result=read(HERE/'cutoff_result.json');overlap=np.load(HERE/'e50_complex_overlaps.npz')
        baseline=read(a.PREV/'grid_result.json')
        for row in result['rows']:
            means={}
            for member in ['host','cd']:
                values=[]
                for label,d in [('Gamma6',2),('Gamma8',4)]:
                    v=np.loadtxt(HERE/(member+'_'+label+'_e50_spectrum.csv'),delimiter=',',skiprows=1)
                    z=overlap[member+'_'+label];p=np.sum(z.real*z.real+z.imag*z.imag,axis=0)/d
                    np.testing.assert_allclose(p,v[:,2],rtol=0,atol=2e-16)
                    t=v[:,1]-row['cutoff50']['reference_offsets_from_own_Fermi_eV'][member]
                    phi=np.exp(-t*t/(2*row['W_eV']**2))
                    M=math.fsum(float(x*y) for x,y in zip(p,phi))
                    N=math.fsum(float(x*y*z) for x,y,z in zip(p,phi,t))
                    self.assertGreater(M,.05);values.append(N/M)
                means[member]=values[0]-values[1]
            self.assertAlmostEqual(means['cd']-means['host'],row['cutoff50']['delta_eV'],places=13)
            before=next(v for v in baseline['rows'] if v['reference_kind']==row['reference_kind'] and v['W_eV']==row['W_eV'])
            self.assertEqual(before['new']['delta_eV'],row['baseline40']['delta_eV'])
            self.assertAlmostEqual(row['cutoff50']['delta_eV']-row['baseline40']['delta_eV'],row['cutoff_change_eV'],places=15)
            self.assertGreater(row['cutoff50']['conditional_interval_eV'][0],0)
            self.assertLess(row['conditional_difference_interval_eV'][0],0)
            self.assertGreater(row['conditional_difference_interval_eV'][1],0)

    def test_joint_bound_extremizers_and_reference_invariance(self):
        for W in [1.,2.,3.]:
            B=W/np.sqrt(np.e);M=.3;c=-.8;r=.01;eps=.002;rho=1e-7;d=2*eps+rho
            bound=(r+d)*(B+abs(c))/(M-d)
            for dm in [-d,d]:
                for dn in [-d*B,d*B]:
                    for mass in [0,r]:
                        for moment in [-r*B,r*B]:
                            self.assertLessEqual(abs((M*c+moment+dn)/(M+mass+dm)-c),bound+1e-14)
        result=read(HERE/'cutoff_result.json')
        for W in a.curves.WIDTHS:
            rows=[v for v in result['rows'] if v['W_eV']==W]
            self.assertAlmostEqual(rows[0]['cutoff50']['delta_eV'],rows[1]['cutoff50']['delta_eV'],places=11)
        # Shift BOTH energies and references; never recenter an unknown spectrum.
        data,_=a.base_data();eps={'Gamma6':0.,'Gamma8':0.}
        shifted={m:{l:dict(v,energy_relative_Fermi_eV=v['energy_relative_Fermi_eV']+2.7) for l,v in branches.items()} for m,branches in data.items()}
        first=a.curves.response(data,2,{m:0. for m in data},eps,0.)
        second=a.curves.response(shifted,2,{m:2.7 for m in data},eps,0.)
        self.assertAlmostEqual(first['delta_eV'],second['delta_eV'],places=14)

    def test_hse_source_conditioned_arithmetic_not_admission(self):
        j=read(HERE/'hse_feasibility.json')
        self.assertEqual(j['HSE_native_runs_this_phase'],0)
        ref=j['measured_reference'];self.assertFalse(ref['fully_converged'])
        self.assertAlmostEqual(ref['ACE_wall_s']/ref['outer_updates'],ref['mean_whole_outer_ACE_wall_s'],places=13)
        for v in j['options']:
            self.assertEqual(v['exxbuff_aggregate_bytes'],16*2*176*60**3*v['Nkqs'])
            self.assertFalse(v['full600s_admission']);self.assertTrue(v['additional_backend_and_EXX_scratch_not_bounded'])
        self.assertEqual(sorted(j['best_next_under_current600s']['nonmagnetic_Td_TR_star_sizes']),[1,6,8,12])
        self.assertEqual(sum(j['best_next_under_current600s']['nonmagnetic_Td_TR_star_sizes']),27)
        source=a.previous.DFT/'.local/qe75_lowram_20261011/exx.f90'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),j['pristine_exx_SHA'])

    def test_native_pins_caps_and_preserved_original_failure(self):
        result=read(HERE/'cutoff_result.json')
        for name,pin in result['source_sha256'].items():self.assertEqual(a.old.sha(name),pin)
        for member in ['host','cd']:
            f=read(PAIR/member/'FINAL.json');terminal=read(PAIR/member/'TERMINAL.json')
            self.assertTrue(f['accepted']);self.assertTrue(terminal['terminal'])
            self.assertEqual(terminal['manager']['ExecMainStatus'],'0')
            self.assertEqual(terminal['manager']['InvocationID'],f['guard']['invocation'])
            self.assertTrue(all(f['guard']['rank_kernel_exits'].values()))
            self.assertLess(f['guard']['peak_sampled_RSS_B'],12*2**30)
            self.assertLess(f['guard']['elapsed_s'],600)
            self.assertGreaterEqual(f['guard']['min_host_available_B'],4*2**30)
            self.assertGreaterEqual(f['guard']['min_free_disk_B'],10*2**30)
            for name,pin in f['source_hashes'].items():self.assertEqual(a.old.sha(name),pin)
        original=read(a.previous.OLD/'host_native_result.json')
        self.assertFalse(original['accepted']);self.assertIsNone(original['terminal_pass'])


if __name__=='__main__':unittest.main()
