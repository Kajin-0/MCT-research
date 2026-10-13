! GPL-2.0-or-later. Read-only initial-state capture; never generates SCF waves.
MODULE qe75_initial_state
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64,file_storage_size
  USE ieee_arithmetic, ONLY: ieee_is_finite
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: initial_write,initial_read
CONTAINS
  SUBROUTINE initial_read(path,fingerprint,rank,k,npwx,npw,npol,layout,mill,kpoint,wave,et,wg,rhor,rhog,vrs,code)
    CHARACTER(*), INTENT(IN) :: path,fingerprint
    INTEGER, INTENT(IN) :: rank,k,npwx,npw,npol,mill(:,:)
    INTEGER(int64), INTENT(IN) :: layout(:)
    REAL(DP), INTENT(IN) :: kpoint(3)
    REAL(DP), INTENT(INOUT) :: et(:,:),wg(:,:),rhor(:,:),vrs(:,:)
    COMPLEX(DP), INTENT(INOUT) :: wave(:,:),rhog(:,:)
    INTEGER, INTENT(OUT) :: code
    INTEGER :: u,ios,j,s,close_status
    INTEGER(int64) :: h(13),expected(13),extent,bytes,after_bytes
    INTEGER(int64), ALLOCATABLE :: read_layout(:),read_mill(:,:)
    REAL(DP) :: read_kpoint(3)
    CHARACTER(16) :: magic
    CHARACTER(64) :: read_fingerprint
    code=1
    IF(file_storage_size/=8 .OR. rank<0 .OR. rank>1 .OR. k<1 .OR. npw<1 .OR. npwx<npw .OR. npol/=2) RETURN
    IF(SIZE(wave,1)/=npwx*npol .OR. SIZE(wave,2)/=48 .OR. ANY(SHAPE(mill)/=[3,npw])) RETURN
    IF(SIZE(et,1)/=48 .OR. SIZE(et,2)>8 .OR. ANY(SHAPE(et)/=SHAPE(wg))) RETURN
    IF(ANY(SHAPE(rhor)/=SHAPE(vrs)) .OR. SIZE(rhog,2)/=SIZE(rhor,2)) RETURN
    IF(SIZE(rhor,2)/=1 .AND. SIZE(rhor,2)/=4) RETURN
    expected=INT([1,rank,k,npwx,npw,npol,48,SIZE(et,2),SIZE(rhor,1),SIZE(rhor,2),SIZE(rhog,1),SIZE(layout),0],int64)
    expected(13)=72623859790382856_int64
    ! Shape factors here are bounded default integers; bands/spin/Nt are fixed.
    ! Convert BEFORE multiplication. This is below signed-64 overflow even at
    ! default INTEGER maxima, and the explicit fixture cap is checked first.
    extent=208_int64+8*INT(SIZE(layout),int64)+24*INT(npw,int64)+ &
           16*INT(npwx,int64)*2*48+16_int64*48*SIZE(et,2)+ &
           16*INT(SIZE(rhor,1),int64)*SIZE(rhor,2)+16*INT(SIZE(rhog,1),int64)*SIZE(rhog,2)
    IF(extent>128_int64*1024*1024) RETURN
    OPEN(NEWUNIT=u,FILE=path,STATUS='old',ACCESS='stream',FORM='unformatted',ACTION='read',IOSTAT=ios)
    IF(ios/=0) THEN
      code=2;RETURN
    ENDIF
    INQUIRE(UNIT=u,SIZE=bytes,IOSTAT=ios)
    IF(ios/=0 .OR. bytes/=extent) GOTO 910
    READ(u,IOSTAT=ios)magic,h,read_fingerprint,read_kpoint
    IF(ios/=0) GOTO 900
    IF(magic/='QE75-INITIAL-01 ' .OR. ANY(h/=expected) .OR. read_fingerprint/=fingerprint) GOTO 910
    IF(ANY(TRANSFER(read_kpoint,[0_int64],3)/=TRANSFER(kpoint,[0_int64],3))) GOTO 910
    ALLOCATE(read_layout(SIZE(layout)),read_mill(3,npw),STAT=ios)
    IF(ios/=0) GOTO 900
    READ(u,IOSTAT=ios)read_layout,read_mill
    IF(ios/=0) GOTO 900
    IF(ANY(read_layout/=layout) .OR. ANY(read_mill/=INT(mill,int64))) GOTO 910
    ! Metadata must match before any payload writes. A later payload failure
    ! returns nonzero; partially read arrays are unusable, never restart state.
    DO j=1,SIZE(wave,2)
      READ(u,IOSTAT=ios)wave(:,j)
      IF(ios/=0) GOTO 900
    ENDDO
    DO j=1,SIZE(et,2)
      READ(u,IOSTAT=ios)et(:,j),wg(:,j)
      IF(ios/=0) GOTO 900
    ENDDO
    DO j=1,SIZE(rhor,2)
      READ(u,IOSTAT=ios)rhor(:,j),rhog(:,j),vrs(:,j)
      IF(ios/=0) GOTO 900
    ENDDO
    INQUIRE(UNIT=u,SIZE=after_bytes,IOSTAT=ios)
    IF(ios/=0 .OR. after_bytes/=extent) GOTO 910
    IF(.NOT.ALL(ieee_is_finite(REAL(wave,DP))) .OR. .NOT.ALL(ieee_is_finite(AIMAG(wave)))) GOTO 910
    DO s=1,npol
      IF(ANY(wave((s-1)*npwx+npw+1:s*npwx,:)/=(0._DP,0._DP))) GOTO 910
    ENDDO
    IF(.NOT.ALL(ieee_is_finite(et)) .OR. .NOT.ALL(ieee_is_finite(wg))) GOTO 910
    IF(.NOT.ALL(ieee_is_finite(rhor)) .OR. .NOT.ALL(ieee_is_finite(vrs))) GOTO 910
    IF(.NOT.ALL(ieee_is_finite(REAL(rhog,DP))) .OR. .NOT.ALL(ieee_is_finite(AIMAG(rhog)))) GOTO 910
    CLOSE(u,IOSTAT=close_status)
    code=0
    IF(close_status/=0)code=4
    RETURN
