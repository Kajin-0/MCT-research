"""Owned registered-C-process child; tests the production live bridge RPC only."""
import json
from pathlib import Path
import sys
from production_transport import digest,read_meta
from runtime_client import typed_request,authorize_native_hook
from process_identity import Refusal

root=Path(sys.argv[1]);mode=sys.argv[2];profile=digest(read_meta(root/'PROFILE.json'))
if mode=='forged':
    # This Python child of the launcher is pinned-owned but has no rank ancestor.
    try: typed_request(root,profile)
    except Refusal as error:
        (root/'out/forged_refusal.json').write_text(json.dumps({'reason':str(error)}));sys.exit(0)
    raise RuntimeError('unregistered launcher child was authorized')
receipt=typed_request(root,profile)
try: authorize_native_hook(root,profile,'authorize')
except Refusal as error: native_refusal=str(error)
else: raise RuntimeError('ABI child obtained native checkpoint authority')
(root/'out'/f"hook{receipt['world_rank']}.json").write_text(json.dumps({'receipt':receipt,'native_refusal':native_refusal}))
