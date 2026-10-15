"""Preserve exact native evidence and check protected state after BOTH members."""
from pathlib import Path
import json,subprocess
import owner as r
from prepare_pair import protected


def main():
    if (r.HERE/'evidence_manifest.json').exists():raise FileExistsError('preserve original archive')
    files={};inventories=[];storage=r.LinuxGuard(r.LIB)
    for member in ['unshared','shared']:
        profile,job,root=r.load(member);f=json.loads((root/'FINAL.json').read_text());assert f['accepted'] and f['terminal_pass']
        assert not r.cgroup_path(f['guard']['cgroup']).exists()
        folder=r.HERE/'evidence'/member;folder.mkdir(parents=True)
        for name in ['pw.in','pw.out','JOB.json','READY.json','REFERENCED.json','LAUNCH.json','RANKS.json','GUARD_RESULT.json','TERMINAL.json','FINAL.json','telemetry.jsonl','launch_stderr.json']:
            p=root/name;target=folder/name;target.write_bytes(p.read_bytes());assert r.sha(p)==r.sha(target);files[str(p)]=dict(sha256=r.sha(p),archived=str(target.relative_to(r.HERE)))
        for name in ['data-file-schema.xml','wfc1.hdf5','charge-density.hdf5']:
            p=root/'out/r07pbe.save'/name;files[str(p)]=dict(sha256=r.sha(p),bytes=p.stat().st_size,kept_in_private_native_root=True)
            if name.endswith('.xml'):(folder/name).write_bytes(p.read_bytes())
        inventories.append(r.Account(root,14*2**30,64*2**20,storage).sample())
    charged=sum(i['budget_charge_bytes'] for i in inventories);assert charged<=14*2**30
    for name in ['pw.x','mpirun','prterun']:
        q=subprocess.run(['pgrep','-a','-x',name],text=True,capture_output=True);assert q.returncode==1 and not q.stdout
    assert json.loads(r.REGISTRY.read_text())['phase']=='FINISHED'
    # Source pins include old ledger indirectly; preserve actual registry bytes.
    before=json.loads((r.HERE/'protected_before.json').read_text());after=protected();assert before==after
    r.atomic_json(r.HERE/'protected_after.json',after)
    r.atomic_json(r.HERE/'final_output_inventory.json',dict(members=inventories,aggregate_charge_B=charged,sampled_not_continuous=True,no_live_known_MPI_QE=True,old_registry_sha256=r.sha(r.REGISTRY)))
    r.atomic_json(r.HERE/'evidence_manifest.json',dict(raw_files=files,numerical_result_sha256=r.sha(r.HERE/'numerical_result.json'),protected_state_pass=True,archive_code_sha256=r.sha(Path(__file__))))
    print(json.dumps(dict(protected_state_pass=True,aggregate_charge_B=charged,private_wave_and_density_preserved=True),indent=2))


if __name__=='__main__':main()
