"""Fixed compiled two-peer transport fixture. Never starts MPI/PW."""
import os
from pathlib import Path
import subprocess
import sys
import json
import time

HERE=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1]);job=json.loads((ROOT/'JOB.json').read_text())
EXE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/m5_integration/rank_worker')
env=dict(os.environ,QE75_TEST_PYTHON=sys.executable,QE75_TEST_HOOK=str(HERE/'fixture_hook.py'))
workers=[subprocess.Popen([str(EXE),str(rank),str(ROOT),job['scenario']],env=env,close_fds=True)
         for rank in range(2)]
if job['scenario']=='forged_hook':
    deadline=time.monotonic()+2
    while not (ROOT/'out/hook0.json').exists() and time.monotonic()<deadline: time.sleep(.005)
    subprocess.run([sys.executable,str(HERE/'fixture_hook.py'),str(ROOT),'forged'],check=True,env=env,timeout=2)
codes=[worker.wait() for worker in workers]
sys.exit(0 if all(code==0 for code in codes) else 7)
