"""Geometry and bounded periodic valence-density partitions of accepted sources."""
import itertools
import json,sys
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from scipy.special import logsumexp
from packets import packet
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent
WIDTHS_A=[.5,.75,1.]

def intake(member,cycle):
    root=r.PAIR/member;t=ET.parse(root/'out/r07hse8.save/data-file-schema.xml')
    structure=t.find('.//output/atomic_structure')
    cell=np.array([np.fromstring(structure.findtext('cell/a'+str(i)),sep=' ') for i in [1,2,3]])
    volume=abs(np.linalg.det(cell));atoms=structure.findall('atomic_positions/atom')
    names=[v.attrib['name'] for v in atoms]
    positions=np.array([np.fromstring(v.text,sep=' ') for v in atoms]);fractional=positions@np.linalg.inv(cell)
    assert len(names)==8 and sum(v=='Te' for v in names)==4
    fields=[];labels=[];magR=0.;magG=0.
    for rank in [0,1]:
        p=packet(root,'local1',rank,cycle);assert tuple(p['dim'][5:])==(60,60,60)
        fields.append(p['rhoG'][:,0]);labels.append(p['density_G'])
        magR=max(magR,float(np.max(abs(p['rhoR'][:,1:]))))
        magG=max(magG,float(np.max(abs(p['rhoG'][:,1:]))))
    G=np.concatenate(labels);density=np.concatenate(fields)
    assert len(G)==86791 and len(set(map(tuple,G)))==len(G)
    idx=np.mod(G,60);assert len(set(map(tuple,idx)))==len(G)
    table=np.zeros((60,60,60),complex);table[tuple(idx.T)]=density
    actual=np.fft.ifftn(table)*60**3
    assert np.max(abs(actual.imag))<1e-10
    charge=float(np.mean(actual.real)*volume);assert abs(charge-144)<1e-8
    return cell,fractional,names,actual.real,charge,float(max(abs(actual.imag).ravel())),dict(max_stored_rhoR_magnetization=magR,max_stored_rhoG_magnetization=magG)

def coordination(cell,positions,names):
    result=[]
    for i,name in enumerate(names):
        if name!='Te':continue
        candidates=[]
        for j,species in enumerate(names):
            if species=='Te':continue
            for shift in itertools.product([-1,0,1],repeat=3):
                vector=(positions[j]+np.array(shift)-positions[i])@cell
                candidates.append((float(np.linalg.norm(vector)),j,species,list(shift)))
        candidates.sort();near=candidates[:4]
        assert max(v[0] for v in near)-min(v[0] for v in near)<1e-8
        assert candidates[4][0]>1.2*near[-1][0]
        result.append(dict(Te_atom_1based=i+1,N_Cd=sum(v[2]=='Cd' for v in near),nearest_cations=[dict(atom_1based=v[1]+1,species=v[2],cell_image=v[3],distance_Bohr=v[0]) for v in near]))
    return result

def windows(cell,positions):
    assert np.max(abs(cell-np.eye(3)*cell[0,0]))<1e-9
    f=np.moveaxis(np.indices((60,60,60)),0,-1).reshape(-1,3)/60
    angles=2*np.pi*(f[None,:,:]-positions[:,None,:])
    cos=np.sum(np.cos(angles),axis=2)
    result={}
    for width in WIDTHS_A:
        kappa=(6.46/(2*np.pi*width))**2
        logits=kappa*cos;w=np.exp(logits-logsumexp(logits,axis=0))
        assert max(abs(np.sum(w,axis=0)-1))<2e-15
        result[str(width)]=w
    return result

def main(selected=('host','cd')):
    members={};fields={};partition={};frame=None
    for member in selected:
        final=json.loads((r.PAIR/member/'FINAL.json').read_text());assert final['accepted']
        last=final['science']['last_cycle'];members[member]=dict(cycles={},last_source=last)
        for cycle in sorted({1,last}):
            cell,pos,names,rho,charge,imag,mag=intake(member,cycle)
            if frame is None:frame=(cell.copy(),pos.copy());partition=windows(cell,pos)
            else:np.testing.assert_array_equal(cell,frame[0]);np.testing.assert_array_equal(pos,frame[1])
            values={key:(w@rho.ravel()*abs(np.linalg.det(cell))/60**3).tolist() for key,w in partition.items()}
            for v in values.values():assert abs(sum(v)-charge)<1e-10
            members[member]['cycles'][str(cycle)]=dict(valence_charge_e=charge,Fourier_imaginary_max=imag,local_spin_density=mag,minimum_valence_density_Bohr_minus3=float(np.min(rho)),periodic_window_charges_e=values)
            fields[(member,cycle)]=rho
        members[member]['coordination']=coordination(cell,pos,names)
    contrasts={}
    for key in partition if set(selected)=={'host','cd'} else []:
        def charges(m,c):return np.array(members[m]['cycles'][str(c)]['periodic_window_charges_e'][key])
        contrasts[key]=dict(preliminary_Cd_minus_host_e=(charges('cd',1)-charges('host',1)).tolist(),
            final_Cd_minus_host_e=(charges('cd',members['cd']['last_source'])-charges('host',members['host']['last_source'])).tolist(),
            HSE_relaxation_Cd_minus_host_e=((charges('cd',members['cd']['last_source'])-charges('cd',1))-(charges('host',members['host']['last_source'])-charges('host',1))).tolist())
        for v in contrasts[key].values():assert abs(sum(v))<2e-8
    x=.25;bernoulli=[float(__import__('math').comb(4,N)*x**N*(1-x)**(4-N)) for N in range(5)]
    result=dict(status='CALCULATED actual reciprocal valence density and exact periodic geometry',members=members,
                density_partition_contrasts=contrasts,widths_A=WIDTHS_A,
                windows='positive smooth periodic von-Mises site partition; near-site length parameter, sum to one on actual60^3 density grid',
                pseudovalence_density_only=True,not_Bader_or_unique_atomic_charge=True,no_continuum_quadrature_or_material_error_claim=True,
                random_x025_N_probabilities=bernoulli,
                relaxation_window_charge_e={m:{key:(np.array(members[m]['cycles'][str(members[m]['last_source'])]['periodic_window_charges_e'][key])-np.array(members[m]['cycles']['1']['periodic_window_charges_e'][key])).tolist() for key in partition} for m in members},
                physical_xc=None,not_random_alloy_or_dilute_impurity=True)
    if 'cd' in members:assert all(v['N_Cd']==1 for v in members['cd']['coordination'])
    assert all(v['N_Cd']==0 for v in members['host']['coordination'])
    tag='' if len(selected)==2 else selected[0]+'_'
    (HERE/(tag+'coordination_and_density.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(contrasts=contrasts,relaxation_window_charge_e=result['relaxation_window_charge_e'],random_N_probabilities=bernoulli),indent=2))

if __name__=='__main__':main(tuple(sys.argv[1:]) or ('host','cd'))
