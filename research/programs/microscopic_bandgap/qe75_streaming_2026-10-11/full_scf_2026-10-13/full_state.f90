! GPL-2.0-or-later. Observation only; preserves evc and never changes SCF math.
MODULE qe75_full_state
 USE kinds, ONLY:DP
 IMPLICIT NONE
 INTEGER,SAVE::last_outer=0
CONTAINS
 SUBROUTINE full_observe(iter,stage,tr2_final)
  USE iso_fortran_env, ONLY:int64
  USE qe75_initial_state, ONLY:initial_write
  USE qe75_native_lease, ONLY:native_check,native_phase
  USE mp_world, ONLY:mpime,world_comm
  USE mp, ONLY:mp_max,mp_barrier
  USE klist, ONLY:nks,nkstot,ngk,igk_k,xk
  USE wvfct, ONLY:npwx,nbnd,et,wg
  USE wavefunctions, ONLY:evc
  USE noncollin_module, ONLY:npol
  USE buffers, ONLY:get_buffer
  USE io_files, ONLY:nwordwfc,iunwfc
  USE fft_base, ONLY:dfftp,dffts
  USE gvect, ONLY:mill
  USE scf, ONLY:rho,vrs
  USE ener, ONLY:etot,hwf_energy
  USE exx, ONLY:fock0,fock1,fock2,fock3,dexx
  USE control_flags, ONLY:tr2,ethr,conv_elec
  INTEGER,INTENT(IN)::iter,stage
  REAL(DP),INTENT(IN)::tr2_final
  INTEGER(int64),ALLOCATABLE::layout(:)
  COMPLEX(DP),ALLOCATABLE::saved(:,:)
  INTEGER::ik,code,status,length,u,i,event
  CHARACTER(1024)::root,path
  CHARACTER(64)::fingerprint
  CHARACTER(32)::r,s,k,t
  REAL(DP)::values(10)
  CALL native_check()
  IF(iter>0) last_outer=iter
  event=last_outer
  CALL get_environment_variable('QE75_TRAJECTORY_ROOT',root,LENGTH=length,STATUS=status)
  IF(status/=0 .OR. length<1 .OR. length>850) CALL errore('full_observe','owned trajectory root',1)
  CALL get_environment_variable('QE75_COMMON_INPUT_SHA256',fingerprint,LENGTH=length,STATUS=status)
  IF(status/=0 .OR. length/=64) CALL errore('full_observe','common physical identity',1)
  layout=[INT([dfftp%nnr,dfftp%nr1,dfftp%nr2,dfftp%nr3,dfftp%nr1x,dfftp%nr2x,dfftp%nr3x, &
                dfftp%my_nr2p,dfftp%my_nr3p,dfftp%my_i0r2p,dfftp%my_i0r3p, &
                dffts%nnr,dffts%nr1,dffts%nr2,dffts%nr3,npwx,nbnd,nks,nkstot],int64), &
          INT(dfftp%nl,int64),INT(dffts%nl,int64),INT(RESHAPE(mill,[SIZE(mill)]),int64)]
  ALLOCATE(saved(SIZE(evc,1),SIZE(evc,2)));saved=evc
  WRITE(r,'(I0)') mpime;WRITE(s,'(I0)') event;WRITE(t,'(I0)') stage
  DO ik=1,nks
   IF(nks>1) CALL get_buffer(evc,nwordwfc,iunwfc,ik)
   WRITE(k,'(I0)') ik
   path=TRIM(root)//'/rank'//TRIM(r)//'.step'//TRIM(s)//'.stage'//TRIM(t)//'.k'//TRIM(k)//'.state'
   CALL initial_write(TRIM(path),fingerprint,mpime,ik,npwx,ngk(ik),npol,layout, &
      mill(:,igk_k(1:ngk(ik),ik)),xk(:,ik),evc,et,wg,rho%of_r,rho%of_g,vrs,code)
   CALL mp_max(code,world_comm)
   IF(code/=0) CALL errore('full_observe','collective state write',1)
   CALL mp_barrier(world_comm)
  ENDDO
  evc=saved;DEALLOCATE(saved,layout)
  values=[etot,hwf_energy,fock0,fock1,fock2,fock3,dexx,tr2,ethr,tr2_final]
  path=TRIM(root)//'/rank'//TRIM(r)//'.step'//TRIM(s)//'.stage'//TRIM(t)//'.scalars'
  OPEN(NEWUNIT=u,FILE=TRIM(path),STATUS='new',ACTION='write',IOSTAT=code)
  IF(code/=0) CALL errore('full_observe','scalar open',1)
  WRITE(u,'(A)') fingerprint
  WRITE(u,'(4(I0,1X))') mpime,event,stage,MERGE(1,0,conv_elec)
  DO i=1,SIZE(values)
   WRITE(u,'(ES26.17E3)') values(i)
  ENDDO
  CLOSE(u,IOSTAT=code)
  CALL mp_max(code,world_comm)
  IF(code/=0) CALL errore('full_observe','scalar close',1)
  CALL mp_barrier(world_comm)
  IF(stage==1) CALL native_phase(8)
  IF(stage==2) CALL native_phase(10)
 END SUBROUTINE
END MODULE
