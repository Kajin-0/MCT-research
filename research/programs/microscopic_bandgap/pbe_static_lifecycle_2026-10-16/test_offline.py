"""Focused pre-service checks. No service/MPI/QE. Modeled cases labeled."""
from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import owner,reader
from protocol import Protocol,Refusal,kernel,sha,durable
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3]

def refuses(fn,word=None):
    try:fn()
    except Exception as e:
        if word:assert word in str(e),str(e)
        return str(e)
    raise AssertionError('missing refusal')

def main():
    old=HERE.parent/'pbe_static_completion_2026-10-16'
    transformed=(old/'native_lease.c').read_text().replace('Narrow PBE16 receipt ABI','NON_SCIENCE lifecycle receipt ABI').replace('R07_STATIC_','R07_LIFECYCLE_').replace('R07S','R07L').replace('reply+12)!=16','reply+12)!=1601')
    assert transformed==(HERE/'native_lease.c').read_text()
    # The original physics release still refuses; import only, no native CLI.
    spec=importlib.util.spec_from_file_location('old_owner_source',old/'owner.py')
    original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
    tests={'C_ABI_exact_except_dedicated_namespace_magic_scope_comment':True,
           'original_science_release_still_refuses':refuses(lambda:original.load('unshared'),'no native execution release')}
    private=REPO/'.tmp/r07spc16';private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='offline-a-',dir=private) as tmp:
        root=Path(tmp);path=root/'packet';path.write_text('{"kind":"science"}')
        tests['science_packet_rejected']=refuses(lambda:reader.decode(path),'NON_SCIENCE')
        path.write_text('{"kind":1,"kind":2}')
        tests['duplicate_keys_rejected']=refuses(lambda:reader.decode(path),'duplicate')
        p=Protocol(root,{}, {},'/modeled','a'*32,lambda *a:None,lambda:None)
        class P:
            pid=123
            dead=False
            def exited(self):return self.dead
        peer=P();p.peers={0:peer};p.finals={0,1}
        tests['MODELED_live_FD_denial_absorbing']=refuses(lambda:p.inventory_failure(123,PermissionError()),'STILL LIVE')
        peer.dead=True;tests['MODELED_later_exit_not_retropass']=refuses(p.live,'absorbing')
        p=Protocol(root,{}, {},'/modeled','a'*32,lambda *a:None,lambda:None)
        tests['MODELED_cancel_crash_no_receipts_no_terminal']=refuses(lambda:p.terminal(None,'x',(0,0),None,None),'lost/live rank')
        p=Protocol(root,{}, {},'/modeled','a'*32,lambda *a:None,lambda:None)
        p.peers={0:peer};p.finals={0,1}
        try:p.inventory_failure(123,FileNotFoundError())
        except kernel.TerminalPending:pass
        else:raise AssertionError('no pending')
        assert 0<p.deadline-__import__('time').monotonic()<=3
        tests['MODELED_exited_only_three_second_pending']=True
        result=root/'immutable.json';durable(result,{'status':'FAIL'})
        tests['failure_cannot_overwrite_to_PASS']=refuses(lambda:durable(result,{'status':'PASS'}))
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None)
        program='import sys;sys.path.insert(0,sys.argv[1]);import owner,reader,protocol;assert owner.KIND=="R07_GATE_A_MPI_LIFECYCLE_NON_SCIENCE_V1";print("ISOLATED_IMPORT_OK")'
        r=subprocess.run([sys.executable,'-B','-c',program,str(HERE)],cwd=tmp,env=env,capture_output=True,text=True,timeout=10)
        assert r.returncode==0,r.stderr
        tests['clean_subprocess_owner_reader_import']=r.stdout.strip()
    result=dict(status='PASS_OFFLINE_ONLY',tests=tests,manager_cgroup_and_receipts_MODELED=True,
        actual_MPI=False,actual_systemd=False,live_crash_cancel_NOT_exercised=True)
    durable(HERE/'offline_results.json',result);print(json.dumps(result))

if __name__=='__main__':main()
