"""Focused independent checks on actual retained contractions and one native k.

Read-only; prints results. Does not overwrite validation or launch native code.
"""
import json
import numpy as np
from pathlib import Path
import evaluate as f
from mct_dft.qe_wavefunctions import cross_spinor_overlap


def check():
    r = json.loads((f.HERE/'numerical_result.json').read_text())
    z = np.load(f.HERE/'retained_contractions.npz')
    source = Path(json.loads((f.HERE/'preregistration.json').read_text())['source'])
    P,gp,kp = f.read_spinors(source/'out/r07_open.save/wfc1.hdf5')
    P = P[32:38]
    C,g,k = f.read_spinors(source/'out/r07_open.save/wfc2.hdf5')
    gc,kc = f.canonical(g,k)
    A,_ = f.periodic_contraction(P,gp,C,gc)
    U = np.zeros((6,6),complex)
    U[:2,:2] = np.array([[1,1j],[1j,1]])/np.sqrt(2)
    U[2:,2:] = np.exp(2j*np.pi*np.arange(4)[:,None]*np.arange(4)[None,:]/4)/2
    Ar,_ = f.periodic_contraction(np.einsum('ab,bsg->asg',U,P),gp,C,gc)
    rotation = max(np.max(abs(np.sum(abs(A[a:b])**2,axis=0)-np.sum(abs(Ar[a:b])**2,axis=0))) for a,b in [(0,2),(2,6)])
    assert rotation<1e-12
    origin = np.array([.13,-.27,.09])
    Ao,_ = f.periodic_contraction(P*np.exp(2j*np.pi*(gp@origin))[None,None,:],gp,
        C*np.exp(2j*np.pi*(gc@origin))[None,None,:],gc)
    origin_error = float(np.max(abs(A-Ao)))
    assert origin_error<1e-12
    shift = np.array([1,-2,1])
    gg,kk = f.canonical(g-shift,k+shift)
    assert np.array_equal(gg,gc) and np.max(abs(kk-kc))<1e-12
    try:
        cross_spinor_overlap(P,gp,kp,C,g,k)
    except ValueError as error:
        assert 'Bloch momenta differ' in str(error)
    else:
        raise AssertionError('old physical cross-k refusal weakened')
    for j,name in enumerate(['Gamma6_reference_probe','Gamma8_reference_probe']):
        w,sw = z['k_weights'],z['sector_band_weights'][:,j,:]
        m = (w[:,None]*sw*z['window_masses']).sum()
        n = (w[:,None]*sw*z['relative_window_moments_eV']).sum()
        assert abs(m-r['sectors'][name]['window_mass_lower'])<1e-14
        assert abs(n/m-r['sectors'][name]['relative_centroid_eV'])<1e-14
        assert abs((w[:,None]*sw).sum()+(w*z['plane_space_loss'][:,j]).sum()+(w*z['omitted_band_weight'][:,j]).sum()-1)<1e-12
        d = z['energies_eV'][:,-1]-r['reference_r_native_eV']-r['W_eV']
        envelope = r['eta_eV']/np.pi/d**2*(16*r['W_eV']/15)
        assert np.all(z['window_masses'][:,-1]<=envelope)
        # Permitted positive scalar completion; NOT a measured high-band input.
        lost,tail = np.maximum(z['plane_space_loss'][:,j],0),np.maximum(z['omitted_band_weight'][:,j],0)
        at0 = f.decimal_integrals(0.,r['W_eV'],r['eta_eV'])
        dm = (w*(tail*z['window_masses'][:,-1]+lost*at0[0])).sum()
        dn = (w*tail*z['relative_window_moments_eV'][:,-1]).sum()
        assert abs((n+dn)/(m+dm)-n/m)<=r['sectors'][name]['conditional_centroid_tail_error_upper_eV']
    return dict(passed=True,unitary_error=float(rotation),origin_error=origin_error,
        reciprocal_relabel_pass=True,old_physical_overlap_refusal_preserved=True,
        tail_completion_check_not_new_physical_data=True,no_MPI_QE=True)


if __name__ == '__main__':
    print(json.dumps(check(),indent=2))
