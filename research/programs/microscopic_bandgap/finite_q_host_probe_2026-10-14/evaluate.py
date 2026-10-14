"""ONE read-only native host wavepacket spectral contraction. No QE/MPI.

This defined cell-periodic probe is NOT a cross-k physical eigenstate overlap,
atomic substitution vertex, scattering self-energy or alloy Gamma gap.
"""
import datetime
from decimal import Decimal, localcontext
import hashlib
import json
from math import comb
import os
from pathlib import Path
import resource
import signal
import sys
import time
import xml.etree.ElementTree as ET

import h5py
import numpy as np

HERE = Path(__file__).resolve().parent
DFT = Path('/home/User/opencode_workspace/DFT')
sys.path.insert(0, str(DFT/'src'))
from mct_dft.qe_wavefunctions import read_spinors
from mct_dft.constants import RY_TO_EV


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical(miller, k):
    # Native reciprocal relabeling k->k+s, G->G-s cancels exactly here.
    shift = np.floor(np.asarray(k)+.5+1e-12).astype(int)
    return miller+shift, np.asarray(k)-shift


def periodic_contraction(P, gp, C, g):
    lookup = {tuple(v):i for i,v in enumerate(gp)}
    if len(lookup) != len(gp) or len({tuple(v) for v in g}) != len(g):
        raise ValueError('duplicate Fourier vector')
    src, dest = [], []
    for j, v in enumerate(g):
        i = lookup.get(tuple(v))
        if i is not None:
            src.append(i)
            dest.append(j)
    a = P[:, :, src].reshape(len(P), -1)
    b = C[:, :, dest].reshape(len(C), -1)
    return a.conj()@b.T, a.conj()@a.T


PI = Decimal('3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647')


def atan(x):
    if x < 0:
        return -atan(-x)
    if x > 1:
        return PI/2-atan(1/x)
    if x > Decimal('.5'):
        return PI/4+atan((x-1)/(x+1))
    total, term = x, x
    for j in range(1, 160):
        term *= -x*x
        add = term/(2*j+1)
        total += add
        if abs(add) < Decimal('1e-75'):
            return total
    raise ValueError('bounded Decimal atan series exhausted')


def decimal_integrals(delta, W, eta):
    """Exact polynomial/Cauchy antiderivative, evaluated with 70-digit arithmetic."""
    with localcontext() as ctx:
        ctx.prec = 70
        d, w, h = [Decimal.from_float(float(v)) for v in (delta,W,eta)]
        a, b = -w-d, w-d
        ints = [(atan(b/h)-atan(a/h))/h,
                ((b*b+h*h)/(a*a+h*h)).ln()/2]
        for n in range(2, 6):
            ints.append((b**(n-1)-a**(n-1))/(n-1)-h*h*ints[n-2])
        js = [h/PI*sum(comb(n,j)*(Decimal(1) if n==j else d**(n-j))*ints[j] for j in range(n+1)) for n in range(6)]
        mass = js[0]-2*js[2]/w**2+js[4]/w**4
        moment = js[1]-2*js[3]/w**2+js[5]/w**4
        return float(mass), float(moment)


def quadrature(deltas, W, eta, order=1024):
    # Independent positive-node integration; compared with the antiderivative.
    nodes, weights = np.polynomial.legendre.leggauss(order)
    t, a = W*nodes, W*weights*(1-nodes**2)**2
    masses, moments = [], []
    for start in range(0, len(deltas), 128):
        delta = deltas[start:start+128]
        lor = eta/np.pi/((t[None,:]-delta[:,None])**2+eta**2)
        masses.extend(lor@a)
        moments.extend(lor@(a*t))
    return np.array(masses), np.array(moments)


