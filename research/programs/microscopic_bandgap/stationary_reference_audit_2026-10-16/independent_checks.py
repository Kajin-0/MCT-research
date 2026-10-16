"""Independent scalar/native-packet checks. No QE, new models or DFT writes."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from decimal import Decimal, localcontext

import h5py
import numpy as np
from scipy.optimize import bisect
from scipy.special import expit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def main():
    d = json.loads((HERE/'native_audit.json').read_text())
    results = []
    for row in d['records']:
        save = Path(row['run'])/'out/r07.save'
        t = ET.parse(save/'data-file-schema.xml').getroot()
        rows = t.findall('output/band_structure/ks_energies')
        w = np.array([float(x.find('k_point').attrib['weight']) for x in rows])
        e = np.array([np.fromstring(x.findtext('eigenvalues'),sep=' ') for x in rows])
        f = np.array([np.fromstring(x.findtext('occupations'),sep=' ') for x in rows])
        with localcontext() as c:
            c.prec = 50
            exactN = sum(Decimal(str(wi))*sum(Decimal(str(v)) for v in fi) for wi,fi in zip(w,f))
        sig = float(t.find('input/bands/smearing').attrib['degauss'])
        # Bisection differs from the primary Brent implementation; all spectra are real native data.
        mu = bisect(lambda x: sum(wi*expit((x-ei)/sig).sum() for wi,ei in zip(w,e))-36,
                    float(e.min()-1),float(e.max()+1),xtol=1e-15)
        assert abs((mu-float(t.findtext('output/band_structure/fermi_energy')))*27.211386245988
                   - row['FD_reinterpretation_mu_shift_eV']) < 1e-10
        # Schur: an exactly invariant density on one Gamma8 copy is scalar.
        # Range/2 is a necessary distance to ANY scalar occupation on that copy.
        shell = f[0,34:38]
        schur_distance = np.ptp(shell)/2
        assert schur_distance > 1e-8  # original strict symmetry target; not chosen from this result
        assert abs(sum(wi*fi.sum() for wi,fi in zip(w,f))-36) < 1e-12
        with h5py.File(save/'wfc1.hdf5','r') as h:
            g=h['MillerIndices'][:]
            b=np.array([h['MillerIndices'].attrs['bg'+str(i)] for i in [1,2,3]])
            u=np.ascontiguousarray(h['evc'][:]).view(complex).reshape(44,2,len(g))
        # Direct per-component summation independent of the vectorized primary tail reduction.
        selected=np.array([np.dot(x@b,x@b)>50+1e-10 for x in g])
        tails=[sum(float(z.real*z.real+z.imag*z.imag) for spin in a for z in spin[selected])
               for a in u[32:38]]
        assert max(abs(np.array(tails)-row['Gamma6_Gamma8_loss_projecting_e90_to_e50'])) < 2e-18
        results.append(dict(run=row['run'], charge_from_decimal_text=str(exactN),
            Gamma8_distance_to_scalar_occupation=schur_distance,
            e90_to_e50_amplitude_loss_sqrt=list(np.sqrt(tails)),
            independently_bisected_FD_mu_Ha=mu,
            original_SCF_acceptance_unchanged=row['accepted_scf']))
    nominal=lambda n,b,q: n**3*2*b*q*16
    memory=dict(primitive_f120_nominal_B=nominal(32,44,64),
                primitive_f360_nominal_B=nominal(54,44,64),
                original_16atom_f120_nominal_B=nominal(64,352,8),
                cap_12GiB_B=12*2**30)
    assert memory['original_16atom_f120_nominal_B']==22*2**30
    assert memory['primitive_f360_nominal_B']>memory['cap_12GiB_B']
    assert memory['primitive_f120_nominal_B']==int(2.75*2**30)
    frozen=[]
    for p in ['AGENTS.md',
              'research/programs/microscopic_bandgap/public_optical_intake_2026-10-15/verification.json',
              'research/programs/microscopic_bandgap/append_hamiltonian_2026-10-15/strict_refusal.json',
              'research/programs/microscopic_bandgap/static_environment_2026-10-15/evidence/GUARD_RESULT.json',
              'research/programs/microscopic_bandgap/single_state304_2026-10-15/native_result.json',
              'research/programs/microscopic_bandgap/hybrid_convergence_2026-10-15/decision.md',
              'research/programs/microscopic_bandgap/physical_input_qualification_2026-10-11/decision.md',
              'docs/derivations/host_invariant_reaction_kernel.md']:
        data=(ROOT/p).read_bytes()
        frozen.append(dict(path=p,sha256=hashlib.sha256(data).hexdigest()))
    result=dict(status='PASS_READ_ONLY_INDEPENDENT_CHECKS',records=results,
                memory_arithmetic=memory,protected_MCT=frozen,
                no_native_jobs=True,physical_xc=None,stationary_FD_certified=False,
                notes='Real retained spectra only; no synthetic optical/mass example. '
                      'Schur scalar distance assumes the qualified native irrep frame; '
                      'not an interval-certified full-H or material residual.')
    (HERE/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
