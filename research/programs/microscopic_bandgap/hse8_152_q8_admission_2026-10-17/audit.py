"""One bounded source/archive assessment. No native execution, build or service.

Exact rational grids implement QE7.5 kpoint_grid/exx_qgrid_init set operations.
Output is limited to this new MCT directory. Protected DFT is only read.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools as it
import json
import subprocess
import xml.etree.ElementTree as ET

import numpy as np

P = Path(__file__).resolve().parent
B = P.parent
REPO = B.parents[2]
DFT = Path('/home/User/opencode_workspace/DFT')
QE = DFT/'.local/qe75_lowram_20261011/q-e'
ARCHIVE = DFT/'.local/qe75_lowram_20261011/h8r_20261015/build1/source'
RY = 13.605693122994


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def wrap(k):
    return tuple(v % 1 for v in k)


OPS = [(perm, signs) for perm in it.permutations(range(3))
       for signs in it.product([-1, 1], repeat=3) if np.prod(signs) == 1]


def action(k, op, tr=1):
    perm, signs = op
    return wrap(tuple(tr*signs[j]*k[perm[j]] for j in range(3)))


def regular(n, shift=0):
    return {tuple(F(i, n)+F(shift, 2*n) for i in k)
            for k in it.product(range(n), repeat=3)}


def irreducible(points, ops=OPS):
    """Same first-consecutive-index representative as kpoint_grid.f90.

    With exact Td+TR stars, direct orbit removal independently replaces its
    equiv/weight loop. All fractions are modulo reciprocal integers.
    """
    left = set(points)
    result = []
    for k in sorted(points):
        if k in left:
            orbit = {action(k, op, tr) for op in ops for tr in [-1, 1]} & points
            result.append((k, len(orbit)))
            left -= orbit
    assert not left
    return result


def exx_sources(reps, points, q):
    shifts = regular(q)
    # Mirrors the distinct list indexed by new_ikq in exx_qgrid_init.
    sources = {wrap(tuple(k[j]+v[j] for j in range(3))) for k, _ in reps for v in shifts}
    return sources, sources <= points


def total_variation(points, target):
    return sum(abs(F(int(k in points), len(points))-F(int(k in target), len(target)))
               for k in points | target)/2


def floats(points):
    return [[float(x) for x in p] for p in sorted(points)]


def geometry_group(species, sites):
    return [op for op in OPS if all(sorted(action(site, op) for site, sp in zip(sites, species) if sp == name)
                                   == sorted(site for site, sp in zip(sites, species) if sp == name)
                                   for name in set(species))]


def main():
    checks = []
    source_pins = {}
    source_files = ['PW/src/exx_base.f90', 'PW/src/exx.f90', 'PW/src/exx_band.f90',
                    'PW/src/kpoint_grid.f90', 'PW/src/setup.f90', 'PW/src/input.f90',
                    'PW/src/allocate_wfc.f90', 'PW/src/wfcinit.f90', 'PW/src/c_bands.f90',
                    'PW/src/h_psi.f90', 'PW/src/buffers.f90', 'Modules/mp_exx.f90',
                    'Modules/wavefunctions.f90', 'Modules/input_parameters.f90', 'Modules/read_namelists.f90',
                    'KS_Solvers/Davidson/cegterg.f90',
                    'PW/Doc/INPUT_PW.def']
    for name in source_files:
        data = subprocess.check_output(['git', '--no-optional-locks', '-C', str(QE),
                                        'show', 'qe-7.5:'+name])
        item = dict(tag='qe-7.5', sha256=hashlib.sha256(data).hexdigest(),
                    lines=len(data.splitlines()),
                    primary_URL='https://github.com/QEF/q-e/blob/qe-7.5/'+name,
                    working_file_matches_tag=(QE/name).read_bytes() == data)
        if name == 'PW/src/exx.f90':
            assert (ARCHIVE/'pristine_exx.f90').read_bytes() == data
            item['trusted_archive'] = str(ARCHIVE/'pristine_exx.f90')
        source_pins[name] = item
    checks.append('archived pristine EXX is byte-identical to local qe-7.5 tag')

    # Enumerate the exact physical primitive4^3 -> conventional folding.
    t = np.array([[-1, 1, 1], [1, -1, 1], [1, 1, -1]])
    folded = {}
    for n in it.product(range(4), repeat=3):
        key = tuple(F(int(v) % 4, 4) for v in np.array(n)@t)
        folded[key] = folded.get(key, 0)+1
    target = set(folded)
    assert len(target) == 16 and set(folded.values()) == {4}
    assert target == regular(2) | regular(2, 1)
    checks.append('folded16 equals unshifted2^3 plus all-axis half-shifted2^3')
    grids = []
    for n, sh, q in [(2,0,2), (2,1,2), (3,0,2), (4,0,2), (4,1,2), (4,0,4)]:
        points = regular(n, sh)
        reps = irreducible(points)
        requested_sources, requested_compatible = exx_sources(reps, points, q)
        # exx_grid_init forces q1 when nkstot==nspin_lsda==1, including
        # the ONE-IRREP shifted k2 grid (not just a Gamma-only input).
        effective_q = 1 if len(reps) == 1 else q
        sources, compatible = exx_sources(reps, points, effective_q)
        if not compatible:
            # First exact source fallback for these equal-axis q2 cases is1.
            assert q == 2
            effective_q = 1
            sources, compatible = exx_sources(reps, points, effective_q)
        assert compatible
        grids.append(dict(electronic_grid=[n]*3, offset_flags=[sh]*3, requested_q=[q]*3,
                          effective_q=[effective_q]*3,
                          electronic_full_count=len(points), irreducible_count=len(reps),
                          representatives=[dict(k=[float(x) for x in k], multiplicity=w) for k,w in reps],
                          requested_transfer_count=q**3, effective_transfer_count=effective_q**3,
                          source_union_count=len(sources),
                          requested_translations_supported=requested_compatible,
                          effective_translations_supported=compatible,
                          Gamma_included=(F(0),)*3 in points,
                          full_Gamma_weight=1/len(points) if (F(0),)*3 in points else 0,
                          intersect_folded_target=len(points & target),
                          electronic_rule_TV_from_folded16=float(total_variation(points, target)),
                          nominal_source_buffer_B=60**3*2*152*len(sources)*16 if compatible else None,
                          source_points=floats(sources)))
    assert grids[0]['irreducible_count'] == 4 and grids[0]['source_union_count'] == 8
    assert grids[3]['irreducible_count'] == 10 and grids[3]['source_union_count'] == 56
    assert not grids[2]['requested_translations_supported'] and grids[2]['effective_q'] == [1]*3
    assert grids[1]['source_union_count'] == 1 and grids[1]['effective_q'] == [1]*3
    checks.append('k4/q2 union56; shifted single-irrep k2 forcesq1; incompatible k3/q2 falls backq1')
    freps = irreducible(target)
    fsrc, ok = exx_sources(freps, target, 2)
    assert len(freps) == 5 and ok and len(fsrc) == 16
    # Independent source-count check: q2 translations form 8-point cosets.
    for rec in grids:
        if rec['effective_q'][0] == 2:
            representatives = [tuple(F(str(v)) for v in z['k']) for z in rec['representatives']]
            cosets = {tuple((2*x) % 1 for x in k) for k in representatives}
            assert len(cosets)*8 == rec['source_union_count']
    checks.append('independent q2-coset count reproduces all compatible source unions')
    d2 = [op for op in OPS if op[0] == (0,1,2)]
    lower = irreducible(regular(4), d2)
    lower_src, lower_ok = exx_sources(lower, regular(4), 2)
    assert len(lower) == 27 and lower_ok and len(lower_src) == 64

    sites = [(F(0),F(0),F(0)),(F(0),F(1,2),F(1,2)),
             (F(1,2),F(0),F(1,2)),(F(1,2),F(1,2),F(0)),
             (F(1,4),F(1,4),F(1,4)),(F(1,4),F(3,4),F(3,4)),
             (F(3,4),F(1,4),F(3,4)),(F(3,4),F(3,4),F(1,4))]
    host_species = ['Hg']*4+['Te']*4
    cd_species = ['Cd']+['Hg']*3+['Te']*4
    assert len(geometry_group(host_species, sites)) == len(geometry_group(cd_species, sites)) == 24
    translations = sites[:4]
    pure_trans = []
    cd_trans = []
    for shift in translations:
        def preserves(species):
            return all(sorted(wrap(tuple(site[j]+shift[j] for j in range(3)))
                              for site, sp in zip(sites,species) if sp==name)
                       == sorted(site for site,sp in zip(sites,species) if sp==name)
                       for name in set(species))
        if preserves(host_species): pure_trans.append(shift)
        if preserves(cd_species): cd_trans.append(shift)
    assert len(pure_trans)==4 and len(cd_trans)==1
    checks.append('Cd-at-origin retains all24 Td operations but only1 of4 fcc translations')

    archives = B/'chemical_hse_relax_2026-10-15'
    retained = {}
    raw_pins = {}
    for member in ['host', 'cd']:
        path = archives/f'{member}_native_result.json'
        report = json.loads(path.read_text());raw_pins[str(path)] = sha(path)
        e = np.array(report['eigenvalues_Ry'][0]); f = np.array(report['occupations'][0]);mu=report['fermi_Ry']
        xml_path = next(Path(x) for x in report['source_hashes'] if x.endswith('data-file-schema.xml'))
        assert sha(xml_path) == report['source_hashes'][str(xml_path)]
        raw_pins[str(xml_path)] = sha(xml_path)
        xt = ET.parse(xml_path)
        actual = xt.findall('output/atomic_structure/atomic_positions/atom')
        assert [v.attrib['name'] for v in actual] == (host_species if member=='host' else cd_species)
        assert xt.findtext('output/symmetries/nsym') == '24'
        h = dict(nonstationary=True, HSE_converged=report['HSE_converged'],
                 native_nsym=report['native_nsym'], band152_minus_mu_eV=float((e[151]-mu)*RY),
                 dropped_153_176_occupation=float(sum(f[152:])),
                 band152_occupation=float(f[151]),
                 atomic_starting_columns=int(xt.find('output/atomic_structure').attrib['num_of_atomic_wfc']))
        assert not h['HSE_converged']
        retained[member] = h
    p = B/'stock_hse_stationary_2026-10-16/host_projected_state.npz'
    with np.load(p) as z:
        retained['rejected_stock79build_host'] = dict(
            projection_probability_in_bands153_176=np.sum(abs(z['overlap'][:,152:])**2, axis=1).tolist(),
            occupation_in_bands153_176=float(sum(z['occupations'][152:])),
            native_band152_minus_mu_eV=None,
            NOT_a_bound_for_new_152_k2_q2_state=True)
    raw_pins[str(p)] = sha(p)

    frozen = json.loads((archives/'frozen_protocol.json').read_text())
    pp = {}
    for species in ['Hg','Cd','Te']:
        path = next(Path(v) for v in frozen['profile']['pins'] if v.endswith(f'{species}_sg15_pbe_fr_v12.UPF'))
        assert sha(path) == frozen['profile']['pins'][str(path)]
        header = ET.parse(path).find('PP_HEADER')
        pp[species] = dict(path=str(path), sha256=sha(path), **header.attrib)
        assert header.attrib['pseudo_type']=='NC' and header.attrib['has_so']=='T'
        assert header.attrib['relativistic']=='full'
        raw_pins[str(path)] = sha(path)
    nelec = sum(float(pp[sp]['z_valence']) for sp in host_species)
    assert nelec == sum(float(pp[sp]['z_valence']) for sp in cd_species) == 144
    checks.append('actual FR NC SG15 header valences give144 spinor electrons in both cells')

    # Phase-aware payloads, NOT a peak certificate. Two ranks, one pool,
    # one EXX band group, no GPU, default jblock7, measured old60^3 descriptor.
    m=152;n=60**3;ir=4;npw=10827;one=n*2*m*16;phi=npw*2*m*16
    ace_payload=dict(exxbuff_q8_B=one*8, two_spinor_FFT_batches_B=2*one,
        FFT_rhoc_vc_jblock7_B=2*n*7*16,
        xi_all4k_B=phi*ir, evc_B=phi, evc_exx_B=phi,
        direct_big_result_B=phi, wave_records_4k_B=phi*ir,
        rir_24ops_duplicated2ranks_B=n*24*4*2,
        coulomb_fac_grid_extent_ceiling_B=n*8*ir*8)
    subtotal=sum(ace_payload.values())
    memory=dict(band152_q8_nominal_B=one*8,hard_12GiB_B=12*2**30,
        persistent_plus_two_EXX_batches_B=10*one,
        nominal_known_ACE_phase_payload=ace_payload, nominal_known_ACE_phase_sum_B=subtotal,
        nominal_unassigned_headroom_B=12*2**30-subtotal,
        plane_wave_payload_uses_old_Gamma_count=npw,
        actual_new_npwx_FFT_padding_cache_and_library_peak_qualified=False,
        Davidson_NC_vectors_B=4*phi,
        Davidson_replicated_dense3matrices_B=3*(2*m)**2*16*2,
        Davidson_phase_excludes_direct_EXX_FFT_batches=True,
        exxinit_replicated_two_global_spinor_FFT_arrays_B=2*n*2*16*2,
        exxinit_global_temporaries_do_not_overlap_aceinit_batches=True,
        old_stock_q1_176_kernel_peak_B=4224897024,
        old_diagnostic_q1_176_peak_B=4548526080,
        overhead_cannot_be_subtracted_and_reused_as_upper=True,
        complete_peak_upper_B=None, credible_overall_peak='UNQUALIFIED; named payload is not all resident charge',
        execution_under_12GiB='NO-GO', deliberate_cgroup_OOM_probe_permitted=False)
    assert one*8 == 8404992000
    checks.append('q8/152 allocation8404992000B; simultaneous full EXX spinor batches add2101248000B')

    # Protection check: no source/root mutation, no science or runtime calls.
    historic = B/'static_environment_2026-10-15'
    pins=dict(json.loads((historic/'frozen_protocol.json').read_text())['profile']['pins'])
    pins.update({k:v['sha256'] for k,v in json.loads((historic/'evidence_manifest.json').read_text())['raw'].items()})
    build=json.loads((B/'pbe_density_driver_2026-10-16/source_build_evidence.json').read_text())
    for key in ['linked_archive_pins','compiler_object_pins','compiled_module_pins']: pins.update(build[key])
    protection=json.loads((historic/'protected_before.json').read_text());pins.update(protection['files'])
    assert len(pins)==822
    for path,h in pins.items(): assert sha(path)==h,path
    assert subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)==protection['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','-C',str(DFT),'diff','--binary'])).hexdigest()==protection['DFT_tracked_diff_sha256']
    count=0
    for folder in ['pbe_density_driver_2026-10-16','pbe_static_lifecycle_2026-10-16',
                   'pbe_static_completion_2026-10-16','pbe_density_only_feasibility_2026-10-16']:
        for name in subprocess.check_output(['git','ls-tree','-r','--name-only','3053279',str((B/folder).relative_to(REPO))],text=True).splitlines():
            assert (REPO/name).read_bytes()==subprocess.check_output(['git','show','3053279:'+name]);count+=1
    assert count==76
    assert subprocess.check_output(['git','diff','3053279','--',str((B/'primitive_k4_hse_2026-10-17').relative_to(REPO)),
                                    str((B/'stock_hse_stationary_2026-10-16').relative_to(REPO))],text=True)==''
    checks.append('822protected pins/76historical files, dirtyDFT and previous host acceptances/refusals unchanged')
    for path,h in raw_pins.items():assert sha(path)==h

    result=dict(baseline='305327988ae72196c07eaf32856809c65136a820',
        verdict='NO-GO for execution under12GiB; stock/model compatibility conditional YES',
        native_jobs=0, builds=0, services=0, source_edits=0,
        stock_ELF=str(DFT/'.local/qe-env/bin/pw.x'),
        stock_ELF_sha256=sha(DFT/'.local/qe-env/bin/pw.x'), stock_ELF_executed=False,
        exact_source_tag_commit=subprocess.check_output(['git','-C',str(QE),'rev-parse','qe-7.5^{}'],text=True).strip(),
        source_pins=source_pins, raw_pins=raw_pins, PP=pp,
        grid_models=grids,
        folded16=dict(points=floats(target), irreducible_count=len(freps), q2_source_count=len(fsrc),
                      q2_includes_only_same_coset_not_full16_transfer_rule=True,
                      nominal152_source_buffer_B=one*len(fsrc)),
        lower_D2_TR_k4_q2=dict(irreducible_count=len(lower), source_count=len(lower_src)),
        chemical_geometry=dict(host_Td_operations=24,Cd_at_origin_Td_operations=24,
                               host_primitive_translations_in_conventional_cell=4,Cd_translations=1,
                               generic_lower_point_symmetry_assumption_false_for_frozen_motif=True),
        spinor_bands=dict(electrons=nelec,proposed=152,extra_over_electron_count=8,
                         stock_default_from_setup=172,old_explicit=176,
                         ACE_projection_equals_nbnd_in_normal_SCF=True,
                         random_atomic_perturbation_branch_changes_when_nbnd_equals_natomwfc=True,
                         FD_operator_tail_1e8_requires_energy_margin_eV=float(.001*RY*np.log(1e8-1)),
                         FD_24state_charge_tail_1e8_requires_margin_eV=float(.001*RY*np.log(24e8-1))),
        retained_nonstationary_data=retained,memory=memory,checks=checks,
        protected_pins_unchanged=822,historical_files_unchanged=count,
        best_unadmitted_candidate=dict(electron_mesh=[2,2,2],offset=[0,0,0],q_mesh=[2,2,2],nbnd=152,
            new_model_relative_to_primitive4=True,equivalent_to_primitive4=False,
            execution_admitted=False,scientific_response_error_meV_certified=None),
        physical_xc=None)
    (P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(verdict=result['verdict'],grid_summary=[{k:g[k] for k in
        ['electronic_grid','offset_flags','effective_q','irreducible_count','source_union_count','requested_translations_supported','electronic_rule_TV_from_folded16']} for g in grids],
        known_payload_B=subtotal,unassigned_headroom_B=memory['nominal_unassigned_headroom_B'],
        checks=checks),indent=2))


if __name__ == '__main__':
    main()
