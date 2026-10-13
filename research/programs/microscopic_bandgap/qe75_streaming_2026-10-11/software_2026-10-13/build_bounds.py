"""Pristine serial FFT support only; no FFT transform, MPI or QE execution."""
from pathlib import Path
import json
from build_wave import PRIVATE,FC,INCLUDES,run,HERE,ROOT
from native_bundle import artifact_sha256


def main():
    obj=PRIVATE/'bounds';obj.mkdir(exist_ok=False);src=ROOT/'q-e/FFTXlib/src'
    records=[]
    for name in ['fft_param','fft_support']:
        records.append(run([FC,'-cpp','-O0','-fcheck=all','-J',obj,'-I',obj,'-c',src/(name+'.f90'),'-o',obj/(name+'.o')]))
    records.append(run([FC,'-O0','-fcheck=all','-I',obj,HERE/'fft_unit.f90',obj/'fft_support.o',
                        obj/'fft_param.o','-o',obj/'fft_unit']))
    report={'passed':True,'records':records,'native_MPI_QE_run':False,'FFT_transform_run':False,
            'source_sha256':{str(p):artifact_sha256(p) for p in [src/'fft_param.f90',src/'fft_support.f90',HERE/'fft_unit.f90']}}
    (PRIVATE/'bounds_build.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: pristine QE FFT size/padding component compiled without MPI.')


if __name__=='__main__':main()