910 code=6
    CLOSE(u,IOSTAT=close_status)
    RETURN
900 code=3
    CLOSE(u,IOSTAT=close_status)
  END SUBROUTINE
  SUBROUTINE initial_write(path,fingerprint,rank,k,npwx,npw,npol,layout,mill,kpoint,wave,et,wg,rhor,rhog,vrs,code)
    CHARACTER(*), INTENT(IN) :: path,fingerprint
    INTEGER, INTENT(IN) :: rank,k,npwx,npw,npol,mill(:,:)
    INTEGER(int64), INTENT(IN) :: layout(:)
    REAL(DP), INTENT(IN) :: kpoint(3),et(:,:),wg(:,:),rhor(:,:),vrs(:,:)
    COMPLEX(DP), INTENT(IN) :: wave(:,:),rhog(:,:)
    INTEGER, INTENT(OUT) :: code
    INTEGER :: u,ios,j,s,close_status
    INTEGER(int64) :: h(13)
    COMPLEX(DP), ALLOCATABLE :: padding(:)
    code=1
    IF(file_storage_size/=8 .OR. STORAGE_SIZE(0._DP)/=64 .OR. STORAGE_SIZE((0._DP,0._DP))/=128) RETURN
    IF(rank<0 .OR. rank>1 .OR. k<1 .OR. npwx<npw .OR. npw<1 .OR. npol/=2) RETURN
    IF(SIZE(wave,1)/=npwx*npol .OR. SIZE(wave,2)/=48 .OR. SIZE(mill,1)/=3 .OR. SIZE(mill,2)/=npw) RETURN
    IF(SIZE(et,1)/=48 .OR. ANY(SHAPE(et)/=SHAPE(wg)) .OR. ANY(SHAPE(rhor)/=SHAPE(vrs))) RETURN
    IF(SIZE(rhog,2)/=SIZE(rhor,2) .OR. MIN(SIZE(layout),SIZE(et,2),SIZE(rhor,1),SIZE(rhog,1))<1) RETURN
    IF(LEN(fingerprint)/=64 .OR. VERIFY(fingerprint,'0123456789abcdef')/=0) RETURN
    ALLOCATE(padding(npwx-npw),STAT=ios)
    IF(ios/=0) THEN
      code=5;RETURN
    ENDIF
    padding=(0._DP,0._DP)
    h=INT([1,rank,k,npwx,npw,npol,48,SIZE(et,2),SIZE(rhor,1),SIZE(rhor,2),SIZE(rhog,1),SIZE(layout),0],int64)
    h(13)=72623859790382856_int64
    OPEN(NEWUNIT=u,FILE=path,STATUS='new',ACCESS='stream',FORM='unformatted',IOSTAT=ios)
    IF(ios/=0) THEN
      code=2;RETURN
    ENDIF
    WRITE(u,IOSTAT=ios) 'QE75-INITIAL-01 ',h,fingerprint,kpoint,layout,INT(mill,int64)
    IF(ios/=0) GOTO 900
    DO j=1,SIZE(wave,2)
      DO s=1,npol
        ! Unused padded rows are not physical coefficients. Canonicalize the
        ! serialized padding only; never modify evc or copy all source bands.
        WRITE(u,IOSTAT=ios) wave((s-1)*npwx+1:(s-1)*npwx+npw,j),padding
        IF(ios/=0) GOTO 900
      ENDDO
    ENDDO
    DO j=1,SIZE(et,2)
      WRITE(u,IOSTAT=ios) et(:,j),wg(:,j)
      IF(ios/=0) GOTO 900
    ENDDO
    DO j=1,SIZE(rhor,2)
      WRITE(u,IOSTAT=ios) rhor(:,j),rhog(:,j),vrs(:,j)
      IF(ios/=0) GOTO 900
    ENDDO
    CLOSE(u,IOSTAT=close_status)
    code=0
    IF(close_status/=0) code=4
    RETURN
900 CLOSE(u,IOSTAT=close_status)
    code=3
  END SUBROUTINE
END MODULE
