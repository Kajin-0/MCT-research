! Private fixed-trial diagnostic. Native physics/EXX routines are unchanged.
  SUBROUTINE r07_same_density_H()
    USE wavefunctions,ONLY:evc
    USE wvfct,ONLY:npwx,nbnd,current_k,et,wg,g2kin
    USE klist,ONLY:ngk,igk_k,xk,wk,degauss,ngauss,nks
    USE gvect,ONLY:mill,ngm
    USE cell_base,ONLY:bg,tpiba,omega
    USE xc_lib,ONLY:get_screening_parameter
    USE mp_world,ONLY:mpime
    USE mp,ONLY:mp_barrier,mp_max,mp_min,mp_sum
    USE mp_bands,ONLY:intra_bgrp_comm
    USE exx_base,ONLY:nkqs,index_xk,index_sym,index_xkq,xkq_collect,coulomb_fac
    USE becmod,ONLY:becp,allocate_bec_type,deallocate_bec_type,calbec
    USE uspp,ONLY:nkb,vkb,deeq_nc,okvan
    USE uspp_param,ONLY:nh,nhm
    USE ions_base,ONLY:nat,ityp
    USE scf,ONLY:rho,v,vrs,rho_core,rhog_core,kedtau,vltot
    USE ener,ONLY:ehart,etxc,vtxc,demet
    USE fft_base,ONLY:dfftp,dffts
    USE dfunct,ONLY:newd
    USE lsda_mod,ONLY:nspin
    USE gvecs,ONLY:doublegrid
    USE fixed_occ,ONLY:tfixed_occ,f_inp
    USE noncollin_module,ONLY:domag,lspinorb
    INTEGER::u,ios,n,nt,j,i,na,nhere
    INTEGER(8)::h(16),dims(15),fft(14,3)
    INTEGER(8),ALLOCATABLE::labels(:,:)
    REAL(DP)::B0(3,3),k0(3),bounds(12),charge,entropy,eth,etotefield
    REAL(DP),ALLOCATABLE::oldf(:,:),density(:),savedwg(:)
    COMPLEX(DP),ALLOCATABLE::trial(:,:),kin(:,:),loc(:,:),nl(:,:),fock(:,:),check(:,:)
    LOGICAL::oldfixed
    CHARACTER(1024)::root
    CHARACTER(16)::rank
    CHARACTER::tail
    current_k=1
    CALL pilot_guard()
    IF(use_ace.OR.domag.OR..NOT.lspinorb.OR.nspin/=4.OR.nks/=1.OR.ngauss/=-99.OR. &
       ABS(degauss-.001_DP)>1.e-14_DP)CALL errore('sameD','fixed trial direct HSE/FD domain refused',1)
    n=ngk(1);nt=164
    CALL get_environment_variable('R07_FIRSTACE_ROOT',root)
    WRITE(rank,'(I0)')mpime
    OPEN(NEWUNIT=u,FILE=TRIM(root)//'/pilot/input.rank'//TRIM(rank),STATUS='OLD', &
         ACCESS='STREAM',FORM='UNFORMATTED',ACTION='READ',IOSTAT=ios)
    CALL pilot_check_io(ios)
    READ(u,IOSTAT=ios)h
    CALL pilot_check_io(ios)
    IF(ANY(h/=[70251510_8,1_8,INT(mpime,8),INT(npwx,8),INT(n,8),176_8,2_8,164_8, &
       152_8,146_8,142_8,4_8,144_8,0_8,0_8,0_8]))CALL errore('sameD','input extents refused',1)
    ALLOCATE(labels(3,n),trial(2*npwx,nt),kin(2*npwx,nt),loc(2*npwx,nt),nl(2*npwx,nt), &
       fock(2*npwx,nt),check(2*npwx,6),savedwg(nbnd))
    READ(u,IOSTAT=ios)B0,k0,labels,wg(:,1),evc,trial
    CALL pilot_check_io(ios)
    READ(u,IOSTAT=ios)tail
    IF(ios>=0)CALL errore('sameD','trailing canonical bytes',1)
    CLOSE(u)
    IF(ANY(labels/=INT(mill(:,igk_k(1:n,1)),8)).OR.MAXVAL(ABS(B0-bg*tpiba))>1.e-12_DP.OR. &
       MAXVAL(ABS(k0-xk(:,1)))>1.e-12_DP.OR.ABS(wk(1)-1._DP)>1.e-12_DP) &
       CALL errore('sameD','physical frame mismatch',1)
    IF(ANY(wg(1:142,1)/=1._DP).OR.ANY(wg(143:146,1)/=.5_DP).OR.ANY(wg(147:176,1)/=0._DP)) &
       CALL errore('sameD','declared trial weights mismatch',1)
    savedwg=wg(:,1)
    ! Existing native fixed-occupation branch, used for trial charge ONLY.
    ! No et/ef/eband produced by this call is called a solved spectrum.
    oldfixed=tfixed_occ
    IF(ALLOCATED(f_inp))CALL MOVE_ALLOC(f_inp,oldf)
    ALLOCATE(f_inp(nbnd,2));f_inp=0._DP;f_inp(:,1)=savedwg
    tfixed_occ=.TRUE.;et=0._DP
    CALL sum_band()
    tfixed_occ=oldfixed
    DEALLOCATE(f_inp)
    IF(ALLOCATED(oldf))CALL MOVE_ALLOC(oldf,f_inp)
    IF(ANY(wg(:,1)/=savedwg))CALL errore('sameD','native density weights changed',1)
    entropy=4._DP*LOG(2._DP);demet=-degauss*entropy
    ! exxinit activates HSE BEFORE rebuilding the SAME-D local functional.
    CALL exxinit(.FALSE.)
    IF(nkqs/=1.OR.ANY(index_xk/=1).OR.ANY(index_sym/=1).OR.ANY(index_xkq/=1).OR. &
       MAXVAL(ABS(xkq_collect))>1.e-12_DP.OR.x_nbnd_occ/=146)CALL errore('sameD','q/source layout',1)
    IF(ANY([dfftt%nr1,dfftt%nr2,dfftt%nr3]/=[60,60,60]).OR. &
       ABS(exxalfa-.25_DP)>1.e-12_DP.OR.ABS(ecutfock-200._DP)>1.e-10_DP.OR. &
       ABS(get_screening_parameter()-.106_DP)>1.e-12_DP)CALL errore('sameD','HSE domain',1)
    CALL v_of_rho(rho,rho_core,rhog_core,ehart,etxc,vtxc,eth,etotefield,charge,v)
    IF(ABS(charge-144._DP)>1.e-8_DP)CALL errore('sameD','native charge refused',1)
    CALL set_vrs(vrs,vltot,v%of_r,kedtau,v%kin_r,dfftp%nnr,nspin,doublegrid)
    CALL newd()
    CALL g2_kin(1)
    IF(ALLOCATED(becp%nc))CALL deallocate_bec_type(becp)
    CALL allocate_bec_type(nkb,nbnd,becp)
    kin=(0._DP,0._DP);loc=kin;nl=kin;fock=kin
    DO j=1,nt
       kin(1:n,j)=g2kin(1:n)*trial(1:n,j)
       kin(npwx+1:npwx+n,j)=g2kin(1:n)*trial(npwx+1:npwx+n,j)
    ENDDO
    CALL vloc_psi_nc_acc(npwx,n,nt,trial,vrs,loc)
    CALL calbec(n,vkb,trial,becp,nt)
    CALL add_vuspsi(npwx,n,nt,nl)
    CALL vexx(npwx,n,nt,trial,fock,becp)
    ! Independent native full wrapper on unchanged ORIGINAL six physical probes.
    CALL h_psi(npwx,n,6,trial(:,153:158),check)
    bounds=0._DP
    bounds(1)=MAXVAL(g2kin(1:n));CALL mp_max(bounds(1),intra_bgrp_comm)
    bounds(2)=MAXVAL(ABS(vrs(:,1))+SQRT(SUM(vrs(:,2:4)**2,DIM=2)))
    CALL mp_max(bounds(2),intra_bgrp_comm)
    bounds(3)=SUM(ABS(vkb(1:n,:))**2);CALL mp_sum(bounds(3),intra_bgrp_comm)
    DO na=1,nat
       nhere=nh(ityp(na));bounds(4)=bounds(4)+SUM(ABS(deeq_nc(1:nhere,1:nhere,na,:))**2)
    ENDDO
    bounds(4)=SQRT(bounds(4));bounds(5)=MINVAL(coulomb_fac);bounds(6)=MAXVAL(ABS(coulomb_fac))
    CALL mp_min(bounds(5),intra_bgrp_comm);CALL mp_max(bounds(6),intra_bgrp_comm)
    ALLOCATE(density(dfftt%nnr));density=0._DP
    DO j=1,x_nbnd_occ
       density=density+x_occupation(j,1)*(ABS(exxbuff(1:dfftt%nnr,j,1))**2+ &
           ABS(exxbuff(dfftt%nnr+1:2*dfftt%nnr,j,1))**2)
    ENDDO
    bounds(7)=MAXVAL(density);CALL mp_max(bounds(7),intra_bgrp_comm)
    bounds(8)=exxalfa*bounds(6)*bounds(7)/omega
    bounds(9)=bounds(1)+bounds(2)+bounds(3)*bounds(4)+bounds(8)
    bounds(10)=charge;bounds(11)=entropy;bounds(12)=demet
    DEALLOCATE(density)
    fft(:,1)=[INT(dfftp%nr1,8),INT(dfftp%nr2,8),INT(dfftp%nr3,8),INT(dfftp%nr1x,8), &
      INT(dfftp%nr2x,8),INT(dfftp%nr3x,8),INT(dfftp%my_nr2p,8),INT(dfftp%my_nr3p,8), &
      INT(dfftp%my_i0r2p,8),INT(dfftp%my_i0r3p,8),INT(dfftp%nproc2,8),INT(dfftp%nproc3,8), &
      INT(dfftp%nnr,8),0_8]
    fft(:,2)=[INT(dffts%nr1,8),INT(dffts%nr2,8),INT(dffts%nr3,8),INT(dffts%nr1x,8), &
      INT(dffts%nr2x,8),INT(dffts%nr3x,8),INT(dffts%my_nr2p,8),INT(dffts%my_nr3p,8), &
      INT(dffts%my_i0r2p,8),INT(dffts%my_i0r3p,8),INT(dffts%nproc2,8),INT(dffts%nproc3,8), &
      INT(dffts%nnr,8),0_8]
    fft(:,3)=[INT(dfftt%nr1,8),INT(dfftt%nr2,8),INT(dfftt%nr3,8),INT(dfftt%nr1x,8), &
      INT(dfftt%nr2x,8),INT(dfftt%nr3x,8),INT(dfftt%my_nr2p,8),INT(dfftt%my_nr3p,8), &
      INT(dfftt%my_i0r2p,8),INT(dfftt%my_i0r3p,8),INT(dfftt%nproc2,8),INT(dfftt%nproc3,8), &
      INT(dfftt%nnr,8),0_8]
    h=[70251511_8,1_8,INT(mpime,8),INT(getpid(),8),INT(npwx,8),INT(n,8),176_8,164_8, &
       INT(ngm,8),INT(dfftp%nnr,8),INT(dffts%nnr,8),INT(nkb,8),INT(nhm,8),8_8,4_8,146_8]
    dims=[INT(SIZE(exxbuff,1),8),INT(SIZE(exxbuff,2),8),INT(SIZE(exxbuff,3),8), &
      INT(x_nbnd_occ,8),INT(SIZE(vrs,1),8),INT(SIZE(rho%of_r,1),8),INT(SIZE(rho%of_g,1),8), &
      INT(nkqs,8),INT(npol,8),INT(nks,8),0_8,0_8,0_8,0_8,0_8]
    OPEN(NEWUNIT=u,FILE=TRIM(root)//'/pilot/H.rank'//TRIM(rank),STATUS='NEW', &
       ACCESS='STREAM',FORM='UNFORMATTED',ACTION='WRITE',IOSTAT=ios)
    CALL pilot_check_io(ios)
    WRITE(u,IOSTAT=ios)h,dims,fft,bg*tpiba,xk(:,1),omega,wk(1),exxalfa,ecutfock, &
      get_screening_parameter(),degauss,bounds,ehart,etxc,vtxc, &
      INT(mill(:,igk_k(1:n,1)),8),INT(mill(:,1:ngm),8),wg(:,1),evc,trial,kin,loc,nl,fock,check, &
      rho%of_g,rho%of_r,vrs
    CALL pilot_check_io(ios)
    CLOSE(u)
    CALL mp_barrier(intra_bgrp_comm)
    WRITE(stdout,'(A,3ES25.16)')'R07_SAME_D_FULL_H_COMPLETE ',charge,entropy,bounds(9)
    DEALLOCATE(labels,trial,kin,loc,nl,fock,check,savedwg)
  END SUBROUTINE r07_same_density_H
