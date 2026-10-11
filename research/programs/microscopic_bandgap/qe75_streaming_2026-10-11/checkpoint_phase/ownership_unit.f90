! GPL-2.0-or-later. Single-process storage ownership test, no MPI or QE init.
PROGRAM ownership_unit
  USE kinds,ONLY: DP
  USE exx_qstream
  IMPLICIT NONE
  TYPE(exx_qstore) :: store
  COMPLEX(DP) :: vector(16),plane(16,3:7)
  CHARACTER(1024) :: path
  CHARACTER(32) :: mode,ack
  INTEGER :: q,b,i
  CALL GET_COMMAND_ARGUMENT(1,mode)
  CALL GET_COMMAND_ARGUMENT(2,path)
  IF(TRIM(mode)=='write') THEN
    CALL qs_begin(store,TRIM(path),16,3,7,4)
    DO b=3,7
      DO q=1,4
        DO i=1,16
          vector(i)=CMPLX(REAL(i+q+2*b,DP),REAL(i-q-b,DP),DP)
        ENDDO
        CALL qs_put(store,q,b,vector)
      ENDDO
    ENDDO
    CALL qs_seal(store)
    WRITE(*,'(A)') 'SEALED_OLD_GENERATION'
    FLUSH(6)
    READ(*,'(A)') ack
    IF(TRIM(ack)/='COMMITTED') ERROR STOP 'checkpoint not acknowledged'
    ! Deletes ONLY the live name; checkpoint hard link must retain identical data.
    CALL qs_close(store)
    WRITE(*,'(A)') 'OWNERSHIP_RELEASE_PASS'
  ELSE
    IF(TRIM(mode)=='wrong_shape') THEN
      CALL qs_restore_readonly(store,TRIM(path),15,3,7,4)
      ERROR STOP 'bad layout accepted'
    ENDIF
    CALL qs_restore_readonly(store,TRIM(path),16,3,7,4)
    IF(TRIM(mode)=='write_after_restore') THEN
      CALL qs_put(store,1,3,vector)
      ERROR STOP 'restored generation accepted write'
    ENDIF
    DO q=4,1,-1
      CALL qs_load(store,q,plane)
      DO b=3,7
        DO i=1,16
          IF(plane(i,b)/=CMPLX(REAL(i+q+2*b,DP),REAL(i-q-b,DP),DP)) ERROR STOP 'old payload changed'
        ENDDO
      ENDDO
    ENDDO
    CALL qs_close(store)
    WRITE(*,'(A)') 'READONLY_OLD_GENERATION_PASS'
  ENDIF
END PROGRAM

SUBROUTINE errore(routine,message,code)
  IMPLICIT NONE
  CHARACTER(*),INTENT(IN) :: routine,message
  INTEGER,INTENT(IN) :: code
  WRITE(*,'(A)') TRIM(routine)//': '//TRIM(message)
  STOP 9
END SUBROUTINE
