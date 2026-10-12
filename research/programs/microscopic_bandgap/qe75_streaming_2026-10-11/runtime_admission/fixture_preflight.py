"""Read-only fixture qualification + explicit link-only control. Never runs QE/MPI.

Exact text whitelist is deliberately narrower than a general QE parser. This
is a preregistration audit, not a native FFT sizing or initial-state certificate.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import resource
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

from family_runtime import HERE,PRIVATE,LIB,memory,Refusal,exact_extent
from native_bundle import artifact_sha256
from resource_guard import LinuxGuard
from process_identity import mpi_inventory

DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011'
NATIVE=ROOT/'native_bridge'
CONTROL=PRIVATE/'link-only/pw.control.M4_UNVALIDATED'
STREAM=NATIVE/'link-only/pw.bridge.RUNTIME_REFUSED'
QE_PIN='770a0b2d12928a67048e2f3da8d10d057e52179e'
PP_SHA={'Hg':'846a3a2bbef4b97835486a60468a0dafd68d622e21ebfb76011e51ce65fafee0',
        'Te':'1b6d3177b82988cecabebf7da1636825613b7270bc269795a1fb6c12743e12fa'}
PW_OPTIONS=['-npool','1','-nb','1','-nt','1','-nd','1']
THREAD_ENV={'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}


def template(mode):
    if mode not in ['control','stream']: raise Refusal('fixture mode')
    return f"""&CONTROL
 calculation = 'scf'
 pseudo_dir = '{DFT}/pseudopotentials'
 outdir = '{PRIVATE}/native-fixture-{mode}/out'
 verbosity = 'high'
 tprnfor = .false.
 tstress = .false.
 wf_collect = .true.
 prefix = 'r07m4'
 nstep = 1
 max_seconds = 600.0
 restart_mode = 'from_scratch'
/
&SYSTEM
 ibrav = 0
 nat = 2
 ntyp = 2
 ecutwfc = 90
 ecutrho = 360
 ecutfock = 120
 occupations = 'smearing'
 smearing = 'mv'
 degauss = 0.001
 nbnd = 48
 noncolin = .true.
 lspinorb = .true.
 input_dft = 'HSE'
 exx_fraction = 0.25
 screening_parameter = 0.106
 nqx1 = 2
 nqx2 = 2
 nqx3 = 2
/
&ELECTRONS
 conv_thr = 1e-10
 mixing_beta = 0.3
 electron_maxstep = 100
 exx_maxstep = 20
 adaptive_thr = .true.
 conv_thr_init = 1e-5
 conv_thr_multi = 0.1
 diagonalization = 'david'
 diago_full_acc = .true.
/
ATOMIC_SPECIES
 Hg 200.5920 Hg_sg15_pbe_fr_v12.UPF
 Te 127.6000 Te_sg15_pbe_fr_v12.UPF
CELL_PARAMETERS angstrom
 0.0 3.23 3.23
 3.23 0.0 3.23
 3.23 3.23 0.0
ATOMIC_POSITIONS crystal
 Hg 0.0 0.0 0.0
 Te 0.25 0.25 0.25
K_POINTS automatic
 2 2 2 0 0 0
