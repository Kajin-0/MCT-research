PROGRAM diagnostic_unit
  USE kinds, ONLY: DP
  USE iso_fortran_env, ONLY: int64
  USE qe75_diagnostics
  IMPLICIT NONE
  COMPLEX(DP) :: phi(6,2),vphi(6,2),gram(2,2),probe(6,1),direct(6,1),xi(6,2),factor(2,2),ace(6,1)
  REAL(DP) :: occ(2,1)
  CHARACTER(1024) :: root
  CALL get_command_argument(1,root)
  phi=(0._DP,0._DP);phi(1,1)=(1._DP,0._DP);phi(4,2)=(1._DP,0._DP)
  vphi=-phi;gram=MATMUL(CONJG(TRANSPOSE(phi)),vphi)
  CALL make_probe(3,2,2,1,[7,11],probe)
  probe=probe/SQRT(SUM(ABS(probe)**2));direct=-probe
  xi=-phi;factor=-gram;ace=-MATMUL(xi,MATMUL(CONJG(TRANSPOSE(xi)),probe))
  occ(:,1)=[1._DP,0.5_DP]
  CALL write_ace_before(TRIM(root)//'/before',0,1,3,2,2,[41_int64,42_int64],[7,11], &
                        -2._DP,phi,vphi,gram,probe,direct,occ)
  CALL write_ace_after(TRIM(root)//'/after',0,1,3,2,2,[41_int64,42_int64],[7,11], &
                       -2._DP,xi,factor,ace)
END PROGRAM
