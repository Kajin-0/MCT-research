"""Prepare exact two-atom deck pins and report the FIRST unpassed launch gate.

No launch command is executed; no service, reservation, queue or lease is issued.
"""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
for name in ['software_2026-10-13', 'm5_readiness', 'runtime_admission',
             'checkpoint_phase', 'native_bridge']:
    sys.path.insert(0, str(BASE/name))
from phase_sources import DFT, ROOT, PRIVATE, sha
from fixture_preflight import template, physical_text, PP_SHA, QE_PIN, backends, PW_OPTIONS
from common_state import common_input_id
from family_runtime import LinuxGuard, LIB, memory


def main():
    build = json.loads((PRIVATE/'build.json').read_text())
    tests = json.loads((HERE/'test_results.json').read_text())
    if not build['passed'] or not tests['passed']:
        raise RuntimeError('unpassed NEW source/wire/comparison tests')
    qe = subprocess.check_output(['git', '-C', str(ROOT/'q-e'), 'rev-parse', 'HEAD'], text=True).strip()
    if qe != QE_PIN:
        raise RuntimeError('QE base revision changed')
    for mode, record in build['candidates'].items():
        if sha(record['binary']) != record['sha256'] or backends(record['binary']) != record['backends']:
            raise RuntimeError('candidate/backend pins changed')
    pp = {}
    for species, expected in PP_SHA.items():
        p = DFT/'pseudopotentials'/(species+'_sg15_pbe_fr_v12.UPF')
        if sha(p) != expected:
            raise RuntimeError('physical pseudopotential pin changed')
        pp[species] = dict(path=str(p), sha256=expected)
    folder = PRIVATE/'protocol'
    folder.mkdir(exist_ok=False)
    originals = {mode: template(mode) for mode in ['control', 'stream']}
    common = common_input_id(originals['control'], originals['stream'], build['candidates']['stock']['backends'])
    decks = {}
    commands = {}
    for mode, arithmetic in [('control', 'stock'), ('stream', 'stream')]:
        original = originals[mode]
        oldpath = original.split("outdir = '", 1)[1].split("'", 1)[0]
        root = folder/mode
        text = original.replace(oldpath, str(root/'out'))
        if physical_text(text) != physical_text(original):
            raise RuntimeError('physics/numerical deck changed')
        p = folder/(mode+'.in'); p.write_text(text)
        decks[mode] = dict(path=str(p), sha256=sha(p), output_path=str(root/'out'),
                           only_operational_outdir_changed=True)
        # A pinned recipe, not an issued JOB or executable launcher.
        commands[mode] = [str(DFT/'.local/qe-env/bin/mpirun'), '--oversubscribe',
            '--host', 'localhost:2', '-np', '2', build['candidates'][arithmetic]['binary'],
            *PW_OPTIONS, '-in', str(p)]
    if physical_text((folder/'control.in').read_text()) != physical_text((folder/'stream.in').read_text()):
        raise RuntimeError('paired physical/numerical input differs')
    storage = LinuxGuard(LIB).probe(PRIVATE)
    mem = memory()['MemAvailable']
    before = subprocess.run([sys.executable, str(BASE/'software_2026-10-13/preservation.py')],
        cwd=DFT, capture_output=True, text=True, timeout=30, check=True)
    preservation = json.loads(before.stdout)
    # The old helper's False is scoped to its source-only phase; it cannot erase
    # the user's genuine native MPI run. Preserve the actual artifact checks.
    preservation.pop('native_MPI_QE_run', None)
    preservation['this_Codex_phase_started_MPI_QE'] = False
    p = dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status='BLOCKED_BEFORE_LAUNCH', QE_or_MPI_executed_this_phase=False,
        local_contract='LOCAL_OWNED_QE_FIRST_ACE_ONLY; not original host-wide exclusion',
        QE_source_revision=qe, candidate_pins=build['candidates'], pseudopotentials=pp,
        compiler_sha256=sha(ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran'),
        launcher_sha256=sha((DFT/'.local/qe-env/bin/mpirun').resolve()),
        decks=decks, common_input_sha256=common, proposed_commands_NOT_ISSUED=commands,
        required_environment=dict(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
            OMPI_MCA_plm='isolated', OMPI_MCA_btl='self,sm', OMPI_MCA_pml='ob1'),
        ceilings=dict(cgroup_memory_max_bytes=12*2**30, memory_swap_max_bytes=0,
            tasks_max=32, runtime_max_seconds=600, family_summed_RSS_limit_bytes=12*2**30,
            host_MemAvailable_floor_bytes=4*2**30, disk_free_floor_bytes=10*2**30,
            initial_host_MemAvailable_required_bytes=16*2**30),
        observed=dict(MemAvailable_bytes=mem, storage_snapshot=storage,
            initial_RAM_floor_pass=mem>=16*2**30,
            raw_disk_floor_pass=storage['available_bytes']>=10*2**30),
        first_unpassed_gate='Complete pre-first-ACE resource/producer certificate is absent. '
            'No certified full RSS/backend peak and live-output inode/allocation envelope; '
            'floors and a cgroup hard cap do not substitute for these quantities.',
        targeted_state_remedy=dict(compiled_and_linked=True, live_phase_scope=4,
            stages={4:'all-rank actual initial-state validation/parity',
                    5:'actual FFT/resource certificate',
                    7:'actual fresh per-rank allocated stream inode/extents',
                    6:'all-rank first-ACE packet coverage then intentional cutoff'},
            production_scope4_issuer_integrated=False, actual_initial_wave_observations_available=False,
            actual_FFT_descriptors_available=False),
        old_scope2_restart_bridge_kept_strict=True, hostwide_exclusion_passed=False,
        private_network_passed=False, no_new_reservations_or_unit_created=True,
        preservation=preservation)
    (HERE/'preflight_results.json').write_text(json.dumps(p, indent=2)+'\n')
    (HERE/'control.in').write_bytes((folder/'control.in').read_bytes())
    (HERE/'stream.in').write_bytes((folder/'stream.in').read_bytes())
    print(json.dumps(dict(status=p['status'], first_unpassed_gate=p['first_unpassed_gate'],
        MemAvailable_bytes=mem, free_disk_bytes=storage['available_bytes'],
        state_remedy='compiled fenced candidates and tested strict comparator; native observations/issuer not qualified',
        preservation=preservation), indent=2))


if __name__ == '__main__':
    main()
