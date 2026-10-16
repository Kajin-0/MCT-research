"""Final read-only evidence, selected source budget, and preservation checks."""
from pathlib import Path
from datetime import datetime,timezone
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
REPO=HERE.parents[3]
OLD=BASE/'static_environment_2026-10-15'
DFT=Path('/home/User/opencode_workspace/DFT')


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def main():
    audit=json.loads((HERE/'input_audit.json').read_text())
    importer=json.loads((HERE/'import_results.json').read_text())
    owner=json.loads((HERE/'owner_results.json').read_text())
    assert importer['explicit_new_dependency_import_pass'] and owner['all_test_children_reaped']
    assert owner['production_owner_integrated'] is owner['native_admission'] is False
    assert 'cannot resurrect' in owner['cases']['live_denied_attempt_STAYS_REFUSED_after_REAL_exit']
    assert audit['minimum_static_actions_total']==24 and audit['extra_Theta_rank_above1e8']==6
    old=json.loads((OLD/'frozen_protocol.json').read_text())
    for p,h in old['profile']['pins'].items():assert sha(p)==h,p
    for p,h in audit['source_pins'].items():assert sha(p)==h,p
    for p,h in importer['pins'].items():assert sha(p)==h,p
    raw=json.loads((OLD/'evidence_manifest.json').read_text())['raw']
    for p,r in raw.items():assert sha(p)==r['sha256'],p
    protected=json.loads((OLD/'protected_before.json').read_text())
    for p,h in protected['files'].items():assert sha(p)==h,p
    # Source-only hooks/ownership inspection, plus ELF symbol TABLE inspection.
    build=json.loads((OLD/'build_result.json').read_text())
    elf=Path(build['binary']);assert sha(elf)==build['binary_sha256']
    symbols=subprocess.check_output(['/usr/bin/nm','-g','--defined-only',str(elf)],text=True,timeout=20)
    assert 'r07_static_h_' in symbols
    hook_symbols=[line for line in symbols.splitlines() if 'qe75_lease_call' in line or 'native_complete' in line]
    assert not hook_symbols
    driver=(OLD/'native_probe.inc').read_text()
    assert 'lease_call' not in driver and 'native_complete' not in driver
    ot=ast.parse((OLD/'owner.py').read_text())
    accounts=[n for n in ast.walk(ot) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Account']
    assert accounts and all('retirement' not in [k.arg for k in n.keywords] for n in accounts)
    assert 'action==10' not in (OLD/'owner.py').read_text().replace(' ','')
    # Passive ext4/quota/memory check on MCT scratch ONLY: no reservation,
    # service, native launch, global inventory or protected directory changes.
    stream=BASE/'qe75_streaming_2026-10-11'
    sys.path.insert(0,str(stream/'checkpoint_phase'))
    spec=importlib.util.spec_from_file_location('_r07_static_resource_readonly',OLD/'environment_resource_guard.py')
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    lib=next(Path(p) for p in old['profile']['pins'] if p.endswith('/storage_guard.so'))
    assert sha(lib)==old['profile']['pins'][str(lib)]
    scratch=REPO/'.tmp/r07ps16'
    memory={line.split(':')[0]:int(line.split()[1])*1024 for line in Path('/proc/meminfo').read_text().splitlines()
            if line.startswith(('MemAvailable:','MemTotal:'))}
    probe=guard.LinuxGuard(lib).probe(scratch)
    try:
        passive=guard.admission(probe,[64*(1<<20)],14*(1<<30),memory['MemAvailable'])
        passive_status='PASS capacity/quota component ONLY'
    except Exception as e:
        passive={'refusal':repr(e)};passive_status='REFUSED capacity/quota component'
    qsrc=DFT/'.local/qe75_lowram_20261011/q-e/PW/src'
    relevant={}
    markers={
        'v_of_rho.f90':['NB: V(G=0)=0','aux1(:,:) = 0.D0'],
        'setlocal.f90':['vloc(igtongl(1:ngm),nt) * strf(1:ngm,nt)','v_of_0 = DBLE( aux(1) )'],
        'set_vrs.f90':['vrs(:,is) = vltot(:) + vr(:,is)'],
        'wfcinit.f90':["starting_wfc = 'atomic+random'",'CALL read_collected_wfc'],
        'allocate_wfc.f90':['CALL allocate_wfc( npwx, npol, nbnd )','ALLOCATE( vkb(npwx,nkb) )'],
    }
    for name,parts in markers.items():
        p=qsrc/name;text=p.read_text();assert all(s in text for s in parts),name
        relevant[str(p)]=dict(sha256=sha(p),lines={s:text[:text.index(s)].count('\n')+1 for s in parts})
    saves=sum(r['saved_files_logical_B'] for r in audit['members'].values())
    N=21595
    probe_input=2*(128+72+24*N+16*2*N*12)
    frame=16*2*N*12+24*N+72
    bounds=dict(status='SOURCE_SELECTED_BOUNDS_ONLY; COMPLETE_NATIVE_ENVELOPE_NOT_CERTIFIED',
        dimensions_from_unqualified_packet_NOT_physics_acceptance=True,
        per_rank=audit['rank_source_extents'],
        two_member_native_packet_payload_B=audit['native_packet_payload_two_members_exact_B'],
        source_copied_saves_logical_B=saves,probes_two_members_exact_B=probe_input,
        frame_np_arrays_payload_B=frame,
        selected_persistent_and_driver_RAM_B=audit['selected_payload_two_rank_B'],
        known_copies_probe_frame_packets_logical_subtotal_B=saves+probe_input+frame+audit['native_packet_payload_two_members_exact_B'],
        unknown_total_RAM_terms=audit['resource_unknowns'],
        additional_unknown_disk_terms=['wfc buffer close/readback layout','MPI/HDF5/error/tmp/log generations',
            'inode/block rounding/metadata and new owner capture'],
        complete_RAM_runtime_or_disk_bound=False,old_1GiB_4s_observation_NOT_bound=True,
        inherited_caps=dict(memory_B=12*(1<<30),swap_B=0,tasks=12,wall_s=600,
            host_floor_B=4*(1<<30),disk_floor_B=10*(1<<30),sampled_output_cap_B=14*(1<<30)),
        passive_current_storage=probe,passive_current_memory=memory,passive_capacity_status=passive_status,
        passive_capacity_component=passive,new_cgroup_or_reservation_created=False,
        socket_lengths_bytes={m:r['socket_bytes'] for m,r in audit['members'].items()},
        actual_future_address_bind_NOT_attempted=True,source_allocation_and_gauge_pins=relevant)
    (HERE/'source_budget.json').write_text(json.dumps(bounds,indent=2)+'\n')
    # Entire previous handoff preserved; scoped new files and two navigation edits.
    oldhand=subprocess.check_output(['git','show','fdc1b02:research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md'],cwd=REPO).decode()
    hand=(BASE/'SUCCESSOR_HANDOFF.md').read_text()
    begin='<!-- PBE_STATIC_ADMISSION_20261016_BEGIN -->\n';end='<!-- PBE_STATIC_ADMISSION_20261016_END -->\n\n'
    assert hand.count(begin)==hand.count(end)==1
    assert hand[:hand.index(begin)]+hand[hand.index(end)+len(end):]==oldhand
    changed=subprocess.check_output(['git','diff','--name-only','fdc1b02'],cwd=REPO,text=True).splitlines()
    allowed={str((BASE/p).relative_to(REPO)) for p in ['state.md','SUCCESSOR_HANDOFF.md']}
    prefix=str(HERE.relative_to(REPO))+'/'
    assert all(p in allowed or p.startswith(prefix) for p in changed),changed
    for p in HERE.glob('*.py'):ast.parse(p.read_text())
    out=dict(status='PASS bounded read-only admission study; FUTURE_NATIVE_PAIR_NO_GO',
        timestamp_UTC=datetime.now(timezone.utc).isoformat(),baseline='fdc1b02',
        scientific_static_observable='GO under stated finite saved-density definition',
        importer='PASS isolated dependency/format tests; not full science admission',
        owner='PASS component predicates; production native hook/caller NOT qualified',
        first_unpassed_gate='No authenticated native final hook or terminal/FD integration in pinned static PBE executable/owner.',
        ELF_completion_symbols=hook_symbols,old_profile_pins_rechecked=len(old['profile']['pins']),
        original_refused_raw_pins_rechecked=len(raw),all_historical_MCT_files_and_handoff_preserved=True,
        stock_and_pinned_protected_DFT_files_unchanged=True,registry_status_unchanged=True,
        native_QE_PW_MPI_runs=0,SCF=0,builds=0,DFT_writes=0,new_services=0,
        source_budget_complete=False,physical_xc=None,
        package_sha256={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='verification.json'})
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','first_unpassed_gate','old_profile_pins_rechecked','native_QE_PW_MPI_runs']},indent=2))


if __name__=='__main__':main()
