! GPL-2.0-or-later. NEW density-only PBE16 query, NOT pw.x/restart/SCF.
! Build gate is deliberately unreleased. This ELF MUST NOT RUN this phase.
PROGRAM r07_density_only_v1
 USE iso_c_binding,ONLY:c_int,c_char,c_null_char
 USE kinds,ONLY:DP
 USE mp_global,ONLY:mp_startup,mp_global_end
 USE mp_world,ONLY:nproc,mpime
 USE mp_pools,ONLY:npool
 USE mp_bands,ONLY:nbgrp,ntask_groups
 USE environment,ONLY:environment_start,environment_end
 USE io_files,ONLY:tmp_dir,prefix
 USE control_flags,ONLY:use_gpu,smallmem,gamma_only,lscf,scissor,sic,tq_smoothing,tbeta_smoothing
 USE noncollin_module,ONLY:noncolin,lspinorb,domag,npol,report,lforcet
 USE wavefunctions,ONLY:evc
 USE wvfct,ONLY:nbnd,npwx,current_k,g2kin
 USE klist,ONLY:nks,nkstot,xk,wk,ngk,igk_k,nelec,degauss,init_igk
 USE gvecw,ONLY:gcutw,ecutwfc,qcutz
 USE gvecs,ONLY:doublegrid
 USE gvect,ONLY:ngm,mill,g,ecutrho
 USE cell_base,ONLY:bg,tpiba,omega,alat,at
 USE ions_base,ONLY:nat,nsp,tau,ityp
 USE uspp,ONLY:nkb,vkb,okvan
 USE uspp_param,ONLY:upf
 USE paw_variables,ONLY:okpaw
 USE scf,ONLY:rho,vrs,vltot,v,kedtau,v_of_0
 USE fft_base,ONLY:dfftp,dffts
 USE uspp_init,ONLY:init_us_2
 USE becmod,ONLY:becp,allocate_bec_type,calbec
 USE xc_lib,ONLY:xclib_dft_is,exx_is_active
 USE funct,ONLY:get_dft_name
 USE symm_base,ONLY:nsym
#if defined(__HDF5)
 USE qeh5_base_module,ONLY:finalize_hdf5
