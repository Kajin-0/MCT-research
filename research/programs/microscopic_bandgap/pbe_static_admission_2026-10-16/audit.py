"""Saved PBE inputs, exact frame and static-driver bounds; never native physics."""
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import Counter
from itertools import product
import hashlib
import json
import os
import numpy as np
import h5py
from scipy.special import expit

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OLD = BASE/'static_environment_2026-10-15'
DFT = Path('/home/User/opencode_workspace/DFT')
PRIVATE = DFT/'.local/qe75_lowram_20261011/p16h_20261015'
FUTURE = PRIVATE/'jobs/p2'  # only a proposed, NOT CREATED, fresh subtree


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def geometry(tree):
    at = tree.find('.//output/atomic_structure')
    A = np.array([np.fromstring(at.findtext('cell/a'+str(i)), sep=' ') for i in [1,2,3]])
    atoms = at.find('atomic_positions')
    names = [x.attrib['name'] for x in atoms]
    frac = np.array([np.fromstring(x.text, sep=' ') for x in atoms])@np.linalg.inv(A)
    ops = []
    for x in tree.findall('.//output/symmetries/symmetry'):
        if x.findtext('info') != 'crystal_symmetry':
            continue
        S = np.fromstring(x.findtext('rotation'), sep=' ').reshape(3,3)
        t = np.fromstring(x.findtext('fractional_translation'), sep=' ')
        eq = np.fromstring(x.findtext('equivalent_atoms'), sep=' ', dtype=int)-1
        d = frac@S.T+t-frac[eq]
        assert np.max(abs(d-np.rint(d))) < 1e-9
        assert all(names[i] == names[j] for i,j in enumerate(eq))
        ops.append((S,t))
    return A, names, frac, ops


