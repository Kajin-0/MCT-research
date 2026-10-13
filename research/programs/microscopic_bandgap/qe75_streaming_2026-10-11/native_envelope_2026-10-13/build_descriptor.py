"""Compile actual QE FFT observer in both modes; run only standalone serial codec."""
import json
from build_transport import PRIVATE,ROOT,HERE,FC,INCLUDES,FLAGS,run,LinuxGuard,LIB,memory
from descriptor_source import generate
from native_bundle import artifact_sha256


def main():
    if LinuxGuard(LIB).probe(PRIVATE)['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):
        raise RuntimeError('descriptor build headroom')
    folder=PRIVATE/'descriptor';pins=generate(folder);records=[]
    for mode in ['stock','stream']:
        obj=folder/mode;obj.mkdir(exist_ok=True)
        records.append(run([FC,*FLAGS,'-J',obj,'-I',obj,*INCLUDES,'-c',folder/'resource_descriptor.f90','-o',obj/'resource_descriptor.o']))
        flags=FLAGS+['-D__QE75_RESOURCE_CAPTURE']+(['-D__EXX_QSTREAM'] if mode=='stream' else [])
        records.append(run([FC,*flags,'-J',obj,'-I',obj,'-I',PRIVATE/'transport'/mode,
                            '-I',ROOT/'m5_readiness'/f'{mode}-objects',*INCLUDES,
                            '-c',folder/'exx.f90','-o',obj/'exx.o']))
        records.append(run([FC,'-O0','-fcheck=all','-ffree-line-length-none','-I',obj,*INCLUDES,
                            HERE/'descriptor_unit.f90',obj/'resource_descriptor.o','-o',obj/'descriptor_unit']))
    old=(ROOT/'m5_readiness/source/exx.f90').read_text();new=(folder/'exx.f90').read_text();equal={}
    for a,b in [('  SUBROUTINE vexx_k(', '  END SUBROUTINE vexx_k'),
                ('  FUNCTION exxenergy2_k(', '  END FUNCTION  exxenergy2_k'),
                ('  SUBROUTINE aceupdate_k(', '  END SUBROUTINE aceupdate_k'),
                ('  SUBROUTINE vexxace_k(', '  END SUBROUTINE vexxace_k')]:
        def part(t):
            i=t.index(a);return t[i:t.index(b,i)+len(b)]
        if part(old)!=part(new):raise RuntimeError('EXX arithmetic changed')
        equal[a.strip()]=True
    report={'passed':True,'pins':pins,'records':records,'core_arithmetic_byte_equal':equal,
            'binary_sha256':{str(folder/m/'descriptor_unit'):artifact_sha256(folder/m/'descriptor_unit') for m in ['stock','stream']},
            'actual_native_MPI_descriptor_observed':False,'PW_MPI_executed':False}
    (PRIVATE/'descriptor_build.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: actual QE typed FFT observer compiles in both modes; native NOT RUN.')


if __name__=='__main__':main()
