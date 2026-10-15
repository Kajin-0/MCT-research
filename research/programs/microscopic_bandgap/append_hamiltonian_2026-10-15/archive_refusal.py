"""Preserve native refusal/provenance; never edits old or native records."""
from pathlib import Path
import json,subprocess
from accepted import HERE,PRIVATE,OLD,sha


def main():
    target=HERE/'evidence_manifest.json'
    if target.exists():raise FileExistsError('preserve first refusal archive')
    f=json.loads((HERE/'frozen_protocol.json').read_text())
    for p,h in f['profile']['pins'].items():assert sha(p)==h
    before=json.loads((OLD/'protected_after.json').read_text());DFT=PRIVATE.parents[2]
    assert DFT==Path('/home/User/opencode_workspace/DFT')
    assert subprocess.check_output(['git','-C',str(DFT),'status','--short'],text=True)==before['DFT_status']
    assert __import__('hashlib').sha256(subprocess.check_output(['git','-C',str(DFT),'diff','--binary'])).hexdigest()==before['DFT_tracked_diff_sha256']
    for p,h in before['files'].items():assert sha(p)==h
    root=PRIVATE/'p2/host';g=json.loads((root/'GUARD_RESULT.json').read_text());assert g['pass_guard']
    assert not (Path('/sys/fs/cgroup')/g['cgroup'].lstrip('/')).exists()
    assert not (root/'FINAL.json').exists() and not (HERE/'native_science.json').exists()
    ev=HERE/'evidence';ev.mkdir();records={}
    for name in ['pw.in','pw.out','JOB.json','READY.json','RANKS.json','LAUNCH.json','REFERENCED.json','GUARD_RESULT.json','TERMINAL.json','launch_stderr.json','launch_stdout.json','telemetry.jsonl']:
        src=root/name;dst=ev/name;dst.write_bytes(src.read_bytes());records[str(src)]=dict(sha256=sha(src),archived=str(dst.relative_to(HERE)))
    for p in (root/'pilot').iterdir():records[str(p)]=dict(sha256=sha(p),bytes=p.stat().st_size,private_raw_retained=True)
    total=sum(p.stat().st_blocks*512+4096 for p in PRIVATE.rglob('*') if p.is_file());assert total<14*2**30
    target.write_text(json.dumps(dict(status='VERIFIED original refusal preserved; NOT accepted splice',old_frozen_native_source_pins_PASS=True,protected_DFT_exact=True,cgroup_gone=True,all_shared_h8h_owned_bytes=total,no304splice_or_FDresult=True,raw=records,source_sha256=sha(Path(__file__))),indent=2)+'\n');print('PASS refusal/protected/raw/source archive; strict science FAIL preserved')


if __name__=='__main__':main()
