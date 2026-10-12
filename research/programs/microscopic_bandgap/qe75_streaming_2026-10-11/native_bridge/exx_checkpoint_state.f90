! GPL-2.0-or-later. Private QE 7.5 CPU/NC/one-pool ACE checkpoint codec.
! Exact native encoding, NOT portable across compiler/endianness/layout changes.
MODULE exx_checkpoint_state
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64, file_storage_size
  USE ieee_arithmetic, ONLY: ieee_is_finite
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: bridge_write, bridge_read, bridge_extent, bridge_outer, bridge_pending
  CHARACTER(16), PARAMETER :: magic='QE75-EXX-STATE02'
  INTEGER(int64), PARAMETER :: version=2_int64, sentinel=72623859790382856_int64
  INTEGER, PARAMETER :: ns=9
  LOGICAL :: bridge_pending=.FALSE.
  TYPE bridge_outer
    INTEGER :: iter=0, mode=0
    ! tr2, dexx, exxen, fock0, fock1, fock2, fock3, tr2_final, ethr
    REAL(DP) :: scalar(ns)=0._DP
  END TYPE
CONTAINS
  SUBROUTINE die(message)
    CHARACTER(*), INTENT(IN) :: message
    CALL errore('exx_checkpoint_state',message,1)
    ERROR STOP 'nonreturning QE errore returned'
  END SUBROUTINE

  FUNCTION mul(a,b) RESULT(c)
    INTEGER(int64), INTENT(IN) :: a,b
    INTEGER(int64) :: c
    IF(a<0 .OR. b<0) CALL die('negative extent')
    IF(b>0) THEN
      IF(a>HUGE(a)/b) CALL die('extent overflow')
    ENDIF
    c=a*b
  END FUNCTION

  FUNCTION plus(a,b) RESULT(c)
    INTEGER(int64), INTENT(IN) :: a,b
    INTEGER(int64) :: c
    IF(a<0 .OR. b<0) CALL die('negative extent')
    IF(a>HUGE(a)-b) CALL die('extent overflow')
    c=a+b
  END FUNCTION

  FUNCTION bridge_extent(nlayout,no1,no2,nw1,nw2,nx1,nx2,nx3) RESULT(n)
    INTEGER, INTENT(IN) :: nlayout,no1,no2,nw1,nw2,nx1,nx2,nx3
    INTEGER(int64) :: n
    IF(MIN(nlayout,no1,no2,nw1,nw2,nx1,nx2,nx3)<=0) CALL die('invalid shape')
    ! magic, nine header int64s, fingerprint, layout, mode/iter, nine scalars
    n=plus(16_int64+9_int64*8+64+2*8+ns*8,mul(INT(nlayout,int64),8_int64))
    n=plus(n,mul(mul(INT(no1,int64),INT(no2,int64)),8_int64))
    n=plus(n,mul(mul(INT(nw1,int64),INT(nw2,int64)),16_int64)) ! wg plus et
    n=plus(n,mul(mul(mul(INT(nx1,int64),INT(nx2,int64)),INT(nx3,int64)),16_int64))
  END FUNCTION

  SUBROUTINE check_encoding()
    COMPLEX(DP) :: c
    REAL(DP) :: r
    INTEGER :: nc,nr
    INQUIRE(IOLENGTH=nc) c
    INQUIRE(IOLENGTH=nr) r
    IF(file_storage_size/=8 .OR. nc/=16 .OR. nr/=8) CALL die('native encoding unsupported')
  END SUBROUTINE

  SUBROUTINE fingerprint_ok(fingerprint)
    CHARACTER(*), INTENT(IN) :: fingerprint
    INTEGER :: i
    IF(LEN(fingerprint)/=64) CALL die('fingerprint must be 64 hex characters')
    DO i=1,64
      IF(INDEX('0123456789abcdef',fingerprint(i:i))==0) CALL die('invalid fingerprint')
    ENDDO
  END SUBROUTINE

  SUBROUTINE bridge_write(path,fingerprint,layout,outer,occ,wg,et,xi)
    CHARACTER(*), INTENT(IN) :: path,fingerprint
    INTEGER(int64), INTENT(IN) :: layout(:)
    TYPE(bridge_outer), INTENT(IN) :: outer
    REAL(DP), CONTIGUOUS, INTENT(IN) :: occ(:,:),wg(:,:),et(:,:)
    COMPLEX(DP), CONTIGUOUS, INTENT(IN) :: xi(:,:,:)
    INTEGER :: u,ios,j,k
    INTEGER(int64) :: header(9), n
    CALL check_encoding()
    CALL fingerprint_ok(fingerprint)
    IF(ANY(SHAPE(wg)/=SHAPE(et))) CALL die('wg/et shape mismatch')
    IF(outer%iter<0 .OR. (outer%mode/=1 .AND. outer%mode/=2)) CALL die('invalid stop state')
    IF(.NOT.ALL(ieee_is_finite(outer%scalar))) CALL die('nonfinite outer state')
    n=bridge_extent(SIZE(layout),SIZE(occ,1),SIZE(occ,2),SIZE(wg,1),SIZE(wg,2), &
                    SIZE(xi,1),SIZE(xi,2),SIZE(xi,3))
    header=[version,sentinel,INT(SIZE(layout),int64),INT(SIZE(occ,1),int64), &
            INT(SIZE(occ,2),int64),INT(SIZE(wg,1),int64),INT(SIZE(wg,2),int64), &
            INT(SIZE(xi,1),int64),INT(SIZE(xi,3),int64)]
    ! nx2 equals nw1 (all source/ACE bands are retained).
    IF(SIZE(xi,2)/=SIZE(wg,1)) CALL die('full-band ACE required')
    OPEN(NEWUNIT=u,FILE=path,STATUS='new',ACCESS='stream',FORM='unformatted',IOSTAT=ios)
    IF(ios/=0) CALL die('state open refused: require owned fresh name')
    WRITE(u,IOSTAT=ios) magic,header,fingerprint,layout, &
                        INT(outer%mode,int64),INT(outer%iter,int64),outer%scalar
    IF(ios/=0) CALL die('state header write failed')
    DO j=1,SIZE(occ,2)
      WRITE(u,IOSTAT=ios) occ(:,j)
      IF(ios/=0) CALL die('occupation write failed')
    ENDDO
    DO j=1,SIZE(wg,2)
      WRITE(u,IOSTAT=ios) wg(:,j),et(:,j)
      IF(ios/=0) CALL die('current wg/et write failed')
    ENDDO
    ! No xi-sized temporary or copy of the q store: one already resident column.
    DO k=1,SIZE(xi,3)
      DO j=1,SIZE(xi,2)
        WRITE(u,IOSTAT=ios) xi(:,j,k)
        IF(ios/=0) CALL die('old ACE write failed')
      ENDDO
    ENDDO
    FLUSH(u,IOSTAT=ios)
    IF(ios/=0) CALL die('state flush failed')
    CLOSE(u,IOSTAT=ios)
    IF(ios/=0) CALL die('state close failed')
    INQUIRE(FILE=path,SIZE=header(1),IOSTAT=ios)
    IF(ios/=0 .OR. header(1)/=n) CALL die('state extent mismatch')
    ! Pending is set only after the entire rank packet is closed. fsync and
    ! the all-rank commit belong to the post-punch coordinator, not FLUSH.
    bridge_pending=.TRUE.
  END SUBROUTINE

  SUBROUTINE bridge_read(path,fingerprint,layout,outer,occ,wg,et,xi)
    CHARACTER(*), INTENT(IN) :: path,fingerprint
    INTEGER(int64), INTENT(IN) :: layout(:)
    TYPE(bridge_outer), INTENT(OUT) :: outer
    REAL(DP), CONTIGUOUS, INTENT(OUT) :: occ(:,:),wg(:,:),et(:,:)
    COMPLEX(DP), CONTIGUOUS, INTENT(OUT) :: xi(:,:,:)
    INTEGER :: u,ios,j,k
    INTEGER(int64) :: header(9), expected(9),n,length,mode,iter
    INTEGER(int64), ALLOCATABLE :: saved_layout(:)
    CHARACTER(16) :: saved_magic
    CHARACTER(64) :: saved_fingerprint
    CALL check_encoding()
    CALL fingerprint_ok(fingerprint)
    IF(ANY(SHAPE(wg)/=SHAPE(et)) .OR. SIZE(xi,2)/=SIZE(wg,1)) CALL die('restore shape mismatch')
    n=bridge_extent(SIZE(layout),SIZE(occ,1),SIZE(occ,2),SIZE(wg,1),SIZE(wg,2), &
                    SIZE(xi,1),SIZE(xi,2),SIZE(xi,3))
    expected=[version,sentinel,INT(SIZE(layout),int64),INT(SIZE(occ,1),int64), &
              INT(SIZE(occ,2),int64),INT(SIZE(wg,1),int64),INT(SIZE(wg,2),int64), &
              INT(SIZE(xi,1),int64),INT(SIZE(xi,3),int64)]
    OPEN(NEWUNIT=u,FILE=path,STATUS='old',ACTION='read',ACCESS='stream',FORM='unformatted',IOSTAT=ios)
    IF(ios/=0) CALL die('state restore open failed')
    INQUIRE(UNIT=u,SIZE=length,IOSTAT=ios)
    IF(ios/=0 .OR. length/=n) CALL die('truncated/extended state')
    READ(u,IOSTAT=ios) saved_magic,header,saved_fingerprint
    IF(ios/=0) CALL die('state header read failed')
    IF(saved_magic/=magic .OR. ANY(header/=expected)) CALL die('version/encoding/dimensions refused')
    IF(saved_fingerprint/=fingerprint) CALL die('source/physics/layout fingerprint refused')
    ALLOCATE(saved_layout(SIZE(layout)))
    READ(u,IOSTAT=ios) saved_layout,mode,iter,outer%scalar
    IF(ios/=0) CALL die('state layout read failed')
    IF(ANY(saved_layout/=layout)) CALL die('actual rank/FFT/G-map layout refused')
    DEALLOCATE(saved_layout)
    IF(iter<0 .OR. iter>HUGE(outer%iter) .OR. (mode/=1 .AND. mode/=2)) CALL die('invalid stop counter')
    IF(.NOT.ALL(ieee_is_finite(outer%scalar))) CALL die('nonfinite restored outer state')
    outer%iter=INT(iter); outer%mode=INT(mode)
    ! Full-file SHA-256 and ownership must already have passed before QE's
    ! first native restart read. Header checks alone are NOT integrity checks.
    DO j=1,SIZE(occ,2)
      READ(u,IOSTAT=ios) occ(:,j)
      IF(ios/=0) CALL die('occupation read failed')
    ENDDO
    DO j=1,SIZE(wg,2)
      READ(u,IOSTAT=ios) wg(:,j),et(:,j)
      IF(ios/=0) CALL die('current wg/et read failed')
    ENDDO
    DO k=1,SIZE(xi,3)
      DO j=1,SIZE(xi,2)
        READ(u,IOSTAT=ios) xi(:,j,k)
        IF(ios/=0) CALL die('old ACE read failed')
      ENDDO
    ENDDO
    CLOSE(u,IOSTAT=ios)
    IF(ios/=0) CALL die('state restore close failed')
    bridge_pending=.FALSE.
  END SUBROUTINE
END MODULE
