! Serial decision stubs. NOT MPI; NOT a live phase receipt.
MODULE mp_world
  INTEGER :: mpime=0,nproc=2,world_comm=77
END MODULE
MODULE mp
CONTAINS
  SUBROUTINE mp_max(code,comm)
    INTEGER, INTENT(INOUT) :: code
    INTEGER, INTENT(IN) :: comm
    CHARACTER(32) :: remote
    INTEGER :: r
    CALL get_environment_variable('TEST_REMOTE_FAILURE',remote)
    READ(remote,*) r
    IF(comm/=77 .OR. (code/=0 .AND. code/=1)) ERROR STOP 'invalid collective indicator'
    code=MAX(code,r)
    WRITE(*,*) 'SERIAL_MODEL_MAX',code
  END SUBROUTINE
  SUBROUTINE mp_barrier(comm)
    INTEGER, INTENT(IN) :: comm
    IF(comm/=77) ERROR STOP 'wrong communicator'
    WRITE(*,*) 'SERIAL_MODEL_BARRIER'
  END SUBROUTINE
END MODULE
FUNCTION serial_phase_call(rank,size,action,scope) RESULT(code) BIND(C,NAME='qe75_lease_call')
  USE iso_c_binding, ONLY: c_int
  INTEGER(c_int), VALUE :: rank,size,action,scope
  INTEGER(c_int) :: code
  CHARACTER(32) :: value
  IF(rank/=0 .OR. size/=2 .OR. scope/=4 .OR. action<4 .OR. action>7) ERROR STOP 'typed phase'
  CALL get_environment_variable('TEST_LOCAL_STATUS',value)
  READ(value,*) code
  WRITE(*,*) 'SERIAL_MODEL_PHASE',action,scope
END FUNCTION
SUBROUTINE errore(name,message,code)
  CHARACTER(*), INTENT(IN) :: name,message
  INTEGER, INTENT(IN) :: code
  WRITE(*,*) 'SERIAL_MODEL_REFUSAL',name,message,code
  STOP 91
END SUBROUTINE
