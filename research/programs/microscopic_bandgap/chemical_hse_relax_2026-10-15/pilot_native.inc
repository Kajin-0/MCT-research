! Exactly two source updates: preliminary and one hybrid inner solve.
  SUBROUTINE pilot_begin()
    USE control_flags,ONLY:conv_elec,restart
    IF(.NOT.conv_elec.OR.restart)CALL errore('pilot','unconverged/restarted source refused',1)
    pilot_cycle=pilot_cycle+1
    IF(pilot_cycle<1.OR.pilot_cycle>2)CALL errore('pilot','more than one relaxation refused',1)
  END SUBROUTINE

! Diagnostic-only additions to pristine exx. GPL-2.0-or-later, QE conventions.
  SUBROUTINE pilot_guard()
    USE ions_base, ONLY:nat
    USE wvfct, ONLY:nbnd,current_k
    USE klist, ONLY:nks,nelec,xk
    USE uspp, ONLY:okvan
    USE mp_world, ONLY:nproc,mpime
    USE xc_lib, ONLY:get_screening_parameter
    INTEGER::status
    CHARACTER(1024)::root
    CALL get_environment_variable('R07_FIRSTACE_ROOT',root,STATUS=status)
    IF(status/=0.OR.INDEX(TRIM(root),'/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8r_20261015/')/=1) &
      CALL errore('pilot','private owned root absent',1)
    IF(nat/=8.OR.nbnd/=176.OR.npol/=2.OR.nks/=1.OR.nproc/=2.OR.okvan.OR.gamma_only.OR.use_gpu) &
      CALL errore('pilot','unsupported fixed native domain',1)
    IF(ABS(nelec-144._DP)>1.e-12_DP.OR.MAXVAL(ABS(xk(:,1)))>1.e-12_DP) CALL errore('pilot','source charge/k domain',1)
  END SUBROUTINE

  SUBROUTINE pilot_check_io(status)
    USE mp,ONLY:mp_sum
    USE mp_bands,ONLY:intra_bgrp_comm
    INTEGER,INTENT(IN)::status
    INTEGER::bad
    bad=0
    IF(status/=0)bad=1
    CALL mp_sum(bad,intra_bgrp_comm)
    IF(bad/=0)CALL errore('pilot','collective diagnostic I/O refusal',1)
  END SUBROUTINE

  SUBROUTINE pilot_open(stage,unit)
    USE mp_world,ONLY:mpime
    CHARACTER(*),INTENT(IN)::stage
    INTEGER,INTENT(OUT)::unit
    INTEGER::status
    CHARACTER(1024)::root
    CHARACTER(16)::rank,cycle
    CALL pilot_guard()
    CALL get_environment_variable('R07_FIRSTACE_ROOT',root)
    WRITE(rank,'(I0)')mpime
    WRITE(cycle,'(I0)')pilot_cycle
    OPEN(NEWUNIT=unit,FILE=TRIM(root)//'/pilot/c'//TRIM(cycle)//'_'//stage//'.rank'//TRIM(rank),STATUS='NEW', &
      ACCESS='STREAM',FORM='UNFORMATTED',ACTION='WRITE',IOSTAT=status)
    CALL pilot_check_io(status)
  END SUBROUTINE

  SUBROUTINE pilot_header(unit,stage)
    USE wvfct,ONLY:npwx,nbnd,current_k
    USE klist,ONLY:ngk,nks,nelec
    USE mp_world,ONLY:mpime,nproc
    INTEGER,INTENT(IN)::unit,stage
    INTEGER(8)::h(16)
    h=[7025101408_8,1_8,INT(stage,8),INT(mpime,8),INT(getpid(),8),INT(npwx,8), &
      INT(ngk(current_k),8),INT(nbnd,8),INT(npol,8),INT(current_k,8),INT(nks,8), &
      INT(nproc,8),INT(nelec,8),INT(pilot_cycle,8),0_8,0_8]
    WRITE(unit)h
  END SUBROUTINE

  SUBROUTINE pilot_make_probe()
    USE wvfct,ONLY:npwx,current_k
    USE klist,ONLY:ngk,igk_k
    USE gvect,ONLY:mill
    USE cell_base,ONLY:bg,tpiba
    USE mp,ONLY:mp_sum
    USE mp_bands,ONLY:intra_bgrp_comm
    INTEGER::unit,status,ng,ig,j,b
    INTEGER(8)::h(4)
    INTEGER(8),ALLOCATABLE::labels(:,:)
    INTEGER,ALLOCATABLE::matched(:)
    COMPLEX(DP),ALLOCATABLE::source(:,:)
    COMPLEX(DP)::gram(6,6)
    REAL(DP)::Bsource(3,3),ksource(3)
    CHARACTER(1024)::root
    IF(ALLOCATED(pilot_probe))RETURN
    CALL pilot_guard()
    CALL get_environment_variable('R07_FIRSTACE_ROOT',root)
    OPEN(NEWUNIT=unit,FILE=TRIM(root)//'/reference.bin',ACCESS='STREAM',FORM='UNFORMATTED', &
      STATUS='OLD',ACTION='READ',IOSTAT=status)
    CALL pilot_check_io(status)
    READ(unit,IOSTAT=status)h
    CALL pilot_check_io(status)
    IF(h(1)/=70251406_8.OR.h(2)/=7809_8.OR.h(3)/=6_8.OR.h(4)/=1_8)CALL errore('pilot','reference header refusal',1)
    ng=INT(h(2));ALLOCATE(labels(3,ng),matched(ng),source(2*ng,6))
    READ(unit,IOSTAT=status)Bsource,ksource,labels,source
    CALL pilot_check_io(status)
    CLOSE(unit)
    IF(MAXVAL(ABS(Bsource-bg*tpiba))>1.e-12_DP.OR.MAXVAL(ABS(ksource))>1.e-12_DP)CALL errore('pilot','physical reciprocal frame mismatch',1)
    ALLOCATE(pilot_probe(npwx*2,6));pilot_probe=(0._DP,0._DP);matched=0
    DO j=1,ng
      DO ig=1,ngk(current_k)
        IF(ALL(INT(mill(:,igk_k(ig,current_k)),8)==labels(:,j)))THEN
          matched(j)=matched(j)+1
          pilot_probe(ig,:)=source(j,:)
          pilot_probe(ig+npwx,:)=source(j+ng,:)
        ENDIF
      ENDDO
    ENDDO
    CALL mp_sum(matched,intra_bgrp_comm)
    IF(ANY(matched/=1))CALL errore('pilot','source reciprocal label coverage refusal',1)
    gram=MATMUL(CONJG(TRANSPOSE(pilot_probe)),pilot_probe)
    CALL mp_sum(gram,intra_bgrp_comm)
    DO b=1,6
      gram(b,b)=gram(b,b)-1._DP
    ENDDO
    IF(MAXVAL(ABS(gram))>1.e-8_DP)CALL errore('pilot','fixed reference Gram refusal',1)
    DEALLOCATE(labels,matched,source)
  END SUBROUTINE

  SUBROUTINE pilot_local(stage)
    USE wvfct,ONLY:npwx,current_k
    USE klist,ONLY:ngk
    USE scf,ONLY:vrs,rho
    USE gvect,ONLY:mill
    USE fft_base,ONLY:dfftp
    INTEGER,INTENT(IN)::stage
    INTEGER::unit
    INTEGER(8)::dimensions(8)
    COMPLEX(DP),ALLOCATABLE::action(:,:)
    CALL pilot_make_probe()
    ALLOCATE(action(npwx*2,6));action=(0._DP,0._DP)
    CALL vloc_psi_nc_acc(npwx,ngk(current_k),6,pilot_probe,vrs,action)
    IF(stage==0)THEN
      CALL pilot_open('local0',unit)
    ELSE
      CALL pilot_open('local1',unit)
    ENDIF
    CALL pilot_header(unit,stage)
    dimensions=[INT(SIZE(rho%of_r,1),8),INT(SIZE(rho%of_r,2),8), &
      INT(SIZE(rho%of_g,1),8),INT(SIZE(rho%of_g,2),8),INT(SIZE(vrs,1),8),INT(dfftp%nr1,8),INT(dfftp%nr2,8),INT(dfftp%nr3,8)]
    WRITE(unit)dimensions,INT(mill(:,1:SIZE(rho%of_g,1)),8),pilot_probe,action,rho%of_r,rho%of_g,vrs
    CLOSE(unit)
  END SUBROUTINE

  SUBROUTINE pilot_before(nnpw,nbnd,phi,action,gram,energy)
    USE wvfct,ONLY:npwx,et,wg,current_k
    USE klist,ONLY:igk_k,xk,wk
    USE gvect,ONLY:mill
    USE cell_base,ONLY:bg,tpiba
    INTEGER,INTENT(IN)::nnpw,nbnd
    COMPLEX(DP),INTENT(IN)::phi(npwx*npol,nbnd),action(npwx*npol,nbnd),gram(nbndproj,nbndproj)
    REAL(DP),INTENT(IN)::energy
    INTEGER::unit
    INTEGER(8)::extent(10)
    CALL pilot_open('before',unit)
    CALL pilot_header(unit,2)
    extent=[INT(dfftt%nr1,8),INT(dfftt%nr2,8),INT(dfftt%nr3,8),INT(dfftt%nnr,8), &
      INT(SIZE(exxbuff,1),8),INT(SIZE(exxbuff,2),8),INT(SIZE(exxbuff,3),8),INT(x_nbnd_occ,8),INT(nbndproj,8),0_8]
    WRITE(unit)extent,bg*tpiba,xk(:,current_k),wk(current_k),exxalfa,ecutfock,energy
    WRITE(unit)INT(mill(:,igk_k(1:nnpw,current_k)),8),et(:,current_k),wg(:,current_k)
    WRITE(unit)phi,action,gram
    CLOSE(unit)
  END SUBROUTINE

  SUBROUTINE pilot_after(nnpw,nbnd,phi,projectors,becpsi)
    USE becmod,ONLY:bec_type
    USE wvfct,ONLY:npwx,current_k
    INTEGER,INTENT(IN)::nnpw,nbnd
    COMPLEX(DP),INTENT(IN)::phi(npwx*npol,nbnd),projectors(npwx*npol,nbndproj)
    TYPE(bec_type),INTENT(IN)::becpsi
    COMPLEX(DP),ALLOCATABLE::action(:,:),gram(:,:),reference_action(:,:)
    REAL(DP)::energy
    INTEGER::unit
    LOGICAL::old_domat
    ALLOCATE(action(npwx*npol,nbnd),gram(nbnd,nbnd),reference_action(npwx*2,6))
    action=(0._DP,0._DP);old_domat=domat;domat=.FALSE.
    CALL vexxace_k(nnpw,nbnd,phi,energy,action)
    domat=old_domat
    CALL matcalc_k('pilotACE',.TRUE.,0,current_k,npwx*npol,nbnd,nbnd,phi,action,gram,energy)
    reference_action=(0._DP,0._DP)
    CALL vexx(npwx,nnpw,6,pilot_probe,reference_action,becpsi)
    CALL pilot_open('after',unit)
    CALL pilot_header(unit,3)
    WRITE(unit)energy,projectors,action,gram,pilot_probe,reference_action
    CLOSE(unit)
    DEALLOCATE(action,gram,reference_action)
  END SUBROUTINE

  SUBROUTINE pilot_finish(energy,fock,total)
    USE control_flags,ONLY:conv_elec,scf_error,n_scf_steps
    REAL(DP),INTENT(IN)::energy,fock,total
    INTEGER::unit
    IF(.NOT.conv_elec)CALL errore('pilot','preliminary source did not converge',1)
    CALL pilot_open('summary',unit)
    CALL pilot_header(unit,4)
    WRITE(unit)energy,fock,total,scf_error,REAL(n_scf_steps,DP)
    CLOSE(unit)
    IF(pilot_cycle==2)THEN
      CALL pilot_open('residual',unit)
      CALL pilot_header(unit,6)
      WRITE(unit)fock0,fock1,fock2,dexx,fock1-0.5_DP*(fock0+fock2)
      CLOSE(unit)
    ENDIF
    pilot_done=pilot_cycle==2
    WRITE(stdout,'(A,3ES25.16)')'R07_RELAX_SOURCE_OPERATOR ',energy,fock,total
  END SUBROUTINE

  SUBROUTINE pilot_publish()
    USE mp,ONLY:mp_barrier
    USE mp_bands,ONLY:intra_bgrp_comm
    INTEGER::unit
    IF(.NOT.pilot_done)CALL errore('pilot','post-punch before completion',1)
    CALL mp_barrier(intra_bgrp_comm)
    CALL pilot_open('complete',unit)
    CALL pilot_header(unit,5)
    CLOSE(unit)
    WRITE(stdout,'(A)')'R07_ONE_RELAXATION_PUNCH_COMPLETE; HSE_NOT_CONVERGED'
  END SUBROUTINE
