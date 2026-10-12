  ! Caller verified/reserved a fresh rank inode after closing the old generation.
  SUBROUTINE qs_begin_reserved(s,path,nr,lo,hi,nq)
    TYPE(exx_qstore), INTENT(INOUT) :: s
    CHARACTER(*), INTENT(IN) :: path
    INTEGER, INTENT(IN) :: nr,lo,hi,nq
    INTEGER :: ios
    INTEGER(int64) :: length
    CHARACTER(256) :: message
    IF(s%opened) CALL fail('reservation import requires closed old generation')
    s%total_units=qs_extent(nr,lo,hi,nq)
    s%vector_units=product(INT(nr,int64),16_int64)
    s%nr=nr;s%lo=lo;s%hi=hi;s%nq=nq
    OPEN(NEWUNIT=s%unit,FILE=path,STATUS='old',ACCESS='stream',FORM='unformatted', &
         ACTION='readwrite',IOSTAT=ios,IOMSG=message)
    IF(ios/=0) CALL fail('reservation open: '//TRIM(message))
    s%opened=.TRUE.;s%sealed=.FALSE.
    INQUIRE(UNIT=s%unit,SIZE=length,IOSTAT=ios)
    IF(ios/=0 .OR. length/=s%total_units) CALL fail('reservation extent refused')
    ALLOCATE(s%written(lo:hi,nq));s%written=.FALSE.
  END SUBROUTINE
