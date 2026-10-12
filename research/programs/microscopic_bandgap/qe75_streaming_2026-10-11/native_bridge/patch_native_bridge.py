"""Patch new private copies only. Does not mutate q-e or stock QE; never runs PW.

Candidate hooks stay fail-closed at the Python coordinator until resource/monitor
handshake and native comparison are qualified. Build success is not that gate.
"""
from pathlib import Path
import hashlib
import shutil
import subprocess

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011'
PIN='770a0b2d12928a67048e2f3da8d10d057e52179e'
BASELINE_SHA={'exx':'87f1f23a0333818e0979c2ca51b6bf00ebd224ee87fe5cc5600f9cd302ae1173',
              'electrons':'48a5928cc5aa63fd64c872f87a950c44ed10f908d829dac561b2ada09af5c8fe'}


def replace_once(text,old,new):
    if text.count(old)!=1: raise ValueError('source anchor not unique: '+old[:100])
    return text.replace(old,new,1)


EXX_ROUTINES=r'''
#if defined(__EXX_QSTREAM)
  SUBROUTINE qbridge_transaction(action)
    USE mp, ONLY: mp_barrier, mp_bcast
    USE mp_images, ONLY: intra_image_comm,nimage
    USE io_global, ONLY: ionode, ionode_id
    CHARACTER(*), INTENT(IN) :: action
    INTEGER :: code,cmdcode
    CHARACTER(256) :: message
    IF(nimage/=1) CALL errore('qbridge_transaction','one image required',1)
    CALL mp_barrier(intra_image_comm)
    code=0
    IF(ionode) THEN
      ! Fixed source path, fixed action, no shell expansion of user paths.
      IF(action/='pre_import' .AND. action/='post_punch' .AND. action/='retire_operator') &
        CALL errore('qbridge_transaction','unknown transaction',1)
      CALL execute_command_line('/usr/bin/python3 /home/User/repos/MCT-research/research/programs/'// &
        'microscopic_bandgap/qe75_streaming_2026-10-11/native_bridge/native_bundle.py '//action, &
        WAIT=.TRUE.,EXITSTAT=code,CMDSTAT=cmdcode,CMDMSG=message)
      IF(cmdcode/=0) code=1
    ENDIF
    CALL mp_bcast(code,ionode_id,intra_image_comm)
    IF(code/=0) CALL errore('qbridge_transaction','checkpoint/guard transaction refused',1)
    CALL mp_barrier(intra_image_comm)
  END SUBROUTINE

  FUNCTION qbridge_fingerprint() RESULT(fingerprint)
    CHARACTER(64) :: fingerprint
    INTEGER :: status,length
    CALL get_environment_variable('QE75_BRIDGE_FINGERPRINT',fingerprint,LENGTH=length,STATUS=status)
    IF(status/=0 .OR. length/=64) CALL errore('qbridge','missing exact profile fingerprint',1)
  END FUNCTION

  FUNCTION qbridge_state_path() RESULT(path)
    USE io_files, ONLY: tmp_dir,prefix
    USE mp_pools, ONLY: me_pool
    CHARACTER(1024) :: path
    CHARACTER(32) :: rank
    WRITE(rank,'(I0)') me_pool
    path=TRIM(tmp_dir)//'/'//TRIM(prefix)//'.exx_state.'//TRIM(rank)
  END FUNCTION

  SUBROUTINE qbridge_request_store(nr,lo,hi,nq)
    USE iso_fortran_env, ONLY: int64
    USE io_files, ONLY: tmp_dir,prefix
    USE mp_pools, ONLY: me_pool
    INTEGER, INTENT(IN) :: nr,lo,hi,nq
    INTEGER :: unit,ios
    CHARACTER(32) :: rank
    CHARACTER(1024) :: path
    WRITE(rank,'(I0)') me_pool
    path=TRIM(tmp_dir)//'/'//TRIM(prefix)//'.stream_request.'//TRIM(rank)
    CALL qs_close(qstore)
    OPEN(NEWUNIT=unit,FILE=TRIM(path),STATUS='new',IOSTAT=ios)
    IF(ios/=0) CALL errore('qbridge','owned stream reservation request collision',1)
    WRITE(unit,'(A)',IOSTAT=ios) qbridge_fingerprint()
    IF(ios/=0) CALL errore('qbridge','reservation fingerprint write failed',1)
    WRITE(unit,'(I0)',IOSTAT=ios) qs_extent(nr,lo,hi,nq)
    IF(ios/=0) CALL errore('qbridge','reservation extent write failed',1)
    CLOSE(unit,IOSTAT=ios)
    IF(ios/=0) CALL errore('qbridge','reservation request close failed',1)
    CALL qbridge_transaction('retire_operator')
  END SUBROUTINE

  SUBROUTINE qbridge_layout(layout)
    USE iso_fortran_env, ONLY: int64
    USE mp_pools, ONLY: me_pool,nproc_pool
    USE klist, ONLY: nks,nkstot,ngk,igk_k,xk
    USE wvfct, ONLY: npwx,nbnd
    USE exx_base, ONLY: nkqs,index_xk,index_sym,index_xkq,xkq_collect
    INTEGER(int64), ALLOCATABLE, INTENT(OUT) :: layout(:)
    INTEGER :: k
    ! Compare actual reconstructed reciprocal/FFT maps, not dimensions alone.
    ! Float geometry/functional/PP/solver are separately fingerprinted by profile.
    layout=[INT([me_pool,nproc_pool,dfftt%nnr*npol,nbnd,nkqs,npwx,npol,nks,nkstot, &
             dfftt%nr1,dfftt%nr2,dfftt%nr3,dfftt%nr1x,dfftt%nr2x,dfftt%nr3x, &
             dfftt%my_nr2p,dfftt%my_nr3p,dfftt%my_i0r2p,dfftt%my_i0r3p,nbndproj],int64), &
             INT(ngk,int64),[(INT(igk_k(1:ngk(k),k),int64),k=1,nks)], &
             INT(index_xk,int64),INT(index_sym,int64), &
             INT(RESHAPE(index_xkq,[SIZE(index_xkq)]),int64),INT(dfftt%nl,int64), &
             INT([dfftt%nproc,dfftt%nproc2,dfftt%nproc3,dfftt%mype,dfftt%mype2,dfftt%mype3],int64), &
             INT(dfftt%nr1p,int64),INT(dfftt%nr1w,int64),INT(dfftt%nr2p,int64),INT(dfftt%nr3p,int64), &
             INT(dfftt%i0r2p,int64),INT(dfftt%i0r3p,int64),INT(dfftt%ir1p,int64),INT(dfftt%ir1w,int64), &
             INT(RESHAPE(dfftt%indp,[SIZE(dfftt%indp)]),int64), &
             INT(RESHAPE(dfftt%indw,[SIZE(dfftt%indw)]),int64), &
             TRANSFER(xk,[0_int64],SIZE(xk)),TRANSFER(xkq_collect,[0_int64],SIZE(xkq_collect)), &
             TRANSFER(gt,[0_int64],SIZE(gt)),TRANSFER(ggt,[0_int64],SIZE(ggt))]
  END SUBROUTINE

  SUBROUTINE qbridge_capture(iter,mode,tr2,tr2_final,exxen)
    USE iso_fortran_env, ONLY: int64
    USE wvfct, ONLY: wg,et
    USE control_flags, ONLY: ethr
    USE exx_checkpoint_state, ONLY: bridge_write,bridge_outer
    INTEGER, INTENT(IN) :: iter,mode
    REAL(DP), INTENT(IN) :: tr2,tr2_final,exxen
    INTEGER(int64), ALLOCATABLE :: layout(:)
    TYPE(bridge_outer) :: state
    IF(.NOT.ALLOCATED(xi) .OR. .NOT.ALLOCATED(x_occupation)) &
      CALL errore('qbridge_capture','old operator state absent',1)
    CALL qbridge_layout(layout)
    state%iter=iter;state%mode=mode
    state%scalar=[tr2,dexx,exxen,fock0,fock1,fock2,fock3,tr2_final,ethr]
    CALL bridge_write(TRIM(qbridge_state_path()),qbridge_fingerprint(),layout,state,x_occupation,wg,et,xi)
    DEALLOCATE(layout)
    ! No commit here: native punch has not completed. All readers retain qstore.
  END SUBROUTINE

  SUBROUTINE qbridge_restore(DoLoc,iter,tr2,tr2_final,exxen)
    USE control_flags, ONLY: nexxiter,ethr
    LOGICAL, INTENT(IN) :: DoLoc
    INTEGER, INTENT(OUT) :: iter
    REAL(DP), INTENT(OUT) :: tr2,tr2_final,exxen
    INTEGER :: unit,ios
    qbridge_import=.TRUE.
    CALL exxinit(DoLoc)
    qbridge_import=.FALSE.
    iter=qbridge_restored%iter
    IF(iter>nexxiter) CALL errore('qbridge_restore','outer count incompatible with input',1)
    tr2=qbridge_restored%scalar(1);dexx=qbridge_restored%scalar(2)
    exxen=qbridge_restored%scalar(3);fock0=qbridge_restored%scalar(4)
    fock1=qbridge_restored%scalar(5);fock2=qbridge_restored%scalar(6)
    fock3=qbridge_restored%scalar(7);tr2_final=qbridge_restored%scalar(8)
    ethr=qbridge_restored%scalar(9)
    domat=.FALSE.
    ! Early global import consumed the manifest before any native write. The
    ! now-restored rank sidecar must not collide with a subsequent capture.
    OPEN(NEWUNIT=unit,FILE=TRIM(qbridge_state_path()),STATUS='old',ACTION='read',IOSTAT=ios)
    IF(ios/=0) CALL errore('qbridge_restore','owned sidecar retirement open failed',1)
    CLOSE(unit,STATUS='delete',IOSTAT=ios)
    IF(ios/=0) CALL errore('qbridge_restore','owned sidecar retirement failed',1)
  END SUBROUTINE
#endif
'''


