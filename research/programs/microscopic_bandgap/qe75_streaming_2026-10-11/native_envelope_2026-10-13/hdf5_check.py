"""Small genuine qeh5 serialization tests; observed overhead is NOT a bound."""
import json
from pathlib import Path
import resource
import subprocess
import tempfile
import h5py
import numpy as np
from build_transport import PRIVATE,ROOT,HERE,FC,INCLUDES,DFT,run,LinuxGuard,LIB,memory
from envelope import wave_file_payload,density_file_payload
from native_bundle import artifact_sha256


def main():
    if LinuxGuard(LIB).probe(PRIVATE)['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):
        raise RuntimeError('serial HDF5 check headroom')
    folder=PRIVATE/'hdf5';folder.mkdir(exist_ok=False)
    old=ROOT/'m5_readiness/hdf5-serial';qlib=DFT/'.local/qe-env/lib'
    binary=folder/'schema_unit';records=[];observations=[]
    records.append(run([FC,'-O0','-fcheck=all','-ffree-line-length-none','-I',old,*INCLUDES,
                        HERE/'hdf5_schema_unit.f90',old/'qeh5.o',old/'no_mpi_init.o','-Wl,--export-dynamic',
                        '-L',qlib,'-Wl,-rpath,'+str(qlib),'-lhdf5_fortran','-lhdf5','-o',binary]))
    for n in [17,257]:
        for kind in ['wave','density']:
            path=folder/f'{kind}.{n}.h5';records.append(run([binary,path,str(n),kind]))
            with h5py.File(path,'r') as f:
                expected={'MillerIndices','evc'} if kind=='wave' else {'MillerIndices','rhotot_g','m_x','m_y','m_z'}
                if set(f.keys())!=expected:raise RuntimeError('schema mismatch')
                np.testing.assert_array_equal(f['MillerIndices'][:],np.arange(1,3*n+1).reshape(n,3))
                sizes={name:d.id.get_storage_size() for name,d in f.items()}
                if any(d.chunks is not None or d.compression is not None for d in f.values()):raise RuntimeError('default contiguous unfiltered changed')
                if kind=='wave':
                    if f['evc'].shape!=(48,4*n) or len(f.attrs)!=9:raise RuntimeError('wave attributes/shape')
                    np.testing.assert_array_equal(f['evc'][:],np.tile([1.0,2.0],(48,2*n)))
                else:
                    if len(f.attrs)!=3:raise RuntimeError('density attributes')
                    for name in expected-{'MillerIndices'}:np.testing.assert_array_equal(f[name][:],np.tile([1.0,2.0],n))
                payload=wave_file_payload(n,2,48) if kind=='wave' else density_file_payload(n,4)
                if sum(sizes.values())!=payload:raise RuntimeError('source payload formula mismatch')
                st=path.stat()
                observations.append({'kind':kind,'G':n,'dataset_storage_bytes':sizes,'payload_bytes':payload,
                       'logical_file_bytes':st.st_size,'allocated_file_bytes':512*st.st_blocks,
                       'logical_nonpayload_bytes_observed':st.st_size-payload,
                       'default_contiguous_unfiltered':True,'universal_overhead_bound_proven':False})
    report={'passed':True,'records':records,'observations':observations,'max_serial_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'qeh5_object_sha256':artifact_sha256(old/'qeh5.o'),'MPI_init_trap_sha256':artifact_sha256(old/'no_mpi_init.o'),
            'binary_sha256':artifact_sha256(binary),'native_PW_MPI_run':False,'whole_HDF5_RSS_or_disk_bound_proven':False}
    (PRIVATE/'hdf5_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: pristine qeh5 four tiny schema/payload checks with MPI-init trap; no PW/MPI; overhead observations only.')


if __name__=='__main__':main()
