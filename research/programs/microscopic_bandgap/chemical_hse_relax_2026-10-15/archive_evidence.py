"""Archive small native evidence, pin large private packets/waves without alteration."""
from pathlib import Path
import json,shutil
from datetime import datetime,timezone
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main():
    paths={}
    for member in ['host','cd']:
        root=r.PAIR/member
        final=json.loads((root/'FINAL.json').read_text())
        assert final['accepted'] and final['terminal_pass'] and final['scientific_pass']
        dest=HERE/'evidence'/member;dest.mkdir(parents=True,exist_ok=False)
        files=[root/n for n in ['pw.in','pw.out','JOB.json','READY.json','REFERENCED.json','LAUNCH.json','RANKS.json','GUARD_RESULT.json','TERMINAL.json','FINAL.json','telemetry.jsonl','reference.bin']]
        files+=[root/'out/r07hse8.save/data-file-schema.xml']
        for f in files:
            target=dest/f.name;shutil.copy2(f,target)
            paths[str(f)]=dict(sha256=r.sha(f),bytes=f.stat().st_size,archive_relative=str(target.relative_to(HERE)))
        for f in sorted((root/'pilot').iterdir())+sorted((root/'out/r07hse8.save').glob('*.hdf5')):
            paths[str(f)]=dict(sha256=r.sha(f),bytes=f.stat().st_size,retained_private=True)
        for f in [root/'pp'/n for n in ['Hg_sg15_pbe_fr_v12.UPF','Cd_sg15_pbe_fr_v12.UPF','Te_sg15_pbe_fr_v12.UPF']]:
            paths[str(f)]=dict(sha256=r.sha(f),bytes=f.stat().st_size,retained_private=True)
    (HERE/'evidence_manifest.json').write_text(json.dumps(dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='bce98cc',scope='real one-relaxation/second-ACE native pair; deliberately HSE unconverged',QE_ELF=str(r.QE),QE_ELF_sha256=r.sha(r.QE),files=paths),indent=2)+'\n')
    print('Archived native logs/state/owners and pinned all private packets/waves/PPs; no original evidence changed.')

if __name__=='__main__':main()
