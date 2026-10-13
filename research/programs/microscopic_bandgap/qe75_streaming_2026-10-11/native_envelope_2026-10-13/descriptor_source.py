"""Generate a read-only typed actual-FFT observer in a NEW private source tree."""
from fft_descriptor import SCALARS,ARRAY1,ARRAY2
from build_transport import HERE,ROOT
from native_bundle import artifact_sha256

HOOK=r'''
#if defined(__QE75_RESOURCE_CAPTURE)
SUBROUTINE qe75_capture_fft(fock)
  USE iso_fortran_env, ONLY: int64
  USE fft_types, ONLY: fft_type_descriptor
  USE fft_base, ONLY: dfftp,dffts
  USE qe75_resource_descriptor, ONLY: resource_write
  USE qe75_native_lease, ONLY: native_check
  USE mp_world, ONLY: mpime,nproc,world_comm
  USE mp_pools, ONLY: npool
  USE mp, ONLY: mp_max,mp_barrier
  USE wvfct, ONLY: npwx,nbnd
  USE klist, ONLY: nks,nkstot
  USE exx_base, ONLY: nkqs,nqs
  USE gvect, ONLY: ngm
  USE gvecs, ONLY: ngms
  USE lsda_mod, ONLY: nspin
  USE noncollin_module, ONLY: npol
  USE control_flags, ONLY: nmix,io_level,use_gpu
  USE ions_base, ONLY: nat
  USE uspp, ONLY: okvan
  IMPLICIT NONE
  TYPE(fft_type_descriptor), INTENT(IN) :: fock
  CHARACTER(1024) :: root,path
  CHARACTER(64) :: profile,common
  CHARACTER(32) :: rank
  INTEGER :: length,status,code
  LOGICAL, SAVE :: captured=.FALSE.
  CALL native_check()
  IF(captured) RETURN
  code=0
  IF(nproc/=2 .OR. npool/=1 .OR. nat/=2 .OR. npol/=2 .OR. nbnd/=48 .OR. okvan .OR. use_gpu) code=1
  CALL get_environment_variable('QE75_RESOURCE_ROOT',root,LENGTH=length,STATUS=status)
  IF(status/=0 .OR. length<1 .OR. length>850) code=1
  CALL get_environment_variable('QE75_PROFILE_SHA256',profile,LENGTH=length,STATUS=status)
  IF(status/=0 .OR. length/=64) code=1
  CALL get_environment_variable('QE75_COMMON_INPUT_SHA256',common,LENGTH=length,STATUS=status)
  IF(status/=0 .OR. length/=64) code=1
  code=MERGE(1,0,code/=0)
  CALL mp_max(code,world_comm)
  IF(code/=0) CALL errore('resource_capture','fixture/profile/root refused',1)
  WRITE(rank,'(I0)') mpime
  path=TRIM(root)//'/rank'//TRIM(rank)//'.fft'
  CALL resource_write(TRIM(path),profile,common,mpime,nproc, &
       INT([npwx,npol,nbnd,nks,nkstot,nkqs,nqs,ngm,ngms,nspin,nmix,io_level],int64), &
       dfftp,dffts,fock,code)
  ! Every rank takes this collective on local I/O failure before any EXX
  ! allocation proceeds. An absent/truncated packet NEVER certifies a layout.
  code=MERGE(1,0,code/=0)
  CALL mp_max(code,world_comm)
  IF(code/=0) CALL errore('resource_capture','all-rank FFT capture refused',1)
  CALL mp_barrier(world_comm)
  captured=.TRUE.
END SUBROUTINE
#endif
'''


