"""Retained-data antiunitary response audit; no native/build/DFT write.

An exact six-column reconstruction is refused when the reference is not closed.
Reported even/odd intervals then bound all Hermitian QQ completions under the
separately derived, source-conditioned finite-grid norm certificate.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import resource
import sys
import time
from xml.etree import ElementTree as ET
import numpy as np
from scipy.linalg import qr

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'screening_feasibility_2026-10-16'
sys.path.insert(0, str(PARENT))
import audit_retained as old

RY = old.RY_MEV
W = np.diag([.5, .5, -.25, -.25, -.25, -.25])
TOL = 1e-8  # inherited closure gate; never changed to accept this reference


def op(a): return float(np.linalg.norm(a, 2))
def hs(a): return float(np.linalg.norm(a))
def herm(a): return (a+a.conj().T)/2


def vrs(member, cycle, rank, stage):
    r = old.Packet(old.ROOT/member/'pilot'/f'c{cycle}_local{stage}.rank{rank}', rank, stage, cycle)
    h = r.take('<i8', (8,)); nr, ns, ng, nsg, nv = map(int, h[:5])
    assert ns == nsg == 4 and tuple(h[5:]) == (60, 60, 60)
    r.take('<i8', (3, ng)); r.matrix(6); r.matrix(6)
    rho = r.take('<f8', (nr, ns)); r.take('<c16', (ng, nsg))
    v = r.take('<f8', (nv, 4)).copy(); r.end()
    return v, float(np.max(abs(rho[:, 1:])))


def source_density(phi, f, theta):
    """Exact finite-rank reduction plus explicit span/Gram error estimates."""
    Tphi = theta(phi)
    Q, _, _ = qr(np.column_stack((phi, Tphi)), mode='economic', pivoting=True)
    A, B = Q.conj().T@phi, Q.conj().T@Tphi
    K = herm((A*f)@A.conj().T-(B*f)@B.conj().T)
    eig = np.linalg.eigvalsh(K)
    # Frobenius residual bounds also bound the operator residual; no tiny
    # subtraction of O(144) squared norms to resolve a 1e-7 density difference.
    sf = np.sqrt(f)
    U, V = phi*sf, Tphi*sf
    eU, eV = hs(U-Q@(Q.conj().T@U)), hs(V-Q@(Q.conj().T@V))
    gram = op(Q.conj().T@Q-np.eye(Q.shape[1]))
    b = np.sqrt(op(phi.conj().T@phi))*np.sqrt(max(f))
    fullop, fullF = float(max(abs(eig))), hs(K)
    # For a nonorthogonal numerical Q, its exact orthogonal projector is
    # Q (Qdagger Q)^-1 Qdagger. Bound that correction before controlling either
    # norm; a rank-independent operator allowance alone is not an HS allowance.
    projection_factor=(1+gram)*gram/(1-gram)
    span_error=2*b*(eU+eV+projection_factor*(hs(U)+hs(V)))
    op_allowance=span_error+gram/(1-gram)*fullop
    F_allowance=span_error+gram/(1-gram)*fullF
    # Independent actual scalar contraction at the extremal reduced eigenvector.
    _, vec = np.linalg.eigh(K); j = int(np.argmax(abs(eig))); u = Q@vec[:, j]; u /= np.linalg.norm(u)
    import math
    scalar = math.fsum(float(f[k])*(abs(np.vdot(phi[:, k],u))**2-abs(np.vdot(Tphi[:, k],u))**2) for k in range(len(f)))
    assert abs(abs(scalar)-fullop) < max(2e-12, 2*op_allowance)
    return dict(opnorm=fullop, Frobenius=fullF, rank_reduction_dimension=Q.shape[1],
                op_interval=[max(0.,fullop-op_allowance), fullop+op_allowance],
                Frobenius_interval=[max(0.,fullF-F_allowance), fullF+F_allowance],
                op_span_Gram_allowance=op_allowance, F_span_Gram_allowance=F_allowance,
                reduced_Gram_error=gram,
                independent_unit_vector_witness=scalar,
                exact_finite_rank_identity=True, directed_rounding_enclosure=False)


def setup(F, G):
    N = len(G); index = {tuple(g):i for i,g in enumerate(G)}
    minus = np.array([index[tuple(-g)] for g in G]); assert np.array_equal(minus[minus], np.arange(N))
    theta = lambda a: np.r_[a[N+minus].conj(), -a[minus].conj()]
    np.testing.assert_array_equal(theta(theta(F)), -F)
    S = herm(F.conj().T@F); w,v = np.linalg.eigh(S)
    inv = (v/np.sqrt(w))@v.conj().T; V = F@inv
    J = V.conj().T@theta(V); R = theta(V)-V@J
    q, _ = np.linalg.qr(R,mode='reduced'); small = herm((q.conj().T@R)@W@(R.conj().T@q))
    trace_coeff = float(sum(abs(np.linalg.eigvalsh(small)))/2)
    sectors = {}
    for name,sl in [('Gamma6',slice(0,2)),('Gamma8',slice(2,6))]:
        A=F[:,sl]; ew,ev=np.linalg.eigh(herm(A.conj().T@A)); A=A@((ev/np.sqrt(ew))@ev.conj().T)
        TA=theta(A); e=TA-A@(A.conj().T@TA)
        sectors[name]=dict(closure_singular_values=np.linalg.svd(e,compute_uv=False).tolist(),closure_op=op(e))
    info = dict(reference_Gram=op(S-np.eye(6)), normalized_Gram=op(V.conj().T@V-np.eye(6)),
                sector_closure=sectors, full_closure_singular_values=np.linalg.svd(R,compute_uv=False).tolist(),
                closure_op=op(R), exact_closure=False, inherited_1e_8_gate_pass=op(R)<=TOL,
                J_skew=op(J+J.T), J_square_defect=op(J@J.conj()+np.eye(6)),
                sector_Theta_overlap=op(V[:,:2].conj().T@theta(V[:,2:])),
                trace_QQ_ambiguity_coefficient_per_Ry=trace_coeff,
                action_QQ_ambiguity_coefficient=op(R)/2,
                original_frame_unchanged=True, normalization_is_bookkeeping=True)
    return theta,V,inv,R,info


def split(Y, F, theta, V, inv, R, M):
    """Known-column Hermitian completion centres, not a new material operator."""
    Yv=Y@inv; raw=V.conj().T@Yv; A=herm(raw); B=Yv-V@raw
    anchor=float(np.trace(A).real/6)
    H0=lambda x:V@(A@(V.conj().T@x))+B@(V.conj().T@x)+V@(B.conj().T@x)
    # Scalar-anchored QQ representative: shifts by cI when C shifts by cI.
    # Its difference from actual C is the unknown Q(C-anchor*I)Q, never set to
    # zero in physical claims; all reported intervals retain that ambiguity.
    H=lambda x:H0(x)+anchor*(x-V@(V.conj().T@x))
    Yh=H(V)
    tY=-theta(H(theta(V)))
    even=(Yh+tY)/2; odd=(Yh-tY)/2
    radius=M*op(R)*RY/2
    q,_=np.linalg.qr(R,mode='reduced'); small=herm((q.conj().T@R)@W@(R.conj().T@q))
    trace_radius=M*sum(abs(np.linalg.eigvalsh(small)))*RY/2
    out = dict(completion_bound_Ry=M, representative_scalar_anchor_Ry=anchor,
               Q_singular_radius_meV=radius,
               trace_ambiguity_radius_meV=float(trace_radius),
               original_trace_meV=old.observable(F.conj().T@Y),
               Hermitian_consistency_correction_action_meV=op(Yh-Yv)*RY,
               P_compression_Hermiticity_meV=op(raw-raw.conj().T)*RY,
               reconstruction_residual_meV=op(even+odd-Yh)*RY)
    for name,Z in [('even',even),('odd',odd)]:
        P=V.conj().T@Z; QZ=Z-V@P; sv=np.linalg.svd(QZ,compute_uv=False)*RY
        value=float(np.trace(W@P).real*RY)
        out[name]=dict(known_column_centre_trace_meV=value,
          trace_interval_meV=[value-trace_radius,value+trace_radius],
          Q_op_centre_meV=float(sv[0]), Q_op_interval_meV=[max(0.,sv[0]-radius),sv[0]+radius],
          Q_singular_centres_meV=sv.tolist(),
          Q_singular_intervals_meV=[[max(0.,float(s)-radius),float(s)+radius] for s in sv],
          compression_Hermiticity_meV=op(P-P.conj().T)*RY)
    # Probe parity of the explicitly declared mathematical completion on arbitrary
    # actual vectors, including ThetaV; no closure of P or C has been assumed.
    def T_H(x):return -theta(H(theta(x)))
    HE=lambda x:(H(x)+T_H(x))/2
    HO=lambda x:(H(x)-T_H(x))/2
    out['completion_parity_even_meV']=op(-theta(HE(theta(V)))-HE(V))*RY
    out['completion_parity_odd_meV']=op(-theta(HO(theta(V)))+HO(V))*RY
    return out,even,odd


def main():
    start=time.monotonic(); data=np.load(PARENT/'contracted_actions.npz'); G=data['G']; F=data['reference']
    theta,V,inv,R,closure=setup(F,G)
    assert not closure['inherited_1e_8_gate_pass']
    index={tuple(g):i for i,g in enumerate(G)}; N=len(G)
    actions={}; density={}; local_source={}; baseline={}
    for member in ('host','cd'):
        for cycle in (1,2):
            rows=[old.read(member,cycle,r) for r in (0,1)]
            phi=np.empty((2*N,176),complex); fields={k:np.empty_like(F) for k in ('direct','local0','local1')}
            for rank,row in enumerate(rows):
                ix=np.array([index[tuple(g)] for g in row['G']]); dest=np.r_[ix,N+ix]
                phi[dest]=row['phi']; np.testing.assert_array_equal(row['probe'],F[dest])
                for key in fields:fields[key][dest]=row[key]
                assert abs(row['B'][0,0]-2*np.pi/12.207630765082476)<1e-12
                v0,s0=vrs(member,cycle,rank,0); v1,s1=vrs(member,cycle,rank,1)
                if cycle==1:baseline[member,rank]=v0
                dv=v1-baseline[member,rank]
                scalar_spin_bound=float(np.max(abs(dv[:,0])+np.linalg.norm(dv[:,1:],axis=1)))
                local_source[f'{member}_{cycle}_{rank}']=dict(local_delta_op_bound_Ry=scalar_spin_bound,
                     magnetic_potential_max_Ry=float(max(np.max(abs(v0[:,1:])),np.max(abs(v1[:,1:])))),
                     local_spin_density_max=max(s0,s1))
                assert scalar_spin_bound<7 and not np.any(v0[:,1:]) and not np.any(v1[:,1:])
            f=rows[0]['wg']; np.testing.assert_array_equal(f,rows[1]['wg'])
            assert min(f)>=0 and max(f)<=1 and op(phi.conj().T@phi-np.eye(176))<TOL
            density[f'{member}_{cycle}']=source_density(phi,f,theta)
            if cycle==1:baseline[member,'action']=fields['local0']
            actions[f'{member}_{cycle}']=fields['direct']+fields['local1']-baseline[member,'action']
            anchor=float(np.trace(V.conj().T@(actions[f'{member}_{cycle}']@inv)).real/6)
            for rank in (0,1):
                entry=local_source[f'{member}_{cycle}_{rank}']
                entry['centered_local_bound_Ry']=entry['local_delta_op_bound_Ry']+abs(anchor)
                assert entry['centered_local_bound_Ry']<7
    for c in (1,2):
        actions[f'chemical_{c}']=actions[f'cd_{c}']-actions[f'host_{c}']
        assert op(actions[f'chemical_{c}']-data[f'c{c}_action_Ry'])<1e-12
    actions['chemical_change']=actions['chemical_2']-actions['chemical_1']
    results={}; centres={}
    for key,Y in actions.items():
        M=128 if key=='chemical_change' else (64 if key.startswith('chemical') else 32)
        results[key],E,O=split(Y,F,theta,V,inv,R,M)
        if key.startswith('chemical'):centres[key]=(E,O)
    # Check primary original source/ELF/PP pins, not just the derived NPZ.
    source_pins=json.loads((PARENT/'source_and_budget.json').read_text())['preserved_private_source_ELF_PP_pins']
    for path,s in source_pins.items():assert old.digest(path)==s,path
    exx_base=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/q-e/PW/src/exx_base.f90')
    code=exx_base.read_text()
    assert 'grid_factor = 8.d0/7.d0' in code and 'alpha  = 10._dp / gcutw' in code
    assert 'nqq = 100000' in code and 'dq = 5.0d0 / SQRT(alpha) / nqq' in code
    assert 'fac(ig) = - exxdiv' in code
    for member in ('host','cd'):
        xml=old.OLD/'evidence'/member/'data-file-schema.xml'
        original=old.MANIFEST['files'][str(old.ROOT/member/'out/r07hse8.save/data-file-schema.xml')]
        assert old.digest(xml)==original['sha256']
        t=ET.parse(xml)
        assert t.findtext('.//output/dft/hybrid/x_gamma_extrapolation')=='true'
        assert t.findtext('.//output/dft/hybrid/exxdiv_treatment')=='gygi-baldereschi'
        assert abs(float(t.findtext('.//output/dft/hybrid/screening_parameter'))-.106)<1e-14
        assert float(t.find('.//output/atomic_structure').get('alat'))>12
    norm_certificate=dict(source_conditioned=True, source= str(exx_base),sha256=old.digest(exx_base),
       kernel_nonzero_L1_over_volume_Ry_upper=46,
       kernel_zero_absolute_over_volume_Ry_upper=50,
       Fock_norm_Ry_upper=24*(1+TOL), centered_local_change_per_member_Ry_upper=7,
       actual_local_delta_max_Ry=max(a['local_delta_op_bound_Ry'] for a in local_source.values()),
       centered_member_activation_Ry_upper=32, centered_chemical_activation_Ry_upper=64,
       centered_chemical_increment_Ry_upper=128, raw_kernel_multiplier_packet_available=False,
       original_Theta_closure_gate_pass=False, native_or_state_gate_changed=False)
    output=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),baseline='4cfc16b',native_jobs=0,
      status='EXACT_SIX_COLUMN_RECONSTRUCTION_NO_GO; SOURCE_CONDITIONED_INTERVALS',
      closure=closure,source_density_Theta_defects=density, local_checks=local_source,
      source_norm_certificate=norm_certificate, observations=results,
      source_ELF_PP_pins=source_pins,native_packet_pins=old.PINS,
      parent_contracted_actions_sha256=old.digest(PARENT/'contracted_actions.npz'),
      wall_s=time.monotonic()-start,peak_audit_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      physically_stationary_state=False,material_gap_or_xc=None,
      interval_meaning='analytical completion intervals under reviewed frozen QE model norm bound, evaluated in floating arithmetic; not directed-rounding or material error bars')
    (HERE/'result.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(closure=closure,density=density,
      chemical={k:v for k,v in results.items() if k.startswith('chemical')},
      norm_certificate=norm_certificate,wall_s=output['wall_s']),indent=2),flush=True)


if __name__=='__main__':main()
