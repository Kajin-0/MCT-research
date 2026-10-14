"""READ-ONLY exact scalar checks on the one new refused control, no native launch."""
import ctypes,json,math
from pathlib import Path
import numpy as np
import observables as v, owned_pair as o, audit

def main():
 root=o.PRIVATE/'control';packet=v.decode(v.paths(root,5,1)[(0,1)])
 et=np.array(packet['et'],order='F');wk=np.array(audit.WK);isk=np.ones(3,dtype=np.int32)
 ptr=ctypes.POINTER(ctypes.c_double);iptr=ctypes.POINTER(ctypes.c_int)
 lib=ctypes.CDLL(str(audit.PRIVATE/'replay.so'));nb=ctypes.c_int(48);nk=ctypes.c_int(3)
 sigma=ctypes.c_double(.001);ng=ctypes.c_int(-1);spin=ctypes.c_int(0)
 def stats(mu):
  m=ctypes.c_double(mu)
  args=[et.ctypes.data_as(ptr),ctypes.byref(nb),ctypes.byref(nk),wk.ctypes.data_as(ptr),ctypes.byref(sigma),ctypes.byref(ng),ctypes.byref(m),ctypes.byref(spin),isk.ctypes.data_as(iptr)]
  output=[]
  for name in ['sumkg_','sumkg1_','sumkg2_']:
   fn=getattr(lib,name);fn.restype=ctypes.c_double;output.append(fn(*args))
  return output
 mu=v.scalars(root,5,1)['values']['ef_Ry'];N,d1,d2=stats(mu)
 assert N==float(packet['wg'].sum()) and abs(N-36)>1e-8
 out=np.zeros_like(et,order='F');ef=ctypes.c_double();lib.replay.argtypes=[ptr,ptr,ptr]
 lib.replay(et.ctypes.data_as(ptr),ctypes.byref(ef),out.ctypes.data_as(ptr))
 assert np.float64(mu).tobytes()==np.float64(ef.value).tobytes() and v.bit_equal(out,packet['wg'])
 try:v.check_cold(v.paths(root,5,1),mu)
 except v.Refusal as err:assert str(err)=='independent neutrality budget'
 else:raise AssertionError('frozen scientific refusal missing')
 assert not (o.PRIVATE/'stream/ATTEMPT.json').exists()
 result=json.loads((root/'RESULT.json').read_text());assert result['owned_cgroup_empty'] and not result['native_execution_complete']
 assert o.show(result['unit'])['LoadState']=='not-found'
 print(json.dumps(dict(PASS_preserved_refusal=True,charge=N,ef_Ry=mu,Nprime=d1,Nsecond=d2,squared_residual_gradient=2*(N-36)*d1,squared_residual_curvature=2*(d1*d1+(N-36)*d2),native_replay_bitwise=True,stream_not_launched=True)))
if __name__=='__main__':main()
