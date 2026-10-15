"""Qualify a paired cover on actual retained C1 and save only new private data."""
import hashlib
import json
from pathlib import Path
import numpy as np
from audit_native import gather, orthonormal
from constructor import paired_cover

HERE = Path(__file__).resolve().parent
PRIVATE = Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8s_20261015/analysis')


def main():
    if PRIVATE.exists():
        raise FileExistsError('preserve constructor evidence; no overwrite')
    phi, _, theta, _, wg = gather(1)
    U, _ = orthonormal(phi)
    Q, history = paired_cover(U, theta, 1e-10)
    gram = float(np.linalg.norm(Q.conj().T@Q-np.eye(Q.shape[1]), 2))
    cover = float(np.linalg.norm(phi-Q@(Q.conj().T@phi), 2))
    pairing = float(np.linalg.norm(theta(Q[:, ::2])-Q[:, 1::2], 2))
    reverse = float(np.linalg.norm(theta(Q[:, 1::2])+Q[:, ::2], 2))
    leak = float(np.linalg.norm(theta(Q)-Q@(Q.conj().T@theta(Q)), 2))
    assert gram < 1e-10 and cover < 1e-10 and max(pairing, reverse, leak) < 1e-10
    # No claim that native D already equals its nonmagnetic ensemble projection.
    PRIVATE.mkdir(parents=True, mode=0o700)
    target = PRIVATE/'paired_basis.npz'
    np.savez(target, Q=Q)
    result = dict(status='CALCULATED constructive actual-source cover, not a new SCF state',
        dimension=Q.shape[1], tolerance=1e-10, source_cover_op=cover, Gram_defect_op=gram,
        forward_Kramers_pair_error=pairing, reverse_Kramers_pair_error=reverse,
        TR_closure_op=leak, history=history, source_charge_e=float(sum(wg)),
        density_or_occupations_modified=False, basis_path=str(target),
        basis_sha256=hashlib.sha256(target.read_bytes()).hexdigest(), native_actions_on_new_directions_unknown=True)
    (HERE/'constructor_result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__=='__main__':
    main()
