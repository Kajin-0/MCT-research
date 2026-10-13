"""Read-only intake of the user's actual stock HSE run; no QE launch."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import h5py
import numpy as np

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011/hse_native_probe_20261013'
UNIT='r07-small-hgte-hse-20261013.service'
INVOCATION='ccd6ca6666f84679a01a048dbb6d6990'


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def main():
    result=json.loads((ROOT/'result.json').read_text()); manifest=json.loads((ROOT/'manifest.json').read_text())
    text=(ROOT/'pw.out').read_text()
    assert sha(ROOT/'pw.in')==result['input_sha256']==manifest['input_sha256']
    assert sha(ROOT/'pw.out')==result['stdout_sha256']
    energies=[float(v) for v in re.findall(r'^\s*!?\s+total energy\s*=\s*([-+\d.]+)\s+Ry',text,re.M)]
    dexx=[float(v) for v in re.findall(r'est\. exchange err \(dexx\)\s*=\s*([-+\d.Ee]+)',text)]
    fock=[float(v) for v in re.findall(r'\+ Fock energy \(ACE\)\s*=\s*([-+\d.Ee]+)',text)]
    stopped=int(re.search(r'Calculation \(EXX\) stopped after iteration #\s+(\d+)',text)[1])
    assert stopped==14 and energies[-len(result['all_total_energies_ry']):]==result['all_total_energies_ry']
    assert energies[-1]==-484.05790653 and dexx[-1]==3.87e-6 and fock[-1]==-8.96709093
    assert 'Maximum CPU time exceeded' in text and 'JOB DONE.' in text
    assert re.search(r'MPI processes:\s+2',text) and 'Non magnetic calculation with spin-orbit' in text
    xmlpath=ROOT/'out/r07m4.save/data-file-schema.xml'; tree=ET.parse(xmlpath)
    def nodes(tag):return [n for n in tree.iter() if n.tag.split('}')[-1]==tag]
    assert nodes('convergence_achieved')[0].text=='false'
    xml_energy_Ry=2*float(nodes('etot')[0].text)
    assert abs(xml_energy_Ry-energies[-1])<5e-9
    save=[]; grams={}
    for p in sorted((ROOT/'out').rglob('*')):
        if p.is_file():
            record=dict(path=str(p),bytes=p.stat().st_size,allocated_bytes=p.stat().st_blocks*512,sha256=sha(p))
            if p.suffix=='.hdf5':
                with h5py.File(p,'r') as f:
                    convert=lambda v: v.decode() if isinstance(v,bytes) else v.tolist() if hasattr(v,'tolist') else v
                    record['attributes']={k:convert(v) for k,v in f.attrs.items()}
                    record['datasets']={k:dict(shape=list(v.shape),dtype=str(v.dtype),storage_bytes=v.id.get_storage_size()) for k,v in f.items()}
                    if p.name.startswith(('wfc','ace')):
                        assert int(f.attrs['nbnd'])==48 and int(f.attrs['npol'])==2
                        for row in f['evc']: assert np.isfinite(row).all()
                        if p.name.startswith('wfc'):
                            a=f['evc'][:].view(np.complex128)
                            grams[p.name]=float(np.max(np.abs(a.conj()@a.T-np.eye(48))))
                            assert grams[p.name]<1e-12
            save.append(record)
    events=[json.loads(s) for s in subprocess.check_output(['journalctl','--user','-u',UNIT,'--no-pager','-o','json'],text=True).splitlines()]
    exact=[e for e in events if e.get('USER_INVOCATION_ID')==INVOCATION]
    start=next(e for e in exact if e.get('JOB_TYPE')=='start')
    final=next(e for e in exact if 'MEMORY_PEAK' in e)
    assert ROOT.name in start['MESSAGE'] and '--host localhost:2 -np 2 pw.x' in start['MESSAGE']
    assert start['_BOOT_ID']==final['_BOOT_ID'] and start['_UID']==final['_UID']=='1001'
    observation=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        kind='ACTUAL_NATIVE_STOCK_QE_HSE_PROGRESS_NOT_CONVERGED',source=str(ROOT),
        QE_version='7.5',MPI_ranks=2,atoms=2,bands=48,HSE_fraction=.25,screening_parameter=.106,
        cutoffs_Ry=[90,360,120],k_mesh=[2,2,2],q_mesh=[2,2,2],SOC=True,
        outer_EXX_iterations=stopped,last_total_energy_Ry=energies[-1],last_dexx_Ry=dexx[-1],
        all_stdout_total_energy_records_Ry=energies,supplied_result_energies_are_tail_not_all=True,
        last_Fock_ACE_Ry=fock[-1],saved_XML_energy_Ry=xml_energy_Ry,
        fully_converged=False,termination='MAX_SECONDS 420; native elapsed429.15s; JOB DONE is not convergence',
        journal=dict(unit=UNIT,invocation=INVOCATION,memory_peak_bytes=int(final['MEMORY_PEAK']),
            swap_peak_bytes=int(final['MEMORY_SWAP_PEAK']),cpu_seconds=int(final['CPU_USAGE_NSEC'])/1e9,
            elapsed_journal_seconds=(int(final['__MONOTONIC_TIMESTAMP'])-int(start['__MONOTONIC_TIMESTAMP']))/1e6),
        hashes={p.name:sha(p) for p in [ROOT/'pw.in',ROOT/'pw.out',ROOT/'pw.err',ROOT/'result.json',ROOT/'manifest.json',xmlpath]},
        current_stock_executable_sha256=sha((DFT/'.local/qe-env/bin/pw.x').resolve()),
        current_PP_sha256={s:sha(DFT/'pseudopotentials'/(s+'_sg15_pbe_fr_v12.UPF')) for s in ['Hg','Te']},
        DFT_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=DFT,text=True).strip(),
        save_logical_bytes=sum(r['bytes'] for r in save),save_allocated_bytes=sum(r['allocated_bytes'] for r in save),
        xml_input_ecutfock_Ha=[n.text for n in nodes('ecutfock')],
        schema_caution='Input-section ecutfock=0; output-section60Ha plus native stdout120Ry identifies actual cutoff. Do not read the first XML match as the run value.',
        exact_matching_startup_seed=False,save_is_after_outer_iteration14=True,
        independently_checked_saved_NC_Gram_errors=grams,
        native_streamed_equivalence=False,Cd_material_result=False,physical_xc_claim=False)
    for name,value in [('reference_evidence.json',observation),('reference_save_inventory.json',save),('reference_journal.json',events)]:
        (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
    for name in ['pw.in','result.json','manifest.json']:(HERE/('stock_'+name)).write_bytes((ROOT/name).read_bytes())
    (HERE/'stock_stdout.txt').write_bytes((ROOT/'pw.out').read_bytes())
    (HERE/'stock_stderr.txt').write_bytes((ROOT/'pw.err').read_bytes())
    pbe=DFT/'.local/qe75_lowram_20261011/physical_pbe_soc_16atom_20261013'
    rejection=(pbe/'host/pw_160.out').read_text()
    assert 'too few bands noncolin case' in rejection
    pbe_record=dict(provenance_sha256=sha(pbe/'provenance.json'),
        host_stdout_sha256=sha(pbe/'host/pw.out'),rejected160_stdout_sha256=sha(pbe/'host/pw_160.out'),
        rejected160_reason='QE setup: too few bands noncolin case',
        larger_host_last_observation='Slow Davidson; no completed material packet in retained stdout',
        larger_host_stopping_action='User-reported stopped; not inferred from truncated stdout alone',
        Cd_result=False,original_HSE_352_input_changed=False)
    (HERE/'prior_pbe_attempts.json').write_text(json.dumps(pbe_record,indent=2)+'\n')
    print(json.dumps(observation,indent=2))


if __name__=='__main__':main()