def generate(folder):
    folder.mkdir(exist_ok=True)
    def keep(path,content):
        if path.exists():
            if path.read_text()!=content:raise RuntimeError('retained private descriptor source differs')
        else:path.write_text(content)
    scalar=[]
    for name in SCALARS:
        if name in ['has_task_groups','use_pencil_decomposition']:scalar.append(f'INT(MERGE(1,0,d%{name}),int64)')
        else:scalar.append(f'INT(d%{name},int64)')
    body='''! GPL-2.0-or-later. Read-only observation; no FFT initialization changes.
MODULE qe75_resource_descriptor
  USE iso_fortran_env, ONLY: int64
  USE fft_types, ONLY: fft_type_descriptor
  IMPLICIT NONE
CONTAINS
  SUBROUTINE resource_write(path,profile,common,rank,world,scope,dense,smooth,fock,code)
    CHARACTER(*), INTENT(IN) :: path
    CHARACTER(64), INTENT(IN) :: profile,common
    INTEGER, INTENT(IN) :: rank,world
    INTEGER(int64), INTENT(IN) :: scope(:)
    TYPE(fft_type_descriptor), INTENT(IN) :: dense,smooth,fock
    INTEGER, INTENT(OUT) :: code
    INTEGER :: u,ios,closing
    code=1
    IF(SIZE(scope)/=12 .OR. rank<0 .OR. rank>=world .OR. world/=2) RETURN
    IF(STORAGE_SIZE(0_int64)/=64 .OR. STORAGE_SIZE(0)/=32) RETURN
    OPEN(NEWUNIT=u,FILE=path,STATUS='new',ACCESS='stream',FORM='unformatted', &
         ACTION='write',CONVERT='little_endian',IOSTAT=ios)
    IF(ios/=0) RETURN
    WRITE(u,IOSTAT=ios) 'FFTRES01',1_int64,INT(rank,int64),INT(world,int64),12_int64,profile,common,scope
    CALL put_descriptor(u,'dense',dense,ios)
    CALL put_descriptor(u,'smooth',smooth,ios)
    CALL put_descriptor(u,'fock',fock,ios)
    IF(ios==0) WRITE(u,IOSTAT=ios) 'FFTEND01'
    CLOSE(u,IOSTAT=closing)
    IF(ios==0 .AND. closing==0) code=0
  END SUBROUTINE
  SUBROUTINE put_descriptor(u,name,d,ios)
    INTEGER, INTENT(IN) :: u
    CHARACTER(*), INTENT(IN) :: name
    TYPE(fft_type_descriptor), INTENT(IN) :: d
    INTEGER, INTENT(INOUT) :: ios
    CHARACTER(16) :: label
    label=name
    IF(ios/=0) RETURN
    WRITE(u,IOSTAT=ios) label, [SCALAR_VALUES]
ARRAY_CALLS
  END SUBROUTINE
  SUBROUTINE put1(u,name,a,ios)
    INTEGER, INTENT(IN) :: u
    CHARACTER(*), INTENT(IN) :: name
    INTEGER, ALLOCATABLE, INTENT(IN) :: a(:)
    INTEGER, INTENT(INOUT) :: ios
    CHARACTER(24) :: label
    label=name
    IF(ios/=0) RETURN
    IF(ALLOCATED(a)) THEN
      WRITE(u,IOSTAT=ios) label,INT(SIZE(a),int64),1_int64,INT(a,int64)
    ELSE
      WRITE(u,IOSTAT=ios) label,-1_int64,0_int64
    ENDIF
  END SUBROUTINE
  SUBROUTINE put2(u,name,a,ios)
    INTEGER, INTENT(IN) :: u
    CHARACTER(*), INTENT(IN) :: name
    INTEGER, ALLOCATABLE, INTENT(IN) :: a(:,:)
    INTEGER, INTENT(INOUT) :: ios
    CHARACTER(24) :: label
    label=name
    IF(ios/=0) RETURN
    IF(ALLOCATED(a)) THEN
      WRITE(u,IOSTAT=ios) label,INT(SIZE(a,1),int64),INT(SIZE(a,2),int64),INT(a,int64)
    ELSE
      WRITE(u,IOSTAT=ios) label,-1_int64,0_int64
    ENDIF
  END SUBROUTINE
END MODULE
'''
    body=body.replace('SCALAR_VALUES',', &\n      '.join(scalar))
    calls=[f"    CALL put1(u,'{name}',d%{name},ios)" for name in ARRAY1]
    calls += [f"    CALL put2(u,'{name}',d%{name},ios)" for name in ARRAY2]
    body=body.replace('ARRAY_CALLS','\n'.join(calls))
    keep(folder/'resource_descriptor.f90',body)
    old=ROOT/'m5_readiness/source/exx.f90';text=old.read_text()
    # Place BEFORE MPI gather and exxbuff allocations, after the real descriptor
    # has been initialized by the native exx_fft_create. Observe only once.
    needle='    nrxxs = dfftt%nnr\n#if defined(__MPI)'
    if text.count(needle)!=1:raise RuntimeError('pre-allocation descriptor anchor changed')
    text=text.replace(needle,'''    nrxxs = dfftt%nnr
#if defined(__QE75_RESOURCE_CAPTURE)
    CALL qe75_capture_fft(dfftt)
#endif
#if defined(__MPI)''',1)+HOOK
    keep(folder/'exx.f90',text)
    return {'original_exx_sha256':artifact_sha256(old),'new_exx_sha256':artifact_sha256(folder/'exx.f90'),
            'codec_sha256':artifact_sha256(folder/'resource_descriptor.f90'),'native_executed':False,
            'scope':'first native exxinit only; before gather/exxbuff, after FFT creation and transform_evc_to_exx'}
