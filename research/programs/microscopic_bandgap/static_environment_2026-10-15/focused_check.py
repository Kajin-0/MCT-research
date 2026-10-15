"""Independent math/import/negative-record checks, no native execution/retry."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from scipy.special import expit
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    target=HERE/'focused_check.json'
    if target.exists():raise FileExistsError('preserve first focused verification')
    # Test prospective Reader import IN MEMORY; frozen production file is unchanged.
    raw=(HERE/'readback.py').read_text();pin=sha(HERE/'readback.py');fixed=raw.replace("BASE/'native_matched_pilot_2026-10-11'","BASE/'hybrid_convergence_2026-10-15'")
    assert fixed!=raw;ns={'__file__':str(HERE/'readback.py'),'__name__':'r07_prospective_reader_import'};exec(compile(fixed,'prospective-reader','exec'),ns);assert sha(HERE/'readback.py')==pin
    root=ns['PRIVATE']/'jobs/unshared';packet=ns['decode'](root/'pilot/H.rank0');assert packet['h'][13]==12
    # Independent finite-HS FD Lipschitz check; supports theorem, NOT native splice.
    rng=np.random.default_rng(7731);X=rng.normal(size=(12,12))+1j*rng.normal(size=(12,12));A=(X+X.conj().T)/2;Z=rng.normal(size=(12,12))+1j*rng.normal(size=(12,12));E=1e-4*(Z+Z.conj().T)/2;sigma=.001
    def fd(H):
        e,U=np.linalg.eigh(H);return (U*expit(-e/sigma))@U.conj().T
    actual=float(np.linalg.norm(fd(A+E)-fd(A),'fro'));bound=float(np.linalg.norm(E,'fro')/(4*sigma));assert actual<=bound
    old=BASE/'pair_environment_2026-10-15';a=np.load(old/'complex_overlaps.npz');C=np.vstack((a['unshared_Gamma6'],a['unshared_Gamma8']));e=np.loadtxt(old/'unshared_Gamma6_spectrum.csv',delimiter=',',skiprows=1)[:,2];G=(C/(.05j-e))@C.conj().T;K=.05j*np.eye(6)-np.linalg.inv(G);trace=lambda M:float((np.trace(M[:2,:2])/2-np.trace(M[2:,2:])/4).real)
    comparison=json.loads((HERE/'unshared_spectral_comparison.json').read_text());assert abs(trace(K)-comparison['accepted_retained_inverse_trace_eta05_eV'])<1e-13
    g=json.loads((root/'GUARD_RESULT.json').read_text());assert not g['pass_guard'] and not (ns['PRIVATE']/'jobs/shared/LAUNCH.json').exists()
    assert 'ModuleNotFoundError' in (HERE/'unshared_diagnostic.log').read_text()
    output=dict(status='PASS focused checks; owner/native pair remains FAILED/NOT RUN',prospective_Reader_patch_import_and_native_decode_PASS=True,frozen_production_source_NOT_modified=True,original_import_failure_preserved=True,independent_FD_HS_actual=actual,independent_FD_HS_upper_bound=bound,accepted_inverse_trace_reconstruction_eV=trace(K),no_304splice_or_native_retry=True,no_accepted_matched_static_result=True,source_sha256=sha(Path(__file__)),production_readback_sha256=pin)
    target.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))


if __name__=='__main__':main()