def main():
    frozen = json.loads((OLD/'frozen_protocol.json').read_text())
    profile = frozen['profile']
    mismatch = {p:dict(expected=h,actual=sha(p)) for p,h in profile['pins'].items() if sha(p) != h}
    assert not mismatch, mismatch
    build = json.loads((OLD/'build_result.json').read_text())
    assert sha(build['binary']) == build['binary_sha256']
    assert sha(DFT/'.local/qe-env/lib/libqe_pw.a') == build['stock_archive_sha256']
    # The old failed unit is immutable evidence, NOT a new science input.
    failure = json.loads((OLD/'evidence/GUARD_RESULT.json').read_text())
    terminal = json.loads((OLD/'evidence/TERMINAL.json').read_text())
    assert not failure['pass_guard'] and not terminal['terminal']
    assert failure['rank_kernel_exits'] == {'0':False,'1':False}
    assert 'unbound/incomplete owned task FD inventory' in failure['error']
    assert not (PRIVATE/'jobs/shared/LAUNCH.json').exists()
    raw = json.loads((OLD/'evidence_manifest.json').read_text())['raw']
    for p, row in raw.items():
        assert sha(p) == row['sha256'], p
    framepath = PRIVATE/'physical_frame.npz'
    frame = np.load(framepath)
    P,G,B = frame['P'], frame['G'], frame['B']
    N = len(G)
    assert P.shape == (2*N,6) and N == 21595
    ref = json.loads((BASE/'chemical_pbe16_p2_2026-10-15/host_readback_v2.json').read_text())
    assert ref['scientific_pass'] and ref['terminal']['terminal']
    host = DFT/'.local/qe75_lowram_20261011/p16p2_20261015/host'
    indices = sum([ref['science']['host_checks'][k]['native_bands_1based'] for k in ['Gamma6','Gamma8']], [])
    with h5py.File(host/'out/r07pbe.save/wfc1.hdf5') as h:
        sourceG = np.asarray(h['MillerIndices'])
        C = np.array([np.asarray(h['evc'][i-1]).view(np.complex128) for i in indices]).T
    np.testing.assert_array_equal(sourceG,G)
    assert C.tobytes() == P.tobytes(), 'original accepted physical frame changed'
    S = P.conj().T@P
    lookup = {tuple(g):i for i,g in enumerate(G)}
    minus = np.array([lookup[tuple(-g)] for g in G])
    thetaP = np.r_[P[N+minus].conj(), -P[minus].conj()]
    np.testing.assert_array_equal(thetaP,frame['ThetaP'])
    outside = thetaP-P@np.linalg.solve(S,P.conj().T@thetaP)
    singular = np.linalg.svd(outside,compute_uv=False)
    records = {}; reference_coords = None
    sourcepins = {str(framepath):sha(framepath),str(host/'out/r07pbe.save/wfc1.hdf5'):sha(host/'out/r07pbe.save/wfc1.hdf5')}
    for member in ['unshared','shared']:
        root = DFT/'.local/qe75_lowram_20261011/p16e_20261015'/member
        for rows in profile['copied_saves'][member].values():
            assert sha(rows['source']) == rows['sha256']
            sourcepins[rows['source']] = rows['sha256']
        inp = root/'pw.in'; sourcepins[str(inp)] = sha(inp)
        t = ET.parse(root/'out/r07pbe.save/data-file-schema.xml')
        assert t.findtext('.//input/dft/functional') == 'PBE'
        assert 2*float(t.findtext('.//input/basis/ecutwfc')) == 50
        assert 2*float(t.findtext('.//input/basis/ecutrho')) == 200
        assert t.findtext('.//input/spin/noncolin') == 'true'
        assert t.findtext('.//input/spin/spinorbit') == 'true'
        assert t.findtext('.//output/magnetization/do_magnetization') == 'false'
        assert not np.any(np.fromstring(t.findtext('.//output/magnetization/total_vec'),sep=' '))
        A,names,coords,ops = geometry(t)
        assert len(ops) == {'unshared':24,'shared':4}[member]
        assert Counter(names) == {'Hg':6,'Cd':2,'Te':8}
        cd_indices = [i for i,s in enumerate(names) if s=='Cd']
        assert cd_indices == {'unshared':[0,7],'shared':[0,1]}[member]
        if records:
            np.testing.assert_array_equal(A, np.array(records['unshared']['cell_Bohr']))
            np.testing.assert_array_equal(coords,reference_coords)
        else:reference_coords = coords.copy()
        neighbor_counts = []
        shifts = np.array(list(product([-1,0,1],repeat=3)))
        for i,name in enumerate(names):
            if name != 'Te':continue
            candidates = sorted((float(np.linalg.norm((coords[j]+s-coords[i])@A)),j)
                for j in range(8) for s in shifts)
            assert candidates[3][0]-candidates[0][0]<1e-10
            assert candidates[4][0]-candidates[3][0]>1e-3
            neighbor_counts.append(sum(names[j]=='Cd' for _,j in candidates[:4]))
        histogram = [neighbor_counts.count(i) for i in range(5)]
        assert histogram == {'unshared':[0,8,0,0,0],'shared':[2,4,2,0,0]}[member]
        band = t.find('.//output/band_structure')
        ks = band.findall('ks_energies'); assert len(ks) == 1
        E = np.fromstring(ks[0].findtext('eigenvalues'),sep=' ')*2
        w = np.fromstring(ks[0].findtext('occupations'),sep=' ')
        ef = float(band.findtext('fermi_energy'))*2
        assert len(E) == 352 and abs(sum(expit((ef-E)/.001))-288)<1e-8
        assert t.findtext('.//output/convergence_info/scf_conv/convergence_achieved') == 'true'
        with h5py.File(root/'out/r07pbe.save/charge-density.hdf5') as h:
            assert set(h.keys()) == {'MillerIndices','rhotot_g'}
            dg = np.asarray(h['MillerIndices'])
            rho = np.asarray(h['rhotot_g']).view(np.complex128).reshape(-1)
        dlookup = {tuple(g):i for i,g in enumerate(dg)}
        densitysym = []
        for R,ft in ops:
            # Fractional real-space operation x'=R*x+t; reciprocal G'=R^-T G.
            invR = np.rint(np.linalg.inv(R)).astype(int)
            moved = dg@invR
            order = np.array([dlookup[tuple(g)] for g in moved])
            predicted = np.exp(-2j*np.pi*(moved@ft))*rho
            densitysym.append(float(np.linalg.norm(rho[order]-predicted)/np.linalg.norm(rho)))
        zero = np.flatnonzero(np.all(dg==0,axis=1)); assert len(zero)==1
        omega = abs(np.linalg.det(A))
        membersaves = sum(Path(p).stat().st_size for p in sourcepins if str(root/'out/r07pbe.save') in p)
        sock = str(FUTURE/'jobs'/member/'s')
        assert len(sock.encode()) <= 107
        records[member] = dict(cell_Bohr=A.tolist(),species_counts=dict(Counter(names)),
            Cd_indices=cd_indices,Te_nearest4_Cd_counts=neighbor_counts,
            Te_environment_histogram=histogram,
            actual_point_operation_count=len(ops),saved_charge_e=float(omega*rho[zero[0]].real),
            saved_density_group_covariance_relative=densitysym,
            saved_local_model='nonmagnetic PBE+SOC; domag=false, scalar rhoG only',
            full_nonlocal_density_Theta_or_eigenpair_NOT_certified=True,
            FD_charge_error_e=float(sum(expit((ef-E)/.001))-288),
            FD_occupation_max_error=float(max(abs(w-expit((ef-E)/.001)))),
            scf_error_Ry=2*float(t.findtext('.//output/convergence_info/scf_conv/scf_error')),
            saved_eigenpair_full_H_residual_certified=False,own_EF_Ry=ef,
            saved_files_logical_B=membersaves,socket_bytes=len(sock.encode()),future_root_created=False)
    # Only dimensions of the UNQUALIFIED packet, never its H matrix/action.
    extents = {}
    source_arrays = []
    for rank in [0,1]:
        with (PRIVATE/'jobs/unshared/pilot'/f'H.rank{rank}').open('rb') as h:
            head = np.fromfile(h,'<i8',16)
            fft = np.fromfile(h,'<i8',28).reshape(14,2,order='F')
        p,n,ng,nr,ns = map(int,head[[4,5,6,7,8]])
        assert head[0] == 70251521 and head[13] == 12
        # Exact current driver record and selected explicitly allocated payloads.
        packet = 128+224+72+24+48+24*(n+ng)+5*16*(2*p*12)+64*ng+32*(nr+ns)
        pfile = PRIVATE/'jobs/unshared/pilot'/f'H.rank{rank}'
        assert packet == pfile.stat().st_size
        local_queries = 5*16*2*p*12
        evc = 16*2*p*352
        ref = 16*2*N*12+24*N
        lo,hi = G.min(axis=0),G.max(axis=0)
        table = 4*int(np.prod(hi-lo+1))
        source_arrays.append(evc+local_queries+ref+table)
        extents[str(rank)] = dict(npwx=p,active_pw=n,ngm=ng,nrho=nr,nsmooth=ns,
            fft=fft.tolist(),packet_exact_B=packet,driver_arrays_selected_upper_B=local_queries+ref+table,
            persistent_evc_B=evc,initialization_wave_buffer_additional_possible_B=evc,
            packet_source='UNQUALIFIED old packet DIMENSIONS ONLY')
    source = (OLD/'native_probe.inc').read_text()
    assert 'xclib_dft_is(\'hybrid\')' in source and 'CALL h_psi(npwx,n,12,P,full)' in source
    run = (Path(build['binary']).parent/'run_pwscf.f90').read_text()
    assert run.index('CALL r07_static_H()') < run.index('RETURN ! read-only saved-charge operator')
    assert str(FUTURE).startswith(str(PRIVATE/'jobs')+'/') and not FUTURE.exists()
    out = dict(status='READ_ONLY_INPUT_AND_SELECTED_BOUND_AUDIT; NO_NATIVE_ADMISSION',
        old_refusal_preserved=True,old_rank_exits_false_NOT_teardown_proof=True,
        old_profile_pins_checked=len(profile['pins']),old_refused_raw_pins_checked=len(raw),
        source_ELF_PP_saved_inputs_pass=True,source_pins=sourcepins,
        source_ELF_sha256=build['binary_sha256'],stock_sha256=sha(DFT/'.local/qe-env/bin/pw.x'),
        original_frame_bitwise_from_accepted_host=True,frame_Gram_op=float(np.linalg.norm(S-np.eye(6),2)),
        original_Theta_outside_F=float(np.linalg.norm(outside,'fro')),
        original_Theta_outside_singulars=singular.tolist(),extra_Theta_rank_above1e8=int(sum(singular>1e-8)),
        physical_actions_total=12,Theta_control_actions_total=12,minimum_static_actions_total=24,
        members=records,rank_source_extents=extents,
        selected_payload_two_rank_B=sum(source_arrays),
        native_packet_payload_two_members_exact_B=2*sum(x['packet_exact_B'] for x in extents.values()),
        packet_bound_is_conditional_on_same_layout=True,
        resource_unknowns=['complete PW initialization/FFT/beta/radial arrays and temporaries',
            'FFT/HDF5/MPI/allocator/backend RSS and log/tmp producers',
            'new live owner/receipt/FD/terminal integration'],
        complete_12GiB_RAM_or_600s_bound_certified=False,
        complete_14GiB_output_source_envelope_certified=False,
        old_measured_kernel_peak_B=failure['peak_kernel_memory_B'],
        old_observation_is_NOT_bound=True,
        future_private_base=str(FUTURE),native_runs=0,DFT_writes=0,physical_xc=None)
    (HERE/'input_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','old_profile_pins_checked','original_Theta_outside_F',
        'extra_Theta_rank_above1e8','minimum_static_actions_total','native_packet_payload_two_members_exact_B']},indent=2))


if __name__ == '__main__':
    main()
