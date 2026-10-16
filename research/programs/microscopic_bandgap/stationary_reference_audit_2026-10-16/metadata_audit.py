"""Supplement the real-state audit with XML/stdout/container metadata only."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET

import h5py
import numpy as np

HERE=Path(__file__).resolve().parent


def main():
    source=HERE/'native_audit.json'
    a=json.loads(source.read_text())
    result=[]
    common_frames=[]
    for r in a['records']:
        root=Path(r['run'])
        t=ET.parse(root/'out/r07.save/data-file-schema.xml').getroot()
        h=t.find('output/dft/hybrid'); basis=t.find('output/basis_set')
        model=dict(ecutwfc_Ry=2*float(basis.findtext('ecutwfc')),
                   ecutrho_Ry=2*float(basis.findtext('ecutrho')),
                   ecutfock_Ry=2*float(h.findtext('ecutfock')),
                   screening_Bohr_inverse=float(h.findtext('screening_parameter')),
                   exx_fraction=float(h.findtext('exx_fraction')),
                   q_grid=h.find('qpoint_grid').attrib,
                   exxdiv_treatment=h.findtext('exxdiv_treatment'),
                   x_gamma_extrapolation=h.findtext('x_gamma_extrapolation'),
                   SOC=t.findtext('output/band_structure/spinorbit'),
                   nominal_scf_accepted_signed_Gamma_order_eV=json.loads(
                       (root/'gamma/signed_gap.json').read_text())['E_Gamma6_minus_Gamma8_eV'])
        bs=t.find('output/band_structure')
        gamma=bs.findall('ks_energies')[0]
        e=np.fromstring(gamma.findtext('eigenvalues'),sep=' ')*27.211386245988
        f=np.fromstring(gamma.findtext('occupations'),sep=' ')
        pairs=[(32,33),(34,35),(36,37)]
        row=dict(run=r['run'],effective_model=model,
                 input_XML_ecutfock_Ha=t.findtext('input/dft/hybrid/ecutfock'),
                 Gamma_Kramers_pair_energy_differences_eV=[float(abs(e[i]-e[j])) for i,j in pairs],
                 Gamma_Kramers_pair_occupation_differences=[float(abs(f[i]-f[j])) for i,j in pairs],
                 last_native_exchange_convergence_lines=[l.strip() for l in (root/'pw.out').read_text().splitlines()
                                                         if 'dexx' in l or 'EXX self-consistency' in l][-3:])
        cell=t.find('output/atomic_structure/cell')
        positions=t.find('output/atomic_structure/atomic_positions')
        frame=dict(cell_bohr=[np.fromstring(x.text,sep=' ').tolist() for x in cell],
                   species=[x.attrib['name'] for x in positions],
                   positions_bohr=[np.fromstring(x.text,sep=' ').tolist() for x in positions],
                   PP_sha256=json.loads((root/'result.json').read_text())['pp_sha256'])
        common_frames.append(frame)
        row['physical_frame']=frame
        pins=a['preserved_source_hashes']
        row['SCF_and_expanded_rhoG_bytes_equal']=(pins[str(root/'out/r07.save/charge-density.hdf5')]
                                                ==pins[str(root/'out/r07_open.save/charge-density.hdf5')])
        log=root/'gamma/open_grid.out'
        log_hash=hashlib.sha256(log.read_bytes()).hexdigest()
        assert log_hash==json.loads((root/'gamma/open_grid_result.json').read_text())['stdout_sha256']
        row['open_grid_stdout_sha256']=log_hash
        row['open_grid_EXX_grid']=list(map(int,re.findall(
            r'EXX grid:.*?FFT dimensions:\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\)',log.read_text())[-1]))
        with h5py.File(root/'out/r07.save/charge-density.hdf5','r') as aa, h5py.File(root/'out/r07_open.save/charge-density.hdf5','r') as bb:
            row['SCF_expanded_charge_datasets_equal']=all(np.array_equal(aa[k][:],bb[k][:]) for k in ['rhotot_g','MillerIndices'])
            row['SCF_expanded_charge_max_float_diff']=float(np.max(abs(aa['rhotot_g'][:]-bb['rhotot_g'][:])))
        result.append(row)
    assert common_frames[0]==common_frames[1]
    (HERE/'metadata_audit.json').write_text(json.dumps(dict(records=result,
        native_lattice_origin_species_PP_frames_equal=True,
        source_audit_sha256=hashlib.sha256(source.read_bytes()).hexdigest()),indent=2)+'\n')
    print('PASS metadata and original/export charge datasets; no full-rho(orbitals) consistency claim.')


if __name__=='__main__':
    main()
