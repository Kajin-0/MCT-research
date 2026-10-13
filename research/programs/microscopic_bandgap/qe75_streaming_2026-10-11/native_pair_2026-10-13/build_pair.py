"""Compile/link fresh-only native fences. Executables remain UNADMITTED."""
from pathlib import Path
import json
import shutil
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
for folder in ['native_envelope_2026-10-13', 'software_2026-10-13',
               'm5_readiness', 'runtime_admission', 'native_bridge']:
    sys.path.insert(0, str(BASE / folder))
from phase_sources import generate, PRIVATE, ROOT, DFT, sha
from build_transport import FC, FLAGS, INCLUDES, run, LinuxGuard, LIB, memory
from fixture_preflight import backends


def main():
    if PRIVATE.exists():
        raise RuntimeError('one-shot private build directory already exists; preserve it')
    if LinuxGuard(LIB).probe(ROOT)['available_bytes'] < 11*2**30 or memory()['MemAvailable'] < 16*2**30:
        raise RuntimeError('compile/link headroom')
    PRIVATE.mkdir(parents=True)
    source = PRIVATE / 'source'
    report = dict(passed=False, QE_MPI_executed=False, admission_issued=False, records=[])
    try:
        report['source'] = generate(source)
        records = report['records']
        client = PRIVATE / 'lease_client.o'
        records.append(run(['/usr/bin/cc', '-std=c11', '-Wall', '-Wextra', '-Werror',
                            '-O2', '-c', source/'lease_client.c', '-o', client]))
        prior = json.loads((ROOT/'native_envelope_20261013/link.json').read_text())
        candidates = {}
        for mode in ['stock', 'stream']:
            folder = PRIVATE / mode
            folder.mkdir()
            flags = FLAGS + ['-D__QE75_INITIAL_CAPTURE', '-D__QE75_RESOURCE_CAPTURE']
            if mode == 'stream':
                flags += ['-D__EXX_QSTREAM']
            inc = ['-J', folder, '-I', folder,
                   '-I', ROOT/'m5_software_20261013/wave'/mode,
                   '-I', ROOT/'native_envelope_20261013/descriptor'/mode,
                   '-I', ROOT/'m5_readiness'/f'{mode}-objects', *INCLUDES]
            objects = []
            for name in ['native_lease', 'init_run', 'exx']:
                obj = folder / (name+'.f90.o')
                records.append(run([FC, *flags, *inc, '-c', source/(name+'.f90'), '-o', obj]))
                objects.append(obj)
            oldarchive = ROOT/'native_envelope_20261013/link-only'/mode/'libqe_pw_envelope.a'
            oldhash = sha(oldarchive)
            archive = folder / 'libqe_pw_pair.a'
            shutil.copy2(oldarchive, archive)
            records.append(run(['/usr/bin/ar', 'd', archive, 'exx.f90.o', 'init_run.f90.o',
                                'qe75_native_lease.f90.o']))
            # Archive names match the old objects; no duplicate definition.
            lease = folder/'qe75_native_lease.f90.o'
            (folder/'native_lease.f90.o').rename(lease)
            objects[0] = lease
            records.append(run(['/usr/bin/ar', 'r', archive, *objects]))
            binary = folder/'pw.first_ace.UNADMITTED'
            oldbinary = ROOT/'native_envelope_20261013/link-only'/mode/'pw.envelope.NATIVE_UNADMITTED'
            command = next(list(r['command']) for r in prior['records']
                           if r['command'][-1] == str(oldbinary))
            command = [str(archive) if v == str(oldarchive) else
                       str(client) if v.endswith('/native_envelope_20261013/link-only/lease_client.o') else v
                       for v in command]
            command[-1] = str(binary)
            records.append(run(command))
            if sha(oldarchive) != oldhash:
                raise RuntimeError('prior archive modified')
            symbols = run(['/usr/bin/nm', '--defined-only', binary])['stdout']
            for symbol in ['__qe75_native_lease_MOD_native_phase',
                           'qe75_capture_initial_', 'qe75_capture_fft_', 'qe75_lease_call']:
                if sum(line.split()[-1] == symbol for line in symbols.splitlines()) != 1:
                    raise RuntimeError('missing/duplicate native phase symbol: '+symbol)
            candidates[mode] = dict(binary=str(binary), sha256=sha(binary),
                                    backends=backends(binary), archive_sha256=sha(archive))
        if candidates['stock']['backends'] != candidates['stream']['backends']:
            raise RuntimeError('paired backend mismatch')
        if candidates['stock']['backends'] != prior['candidates']['stock']['backends']:
            raise RuntimeError('retained backend changed')
        report.update(passed=True, candidates=candidates,
                      stop_semantics='intentional error 85 only after live phase 6, not SCF/restart success')
    finally:
        (PRIVATE/'build.json').write_text(json.dumps(report, indent=2)+'\n')
        (HERE/'build_results.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: six real-QE objects compiled; two fenced candidates linked. No MPI/QE run or authority.')


if __name__ == '__main__':
    main()
