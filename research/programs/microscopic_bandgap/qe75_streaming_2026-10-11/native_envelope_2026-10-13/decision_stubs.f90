! Serial counterexample model only. No MPI and no native authority.
MODULE mp_world
  INTEGER :: mpime=0,nproc=2,world_comm=17
END MODULE
MODULE decision_fixture
  INTEGER :: scenario=0,action=0
END MODULE
MODULE mp
CONTAINS
  SUBROUTINE mp_max(code,comm)
    USE decision_fixture
    INTEGER, INTENT(INOUT) :: code
    INTEGER, INTENT(IN) :: comm
    ! Model a second rank with status zero. MPI_MAX can mask a negative code.
    code=MAX(code,0)
    WRITE(*,*)'REDUCE',action,code,comm
  END SUBROUTINE
  SUBROUTINE mp_barrier(comm)
    INTEGER, INTENT(IN) :: comm
    WRITE(*,*)'BARRIER',comm
  END SUBROUTINE
END MODULE
FUNCTION qe75_lease_call(rank,size,op,scope) RESULT(code) BIND(C,NAME='qe75_lease_call')
  USE iso_c_binding, ONLY:c_int
  USE decision_fixture
  INTEGER(c_int), VALUE :: rank,size,op,scope
  INTEGER(c_int) :: code
  action=op;code=0
  IF(scenario==1)code=-13
  IF(scenario==2)code=-HUGE(code)-1
  IF(scenario==3)code=13
  WRITE(*,*)'SERIAL_MODEL_NO_AUTHORITY',rank,size,op,scope,code
END FUNCTION
SUBROUTINE errore(where,message,code)
  CHARACTER(*), INTENT(IN) :: where,message
  INTEGER, INTENT(IN) :: code
  WRITE(*,*)'REFUSE',where,message,code
  STOP 88
END SUBROUTINE
