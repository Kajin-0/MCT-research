! GPL-2.0-or-later. Read-only initial-state capture; never generates SCF waves.
MODULE qe75_initial_state
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64,file_storage_size
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: initial_write
CONTAINS
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
