"""Three bounded source/reference/refusal checks; no service/MPI/QE launch."""
from pathlib import Path
import json
import re
import unittest
import numpy as np
from packets import Reader,PAIR
from address_admission import checked_address,refuse_reuse

HERE=Path(__file__).resolve().parent


class Focused(unittest.TestCase):
    def test_compiled_original_arithmetic_and_false_convergence_stop(self):
        j=json.loads((HERE/'build_results.json').read_text());self.assertTrue(j['passed'])
        self.assertTrue(all(v['returncode']==0 for v in j['records']))
        src=Path(j['binary']).parent/'source';old=(src/'pristine_exx.f90').read_text();new=(src/'exx.f90').read_text()
        def body(text,name):
            a=re.search(r'^ *SUBROUTINE +'+name+r' *\(',text,re.M|re.I).start()
            b=re.search(r'^ *END SUBROUTINE +'+name+r'\b',text[a:],re.M|re.I).end()+a
            return text[a:b]
        for name in ['vexx_k','aceupdate_k','vexxace_k']:self.assertEqual(body(old,name),body(new,name))
        e=(src/'electrons.f90').read_text();self.assertEqual(e.count('CALL pilot_finish(exxen,fock2,etot)'),1)
        self.assertIn('conv_elec=.FALSE.',e)
        run=(src/'run_pwscf.f90').read_text();segment=run[run.index('IF(pilot_done)THEN'):run.index('IF(pilot_done)THEN')+300]
        self.assertIn("CALL punch('all')",segment);self.assertIn('CALL pilot_publish()',segment);self.assertNotIn('conv_elec=.TRUE.',segment)

    def test_reference_byte_roundtrip_and_density_map_source(self):
        files=[PAIR/m/'reference.bin' for m in ['host','cd']];self.assertEqual(files[0].read_bytes(),files[1].read_bytes())
        r=Reader(files[0]);self.assertEqual(tuple(r.take('<i8',(4,))),(70251406,7809,6,1))
        r.take('<f8',(3,3));self.assertEqual(max(abs(r.take('<f8',(3,)))),0)
        g=r.take('<i8',(3,7809));c=r.take('<c16',(15618,6));r.end()
        self.assertEqual(len(set(map(tuple,g.T))),7809);self.assertLess(np.linalg.norm(c.conj().T@c-np.eye(6),2),1e-8)
        text=(HERE/'pilot_native.inc').read_text();self.assertIn('INT(mill(:,1:SIZE(rho%of_g,1)),8)',text)

    def test_exact_address_refusal_and_no_native_execution(self):
        j=json.loads((HERE/'address_result.json').read_text());failure=json.loads((HERE/'owner_failure.json').read_text())
        self.assertEqual(j['original_bytes'],114);self.assertEqual(j['short_bytes'],105)
        self.assertEqual(j['original_bind_failure']['text'],'AF_UNIX path too long');self.assertTrue(j['short_real_bind_pass'])
        with self.assertRaises(ValueError):checked_address(PAIR/'host','lease.sock')
        with self.assertRaises(ValueError):refuse_reuse(PAIR/'host')
        self.assertEqual(failure['native_executable_invocations'],0);self.assertTrue(failure['Cd_not_launched']);self.assertTrue(failure['own_cgroup_absent'])
        for m in ['host','cd']:self.assertFalse((PAIR/m/'LAUNCH.json').exists());self.assertFalse((PAIR/m/'RANKS.json').exists())


if __name__=='__main__':unittest.main()
