PROGRAM collective_unit
  USE decision_fixture
  USE mp_world
  USE qe75_native_lease,ONLY:native_register
  IMPLICIT NONE
  CHARACTER(32) :: arg
  CALL get_command_argument(1,arg);READ(arg,*)scenario
  CALL get_command_argument(2,arg);READ(arg,*)mpime
  IF(scenario==4)nproc=3
  CALL native_register()
  WRITE(*,*)'SERIAL_DECISION_ACCEPT_NOT_NATIVE_AUTHORITY'
END PROGRAM
