"""Independent actual-data Fourier/physical-label checks; NO H application."""
from pathlib import Path
import json
import sys
import h5py
import numpy as np
HERE=Path(__file__).resolve().parent

def run(check=False):
    audit=json.loads((HERE/'audit_result.json').read_text());rows={}
    for name,row in audit['members'].items():
        with h5py.File(Path(row['save'])/'charge-density.hdf5','r') as h:
            G=np.asarray(h['MillerIndices']);rho=np.asarray(h['rhotot_g']).view(np.complex128)
        grid=np.array(row['grid']);recip=np.zeros(tuple(grid),complex);recip[tuple((G%grid).T)]=rho
        r=np.fft.ifftn(recip)*np.prod(grid)
        errors=[]
        for j in [np.array([0,0,0]),np.array([1,2,3]),np.array([13,7,5])]:
            direct=np.sum(rho*np.exp(2j*np.pi*(G@(j/grid))))
            errors.append(float(abs(direct-r[tuple(j)])))
        assert max(errors)<1e-11
        # Exactly the same data reordered into a deliberately different local
        # array. Integer-label gather restores every native complex byte.
        order=np.arange(len(G))[::-1];lookup={tuple(g):i for i,g in enumerate(G[order])}
        recovered=rho[order][[lookup[tuple(g)] for g in G]]
        assert recovered.tobytes()==rho.tobytes()
        rows[name]=dict(direct_three_point_Fourier_vs_FFT_abs_errors=errors,
            arbitrary_density_G_reordering_restores_exact_bytes=True,
            zero_frequency_Nyquist_alias_collisions=len(G)-len(np.unique(np.ravel_multi_index(tuple((G%grid).T),tuple(grid)))))
    # Packet and memory formulas checked independently of the source parser.
    n=21595;ng=173631;nr=80**3
    arrays=[np.dtype('complex128').itemsize*(2*n)*12]*5
    packet=sum(arrays)+16*ng*4+8*nr*4*2+8*3*(n+ng)+16*8+28*8+9*8+3*8+6*8
    assert packet==audit['same_field_set_single_rank_packet_bytes_CONDITIONAL']
    record=dict(status='PASS_READ_ONLY_DATA_AND_FORMULA_CHECKS_NOT_NATIVE_EQUIVALENCE',members=rows,
        independent_single_rank_packet_formula_B=packet,native_H_action_count=0,
        PBE_XC_SOC_or_singleton_runtime_NOT_validated=True)
    if check:
        assert record==json.loads((HERE/'independent_results.json').read_text())
        print('INDEPENDENT_READ_ONLY_RECHECK_PASS')
    else:
        with (HERE/'independent_results.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
        print(json.dumps(record,indent=2))

if __name__=='__main__':run(sys.argv[1:]==['--check'])
