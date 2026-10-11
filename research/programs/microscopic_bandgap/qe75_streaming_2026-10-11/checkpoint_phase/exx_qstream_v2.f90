! Copyright (C) 2026 MCT-research contributors.
! GPL-2.0-or-later, compatible with Quantum ESPRESSO's License.
! Storage-only checkpoint adapter. NOT a qualified native QE restart bridge.
MODULE exx_qstream
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64, file_storage_size
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: exx_qstore, qs_begin, qs_put, qs_seal, qs_load, qs_close, qs_extent, qs_restore_readonly
  TYPE exx_qstore
    PRIVATE
    INTEGER :: unit = 0, nr = 0, lo = 0, hi = -1, nq = 0
    INTEGER(int64) :: vector_units = 0, total_units = 0
    LOGICAL :: opened = .FALSE., sealed = .FALSE.
    LOGICAL, ALLOCATABLE :: written(:,:)
  END TYPE
CONTAINS
  SUBROUTINE fail(message)
    CHARACTER(*), INTENT(IN) :: message
    CALL errore('exx_qstream', message, 1)
    ! QE errore is nonreturning for code > 0; no ignored I/O failure.
    ERROR STOP 'exx_qstream: errore unexpectedly returned'
  END SUBROUTINE

  FUNCTION product(a,b) RESULT(c)
    INTEGER(int64), INTENT(IN) :: a,b
    INTEGER(int64) :: c
    IF (a <= 0 .OR. b <= 0) CALL fail('nonpositive storage extent')
    IF (a > HUGE(a)/b) CALL fail('64-bit storage offset overflow')
    c = a*b
  END FUNCTION

  FUNCTION qs_extent(nr,lo,hi,nq) RESULT(total)
    INTEGER, INTENT(IN) :: nr,lo,hi,nq
    INTEGER(int64) :: total, stride
    COMPLEX(DP) :: sample
    INTEGER :: units
    IF (nr <= 0 .OR. lo < 1 .OR. hi < lo .OR. nq <= 0) CALL fail('invalid store shape')
    INQUIRE(IOLENGTH=units) sample
    IF (file_storage_size /= 8 .OR. units /= 16) CALL fail('requires 16-byte complex DP and byte stream units')
    stride = product(INT(nr,int64), INT(units,int64))
    total = product(product(stride, INT(hi,int64)-INT(lo,int64)+1_int64), INT(nq,int64))
    ! The final POS is at most total; reserve one for the offset formula.
    IF (total == HUGE(total)) CALL fail('64-bit storage position overflow')
  END FUNCTION

  SUBROUTINE qs_begin(s,path,nr,lo,hi,nq)
    TYPE(exx_qstore), INTENT(INOUT) :: s
    CHARACTER(*), INTENT(IN) :: path
    INTEGER, INTENT(IN) :: nr,lo,hi,nq
    INTEGER :: ios
    LOGICAL :: exists
    CHARACTER(256) :: message
    CALL qs_close(s)
    s%total_units = qs_extent(nr,lo,hi,nq)
    s%vector_units = product(INT(nr,int64),16_int64)
    s%nr=nr; s%lo=lo; s%hi=hi; s%nq=nq
    INQUIRE(FILE=path, EXIST=exists)
    IF (exists) CALL fail('refusing pre-existing stream file; require unique fresh outdir')
    OPEN(NEWUNIT=s%unit, FILE=path, STATUS='new', ACCESS='stream', FORM='unformatted', &
         ACTION='readwrite', IOSTAT=ios, IOMSG=message)
    IF (ios /= 0) CALL fail('open: '//TRIM(message))
    s%opened=.TRUE.; s%sealed=.FALSE.
    ALLOCATE(s%written(lo:hi,nq)); s%written=.FALSE.
  END SUBROUTINE

  SUBROUTINE qs_put(s,q,b,vector)
    TYPE(exx_qstore), INTENT(INOUT) :: s
    INTEGER, INTENT(IN) :: q,b
    COMPLEX(DP), CONTIGUOUS, INTENT(IN) :: vector(:)
    INTEGER :: ios
    INTEGER(int64) :: offset
    CHARACTER(256) :: message
    IF (.NOT.s%opened .OR. s%sealed) CALL fail('put requires unsealed open generation')
    IF (q < 1 .OR. q > s%nq .OR. b < s%lo .OR. b > s%hi) CALL fail('put index outside store')
    IF (SIZE(vector) /= s%nr) CALL fail('put vector shape mismatch')
    IF (s%written(b,q)) CALL fail('duplicate producer vector')
    offset = (INT(q-1,int64)*(INT(s%hi,int64)-INT(s%lo,int64)+1_int64)+INT(b-s%lo,int64))*s%vector_units
    WRITE(s%unit, POS=offset+1_int64, IOSTAT=ios, IOMSG=message) vector
    IF (ios /= 0) CALL fail('write: '//TRIM(message))
    s%written(b,q)=.TRUE.
  END SUBROUTINE

  SUBROUTINE qs_seal(s)
    TYPE(exx_qstore), INTENT(INOUT) :: s
    INTEGER :: ios
    INTEGER(int64) :: length
    CHARACTER(256) :: message
    IF (.NOT.s%opened .OR. s%sealed) CALL fail('seal requires unsealed open generation')
    IF (.NOT.ALL(s%written)) CALL fail('missing producer vectors')
    FLUSH(s%unit, IOSTAT=ios, IOMSG=message)
    IF (ios /= 0) CALL fail('flush: '//TRIM(message))
    length=-1_int64
    INQUIRE(UNIT=s%unit, SIZE=length, IOSTAT=ios)
    IF (ios /= 0 .OR. length /= s%total_units) CALL fail('unexpected stream extent')
    s%sealed=.TRUE.
  END SUBROUTINE

  SUBROUTINE qs_load(s,q,plane)
    TYPE(exx_qstore), INTENT(INOUT) :: s
    INTEGER, INTENT(IN) :: q
    COMPLEX(DP), CONTIGUOUS, INTENT(OUT) :: plane(:,:)
    INTEGER :: ios
    INTEGER(int64) :: offset
    CHARACTER(256) :: message
    IF (.NOT.s%opened .OR. .NOT.s%sealed) CALL fail('load requires sealed generation')
    IF (q < 1 .OR. q > s%nq) CALL fail('load q outside store')
    IF (SIZE(plane,1) /= s%nr .OR. INT(SIZE(plane,2),int64) /= INT(s%hi,int64)-INT(s%lo,int64)+1_int64) &
      CALL fail('load plane shape mismatch')
    offset = INT(q-1,int64)*s%vector_units*(INT(s%hi,int64)-INT(s%lo,int64)+1_int64)
    ! One contiguous plane, no whole-store temporary, compression or conversion.
    READ(s%unit, POS=offset+1_int64, IOSTAT=ios, IOMSG=message) plane
    IF (ios /= 0) CALL fail('read: '//TRIM(message))
  END SUBROUTINE

  SUBROUTINE qs_close(s,keep)
    TYPE(exx_qstore), INTENT(INOUT) :: s
    LOGICAL, OPTIONAL, INTENT(IN) :: keep
    CHARACTER(6) :: disposition
    INTEGER :: ios
    CHARACTER(256) :: message
    IF (s%opened) THEN
      disposition='delete'
      IF (PRESENT(keep)) THEN
        IF (keep) disposition='keep'
      ENDIF
      CLOSE(s%unit, STATUS=TRIM(disposition), IOSTAT=ios, IOMSG=message)
      IF (ios /= 0) CALL fail('close: '//TRIM(message))
    ENDIF
    IF (ALLOCATED(s%written)) DEALLOCATE(s%written)
    s%opened=.FALSE.; s%sealed=.FALSE.
    s%nr=0; s%lo=0; s%hi=-1; s%nq=0
    s%vector_units=0; s%total_units=0
  END SUBROUTINE
  ! Caller must validate/adopt a Capsule receipt before this storage-only API.
  ! The pathname is an owned active hard link, never the committed generation.
  ! Sealed read-only import forbids writes; full native QE state is not restored.
  SUBROUTINE qs_restore_readonly(s,path,nr,lo,hi,nq)
    TYPE(exx_qstore), INTENT(INOUT) :: s
    CHARACTER(*), INTENT(IN) :: path
    INTEGER, INTENT(IN) :: nr,lo,hi,nq
    INTEGER :: ios
    INTEGER(int64) :: length
    CHARACTER(256) :: message
    CALL qs_close(s)
    s%total_units=qs_extent(nr,lo,hi,nq)
    s%vector_units=product(INT(nr,int64),16_int64)
    s%nr=nr; s%lo=lo; s%hi=hi; s%nq=nq
    OPEN(NEWUNIT=s%unit,FILE=path,STATUS='old',ACCESS='stream',FORM='unformatted', &
         ACTION='read',IOSTAT=ios,IOMSG=message)
    IF(ios/=0) CALL fail('checkpoint open: '//TRIM(message))
    s%opened=.TRUE.; length=-1_int64
    INQUIRE(UNIT=s%unit,SIZE=length,IOSTAT=ios)
    IF(ios/=0 .OR. length/=s%total_units) CALL fail('checkpoint extent/layout mismatch')
    s%sealed=.TRUE.
  END SUBROUTINE
END MODULE
