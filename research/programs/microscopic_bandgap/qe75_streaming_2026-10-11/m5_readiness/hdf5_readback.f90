! Serial QE qeh5 I/O component ONLY, not PW/HSE. MPI initialization is trapped;
! the installed parallel-HDF5 library transitively loads an MPI dependency.
PROGRAM readback
  USE kinds, ONLY: DP
  USE qeh5_base_module
  IMPLICIT NONE
  TYPE(qeh5_file) :: f
  TYPE(qeh5_dataset) :: d
  CHARACTER(256) :: input,output,kind
  COMPLEX(DP), ALLOCATABLE :: column(:)
  INTEGER :: npol,igwx,nbnd,j,u
  CALL get_command_argument(1,input)
  CALL get_command_argument(2,output)
  CALL get_command_argument(3,kind)
  ! Initialize QE's private REALDP/SP datatype handles as native PW does;
  ! h5open_f alone is insufficient for qeh5_read_complex.
  CALL initialize_hdf5()
  CALL qeh5_openfile(f,TRIM(input),ACTION='read')
  IF(TRIM(kind)=='wave') THEN
    CALL qeh5_read_attribute(f%id,'npol',npol)
    CALL qeh5_read_attribute(f%id,'igwx',igwx)
    CALL qeh5_read_attribute(f%id,'nbnd',nbnd)
    IF(npol/=2 .OR. igwx<1 .OR. igwx>100000 .OR. nbnd<1 .OR. nbnd>352) ERROR STOP 'bounded wave shape'
    CALL qeh5_open_dataset(f,d,ACTION='read',NAME='evc')
  ELSEIF(TRIM(kind)=='density') THEN
    npol=1;nbnd=1
    CALL qeh5_read_attribute(f%id,'ngm_g',igwx)
    IF(igwx<1 .OR. igwx>100000) ERROR STOP 'bounded density shape'
    CALL qeh5_open_dataset(f,d,ACTION='read',NAME='rhotot_g')
  ELSE
    ERROR STOP 'readback kind'
  ENDIF
  ALLOCATE(column(npol*igwx))
  CALL qeh5_set_space(d,column(1),RANK=1,DIMENSIONS=[npol*igwx],MODE='m')
  OPEN(NEWUNIT=u,FILE=TRIM(output),STATUS='new',ACCESS='stream',FORM='unformatted')
  WRITE(u) npol,igwx,nbnd
  DO j=1,nbnd
    IF(TRIM(kind)=='wave') CALL qeh5_set_file_hyperslab(d,OFFSET=[0,j-1],COUNT=[2*npol*igwx,1])
    CALL qeh5_read_dataset(column,d)
    WRITE(u) column
  ENDDO
  CLOSE(u)
  CALL qeh5_close(d)
  CALL qeh5_close(f)
  CALL finalize_hdf5()
END PROGRAM
SUBROUTINE errore(where,message,code)
  CHARACTER(*), INTENT(IN) :: where,message
  INTEGER, INTENT(IN) :: code
  IF(code==0) RETURN ! Native QE errore() is a no-op for successful status zero.
  PRINT *,where,message,code
  ERROR STOP 'QE HDF5 component refused'
END SUBROUTINE
SUBROUTINE infomsg(where,message)
  CHARACTER(*), INTENT(IN) :: where,message
  PRINT *,where,message
END SUBROUTINE