def build_sources(destination):
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/'q-e',text=True).strip()!=PIN:
        raise ValueError('QE source pin mismatch')
    for name,expected in BASELINE_SHA.items():
      if hashlib.sha256((ROOT/'q-e/PW/src'/(name+'.f90')).read_bytes()).hexdigest()!=expected:
        raise ValueError('previous candidate drift: '+name)
    destination=Path(destination).absolute()
    if destination.parent!=ROOT/'native_bridge': raise ValueError('private native_bridge output only')
    if destination.exists():
      if any(destination.iterdir()): raise ValueError('refusing existing populated output')
    else: destination.mkdir()
    e=(ROOT/'q-e/PW/src/exx.f90').read_text()
    e=replace_once(e,'qs_seal, qs_load, qs_close',
      'qs_seal, qs_load, qs_close, qs_restore_readonly, qs_begin_reserved, qs_extent')
    e=replace_once(e,'  TYPE(exx_qstore), PRIVATE :: qstore',
      '  TYPE(exx_qstore), PRIVATE :: qstore\n  LOGICAL, PRIVATE :: qbridge_import=.FALSE.\n  TYPE(bridge_outer), PRIVATE :: qbridge_restored')
    e=replace_once(e,'\n  USE noncollin_module,     ONLY : noncolin, npol',
      '\n#if defined(__EXX_QSTREAM)\n  USE exx_checkpoint_state, ONLY: bridge_outer,bridge_pending,bridge_read\n#endif\n  USE noncollin_module,     ONLY : noncolin, npol')
    e=replace_once(e,' CONTAINS\n', ' CONTAINS\n'+EXX_ROUTINES)
    e=replace_once(e,'#if defined(__EXX_QSTREAM)\n    CALL qs_close(qstore)\n#endif',
      '#if defined(__EXX_QSTREAM)\n    CALL qs_close(qstore,keep=bridge_pending)\n#endif')
    e=replace_once(e,'    USE control_flags,        ONLY : lscf, restart, tstress, tprnfor',
      '    USE control_flags,        ONLY : lscf, restart, tstress, tprnfor, io_level, sic, lmd\n'+
      '    USE ldaU, ONLY: lda_plus_u\n    USE rism_module, ONLY: lrism\n'+
      '    USE bp, ONLY: lelfield\n    USE extfield, ONLY: tefield\n'+
      '    USE cellmd, ONLY: lmovecell\n    USE iso_fortran_env, ONLY: int64')
    e=replace_once(e,'    USE cellmd, ONLY: lmovecell',
      '    USE cellmd, ONLY: lmovecell\n    USE mp_bands, ONLY: nbgrp')
    e=replace_once(e,'    CHARACTER(32) :: qstream_rank',
      '    CHARACTER(32) :: qstream_rank\n    INTEGER(int64), ALLOCATABLE :: qbridge_actual_layout(:)')
    e=replace_once(e,'    USE buffers,              ONLY : get_buffer\n    USE wvfct,                ONLY : nbnd, npwx, wg, current_k',
      '    USE buffers,              ONLY : get_buffer\n    USE wvfct,                ONLY : nbnd, npwx, wg, et, current_k')
    e=replace_once(e,'IF (.NOT.lscf .OR. PRESENT(nbndproj_) .OR. restart)',
      'IF (.NOT.lscf .OR. PRESENT(nbndproj_) .OR. (restart .AND. .NOT.qbridge_import .AND. .NOT.ALLOCATED(exxbuff)))')
    e=replace_once(e,"'qstream requires fresh SCF; restart/non-SCF unsupported'",
      "'qstream requires SCF and qualified old-operator restore'")
    e=replace_once(e,'    CALL start_clock (\'exxinit\')',
      '#if defined(__EXX_QSTREAM)\n'+
      '    IF(io_level<0 .OR. nbgrp/=1 .OR. lda_plus_u .OR. lrism .OR. sic .OR. lmd .OR. lmovecell .OR. lelfield .OR. tefield) &\n'+
      "      CALL errore('exxinit','bridge excludes incomplete-I/O/additional-state modes',1)\n"+
      '#endif\n    CALL start_clock (\'exxinit\')')
    anchor='    ALLOCATE( occ(nbnd,nks) )'
    e=replace_once(e,anchor,'''#if defined(__EXX_QSTREAM)
    IF(qbridge_import) THEN
      ! aceinit0 already allocated/read xi. Restore the exact rank packet;
      ! CURRENT wg/et NEVER determine old exchange occupations/projectors.
      IF(.NOT.ALLOCATED(xi)) CALL errore('exxinit','native old ACE absent',1)
      nbndproj=nbnd
      CALL qbridge_layout(qbridge_actual_layout)
      CALL bridge_read(TRIM(qbridge_state_path()),qbridge_fingerprint(),qbridge_actual_layout, &
                       qbridge_restored,x_occupation,wg,et,xi)
      DEALLOCATE(qbridge_actual_layout)
    ELSE
#endif
'''+anchor)
    e=replace_once(e,'    DEALLOCATE( occ )','    DEALLOCATE( occ )\n#if defined(__EXX_QSTREAM)\n    ENDIF\n#endif')
    begin='      CALL qs_begin(qstore,TRIM(qstream_path),nrxxs*npol,ibnd_buff_start, &\n                    ibnd_buff_start+max_buff_bands_per_egrp-1,nkqs)'
    e=replace_once(e,begin,'''      IF(qbridge_import) THEN
        CALL qs_restore_readonly(qstore,TRIM(qstream_path),nrxxs*npol,ibnd_buff_start, &
                      ibnd_buff_start+max_buff_bands_per_egrp-1,nkqs)
      ELSE
        CALL qbridge_request_store(nrxxs*npol,ibnd_buff_start, &
                                  ibnd_buff_start+max_buff_bands_per_egrp-1,nkqs)
'''+begin.replace('CALL qs_begin(', 'CALL qs_begin_reserved(')+'''
      ENDIF''')
    # Jump past entire source producer and seal, but through common temporary
    # deallocation, US/PAW exclusions, representation reset and clock cleanup.
    e=replace_once(e,'    !assign buffer','''#if defined(__EXX_QSTREAM)
    IF(qbridge_import) GOTO 975
#endif
    !assign buffer''')
    e=replace_once(e,'    DEALLOCATE( psic_exx )','975 CONTINUE\n    DEALLOCATE( psic_exx )')
    e=replace_once(e,'    CALL qs_seal(qstore)','    IF(.NOT.qbridge_import) CALL qs_seal(qstore)')
    (destination/'exx.f90').write_text(e)

    e=(ROOT/'q-e/PW/src/electrons.f90').read_text()
    # Both electrons and electrons_scf have this USE: alter only outer routine.
    if e.count('  USE kinds,                ONLY : DP')!=2: raise ValueError('electrons preamble drift')
    e=e.replace('  USE kinds,                ONLY : DP','''#if defined(__EXX_QSTREAM)
  USE exx, ONLY: qbridge_capture,qbridge_restore
#endif
  USE kinds,                ONLY : DP''',1)
    old='''#if defined(__EXX_QSTREAM)
  IF (restart .AND. xclib_dft_is('hybrid')) &
    CALL errore('electrons','qstream EXX restart import is not implemented',1)
#endif
  IF ( restart ) THEN'''
    new='''#if defined(__EXX_QSTREAM)
  IF(restart .AND. xclib_dft_is('hybrid')) THEN
    CALL stop_exx()
    CALL qbridge_restore(DoLoc,iter,tr2,tr2_final,exxen)
    first=.FALSE.
    CALL v_of_rho(rho,rho_core,rhog_core,ehart,etxc,vtxc,eth,etotefield,charge,v)
    CALL set_vrs(vrs,vltot,v%of_r,kedtau,v%kin_r,dfftp%nnr,nspin,doublegrid)
  ENDIF
#else
  IF ( restart ) THEN'''
    e=replace_once(e,old,new)
    e=replace_once(e,'  !  ... energy calculation of neutral case',
      '#endif\n  !  ... energy calculation of neutral case')
    # Replace full old export block, avoiding stock single-plane restart_exx.
    first=e.index('        IF ( .NOT. first) THEN')
    end=e.index('        ENDIF\n        RETURN',first)
    body=e[first:end+len('        ENDIF')]
    native=body.replace('''#if defined(__EXX_QSTREAM)
           ! Never mislabel a single cached q plane as a full stock checkpoint.
           CALL errore('electrons','qstream EXX checkpoint export is not implemented; run unaccepted',1)
#endif
''','')
    e=e[:first]+'''        IF (.NOT.first) THEN
#if defined(__EXX_QSTREAM)
          CALL qbridge_capture(iter-1,1,tr2,tr2_final,exxen)
#else
'''+native.replace('        IF ( .NOT. first) THEN\n','').rsplit('        ENDIF',1)[0]+'''#endif
        ENDIF'''+e[end+len('        ENDIF'):]
    anchor="        CALL seqopn (iunres, 'restart_e', 'formatted', exst)"
    start=e.index(anchor,e.index("'Calculation (EXX) stopped after iteration #")) if "'Calculation (EXX) stopped after iteration #" in e else -1
    if start<0: start=e.index(anchor,e.index('IF ( check_stop_now() .or. (iter.ge.nexxiter) )'))
    end=e.index("        CLOSE (unit=iunres, status='keep')",start)+len("        CLOSE (unit=iunres, status='keep')")
    e=e[:start]+'''#if defined(__EXX_QSTREAM)
        CALL qbridge_capture(iter,2,tr2,tr2_final,exxen)
#else
'''+e[start:end]+'''\n#endif'''+e[end:]
    anchor='  n_scf_steps = iter\n  scf_error = dr2'
    e=replace_once(e,anchor,anchor+'''
#if defined(__EXX_QSTREAM)
  ! Natural iteration-limit exit: native stock lacks restart_scf here.
  ! Earlier partial-k/top-loop stops jump to label 10 and retain their own
  ! already-written counter (iter-1 or iter respectively).
  IF(.NOT.conv_elec) CALL save_in_electrons(iter,dr2,ethr,et)
#endif''')
    (destination/'electrons.f90').write_text(e)

    for name in ['run_pwscf','punch']:
      e=subprocess.check_output(['git','show',f'{PIN}:PW/src/{name}.f90'],cwd=ROOT/'q-e',text=True)
      e=replace_once(e,'  USE kinds,                ONLY : DP' if name=='run_pwscf' else '  USE io_global,            ONLY : stdout, ionode',
        '#if defined(__EXX_QSTREAM)\n  USE exx, ONLY: qbridge_transaction\n'+
        ('  USE exx_checkpoint_state, ONLY: bridge_pending\n' if name=='punch' else '')+
        '#endif\n'+('  USE kinds,                ONLY : DP' if name=='run_pwscf' else '  USE io_global,            ONLY : stdout, ionode'))
      if name=='run_pwscf':
        e=replace_once(e,'  CALL iosys()','''#if defined(__EXX_QSTREAM)
  ! Verify+retire the full native snapshot before iosys/setup/init_run can
  ! read or rewrite XML, density, waves or old ACE. Currently runtime refuses.
  CALL qbridge_transaction('pre_import')
#endif
  CALL iosys()''')
      else:
        e=replace_once(e,'  IF ( la2F ) CALL a2Fsave()','''  IF ( la2F ) CALL a2Fsave()
#if defined(__EXX_QSTREAM)
  IF(bridge_pending) THEN
    IF(TRIM(what)/='all' .OR. io_level<0) CALL errore('punch','incomplete native checkpoint',1)
    ! This all-rank transaction runs only AFTER schema, density, collected
    ! current waves, old ACE and other native punch operations have finished.
    CALL qbridge_transaction('post_punch')
  ENDIF
#endif''')
      (destination/(name+'.f90')).write_text(e)
    e=subprocess.check_output(['git','show',f'{PIN}:PW/src/wfcinit.f90'],cwd=ROOT/'q-e',text=True)
    e=replace_once(e,'  USE control_flags,        ONLY : io_level, lscf',
      '  USE control_flags,        ONLY : io_level, lscf, restart')
    e=replace_once(e,"  IF ( TRIM(starting_wfc) == 'file') THEN",'''#if defined(__EXX_QSTREAM)
  IF(restart .AND. TRIM(starting_wfc)/='file') &
    CALL errore('wfcinit','bridge refuses replacement starting waves',1)
#endif
  IF ( TRIM(starting_wfc) == 'file') THEN''')
    e=replace_once(e,'     IF ( twfcollect_file ) THEN','''#if defined(__EXX_QSTREAM)
     IF(restart .AND. .NOT.twfcollect_file) CALL errore('wfcinit','bridge requires collected current waves',1)
#endif
     IF ( twfcollect_file ) THEN''')
    e=replace_once(e,'10      IF ( ierr /= 0 ) THEN','''10      IF ( ierr /= 0 ) THEN
#if defined(__EXX_QSTREAM)
           IF(restart) CALL errore('wfcinit','bridge refuses atomic/random fallback on import',1)
#endif''')
    (destination/'wfcinit.f90').write_text(e)
    shutil.copy2(HERE/'exx_checkpoint_state.f90',destination/'exx_checkpoint_state.f90')
    q=(HERE.parent/'checkpoint_phase/exx_qstream_v2.f90').read_text()
    q=replace_once(q,'qs_extent, qs_restore_readonly','qs_extent, qs_restore_readonly, qs_begin_reserved')
    q=replace_once(q,'END MODULE', (HERE/'reserved_store.f90.inc').read_text()+'\nEND MODULE')
    (destination/'exx_qstream.f90').write_text(q)
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in destination.iterdir()}


if __name__=='__main__':
    import sys,json
    print(json.dumps(build_sources(Path(sys.argv[1])),indent=2))