def evaluate():
    started = time.monotonic()
    prereg = json.loads((HERE/'preregistration.json').read_text())
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('60-s scientific-analysis cap')))
    signal.alarm(60)
    resource.setrlimit(resource.RLIMIT_AS, (512 << 20, 512 << 20))
    source = Path(prereg['source'])
    saved = source/'out/r07_open.save'
    result = json.loads((source/'result.json').read_text())
    if not all(result[k] for k in ['accepted_scf','exx_converged','job_done','all_native_processes_terminated']):
        raise ValueError('accepted parent native SCF required')
    for species, digest in prereg['PP_sha256'].items():
        if sha(DFT/'pseudopotentials'/(species+'_sg15_pbe_fr_v12.UPF')) != digest:
            raise ValueError('PP source pin')
    assignment = json.loads((source/'gamma/signed_gap.json').read_text())
    irrep_file = HERE.parent/'native_matched_pilot_2026-10-11/reference_irrep_check.json'
    irreps = json.loads(irrep_file.read_text())
    for name in ['Gamma6','Gamma8']:
        if not irreps['sectors'][name]['nearest_integer_classification_admitted_under_model']:
            raise ValueError('previous physical-frame classification fails')
    for p, digest in irreps['source_sha256'].items():
        if sha(p) != digest:
            raise ValueError('physical reference frame changed')
    schema = saved/'data-file-schema.xml'
    tree = ET.parse(schema).getroot()
    for e in tree.iter():
        e.tag = e.tag.split('}')[-1]
    alat_bohr = float(tree.find('.//output/atomic_structure').attrib['alat'])
    tpiba = 2*np.pi/alat_bohr
    schema_bg = np.array([np.fromstring(tree.findtext('.//output/basis_set/reciprocal_lattice/b'+str(j)),sep=' ') for j in (1,2,3)])
    ks = tree.findall('.//ks_energies')
    if len(ks) != 64:
        raise ValueError('fixed full-grid64 scope')
    energies = np.array([np.fromstring(v.findtext('eigenvalues'),sep=' ')*2*RY_TO_EV for v in ks])
    weights = np.array([float(v.find('k_point').attrib['weight']) for v in ks])
    if energies.shape != (64,44) or np.max(abs(weights-1/64))>1e-14:
        raise ValueError('actual full-grid/native spectral prefix')
    if np.min(np.diff(energies,axis=1)) < -1e-8:
        raise ValueError('unordered spectral prefix')
    gamma = [i for i,v in enumerate(ks) if np.linalg.norm(np.fromstring(v.findtext('k_point'),sep=' '))<1e-9]
    if len(gamma) != 1:
        raise ValueError('unique Gamma')
    gidx = gamma[0]
    Cg, gp, kg = read_spinors(saved/f'wfc{gidx+1}.hdf5')
    P = Cg[32:38]
    if np.linalg.norm(P.reshape(6,-1).conj()@P.reshape(6,-1).T-np.eye(6),2)>1e-10:
        raise ValueError('fixed NC physical frame metric')
    E6, E8 = energies[gidx,32:34].mean(), energies[gidx,34:38].mean()
    if abs(E6-E8-assignment['E_Gamma6_minus_Gamma8_eV'])>1e-8:
        raise ValueError('native energy/irrep assignment mismatch')
    r, W, eta = (E6+E8)/2, prereg['W_eV'], prereg['eta_eV']
    hashes = {str(p):sha(p) for p in [source/'result.json',source/'pw.in',source/'pw.out',schema,
        source/'gamma/signed_gap.json',irrep_file,DFT/'src/mct_dft/qe_wavefunctions.py',HERE/'preregistration.json']}
    rows, sector_weights, geom, omitted = [], [], [], []
    band_gram_max = 0
    for i in range(64):
        path = saved/f'wfc{i+1}.hdf5'
        C, g, k = read_spinors(path)
        hashes[str(path)] = sha(path)
        with h5py.File(path) as h:
            if int(h.attrs['ik']) != i+1:
                raise ValueError('wave/native k index')
            basis = np.array([h['MillerIndices'].attrs['bg'+str(j)] for j in (1,2,3)])
            if np.max(abs(basis/tpiba-schema_bg))>1e-12:
                raise ValueError('actual reciprocal basis/cell units')
            if np.max(abs(k@basis/tpiba-np.fromstring(ks[i].findtext('k_point'),sep=' ')))>1e-12:
                raise ValueError('actual wave/eigen k correspondence')
        flat = C.reshape(44,-1)
        defect = np.linalg.norm(flat.conj()@flat.T-np.eye(44),2)
        band_gram_max = max(band_gram_max,float(defect))
        if defect>1e-8:
            raise ValueError('native44-band NC Gram')
        gcan, kcan = canonical(g,k)
        A, coverage = periodic_contraction(P,gp,C,gcan)
        missing = coverage-A@A.conj().T
        if np.linalg.eigvalsh(missing).min() < -1e-9:
            raise ValueError('spectral probability closure fails')
        sw = np.array([np.sum(abs(A[:2])**2,axis=0)/2,np.sum(abs(A[2:])**2,axis=0)/4])
        cover = np.array([np.trace(coverage[:2,:2]).real/2,np.trace(coverage[2:,2:]).real/4])
        geo, tail = 1-cover, cover-sw.sum(axis=1)
        if np.min(np.r_[geo,tail]) < -1e-9:
            raise ValueError('negative omitted mass')
        sector_weights.append(sw)
        geom.append(geo)
        omitted.append(tail)
        rows.append(dict(k_index=i+1,k_fractional_canonical=kcan.tolist(),prefix_mass=sw.sum(axis=1).tolist(),
            plane_space_loss=geo.tolist(),omitted_band_weight=tail.tolist(),Gram_2norm=float(defect)))
    sw, geom, omitted = map(np.array,(sector_weights,geom,omitted))
    delta = (energies-r).ravel()
    exact = np.array([decimal_integrals(v,W,eta) for v in delta])
    masses, moments = exact[:,0].reshape(64,44), exact[:,1].reshape(64,44)
    independent_m, independent_n = quadrature(delta,W,eta)
    merr = float(np.max(abs(independent_m-exact[:,0])))
    nerr = float(np.max(abs(independent_n-exact[:,1])))
    if merr>1e-9 or nerr>1e-9 or min(masses.ravel()) < 0:
        raise ValueError('independent spectral quadrature/positivity')
    distance = energies[:,-1]-r-W
    if np.min(distance)<=0:
        raise ValueError('uncomputed spectral prefix enters fixed probe window')
    source_geometry_weight = np.sum(weights[:,None]*np.maximum(geom,0),axis=0)
    spectral_tail_weight = np.sum(weights[:,None]*np.maximum(omitted,0),axis=0)
    # Known prefix is not renormalized. An arbitrary plane-space completion is
    # bounded by loss; uncomputed finite-basis bands lie above the last energy.
    tau_per_k = np.maximum(geom,0)+np.maximum(omitted,0)*eta/np.pi/distance[:,None]**2*(16*W/15)
    tau = np.sum(weights[:,None]*tau_per_k,axis=0)+1e-9
    sectors = {}
    for j,name in enumerate(['Gamma6_reference_probe','Gamma8_reference_probe']):
        m = float(np.sum(weights[:,None]*sw[:,j,:]*masses))
        n = float(np.sum(weights[:,None]*sw[:,j,:]*moments))
        if m<=0:
            raise ValueError('no retained window mass')
        c = n/m
        error = (W+abs(c))*tau[j]/m+2e-9/m
        raw_window = abs(energies-r)<=W
        near = float(np.sum(weights[:,None]*sw[:,j,:]*raw_window))
        non_gamma = float(np.sum(weights[np.arange(64)!=gidx,None]*sw[np.arange(64)!=gidx,j,:]*raw_window[np.arange(64)!=gidx]))
        sectors[name] = dict(retained_probability=float(np.sum(weights[:,None]*sw[:,j,:])),
            arbitrary_plane_space_unresolved_probability=float(source_geometry_weight[j]),
            uncomputed_band_probability=float(spectral_tail_weight[j]),window_mass_lower=m,
            relative_window_moment_eV=n,relative_centroid_eV=c,raw_near_window_probability=near,
            raw_nonGamma_near_window_probability=non_gamma,conditional_added_window_mass_upper=float(tau[j]),
            conditional_centroid_tail_error_upper_eV=float(error),centroid_interval_relative_eV=[c-error,c+error])
    order = sectors['Gamma6_reference_probe']['relative_centroid_eV']-sectors['Gamma8_reference_probe']['relative_centroid_eV']
    order_error = sum(v['conditional_centroid_tail_error_upper_eV'] for v in sectors.values())
    np.savez_compressed(HERE/'retained_contractions.npz',energies_eV=energies,k_weights=weights,sector_band_weights=sw,
        plane_space_loss=geom,omitted_band_weight=omitted,window_masses=masses,relative_window_moments_eV=moments)
    signal.alarm(0)
    return dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),claim_status='CALCULATED specified coherent-host finite-grid wavepacket probe; conditional spectral completion only',
        parent_HSE_accepted=True,new_HSE_run=False,parent_QE_version=result['QE_version_line'],parent_MPI_ranks=result['mpi_ranks'],
        parent_DFT_commit=result['git_commit'],PP_sha256=prereg['PP_sha256'],native_Gamma_gap_eV=float(E6-E8),reference_r_native_eV=float(r),
        W_eV=W,eta_eV=eta,k_count=64,band_count=44,sectors=sectors,
        probe_centroid_difference_eV=float(order),conditional_difference_error_upper_eV=float(order_error),
        conditional_difference_interval_eV=[float(order-order_error),float(order+order_error)],
        physical_impurity_vertex_or_material_observable=False,physical_xc=None,
        unresolved_error_eV=dict(native_eigenpair=None,SCF_operator=None,finite_grid_to_continuum=None,material=None,probe_to_substitution=None),
        maximum_native_NC_Gram_2norm=band_gram_max,minimum_omitted_energy_distance_to_window_eV=float(distance.min()),
        independent_1024_node_quadrature_max_mass_error=merr,independent_quadrature_max_moment_error_eV=nerr,
        native_geometry_or_missing_weight_never_renormalized=True,source_hashes=hashes,per_k=rows,
        elapsed_seconds=time.monotonic()-started,peak_process_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        evaluator_sha256=sha(__file__),preregistration_sha256=sha(HERE/'preregistration.json'),no_new_MPI_QE=True)


if __name__ == '__main__':
    if (HERE/'numerical_result.json').exists() or (HERE/'attempt2_failure.json').exists():
        raise FileExistsError('one scientific attempt; do not overwrite evidence')
    try:
        value = evaluate()
    except BaseException:
        import traceback
        (HERE/'attempt2_failure.json').write_text(json.dumps(dict(error=traceback.format_exc(),no_new_MPI_QE=True),indent=2)+'\n')
        raise
    (HERE/'numerical_result.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:value[k] for k in ['native_Gamma_gap_eV','sectors','probe_centroid_difference_eV','conditional_difference_interval_eV','elapsed_seconds','peak_process_RSS_bytes']},indent=2))
