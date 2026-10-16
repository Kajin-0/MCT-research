! GPL-2.0-or-later. Uses actual QE world identity; never environment rank.
SUBROUTINE r07_static_phase(stage,extent)
 USE iso_c_binding,ONLY:c_int,c_int64_t
 USE mp_world,ONLY:mpime,nproc,world_comm
 USE mp,ONLY:mp_max,mp_barrier
 IMPLICIT NONE
 INTEGER,INTENT(IN)::stage
 INTEGER(c_int64_t),INTENT(IN)::extent
 INTEGER::code
 INTERFACE
  INTEGER(c_int) FUNCTION lease(rank,size,action,nbytes) BIND(C,NAME='r07_static_lease')
   IMPORT c_int,c_int64_t
   INTEGER(c_int),VALUE::rank,size,action
   INTEGER(c_int64_t),VALUE::nbytes
  END FUNCTION
 END INTERFACE
 IF(nproc/=2)CALL errore('r07_static_phase','two actual world ranks required',1)
 code=lease(INT(mpime,c_int),INT(nproc,c_int),INT(stage,c_int),extent)
 ! The C ABI returns nonnegative errno; normalize even a broken signed result.
 IF(code<0)code=1
 CALL mp_max(code,world_comm)
 IF(code/=0)CALL errore('r07_static_phase','authenticated native phase refused',1)
 CALL mp_barrier(world_comm)
END SUBROUTINE
