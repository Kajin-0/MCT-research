"""Independent private init-run observation hook. No initialization changes."""
from pathlib import Path
import hashlib
HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011'

ROUTINE=r'''
#if defined(__QE75_INITIAL_CAPTURE)
SUBROUTINE qe75_capture_initial()
  USE iso_fortran_env, ONLY: int64
  USE qe75_initial_state, ONLY: initial_write
  USE qe75_native_lease, ONLY: native_check
  USE kinds, ONLY: DP
  USE mp_world, ONLY: mpime,nproc,world_comm
  USE mp_pools, ONLY: npool
  USE mp, ONLY: mp_max,mp_barrier
  USE klist, ONLY: nks,nkstot,ngk,igk_k,xk
  USE wvfct, ONLY: npwx,nbnd,et,wg
  USE wavefunctions, ONLY: evc
  USE noncollin_module, ONLY: npol
  USE ions_base, ONLY: nat
  USE uspp, ONLY: okvan
  USE control_flags, ONLY: use_gpu
  USE buffers, ONLY: get_buffer
  USE io_files, ONLY: nwordwfc,iunwfc
  USE fft_base, ONLY: dfftp,dffts
  USE gvect, ONLY: mill
  USE scf, ONLY: rho,vrs
  IMPLICIT NONE
  INTEGER(int64), ALLOCATABLE :: layout(:)
  INTEGER :: ik,code,status,length
  CHARACTER(1024) :: root,path
  CHARACTER(64) :: fingerprint
  CHARACTER(32) :: rank,ks
  CALL native_check()
  code=0
  IF(nproc/=2 .OR. npool/=1 .OR. nat/=2 .OR. npol/=2 .OR. nbnd/=48 .OR. okvan .OR. use_gpu) code=1
  CALL get_environment_variable('QE75_INITIAL_ROOT',root,LENGTH=length,STATUS=status)
  IF(status/=0 .OR. length<1 .OR. length>850) code=1
  CALL get_environment_variable('QE75_PROFILE_SHA256',fingerprint,LENGTH=length,STATUS=status)
  IF(status/=0 .OR. length/=64) code=1
  CALL mp_max(code,world_comm)
  IF(code/=0) CALL errore('initial_capture','fixture/profile/root refused',1)
  ! Actual density/smooth FFT maps and density reciprocal labels. No guessed
  ! q-layout: EXX's descriptor is not initialized at this stage.
  layout=[INT([dfftp%nnr,dfftp%nr1,dfftp%nr2,dfftp%nr3,dfftp%nr1x,dfftp%nr2x,dfftp%nr3x, &
                dfftp%my_nr2p,dfftp%my_nr3p,dfftp%my_i0r2p,dfftp%my_i0r3p, &
                dffts%nnr,dffts%nr1,dffts%nr2,dffts%nr3,npwx,nbnd,nks,nkstot],int64), &
          INT(dfftp%nl,int64),INT(dffts%nl,int64),INT(RESHAPE(mill,[SIZE(mill)]),int64)]
  WRITE(rank,'(I0)') mpime
  DO ik=1,nks
    IF(nks>1) CALL get_buffer(evc,nwordwfc,iunwfc,ik)
    WRITE(ks,'(I0)') ik
    path=TRIM(root)//'/rank'//TRIM(rank)//'.k'//TRIM(ks)//'.initial'
    CALL initial_write(TRIM(path),fingerprint,mpime,ik,npwx,ngk(ik),npol,layout, &
         mill(:,igk_k(1:ngk(ik),ik)),xk(:,ik),evc,et,wg,rho%of_r,rho%of_g,vrs,code)
    ! A recoverable local I/O/shape error is reported by every participant at
    ! the SAME collective, before any rank advances to the next k.
    CALL mp_max(code,world_comm)
    IF(code/=0) CALL errore('initial_capture','collective initial write refused',1)
    CALL mp_barrier(world_comm)
  ENDDO
  DEALLOCATE(layout)
END SUBROUTINE
#endif
'''


def generate(destination):
    original=(ROOT/'q-e/PW/src/init_run.f90').read_text()
    needle='  CALL wfcinit()'
    if original.count(needle)!=1: raise RuntimeError('initial capture anchor changed')
    patched=original.replace(needle,needle+"\n#if defined(__QE75_INITIAL_CAPTURE)\n  CALL qe75_capture_initial()\n#endif",1)+ROUTINE
    Path(destination).write_text(patched)
    return {'original_sha256':hashlib.sha256(original.encode()).hexdigest(),
            'capture_source_sha256':hashlib.sha256(patched.encode()).hexdigest(),
            'writes_existing_initialization':False,'requires_live_native_scope':True}
