! GPL-2.0-or-later. Real QE mp_world metadata, not arguments or environment rank.
MODULE qe75_native_lease
  USE iso_c_binding, ONLY: c_int
  USE mp_world, ONLY: mpime,nproc,world_comm
  USE mp, ONLY: mp_max,mp_barrier
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: native_register,native_check
  INTERFACE
    INTEGER(c_int) FUNCTION lease_call(rank,size,action,scope) BIND(C,NAME='qe75_lease_call')
      IMPORT c_int
      INTEGER(c_int), VALUE :: rank,size,action,scope
    END FUNCTION
  END INTERFACE
CONTAINS
  SUBROUTINE native_register()
    INTEGER :: code
    IF(nproc/=2) CALL errore('native_register','exact two-world-rank scope required',1)
    code=lease_call(INT(mpime,c_int),INT(nproc,c_int),1_c_int,2_c_int)
    CALL mp_max(code,world_comm)
    IF(code/=0) CALL errore('native_register','live typed native lease refused',1)
    CALL mp_barrier(world_comm)
    CALL native_check()
  END SUBROUTINE
  SUBROUTINE native_check()
    INTEGER :: code
    code=lease_call(INT(mpime,c_int),INT(nproc,c_int),2_c_int,2_c_int)
    CALL mp_max(code,world_comm)
    IF(code/=0) CALL errore('native_check','all-rank native receipt absent/lost',1)
    CALL mp_barrier(world_comm)
  END SUBROUTINE
END MODULE
