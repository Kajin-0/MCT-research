"""Read-only original state and our transient-unit closure audit."""
import importlib.util
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'native_envelope_2026-10-13'))
from contracts import PRIVATE,BASE,REGISTRY,LOCK,flock_owner,show,artifact_sha256


def check():
    spec=importlib.util.spec_from_file_location('prior_native_preserve',HERE.parent/'native_envelope_2026-10-13/preservation.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    r=module.check()
    expected=json.loads((HERE.parent/'native_envelope_2026-10-13/link_results.json').read_text())['candidates']
    for c in expected.values():
        if artifact_sha256(Path(c['binary']))!=c['sha256']:raise RuntimeError('de000d4 candidate changed')
    if REGISTRY.read_bytes()!=(PRIVATE/'legacy_registry_original.bytes').read_bytes():raise RuntimeError('legacy ledger not restored byte-exact')
    units=[]
    for root in PRIVATE.glob('case-*'):
        job=json.loads((root/'JOB.json').read_text())
        state=show(job['unit'])['LoadState']
        if state!='not-found':raise RuntimeError('our transient unit not collected: '+job['unit'])
        units.append({'unit':job['unit'],'state':state})
    if flock_owner(LOCK):raise RuntimeError('lease remains held')
    r.update(legacy_registry_restored_byte_exact=True,de000d4_candidates_unchanged=True,owned_units=units,
             own_cgroup_ledger_phase=json.loads((PRIVATE/'CURRENT_UNIT.json').read_text())['phase'])
    if r['own_cgroup_ledger_phase']!='FINISHED':raise RuntimeError('our cgroup ledger not closed')
    return r


if __name__=='__main__':print(json.dumps(check(),indent=2))
