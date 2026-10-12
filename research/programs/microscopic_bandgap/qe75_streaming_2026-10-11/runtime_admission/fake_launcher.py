"""Exactly two tiny test workers; never starts MPI/QE or accepts arbitrary argv."""
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
root=Path(sys.argv[1])
workers=[subprocess.Popen([sys.executable,str(HERE/'fake_worker.py'),str(root),str(rank)],close_fds=True)
         for rank in range(2)]
codes=[worker.wait() for worker in workers]
sys.exit(0 if all(code==0 for code in codes) else 7)
