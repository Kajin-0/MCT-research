"""Read-only access to accepted native packets; no execution on import."""
from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
OLD=BASE/'same_density_hamiltonian_2026-10-15'
PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8h_20261015')
spec=importlib.util.spec_from_file_location('r07_accepted_sameD_readback',OLD/'readback.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
decode=module.decode;td_operations=module.td_operations
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def frames():
    f=np.load(PRIVATE/'trial.npz');b=np.load(PRIVATE/'full_action_basis.npz')
    return f,b,f['G'],f['Q'],b['new_queries'],b['Q']


def global_indices(b,G):
    lookup={tuple(g):i for i,g in enumerate(G)};p,n=map(int,b['h'][4:6]);i=np.array([lookup[tuple(g)] for g in b['G']])
    return np.r_[np.arange(n),np.arange(p,p+n)],np.r_[i,len(G)+i]


def old_action(G):
    H=np.zeros((2*len(G),152),complex)
    for rank in [0,1]:
        b=decode(PRIVATE/'p1/host/pilot'/f'H.rank{rank}');i,j=global_indices(b,G)
        H[j]=sum(b[k][i,:152] for k in ['kin','loc','nl','fock'])
    return H
