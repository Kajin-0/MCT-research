! GPL-2.0-or-later. Small exact codec test, NOT a native SCF validation.
PROGRAM state_unit
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64
  USE exx_checkpoint_state
  IMPLICIT NONE
  CHARACTER(1024) :: path
  CHARACTER(64) :: fingerprint
  CHARACTER(32) :: action,arg
  INTEGER :: rank,stop_mode,j,k
  INTEGER(int64) :: layout(20),n
  TYPE(bridge_outer) :: outer
  REAL(DP) :: occ(2,2),wg(2,2),et(2,2)
  COMPLEX(DP) :: xi(3,2,2)
  CALL get_command_argument(1,action)
  CALL get_command_argument(2,path)
  CALL get_command_argument(3,fingerprint)
  CALL get_command_argument(4,arg);READ(arg,*) rank
  CALL get_command_argument(5,arg);READ(arg,*) stop_mode
  layout=INT([rank,2,3,2,2,3,1,2,2,2,2,2,2,2,2,1,1,0,0,2],int64)
  outer%mode=stop_mode;outer%iter=5
  outer%scalar=[1.d-10,2.d-8,-3.d0,-4.d0,-5.d0,-6.d0,-7.d0,1.d-12,1.d-13]
  occ=RESHAPE([1.d0,0.d0,0.8d0,0.2d0],[2,2])
  wg=RESHAPE([0.45d0,0.05d0,0.3d0,0.2d0],[2,2]) ! current != old weights
  et=RESHAPE([-4.d0,-3.d0,-2.d0,1.d0],[2,2])
  DO k=1,2
    DO j=1,2
      xi(:,j,k)=[CMPLX(j,k,DP),CMPLX(-j,k,DP),CMPLX(j,-k,DP)]
    ENDDO
  ENDDO
  IF(action=='write') THEN
    CALL bridge_write(TRIM(path),fingerprint,layout,outer,occ,wg,et,xi)
    IF(.NOT.bridge_pending) ERROR STOP 'pending not set'
  ELSEIF(action=='read' .OR. action=='wrong_layout') THEN
    occ=-999;wg=-999;et=-999;xi=-999
    IF(action=='wrong_layout') layout(20)=3
    CALL bridge_read(TRIM(path),fingerprint,layout,outer,occ,wg,et,xi)
    IF(bridge_pending) ERROR STOP 'import unexpectedly pending'
    IF(outer%iter/=5 .OR. outer%mode/=stop_mode) ERROR STOP 'counter mismatch'
    IF(ANY(outer%scalar/=[1.d-10,2.d-8,-3.d0,-4.d0,-5.d0,-6.d0,-7.d0,1.d-12,1.d-13])) ERROR STOP 'scalar mismatch'
    IF(ANY(occ/=RESHAPE([1.d0,0.d0,0.8d0,0.2d0],[2,2]))) ERROR STOP 'old occupation mismatch'
    IF(ANY(wg/=RESHAPE([0.45d0,0.05d0,0.3d0,0.2d0],[2,2]))) ERROR STOP 'current weight mismatch'
    IF(ANY(et/=RESHAPE([-4.d0,-3.d0,-2.d0,1.d0],[2,2]))) ERROR STOP 'eigenvalue mismatch'
    DO k=1,2
      DO j=1,2
        IF(ANY(xi(:,j,k)/=[CMPLX(j,k,DP),CMPLX(-j,k,DP),CMPLX(j,-k,DP)])) ERROR STOP 'old ACE mismatch'
      ENDDO
    ENDDO
  ELSEIF(action=='extent64') THEN
    n=bridge_extent(20,352,8,352,8,500000,352,8)
    IF(n<=INT(HUGE(1),int64)) ERROR STOP 'missing 64-bit extent'
    PRINT *, 'EXACT_64BIT_EXTENT',n
  ELSE
    ERROR STOP 'invalid action'
  ENDIF
  PRINT *, 'STATE_CODEC_PASS'
END PROGRAM

SUBROUTINE errore(where,message,code)
  CHARACTER(*), INTENT(IN) :: where,message
  INTEGER, INTENT(IN) :: code
  PRINT *, TRIM(where),': ',TRIM(message),code
  STOP 9
END SUBROUTINE
