"""Source-conditioned HSE feasibility only. NO native launch interface."""
from pathlib import Path
import json
import re
import hashlib
import itertools
import sys
import subprocess
import numpy as np
import h5py
from xml.etree import ElementTree as ET

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
BASE=DFT/'.local/qe75_lowram_20261011'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def evaluate():
    manifest=json.loads((HERE.parent/'qe75_streaming_2026-10-11/source_manifest.json').read_text())
    src=BASE/'exx.f90';exxbase=BASE/'q-e/PW/src/exx_base.f90'
    assert sha(src)==manifest['files']['exx.f90']['sha256']
    blob=subprocess.check_output(['git','-C',str(BASE/'q-e'),'show','HEAD:PW/src/exx_base.f90'])
    assert hashlib.sha256(blob).hexdigest()==sha(exxbase)
    oldrun=BASE/'hse_native_probe_20261013';out=(oldrun/'pw.out').read_text();oldresult=json.loads((oldrun/'result.json').read_text())
    assert sha(oldrun/'pw.in')==oldresult['input_sha256'] and sha(oldrun/'pw.out')==oldresult['stdout_sha256']
    m=re.search(r'aceinit\s+:\s+[0-9.]+s CPU\s+([0-9.]+)s WALL\s+\(\s*(\d+) calls\)',out);assert m
    ACEwall=float(m[1]);calls=int(m[2]);nouter=oldresult['outer_exx_iterations'];perouter=ACEwall/nouter
    refFFT=[32,32,32];assert 'FFT dimensions: (  32,  32,  32)' in out
    tree=ET.parse(BASE/'chemical_pbe8_k2_e50_20261014/host/out/r07pbe.save/data-file-schema.xml')
    fft=tree.find('.//output/basis_set/fft_grid');grid=[int(fft.attrib[k]) for k in ['nr1','nr2','nr3']];assert grid==[60,60,60]
    measured=json.loads((HERE/'cutoff_result.json').read_text());krep=np.mod(np.array(measured['members']['host']['k_XML_vectors']),1)
    def nkq(ks,n):
        q=np.array(list(itertools.product([i/n for i in range(n)],repeat=3)))
        return len({tuple(np.round(np.mod(k+v,1),12)) for k in ks for v in q})
    assert nkq(krep,2)==8 and nkq(krep,1)==4 and nkq(np.zeros((1,3)),1)==1
    allPW=[]
    for path in (BASE/'chemical_pbe8_k2_e50_20261014/host/out/r07pbe.save').glob('wfc*.hdf5'):
        with h5py.File(path) as f:allPW.append(len(f['MillerIndices']))
    fftRatio=np.prod(grid)/np.prod(refFFT);records=[]
    for label,nks,nqx,nkqs in [('Gamma_k1_q1',1,1,1),('same_k2_q1',4,1,4),('same_k2_q2',4,2,8)]:
        # All ranks, one pool/bandgroup; complex16 spinors, no real shortcut.
        buffer=int(16*2*176*np.prod(grid)*nkqs)
        # Sum_rank(max_k ngk_rank) <= sum_k(global ngk) gives an upper bound
        # for xi ONLY, conditional on one-pool normal wave distribution.
        npwxsum=sum(allPW) if nks==4 else measured['members']['host']['native_Gamma_PW']
        ACEupper=int(16*2*176*nks*npwxsum)
        ratio=(176*144*nks*nqx**3)/(48*36*3*8)*fftRatio
        aceheur=perouter*ratio;PBEstarter=226.27/4 if nks==1 else 226.27
        records.append(dict(option=label,k_representatives=nks,q_mesh=[nqx]*3,Nq=nqx**3,Nkqs=nkqs,conditional_real_FFT_grid=grid,
            exxbuff_aggregate_bytes=buffer,exxbuff_aggregate_GiB=buffer/2**30,
            ACE_xi_aggregate_source_bound_bytes=ACEupper,retained_native_PBE_peak_bytes=1037570048,
            buffer_plus_xi_bound_plus_PBE_peak_GiB=(buffer+ACEupper+1037570048)/2**30,
            additional_backend_and_EXX_scratch_not_bounded=True,work_proxy_vs_retained_HSE=ratio,
            heuristic_ACE_rebuild_s=aceheur,heuristic_PBE_start_s=PBEstarter,
            heuristic_first_rebuild_total_s=PBEstarter+aceheur,heuristic_14_rebuilds_total_s=PBEstarter+14*aceheur,
            full600s_admission=False))
    # A next PBE3 mesh is analytically cheap: Td plus nonmagnetic TR gives
    # four stars on27 points, not27 independent diagonalizations.
    sys.path.insert(0,str(HERE.parent/'native_matched_pilot_2026-10-11'));from reference_irrep_check import td_operations
    points=np.array(list(itertools.product([0,1/3,2/3],repeat=3)));stars={}
    for point in points:
        orbit={tuple(np.round(np.mod(sign*point@op['spatial'].T,1),12)) for op in td_operations() for sign in [-1,1]}
        stars[min(orbit)]=len(orbit)
    assert sorted(stars.values())==[1,6,8,12]
    result=dict(status='SOURCE-CONDITIONED arrays / HEURISTIC times; HSE NOT ADMITTED OR LAUNCHED',source_commit=manifest['upstream_git_commit'],
        pristine_exx_SHA=sha(src),pristine_exx_base_SHA=sha(exxbase),source_matches_Git_blob=True,
        source_formulas=dict(exxbuff='complex16 * local_nnr * npol2 * bandgroup176 * Nkqs',xi='complex16 * local_npwx * npol2 * nbndproj176 * nks'),
        measured_reference=dict(input=str(oldrun/'pw.in'),input_sha256=sha(oldrun/'pw.in'),stdout_sha256=sha(oldrun/'pw.out'),nat=2,nbnd=48,nelec=36,
            irreducible_k=3,q_mesh=[2,2,2],FFT=refFFT,ACE_wall_s=ACEwall,ACE_calls=calls,outer_updates=nouter,
            mean_whole_outer_ACE_wall_s=perouter,fully_converged=oldresult['fully_converged']),
        options=records,heuristic_assumptions=['source occupied bands approximated by nelec; FD tails can increase work',
            'FFT60^3 follows same dense cutoff/cell/library IF layout unchanged; not a native HSE descriptor certificate',
            'FFT-volume times source/trial pair count excludes FFTlogs/kernels and changing SCF iterations',
            'old timing reference is cold90/360/120; new candidate FD50/200/200 is a different regime'],
        best_next_under_current600s=dict(experiment='matched PBE+SOC50/200Ry unshifted3x3x3 pair, SAME frames; NOT launched',full_points=27,
            nonmagnetic_Td_TR_star_sizes=sorted(stars.values()),representatives=4,estimated_member_wall_s=[220,260],not_BZ_convergence_guarantee=True),
        minimum_missing_HSE_input='actual eight-atom ACE/update timing, peak and descriptor under separately admitted scope; arrays alone cannot certify full600s SCF completion',
        HSE_native_runs_this_phase=0,physical_xc=None,analysis_source_sha256=sha(__file__))
    (HERE/'hse_feasibility.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for row in records:print(row['option'],'bufferGiB',row['exxbuff_aggregate_GiB'],'memory_subtotalGiB',row['buffer_plus_xi_bound_plus_PBE_peak_GiB'],'first_s',row['heuristic_first_rebuild_total_s'],'14_s',row['heuristic_14_rebuilds_total_s'])
    print('Next PBE3 star sizes',sorted(stars.values()));return result


if __name__=='__main__':
    if (HERE/'hse_feasibility.json').exists():raise FileExistsError('preserve assessment')
    evaluate()
