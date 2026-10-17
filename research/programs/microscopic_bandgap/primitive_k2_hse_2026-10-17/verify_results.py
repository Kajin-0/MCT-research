"""Independent saved-state witness and focused integrity checks, no native calls."""
import hashlib
import json
from pathlib import Path
import subprocess
from xml.etree import ElementTree as ET

import h5py
import numpy as np
from scipy.optimize import brentq
from scipy.special import expit

P = Path(__file__).resolve().parent
B = P.parent
REPO = P.parents[3]
DFT = Path('/home/User/opencode_workspace/DFT')


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    f = json.loads((P/'preregistration.json').read_text())
    state = json.loads((P/'state_result.json').read_text())
    res = json.loads((P/'resources.json').read_text())
    root = Path(f['root'])
    save = root/'out/r07pk2.save'
    live=json.loads((P/'initial_live.json').read_text())
    native=[v for v in live['processes'] if Path(v['exe']).name=='pw.x']
    assert len(native)==2 and all(v['exe_sha256']==f['pins'][v['exe']] for v in native)
    assert live['kernel']['memory.max']==str(12*2**30)
    assert live['kernel']['memory.swap.max']=='0' and live['kernel']['pids.max']=='12'
    for p,h in {**f['pins'],**state['raw_pins'],**state['analysis_pins']}.items():
        assert sha(p)==h,p
    assert sha(root/'pw.in')==f['input_sha256']
    for name,src in [('host_pw.out',root/'pw.out'),('host_pw.err',root/'pw.err'),
                     ('host_data-file-schema.xml',save/'data-file-schema.xml')]:
        assert (P/name).read_bytes()==src.read_bytes()
    text=(root/'pw.out').read_bytes()
    assert text.startswith((P/'stop_stdout_prefix.txt').read_bytes())
    assert b'Calculation (EXX) stopped after iteration #    16' in text
    assert b'EXX self-consistency reached' not in text
    assert b'Maximum CPU time exceeded' not in text
    assert not state['native_outer_converged'] and len(state['trajectory'])==15
    assert state['XML_convergence']=='false'
    assert state['trajectory'][-1]['dexx_Ry']>1e-9
    assert state['inner_scf_error_Ry']<=1e-9
    assert not state['symmetry_1e8_qualified'] and not state['stationary_nonmagnetic_host_accepted']
    assert state['Cd_runs']==0 and state['physical_xc'] is None
    assert abs(state['charge_error_e'])<1e-8 and abs(state['independent_rhoG_charge_error_e'])<1e-8

    # Independent manual Theta on ONE actual occupied Gamma spinor.
    # No imported transformation/QR helper and no assumed Kramers span.
    out=ET.parse(save/'data-file-schema.xml').find('output')
    rows=out.findall('band_structure/ks_energies')
    e=np.array([2*np.fromstring(row.findtext('eigenvalues'),sep=' ') for row in rows])
    occ=np.array([np.fromstring(row.findtext('occupations'),sep=' ') for row in rows])
    weights=np.array([float(row.find('k_point').attrib['weight']) for row in rows])
    mu_native=2*float(out.findtext('band_structure/fermi_energy'))
    mu_root=brentq(lambda x:np.sum(weights[:,None]*expit((x-e)/.001))-36,
                   float(e.min()-1),float(e.max()+1),xtol=1e-15)
    root_charge=float(np.sum(weights[:,None]*expit((mu_root-e)/.001))-36)
    assert abs(root_charge)<1e-10
    with h5py.File(save/'wfc1.hdf5','r') as h:
        g=h['MillerIndices'][:].astype(int)
        c=np.ascontiguousarray(h['evc'][:]).view(complex).reshape(44,2,len(g))
        assert np.linalg.norm(h.attrs['xk'])<1e-14
    lookup={tuple(v):i for i,v in enumerate(g)}
    inv=np.array([lookup[tuple(-v)] for v in g])
    u=c[34].copy()
    theta=np.empty_like(u)
    theta[0,inv]=u[1].conj()
    theta[1,inv]=-u[0].conj()
    flat=c.reshape(44,-1)
    expect=float(np.dot(occ[0],abs(flat.conj()@u.reshape(-1))**2))
    expect_theta=float(np.dot(occ[0],abs(flat.conj()@theta.reshape(-1))**2))
    witness=(expect-expect_theta)/float(np.vdot(u,u).real)
    assert abs(witness)>1e-8
    assert abs(witness)<=state['stored_irreducible_states'][0]['Theta']['op']+1e-10
    assert max(q['Gram_op'] for q in state['stored_irreducible_states'])<1e-8
    assert max(q['Theta_squared_error'] for q in state['stored_irreducible_states'])<1e-14
    assert max(q['FD_max_error'] for q in state['stored_irreducible_states'])<1e-8
    assert len(state['full_BZ_Td_covariance'])==192
    assert len(state['full_BZ_reconstructed_Theta'])==8
    assert state['XML_cartesian_Td_group_verified'] and state['native_nsym']==24
    assert state['native_nrot']==48
    assert res['kernel_MemoryPeak_B']<12*2**30 and res['swap_peak_B']==0
    assert res['sampled_tasks_peak']<=12 and res['elapsed_OS_wall_s']<21600
    assert res['sampled_MemAvailable_min_B']>=4*2**30 and res['sampled_disk_free_min_B']>=10*2**30
    assert res['sampled_owned_blocks_metadata_max_B']<14*2**30
    assert res['monitor_terminal_complete'] and res['no_resource_refusal']
    cleanup=json.loads((P/'cleanup.json').read_text())
    assert cleanup['original_cgroup_absent'] and not Path(cleanup['original_cgroup']).exists()
    assert 'LoadState=not-found' in cleanup['after']

    # Preserve the same822 immutable source/data pins and76 historical files.
    old=B/'static_environment_2026-10-15'
    pins=dict(json.loads((old/'frozen_protocol.json').read_text())['profile']['pins'])
    pins.update({p:v['sha256'] for p,v in json.loads((old/'evidence_manifest.json').read_text())['raw'].items()})
    build=json.loads((B/'pbe_density_driver_2026-10-16/source_build_evidence.json').read_text())
    for key in ['linked_archive_pins','compiler_object_pins','compiled_module_pins']:
        pins.update(build[key])
    protection=json.loads((old/'protected_before.json').read_text())
    pins.update(protection['files'])
    assert len(pins)==822
    for name,h in pins.items():
        assert sha(name)==h,name
    assert subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)==protection['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','-C',str(DFT),'diff','--binary'])).hexdigest()==protection['DFT_tracked_diff_sha256']
    count=0
    folders=['pbe_density_driver_2026-10-16','pbe_static_lifecycle_2026-10-16',
             'pbe_static_completion_2026-10-16','pbe_density_only_feasibility_2026-10-16']
    for folder in folders+['pbe_final_admission_2026-10-16','stock_hse_stationary_2026-10-16']:
        prefix=str((B/folder).relative_to(REPO))
        names=subprocess.check_output(['git','ls-tree','-r','--name-only','53ca7b3',prefix],text=True).splitlines()
        if folder in folders:
            count+=len(names)
        for name in names:
            assert (REPO/name).read_bytes()==subprocess.check_output(['git','show','53ca7b3:'+name]),name
    assert count==76
    assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='research/hgcdte-impurity-tmatrix-20261010'
    manifest={str(q):dict(sha256=sha(q),size_B=q.stat().st_size,blocks_B=q.stat().st_blocks*512)
              for q in sorted(root.rglob('*')) if q.is_file()}
    (P/'raw_manifest.json').write_text(json.dumps(dict(root=str(root),files=manifest),indent=2)+'\n')
    result=dict(verified=True,meaning='Verification of observed failed candidate, NOT host SCF or symmetry PASS',
                independent_Gamma_band35_Theta_density_scalar_witness=witness,
                independent_FD_mu_Ry=mu_root,native_mu_Ry=mu_native,
                independent_mu_shift_eV=(mu_root-mu_native)*13.605693122994,
                independent_root_charge_residual_e=root_charge,
                protected_pins_unchanged=822,historical_original_files_unchanged=76,
                prior_stock8_and_closed_PBE_unchanged=True,DFT_dirty_unchanged=True,
                one_native_control_no_retry=True,no_owned_native_job_remaining=True,
                native_occupied_density_symmetry_failed=True,native_outer_converged=False,
                investigator_early_stop_not_preregistered_plateau=True,
                raw_file_count=len(manifest),physical_xc=None)
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
