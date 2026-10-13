! GPL-2.0-or-later. Read-only observation; no FFT initialization changes.
MODULE qe75_resource_descriptor
  USE iso_fortran_env, ONLY: int64
  USE fft_types, ONLY: fft_type_descriptor
  IMPLICIT NONE
CONTAINS
  SUBROUTINE resource_write(path,profile,common,rank,world,scope,dense,smooth,fock,code)
    CHARACTER(*), INTENT(IN) :: path
    CHARACTER(64), INTENT(IN) :: profile,common
    INTEGER, INTENT(IN) :: rank,world
    INTEGER(int64), INTENT(IN) :: scope(:)
    TYPE(fft_type_descriptor), INTENT(IN) :: dense,smooth,fock
    INTEGER, INTENT(OUT) :: code
    INTEGER :: u,ios,closing
    code=1
    IF(SIZE(scope)/=12 .OR. rank<0 .OR. rank>=world .OR. world/=2) RETURN
    IF(STORAGE_SIZE(0_int64)/=64 .OR. STORAGE_SIZE(0)/=32) RETURN
    OPEN(NEWUNIT=u,FILE=path,STATUS='new',ACCESS='stream',FORM='unformatted', &
         ACTION='write',CONVERT='little_endian',IOSTAT=ios)
    IF(ios/=0) RETURN
    WRITE(u,IOSTAT=ios) 'FFTRES01',1_int64,INT(rank,int64),INT(world,int64),12_int64,profile,common,scope
    CALL put_descriptor(u,'dense',dense,ios)
    CALL put_descriptor(u,'smooth',smooth,ios)
    CALL put_descriptor(u,'fock',fock,ios)
    IF(ios==0) WRITE(u,IOSTAT=ios) 'FFTEND01'
    CLOSE(u,IOSTAT=closing)
    IF(ios==0 .AND. closing==0) code=0
  END SUBROUTINE
  SUBROUTINE put_descriptor(u,name,d,ios)
    INTEGER, INTENT(IN) :: u
    CHARACTER(*), INTENT(IN) :: name
    TYPE(fft_type_descriptor), INTENT(IN) :: d
    INTEGER, INTENT(INOUT) :: ios
    CHARACTER(16) :: label
    label=name
    IF(ios/=0) RETURN
    WRITE(u,IOSTAT=ios) label, [INT(d%nr1,int64), &
      INT(d%nr2,int64), &
      INT(d%nr3,int64), &
      INT(d%nr1x,int64), &
      INT(d%nr2x,int64), &
      INT(d%nr3x,int64), &
      INT(d%nproc,int64), &
      INT(d%nproc2,int64), &
      INT(d%nproc3,int64), &
      INT(d%mype,int64), &
      INT(d%mype2,int64), &
      INT(d%mype3,int64), &
      INT(d%my_nr2p,int64), &
      INT(d%my_nr3p,int64), &
      INT(d%my_i0r2p,int64), &
      INT(d%my_i0r3p,int64), &
      INT(d%nnp,int64), &
      INT(d%nnr,int64), &
      INT(d%nnr_tg,int64), &
      INT(MERGE(1,0,d%has_task_groups),int64), &
      INT(MERGE(1,0,d%use_pencil_decomposition),int64)]
    CALL put1(u,'nr1p',d%nr1p,ios)
    CALL put1(u,'nr1w',d%nr1w,ios)
    CALL put1(u,'nr2p',d%nr2p,ios)
    CALL put1(u,'nr3p',d%nr3p,ios)
    CALL put1(u,'nr2p_offset',d%nr2p_offset,ios)
    CALL put1(u,'nr3p_offset',d%nr3p_offset,ios)
    CALL put1(u,'i0r2p',d%i0r2p,ios)
    CALL put1(u,'i0r3p',d%i0r3p,ios)
    CALL put1(u,'ir1p',d%ir1p,ios)
    CALL put1(u,'ir1w',d%ir1w,ios)
    CALL put1(u,'nsp',d%nsp,ios)
    CALL put1(u,'nsw',d%nsw,ios)
    CALL put1(u,'ngl',d%ngl,ios)
    CALL put1(u,'nwl',d%nwl,ios)
    CALL put1(u,'iproc2',d%iproc2,ios)
    CALL put1(u,'iproc3',d%iproc3,ios)
    CALL put1(u,'iplp',d%iplp,ios)
    CALL put1(u,'iplw',d%iplw,ios)
    CALL put1(u,'iss',d%iss,ios)
    CALL put1(u,'isind',d%isind,ios)
    CALL put1(u,'ismap',d%ismap,ios)
    CALL put1(u,'nl',d%nl,ios)
    CALL put1(u,'nlm',d%nlm,ios)
    CALL put1(u,'tg_snd',d%tg_snd,ios)
    CALL put1(u,'tg_rcv',d%tg_rcv,ios)
    CALL put1(u,'tg_sdsp',d%tg_sdsp,ios)
    CALL put1(u,'tg_rdsp',d%tg_rdsp,ios)
    CALL put2(u,'iproc',d%iproc,ios)
    CALL put2(u,'indp',d%indp,ios)
    CALL put2(u,'indw',d%indw,ios)
    CALL put2(u,'nsp_offset',d%nsp_offset,ios)
    CALL put2(u,'nsw_offset',d%nsw_offset,ios)
  END SUBROUTINE
  SUBROUTINE put1(u,name,a,ios)
    INTEGER, INTENT(IN) :: u
    CHARACTER(*), INTENT(IN) :: name
    INTEGER, ALLOCATABLE, INTENT(IN) :: a(:)
    INTEGER, INTENT(INOUT) :: ios
    CHARACTER(24) :: label
    label=name
    IF(ios/=0) RETURN
    IF(ALLOCATED(a)) THEN
      WRITE(u,IOSTAT=ios) label,INT(SIZE(a),int64),1_int64,INT(a,int64)
    ELSE
      WRITE(u,IOSTAT=ios) label,-1_int64,0_int64
    ENDIF
  END SUBROUTINE
  SUBROUTINE put2(u,name,a,ios)
    INTEGER, INTENT(IN) :: u
    CHARACTER(*), INTENT(IN) :: name
    INTEGER, ALLOCATABLE, INTENT(IN) :: a(:,:)
    INTEGER, INTENT(INOUT) :: ios
    CHARACTER(24) :: label
    label=name
    IF(ios/=0) RETURN
    IF(ALLOCATED(a)) THEN
      WRITE(u,IOSTAT=ios) label,INT(SIZE(a,1),int64),INT(SIZE(a,2),int64),INT(a,int64)
    ELSE
      WRITE(u,IOSTAT=ios) label,-1_int64,0_int64
    ENDIF
  END SUBROUTINE
END MODULE
