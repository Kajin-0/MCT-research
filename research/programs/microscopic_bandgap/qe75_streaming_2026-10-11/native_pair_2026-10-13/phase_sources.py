"""Generate fresh-only FIRST-ACE fences in NEW private sources. No launch API."""
from pathlib import Path
import hashlib

DFT = Path('/home/User/opencode_workspace/DFT')
ROOT = DFT / '.local/qe75_lowram_20261011'
PRIVATE = ROOT / 'native_pair_20261013/v3'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError('native anchor changed: ' + old)
    return text.replace(old, new, 1)


PHASE = '''
  SUBROUTINE native_phase(stage)
    INTEGER, INTENT(IN) :: stage
    INTEGER :: code
    ! This is a request to a LIVE owner, not a Boolean environment bypass.
    ! 4 = complete captured initial state; 5 = actual FFT/resource admission;
    ! 6 = complete first-ACE evidence; 7 = exact fresh stream reservations.
    ! The fresh-only scope is distinct from
    ! legacy native restart scope 2 and standalone collective scope 3.
    code=1
    IF(stage==4 .OR. stage==5 .OR. stage==6 .OR. stage==7) &
      code=lease_call(INT(mpime,c_int),INT(nproc,c_int),INT(stage,c_int),4_c_int)
    code=MERGE(1,0,code/=0)
    CALL mp_max(code,world_comm)
    IF(code/=0) CALL errore('native_phase','live all-rank phase receipt refused',1)
    CALL mp_barrier(world_comm)
  END SUBROUTINE
'''


def generate(destination):
    destination = Path(destination)
    destination.mkdir(exist_ok=False)
    oldexx = ROOT / 'native_envelope_20261013/descriptor/exx.f90'
    oldinit = ROOT / 'm5_software_20261013/wave/init_run.f90'
    oldlease = ROOT / 'native_envelope_20261013/transport/native_lease.f90'
    oldclient = ROOT / 'native_envelope_20261013/transport/lease_client.c'
    original = {str(p): sha(p) for p in [oldexx, oldinit, oldlease, oldclient]}
    lease = oldlease.read_text().replace('PUBLIC :: native_register,native_check',
                                       'PUBLIC :: native_register,native_check,native_phase')
    lease = once(lease, '1_c_int,2_c_int)', '1_c_int,4_c_int)')
    lease = once(lease, '2_c_int,2_c_int)', '2_c_int,4_c_int)')
    lease = once(lease, 'END MODULE', PHASE + 'END MODULE')
    c = once(oldclient.read_text(),
        '(action!=1&&action!=2)||(required_scope!=1&&required_scope!=2)',
        '(action!=1&&action!=2&&action!=4&&action!=5&&action!=6&&action!=7)'
        '||(required_scope!=1&&required_scope!=2&&required_scope!=4)'
        '||(action>=4&&required_scope!=4)')
    init = once(oldinit.read_text(),
        '  USE qe75_native_lease, ONLY: native_check',
        '  USE qe75_native_lease, ONLY: native_check,native_phase')
    init = once(init, '  DEALLOCATE(layout)\nEND SUBROUTINE',
        '  DEALLOCATE(layout)\n  CALL native_phase(4)\nEND SUBROUTINE')
    exx = oldexx.read_text()
    # Restrict edits to the passive FFT observer and wrapper, never the four
    # native arithmetic bodies or production 352-band files.
    i = exx.index('SUBROUTINE qe75_capture_fft(fock)')
    hook = exx[i:]
    hook = once(hook, 'ONLY: native_check', 'ONLY: native_check,native_phase')
    hook = once(hook, '  captured=.TRUE.',
                '  CALL native_phase(5)\n  captured=.TRUE.')
    exx = exx[:i] + hook
    # The retained restart transaction requires scope 2 and retires OLD native
    # density/operator generations. It is incompatible with a fresh-only
    # scope-4 numerical fixture. Do not weaken it. Only this new private fresh
    # path requests owner-certified fresh inode reservations via live phase 7;
    # qs_begin_reserved and all checked 64-bit stream arithmetic stay unchanged.
    a = exx.index('  SUBROUTINE qbridge_request_store(')
    b = exx.index('  END SUBROUTINE', a)
    store = exx[a:b]
    store = once(store, '    USE iso_fortran_env, ONLY: int64',
                 '    USE iso_fortran_env, ONLY: int64\n    USE qe75_native_lease, ONLY: native_phase')
    store = once(store, "    CALL qbridge_transaction('retire_operator')", '    CALL native_phase(7)')
    exx = exx[:a] + store + exx[b:]
    a = exx.index('  SUBROUTINE aceinit(')
    b = exx.index('  END SUBROUTINE aceinit', a)
    body = exx[a:b]
    anchor = '    USE becmod,'
    j = body.index(anchor)
    body = body[:j] + '    USE qe75_native_lease, ONLY: native_phase\n' + body[j:]
    body = once(body, '    domat = .FALSE.', '''    ! A fresh diagnostic member ends here, after ALL local k actions and
    ! global energy reduction. No next HSE iteration, punch, SCF convergence
    ! or checkpoint/restart success is implied by this deliberate termination.
    CALL native_phase(6)
    CALL errore('r07_first_ace','first ACE captured; intentional fixture stop, not SCF',85)
    domat = .FALSE.''')
    exx = exx[:a] + body + exx[b:]
    for name, text in [('native_lease.f90', lease), ('lease_client.c', c),
                       ('init_run.f90', init), ('exx.f90', exx)]:
        (destination / name).write_text(text)
    arithmetic = {}
    for start, end in [('  SUBROUTINE vexx_k(', '  END SUBROUTINE vexx_k'),
                       ('  FUNCTION exxenergy2_k(', '  END FUNCTION  exxenergy2_k'),
                       ('  SUBROUTINE aceupdate_k(', '  END SUBROUTINE aceupdate_k'),
                       ('  SUBROUTINE vexxace_k(', '  END SUBROUTINE vexxace_k')]:
        def part(t):
            i = t.index(start)
            return t[i:t.index(end, i) + len(end)]
        if part(exx) != part(oldexx.read_text()):
            raise RuntimeError('native arithmetic changed')
        arithmetic[start.strip()] = True
    if any(sha(Path(p)) != h for p, h in original.items()):
        raise RuntimeError('prior source modified')
    return dict(prior_source_pins=original,
                new_source_pins={p.name: sha(p) for p in destination.iterdir()},
                native_arithmetic_byte_equal=arithmetic,
                phase_scope=4, source_compilation_is_not_phase_authority=True)
