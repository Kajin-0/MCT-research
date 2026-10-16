"""Read-only independent source/object/resource/preservation checks. NO QE."""
from pathlib import Path
from xml.etree import ElementTree as ET
from datetime import datetime,timezone
import ast
import hashlib
import json
import subprocess
import numpy as np

HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3];BASE=HERE.parent
DFT=Path('/home/User/opencode_workspace/DFT')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    build=json.loads((HERE/'build_result.json').read_text());assert build['passed']
    comp=json.loads((HERE/'component_results.json').read_text())
    assert comp['all_children_reaped'] and not comp['actual_systemd_unit_or_MPI']
    assert comp['terminal_manager_cgroup_and_fixture_reader_MOCKED']
    assert comp['tests']['clean_production_owner_and_reader_import']
    for p,h in {**build['source_object_ELF_pins'],**build['unchanged_originals'],**comp['source_sha256']}.items():assert sha(p)==h,p
    raw=json.loads((BASE/'static_environment_2026-10-15/evidence_manifest.json').read_text())['raw']
    for p,r in raw.items():assert sha(p)==r['sha256'],p
    failed=json.loads((BASE/'static_environment_2026-10-15/evidence/GUARD_RESULT.json').read_text())
    assert failed['rank_kernel_exits']=={'0':False,'1':False} and not failed['pass_guard']
    protected=json.loads((BASE/'static_environment_2026-10-15/protected_before.json').read_text())
    for p,h in protected['files'].items():assert sha(p)==h,p
    status=subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)
    diff=subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'diff','--binary'])
    assert status==protected['DFT_status']
    assert hashlib.sha256(diff).hexdigest()==protected['DFT_tracked_diff_sha256']
    stock=DFT/'.local/qe-env/lib/libqe_pw.a'
    private=Path(build['binary']).parent/'libqe_pw_static.a'
    def members(p):return subprocess.check_output(['/usr/bin/ar','t',str(p)],text=True).splitlines()
    names=members(stock);assert names==members(private) and len(names)==len(set(names))
    changed=[]
    for name in names:
        old=subprocess.check_output(['/usr/bin/ar','p',str(stock),name])
        new=subprocess.check_output(['/usr/bin/ar','p',str(private),name])
        if old!=new:changed.append(name)
    assert changed==['run_pwscf.f90.o'],changed
    text=(Path(build['binary']).parent/'run_pwscf.f90').read_text()
    assert text.index('CALL r07_static_phase(1,0_8)')<text.index('CALL init_run()')<text.index('CALL r07_static_H()')
    newprobe=(HERE/'native_probe.inc').read_text()
    pclose=newprobe.index("IF(ios/=0)CALL errore('staticH','packet close',1)")
    assert pclose<newprobe.index('CALL mp_barrier(intra_bgrp_comm)')<newprobe.index('CALL r07_static_phase(10,packet_bytes)')
    phase=(HERE/'native_phase.inc').read_text();assert 'INT(mpime,c_int)' in phase and 'CALL mp_max(code,world_comm)' in phase
    for call in ['CALL h_psi(npwx,n,12,P,full)','CALL allocate_bec_type(nkb,12,becp)',
        'CALL vloc_psi_nc_acc(npwx,n,12,P,vrs,loc)','CALL add_vuspsi(npwx,n,12,nl)']:
        assert call in newprobe and call in (BASE/'static_environment_2026-10-15/native_probe.inc').read_text()
    # PP-derived projector extent; no use of refused Hamiltonian/action values.
    counts={'Hg':6,'Cd':2,'Te':8};projectors={};pins={}
    for species,count in counts.items():
        p=DFT/'.local/qe75_lowram_20261011/p16e_20261015/unshared/out/r07pbe.save'/(species+'_sg15_pbe_fr_v12.UPF')
        t=ET.parse(p);ls=[int(b.attrib['angular_momentum']) for b in t.findall('./PP_NONLOCAL/*') if b.tag.startswith('PP_BETA')]
        projectors[species]=dict(l=ls,angular_projectors=sum(2*l+1 for l in ls),atoms=count)
        pins[str(p)]=sha(p)
    nkb=sum(r['atoms']*r['angular_projectors'] for r in projectors.values());assert nkb==712
    old=json.loads((BASE/'pbe_static_admission_2026-10-16/input_audit.json').read_text())
    rows={}
    for rank,r in old['rank_source_extents'].items():
        p,n,ng,nr,ns=[r[k] for k in ['npwx','active_pw','ngm','nrho','nsmooth']]
        rows[rank]=dict(npwx=p,active_pw=n,ngm=ng,dense_local_grid=nr,smooth_local_grid=ns,
            evc_capacity_352_B=16*2*p*352,vkb_B=16*p*nkb,becp_12_B=16*nkb*2*12,
            initialization_becp_352_B=16*nkb*2*352,
            vloc_transient_psi1_psic_B=16*2*(n+ns),
            selected_fft_persistent_B=8*nr*2+16*ng+16*nr+8*nr*4+16*nr*2,
            one_scf_density_rho_B=8*nr*4+16*ng*4,
            driver_selected_B=r['driver_arrays_selected_upper_B'],
            possible_extra_saved_wave_buffer_B=r['persistent_evc_B'],
            exact_packet_B=r['packet_exact_B'])
    src=DFT/'.local/qe75_lowram_20261011/q-e'
    files=['PW/src/init_run.f90','PW/src/allocate_wfc.f90','PW/src/allocate_fft.f90',
        'PW/src/allocate_locpot.f90','PW/src/scf_mod.f90','PW/src/wfcinit.f90','PW/src/h_psi.f90',
        'PW/src/vloc_psi_acc.f90','PW/src/stop_run.f90','PW/src/pwscf.f90',
        'Modules/wavefunctions.f90','Modules/becmod.f90','upflib/uspp.f90']
    for rel in files:pins[str(src/rel)]=sha(src/rel)
    lines={rel:[dict(line=i,text=line.strip()) for i,line in enumerate((src/rel).read_text().splitlines(),1)
        if any(s in line for s in ['ALLOCATE(','CALL allocate_','CALL stop_run','CALL close_files','CALL mp_global_end','CALL read_collected_wfc'])]
        for rel in files}
    # A non-authorizing profile: new ELF/source/backend/PP pins, inherited exact
    # science and proposed short roots, no new save copies/jobs/leases created.
    frozen=json.loads((BASE/'static_environment_2026-10-15/frozen_protocol.json').read_text())
    roots={m:str(REPO/'.tmp/r07spc16/jobs'/m) for m in ['unshared','shared']}
    profile=dict(kind='PROSPECTIVE_SOURCE_PINS_ONLY_NOT_EXECUTION_RELEASE',native_kind='R07_PBE16_STATIC_NATIVE_COMPLETION_V2',
        roots=roots,socket_bytes={m:len((p+'/s').encode()) for m,p in roots.items()},
        elf=build['binary'],elf_sha256=build['binary_sha256'],frame=next(p for p in old['source_pins'] if p.endswith('/physical_frame.npz')),
        physical=frozen['profile']['physical'],limits=dict(memory_B=12*(1<<30),swap_B=0,tasks=12,wall_s=600,
            host_floor_B=4*(1<<30),disk_floor_B=10*(1<<30),output_B=14*(1<<30)),
        original_source_pins=frozen['profile']['pins'],new_source_pins={str(p):sha(p) for p in HERE.iterdir() if p.suffix in ['.py','.c','.inc']},
        new_roots_or_copies_or_native_authority_created=False)
    assert all(n<=107 for n in profile['socket_bytes'].values())
    assert all(not Path(p).exists() for p in roots.values())
    (HERE/'prospective_pins.json').write_text(json.dumps(profile,indent=2)+'\n')
    budget=dict(status='NO_GO_COMPLETE_NATIVE_AND_OUTSIDE_OWNER_ENVELOPE_UNKNOWN',
        PP_nkb=nkb,PP_projection_derivation=projectors,per_rank_selected_allocations=rows,
        physical_actions=12,Theta_controls=12,applications_per_member=12,total_pair_applications=24,
        total_pair_packet_payload_B=2*sum(r['exact_packet_B'] for r in rows.values()),
        source_lines=lines,source_and_PP_pins=pins,
        unknown_required_terms=['all simultaneous PW initialization/radial/SOC/FFT descriptor allocations',
            'FFTW/MPI/HDF5/BLAS/allocator heap and collective workspace/timing',
            'saved-wfc import/buffer lifetimes and post-final close_files generations',
            'outside-owner Python/HDF5/readback peak, cgroup inventory and account inode/tree memory',
            'complete output/log/temp/reservation/metadata bound and between-sample bursts'],
        complete_peak_RAM_or_runtime_upper_bound=False,complete_14GiB_disk_bound=False,
        past_1GiB_4s_NOT_a_bound=True,output_account_is_sampled_NOT_continuous_quota=True,
        actual_cgroup_limits_or_MPI_collectives_tested_this_phase=False,resource_experiment_authorized=False)
    (HERE/'resource_audit.json').write_text(json.dumps(budget,indent=2)+'\n')
    # Navigation changes alone, with all preceding handoff text unchanged.
    hand=(BASE/'SUCCESSOR_HANDOFF.md').read_text()
    begin='<!-- PBE_STATIC_COMPLETION_20261016_BEGIN -->\n';end='<!-- PBE_STATIC_COMPLETION_20261016_END -->\n\n'
    assert hand.count(begin)==hand.count(end)==1
    stripped=hand[:hand.index(begin)]+hand[hand.index(end)+len(end):]
    assert stripped==subprocess.check_output(['git','show','37f48db:research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md'],cwd=REPO,text=True)
    allowed={'.gitignore',str((BASE/'state.md').relative_to(REPO)),str((BASE/'SUCCESSOR_HANDOFF.md').relative_to(REPO))}
    prefix=str(HERE.relative_to(REPO))+'/'
    changes=subprocess.check_output(['git','diff','--name-only','37f48db'],cwd=REPO,text=True).splitlines()
    assert all(p in allowed or p.startswith(prefix) for p in changes),changes
    for p in HERE.glob('*.py'):ast.parse(p.read_text())
    result=dict(status='COMPILE_AND_REAL_NON_MPI_COMPONENT_PASS; FULL_PRODUCTION_QUALIFICATION_BLOCKED',
        UTC=datetime.now(timezone.utc).isoformat(),baseline='37f48db',
        old_refused_raw_pins_unchanged=len(raw),old_profile_pins_unchanged=len(frozen['profile']['pins']),
        DFT_dirty_status_and_tracked_diff_unchanged=True,stock_and_all_original_pins_unchanged=True,
        archive_members_compared=len(names),only_archive_difference=changed,
        source_placement_and_native_world_identity_PASS=True,compiled_NATIVE_ELF_NEVER_executed=True,
        production_dispatch_and_reader_gate_exercised_with_real_C_clients=True,
        actual_MPI_systemd_full_owner_loop_NOT_executed=True,
        source_complete_peak_and_time_certificate=False,numerical_2meV_certificate=False,
        native_QE_MPI_SCF=0,new_systemd_units=0,DFT_writes=0,
        full_production_owner_qualified=False,science_observable_unchanged=True,physical_xc=None,
        old_handoff_preserved=True,registry_status_unchanged=True,
        package_sha256={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='verification.json'})
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','archive_members_compared','only_archive_difference','native_QE_MPI_SCF']},indent=2))


if __name__=='__main__':main()
