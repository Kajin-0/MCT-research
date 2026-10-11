"""Focused independent artifact/source checks. No compile, PW or MPI launch."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
SOURCE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/q-e')
spec=importlib.util.spec_from_file_location('validate_candidate', HERE/'validate_candidate.py')
validator=importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class EngineeringChecks(unittest.TestCase):
    def test_capacity_identity_including_arbitrary_padding(self):
        self.assertEqual(64**3*2*352*8*16,23622320128)
        self.assertEqual(64**3*2*352*16,2952790016)
        # Geometry padding changes capacity, never the 7/8 fraction for Q=8.
        for local_sites in ([43691]*6,[45056]*6,[1,3,5,9,11,13]):
            full=sum(16*n*2*352*8 for n in local_sites)
            streamed=sum(16*n*2*352 for n in local_sites)
            self.assertEqual(full,8*streamed)
            self.assertEqual(full-streamed,7*streamed)

    def test_final_unit_and_preservation_evidence(self):
        v=json.loads((HERE/'validation.json').read_text())
        self.assertTrue(v['passed'])
        self.assertFalse(v['native_executables_invoked'])
        self.assertFalse(v['qualified_for_native_run'])
        self.assertEqual(len(v['unit_cases']),24)
        self.assertTrue(all(case['passed'] for case in v['unit_cases']))
        self.assertEqual({case['returncode'] for case in v['unit_cases'] if case['case']=='normal'},{0})
        self.assertEqual({case['returncode'] for case in v['unit_cases'] if case['case']=='truncate'},{9})
        self.assertEqual(v['link']['returncode'],0)
        p=json.loads((HERE/'preservation_and_resources.json').read_text())
        pins=p['all_17_source_supervisor_pins_unchanged']
        self.assertEqual(len(pins),17)
        self.assertTrue(all(x['expected']==x['observed'] for x in pins.values()))
        self.assertTrue(p['dirty_DFT_status_identical'])
        self.assertTrue(p['stock_QE_artifacts_unchanged'])
        self.assertTrue(p['native_peak_unknown'])

    @unittest.skipUnless(SOURCE.exists(),'requires recorded private source; no automatic download')
    def test_actual_source_operation_audit(self):
        self.assertEqual(len(validator.audit_sources(SOURCE)),8)

    @unittest.skipUnless(SOURCE.exists(),'requires recorded private source; no automatic download')
    def test_continued_source_index_defect_is_rejected(self):
        original_read=Path.read_text
        text=(SOURCE/'PW/src/exx.f90').read_text()
        needle='iexx_start,iqbuf))*temppsic_nc(ir,1,ii)'
        self.assertEqual(text.count(needle),1)
        bad=text.replace(needle,needle.replace('iqbuf','ikq'),1)
        def corrupted(path,*args,**kwargs):
            return bad if path == SOURCE/'PW/src/exx.f90' else original_read(path,*args,**kwargs)
        with patch.object(Path,'read_text',corrupted):
            with self.assertRaises(AssertionError):
                validator.audit_sources(SOURCE)

    @unittest.skipUnless(SOURCE.exists(),'requires recorded private source; no automatic download')
    def test_changed_global_weight_is_rejected(self):
        original_read=Path.read_text
        text=(SOURCE/'PW/src/exx.f90').read_text()
        start=text.index('  SUBROUTINE vexx_k(')
        end=text.index('  END SUBROUTINE vexx_k',start)
        body=text[start:end]
        self.assertIn('nqs_inv = 1.0 / nqs',body)
        bad=text[:start]+body.replace('nqs_inv = 1.0 / nqs','nqs_inv = 0.5 / nqs',1)+text[end:]
        def corrupted(path,*args,**kwargs):
            return bad if path == SOURCE/'PW/src/exx.f90' else original_read(path,*args,**kwargs)
        with patch.object(Path,'read_text',corrupted):
            with self.assertRaises(AssertionError):
                validator.audit_sources(SOURCE)


if __name__=='__main__':
    unittest.main(verbosity=2)
