"""Generate isolated M5-ready candidate source. Never overwrites old candidates."""
from pathlib import Path
import hashlib
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'native_bridge'))
from patch_native_bridge import replace_once,EXX_ROUTINES

DIAG_ROUTINES=r'''
#if defined(__QE75_M5)
  FUNCTION qdiag_path(k,stage) RESULT(path)
    USE mp_world, ONLY: mpime
    CHARACTER(*), INTENT(IN) :: stage
    INTEGER, INTENT(IN) :: k
    CHARACTER(1024) :: path,root
    CHARACTER(32) :: r,s
    INTEGER :: status,length
    CALL get_environment_variable('QE75_DIAG_ROOT',root,LENGTH=length,STATUS=status)
    IF(status/=0 .OR. length<1 .OR. length>900) CALL errore('qdiag','owned diagnostic root missing',1)
    WRITE(r,'(I0)') mpime
    WRITE(s,'(I0)') k
    path=TRIM(root)//'/rank'//TRIM(r)//'.k'//TRIM(s)//'.'//stage
  END FUNCTION
#endif
'''


def generate(destination):
    destination=Path(destination);destination.mkdir(exist_ok=False)
    prior=json.loads((HERE.parent/'native_bridge/build_results.json').read_text())
    old=Path(prior['source_directory'])
    sources={p.name:p.read_text() for p in old.glob('*.f90')}
    for name,sha in prior['source_sha256'].items():
        if hashlib.sha256(sources[name].encode()).hexdigest()!=sha: raise RuntimeError('M3 source pin changed '+name)
    exx=sources['exx.f90']
    exx=replace_once(exx,'  SAVE\n','''  SAVE
#if defined(__QE75_M5)
  LOGICAL, ALLOCATABLE, PRIVATE :: qdiag_seen(:)
#endif
''')
    # Exact common layout descriptor copied from retained M3 code; made
    # available in BOTH private modes without modifying existing qbridge code.
    layout=EXX_ROUTINES[EXX_ROUTINES.index('  SUBROUTINE qbridge_layout('):EXX_ROUTINES.index('  SUBROUTINE qbridge_capture(')]
    layout=layout.replace('qbridge_layout','qdiag_layout')
    exx=replace_once(exx,'CONTAINS\n','CONTAINS\n'+DIAG_ROUTINES+'\n#if defined(__QE75_M5)\n'+layout+'#endif\n')
    start=exx.index('  SUBROUTINE aceinit_k(');end=exx.index('  END SUBROUTINE aceinit_k',start)
    body=exx[start:end]
    body=replace_once(body,'    USE becmod,               ONLY : bec_type','''#if defined(__QE75_M5)
    USE qe75_native_lease, ONLY: native_check
    USE qe75_diagnostics, ONLY: make_probe,write_ace_before,write_ace_after
    USE iso_fortran_env, ONLY: int64
    USE gvect, ONLY: ig_l2g
    USE klist, ONLY: igk_k,nks
    USE mp_world, ONLY: mpime
    USE mp, ONLY: mp_sum
    USE mp_bands, ONLY: intra_bgrp_comm
#endif
    USE becmod,               ONLY : bec_type''')
    body=replace_once(body,'    LOGICAL :: domat0','''    LOGICAL :: domat0
#if defined(__QE75_M5)
    LOGICAL :: capture,diag_domat
    INTEGER(int64), ALLOCATABLE :: diag_layout(:)
    INTEGER, ALLOCATABLE :: diag_globals(:)
    COMPLEX(DP), ALLOCATABLE :: diag_probe(:,:),diag_direct(:,:),diag_ace(:,:)
    REAL(DP) :: diag_norm,diag_energy
#endif''')
    body=replace_once(body,"    CALL start_clock( 'aceinit' )",'''#if defined(__QE75_M5)
    IF(.NOT.ALLOCATED(qdiag_seen)) THEN
      ALLOCATE(qdiag_seen(nks));qdiag_seen=.FALSE.
    ENDIF
    IF(SIZE(qdiag_seen)/=nks) CALL errore('qdiag','changed k layout',1)
    capture=.NOT.qdiag_seen(current_k)
    IF(capture) THEN
      CALL native_check()
      IF(DoLoc .OR. gamma_only .OR. use_gpu .OR. npol/=2 .OR. nbnd/=48 .OR. nbndproj/=nbnd) &
        CALL errore('qdiag','exact small CPU NC full-band SOC scope required',1)
      ! Full nbnd storage respects vexx_k's explicit max_ibands dummy extent,
      ! even though only the first diagnostic band is acted on.
      ALLOCATE(diag_probe(npwx*npol,nbnd),diag_direct(npwx*npol,nbnd),diag_ace(npwx*npol,1))
      ALLOCATE(diag_globals(nnpw))
      diag_globals=ig_l2g(igk_k(1:nnpw,current_k))
      diag_probe=(0._DP,0._DP);diag_direct=(0._DP,0._DP);diag_ace=(0._DP,0._DP)
      CALL make_probe(npwx,nnpw,npol,current_k,diag_globals,diag_probe(:,1:1))
      diag_norm=SUM(ABS(diag_probe(:,1))**2)
      CALL mp_sum(diag_norm,intra_bgrp_comm)
      IF(diag_norm<=0._DP) CALL errore('qdiag','zero probe',1)
      diag_probe(:,1)=diag_probe(:,1)/SQRT(diag_norm)
      CALL qdiag_layout(diag_layout)
    ENDIF
#endif
    CALL start_clock( 'aceinit' )''')
    body=replace_once(body,'    ! Skip k-points that have exactly zero weight','''#if defined(__QE75_M5)
    IF(capture) THEN
      CALL vexx(npwx,nnpw,1,diag_probe,diag_direct)
      CALL write_ace_before(qdiag_path(current_k,'before'),mpime,current_k,npwx,nnpw,npol, &
        diag_layout,diag_globals,exxe,phi,xitmp,mexx,diag_probe,diag_direct,x_occupation)
    ENDIF
#endif
    ! Skip k-points that have exactly zero weight''')
    body=replace_once(body,'    DEALLOCATE( mexx )','''#if defined(__QE75_M5)
    IF(capture) THEN
      IF(wk(current_k)==0._DP) CALL errore('qdiag','zero-weight ACE not eligible',1)
      diag_domat=domat;domat=.FALSE.
      CALL vexxace_k(nnpw,1,diag_probe,diag_energy,diag_ace)
      domat=diag_domat
      CALL write_ace_after(qdiag_path(current_k,'after'),mpime,current_k,npwx,nnpw,npol, &
        diag_layout,diag_globals,exxe,xitmp,mexx,diag_ace)
      qdiag_seen(current_k)=.TRUE.
      DEALLOCATE(diag_layout,diag_globals,diag_probe,diag_direct,diag_ace)
    ENDIF
#endif
    DEALLOCATE( mexx )''')
    exx=exx[:start]+body+exx[end:];sources['exx.f90']=exx
    run=sources['run_pwscf.f90']
    run=replace_once(run,'  USE kinds,                ONLY : DP','''#if defined(__QE75_M5)
  USE qe75_native_lease, ONLY: native_register
#endif
  USE kinds,                ONLY : DP''')
    run=replace_once(run,'  ions_status = 3','''#if defined(__QE75_M5)
  ! MPI initialization/input reading occurred in the caller. Every real world
  ! rank registers before iosys, XML/state reads or large scientific allocation.
  CALL native_register()
#endif
  ions_status = 3''')
    sources['run_pwscf.f90']=run
    for name,text in sources.items(): (destination/name).write_text(text)
    return {name:hashlib.sha256(text.encode()).hexdigest() for name,text in sources.items()}
