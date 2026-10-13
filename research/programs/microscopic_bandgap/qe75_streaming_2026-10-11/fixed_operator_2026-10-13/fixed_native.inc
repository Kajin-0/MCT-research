! GPL-2.0-or-later. Fixed-operator fixture ONLY; no electronic SCF/restart claim.
  FUNCTION fixed_path(k,readback) RESULT(path)
    USE mp_world, ONLY: mpime
    INTEGER,INTENT(IN)::k
    LOGICAL,INTENT(IN)::readback
    CHARACTER(1024)::path,root
    CHARACTER(32)::r,s
    INTEGER::status,length
    IF(readback) THEN
      CALL get_environment_variable('QE75_FIXED_READBACK',root,LENGTH=length,STATUS=status)
    ELSE
      CALL get_environment_variable('QE75_FIXED_INPUT',root,LENGTH=length,STATUS=status)
    ENDIF
    IF(status/=0 .OR. length<1 .OR. length>900) CALL errore('fixed','input/readback root',1)
    WRITE(r,'(I0)') mpime;WRITE(s,'(I0)') k
    path=TRIM(root)//'/rank'//TRIM(r)//'.k'//TRIM(s)//'.input'
  END FUNCTION

  SUBROUTINE fixed_driver()
    USE iso_fortran_env, ONLY:int64
    USE mp_world, ONLY:mpime,nproc
    USE mp_pools, ONLY:npool
    USE mp_exx, ONLY:negrp
    USE mp_bands, ONLY:nbgrp
    USE wvfct, ONLY:npwx,nbnd,wg
    USE klist, ONLY:nks,nkstot,ngk,igk_k,wk
    USE gvect, ONLY:ig_l2g
    USE wavefunctions, ONLY:evc
    USE io_files, ONLY:nwordwfc,iunwfc
    USE buffers, ONLY:save_buffer,get_buffer
    USE xc_lib, ONLY:stop_exx
    USE uspp, ONLY:okvan
    USE paw_variables, ONLY:okpaw
    USE qe75_native_lease, ONLY:native_check,native_phase
    INTEGER(int64)::header(8)
    INTEGER(int64),ALLOCATABLE::layout(:),globals(:)
    REAL(DP),ALLOCATABLE::occ(:,:),weights(:,:),kw(:)
    COMPLEX(DP),ALLOCATABLE::phi(:,:),probe(:,:)
    CHARACTER(16)::magic,footer
    CHARACTER(64)::identity,wanted
    INTEGER::k,u,ios,status,length
    CALL native_check()
    IF(nproc/=2 .OR. npool/=1 .OR. negrp/=1 .OR. nbgrp/=1 .OR. nks/=3 .OR. nkstot/=3 &
       .OR. nbnd/=48 .OR. npol/=2 .OR. .NOT.noncolin .OR. gamma_only .OR. use_gpu &
       .OR. okvan .OR. okpaw .OR. .NOT.use_ace) CALL errore('fixed','exact operator scope',1)
    CALL get_environment_variable('QE75_FIXED_IDENTITY',wanted,LENGTH=length,STATUS=status)
    IF(status/=0 .OR. length/=64) CALL errore('fixed','canonical identity missing',1)
    ALLOCATE(phi(npwx*npol,nbnd),probe(npwx*npol,1),occ(nbnd,nks),weights(nbnd,nks),kw(nks))
    ALLOCATE(fixed_probes(npwx*npol,nks),fixed_occ(nbnd,nks))
    DO k=1,nks
      OPEN(NEWUNIT=u,FILE=TRIM(fixed_path(k,.FALSE.)),ACCESS='stream',FORM='unformatted', &
           STATUS='old',ACTION='read',IOSTAT=ios)
      IF(ios/=0) CALL errore('fixed','canonical open',1)
      READ(u,IOSTAT=ios) magic,header,identity
      IF(ios/=0) CALL errore('fixed','canonical header read',1)
      IF(magic/='QE75-FIXED-01   ' .OR. identity/=wanted &
         .OR. ANY(header(1:7)/=INT([mpime,k,npwx,ngk(k),npol,nbnd,nks],int64)) &
         .OR. header(8)<1 .OR. header(8)>1000000) CALL errore('fixed','canonical shape/identity',1)
      ALLOCATE(layout(header(8)),globals(ngk(k)))
      READ(u,IOSTAT=ios) layout,globals,phi,occ,weights,kw,probe,footer
      IF(ios/=0 .OR. footer/='QE75-FIXED-END  ') CALL errore('fixed','canonical payload',1)
      READ(u,IOSTAT=ios) magic
      IF(ios/=-1) CALL errore('fixed','canonical trailing data',1)
      CLOSE(u)
      IF(ANY(globals/=INT(ig_l2g(igk_k(1:ngk(k),k)),int64))) CALL errore('fixed','actual G basis',1)
      IF(ANY(TRANSFER(kw,[0_int64],SIZE(kw))/=TRANSFER(wk,[0_int64],SIZE(wk)))) &
        CALL errore('fixed','actual k weights',1)
      IF(k==1) THEN
        fixed_layout=layout;fixed_occ=occ;wg=weights
      ELSE
        IF(ANY(layout/=fixed_layout) .OR. &
           ANY(TRANSFER(occ,[0_int64],SIZE(occ))/=TRANSFER(fixed_occ,[0_int64],SIZE(fixed_occ))) &
           .OR. ANY(TRANSFER(weights,[0_int64],SIZE(weights))/=TRANSFER(wg,[0_int64],SIZE(wg)))) &
          CALL errore('fixed','source consistency',1)
      ENDIF
      evc=phi;fixed_probes(:,k)=probe(:,1)
      CALL save_buffer(evc,nwordwfc,iunwfc,k)
      ! Real buffer readback, not a serialization of an unused input variable.
      evc=(0._DP,0._DP)
      CALL get_buffer(evc,nwordwfc,iunwfc,k)
      IF(ANY(TRANSFER(evc,[0_int64],2*SIZE(evc))/=TRANSFER(phi,[0_int64],2*SIZE(phi)))) &
         CALL errore('fixed','native source buffer readback',1)
      OPEN(NEWUNIT=u,FILE=TRIM(fixed_path(k,.TRUE.)),ACCESS='stream',FORM='unformatted', &
           STATUS='new',ACTION='write',IOSTAT=ios)
      IF(ios/=0) CALL errore('fixed','readback open',1)
      WRITE(u,IOSTAT=ios) 'QE75-FIXED-01   ',header,identity,layout,globals,evc,fixed_occ,wg,wk(1:nks), &
                           fixed_probes(:,k),'QE75-FIXED-END  '
      IF(ios/=0) CALL errore('fixed','readback write',1)
      CLOSE(u,IOSTAT=ios)
      IF(ios/=0) CALL errore('fixed','readback close',1)
      DEALLOCATE(layout,globals)
    ENDDO
    CALL native_phase(8)
    DEALLOCATE(phi,probe,occ,weights,kw)
    ! Match the original first-ACE functional activation, not the seed's old ACE.
    CALL stop_exx()
    nbndproj=nbnd
    CALL exxinit(.FALSE.)
    CALL aceinit(.FALSE.)
    CALL errore('fixed','unexpected return after first ACE fence',1)
  END SUBROUTINE

  SUBROUTINE fixed_kernel_capture(d_spin)
    USE iso_fortran_env, ONLY:int64
    USE mp_world, ONLY:mpime
    USE klist, ONLY:nks,xk,wk
    USE wvfct, ONLY:wg,nbnd,npwx
    USE symm_base, ONLY:nsym,s,sr
    USE cell_base, ONLY:omega,alat,tpiba,tpiba2,at,bg
    USE exx_base, ONLY:nqs,nkqs,nq1,nq2,nq3,index_xk,index_sym,index_xkq,xkq_collect,rir, &
      working_pool,coulomb_fac,coulomb_done,g2_convolution_all,exxdiv,erfc_scrlen,erf_scrlen, &
      gau_scrlen,yukawa,eps,eps_qdiv,grid_factor,x_gamma_extrapolation,on_double_grid, &
      use_regularization,use_coulomb_vcut_ws,use_coulomb_vcut_spheric,exxdiv_treatment
    USE qe75_native_lease, ONLY:native_phase
    COMPLEX(DP),INTENT(IN)::d_spin(2,2,48)
    INTEGER(int64),ALLOCATABLE::layout(:)
    INTEGER::k,q,ikq,u,ios,status,length
    CHARACTER(1024)::root,path
    CHARACTER(32)::r,mode
    REAL(DP)::xkp(3),xkq(3)
    CALL qdiag_layout(layout)
    IF(SIZE(layout)/=SIZE(fixed_layout)) CALL errore('fixed','operator layout length',1)
    IF(ANY(layout/=fixed_layout)) CALL errore('fixed','actual control/operator layout mismatch',1)
    IF(ANY(TRANSFER(x_occupation,[0_int64],SIZE(x_occupation))/= &
           TRANSFER(fixed_occ,[0_int64],SIZE(fixed_occ)))) CALL errore('fixed','occupation bits',1)
    IF(nqs/=8 .OR. nkqs/=8 .OR. ANY(index_xk<1) .OR. ANY(index_xk>3) .OR. &
       ANY(ABS(index_sym)>nsym) .OR. ANY(index_sym==0) .OR. ANY(index_xkq<1) .OR. &
       ANY(index_xkq>8)) CALL errore('fixed','complete q coverage',1)
    DO k=1,nks
      xkp=xk(:,k)
      DO q=1,nqs
        ikq=index_xkq(k,q);xkq=xkq_collect(:,ikq)
        CALL g2_convolution_all(dfftt%ngm,gt,xkp,xkq,q,k)
      ENDDO
    ENDDO
    IF(.NOT.ALL(coulomb_done)) CALL errore('fixed','incomplete screened kernel',1)
    CALL get_environment_variable('QE75_FIXED_KERNEL',root,LENGTH=length,STATUS=status)
    IF(status/=0 .OR. length<1 .OR. length>900) CALL errore('fixed','kernel root',1)
    WRITE(r,'(I0)') mpime;path=TRIM(root)//'/rank'//TRIM(r)//'.kernel'
    OPEN(NEWUNIT=u,FILE=TRIM(path),ACCESS='stream',FORM='unformatted',STATUS='new',ACTION='write',IOSTAT=ios)
    IF(ios/=0) CALL errore('fixed','kernel capture open',1)
    WRITE(u,IOSTAT=ios) 'QE75-KERNEL-01  ',INT([mpime,nks,nqs,nkqs,nsym,dfftt%ngm, &
      SIZE(layout),SIZE(rir),SIZE(coulomb_fac)],int64),layout, &
      omega,alat,tpiba,tpiba2,at,bg,exxalfa,ecutfock,exxdiv,erfc_scrlen,erf_scrlen,gau_scrlen, &
      yukawa,eps,eps_qdiv,grid_factor,exxdiv_treatment, &
      INT([nq1,nq2,nq3,gstart_t,ngmt_g,x_nbnd_occ],int64), &
      x_gamma_extrapolation,on_double_grid,use_regularization,use_coulomb_vcut_ws,use_coulomb_vcut_spheric, &
      INT(s(:,:,1:nsym),int64),sr(:,:,1:nsym),d_spin(:,:,1:nsym),INT(rir,int64), &
      INT(working_pool,int64),x_occupation,wg,wk(1:nks),coulomb_fac,'QE75-KERNEL-END '
    IF(ios/=0) CALL errore('fixed','kernel capture write',1)
    CLOSE(u,IOSTAT=ios)
    IF(ios/=0) CALL errore('fixed','kernel capture close',1)
    DEALLOCATE(layout)
    CALL native_phase(9)
    CALL get_environment_variable('QE75_FIXED_MODE',mode,STATUS=status)
    IF(status/=0) CALL errore('fixed','typed operator mode absent',1)
    IF(TRIM(mode)=='setup') CALL errore('fixed_setup','kernel inputs captured; intentional no-SCF no-ACE stop',86)
    IF(TRIM(mode)/='stream') CALL errore('fixed','unknown operator mode',1)
  END SUBROUTINE