"""


def match_deck(text,mode):
    if text!=template(mode): raise Refusal('exact small-fixture deck whitelist mismatch')
    return hashlib.sha256(text.encode()).hexdigest()


def physical_text(text):
    return re.sub(r"outdir = '[^']+'", "outdir = 'OPERATIONAL_PATH'",text)


def backends(binary):
    # Only a previously locally built ELF is inspected. ldd invokes the loader
    # in tracing mode, never the PW main program, MPI launcher or SCF routines.
    r=subprocess.run(['/usr/bin/ldd',str(binary)],capture_output=True,text=True,timeout=10,check=True)
    if 'not found' in r.stdout: raise Refusal('missing linked backend')
    paths=set()
    for line in r.stdout.splitlines():
        for name in re.findall(r'(/[^\s()]+)',line):
            path=Path(name).resolve()
            if path.is_file(): paths.add(path)
    return {str(p):artifact_sha256(p) for p in sorted(paths)}


def link_control():
    """Reuse already compiled matched stock-mode objects; bounded private link."""
    if CONTROL.exists(): raise Refusal('preserve existing control: link is one-shot')
    guard=LinuxGuard(LIB);info=guard.probe(PRIVATE)
    if info['probe_errno'] or info['fs_type']!=0xef53: raise Refusal('local ext4 required')
    if info['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):
        raise Refusal('link-only resource reserve unsafe')
    old=json.loads((HERE.parent/'native_bridge/build_results.json').read_text())
    if artifact_sha256(STREAM)!=old['link']['sha256']: raise Refusal('stream binary pin changed')
    command=list(old['records'][-1]['command'])
    destination=CONTROL.parent;destination.mkdir(exist_ok=False)
    archive=destination/'libqe_pw_control.a'
    stock=DFT/'.local/qe-env/lib/libqe_pw.a';stock_sha=artifact_sha256(stock)
    shutil.copy2(stock,archive)
    replaced=['exx','electrons','punch','run_pwscf','wfcinit']
    subprocess.run(['/usr/bin/ar','d',str(archive),*[n+'.f90.o' for n in replaced]],check=True,timeout=10)
    units=['exx_checkpoint_state','exx_qstream',*replaced]
    objects=[]
    for name in units:
        source=NATIVE/'stock-objects'/(name+'.o');target=destination/(name+'.f90.o')
        shutil.copy2(source,target);objects.append(target)
    subprocess.run(['/usr/bin/ar','r',str(archive),*map(str,objects)],check=True,timeout=10)
    command[command.index(str(NATIVE/'link-only/libqe_pw_bridge.a'))]=str(archive)
    command[-1]=str(CONTROL)
    started=time.monotonic()
    result=subprocess.run(command,capture_output=True,text=True,timeout=60,check=True,cwd=DFT)
    if artifact_sha256(stock)!=stock_sha: raise Refusal('stock archive changed')
    report={'passed':True,'command':command,'wall_seconds':time.monotonic()-started,
            'stderr':result.stderr,'maximum_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'control_sha256':artifact_sha256(CONTROL),'compiler_sha256':artifact_sha256(Path(command[0])),
            'stock_archive_preserved':True,'PW_MPI_HSE_executed':False,
            'objects':{str(p):artifact_sha256(p) for p in objects}}
    (PRIVATE/'link_control.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def check():
    result={'status':'BLOCKED','PW_MPI_HSE_executed':False,'qe_source_pin':QE_PIN,
            'exact_extents_bytes':None,'native_output_envelope_bytes':None,'native_admission_issued':False}
    result['deck_sha256']={mode:match_deck((HERE/(mode+'.in')).read_text(),mode) for mode in ['control','stream']}
    result['physical_numerical_text_identical']=physical_text(template('control'))==physical_text(template('stream'))
    result['PP']={}
    for element,sha in PP_SHA.items():
        path=DFT/'pseudopotentials'/(element+'_sg15_pbe_fr_v12.UPF')
        if artifact_sha256(path)!=sha: raise Refusal('pseudopotential pin mismatch')
        header=ET.fromstring(re.search(r'<PP_HEADER\b.*?/>',path.read_text(),re.S).group()).attrib
        if header['pseudo_type']!='NC' or header['relativistic']!='full' or header['has_so'] not in ['T','true']:
            raise Refusal('wrong PP type/SOC')
        result['PP'][element]={'path':str(path),'sha256':sha,'header':header}
    result['valence_electrons']=sum(float(v['header']['z_valence']) for v in result['PP'].values())
    if result['valence_electrons']!=36 or 48<=result['valence_electrons']: raise Refusal('spinor occupancy fixture invalid')
    old=json.loads((HERE.parent/'native_bridge/build_results.json').read_text())
    for name,sha in old['source_sha256'].items():
        if artifact_sha256(Path(old['source_directory'])/name)!=sha: raise Refusal('matched native source changed')
    if artifact_sha256(STREAM)!=old['link']['sha256']: raise Refusal('stream candidate changed')
    build=json.loads((PRIVATE/'link_control.json').read_text())
    if artifact_sha256(CONTROL)!=build['control_sha256']: raise Refusal('control changed')
    result['binary_sha256']={str(p):artifact_sha256(p) for p in [CONTROL,STREAM]}
    result['backend_files']={mode:backends(p) for mode,p in [('control',CONTROL),('stream',STREAM)]}
    result['same_dynamic_backend']=result['backend_files']['control']==result['backend_files']['stream']
    if not result['same_dynamic_backend']: raise Refusal('unmatched dynamic backend')
    result['compiler_sha256']=build['compiler_sha256']
    result['compile_flags_by_mode']={mode:next(r['command'][1:r['command'].index('-J')] for r in old['records']
                                            if r.get('mode')==mode) for mode in ['stock','stream']}
    result['MPI_launcher']={'path':str((DFT/'.local/qe-env/bin/mpiexec').resolve()),
                            'sha256':artifact_sha256((DFT/'.local/qe-env/bin/mpiexec').resolve()),
                            'rank_count':2,'PW_options':PW_OPTIONS,'thread_environment':THREAD_ENV,
                            'actual_native_layout_certified':False}
    result['visible_MPI_families']=mpi_inventory()
    try:
        mpi_inventory(require_global=True);result['global_MPI_inventory_complete']=True
    except Refusal as error:
        result['global_MPI_inventory_complete']=False;result['inventory_refusal']=str(error)
    result['storage_snapshot']=LinuxGuard(LIB).probe(PRIVATE)
    result['MemAvailable_bytes']=memory()['MemAvailable']
    result['original_22GiB_plus_10GiB_refused']=result['storage_snapshot']['available_bytes']<32*(1<<30)
    result['blockers']=[
      'All-rank compiled native MPI lease registration and ancestor-hook mapping are absent; fake peers cannot grant native authority.',
      'Native EXX probe action/energy/Gram/ACE instrumentation and actual checkpoint density/wave/old-ACE readback comparison are absent.',
      'Exact two-rank FFT/stream/state extents and maximum native output allocation are uncertified; no guessed reservation admitted.',
      'Identical initial wave/G/k state is not certified; matching decks alone do not certify a matched action comparison.']
    if not result['global_MPI_inventory_complete']: result['blockers'].append(result['inventory_refusal']+'; no global exclusivity claim.')
    (PRIVATE/'fixture_preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    if sys.argv[1:] == ['link-control']: print(json.dumps(link_control(),indent=2))
    elif sys.argv[1:] == ['check']: print(json.dumps(check(),indent=2))
    else: raise Refusal('explicit link-control or read-only check only; no launch command')
