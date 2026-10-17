"""One-case stdlib OS sampling and frozen printed-spectrum stop guideline.

No science launch, lease, FD inventory, native call, restart or state acceptance.
Run the pinned copy in this case's private root. Stock systemd owns the worker.
"""
from pathlib import Path
import datetime
import json
import os
import re
import shutil
import subprocess
import time


def numbers(lines, start):
    ans = []
    for line in lines[start:]:
        if not line.strip():
            if ans:
                break
            continue
        ans += [float(x) for x in re.findall(r'[-+]?\d+\.\d+', line)]
    return ans


def progress(text):
    lines = text.splitlines()
    if text and not text.endswith('\n'):
        lines = lines[:-1]
    residuals = []
    blocks = []
    upper_occupations = []
    for i, line in enumerate(lines):
        if 'est. exchange err (dexx)' in line:
            match = re.search(r'=\s*([-+0-9.Ee]+)\s+Ry',line)
            if match:
                residuals.append(float(match.group(1)))
        if 'occupation numbers' in line:
            all_f = numbers(lines,i+1)
            if len(all_f)==44:
                upper_occupations.append(all_f[-1])
        if not re.search(r'k\s*=\s*0\.0000\s+0\.0000\s+0\.0000', line):
            continue
        e = numbers(lines, i+2)
        occ_start = next((j for j in range(i+2, min(i+22, len(lines)))
                          if 'occupation numbers' in lines[j]), None)
        f = numbers(lines, occ_start+1) if occ_start is not None else []
        if len(e) != 44 or len(f) != 44:
            continue
        blocks.append(dict(Gamma6_candidate_spread_eV=max(e[32:34])-min(e[32:34]),
                           Gamma8_candidate_spread_eV=max(e[34:38])-min(e[34:38]),
                           Gamma8_candidate_occupations=f[34:38],
                           occupation_spread=max(f[34:38])-min(f[34:38]),
                           separated=(e[34]-e[33]>.01 and e[38]-e[37]>.01)))
    completed = len(residuals)+1 if residuals else 0
    trigger = False
    if completed >= 12 and len(blocks) >= 3:
        last = blocks[-3:]
        spread = [v['Gamma8_candidate_spread_eV'] for v in last]
        trigger = (all(s>.2 for s in spread) and spread[-1]>=spread[0]-.0002
                   and blocks[0]['occupation_spread']<=.1
                   and all(v['occupation_spread']>=.8 and v['separated'] for v in last)
                   and all(v>1e-8 for v in residuals[-3:])
                   and residuals[-1]>=.5*residuals[-3])
    return dict(completed_source_builds=completed, residuals_Ry=residuals,
                latest_Gamma_candidate_blocks=blocks[-3:],
                topmost_printed_occupation_max=max(upper_occupations,default=0),
                reached_EXX='EXX self-consistency reached' in text,
                provisional_index_stop_guideline=bool(trigger),
                note='Printed index probes only; final G-labelled spinors must qualify/refute sector labels. No density-Theta inference.')


