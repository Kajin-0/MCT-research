"""Read-only source/retained-input audit. No native code/build/service/H action.

Only writes report JSON in this NEW MCT package. Optional --check repeats
assertions without replacing evidence. Landlock call is a VERSION query only.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
from datetime import datetime,timezone
import ctypes
import hashlib
import json
import os
import platform
import subprocess
import sys
import h5py
import numpy as np

HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=HERE.parents[3]
DFT=Path('/home/User/opencode_workspace/DFT');QE=DFT/'.local/qe75_lowram_20261011/q-e'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def source(rel):return (QE/rel).read_text()
def between(text,start,end):return text[text.index(start):text.index(end,text.index(start))]

def run(check=False):
    frozen=json.loads((BASE/'static_environment_2026-10-15/frozen_protocol.json').read_text())
    for p,h in frozen['profile']['pins'].items():assert sha(p)==h,p
    raw=json.loads((BASE/'static_environment_2026-10-15/evidence_manifest.json').read_text())['raw']
    for p,r in raw.items():assert sha(p)==r['sha256'],p
    refused=json.loads((BASE/'pbe_static_lifecycle_2026-10-16/evidence/RESULT.json').read_text())
    assert refused['status']=='REFUSED_ABSORBING' and refused['ranks']=={} and refused['finals']==[]
    protected=json.loads((BASE/'static_environment_2026-10-15/protected_before.json').read_text())
    assert subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)==protected['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'diff','--binary'])).hexdigest()==protected['DFT_tracked_diff_sha256']
    for p,h in protected['files'].items():assert sha(p)==h,p

    read=source('PW/src/read_file_new.f90')
    entry=between(read,'SUBROUTINE read_file_new ( needwf )','END SUBROUTINE read_file_new')
    post=between(read,'SUBROUTINE post_xml_init','END SUBROUTINE post_xml_init')
    branch=between(entry,'IF ( needwf ) THEN','END IF')
    tests={}
    tests['density_entry_calls_post_xml_before_needwf_branch']=entry.index('CALL post_xml_init')<entry.index('IF ( needwf ) THEN')
    tests['allocate_wfc_k_ONLY_in_needwf_branch']=entry.count('CALL allocate_wfc_k()')==1 and 'CALL allocate_wfc_k()' in branch
    # Distinguish the conditional allocation in entry from unconditional post.
    tests['density_entry_no_wfcinit_or_saved_wfc_import']=all(v not in entry+post for v in ['CALL wfcinit','CALL read_collected_wfc'])
    tests['post_no_band_wave_allocation_or_openfil']=all(v not in post for v in ['CALL allocate_wfc_k','CALL allocate_wfc(','CALL openfil','CALL wfcinit','CALL init_wfc'])
    tests['post_rebuilds_density_Hartree_XC_ionic_SOC_coefficients']=all(v in post for v in ['CALL read_scf','CALL rho_g2r','CALL init_vloc','CALL init_us_1','CALL init_tab_beta','CALL struc_fact','CALL setlocal','CALL set_rhoc','CALL v_of_rho','CALL newd()'])
    tests['post_missing_set_vrs_MUST_be_added']='CALL set_vrs' not in post
    tests['needwf_is_overwritten_on_return']='needwf = wfc_is_collected' in entry
    init=source('PW/src/init_run.f90');alloc=source('PW/src/allocate_wfc.f90')
    tests['legacy_init_unconditionally_allocates_and_initializes_waves']=all(s in init for s in ['CALL allocate_wfc_k()','CALL openfil()','CALL wfcinit()']) and 'CALL allocate_wfc( npwx, npol, nbnd )' in alloc
    newd=between(source('PW/src/newd_acc.f90'),'SUBROUTINE newd_nous','END SUBROUTINE newd_nous')
    tests['NC_SOC_newd_is_bare_PP_not_occupied_density']='deeq_nc(ih,jh,na,is) = dvan_so(ih,jh,is,nt)' in newd and 'rho' not in newd.lower()
    hp=source('PW/src/h_psi.f90')
    tests['hpsi_explicit_m_NOT_nbnd']='ONLY : nbnd' not in hp and 'ONLY: nbnd' not in hp and 'psi(lda*npol,m)' in hp
    tests['old_native_probe_and_phase_BOTH_enforce_two_ranks']=all('nproc/=2' in (BASE/'pbe_static_completion_2026-10-16'/f).read_text() for f in ['native_probe.inc','native_phase.inc'])
    tests['stock_stop_run_has_write_delete_side_effects']=all(v in source('PW/src/stop_run.f90') for v in ['CALL seqopn','STATUS = \'DELETE\'','CALL close_files'])
    tests['read_rhog_not_unconditional_Miller_validation']='( gamma_only .NEQV. gamma_only_ )' in source('Modules/io_base.f90')
    assert all(tests.values()),tests

    framepath=next(Path(p) for p in frozen['profile']['pins'] if p.endswith('/physical_frame.npz'))
    with np.load(framepath) as f: G=f['G'].copy();P=f['P'].copy();B=f['B'].copy();T=f['ThetaP'].copy()
    N=len(G);lookup={tuple(g):i for i,g in enumerate(G)}
    minus=np.array([lookup[tuple(-g)] for g in G])
    assert N==21595 and P.shape==(2*N,6)
    assert np.array_equal(T,np.r_[P[N+minus].conj(),-P[minus].conj()])
    S=P.conj().T@P;frame=dict(path=str(framepath),sha256=sha(framepath),N=N,Gram_op=float(np.linalg.norm(S-np.eye(6),2)),
        Theta_explicit_byte_exact=True,rank_change_by_integer_G_lookup_required=True)
    members={};pins={str(framepath):sha(framepath)};pp={}
    for name in ['unshared','shared']:
        save=DFT/'.local/qe75_lowram_20261011/p16e_20261015'/name/'out/r07pbe.save'
        xml=ET.parse(save/'data-file-schema.xml');out=xml.find('output')
        assert out.findtext('dft/functional')=='PBE'
        assert out.findtext('magnetization/noncolin')=='true' and out.findtext('magnetization/spinorbit')=='true'
        assert out.findtext('magnetization/do_magnetization')=='false'
        assert float(out.findtext('basis_set/ecutwfc'))*2==50 and float(out.findtext('basis_set/ecutrho'))*2==200
        assert out.findtext('basis_set/gamma_only')=='false'
        assert int(out.findtext('band_structure/nbnd'))==352 and float(out.findtext('band_structure/nelec'))==288
        assert int(out.findtext('symmetries/nsym'))==({'unshared':24,'shared':4}[name])
        grid=tuple(int(out.find('basis_set/fft_grid').get(v)) for v in ['nr1','nr2','nr3']);assert grid==(80,80,80)
        cell=np.array([[float(x) for x in out.findtext('atomic_structure/cell/'+v).split()] for v in ['a1','a2','a3']]).T
        omega=abs(np.linalg.det(cell))
        with h5py.File(save/'charge-density.hdf5','r') as f:
            mill=np.asarray(f['MillerIndices']);rho=np.asarray(f['rhotot_g']).view(np.complex128)
            assert int(f.attrs['nspin'])==1 and not any(k in f for k in ['m_x','m_y','m_z'])
        assert len(mill)==173631 and len(rho)==len(mill)
        rlookup={tuple(g):i for i,g in enumerate(mill)};rminus=np.array([rlookup[tuple(-g)] for g in mill])
        charge=float(omega*rho[rlookup[(0,0,0)]].real);assert abs(charge-288)<1e-8
        dims=np.array(grid);indices=tuple((mill%dims).T);linear=np.ravel_multi_index(indices,grid)
        assert len(np.unique(linear))==len(mill)
        work=np.zeros(grid,dtype=np.complex128);work[indices]=rho
        real=np.fft.ifftn(work)*np.prod(grid) # QE inverse unnormalized
        recovered=np.fft.fftn(real)/np.prod(grid)
        roundtrip=float(np.max(abs(recovered[indices]-rho)))
        assert roundtrip<1e-12 and np.max(abs(rho-rho[rminus].conj()))<1e-10
        files=['data-file-schema.xml','charge-density.hdf5']+[s+'_sg15_pbe_fr_v12.UPF' for s in ['Hg','Cd','Te']]
        minimal=sum((save/f).stat().st_size for f in files)
        for f in files:pins[str(save/f)]=sha(save/f)
        members[name]=dict(save=str(save),grid=grid,logical_grid_points=int(np.prod(grid)),ngm=len(mill),charge_e=charge,
            charge_error_e=charge-288,rho_Theta_Fourier_max=float(np.max(abs(rho-rho[rminus].conj()))),
            independent_density_FFT_roundtrip_abs=roundtrip,imaginary_rhoR_max=float(np.max(abs(real.imag))),
            rhoR_min=float(np.min(real.real)),minimal_XML_rho_PP_bytes=minimal,
            excluded_member_wfc_bytes=(save/'wfc1.hdf5').stat().st_size,own_EF_NOT_alignment=True,nsym=int(out.findtext('symmetries/nsym')))
        for sp in ['Hg','Cd','Te']:
            tree=ET.parse(save/(sp+'_sg15_pbe_fr_v12.UPF'));header=tree.find('PP_HEADER').attrib
            assert all(header[k]==v for k,v in dict(pseudo_type='NC',relativistic='full',is_ultrasoft='F',is_paw='F',core_correction='F',has_so='T').items())
            assert tree.find('PP_NLCC') is None and tree.find('PP_AUGMENTATION') is None
            ls=[int(v.get('angular_momentum')) for v in tree.findall('./PP_NONLOCAL/*') if v.tag.startswith('PP_BETA')]
            pp[sp]=dict(header=header,NLCC_dataset=False,augmentation_dataset=False,angular_projectors=sum(2*l+1 for l in ls))
    nkb=6*pp['Hg']['angular_projectors']+2*pp['Cd']['angular_projectors']+8*pp['Te']['angular_projectors'];assert nkb==712
    nr=80**3;ng=173631;m=12
    allocations=dict(vkb_B=16*N*nkb,g2kin_B=8*N,trial_plus_four_actions_B=5*16*2*N*m,
        three_scf_objects_main_arrays_B=3*(8*nr*4+16*ng*4),fft_selected_B=8*nr*2+16*ng+16*nr+8*nr*4+16*nr*2,
        local_nc_work_B=16*2*(N+nr),becp_nc_B=16*nkb*2*m,nonlocal_ps_B=16*nkb*2*m,
        excluded_evc_352_B=16*2*N*352,excluded_wfcinit_becp_352_B=16*nkb*2*352)
    packet=128+224+72+24+48+24*N+24*ng+allocations['trial_plus_four_actions_B']+16*ng*4+2*8*nr*4
    probe=128+72+24*N+16*2*N*12
    assert packet==90028704 and probe==8810960
    allocations['listed_conditional_payload_sum_B']=sum(v for k,v in allocations.items() if not k.startswith('excluded_'))

    refs={
      'PW/src/read_file_new.f90':['SUBROUTINE read_file_new ( needwf )','CALL post_xml_init','IF ( needwf ) THEN','CALL allocate_wfc_k()','needwf = wfc_is_collected','SUBROUTINE post_xml_init','CALL read_scf','CALL v_of_rho','CALL newd()'],
      'PW/src/init_run.f90':['CALL allocate_wfc_k()','CALL openfil()','CALL wfcinit()'],
      'PW/src/allocate_wfc.f90':['npwx = n_plane_waves','CALL init_igk','CALL allocate_wfc(','ALLOCATE( vkb','ALLOCATE( g2kin'],
      'PW/src/pw_restart_new.f90':['SUBROUTINE read_xml_file','qexsd_copy_band_structure','qexsd_copy_basis_set','ecutwfc = ecutwfc*e2','qexsd_copy_magnetization'],
      'PW/src/io_rho_xml.f90':['SUBROUTINE read_scf','nspin_=1','CALL read_rhog','rho%of_g(:,nspin_+1:nspin)'],
      'Modules/io_base.f90':['SUBROUTINE read_rhog','readmill =','CALL splitwf'],
      'Modules/recvec_subs.f90':['SUBROUTINE ggen','global_sort = .TRUE.','CALL hpsort_eps','ig_l2g( ngm ) = ng'],
      'PW/src/v_of_rho.f90':['SUBROUTINE v_of_rho','CALL v_xc(','CALL gradcorr','SUBROUTINE v_h','V(G=0)=0','e2 * fpi / tpiba2'],
      'PW/src/gradcorr.f90':['CALL fft_gradient_g2r','CALL xc_gcx','CALL fft_graddot'],
      'PW/src/set_rhoc.f90':['rhog_core(:) = 0.0_DP','IF ( ANY( upf(1:ntyp)%nlcc ) )'],
      'PW/src/setlocal.f90':['vloc(igtongl','v_of_0','CALL rho_g2r'],
      'PW/src/set_vrs.f90':['SUBROUTINE set_vrs','vrs(:,is) = vltot(:) + vr(:,is)','fft_interpolate'],
      'PW/src/newd_acc.f90':['SUBROUTINE newd_nous','dvan_so(ih,jh,is,nt)'],
      'upflib/init_us_1.f90':['subroutine init_us_1','fcoef(ih,kh','dvan_so(ih,jh'],
      'PW/src/init_us_2.f90':['SUBROUTINE init_us_2','CALL init_us_2_acc'],
      'PW/src/h_psi.f90':['SUBROUTINE h_psi(','SUBROUTINE h_psi_(','CALL vloc_psi_nc_acc','CALL calbec','CALL add_vuspsi'],
      'PW/src/vloc_psi_acc.f90':['SUBROUTINE vloc_psi_nc_acc','CALL wave_g2r','CALL wave_r2g'],
      'PW/src/add_vuspsi.f90':['SUBROUTINE add_vuspsi_nc','deeq_nc(ih,jh','CALL ZGEMM'],
      'Modules/mp_world.f90':['CALL MPI_Init','CALL mp_start','CALL mpi_finalize'],
      'Modules/mp_global.f90':['SUBROUTINE mp_startup','CALL mp_start_pools','CALL mp_start_bands'],
      'Modules/fft_wave.f90':['SUBROUTINE wave_r2g','SUBROUTINE wave_g2r'],
      'Modules/fft_rho.f90':['SUBROUTINE rho_g2r_Nspin','CALL invfft'],
      'FFTXlib/src/fft_scalar.FFTW3.f90':['tscale = 1.0_DP / DBLE( nx * ny * nz )'],
      'PW/src/scf_mod.f90':['SUBROUTINE create_scf_type','ALLOCATE( rho%of_r','ALLOCATE( rho%of_g'],
      'PW/src/allocate_fft.f90':['CALL create_scf_type','ALLOCATE( vrs'],
      'PW/src/stop_run.f90':['CALL seqopn','CALL close_files'],
      'Modules/read_pseudo.f90':['pseudo_dir_cur','CALL  read_ps_new']}
    source_map={}
    for rel,needles in refs.items():
        lines=(QE/rel).read_text().splitlines();matches={s:[i for i,l in enumerate(lines,1) if s in l] for s in needles}
        assert all(matches.values()),(rel,matches)
        source_map[rel]=dict(path=str(QE/rel),sha256=sha(QE/rel),lines=matches)
    assert platform.machine()=='x86_64'
    lib=ctypes.CDLL(None,use_errno=True);lib.syscall.restype=ctypes.c_long
    ctypes.set_errno(0);abi=lib.syscall(444,ctypes.c_void_p(),ctypes.c_size_t(0),ctypes.c_uint(1));error=ctypes.get_errno()
    security=dict(kernel=platform.release(),Landlock_VERSION_query=abi,errno=error,VERSION_query_only=True,
        ruleset_created=False,restrict_self_called=False,mount_or_user_namespace_created=False,
        actual_confinement_enforcement_proved=False,actual_singleton_MPI_proved=False,
        unprivileged_userns_clone=Path('/proc/sys/kernel/unprivileged_userns_clone').read_text().strip())
    out=dict(status='CONDITIONAL_SCIENTIFIC_DESIGN_GO_EXECUTION_NO_GO',UTC=datetime.now(timezone.utc).isoformat(),baseline='9a7dafaca4e605b98adf200a6e463a936f748304',
        preferred='QE read_file_new(false), explicit set_vrs and probe-only k/beta setup, ONE native MPI world rank if singleton qualified',
        static_source_assertions=tests,source_map=source_map,input_pins=pins,frame=frame,PP=pp,members=members,
        allocations_CONDITIONAL_selected_payload_NOT_complete_peak=allocations,probe_bytes=probe,
        same_field_set_single_rank_packet_bytes_CONDITIONAL=packet,pair_packet_bytes_CONDITIONAL=2*packet,
        complete_peak_RAM_wall_output_bound=False,security=security,
        old_profile_pins_unchanged=len(frozen['profile']['pins']),old_refused_raw_pins_unchanged=len(raw),
        Gate_A_refusal_unchanged=True,DFT_dirty_and_protected_stock_unchanged=True,
        builds=0,native_QE_MPI_SCF_or_H_actions=0,new_services=0,execution_release=False,physical_xc=None)
    if check:
        old=json.loads((HERE/'audit_result.json').read_text())
        for key in ['static_source_assertions','source_map','input_pins','PP','members','frame','allocations_CONDITIONAL_selected_payload_NOT_complete_peak']:
            assert old[key]==json.loads(json.dumps(out[key])),key
        print('READ_ONLY_RECHECK_PASS_NO_NATIVE_EXECUTION')
    else:
        with (HERE/'audit_result.json').open('x') as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
        print(json.dumps(dict(status=out['status'],members=members,allocations=allocations,security=security),indent=2))

if __name__=='__main__':run(check=sys.argv[1:]==['--check'])
