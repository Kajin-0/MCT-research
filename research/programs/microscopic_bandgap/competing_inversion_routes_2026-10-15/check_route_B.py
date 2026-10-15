"""Exact small Kane Landau/current and causal optical-disorder checks.

All masses/fields/couplings below are synthetic model units, never material
coefficients or an x_c estimate. No QE/native/MPI execution or empirical fit.
"""
from pathlib import Path
import itertools
import json
import numpy as np
from scipy.integrate import quad

HERE=Path(__file__).resolve().parent
norm=lambda a:float(np.linalg.norm(a,2))


def kane_landau(M,B,N=8):
    ident=np.eye(N);zero=np.zeros((N,N))
    lower=np.diag(np.sqrt(np.arange(1,N)),1)
    upper=lower.T
    c=np.sqrt(3)/2
    H=np.block([[2*M*ident,c*np.sqrt(2*B)*upper,-.5*np.sqrt(2*B)*lower],
                [c*np.sqrt(2*B)*lower,zero,zero],
                [-.5*np.sqrt(2*B)*upper,zero,zero]])
    jx=np.block([[zero,c*ident,-.5*ident],[c*ident,zero,zero],[-.5*ident,zero,zero]])
    jy=np.block([[zero,1j*c*ident,.5j*ident],[-1j*c*ident,zero,zero],[-.5j*ident,zero,zero]])
    return H,jx+1j*jy,jx-1j*jy


def optical_line(M,B,n=1):
    H,jp,jm=kane_landau(M,B)
    energies,U=np.linalg.eigh(H)
    a=2*n+.5
    target=M+np.sqrt(M*M+a*B)
    idx=np.argmin(abs(energies-target))
    assert abs(energies[idx]-target)<1e-12
    dark=U[:,abs(energies)<1e-12]
    strengths=[float(np.linalg.norm(U[:,idx].conj()@j@dark)**2) for j in [jp,jm]]
    assert max(strengths)>1e-3
    return float(energies[idx]),sum(strengths),a


def mass(t1,t2,b1,b2):
    D=b2*t1-b1*t2
    assert D>0
    return (b2*t1*t1-b1*t2*t2)/(2*D)


def mass_budget(t,b,dt,db):
    t1,t2=t;b1,b2=b;d1,d2=dt;bb1,bb2=db
    assert b1>bb1 and b1+bb1<b2-bb2
    Q=b2*t1*t1-b1*t2*t2;D=b2*t1-b1*t2
    eQ=b2*(2*abs(t1)*d1+d1*d1)+b1*(2*abs(t2)*d2+d2*d2)
    eQ+=bb2*(abs(t1)+d1)**2+bb1*(abs(t2)+d2)**2
    eD=b2*d1+b1*d2+bb2*(abs(t1)+d1)+bb1*(abs(t2)+d2)
    assert D>eD
    mm=Q/(2*D)
    return mm,(eQ+2*abs(mm)*eD)/(2*(D-eD)),Q,eQ


def L(H):
    d=H.shape[0]
    return np.kron(np.eye(d),H)-np.kron(H.T,np.eye(d))


def third_budget(t1,b1,b3,d1,bb1,bb3,mh,em):
    ah=(t1*t1-2*mh*t1)/b1
    en=2*abs(t1)*d1+d1*d1+2*(abs(mh)*d1+(abs(t1)+d1)*em)
    ea=(en+abs(ah)*bb1)/(b1-bb1)
    amin,amax=ah-ea,ah+ea
    assert amin>0 and b3>bb3
    predicted=mh+np.sqrt(mh*mh+ah*b3)
    error=2*em+((b3+bb3)*ea+amax*bb3)/(2*np.sqrt(amin*(b3-bb3)))
    return predicted,error,ah,ea


