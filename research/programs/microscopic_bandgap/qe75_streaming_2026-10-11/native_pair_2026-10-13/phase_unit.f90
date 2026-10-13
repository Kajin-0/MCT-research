PROGRAM phase_unit
  USE qe75_native_lease, ONLY: native_phase
  INTEGER :: stage
  CHARACTER(32) :: arg
  CALL get_command_argument(1,arg)
  READ(arg,*) stage
  CALL native_phase(stage)
  WRITE(*,*) 'SERIAL_MODEL_ONLY_NO_AUTHORITY'
END PROGRAM
