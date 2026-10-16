"""Source pins and exact storage/conditional observable arithmetic, no launch."""
import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from audit_retained import HERE, OLD, digest


def main():
    frozen = json.loads((OLD/'frozen_protocol.json').read_text())
    pins = frozen['profile']['pins']
    selected = {p:s for p,s in pins.items() if '/build1/' in p or '/pp/' in p or p.endswith('/bin/pw.x')}
    for p, s in selected.items(): assert digest(p) == s, p
    # The inherited archive is explicitly fixed in this model; no live driver import.
    source = Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8r_20261015/build1/source')
    exx = (source/'pristine_exx.f90').read_text()
    assert 'ALLOCATE( exxbuff(nrxxs*npol,ibnd_buff_start:' in exx
    private = (source/'exx.f90').read_text()
    assert 'pilot_cycle>2' in private and 'CALL vexx(npwx,nnpw,6,pilot_probe,reference_action,becpsi)' in private
    store = HERE.parent/'qe75_streaming_2026-10-11/exx_qstream.f90'
    s = store.read_text()
    assert 'units /= 16' in s and 'INT(nq,int64)' in s and 'unexpected stream extent' in s
    GiB = 1 << 30
    payload = 16*64**3*2*352*8
    assert payload == 22*GiB and payload > 14*GiB and payload/8 == 2.75*GiB
    r = json.loads((HERE/'retained_result.json').read_text())
    g, da = r['chemical']['c2']['trace_meV'], abs(r['chemical']['change']['trace_meV'])
    old = json.loads((OLD/'numerical_result.json').read_text())
    steps = {m:old['members'][m]['operators']['relaxation']['total']['ordering_eV']*1000 for m in ('host', 'cd')}
    B = sum(abs(v) for v in steps.values())
    cold_path = HERE.parent/'qe75_streaming_2026-10-11/fermi_root_2026-10-14/cold_root.f90'
    cold = cold_path.read_text()
    assert 'nb/=48.OR.nk/=3.OR.is/=0.OR.ne/=36._DP.OR.sigma/=.001_DP' in cold
    output = dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(), native_jobs=0,
        preserved_private_source_ELF_PP_pins=selected, stream_source_sha256=digest(store),
        memory_and_storage=dict(A_exxbuff_nominal_B=16*60**3*2*176,
          B_stock_exxbuff_nominal_B=payload, B_stream_resident_plane_nominal_B=payload//8,
          B_stream_full_generation_bytes=payload, inherited_owned_output_cap_B=14*GiB,
          B_stream_exceeds_output_cap_B=payload-14*GiB,
          B_single_generation_plus_disk_floor_B=payload+10*GiB,
          total_two_rank_RSS_or_wall_bound_qualified=False,
          no_new_native_admission=True),
        conditional_observable_contraction=dict(chemical_last_increment_abs_meV=da,
          separate_member_last_increments_meV=steps, separate_member_absolute_sum_meV=B,
          uniform_chemical_increment_q_sign_threshold=g/(g+da),
          common_separate_member_increment_q_sign_threshold=g/(g+B),
          q_measured_or_certified=False, mathematical_bound='tail <= q B/(1-q) only with an independently uniform future-increment certificate'),
        state_scope='FD sigma=.001Ry in A; original e90 reference and safeguarded tiny solver are COLD, not substituted into A',
        cold_solver_guard=dict(sha256=digest(cold_path), nbnd=48, nk=3, nelec=36,
                              transfers_to_A_176_144_or_B_352_288=False))
    # Check actual original reference.bin physical embedding without importing DFT.
    data = np.load(HERE/'contracted_actions.npz'); G = data['G']; F = data['reference']
    p = OLD/'evidence/host/reference.bin'; b = p.read_bytes(); pos = 0
    def take(dt, shape):
        nonlocal pos
        n = int(np.prod(shape)); a = np.frombuffer(b,dt,n,pos).reshape(shape,order='F')
        pos += n*np.dtype(dt).itemsize; return a
    assert tuple(take('<i8',(4,))) == (70251406,7809,6,1)
    take('<f8',(3,3)); take('<f8',(3,)); labels=take('<i8',(3,7809)).T; coeff=take('<c16',(15618,6)); assert pos == len(b)
    expected = np.zeros_like(F); lookup={tuple(g):i for i,g in enumerate(G)}
    ix=np.array([lookup[tuple(g)] for g in labels]); expected[ix]=coeff[:7809]; expected[len(G)+ix]=coeff[7809:]
    assert expected.tobytes() == F.tobytes()
    output['fixed_reference_embedding'] = dict(reference_sha256=digest(p), source_G=7809,
      target_G=10827, bitwise_embedded=True, physical_frame_changed=False,
      e90_stationary_reference_silently_substituted=False)
    (HERE/'source_and_budget.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='preserved_private_source_ELF_PP_pins'},indent=2))


if __name__ == '__main__': main()
