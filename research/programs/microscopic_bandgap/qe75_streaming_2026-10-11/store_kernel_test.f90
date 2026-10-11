! Tiny deterministic single-process test. No QE initialization, MPI or SCF.
! GPL-2.0-or-later.
PROGRAM store_kernel_test
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64
  USE ieee_arithmetic, ONLY: ieee_value, ieee_quiet_nan
  USE exx_qstream
  IMPLICIT NONE
  INTEGER, PARAMETER :: n=8, lo=3, hi=7, nb=hi-lo+1, nq=4
  TYPE(exx_qstore) :: s
  COMPLEX(DP) :: full(2*n,lo:hi,nq), plane(2*n,lo:hi), psi(n,2,nb), &
                 old(n,2,nb), new(n,2,nb), u(n,2), v(n,2), &
                 gram_old(nb,nb), gram_new(nb,nb), special(2*n)
  INTEGER :: q,b,i,j,g,k,caseunit,ios,generation
  INTEGER :: order(5)=[4,1,3,2,4]
  INTEGER(int64) :: huge_extent
  CHARACTER(1024) :: path
  CHARACTER(64) :: mode
  REAL(DP) :: a,pi
  pi=ACOS(-1.0_DP)
  CALL GET_COMMAND_ARGUMENT(1,mode)
  CALL GET_COMMAND_ARGUMENT(2,path)
  IF (TRIM(mode)=='extent64') THEN
    huge_extent=qs_extent(524288,1,352,8)
    IF (huge_extent /= 23622320128_int64) ERROR STOP 'wrong >2GiB extent'
    WRITE(*,'(A,I0)') 'EXTENT64_PASS ',huge_extent
    STOP
  ELSE IF (TRIM(mode)=='overflow') THEN
    huge_extent=qs_extent(HUGE(1),1,HUGE(1),HUGE(1))
    ERROR STOP 'overflow incorrectly accepted'
  ENDIF
  IF (LEN_TRIM(path)==0) ERROR STOP 'test path required'
  IF (TRIM(mode)=='shape') THEN
    CALL qs_begin(s,TRIM(path),0,lo,hi,nq)
    ERROR STOP 'invalid shape incorrectly accepted'
  ELSE IF (TRIM(mode)=='preexisting') THEN
    OPEN(NEWUNIT=caseunit,FILE=TRIM(path),STATUS='new')
    WRITE(caseunit,*) 'owned test fixture'
    CLOSE(caseunit)
  ENDIF
  CALL qs_begin(s,TRIM(path),2*n,lo,hi,nq)
  IF (TRIM(mode)=='unsealed') THEN
    CALL qs_load(s,1,plane)
    ERROR STOP 'unsealed load incorrectly accepted'
  ENDIF
  DO generation=1,2
    IF(generation==2) CALL qs_begin(s,TRIM(path),2*n,lo,hi,nq)
    ! Symmetry permutations plus nontrivial spin rotation and both TR branches.
    DO b=lo,hi
      DO i=1,n
        u(i,1)=CMPLX(SIN(0.37_DP*i*b),COS(0.23_DP*(i+b)),DP)*generation
        u(i,2)=CMPLX(COS(0.41_DP*i*b),SIN(0.17_DP*(i-b)),DP)*generation
      ENDDO
      DO q=1,nq
        a=0.2_DP*q
        DO i=1,n
          j=MOD(i+q-2,n)+1
          v(i,1)=COS(a)*u(j,1)+SIN(a)*u(j,2)
          v(i,2)=-SIN(a)*u(j,1)+COS(a)*u(j,2)
        ENDDO
        IF (MOD(q,2)==1) THEN
          full(1:n,b,q)=v(:,1); full(n+1:2*n,b,q)=v(:,2)
        ELSE
          full(1:n,b,q)=CONJG(v(:,2)); full(n+1:2*n,b,q)=-CONJG(v(:,1))
        ENDIF
        IF (TRIM(mode)=='missing' .AND. q==nq .AND. b==hi) CYCLE
        CALL qs_put(s,q,b,full(:,b,q))
        IF (TRIM(mode)=='duplicate') THEN
          CALL qs_put(s,q,b,full(:,b,q))
          ERROR STOP 'duplicate incorrectly accepted'
        ENDIF
      ENDDO
    ENDDO
    CALL qs_seal(s)
    SELECT CASE(TRIM(mode))
    CASE('sealed_write')
      CALL qs_put(s,1,lo,full(:,lo,1))
      ERROR STOP 'sealed write incorrectly accepted'
    CASE('q_range')
      CALL qs_load(s,nq+1,plane)
      ERROR STOP 'invalid q incorrectly accepted'
    CASE('plane_shape')
      CALL qs_load(s,1,plane(:,lo:hi-1))
      ERROR STOP 'invalid plane shape incorrectly accepted'
    CASE('truncate')
      ! Separate handle emulates external storage failure; no large file written.
      OPEN(NEWUNIT=caseunit,FILE=TRIM(path),STATUS='replace',ACCESS='stream',FORM='unformatted')
      WRITE(caseunit) 0
      CLOSE(caseunit)
      CALL qs_load(s,nq,plane)
      ERROR STOP 'truncated file incorrectly accepted'
    END SELECT
    DO k=1,SIZE(order)
      q=order(k)
      plane=CMPLX(100.0_DP,-50.0_DP,DP)
      CALL qs_load(s,q,plane)
      IF (.NOT.same_bits(plane,full(:,:,q))) ERROR STOP 'q-plane bit mismatch'
    ENDDO
    ! Tiny real-space spinor exchange contraction, direct DFT Coulomb surrogate.
    DO b=1,nb
      DO i=1,n
        psi(i,1,b)=CMPLX(SIN(0.83_DP*i*b),COS(0.31_DP*(i+b)),DP)
        psi(i,2,b)=CMPLX(COS(0.57_DP*i*b),SIN(0.29_DP*(i-b)),DP)
      ENDDO
    ENDDO
    old=0; new=0
    DO q=1,nq
      CALL contract(q,full(:,:,q),psi,old)
      CALL qs_load(s,q,plane)
      CALL contract(q,plane,psi,new)
    ENDDO
    IF (ANY(TRANSFER(old,[0_int64],2*SIZE(old)) /= TRANSFER(new,[0_int64],2*SIZE(new)))) &
      ERROR STOP 'kernel bit mismatch'
    DO i=1,nb
      DO j=1,nb
        gram_old(i,j)=SUM(CONJG(psi(:,:,i))*old(:,:,j))
        gram_new(i,j)=SUM(CONJG(psi(:,:,i))*new(:,:,j))
      ENDDO
    ENDDO
    IF (.NOT.same_bits(gram_old,gram_new)) ERROR STOP 'ACE-input Gram bit mismatch'
    WRITE(*,'(A,I0,A,ES12.4)') 'GENERATION_PASS ',generation,' kernel_difference=',MAXVAL(ABS(old-new))
  ENDDO
  CALL qs_close(s)
  ! Non-finite payload and signed zeros are preserved as bytes, not interpreted.
  special=CMPLX(-0.0_DP,0.0_DP,DP)
  special(1)=CMPLX(ieee_value(1.0_DP,ieee_quiet_nan),-0.0_DP,DP)
  CALL qs_begin(s,TRIM(path),2*n,1,1,1)
  CALL qs_put(s,1,1,special); CALL qs_seal(s)
  CALL qs_load(s,1,plane(:,lo:lo))
  IF (ANY(TRANSFER(special,[0_int64],2*SIZE(special)) /= &
          TRANSFER(plane(:,lo:lo),[0_int64],2*SIZE(special)))) ERROR STOP 'payload bit mismatch'
  CALL qs_close(s)
  WRITE(*,'(A)') 'STORE_KERNEL_PASS'
