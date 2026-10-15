"""Read-only exact native firstACE packets and scientific consistency gates."""
from pathlib import Path
import json
import sys
from xml.etree import ElementTree as ET
import numpy as np
from scipy.special import expit
import h5py

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
PAIR=DFT/'.local/qe75_lowram_20261011/h8r_20261015/p1'
sys.path.insert(0,str(DFT/'src'))
from mct_dft.qe_wavefunctions import read_spinors


class Reader:
    def __init__(self,path):self.data=Path(path).read_bytes();self.cursor=0
    def take(self,typ,shape):
        n=int(np.prod(shape));size=n*np.dtype(typ).itemsize
        if self.cursor+size>len(self.data):raise ValueError('truncated native packet')
        x=np.frombuffer(self.data,typ,n,self.cursor).reshape(shape,order='F').copy();self.cursor+=size
        if not np.all(np.isfinite(x)):raise ValueError('nonfinite native packet')
        return x
    def end(self):
        if self.cursor!=len(self.data):raise ValueError('native packet trailing/layout bytes')


def packet(root,stage,rank,cycle=2):
    r=Reader(root/'pilot'/f'c{cycle}_{stage}.rank{rank}');h=r.take('<i8',(16,));npwx,nnpw,nb,npol=map(int,h[5:9])
    if h[2]!={'local0':0,'local1':1,'before':2,'after':3,'summary':4,'complete':5,'residual':6}[stage] or not 0<nnpw<=npwx<=10827:raise ValueError('native stage/extent')
    if h[13]!=cycle:raise ValueError('native source cycle')
    if h[0]!=7025101408 or h[1]!=1 or h[3]!=rank or (nb,npol,h[9],h[10],h[11],h[12])!=(176,2,1,1,2,144):raise ValueError('native header domain')
    v=dict(header=h,npwx=npwx,nnpw=nnpw)
    matrix=lambda n:r.take('<c16',(npwx*2,n))
    if stage=='before':
        v.update(extents=r.take('<i8',(10,)),B=r.take('<f8',(3,3)),k=r.take('<f8',(3,)),scalars=r.take('<f8',(4,)),
            G=r.take('<i8',(3,nnpw)).T,et=r.take('<f8',(176,)),wg=r.take('<f8',(176,)),phi=matrix(176),direct=matrix(176),gram=r.take('<c16',(176,176)))
    elif stage=='after':
        v.update(energy=r.take('<f8',(1,)),xi=matrix(176),ace=matrix(176),gram=r.take('<c16',(176,176)),probe=matrix(6),direct_probe=matrix(6))
    elif stage in ['local0','local1']:
        dim=r.take('<i8',(8,));nr,ns,ng,nsg,nv=map(int,dim[:5]);assert ns==nsg==4
        v.update(dim=dim,density_G=r.take('<i8',(3,ng)).T,probe=matrix(6),action=matrix(6),rhoR=r.take('<f8',(nr,ns)),rhoG=r.take('<c16',(ng,nsg)),vrs=r.take('<f8',(nv,4)))
    elif stage in ['summary','residual']:v['scalars']=r.take('<f8',(5,))
    elif stage!='complete':raise ValueError('unknown stage')
    r.end();return v


def relative(x,y):return float(np.linalg.norm(x-y)/max(1.,np.linalg.norm(x),np.linalg.norm(y)))


