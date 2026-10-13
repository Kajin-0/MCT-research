PROGRAM initial_unit
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64
  USE qe75_initial_state, ONLY: initial_write
  IMPLICIT NONE
  COMPLEX(DP) :: wave(64,48),rg(5,1)
  REAL(DP) :: et(48,2),wg(48,2),rr(8,1),v(8,1),kp(3)
  INTEGER :: mill(3,30),i,j,code,mode
  CHARACTER(1024) :: path,arg
  CALL get_command_argument(1,path);CALL get_command_argument(2,arg);READ(arg,*) mode
  DO i=1,30;mill(:,i)=[i,-i,MOD(i,3)];ENDDO
  wave=(0._DP,0._DP)
  DO j=1,48
    i=j
    IF(j>30) i=32+j-30
    wave(i,j)=(1._DP,0._DP)
  ENDDO
  DO j=1,2;DO i=1,48;et(i,j)=i/8._DP;wg(i,j)=j/4._DP;ENDDO;ENDDO
  rr(:,1)=[(i/4._DP,i=1,8)];v=rr*2;rg(:,1)=[(CMPLX(i/4._DP,-i/2._DP,DP),i=1,5)]
  kp=[0._DP,0.5_DP,0._DP]
  IF(mode==1) wave(1,1)=(-1._DP,0._DP) ! phase-equivalent is not byte-identical
  IF(mode==2) mill(1,1)=99
  IF(mode==4) wave(31,1)=(19._DP,-7._DP) ! unused padding must not alter capture
  CALL initial_write(TRIM(path),REPEAT('a',64),0,1,32,30,2,[1_int64,2_int64],mill,kp,wave,et,wg,rr,rg,v,code)
  IF(mode==3) THEN
    IF(code==0) ERROR STOP 'expected collision/path refusal'
    WRITE(*,*) 'EXPECTED_IO_REFUSAL',code
  ELSE
    IF(code/=0) ERROR STOP 'unexpected initial capture failure'
  ENDIF
END PROGRAM
