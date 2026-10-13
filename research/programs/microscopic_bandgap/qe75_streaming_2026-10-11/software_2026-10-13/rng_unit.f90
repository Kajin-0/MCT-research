PROGRAM rng_unit
  USE kinds, ONLY: DP
  USE random_numbers, ONLY: randy
  IMPLICIT NONE
  REAL(DP) :: values(128),discard
  INTEGER :: i,u,mode
  CHARACTER(1024) :: path,arg
  CALL get_command_argument(1,path);CALL get_command_argument(2,arg);READ(arg,*)mode
  IF(mode==1) discard=randy() ! equal default seed is insufficient if history differs
  DO i=1,128;values(i)=randy();ENDDO
  OPEN(NEWUNIT=u,FILE=TRIM(path),STATUS='new',ACCESS='stream',FORM='unformatted')
  WRITE(u)values;CLOSE(u)
END PROGRAM
SUBROUTINE errore(where,message,code)
  CHARACTER(*), INTENT(IN) :: where,message
  INTEGER, INTENT(IN) :: code
  WRITE(*,*)where,message,code
  ERROR STOP 'pristine RNG component error'
END SUBROUTINE
