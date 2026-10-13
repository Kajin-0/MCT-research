PROGRAM fft_unit
  USE fft_support, ONLY: good_fft_order,good_fft_dimension
  USE iso_fortran_env, ONLY: int64
  IMPLICIT NONE
  INTEGER :: i,u,n2
  CHARACTER(1024) :: path
  CALL get_command_argument(1,path)
  OPEN(NEWUNIT=u,FILE=TRIM(path),STATUS='new',ACCESS='stream',FORM='unformatted')
  DO i=1,512
    n2=0
    IF(i>=2)n2=good_fft_order(i,2)
    WRITE(u)INT([i,good_fft_order(i),n2,good_fft_dimension(i)],int64)
  ENDDO
  CLOSE(u)
END PROGRAM
SUBROUTINE fftx_error__(where,message,code)
  CHARACTER(*), INTENT(IN) :: where,message
  INTEGER, INTENT(IN) :: code
  WRITE(*,*)where,message,code
  ERROR STOP 'pristine FFT support error'
END SUBROUTINE
