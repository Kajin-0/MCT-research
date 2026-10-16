"""Synthetic packet/import/static source tests. No material or QE execution."""
import importlib.util,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
import numpy as np
import reader
P=Path(__file__).resolve().parent
class Checks(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=P.parents[3]/'.tmp/r07spc16');self.p=Path(self.tmp.name)/'H.one';self.packet()
 def tearDown(self):self.tmp.cleanup()
 def packet(self):
  n=4;ng=4;nr=8;P0=np.zeros((2*n,12),complex);P0[:6,:6]=np.eye(6);P0[:,6:]=P0[:,:6]
  H=np.diag(np.arange(8.))@P0
  self.fields=[np.array([reader.MAGIC,1,1,0,123,n,n,ng,nr,nr,352,12,4,712,16,0,24,0,0,0],'<i8'),np.zeros((14,2),'<i8'),np.eye(3),np.zeros(3),np.zeros(8),np.array([[0,1,2,3],[0,0,0,0],[0,0,0,0]],'<i8'),np.array([[0,1,2,3],[0,0,0,0],[0,0,0,0]],'<i8'),P0,H*.25,H*.5,H*.25,H,np.zeros((ng,4),complex),np.zeros((nr,4)),np.zeros((nr,4))]
  self.write()
 def write(self):self.p.write_bytes(b''.join(a.tobytes(order='F') for a in self.fields))
 def test_valid_components_gauge(self):
  d=reader.read(self.p);r=reader.diagnostics(d);self.assertLess(r['component_error_Ry'],1e-14)
  omega=r['Omega_Ry'];q=r['QHP_norm_Ry'];d['H']+=7*d['P']
  r2=reader.diagnostics(d);self.assertAlmostEqual(omega,r2['Omega_Ry']);self.assertAlmostEqual(q,r2['QHP_norm_Ry']);self.assertFalse(r2['science_release'])
 def test_old_rank_schema(self):
  self.fields[0][2]=2;self.write()
  with self.assertRaises(reader.Refusal):reader.read(self.p)
 def test_truncation_and_trailer(self):
  raw=self.p.read_bytes()
  for a in (raw[:-1],raw+b'x'):
   self.p.write_bytes(a)
   with self.assertRaises(reader.Refusal):reader.read(self.p)
 def test_nonfinite_duplicate(self):
  self.fields[7][0,0]=np.nan;self.write()
  with self.assertRaises(reader.Refusal):reader.read(self.p)
  self.packet();self.fields[5][:,1]=self.fields[5][:,0];self.write()
  with self.assertRaises(reader.Refusal):reader.read(self.p)
 def test_no_science_small_packet(self):
  with self.assertRaises(reader.Refusal):reader.read(self.p,science=True)
 def test_hermiticity_normalization(self):
  d=reader.read(self.p);d['H'][0,1]+=1j
  with self.assertRaises(reader.Refusal):reader.diagnostics(d)
  d=reader.read(self.p);d['P'][0,0]=2
  with self.assertRaises(reader.Refusal):reader.diagnostics(d)
 def test_explicit_theta_control(self):
  d=reader.read(self.p);d['G']=np.array([[0,1,-1,0],[0,0,0,1],[0,0,0,0]])
  with self.assertRaises(reader.Refusal):reader.theta(d['P'][:,:6],d['G'])
  d['G']=np.array([[-2,-1,1,2],[0,0,0,0],[0,0,0,0]])
  d['P'][:,6:]=reader.theta(d['P'][:,:6],d['G']);d['H']=3*d['P']
  self.assertEqual(reader.theta_controls(d),0.)
  np.testing.assert_array_equal(reader.theta(reader.theta(d['P'],d['G']),d['G']),-d['P'])
  d['H'][0,6]+=1e-3
  with self.assertRaises(reader.Refusal):reader.theta_controls(d)
 def test_clean_import(self):
  r=subprocess.run([sys.executable,'-I','-B','-c','import importlib.util; s=importlib.util.spec_from_file_location("r07reader",'+repr(str(P/'reader.py'))+'); m=importlib.util.module_from_spec(s);s.loader.exec_module(m); assert not m.MAGIC==70251520'],capture_output=True,text=True,timeout=10)
  self.assertEqual(r.returncode,0,r.stderr)
 def test_source_path(self):
  s=(P/'density_driver.f90').read_text().lower();calls=[]
  import re
  calls=re.findall(r'\bcall\s+(\w+)',s)
  for banned in ('allocate_wfc_k','wfcinit','openfil','electrons','non_scf','read_collected_wfc','stop_run','stop_pp'):self.assertNotIn(banned,calls)
  for required in ('read_file_new','set_vrs','init_igk','init_us_2','allocate_bec_type','h_psi','vloc_psi_nc_acc','calbec','add_vuspsi'):self.assertIn(required,calls)
  self.assertIn('needwf=.false.',s);self.assertNotIn('nbnd=12',s);self.assertLess(s.index('if(build_gate()'),s.index('call mp_startup'))
if __name__=='__main__':unittest.main(verbosity=2)
