! GPL-2.0-or-later. Tiny IO stubs for ACTUAL unmodified QE save/restart routines.
! Tests their zero-counter branch, not native MPI/HDF5 or material physics.
MODULE io_global
  INTEGER :: stdout=6
END MODULE
MODULE klist
  INTEGER :: nks=2
END MODULE
MODULE wvfct
  INTEGER :: nbnd=2
END MODULE
MODULE control_flags
  USE kinds, ONLY: DP
  INTEGER :: n_scf_steps
  REAL(DP) :: scf_error
END MODULE
MODULE add_dmft_occ
  LOGICAL :: dmft=.FALSE.
END MODULE
MODULE io_files
  INTEGER :: iunres=41
  CHARACTER(1024) :: directory
CONTAINS
  SUBROUTINE seqopn(unit,extension,form,exists)
    INTEGER :: unit
    CHARACTER(*) :: extension,form
    LOGICAL :: exists
    INQUIRE(FILE=TRIM(directory)//'/'//extension,EXIST=exists)
    OPEN(UNIT=unit,FILE=TRIM(directory)//'/'//extension,FORM=form,STATUS='unknown')
  END SUBROUTINE
END MODULE

PROGRAM zero_counter_unit
  USE kinds, ONLY: DP
  USE io_files
  IMPLICIT NONE
  REAL(DP) :: et(2,2),dr2,ethr
  INTEGER :: iter
  CALL get_command_argument(1,directory)
  et=-3._DP
  CALL save_in_electrons(0,0._DP,2.d-10,et)
  iter=99;dr2=99;ethr=99;et=99
  CALL restart_in_electrons(iter,dr2,ethr,et)
  IF(iter/=0 .OR. dr2/=99 .OR. ethr/=99 .OR. ANY(et/=99)) ERROR STOP 'stock zero-counter branch changed'
  PRINT *, 'STOCK_ZERO_COUNTER_IGNORES_SAVED_ETHR_ET'
  et=-3._DP
  CALL save_in_electrons(0,0._DP,2.d-10,et)
  ! Packet import has already supplied current et and ethr; SCF initializes
  ! dr2=0 for inner iteration zero. The native branch now cannot reset them.
  iter=99;dr2=0;ethr=2.d-10;et=-3._DP
  CALL restart_in_electrons(iter,dr2,ethr,et)
  IF(iter/=0 .OR. dr2/=0 .OR. ethr/=2.d-10 .OR. ANY(et/=-3._DP)) ERROR STOP 'packet-seeded zero counter changed'
  PRINT *, 'PACKET_SEEDED_ZERO_COUNTER_PASS'
END PROGRAM
