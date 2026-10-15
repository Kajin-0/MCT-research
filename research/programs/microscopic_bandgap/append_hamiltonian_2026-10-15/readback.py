"""Fail-closed same-state append splice and full-vector symmetry validation."""
from pathlib import Path
import json
import numpy as np
from accepted import HERE,PRIVATE,decode,frames,global_indices,td_operations,sha


def validate_native(root):
    if (HERE/'native_science.json').exists():raise FileExistsError('preserve original append verdict')
    f,basis,G,Q,L,V=frames();B=np.column_stack((Q,L));C=V.conj().T@B;N=len(G)
    ranks=json.loads((root/'RANKS.json').read_text());HB=np.zeros_like(B);componentB={k:np.zeros((304,304),complex) for k in ['kin','loc','nl','fock']};seen=set();maxcontrol=0.
    field_checks=['dims','fft','B','k','scalars','bounds','energies','G','density_G','wg','source','rhoG','rhoR','vrs'];parity={k:True for k in field_checks};query=np.column_stack((L,f['trial'][:,152:]))
    kinetic=0.;qcontrol=0.
    for rank in [0,1]:
        old=decode(PRIVATE/'p1/host/pilot'/f'H.rank{rank}');new=decode(root/'pilot'/f'H.rank{rank}');assert new['h'][2]==rank and new['h'][3]==ranks[str(rank)]['pid']
        assert np.array_equal(old['h'][4:],new['h'][4:])
        for key in field_checks:
            assert old[key].tobytes()==new[key].tobytes(),'SAME-D BYTE REFUSAL: '+key
        i,j=global_indices(new,G);assert not seen.intersection(map(tuple,new['G']));seen.update(map(tuple,new['G']))
        assert new['trial'][i].tobytes()==np.ascontiguousarray(query[j]).tobytes(),'append trial bytes'
        for k in ['trial','kin','loc','nl','fock']:
            assert old[k][:,152:].tobytes()==new[k][:,152:].tobytes(),'physical probe byte refusal '+k
        assert old['control'].tobytes()==new['control'].tobytes(),'native hpsi controls differ'
        expected=(G@new['B'].T);T=np.tile(np.sum(expected**2,axis=1),2);kinetic=max(kinetic,float(np.max(abs(new['kin'][i]-T[j,None]*query[j]))));assert kinetic<1e-10
        oldH=sum(old[k][i,:152] for k in componentB);newH=sum(new[k][i,:152] for k in componentB);HB[j,:152]=oldH;HB[j,152:]=newH
        for k in componentB:
            componentB[k][:,:152]+=B[j].conj().T@old[k][i,:152];componentB[k][:,152:]+=B[j].conj().T@new[k][i,:152]
        direct=sum(new[k][i,152:158] for k in componentB);control=new['control'][i];maxcontrol=max(maxcontrol,float(np.linalg.norm(direct-control,'fro')/max(1.,np.linalg.norm(control,'fro'))))
        qcontrol=max(qcontrol,float(np.max(abs(new['bounds'][9]-144))))
    assert len(seen)==N and maxcontrol<1e-8 and qcontrol<1e-8
    assert np.linalg.norm(B.conj().T@B-np.eye(304),2)<1e-8
    HV=np.linalg.solve(C.T,HB.T).T;H=V.conj().T@HV;scale=max(1.,float(np.linalg.norm(H,2)))
    reciprocity=float(np.linalg.norm(componentB['kin'][:152,152:]+componentB['loc'][:152,152:]+componentB['nl'][:152,152:]+componentB['fock'][:152,152:]-(L.conj().T@HB[:,:152]).conj().T,'fro')/scale)
    herm=float(np.linalg.norm(H-H.conj().T,'fro')/scale);assert max(reciprocity,herm)<1e-8
    # Independent coordinate assembly using complete component contractions.
    Ci=np.linalg.inv(C);components={k:Ci.conj().T@M@Ci for k,M in componentB.items()}
    component_error=float(np.linalg.norm(sum(components.values())-H,'fro')/scale);assert component_error<1e-8
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    def rotate(A,op):
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);out=np.empty_like(A).reshape(2,N,A.shape[1]);out[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],A.reshape(2,N,A.shape[1]));return out.reshape(A.shape)
    cov=[];space=[]
    for op in td_operations():
        rotated=rotate(V,op);U=V.conj().T@rotated;space.append(float(np.linalg.norm(rotated-V@U,'fro')));cov.append(float(np.linalg.norm(rotate(HV,op)-HV@U,'fro')/scale))
    U=V.conj().T@theta(V);tr=float(np.linalg.norm(theta(HV)-HV@U,'fro')/scale);space.append(float(np.linalg.norm(theta(V)-V@U,'fro')))
    translations=[]
    for a,b in [(0,1),(0,2),(1,2)]:
        phase=np.tile((-1.)**((G[:,a]+G[:,b])%2),2);U=V.conj().T@(phase[:,None]*V);translations.append(float(np.linalg.norm(phase[:,None]*HV-HV@U,'fro')/scale))
    assert max(cov+[tr]+space+translations)<1e-8
    cached=json.loads((HERE.parent/'same_density_hamiltonian_2026-10-15/native_science.json').read_text());assert abs(cached['native_charge_e']-144)<1e-8
    out=PRIVATE/'p2/assembled_actions.npz';np.savez(out,HV=HV,H=H,**{'H_'+k:M for k,M in components.items()})
    reduced=HERE/'native_matrices.npz';np.savez(reduced,H=H,**{'H_'+k:M for k,M in components.items()})
    result=dict(scientific_pass=True,same_D_complete_state_bitwise=parity,physical_probe_components_and_full_hpsi_bitwise_equal=True,query_source_independent=True,new_native_query_columns=152,cached_native_columns_reused=152,total_Galerkin_dimension=304,exact_accepted_ELF_reused=True,native_charge_e=cached['native_charge_e'],trial_entropy_kB=cached['trial_entropy_kB'],kinetic_max_abs_Ry=kinetic,native_hpsi_component_relative=maxcontrol,cross_block_reciprocity_relative=reciprocity,Hermiticity_relative_F=herm,independent_component_assembly_relative=component_error,all24_Td_full_action_covariance_relative=cov,Theta_full_action_covariance_relative=tr,translations_full_action_covariance_relative=translations,maximum_joint_space_leakage_F=max(space),assembled_action_path=str(out),assembled_action_sha256=sha(out),no_new_D_or_SCF=True,HSE_converged=False,physical_xc=None)
    (HERE/'native_science.json').write_text(json.dumps(result,indent=2)+'\n');return result
