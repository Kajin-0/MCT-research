! GPL-2.0-or-later. Real fallocated inode -> storage producer serial unit.
PROGRAM reserved_unit
  USE kinds, ONLY: DP
  USE exx_qstream
  IMPLICIT NONE
  TYPE(exx_qstore) :: store
  CHARACTER(1024) :: path
  COMPLEX(DP) :: vector(3),plane(3,2)
  INTEGER :: q,b
  CALL get_command_argument(1,path)
  CALL qs_begin_reserved(store,TRIM(path),3,1,2,2)
  DO q=1,2
    DO b=1,2
      vector=CMPLX(q,b,DP)
      CALL qs_put(store,q,b,vector)
    ENDDO
  ENDDO
  CALL qs_seal(store)
  DO q=1,2
    CALL qs_load(store,q,plane)
    DO b=1,2
      IF(ANY(plane(:,b)/=CMPLX(q,b,DP))) ERROR STOP 'reserved roundtrip mismatch'
    ENDDO
  ENDDO
  CALL qs_close(store)
  PRINT *, 'RESERVED_STORE_PASS'
END PROGRAM

SUBROUTINE errore(where,message,code)
  CHARACTER(*), INTENT(IN) :: where,message
  INTEGER, INTENT(IN) :: code
  PRINT *, TRIM(where),': ',TRIM(message),code
  STOP 9
END SUBROUTINE
