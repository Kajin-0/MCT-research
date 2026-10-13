"""Private hardened wire/native-lease builds. No MPI communicator or PW run."""
from pathlib import Path
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'software_2026-10-13'))
from build_wave import ROOT,DFT,FC,INCLUDES,FLAGS,run
from native_bundle import artifact_sha256
from family_runtime import LinuxGuard,LIB,memory
PRIVATE=ROOT/'native_envelope_20261013'


def sources(folder):
    old=HERE.parent/'m5_readiness'
    c=(old/'lease_client.c').read_text()
    c=c.replace('#include <inttypes.h>','#include <inttypes.h>\n#include <limits.h>',1)
    needle='    result=(int)get32(reply+8);'
    if c.count(needle)!=1:raise RuntimeError('wire status anchor changed')
    c=c.replace(needle,'''    /* Wire status is unsigned. Reject nonrepresentable signed errors before
       conversion; a negative value could otherwise disappear in MPI_MAX. */
    uint32_t wire_status=get32(reply+8);
    if(wire_status>INT_MAX){result=EPROTO;goto done;}
    result=(int)wire_status;''',1)
    f=(old/'native_lease.f90').read_text()
    needle='    CALL mp_max(code,world_comm)'
    if f.count(needle)!=2:raise RuntimeError('collective status anchors changed')
    f=f.replace(needle,'''    ! Reduce a Boolean FAILURE indicator, not a signed foreign status.
    ! Preserve every nonzero error including INT_MIN; never use ABS(code).
    code=MERGE(1,0,code/=0)
    CALL mp_max(code,world_comm)''')
    (folder/'lease_client.c').write_text(c);(folder/'native_lease.f90').write_text(f)
    return {'prior_C_sha256':artifact_sha256(old/'lease_client.c'),
            'prior_Fortran_sha256':artifact_sha256(old/'native_lease.f90'),
            'new_C_sha256':artifact_sha256(folder/'lease_client.c'),
            'new_Fortran_sha256':artifact_sha256(folder/'native_lease.f90')}


def main():
    if LinuxGuard(LIB).probe(PRIVATE)['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):
        raise RuntimeError('small build headroom')
    folder=PRIVATE/'transport';folder.mkdir(exist_ok=False);pins=sources(folder);records=[]
    old=HERE.parent/'m5_readiness'
    for name,source in [('legacy',old/'lease_client.c'),('safe',folder/'lease_client.c')]:
        records.append(run(['/usr/bin/cc','-std=c11','-O2','-Wall','-Wextra','-Werror',
                            HERE/'wire_worker.c',source,'-o',folder/(name+'_worker')]))
    for mode in ['stock','stream']:
        obj=folder/mode;obj.mkdir()
        records.append(run([FC,*FLAGS,'-J',obj,*INCLUDES,'-c',folder/'native_lease.f90','-o',obj/'native_lease.o']))
    # Explicit decision-model stubs, not an MPI library or live authority.
    for version,source in [('legacy',old/'native_lease.f90'),('safe',folder/'native_lease.f90')]:
        obj=folder/(version+'-model');obj.mkdir()
        records.append(run([FC,'-O0','-fcheck=all','-J',obj,'-I',obj,'-c',HERE/'decision_stubs.f90','-o',obj/'stubs.o']))
        records.append(run([FC,'-O0','-fcheck=all','-J',obj,'-I',obj,'-c',source,'-o',obj/'lease.o']))
        records.append(run([FC,'-O0','-fcheck=all','-I',obj,HERE.parent/'software_2026-10-13/collective_unit.f90',
                            obj/'lease.o',obj/'stubs.o','-o',folder/(version+'_model')]))
    report={'passed':True,'pins':pins,'records':records,'actual_MPI_PW_run':False,'native_authority_issued':False}
    (PRIVATE/'transport_build.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: exact C ABI and real-QE lease objects hardened; serial models only.')


if __name__=='__main__':main()
