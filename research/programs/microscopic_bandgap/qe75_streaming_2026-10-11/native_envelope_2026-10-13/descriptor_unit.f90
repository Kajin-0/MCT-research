! SERIAL codec fixture against the REAL QE descriptor type. No MPI init.
PROGRAM descriptor_unit
  USE iso_fortran_env, ONLY: int64
  USE fft_types, ONLY: fft_type_descriptor
  USE qe75_resource_descriptor, ONLY: resource_write
  IMPLICIT NONE
  TYPE(fft_type_descriptor) :: d
  INTEGER :: rank,code
  CHARACTER(1024) :: path
  CHARACTER(64) :: profile,common
  CHARACTER(16) :: arg
  CALL get_command_argument(1,path)
  CALL get_command_argument(2,arg);READ(arg,*) rank
  CALL get_command_argument(3,profile)
  CALL get_command_argument(4,common)
  d%nr1=4;d%nr2=4;d%nr3=5;d%nr1x=4;d%nr2x=4;d%nr3x=5
  d%nproc=2;d%nproc2=1;d%nproc3=2;d%mype=rank;d%mype2=0;d%mype3=rank
  d%my_nr2p=4;d%my_nr3p=3-rank;d%my_i0r2p=0;d%my_i0r3p=3*rank
  d%nnr=16*(3-rank);d%nnp=16;d%nnr_tg=0
  ALLOCATE(d%nr2p(1),d%nr3p(2),d%i0r2p(1),d%i0r3p(2),d%nl(3))
  d%nr2p=[4];d%nr3p=[3,2];d%i0r2p=[0];d%i0r3p=[0,3];d%nl=[1,2,3]
  CALL resource_write(TRIM(path),profile,common,rank,2, &
       [3_int64,2_int64,48_int64,8_int64,8_int64,8_int64,8_int64,3_int64,3_int64,4_int64,8_int64,1_int64],d,d,d,code)
  IF(code/=0) STOP 41
  ! Collision fails locally instead of replacing even a synthetic observation.
  CALL resource_write(TRIM(path),profile,common,rank,2, &
       [3_int64,2_int64,48_int64,8_int64,8_int64,8_int64,8_int64,3_int64,3_int64,4_int64,8_int64,1_int64],d,d,d,code)
  IF(code==0) STOP 42
  PRINT *, 'SERIAL_REAL_TYPE_NO_MPI_CODEC_PASS'
END PROGRAM
