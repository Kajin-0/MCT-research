  SUBROUTINE r07_fixed_TR_probe()
    USE wavefunctions,ONLY:evc
    USE wvfct,ONLY:npwx,nbnd,current_k,et,wg
    USE klist,ONLY:ngk,igk_k,xk,wk
    USE gvect,ONLY:mill
    USE cell_base,ONLY:bg,tpiba,omega
    USE xc_lib,ONLY:get_screening_parameter
    USE mp_world,ONLY:mpime
    USE mp,ONLY:mp_barrier,mp_max,mp_min
    USE mp_bands,ONLY:intra_bgrp_comm
    USE exx_base,ONLY:nkqs,index_xk,index_sym,index_xkq,xkq_collect,coulomb_fac
    USE becmod,ONLY:bec_type
    INTEGER::u,ios,n,source,nt,i,j,ending,nr
    INTEGER(8)::h(8),extent(10)
    INTEGER(8),ALLOCATABLE::labels(:,:)
    REAL(DP)::B0(3,3),k0(3),bounds(4)
    REAL(DP),ALLOCATABLE::density(:)
    COMPLEX(DP),ALLOCATABLE::reversed(:,:),trial(:,:),action(:,:)
    TYPE(bec_type)::dummy
    CHARACTER(1024)::root
    CHARACTER(16)::rank,sid
    CHARACTER::tail
    current_k=1
    CALL pilot_guard()
    n=ngk(1)
    CALL get_environment_variable('R07_FIRSTACE_ROOT',root)
    WRITE(rank,'(I0)')mpime
    OPEN(NEWUNIT=u,FILE=TRIM(root)//'/pilot/input.rank'//TRIM(rank),STATUS='OLD', &
         ACCESS='STREAM',FORM='UNFORMATTED',ACTION='READ',IOSTAT=ios)
    CALL pilot_check_io(ios)
    READ(u,IOSTAT=ios)h
    CALL pilot_check_io(ios)
    nt=INT(h(8))
    IF(nt<352.OR.nt>376.OR.MOD(nt,2)/=0)CALL errore('pairedProbe','trial bound refused',1)
    IF(ANY(h/=[70251501_8,1_8,INT(mpime,8),INT(npwx,8),INT(n,8),176_8,2_8,INT(nt,8)])) &
       CALL errore('pairedProbe','canonical input dimensions/rank refused',1)
    ALLOCATE(labels(3,n),reversed(npwx*2,nbnd),trial(npwx*2,nt),action(npwx*2,nt))
    READ(u,IOSTAT=ios)B0,k0,labels,et(:,1),wg(:,1),evc,reversed,trial
    CALL pilot_check_io(ios)
    READ(u,IOSTAT=ios)tail
    IF(ios>=0)CALL errore('pairedProbe','canonical input trailing bytes',1)
    CLOSE(u)
    IF(ANY(labels/=INT(mill(:,igk_k(1:n,1)),8)).OR.MAXVAL(ABS(B0-bg*tpiba))>1.e-12_DP.OR. &
       MAXVAL(ABS(k0-xk(:,1)))>1.e-12_DP.OR.ABS(wk(1)-1._DP)>1.e-12_DP) &
       CALL errore('pairedProbe','canonical physical frame refused',1)
    IF(ABS(SUM(wg(:,1))-144._DP)>1.e-8_DP.OR.ANY(wg(:,1)<0._DP)) &
       CALL errore('pairedProbe','source charge refused',1)
    DO source=1,2
       IF(source==2)evc=reversed
       CALL exxinit(.FALSE.)
       IF(nkqs/=1.OR.ANY(index_xk/=1).OR.ANY(index_sym/=1).OR.ANY(index_xkq/=1).OR. &
          MAXVAL(ABS(xkq_collect))>1.e-12_DP)CALL errore('pairedProbe','Gamma/q1 mapping refused',1)
       IF(ANY([dfftt%nr1,dfftt%nr2,dfftt%nr3]/=[60,60,60]).OR. &
          ABS(exxalfa-.25_DP)>1.e-12_DP.OR.ABS(ecutfock-200._DP)>1.e-10_DP.OR. &
          ABS(get_screening_parameter()-.106_DP)>1.e-12_DP.OR.x_nbnd_occ/=146) &
          CALL errore('pairedProbe','kernel/source domain refused',1)
       nr=dfftt%nnr
       ALLOCATE(density(nr))
       density=0._DP
       DO j=1,x_nbnd_occ
          density=density+x_occupation(j,1)*(ABS(exxbuff(1:nr,j,1))**2+ABS(exxbuff(nr+1:2*nr,j,1))**2)
       ENDDO
       bounds(3)=MAXVAL(density)
       CALL mp_max(bounds(3),intra_bgrp_comm)
       DEALLOCATE(density)
       action=(0._DP,0._DP)
       DO i=1,nt,176
          ending=MIN(i+175,nt)
          CALL vexx(npwx,n,ending-i+1,trial(:,i:ending),action(:,i:ending),dummy)
       ENDDO
       bounds(1)=MINVAL(coulomb_fac)
       bounds(2)=MAXVAL(ABS(coulomb_fac))
       CALL mp_min(bounds(1),intra_bgrp_comm)
       CALL mp_max(bounds(2),intra_bgrp_comm)
       bounds(4)=exxalfa*bounds(2)*bounds(3)/omega
       WRITE(sid,'(I0)')source
       OPEN(NEWUNIT=u,FILE=TRIM(root)//'/pilot/s'//TRIM(sid)//'.rank'//TRIM(rank),STATUS='NEW', &
            ACCESS='STREAM',FORM='UNFORMATTED',ACTION='WRITE',IOSTAT=ios)
       CALL pilot_check_io(ios)
       h=[70251502_8,1_8,INT(mpime,8),INT(getpid(),8),INT(npwx,8),INT(n,8),INT(source,8),INT(nt,8)]
       extent=[INT(dfftt%nr1,8),INT(dfftt%nr2,8),INT(dfftt%nr3,8),INT(dfftt%nnr,8), &
         INT(SIZE(exxbuff,1),8),INT(SIZE(exxbuff,2),8),INT(SIZE(exxbuff,3),8),INT(x_nbnd_occ,8),INT(nbndproj,8),1_8]
       WRITE(u,IOSTAT=ios)h,extent,bg*tpiba,xk(:,1),wk(1),exxalfa,ecutfock,get_screening_parameter(),bounds, &
         INT(mill(:,igk_k(1:n,1)),8),et(:,1),wg(:,1),evc,trial,action
       CALL pilot_check_io(ios)
       CLOSE(u)
       CALL mp_barrier(intra_bgrp_comm)
       WRITE(stdout,'(A,I0)')'R07_PAIRED_FOCK_SOURCE_COMPLETE ',source
    ENDDO
    WRITE(stdout,'(A)')'R07_PAIRED_FOCK_DONE'
    DEALLOCATE(labels,reversed,trial,action)
  END SUBROUTINE r07_fixed_TR_probe