def validate_cycle(member,cycle,pair_root=PAIR):
    root=Path(pair_root)/member;records={s:[packet(root,s,r,cycle) for r in [0,1]] for s in ['before','after','local0','local1','summary']}
    ranks=json.loads((root/'RANKS.json').read_text());gram=np.zeros((176,176),complex);acegram=gram.copy();norm=gram.copy();refX=np.zeros((6,6),complex);localshift=refX.copy();refnorm=refX.copy()
    local_total=np.zeros((6,6),complex)
    action_num=0.;action_den=0.;wave_error=0.;seen=set();normpadding=0.
    wave=root/'out/r07hse8.save/wfc1.hdf5';wf,G,k=read_spinors(wave);assert len(wf)==176 and len(G)==10827 and max(abs(k))<1e-12
    lookup={tuple(g):i for i,g in enumerate(G)}
    rr=Reader(root/'reference.bin');head=rr.take('<i8',(4,));assert tuple(head)==(70251406,7809,6,1)
    sourceB=rr.take('<f8',(3,3));sourcek=rr.take('<f8',(3,));sourceG=rr.take('<i8',(3,7809)).T;sourceC=rr.take('<c16',(15618,6));rr.end()
    reference={tuple(g):i for i,g in enumerate(sourceG)};found=set()
    for rank in [0,1]:
        b=records['before'][rank];a=records['after'][rank];lo=records['local0'][rank];hi=records['local1'][rank]
        for stage in records:
            assert records[stage][rank]['header'][4]==ranks[str(rank)]['pid']
            assert records[stage][rank]['npwx']==b['npwx'] and records[stage][rank]['nnpw']==b['nnpw']
        np.testing.assert_allclose(b['B'],sourceB,rtol=0,atol=1e-12);np.testing.assert_array_equal(b['k'],sourcek)
        assert abs(b['scalars'][1]-.25)<1e-12 and abs(b['scalars'][2]-200)<1e-10
        assert tuple(b['extents'][:3])==(60,60,60) and tuple(lo['dim'][5:])==(60,60,60)
        np.testing.assert_array_equal(lo['probe'],hi['probe']);np.testing.assert_array_equal(lo['probe'],a['probe'])
        # Compare bytes, including signed zero, rather than only numerical equality.
        for field in ['rhoR','rhoG','density_G']:
            assert lo[field].dtype==hi[field].dtype and lo[field].shape==hi[field].shape and lo[field].tobytes()==hi[field].tobytes()
        n,p=b['nnpw'],b['npwx'];active=np.r_[np.arange(n),np.arange(p,p+n)]
        pad=np.setdiff1d(np.arange(p*2),active)
        for field in ['phi','direct']:normpadding=max(normpadding,float(np.linalg.norm(b[field][pad])))
        for field in ['ace','xi']:normpadding=max(normpadding,float(np.linalg.norm(a[field][pad])))
        target=np.array([lookup[tuple(g)] for g in b['G']]);assert not(seen&set(map(tuple,b['G'])));seen.update(map(tuple,b['G']))
        native=b['phi'][active].reshape(2,n,176).transpose(2,0,1)
        if cycle==2:
            wave_error=max(wave_error,float(np.max(abs(native-wf[:,:,target]))));assert native.tobytes()==np.ascontiguousarray(wf[:,:,target]).tobytes()
        expected=np.zeros((p*2,6),complex)
        for i,g in enumerate(b['G']):
            if tuple(g) in reference:
                j=reference[tuple(g)];expected[i]=sourceC[j];expected[i+p]=sourceC[j+7809];found.add(tuple(g))
        np.testing.assert_array_equal(expected,a['probe'])
        phi=b['phi'][active];d=b['direct'][active];ac=a['ace'][active];probe=a['probe'][active]
        norm+=phi.conj().T@phi;gram+=phi.conj().T@d;acegram+=phi.conj().T@ac
        refnorm+=probe.conj().T@probe;refX+=probe.conj().T@a['direct_probe'][active]
        localshift+=probe.conj().T@(hi['action'][active]-lo['action'][active])
        local_total+=probe.conj().T@hi['action'][active]
        action_num+=np.linalg.norm(d-ac)**2;action_den+=max(np.linalg.norm(d)**2,np.linalg.norm(ac)**2)
    assert len(seen)==10827 and len(found)==7809 and normpadding<=1e-12
    assert np.linalg.norm(norm-np.eye(176),2)<1e-8 and np.linalg.norm(refnorm-np.eye(6),2)<1e-8
    for rank in [0,1]:
        np.testing.assert_array_equal(records['before'][rank]['gram'],records['before'][0]['gram'])
        assert relative(gram,records['before'][rank]['gram'])<=1e-8 and relative(acegram,records['after'][rank]['gram'])<=1e-8
    action_error=float(np.sqrt(action_num/max(1.,action_den)));gram_error=relative(gram,acegram)
    assert action_error<=1e-8 and gram_error<=1e-8 and relative(gram,gram.conj().T)<=1e-8
    eig=np.linalg.eigvalsh((gram+gram.conj().T)/2);assert max(eig)<=1e-8*max(1.,max(abs(eig)))
    wg=records['before'][0]['wg'];energy=float(wg@np.real(np.diag(gram)));summary=records['summary'][0]['scalars']
    for rank in [0,1]:
        np.testing.assert_array_equal(records['summary'][rank]['scalars'],summary)
        for v in [records['before'][rank]['scalars'][3],records['after'][rank]['energy'][0],summary[1],2*summary[0]]:
            assert abs(v-energy)<=1e-8*max(1.,abs(energy))
    t=ET.parse(root/'out/r07hse8.save/data-file-schema.xml');b=t.find('.//output/band_structure');ks=b.findall('ks_energies');assert len(ks)==1
    et=records['before'][0]['et'];occ_native=wg
    assert abs(sum(occ_native)-144)<=1e-8
    # Monotone FD consistency root from actual captured all-band spectrum.
    left=float(min(et)-1);right=float(max(et)+1)
    for _ in range(90):
        middle=(left+right)/2
        if sum(expit((middle-et)/.001))<144:left=middle
        else:right=middle
    ef_reconstructed=(left+right)/2;fd_source=expit((ef_reconstructed-et)/.001)
    assert abs(sum(fd_source)-144)<=1e-8 and max(abs(fd_source-occ_native))<=1e-9
    if cycle==2:
        ee=np.fromstring(ks[0].findtext('eigenvalues'),sep=' ')*2;occ=np.fromstring(ks[0].findtext('occupations'),sep=' ');ef=float(b.findtext('fermi_energy'))*2
        fd=expit((ef-ee)/.001);charge=float(sum(fd));assert abs(charge-144)<=1e-8 and max(abs(fd-occ))<=1e-9
        np.testing.assert_allclose(ee,et,rtol=0,atol=2e-14);np.testing.assert_allclose(occ,wg,rtol=0,atol=2e-14)
    else:charge=float(sum(occ_native))
    assert t.findtext('.//output/convergence_info/scf_conv/convergence_achieved')=='false'
    scferror=float(summary[3]);assert 0<=scferror<=1e-9 and summary[4]>=1 and summary[4]==int(summary[4])
    if cycle==2:assert abs(float(t.findtext('.//output/convergence_info/scf_conv/scf_error'))*2-scferror)<=2e-14
    assert t.findtext('.//input/dft/functional')=='HSE' and int(t.findtext('.//output/symmetries/nsym'))==24
    text=(root/'pw.out').read_text();assert text.count('R07_RELAX_SOURCE_OPERATOR')==2 and 'R07_ONE_RELAXATION_PUNCH_COMPLETE; HSE_NOT_CONVERGED' in text and 'JOB DONE.' in text
    result=dict(scientific_pass=True,source_wave_bitwise_readback=cycle==2,source_cycle=cycle,fixed_reference_exact=True,frozen_rhoR_rhoG_bitwise=True,
        charge_residual_e=charge-144,source_scf_error_Ry=scferror,source_scf_steps=int(summary[4]),reconstructed_consistency_fermi_Ry=ef_reconstructed,occupation_max_consistency_error=float(max(abs(fd_source-occ_native))),
        direct_ACE_action_relative=action_error,direct_ACE_Gram_relative=gram_error,source_wave_max_error=wave_error,
        source_Gram_defect_op=float(np.linalg.norm(norm-np.eye(176),2)),native_unhalved_Fock_Ry=energy,native_half_Fock_Ry=float(summary[0]),
        native_first_activation_total_Ry=float(summary[2]),source_mean_operator_change_Ry=dict(exchange=[float(np.trace(refX[:2,:2]).real/2),float(np.trace(refX[2:,2:]).real/4)],local=[float(np.trace(localshift[:2,:2]).real/2),float(np.trace(localshift[2:,2:]).real/4)]),
        global_plane_waves=10827,native_EXX_FFT=[60,60,60],aggregate_EXX_buffer_B=sum(int(np.prod(v['extents'][4:7]))*16 for v in records['before']),
        HSE_converged=False,source_spectra_not_rebuilt_self_consistent_HSE_quasiparticles=True,physical_xc=None)
    np.savez(HERE/(member+'_c'+str(cycle)+'_matrices.npz'),exchange=refX,local=localshift,local_total=local_total,direct_Gram=gram,ACE_Gram=acegram,source_Gram=norm,reference_Gram=refnorm)
    (HERE/(member+'_c'+str(cycle)+'_science.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result


def validate_native(member,pair_root=PAIR):
    root=Path(pair_root)/member
    phases={str(c):validate_cycle(member,c,pair_root) for c in [1,2]}
    residual=[packet(root,'residual',r,2)['scalars'] for r in [0,1]]
    np.testing.assert_array_equal(residual[0],residual[1])
    f0,f1,f2,dexx,raw=residual[0]
    assert abs(f0-phases['1']['native_unhalved_Fock_Ry'])<=1e-8*max(1.,abs(f0))
    assert abs(f2-phases['2']['native_unhalved_Fock_Ry'])<=1e-8*max(1.,abs(f2))
    assert abs(raw-(f1-.5*(f0+f2)))<=1e-12 and raw>=-1e-8*max(1.,abs(f0),abs(f2))
    assert abs(dexx-abs(raw))<=1e-12
    ranks=json.loads((root/'RANKS.json').read_text())
    for rank in [0,1]:assert packet(root,'complete',rank,2)['header'][4]==ranks[str(rank)]['pid']
    assert not any((root/'pilot').glob('c3_*'))
    result=dict(scientific_pass=True,source_cycles=phases,one_hybrid_inner_update=True,
                Fock_old_old_Ry=float(f0),Fock_old_new_Ry=float(f1),Fock_new_new_Ry=float(f2),
                native_dexx_Ry=float(dexx),raw_dexx_Ry=float(raw),HSE_converged=False,
                final_orbitals_solve_first_ACE_not_rebuilt_second_operator=True,physical_xc=None)
    (HERE/(member+'_science.json')).write_text(json.dumps(result,indent=2)+'\n')
    return result
