"""Extend prior read-only preservation checks; never inspect foreign processes."""
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'software_2026-10-13'))
import preservation as prior
from native_bundle import artifact_sha256
from build_transport import PRIVATE


def check():
    result=prior.check()
    snapshot=json.loads((PRIVATE/'preservation_before.json').read_text())
    for path,digest in snapshot['capture_candidates'].items():
        if artifact_sha256(Path(path))!=digest:raise RuntimeError('prior capture changed: '+path)
    result['capture_candidates_unchanged']=True
    result['foreign_process_inventory_repeated']=False
    return result


if __name__=='__main__':print(json.dumps(check(),indent=2))
