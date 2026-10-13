! Isolated pristine qeh5 writer schema check. NO PW, FFT or MPI initialization.
PROGRAM schema_unit
  USE kinds, ONLY: DP
  USE qeh5_base_module
  IMPLICIT NONE
  TYPE(qeh5_file) :: f
  TYPE(qeh5_dataset) :: d
  CHARACTER(1024) :: path
  CHARACTER(32) :: arg,kind
  CHARACTER(10) :: names(4)=['rhotot_g  ','m_x       ','m_y       ','m_z       ']
  INTEGER :: n,j,i
  INTEGER, ALLOCATABLE :: mill(:,:)
  COMPLEX(DP), ALLOCATABLE :: column(:)
  REAL(DP) :: b(3)=[1.0_DP,2.0_DP,3.0_DP]
  CALL get_command_argument(1,path)
  CALL get_command_argument(2,arg);READ(arg,*) n
  CALL get_command_argument(3,kind)
  IF(n<1 .OR. n>257) STOP 1
  CALL initialize_hdf5()
  CALL qeh5_openfile(f,TRIM(path),ACTION='write')
  CALL qeh5_add_attribute(f%id,'gamma_only','.FALSE.')
  IF(TRIM(kind)=='wave') THEN
    CALL qeh5_add_attribute(f%id,'ik',1)
    CALL qeh5_add_attribute(f%id,'xk',b,1,[3])
    CALL qeh5_add_attribute(f%id,'ispin',1)
    CALL qeh5_add_attribute(f%id,'scale_factor',1.0_DP)
    CALL qeh5_add_attribute(f%id,'ngw',n)
    CALL qeh5_add_attribute(f%id,'igwx',n)
    CALL qeh5_add_attribute(f%id,'npol',2)
    CALL qeh5_add_attribute(f%id,'nbnd',48)
  ELSEIF(TRIM(kind)=='density') THEN
    CALL qeh5_add_attribute(f%id,'ngm_g',n)
    CALL qeh5_add_attribute(f%id,'nspin',4)
  ELSE
    STOP 2
  ENDIF
  ALLOCATE(mill(3,n));mill=RESHAPE([(i,i=1,3*n)],[3,n])
  CALL qeh5_set_space(d,mill(1,1),RANK=2,DIMENSIONS=[3,n])
  CALL qeh5_open_dataset(f,d,ACTION='write',NAME='MillerIndices')
  CALL qeh5_add_attribute(d%id,'bg1',b,1,[3])
  CALL qeh5_add_attribute(d%id,'bg2',b,1,[3])
  CALL qeh5_add_attribute(d%id,'bg3',b,1,[3])
  IF(TRIM(kind)=='wave') CALL qeh5_add_attribute(d%id,'doc', &
       'Miller Indices of the wave-vectors, same ordering as wave-function components')
  CALL qeh5_write_dataset(mill,d);CALL qeh5_close(d)
  DEALLOCATE(mill)
  IF(TRIM(kind)=='wave') THEN
    ALLOCATE(column(2*n));column=CMPLX(1.0_DP,2.0_DP,DP)
    CALL qeh5_set_space(d,column(1),2,[2*n,48],MODE='f')
    CALL qeh5_set_space(d,column(1),1,[2*n],MODE='m')
    CALL qeh5_open_dataset(f,d,ACTION='write',NAME='evc')
    CALL qeh5_add_attribute(d%id,'doc:','Wave Functions, (npwx,nbnd), each contiguous line represents a wave function,  '// &
         'each complex coefficient is given by a couple of contiguous floats')
    DO j=1,48
      CALL qeh5_set_file_hyperslab(d,OFFSET=[0,j-1],COUNT=[4*n,1])
      CALL qeh5_write_dataset(column,d)
    ENDDO
    CALL qeh5_close(d)
  ELSE
    ALLOCATE(column(n));column=CMPLX(1.0_DP,2.0_DP,DP)
    DO j=1,4
      CALL qeh5_set_space(d,column(1),1,[n])
      CALL qeh5_open_dataset(f,d,ACTION='write',NAME=TRIM(names(j)))
      CALL qeh5_write_dataset(column,d);CALL qeh5_close(d)
    ENDDO
  ENDIF
  DEALLOCATE(column);CALL qeh5_close(f);CALL finalize_hdf5()
  PRINT *, 'SERIAL_QEH5_SCHEMA_NO_PW_NO_MPI'
END PROGRAM
SUBROUTINE errore(where,message,code)
  CHARACTER(*), INTENT(IN) :: where,message
  INTEGER, INTENT(IN) :: code
  IF(code==0) RETURN
  PRINT *,where,message,code
  ERROR STOP 'serial qeh5 error'
END SUBROUTINE
SUBROUTINE infomsg(where,message)
  CHARACTER(*), INTENT(IN) :: where,message
  PRINT *,where,message
END SUBROUTINE
