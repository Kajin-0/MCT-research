"""Compile unchanged lease source against explicit serial decision stubs only."""
import json
from build_wave import PRIVATE,FC,run,HERE
from native_bundle import artifact_sha256


def main():
    obj=PRIVATE/'collectives';obj.mkdir(exist_ok=False)
    source=HERE.parent/'m5_readiness/native_lease.f90'
    records=[]
    for name,path in [('stubs',HERE/'collective_stubs.f90'),('native_lease',source)]:
        records.append(run([FC,'-O0','-g','-fcheck=all','-J',obj,'-I',obj,'-c',path,'-o',obj/(name+'.o')]))
    records.append(run([FC,'-O0','-fcheck=all','-I',obj,HERE/'collective_unit.f90',obj/'native_lease.o',
                        obj/'stubs.o','-o',obj/'collective_unit']))
    deps=run(['ldd',obj/'collective_unit'])
    if 'libmpi' in deps['stdout'] or 'libmpich' in deps['stdout']:raise RuntimeError('unexpected MPI dependency')
    report={'passed':True,'records':records,'unchanged_native_lease_sha256':artifact_sha256(source),
            'dependencies':deps,'MPI_communicator_or_QE_run':False,'model':'SERIAL_COLLECTIVE_DECISION_STUB_NOT_NATIVE_AUTHORITY'}
    (PRIVATE/'collective_build.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: unchanged lease source compiles against explicit no-MPI decision stubs.')


if __name__=='__main__':main()
