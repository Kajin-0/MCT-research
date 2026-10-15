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


