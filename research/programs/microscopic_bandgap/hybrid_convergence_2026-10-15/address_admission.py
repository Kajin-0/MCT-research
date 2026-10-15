"""Prospective pathname admission + ONE tiny non-MPI exact-address check."""
from pathlib import Path
import socket
import json

HERE=Path(__file__).resolve().parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/chemical_hse8_firstace_20261014')


def checked_address(root,name='s'):
    path=str(Path(root)/name)
    if '\0' in path or len(path.encode())>107:raise ValueError('AF_UNIX pathname exceeds107bytes including no NUL')
    return path


def refuse_reuse(root):
    for name in ['READY.json','REFERENCED.json','LAUNCH.json','GUARD_RESULT.json','output.escrow']:
        if (Path(root)/name).exists():raise ValueError('prior owner attempt cannot be reused')


def main():
    if (HERE/'address_result.json').exists():raise FileExistsError('preserve result')
    host=ROOT/'pair/host';old=str(host/'lease.sock');short=checked_address(host)
    bad=socket.socket(socket.AF_UNIX)
    try:
        bad.bind(old);raise AssertionError('overlength address was accepted')
    except OSError as error:failure=dict(type=type(error).__name__,text=str(error),errno=error.errno)
    finally:bad.close()
    assert not Path(old).exists()
    if Path(short).exists():raise FileExistsError('preserve unrelated socket')
    good=socket.socket(socket.AF_UNIX)
    try:
        good.bind(short);inode=Path(short).lstat().st_ino
        assert Path(short).is_socket()
    finally:
        good.close()
        if Path(short).exists() and Path(short).lstat().st_ino==inode:Path(short).unlink()
    try:checked_address(host,'lease.sock');raise AssertionError('bad preflight accepted')
    except ValueError:pass
    try:refuse_reuse(host);raise AssertionError('failed owner state accepted')
    except ValueError:pass
    future={m:checked_address(ROOT/'p2'/m) for m in ['host','cd']}
    result=dict(scope='ONE tiny AF_UNIX bind experiment; NO MPI/QE/unit/owner retry',
        original_address=old,original_bytes=len(old.encode()),original_bind_failure=failure,
        prospective_short_address=short,short_bytes=len(short.encode()),short_real_bind_pass=True,
        only_new_socket_closed_and_identity_checked_unlinked=True,current_failed_state_reuse_refused=True,
        future_fresh_addresses=future,future_byte_lengths={m:len(v.encode()) for m,v in future.items()},
        prospective_patch_not_executed=True,native_hse_runs=0,chemical_delta_eV=None)
    (HERE/'address_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
