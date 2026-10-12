"""Explicit synthetic worker. Kernel lineage/IPC/resource tests, no native physics."""
import json
import os
from pathlib import Path
import signal
import sys
import time
from runtime_client import request
from process_identity import Refusal,proc

root=Path(sys.argv[1]);rank=int(sys.argv[2]);job=json.loads((root/'JOB.json').read_text())
request(root,'register',rank,2)
for attempt in range(40):
    try:
        authority=request(root,'authorize');break
    except Refusal as error:
        if 'registration incomplete' not in str(error): raise
        time.sleep(.02)
else: raise Refusal('bounded all-rank wait exhausted')
(root/'out'/f'authorized{rank}.json').write_text(json.dumps({'rank':rank,'pid':os.getpid(),
        'start_ticks':proc(os.getpid())['start_ticks'],'authority':'LIVE_KERNEL_LEASE_NO_NATIVE_PHYSICS'}))
if rank==0 and job['scenario'] in ['detach','race_orphan']:
    child=os.fork()
    if child==0:
        os.setsid();signal.signal(signal.SIGTERM,signal.SIG_IGN)
        (root/'out'/'detached_child.json').write_text(json.dumps(proc(os.getpid())))
        time.sleep(8);os._exit(0)
if job['scenario']=='fail' and rank==1: sys.exit(7)
if job['scenario']=='ignore_term': signal.signal(signal.SIGTERM,signal.SIG_IGN)
if job['scenario'] in ['hold','ignore_term']: time.sleep(8)
else: time.sleep(.15)
