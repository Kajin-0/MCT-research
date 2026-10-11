"""Cheap native execution-protocol checks; no native process is started here."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
sys.path.insert(0,str(DFT/'src'))
SOURCE=DFT/'scripts/r07_approved_pair_member_20261011.py'
spec=importlib.util.spec_from_file_location('approved_native_member',SOURCE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def clean_text():
    return 'convergence has been achieved\nEXX self-consistency reached\nestimated scf accuracy < 0.3E-11 Ry\nJOB DONE'


def test_execution_source_and_launch_provenance():
    record=json.loads((HERE/'host_launch_provenance.json').read_text())
    for source in (SOURCE,HERE/'native_member_execution_source.py'):
        assert hashlib.sha256(source.read_bytes()).hexdigest()==record['driver_sha256']
    assert record['mpi_ranks']==6 and record['seconds']+record['grace_seconds']==5400
    assert record['empirical_alloy_gap_inputs']==[] and record['physical_xc'] is None
    for path,expected in record['source_and_supervisor_hashes'].items():
        assert module.digest(path)==expected


def test_runtime_and_output_rewrite_preserves_physics_exactly():
    source=(module.PAIR/'host/pw.in').read_text()
    target=module.changed_input(source,DFT/'calculations/r07/one_approved_probe/out')
    strip=lambda text:re.sub(r'(?m)^\s*(outdir|max_seconds)\s*=.*\n','',text)
    assert strip(source)==strip(target)
    assert 'max_seconds = 3600.0' in target
    assert 'ecutfock = 120.0' in target and 'conv_thr = 1e-10' in target
    assert 'nbnd = 352' in target and 'diago_full_acc = .true.' in target
    try:
        module.changed_input(source+'\n nstep = 0\n',DFT/'calculations/r07/probe/out')
    except ValueError:
        pass
    else:
        raise AssertionError('dry input must never be admitted')


def test_strict_native_terminal_convergence_and_failure_cases():
    ok=clean_text()
    assert module.native_terminal(ok,'',0,False,False,{})['accepted_scf']
    for text in (ok.replace('EXX self-consistency reached',''),
                 ok.replace('convergence has been achieved',''),
                 ok.replace('0.3E-11','0.3E-8'),
                 ok.replace('JOB DONE',''),ok+'\nMaximum CPU time exceeded'):
        assert not module.native_terminal(text,'',0,False,False,{})['accepted_scf']
    for err,code,exit_requested,forced,remaining in (
        ('MPI_ABORT',0,False,False,{}),('',1,False,False,{}),
        ('',0,True,False,{}),('',0,False,True,{}),('',0,False,False,{1:'pw.x'})):
        assert not module.native_terminal(ok,err,code,exit_requested,forced,remaining)['accepted_scf']


def test_external_headroom_change_passes_original_guard_without_relaxing_it():
    original=json.loads((HERE/'preflight.json').read_text())
    resumed=json.loads((HERE/'resumed_preflight.json').read_text())
    assert resumed['policy']==original['policy']
    assert not original['host_preflight_passed'] and resumed['host_preflight_passed']
    assert resumed['effective_available_memory_bytes']>original['effective_available_memory_bytes']
    assert resumed['process_ownership']['exclusive_MPI_snapshot']
    launch=json.loads((HERE/'host_launch_provenance.json').read_text())
    assert launch['process_family_RSS_limit_bytes'] <= .85*launch['RAM_preflight_bytes']['MemTotal']
    assert launch['process_family_RSS_limit_bytes'] <= launch['RAM_preflight_bytes']['MemAvailable']-2*1024**3