#endif
 IMPLICIT NONE
 INTERFACE
  INTEGER(c_int) FUNCTION build_gate() BIND(C,NAME='r07_density_build_gate')
   IMPORT c_int
  END FUNCTION
  INTEGER(c_int) FUNCTION sync_file(path) BIND(C,NAME='r07_density_sync')
   IMPORT c_int,c_char
   CHARACTER(c_char),INTENT(IN)::path(*)
  END FUNCTION
 END INTERFACE
 INTEGER::u,ios,i,j,idx,n,Nref,Ngref,expected_sym
 INTEGER,EXTERNAL::n_plane_waves
 INTEGER(8)::h(20),input(16),fft(14,2),packet_bytes
 INTEGER(8),ALLOCATABLE::pwlabels(:,:),rlabels(:,:)
 INTEGER,ALLOCATABLE::lookup(:,:,:)
 INTEGER::lo(3),hi(3),key(3)
 REAL(DP)::B0(3,3),cell0(3,3),tau0(3,16),charge,scalars(8)
 INTEGER(8)::species0(16)
 COMPLEX(DP),ALLOCATABLE::ref(:,:),rhofile(:),P(:,:),kin(:,:),loc(:,:),nl(:,:),full(:,:)
 CHARACTER(1024)::root,packet
 CHARACTER::tail
 LOGICAL::needwf

 ! External separately linked gate prevents accidental material execution.
 ! It is NOT a Boolean/CLI/ENV permission or a fake native-owner receipt.
 IF(build_gate()/=0)ERROR STOP 'R07 density-only build is UNRELEASED; no material execution'
 CALL get_command_argument(1,root)
 IF(INDEX(TRIM(root),'/home/User/repos/MCT-research/.tmp/r07spc16/density-')/=1)ERROR STOP 'private root'
 IF(INDEX(TRIM(root),'..')/=0.OR.command_argument_count()/=1)ERROR STOP 'root/argv'
 CALL mp_startup()
 IF(nproc/=1.OR.mpime/=0.OR.npool/=1.OR.nbgrp/=1.OR.ntask_groups/=1)ERROR STOP 'one process/world rank domain'
 report=0;use_gpu=.FALSE.;smallmem=.FALSE.;qcutz=0._DP
 lscf=.FALSE.;scissor=.FALSE.;sic=.FALSE.;lforcet=.FALSE.
 tq_smoothing=.FALSE.;tbeta_smoothing=.FALSE.
 CALL environment_start('R07DENSITY')
 prefix='r07pbe';tmp_dir=TRIM(root)//'/input/'
 needwf=.FALSE.
 CALL read_file_new(needwf)
 ! needwf is overwritten on return: NEVER reuse it as a new request.
 IF(ALLOCATED(evc))ERROR STOP 'forbidden full wavefunction allocation'
 IF(nat/=16.OR.nsp/=3.OR.nbnd/=352.OR.npol/=2.OR.nspin_value()/=4)ERROR STOP 'metadata'
 IF(.NOT.noncolin.OR..NOT.lspinorb.OR.domag.OR.gamma_only.OR.okvan.OR.okpaw)ERROR STOP 'spin/NC domain'
 IF(ANY(upf(:)%nlcc).OR.ANY(upf(:)%tvanp).OR.ANY(upf(:)%tpawp).OR.ANY(.NOT.upf(:)%has_so))ERROR STOP 'FR NC no core'
 IF(TRIM(get_dft_name())/='PBE'.OR.xclib_dft_is('hybrid').OR.xclib_dft_is('meta').OR.exx_is_active())ERROR STOP 'PBE only'
 IF(dfftp%nr1/=80.OR.dfftp%nr2/=80.OR.dfftp%nr3/=80)ERROR STOP 'density FFT grid'
 IF(nks/=1.OR.nkstot/=1.OR.nkb/=712.OR.ABS(nelec-288._DP)>1.e-12_DP)ERROR STOP 'state extent'
 IF(ABS(ecutwfc-50._DP)>1.e-12_DP.OR.ABS(ecutrho-200._DP)>1.e-12_DP.OR.ABS(degauss-.001_DP)>1.e-14_DP)ERROR STOP 'cutoff/sigma'
 IF(MAXVAL(ABS(xk))>0._DP.OR.ABS(wk(1)-1._DP)>1.e-12_DP)ERROR STOP 'Gamma'

 OPEN(NEWUNIT=u,FILE=TRIM(root)//'/input/query.bin',STATUS='OLD',ACTION='READ',ACCESS='STREAM',FORM='UNFORMATTED',IOSTAT=ios)
 IF(ios/=0)ERROR STOP 'query absent'
 READ(u,IOSTAT=ios)input,B0,cell0,tau0,species0
 IF(ios/=0.OR.input(1)/=71601001_8.OR.input(2)/=1.OR.input(5)/=12.OR.input(6)/=352.OR.input(7)/=288)ERROR STOP 'query header'
 Nref=INT(input(3));Ngref=INT(input(4))
 IF(Nref/=21595.OR.Ngref/=173631.OR.input(8)<0.OR.input(8)>1)ERROR STOP 'query dimensions/case'
 expected_sym=24;IF(input(8)==1)expected_sym=4
 IF(nsym/=expected_sym.OR.MAXVAL(ABS(B0-bg*tpiba))>1.e-12_DP)ERROR STOP 'symmetry/frame'
 IF(MAXVAL(ABS(cell0-at*alat))>1.e-12_DP.OR.MAXVAL(ABS(tau0-tau*alat))>1.e-12_DP.OR.ANY(species0/=INT(ityp,8)))ERROR STOP 'geometry'
 ALLOCATE(pwlabels(3,Nref),ref(2*Nref,12),rlabels(3,Ngref),rhofile(Ngref))
 READ(u,IOSTAT=ios)pwlabels,ref,rlabels,rhofile
 IF(ios/=0)ERROR STOP 'query payload'
 READ(u,IOSTAT=ios)tail
 IF(ios>=0)ERROR STOP 'trailing query'
 CLOSE(u,IOSTAT=ios);IF(ios/=0)ERROR STOP 'input close'
 ! Verify read_rhog by physical G labels; refuse mismatch, never silently fix.
 lo=INT(MINVAL(rlabels,DIM=2));hi=INT(MAXVAL(rlabels,DIM=2))
 IF(ANY(hi-lo>100))ERROR STOP 'density Miller extent'
 ALLOCATE(lookup(lo(1):hi(1),lo(2):hi(2),lo(3):hi(3)));lookup=0
 DO i=1,Ngref
  key=INT(rlabels(:,i));IF(lookup(key(1),key(2),key(3))/=0)ERROR STOP 'duplicate density G'
  lookup(key(1),key(2),key(3))=i
 ENDDO
 IF(ngm/=Ngref)ERROR STOP 'one-rank density coverage'
 charge=0._DP
 DO i=1,ngm
  key=mill(:,i);IF(ANY(key<lo).OR.ANY(key>hi))ERROR STOP 'outside density G'
  idx=lookup(key(1),key(2),key(3));IF(idx==0)ERROR STOP 'missing density G'
  IF(.NOT.same_complex(rho%of_g(i,1),rhofile(idx)))ERROR STOP 'rhoG not byte exact'
  lookup(key(1),key(2),key(3))=0
  IF(ALL(key==0))charge=omega*REAL(rho%of_g(i,1),DP)
 ENDDO
 IF(ANY(lookup/=0).OR.ABS(charge-288._DP)>1.e-8_DP)ERROR STOP 'density/charge'
 IF(ANY(rho%of_g(:,2:4)/=(0._DP,0._DP)).OR.ANY(rho%of_r(:,2:4)/=0._DP))ERROR STOP 'magnetic density'
 DEALLOCATE(lookup,rlabels,rhofile)
 CALL set_vrs(vrs,vltot,v%of_r,kedtau,v%kin_r,dfftp%nnr,4,doublegrid)
 IF(ANY(vrs(:,2:4)/=0._DP))ERROR STOP 'magnetic potential'
 npwx=n_plane_waves(gcutw,nks,xk,g,ngm)
 CALL init_igk(npwx,ngm,g,gcutw)
 n=ngk(1);IF(n/=Nref.OR.npwx/=Nref)ERROR STOP 'new one-rank plane waves'
 ALLOCATE(vkb(npwx,nkb),g2kin(npwx),P(2*npwx,12),kin(2*npwx,12),loc(2*npwx,12),nl(2*npwx,12),full(2*npwx,12))
 lo=INT(MINVAL(pwlabels,DIM=2));hi=INT(MAXVAL(pwlabels,DIM=2))
 IF(ANY(hi-lo>100))ERROR STOP 'wave Miller extent'
 ALLOCATE(lookup(lo(1):hi(1),lo(2):hi(2),lo(3):hi(3)));lookup=0
 DO i=1,Nref
  key=INT(pwlabels(:,i));IF(lookup(key(1),key(2),key(3))/=0)ERROR STOP 'duplicate wave G'
  lookup(key(1),key(2),key(3))=i
 ENDDO
 P=(0._DP,0._DP)
 DO i=1,n
  key=mill(:,igk_k(i,1));IF(ANY(key<lo).OR.ANY(key>hi))ERROR STOP 'outside wave G'
  idx=lookup(key(1),key(2),key(3));IF(idx==0)ERROR STOP 'missing wave G'
  P(i,:)=ref(idx,:);P(npwx+i,:)=ref(Nref+idx,:);lookup(key(1),key(2),key(3))=0
 ENDDO
 IF(ANY(lookup/=0))ERROR STOP 'incomplete wave G'
 DEALLOCATE(lookup,pwlabels,ref)
 current_k=1;CALL g2_kin(1)
 CALL init_us_2(n,igk_k(:,1),xk(:,1),vkb,.FALSE.)
 CALL allocate_bec_type(nkb,12,becp)
 CALL h_psi(npwx,n,12,P,full)
 kin=(0._DP,0._DP);loc=kin;nl=kin
 DO j=1,12
  kin(1:n,j)=g2kin(1:n)*P(1:n,j);kin(npwx+1:npwx+n,j)=g2kin(1:n)*P(npwx+1:npwx+n,j)
 ENDDO
 CALL vloc_psi_nc_acc(npwx,n,12,P,vrs,loc)
 CALL calbec(n,vkb,P,becp,12)
 CALL add_vuspsi(npwx,n,12,nl)
 fft(:,1)=descriptor(1);fft(:,2)=descriptor(2)
 h=[71601002_8,1_8,1_8,0_8,INT(getpid(),8),INT(npwx,8),INT(n,8),INT(ngm,8),INT(dfftp%nnr,8), &
 INT(dffts%nnr,8),352_8,12_8,4_8,712_8,16_8,input(8),INT(nsym,8),0_8,0_8,0_8]
 scalars=[omega,charge,degauss,ecutwfc,ecutrho,v_of_0,0._DP,0._DP]
 packet=TRIM(root)//'/output/H.one'
 OPEN(NEWUNIT=u,FILE=TRIM(packet),STATUS='OLD',ACTION='WRITE',ACCESS='STREAM',FORM='UNFORMATTED',IOSTAT=ios)
 IF(ios/=0)ERROR STOP 'precreated output missing'
 WRITE(u,IOSTAT=ios)h,fft,bg*tpiba,xk(:,1),scalars,INT(mill(:,igk_k(1:n,1)),8),INT(mill(:,1:ngm),8), &
 P,kin,loc,nl,full,rho%of_g,rho%of_r,vrs
 IF(ios/=0)ERROR STOP 'packet write'
 FLUSH(u,IOSTAT=ios);IF(ios/=0)ERROR STOP 'packet flush'
 INQUIRE(UNIT=u,SIZE=packet_bytes,IOSTAT=ios)
 IF(ios/=0.OR.packet_bytes<1.OR.packet_bytes>1073741824_8)ERROR STOP 'packet extent'
 CLOSE(u,IOSTAT=ios);IF(ios/=0)ERROR STOP 'packet close'
 IF(sync_file(TRIM(packet)//c_null_char)/=0)ERROR STOP 'packet durable close'
 ! Native owner begin/final and numerical admission are NOT released here.
 CALL environment_end('R07DENSITY')
#if defined(__HDF5) && !defined(_HDF5)
 CALL finalize_hdf5()
#endif
 CALL mp_global_end()
CONTAINS
 LOGICAL FUNCTION same_complex(a,b)
  COMPLEX(DP),INTENT(IN)::a,b
  INTEGER(8)::aa(2),bb(2)
  aa=TRANSFER(a,aa);bb=TRANSFER(b,bb);same_complex=ALL(aa==bb)
 END FUNCTION
 INTEGER FUNCTION nspin_value()
  USE lsda_mod,ONLY:nspin
  nspin_value=nspin
 END FUNCTION
 FUNCTION descriptor(which) RESULT(row)
  INTEGER,INTENT(IN)::which
  INTEGER(8)::row(14)
  IF(which==1)THEN
   row=[INT(dfftp%nr1,8),INT(dfftp%nr2,8),INT(dfftp%nr3,8),INT(dfftp%nr1x,8),INT(dfftp%nr2x,8),INT(dfftp%nr3x,8), &
   INT(dfftp%my_nr2p,8),INT(dfftp%my_nr3p,8),INT(dfftp%my_i0r2p,8),INT(dfftp%my_i0r3p,8), &
   INT(dfftp%nproc2,8),INT(dfftp%nproc3,8),INT(dfftp%nnr,8),0_8]
  ELSE
   row=[INT(dffts%nr1,8),INT(dffts%nr2,8),INT(dffts%nr3,8),INT(dffts%nr1x,8),INT(dffts%nr2x,8),INT(dffts%nr3x,8), &
   INT(dffts%my_nr2p,8),INT(dffts%my_nr3p,8),INT(dffts%my_i0r2p,8),INT(dffts%my_i0r3p,8), &
   INT(dffts%nproc2,8),INT(dffts%nproc3,8),INT(dffts%nnr,8),0_8]
  ENDIF
 END FUNCTION
END PROGRAM
