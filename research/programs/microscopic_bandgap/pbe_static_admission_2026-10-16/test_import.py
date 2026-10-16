"""Isolated production-import preflight and dependency failure injection only."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = HERE.parents[3]
OLD = BASE/'static_environment_2026-10-15'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    scratch = REPO/'.tmp/r07_static_admission_20261016'
    scratch.mkdir(parents=True,exist_ok=True)
    oldpin = sha(OLD/'readback.py')
    legacy = BASE/'hybrid_convergence_2026-10-15/packets.py'
    tree = ast.parse(legacy.read_text())
    node = next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name == 'Reader')
    exact_class = ast.get_source_segment(legacy.read_text(),node)
    # Same bounded Reader class, with its TRUE minimal import closure, rather
    # than importing a whole HSE packet module and the protected DFT package.
    dependency = '"""Exact legacy Reader class; isolated minimal dependencies."""\nfrom pathlib import Path\nimport numpy as np\n\n'+exact_class+'\n'
    (HERE/'packet_reader.py').write_text(dependency)
    assert ast.dump(ast.parse(dependency).body[-1]) == ast.dump(node)
    raw = (OLD/'readback.py').read_text()
    body = raw.replace("PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16h_20261015')",
        "PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16h_20261015/jobs/p2')")
    body = body.replace('"""Native static actions, exact saved rhoG and genuine independent Theta trials."""',
        '"""IMPORT-FIX CANDIDATE ONLY; not a qualified new science/owner validator.\n\n'
        'Legacy science logic is retained for dependency testing, NOT certified\n'
        'for the new metric/error-budget contract. No native admission authority.\n"""')
    oldimport = "sys.path.insert(0,str(BASE/'native_matched_pilot_2026-10-11'))\nfrom packets import Reader"
    newimport = """import hashlib,importlib.util
_reader=HERE/'packet_reader.py'
if hashlib.sha256(_reader.read_bytes()).hexdigest()!='READER_SHA':
    raise ImportError('pinned Reader dependency changed')
_spec=importlib.util.spec_from_file_location('_r07_static_pbe_reader_v1',_reader)
_module=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
Reader=_module.Reader""".replace('READER_SHA',sha(HERE/'packet_reader.py'))
    assert oldimport in body
    body = body.replace(oldimport,newimport)
    anchor = 'def validate(root,member):\n'
    assert body.count(anchor) == 1
    body = body.replace(anchor,anchor+"    if member not in ['unshared','shared'] or Path(root)!=PRIVATE/'jobs'/member:\n        raise ValueError('new-scope roots only; refused historical unit cannot be accepted')\n")
    candidate = HERE/'readback_prospective.py'
    candidate.write_text(body)
    (HERE/'readback_import.patch').write_text(''.join(difflib.unified_diff(
        raw.splitlines(True),body.splitlines(True),fromfile='frozen/readback.py',tofile='prospective/readback.py',n=0)))
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    env.pop('PYTHONPATH',None)
    load = """import importlib.util,json,sys
s=importlib.util.spec_from_file_location('reader_under_test',sys.argv[1])
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
assert callable(m.Reader) and callable(m.decode) and callable(m.validate)
print(json.dumps({'imported':True,'reader_file':m._reader.as_posix()}))
"""
    with tempfile.TemporaryDirectory(prefix='import-',dir=scratch) as td:
        # Every subprocess has a clean module cache and unrelated scratch cwd.
        original = subprocess.run([sys.executable,'-B','-c',load,str(OLD/'readback.py')],
            cwd=td,env=env,capture_output=True,text=True,timeout=15)
        assert original.returncode and "No module named 'packets'" in original.stderr
        passing = subprocess.run([sys.executable,'-B','-c',load,str(candidate)],
            cwd=td,env=env,capture_output=True,text=True,timeout=15)
        assert passing.returncode == 0, passing.stderr
        clone = Path(td)/'readback_prospective.py'
        clone.write_text(body)
        absent = subprocess.run([sys.executable,'-B','-c',load,str(clone)],
            cwd=td,env=env,capture_output=True,text=True,timeout=15)
        assert absent.returncode and 'packet_reader.py' in absent.stderr
        (Path(td)/'packet_reader.py').write_text(dependency+'\n# injected corruption\n')
        corrupt = subprocess.run([sys.executable,'-B','-c',load,str(clone)],
            cwd=td,env=env,capture_output=True,text=True,timeout=15)
        assert corrupt.returncode and 'pinned Reader dependency changed' in corrupt.stderr
        # Explicit format-only decode, never validate/reclassify old physics.
        program = load+"""
from pathlib import Path
try:m.validate(Path(sys.argv[2]).parent.parent,'unshared')
except ValueError:pass
else:raise AssertionError('historical root accepted')
p=m.decode(Path(sys.argv[2]))
assert int(p['h'][0])==70251521 and int(p['h'][13])==12
print(json.dumps({'FORMAT_ONLY_unqualified_packet':True,'rank':int(p['h'][2]),'queries':12}))
"""
        packet = Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16h_20261015/jobs/unshared/pilot/H.rank0')
        decoded = subprocess.run([sys.executable,'-B','-c',program,str(candidate),str(packet)],
            cwd=td,env=env,capture_output=True,text=True,timeout=20)
        assert decoded.returncode == 0, decoded.stderr
    assert sha(OLD/'readback.py') == oldpin
    out = dict(status='PASS isolated import/dependency tests; native validation NOT executed',
        historical_missing_packets_reproduced=True,explicit_new_dependency_import_pass=True,
        missing_dependency_refused=True,corrupt_dependency_refused=True,
        copied_Reader_AST_identical=True,old_native_packet_FORMAT_ONLY_decode=True,
        historical_root_validate_refused=True,original_readback_unchanged=True,
        native_jobs=0,DFT_writes=0,native_release=False,
        outputs=dict(success_stdout=passing.stdout,format_stdout=decoded.stdout),
        pins={str(p):sha(p) for p in [OLD/'readback.py',legacy,HERE/'packet_reader.py',candidate]})
    (HERE/'import_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
