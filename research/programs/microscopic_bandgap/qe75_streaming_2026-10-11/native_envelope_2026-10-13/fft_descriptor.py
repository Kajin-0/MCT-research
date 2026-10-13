"""Typed rank FFT evidence codec. Parsing evidence NEVER issues native authority."""
import hashlib
import struct
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'m5_readiness'))
from binding import HERE as _binding_root
from binding import Refusal

SCOPES=['npwx','npol','nbnd','nks','nkstot','nkqs','nqs','ngm','ngms','nspin','nmix','io_level']
SCALARS=['nr1','nr2','nr3','nr1x','nr2x','nr3x','nproc','nproc2','nproc3','mype','mype2','mype3',
         'my_nr2p','my_nr3p','my_i0r2p','my_i0r3p','nnp','nnr','nnr_tg','has_task_groups','use_pencil_decomposition']
ARRAY1=['nr1p','nr1w','nr2p','nr3p','nr2p_offset','nr3p_offset','i0r2p','i0r3p',
        'ir1p','ir1w','nsp','nsw','ngl','nwl','iproc2','iproc3','iplp','iplw','iss','isind','ismap','nl','nlm',
        'tg_snd','tg_rcv','tg_sdsp','tg_rdsp']
ARRAY2=['iproc','indp','indw','nsp_offset','nsw_offset']
LABELS=['dense','smooth','fock']
LIMIT=64*(1<<20)


def read(path):
    p=Path(path)
    if not p.is_file() or p.is_symlink() or p.stat().st_size>LIMIT:raise Refusal('FFT file extent/type')
    raw=p.read_bytes();pos=0
    def take(n):
        nonlocal pos
        if n<0 or pos+n>len(raw):raise Refusal('FFT truncated record')
        value=raw[pos:pos+n];pos+=n;return value
    def ints(n):return list(struct.unpack('<'+'q'*n,take(8*n)))
    if take(8)!=b'FFTRES01':raise Refusal('FFT magic')
    version,rank,world,n=ints(4)
    if (version,world,n)!=(1,2,len(SCOPES)) or rank not in [0,1]:raise Refusal('FFT header')
    hashes=[]
    for _ in range(2):
        h=take(64).decode('ascii')
        if len(h)!=64 or any(c not in '0123456789abcdef' for c in h):raise Refusal('FFT fingerprint syntax')
        hashes.append(h)
    scope=dict(zip(SCOPES,ints(n)))
    if not 1<=scope['npwx']<=19683 or (scope['npol'],scope['nbnd'],scope['nspin'])!=(2,48,4):raise Refusal('FFT fixture scope')
    if not 1<=scope['ngms']<=scope['ngm']<=148877:raise Refusal('FFT reciprocal density scope')
    if not 1<=scope['nks']<=8 or scope['nks']!=scope['nkstot'] or not 1<=scope['nkqs']<=8:raise Refusal('FFT k scope')
    if not 1<=scope['nqs']<=8 or not 1<=scope['nmix']<=25 or scope['io_level']<0:raise Refusal('FFT mix/q/io scope')
    desc={}
    for label in LABELS:
        if take(16).rstrip(b' ').decode('ascii')!=label:raise Refusal('FFT label/order')
        d=dict(zip(SCALARS,ints(len(SCALARS))))
        if min(d[k] for k in ['nr1','nr2','nr3','nr1x','nr2x','nr3x','nnr'])<1:raise Refusal('FFT dimension')
        if any(d[f'nr{i}']>d[f'nr{i}x'] for i in [1,2,3]):raise Refusal('FFT leading dimension')
        if d['nproc']!=2 or d['nproc2']*d['nproc3']!=2 or d['mype']!=rank:raise Refusal('FFT rank/group')
        if d['has_task_groups']!=0 or d['use_pencil_decomposition'] not in [0,1]:raise Refusal('FFT unsupported task groups')
        for name in ARRAY1+ARRAY2:
            if take(24).rstrip(b' ').decode('ascii')!=name:raise Refusal('FFT array label/order')
            a,b=ints(2)
            if a==-1 and b==0:d[name]=None;continue
            if a<0 or b<1 or a*b>2_000_000 or (name in ARRAY1 and b!=1):raise Refusal('FFT array shape')
            d[name]={'shape':[a,b],'values':ints(a*b)}
        for name,nsize in [('nr2p',d['nproc2']),('nr3p',d['nproc3']),('i0r2p',d['nproc2']),('i0r3p',d['nproc3'])]:
            if d[name] is None or d[name]['shape']!=[nsize,1]:raise Refusal('FFT partition shape')
        for direction in [2,3]:
            counts=d[f'nr{direction}p']['values'];offsets=d[f'i0r{direction}p']['values']
            if min(counts)<0 or offsets!=[sum(counts[:i]) for i in range(len(counts))] or sum(counts)!=d[f'nr{direction}']:
                raise Refusal('FFT partition cover')
            me=d[f'mype{direction}']
            if not 0<=me<len(counts) or (d[f'my_nr{direction}p'],d[f'my_i0r{direction}p'])!=(counts[me],offsets[me]):
                raise Refusal('FFT local owner')
        if d['nl'] is None or any(v<1 or v>d['nnr'] for v in d['nl']['values']) or len(set(d['nl']['values']))!=len(d['nl']['values']):raise Refusal('FFT G map')
        desc[label]=d
    if take(8)!=b'FFTEND01' or pos!=len(raw):raise Refusal('FFT trailer/extra bytes')
    return {'rank':rank,'world':world,'profile':hashes[0],'common_input':hashes[1],'scope':scope,'descriptors':desc,
            'extent':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'native_authenticated_observation':False}


def compare(control,stream,profiles,common):
    if len(control)!=2 or len(stream)!=2:raise Refusal('all ranks required')
    pair={}
    for mode,paths in [('stock',control),('stream',stream)]:
        entries=[read(p) for p in paths]
        if {e['rank'] for e in entries}!={0,1}:raise Refusal('FFT rank duplicate/missing')
        if any(e['profile']!=profiles[mode] or e['common_input']!=common for e in entries):raise Refusal('FFT profile/input mismatch')
        pair[mode]={e['rank']:e for e in entries}
        for label in LABELS:
            a,b=[pair[mode][r]['descriptors'][label] for r in [0,1]]
            for key in ['nr1','nr2','nr3','nr1x','nr2x','nr3x','nproc2','nproc3','nr2p','nr3p','i0r2p','i0r3p']:
                if a[key]!=b[key]:raise Refusal('FFT inconsistent global partition')
            if {(a['mype2'],a['mype3']),(b['mype2'],b['mype3'])}!={(i,j) for i in range(a['nproc2']) for j in range(a['nproc3'])}:
                raise Refusal('FFT coordinate cover')
    for r in [0,1]:
        if pair['stock'][r]['scope']!=pair['stream'][r]['scope'] or pair['stock'][r]['descriptors']!=pair['stream'][r]['descriptors']:
            raise Refusal('FFT corresponding-rank layout mismatch')
    return {'passed':True,'typed_layouts_equal':True,'rank_extents':[pair['stock'][r]['extent'] for r in [0,1]],
            'native_authenticated_observation':False,'native_admission_issued':False}