def main():
    fields=[1.,4.,9.];rows=[]
    for M in [-.2,0.,.2]:
        lines=[optical_line(M,B) for B in fields]
        t=[line[0] for line in lines]
        extracted=mass(t[0],t[1],*fields[:2]);a=lines[0][2]
        assert abs(extracted-M)<1e-12
        a2=(t[0]**2-2*extracted*t[0])/fields[0]
        third=extracted+np.sqrt(extracted**2+a2*fields[2])
        assert abs(third-t[2])<1e-12
        worst=0.;maxratio=0.;thirdratio=0.;signs=[]
        for s in itertools.product([-1,1],repeat=4):
            dt=np.array([.001,.0015]);db=np.array([.0002,.0003])
            tt=np.array(t[:2])+dt*np.array(s[:2])
            bb=np.array(fields[:2])+db*np.array(s[2:])
            mh,err,Q,eQ=mass_budget(tt,bb,dt,db)
            assert abs(mh-M)<=err
            predicted3,e3,ah,ea=third_budget(tt[0],bb[0],fields[2],dt[0],db[0],.0004,mh,err)
            assert abs(a-ah)<=ea and abs(predicted3-t[2])<=e3
            thirdratio=max(thirdratio,abs(predicted3-t[2])/e3)
            if abs(Q)>eQ:
                assert np.sign(Q)==np.sign(M)
                signs.append(int(np.sign(Q)))
            worst=max(worst,abs(mh-M));maxratio=max(maxratio,abs(mh-M)/err)
        rows.append(dict(synthetic_M=M,fields=fields,transition_energies=t,
            actual_circular_current_strengths=[line[1] for line in lines],
            extracted_M=extracted,third_field_error=abs(third-t[2]),
            maximum_actual_noisy_mass_error=worst,maximum_fraction_of_bound=maxratio,
            maximum_third_field_fraction_of_bound=thirdratio,
            certified_signs=sorted(set(signs))))

    # Genuine Kane current, not assigned domain intensities.
    m=.4;mix=[];current=[];gvalues=[]
    for B in fields:
        tp,wp,a=optical_line(m,B);tm,wm,_=optical_line(-m,B)
        s=np.sqrt(m*m+a*B)
        centroid=(wp*tp+wm*tm)/(wp+wm)
        assert abs(centroid-(s+m*m/s))<1e-12
        gvalues.extend([wp/((1+m/s)/2),wm/((1-m/s)/2)])
        mix.append(s);current.append(centroid)
    assert np.ptp(gvalues)<1e-12
    mixture_M=mass(mix[0],mix[1],*fields[:2])
    current_M=mass(current[0],current[1],*fields[:2])
    assert mixture_M>0 and current_M>0
    aa=(mix[0]**2-2*mixture_M*mix[0])/fields[0]
    predicted3=mixture_M+np.sqrt(mixture_M**2+aa*fields[2])
    assert abs(predicted3-mix[2])>1e-4
    ac=(current[0]**2-2*current_M*current[0])/fields[0]
    pc=current_M+np.sqrt(current_M**2+ac*fields[2])

    # Finite window/tail bound against an independently specified positive line.
    values=np.array([1.,2.,4.]);weights=np.array([.1,.8,.1]);Eref=2.
    d=.9;n0=np.dot(weights[:2],values[:2]-Eref)
    t_win=Eref+n0/d;t_full=np.dot(weights,values)
    tail_bound=(.2+abs(t_win-Eref)*.1)/d
    assert abs(t_full-t_win)<=tail_bound

    # Same exact averaged one-particle Green functions, different optics.
    aval=.7;z=.12+.13j;Cmax=.4
    ensembles=[[(aval,-aval),(-aval,aval)],[(aval,aval),(-aval,-aval)]]
    greens=[];optics=[]
    j=np.array([[0.,1.],[1.,0.]])
    for ens in ensembles:
        gs=[];lines=[]
        for e1,e2 in ens:
            gs.append([quad(lambda c:(1/(z-c-e)).real,-Cmax,Cmax)[0]/(2*Cmax)
                       +1j*quad(lambda c:(1/(z-c-e)).imag,-Cmax,Cmax)[0]/(2*Cmax)
                       for e in [e1,e2]])
            H=np.diag([e1,e2]);ev,U=np.linalg.eigh(H)
            if ev[1]-ev[0]>1e-12:
                lines.append(dict(energy=float(ev[1]-ev[0]),strength=float(abs(U[:,1].conj()@j@U[:,0])**2)))
            else:
                assert norm(H@j-j@H)==0
        greens.append(np.mean(gs,axis=0));optics.append(lines)
    assert np.max(abs(greens[0]-greens[1]))<1e-13
    assert len(optics[0])==2 and not optics[1]
    assert all(x.imag<0 for x in greens[0])

    # Exact commutator quotient and independent weak-Liouvillian bound.
    H0=np.diag([.2,-.3]);W1=np.array([[0.,.005],[.005,0.]])
    W2=np.array([[.003,-.002j],[.002j,-.003]])
    WW=[W1,W2,-W1-W2]
    Ll=L(H0);LW=[L(w) for w in WW];eta=.2;zz=.4+1j*eta;ident=np.eye(4)
    R0=np.linalg.inv(zz*ident-Ll)
    Rav=sum(np.linalg.inv(zz*ident-Ll-lw) for lw in LW)/3
    BL=sum(lw@R0@lw for lw in LW)/3;RB=np.linalg.inv(zz*ident-Ll-BL)
    wL=max(norm(lw) for lw in LW);r=wL/eta
    bound=(r**3/(1-r)+r**4/(1-r*r))/eta
    err=norm(Rav-RB)
    assert 1e-12<err<=bound and norm(L(100*np.eye(2)))==0
    assert norm(L(H0+100*np.eye(2))-Ll)<1e-12
    assert np.linalg.eigvalsh(-(Rav-Rav.conj().T)/(2j)).min()>0
    # Common scalar shifts of any width destroy atoms for continuous laws,
    # yet the canonical transition/Liouvillian is unchanged exactly.
    out=dict(status='PASS',native_jobs=0,material_validation=False,physical_xc=None,
        all_values_synthetic_model_units=True,Landau_checks=rows,
        zero_mean_mass_mixture=dict(m=m,a=a,fields=fields,equal_weight_centers=mix,
            actual_current_centers=current,equal_weight_Mopt=mixture_M,
            actual_current_Mopt=current_M,current_geometry_factor_range=[min(gvalues),max(gvalues)],
            equal_weight_third_field_discrepancy=predicted3-mix[2],
            actual_current_third_field_discrepancy=pc-current[2]),
        finite_tail_centroid_error=abs(t_full-t_win),finite_tail_centroid_bound=tail_bound,
        same_G_different_optics=dict(g_difference=float(np.max(abs(greens[0]-greens[1]))),
            optical_transitions_A=optics[0],optical_transitions_B=optics[1],
            continuous_scalar_distribution=[-Cmax,Cmax]),
        Liouvillian=dict(active_contrast=wL,centered_noncommuting_configurations=3,
            r=r,exact_resolvent_error=err,
            certified_bound=bound,common_scalar_shift_annihilated=True))
    (HERE/'route_B_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