CONTAINS
  FUNCTION same_bits(a,b) RESULT(equal)
    COMPLEX(DP), INTENT(IN) :: a(:,:),b(:,:)
    LOGICAL :: equal
    equal=ALL(TRANSFER(a,[0_int64],2*SIZE(a))==TRANSFER(b,[0_int64],2*SIZE(b)))
  END FUNCTION
  SUBROUTINE contract(q,source,target,result)
    INTEGER, INTENT(IN) :: q
    COMPLEX(DP), INTENT(IN) :: source(2*n,lo:hi), target(n,2,nb)
    COMPLEX(DP), INTENT(INOUT) :: result(n,2,nb)
    COMPLEX(DP) :: rho(n),rho_g(n),potential(n),phase
    REAL(DP) :: weight,angle,fac
    INTEGER :: it,jb,ir,ig,jr,spin
    DO it=1,nb
      DO jb=lo,hi
        rho=(CONJG(source(1:n,jb))*target(:,1,it)+CONJG(source(n+1:2*n,jb))*target(:,2,it))/7.0_DP
        DO ig=1,n
          rho_g(ig)=0
          DO ir=1,n
            angle=-2*pi*REAL((ig-1)*(ir-1),DP)/n
            phase=CMPLX(COS(angle),SIN(angle),DP)
            rho_g(ig)=rho_g(ig)+rho(ir)*phase
          ENDDO
        ENDDO
        weight=(0.1_DP+0.03_DP*jb+0.02_DP*q)/nq
        DO ir=1,n
          potential(ir)=0
          DO ig=1,n
            angle=2*pi*REAL((ig-1)*(ir-1),DP)/n
            fac=1.0_DP/(1.0_DP+(ig-1.0_DP+0.1_DP*q)**2)
            phase=CMPLX(COS(angle),SIN(angle),DP)
            potential(ir)=potential(ir)+rho_g(ig)*fac*weight*phase/n
          ENDDO
          result(ir,1,it)=result(ir,1,it)-potential(ir)*source(ir,jb)
          result(ir,2,it)=result(ir,2,it)-potential(ir)*source(ir+n,jb)
        ENDDO
      ENDDO
    ENDDO
  END SUBROUTINE
END PROGRAM

SUBROUTINE errore(routine,message,code)
  IMPLICIT NONE
  CHARACTER(*), INTENT(IN) :: routine,message
  INTEGER, INTENT(IN) :: code
  WRITE(*,'(A)') 'EXPECTED_QS_ERROR '//TRIM(routine)//': '//TRIM(message)
  STOP 9
END SUBROUTINE
