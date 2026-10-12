! GPL-2.0-or-later. Bounded first-ACE capture; no SCF result is implied.
MODULE qe75_diagnostics
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64
  IMPLICIT NONE
  PRIVATE
  PUBLIC :: make_probe,write_ace_before,write_ace_after
CONTAINS
  SUBROUTINE make_probe(npwx,npw,npol,k,global_g,probe)
    INTEGER, INTENT(IN) :: npwx,npw,npol,k,global_g(:)
    COMPLEX(DP), INTENT(OUT) :: probe(:,:)
    INTEGER :: i,s
    INTEGER(int64) :: key,a,b
    IF(SIZE(probe,1)/=npwx*npol .OR. SIZE(probe,2)/=1 .OR. SIZE(global_g)/=npw) &
      ERROR STOP 'probe shape'
    probe=(0._DP,0._DP)
    DO s=1,npol
      DO i=1,npw
        key=MODULO(INT(global_g(i),int64),104729_int64)
        a=MODULO(key*31+INT(s,int64)*17+INT(k,int64)*13,127_int64)-63
        b=MODULO(key*19+INT(s,int64)*23+INT(k,int64)*11,131_int64)-65
        probe(i+(s-1)*npwx,1)=CMPLX(REAL(a,DP),REAL(b,DP),DP)
      ENDDO
    ENDDO
    ! Global normalization is performed by the native adapter with mp_sum.
  END SUBROUTINE

  SUBROUTINE header(u,path,rank,k,stage,npwx,npw,npol,bands,layout,globals,energy)
    INTEGER, INTENT(OUT) :: u
    CHARACTER(*), INTENT(IN) :: path
    INTEGER, INTENT(IN) :: rank,k,stage,npwx,npw,npol,bands,globals(:)
    INTEGER(int64), INTENT(IN) :: layout(:)
    REAL(DP), INTENT(IN) :: energy
    INTEGER :: ios
    OPEN(NEWUNIT=u,FILE=path,STATUS='new',ACCESS='stream',FORM='unformatted',IOSTAT=ios)
    IF(ios/=0) ERROR STOP 'owned diagnostic collision/open refused'
    WRITE(u) 'QE75-ACE-DIAG01 ',INT([1,rank,k,stage,npwx,npw,npol,bands,SIZE(layout)],int64), &
            energy,layout,INT(globals,int64)
  END SUBROUTINE

  SUBROUTINE write_ace_before(path,rank,k,npwx,npw,npol,layout,globals,energy,phi,vphi,gram,probe,action,occ)
    CHARACTER(*), INTENT(IN) :: path
    INTEGER, INTENT(IN) :: rank,k,npwx,npw,npol,globals(:)
    INTEGER(int64), INTENT(IN) :: layout(:)
    REAL(DP), INTENT(IN) :: energy,occ(:,:)
    COMPLEX(DP), CONTIGUOUS, INTENT(IN) :: phi(:,:),vphi(:,:),gram(:,:),probe(:,:),action(:,:)
    INTEGER :: u,j
    IF(ANY(SHAPE(phi)/=SHAPE(vphi))) ERROR STOP 'capture action shape'
    CALL header(u,path,rank,k,1,npwx,npw,npol,SIZE(phi,2),layout,globals,energy)
    WRITE(u) INT(SHAPE(occ),int64)
    DO j=1,SIZE(occ,2); WRITE(u) occ(:,j); ENDDO
    DO j=1,SIZE(phi,2); WRITE(u) phi(:,j),vphi(:,j); ENDDO
    DO j=1,SIZE(gram,2); WRITE(u) gram(:,j); ENDDO
    WRITE(u) probe(:,1),action(:,1)
    CLOSE(u)
  END SUBROUTINE

  SUBROUTINE write_ace_after(path,rank,k,npwx,npw,npol,layout,globals,energy,xi,factor,action)
    CHARACTER(*), INTENT(IN) :: path
    INTEGER, INTENT(IN) :: rank,k,npwx,npw,npol,globals(:)
    INTEGER(int64), INTENT(IN) :: layout(:)
    REAL(DP), INTENT(IN) :: energy
    COMPLEX(DP), CONTIGUOUS, INTENT(IN) :: xi(:,:),factor(:,:),action(:,:)
    INTEGER :: u,j
    CALL header(u,path,rank,k,2,npwx,npw,npol,SIZE(xi,2),layout,globals,energy)
    DO j=1,SIZE(xi,2); WRITE(u) xi(:,j); ENDDO
    DO j=1,SIZE(factor,2); WRITE(u) factor(:,j); ENDDO
    WRITE(u) action(:,1)
    CLOSE(u)
  END SUBROUTINE
END MODULE