def main():
    root = Path(__file__).resolve().parent
    frozen = json.loads((root/'preregistration.json').read_text())
    assert root == Path(frozen['root'])
    unit = frozen['unit']
    env = os.environ.copy()
    env.update(XDG_RUNTIME_DIR='/run/user/1001', DBUS_SESSION_BUS_ADDRESS='unix:path=/run/user/1001/bus')
    keys = ['LoadState','ActiveState','SubState','InvocationID','MainPID','ControlGroup',
            'Result','NRestarts','ExecMainCode','ExecMainStatus','MemoryPeak','MemorySwapPeak',
            'ExecMainStartTimestampMonotonic','ExecMainExitTimestampMonotonic']
    invocation = None
    startup_deadline = time.monotonic()+120
    deadline = time.monotonic()+86600
    with (root/'resource_samples.jsonl').open('x', buffering=1) as log:
        while time.monotonic()<deadline:
            proc = subprocess.run(['systemctl','--user','show',unit]+
                                  [v for k in keys for v in ['-p',k]],
                                  env=env, capture_output=True, text=True, timeout=10)
            manager = dict(s.split('=',1) for s in proc.stdout.splitlines() if '=' in s)
            if invocation is None and manager.get('LoadState')=='not-found':
                if time.monotonic()>startup_deadline:
                    raise RuntimeError('worker did not appear within120s; no launch/retry by observer')
                time.sleep(1)
                continue
            current = manager.get('InvocationID')
            if not current or (invocation is not None and current != invocation):
                raise RuntimeError('missing/changed invocation; refuse to act on replacement')
            invocation = current
            mem = int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines()
                           if x.startswith('MemAvailable:')))*1024
            files = [q for folder in [root,Path(frozen['artifact_dir'])]
                     for q in folder.rglob('*') if q.is_file()]
            owned = 0
            vanished = 0
            for q in files:
                try:
                    owned += q.stat().st_blocks*512+4096
                except FileNotFoundError:
                    vanished += 1
            row = dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       manager=manager, host_available_B=mem,
                       disk_free_B=shutil.disk_usage(root).free, owned_sampled_B=owned,
                       files_vanished_during_sample=vanished)
            hazard = (proc.returncode != 0 or mem<4*2**30 or row['disk_free_B']<10*2**30
                      or owned>14*2**30)
            if manager.get('SubState')=='running' and manager.get('ControlGroup'):
                cg = Path('/sys/fs/cgroup'+manager['ControlGroup'])
                try:
                    row['kernel'] = {k:(cg/k).read_text().strip() for k in
                                     ['memory.current','memory.peak','memory.swap.current',
                                      'memory.events','pids.current','cgroup.procs']}
                    rss = 0
                    for pid in row['kernel']['cgroup.procs'].split():
                        try:
                            rss += int(next(x.split()[1] for x in
                                       (Path('/proc')/pid/'status').read_text().splitlines()
                                       if x.startswith('VmRSS:')))*1024
                        except (FileNotFoundError, StopIteration):
                            pass
                    row['family_RSS_B_shared_overcount'] = rss
                except FileNotFoundError:
                    row['terminal_cgroup_disappearance_race'] = True
            out = root/'pw.out'
            if out.exists():
                if out.stat().st_size > 16*2**20:
                    hazard = True
                    row['observer_log_read_cap_refusal'] = True
                else:
                    info = progress(out.read_text(errors='strict'))
                    row['science'] = info
                    (root/'science_progress.json').write_text(json.dumps(info,indent=2)+'\n')
                    band_refusal=info['topmost_printed_occupation_max']>=.0001
                    if ((info['provisional_index_stop_guideline'] or band_refusal)
                            and manager.get('SubState')=='running' and not info['reached_EXX'] and not
                            (root/'scientific_stop_request.json').exists()):
                        (root/'scientific_stop_request.json').write_text(json.dumps(row,indent=2)+'\n')
                        with (root/'r07pk4.EXIT').open('x') as stream:
                            stream.write('Frozen R07 trajectory-stop guideline met. Save all; no restart.\n')
            log.write(json.dumps(row)+'\n')
            if hazard:
                (root/'resource_refusal.json').write_text(json.dumps(row,indent=2)+'\n')
                subprocess.run(['systemctl','--user','stop',unit],env=env,timeout=40,check=True)
                return
            exited = int(manager.get('ExecMainExitTimestampMonotonic','0') or '0')>0
            if (manager.get('ActiveState')=='failed' or
                    (manager.get('SubState') in {'exited','dead','failed'} and exited)):
                (root/'terminal_manager.json').write_text(json.dumps(row,indent=2)+'\n')
                return
            time.sleep(30)
    raise RuntimeError('observer finite deadline reached')


if __name__ == '__main__':
    main()
