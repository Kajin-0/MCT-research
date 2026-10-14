"""ALL retained full-SCF control snapshots, before any new native execution."""
import ctypes,json,hashlib,importlib.util
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
spec=importlib.util.spec_from_file_location('historical_observables',BASE/'full_scf_2026-10-13/observables.py');obs=importlib.util.module_from_spec(spec);spec.loader.exec_module(obs)
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011');OLD=ROOT/'smearing_conditioning_20261013/replay.so'
WK=np.array([.125,.5,.375]);ptr=ctypes.POINTER(ctypes.c_double)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 lib=ctypes.CDLL(str(OLD));lib.replay.argtypes=[ptr,ptr,ptr]
 nb=ctypes.c_int(48);nk=ctypes.c_int(3);sig=ctypes.c_double(.001);ng=ctypes.c_int(-1);spin=ctypes.c_int(0);isk=np.ones(3,dtype=np.int32)
 records=[];inputs={};pins={};i=0
 for directory in sorted(ROOT.glob('*/control/trajectory')):
  for file in sorted(directory.glob('rank0.step*.stage1.k1.state'),key=lambda p:int(p.name.split('.step')[1].split('.')[0])):
   step=int(file.name.split('.step')[1].split('.')[0]);root=directory.parent;pp=obs.paths(root,step,1);packets=[obs.decode(p) for p in pp.values()]
   first=packets[0]
   assert all(obs.bit_equal(first['et'],d['et']) and obs.bit_equal(first['wg'],d['wg']) for d in packets)
   assert first['et'].shape==(48,3)
   et=np.array(first['et'],order='F');w=np.zeros((48,3),order='F');mu=ctypes.c_double();lib.replay(et.ctypes.data_as(ptr),ctypes.byref(mu),w.ctypes.data_as(ptr))
   m=ctypes.c_double(mu.value);args=[et.ctypes.data_as(ptr),ctypes.byref(nb),ctypes.byref(nk),WK.ctypes.data_as(ptr),ctypes.byref(sig),ctypes.byref(ng),ctypes.byref(m),ctypes.byref(spin),isk.ctypes.data_as(ctypes.POINTER(ctypes.c_int))]
   stat=[]
   for n in ['sumkg_','sumkg1_','sumkg2_']:
    fn=getattr(lib,n);fn.restype=ctypes.c_double;stat.append(fn(*args))
   lines=(directory/f'rank0.step{step}.stage1.scalars').read_text().splitlines()
   direct=float(lines[-1]) if len(lines)==13 else None
   if direct is not None:assert np.float64(direct).tobytes()==np.float64(mu.value).tobytes()
   row=dict(id=i,root=str(root),outer=step,all_six_rank_k_et_wg_replicated=True,native_charge_electrons=float(first['wg'].sum()),native_charge_error=float(first['wg'].sum()-36),source_replayed_mu_Ry=mu.value,direct_native_mu_Ry=direct,stock_source_wg_bitwise=obs.bit_equal(w,first['wg']),Nprime=stat[1],Nsecond=stat[2])
   records.append(row);inputs['et_'+str(i)]=et;inputs['wg_'+str(i)]=first['wg'];i+=1
   for p in pp.values():pins[str(p)]=sha(p)
 np.savez(HERE/'retained_inputs.npz',**inputs)
 result=dict(timestamp=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),records=records,packet_sha256=pins,stock_serial_lib_sha256=sha(OLD),all_retained_full_SCF_control_snapshots_in_shallow_archive_included=True,stock14outer_log_only_no_invented_per_outer_eigenvalues=True,no_new_native_QE_MPI=True)
 (HERE/'input_audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps([{k:r[k] for k in ['id','outer','native_charge_error','Nprime','stock_source_wg_bitwise']}|{'archive':Path(r['root']).parent.name} for r in records],indent=2))
if __name__=='__main__':main()
