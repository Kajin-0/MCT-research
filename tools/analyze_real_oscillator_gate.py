#!/usr/bin/env python3
"""Gate one- versus two-scale Bose representations on real specimen data."""
import csv,itertools,json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
THETA=(5.,10.,15.,20.,30.,40.,60.,80.,120.,160.,240.,320.,480.)


def load():
    out={}
    with (ROOT/'data/experimental/seiler1990_figure7_digitized.csv').open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    out['Seiler']=[(f"S{r['sample_number']}",float(r['composition_x_reported']),float(r['temperature_k_digitized']),float(r['gap_mev_digitized'])) for r in rows]
    with (ROOT/'data/experimental/laurenti1990_figure2_cd_rich_digitized.csv').open(newline='',encoding='utf-8') as f:
        rows=[r for r in csv.DictReader(f) if r['point_kind']=='digitized_full_square']
    out['Laurenti']=[(r['sample_id'],float(r['composition_x']),float(r['temperature_k']),float(r['shift_from_2k_mev'])) for r in rows]
    return out


def bose(t,theta): return 2/np.expm1(theta/np.asarray(t,float))


def fit(rows,scales):
    sample=np.array([r[0] for r in rows]);x=np.array([r[1] for r in rows]);t=np.array([r[2] for r in rows]);y=np.array([r[3] for r in rows])
    names=sorted(set(sample));center=float(np.mean(x));X=np.zeros((len(rows),len(names)+2*len(scales)))
    for j,name in enumerate(names): X[:,j]=sample==name
    col=len(names)
    for theta in scales:
        shape=bose(t,theta);X[:,col]=shape;X[:,col+1]=(x-center)*shape;col+=2
    coefficient=np.linalg.lstsq(X,y,rcond=None)[0];residual=X@coefficient-y
    return {'names':names,'center':center,'scales':scales,'coefficient':coefficient,'rmse':float(np.sqrt(np.mean(residual**2))),'max':float(np.max(abs(residual))),'condition':float(np.linalg.cond(X))}


def select(rows,count):
    scales=[(v,) for v in THETA] if count==1 else list(itertools.combinations(THETA,2))
    return min((fit(rows,s) for s in scales),key=lambda model:(model['rmse'],model['max'],model['condition']))


def predict(model,rows,profile_offset):
    sample=np.array([r[0] for r in rows]);x=np.array([r[1] for r in rows]);t=np.array([r[2] for r in rows]);y=np.array([r[3] for r in rows]);p=np.zeros(len(rows))
    for j,name in enumerate(model['names']): p+=model['coefficient'][j]*(sample==name)
    col=len(model['names'])
    for theta in model['scales']:
        shape=bose(t,theta);p+=model['coefficient'][col]*shape+model['coefficient'][col+1]*(x-model['center'])*shape;col+=2
    if profile_offset:
        for name in set(sample)-set(model['names']):
            mask=sample==name;p[mask]+=np.mean(y[mask]-p[mask])
    return p,y


def metric(p,y): return {'rmse_mev':float(np.sqrt(np.mean((p-y)**2))),'max_abs_mev':float(np.max(abs(p-y)))}


def specimen_holdout(rows,count):
    names=sorted(set(r[0] for r in rows));all_prediction=[];all_observed=[];conditions=[];selected=[]
    for name in names:
        training=[r for r in rows if r[0]!=name];testing=[r for r in rows if r[0]==name];model=select(training,count);p,y=predict(model,testing,True)
        all_prediction.extend(p);all_observed.extend(y);conditions.append(model['condition']);selected.append(list(model['scales']))
    return {'aggregate':metric(np.array(all_prediction),np.array(all_observed)),'selected_theta_k':selected,'max_training_condition':max(conditions)}


def temperature_holdout(source,rows,count):
    t=np.array([r[2] for r in rows])
    masks=[t<=40,t>40] if source=='Seiler' else [t<=100,(t>100)&(t<=200),t>200]
    all_prediction=[];all_observed=[];conditions=[];selected=[]
    for mask in masks:
        training=[r for r,flag in zip(rows,mask,strict=True) if not flag];testing=[r for r,flag in zip(rows,mask,strict=True) if flag];model=select(training,count);p,y=predict(model,testing,False)
        all_prediction.extend(p);all_observed.extend(y);conditions.append(model['condition']);selected.append(list(model['scales']))
    return {'aggregate':metric(np.array(all_prediction),np.array(all_observed)),'selected_theta_k':selected,'max_training_condition':max(conditions)}


def analyze():
    result={'source_classes_pooled':False,'candidate_theta_k':list(THETA),'amplitude_degree':1,'classes':{}}
    for source,rows in load().items():
        result['classes'][source]={}
        for count,label in ((1,'one_scale'),(2,'two_scales')):
            result['classes'][source][label]={'all_data_rmse_mev':select(rows,count)['rmse'],'specimen_holdout':specimen_holdout(rows,count),'temperature_holdout':temperature_holdout(source,rows,count)}
    seiler=result['classes']['Seiler'];laurenti=result['classes']['Laurenti']
    if seiler['two_scales']['specimen_holdout']['aggregate']['rmse_mev']<=seiler['one_scale']['specimen_holdout']['aggregate']['rmse_mev']: raise RuntimeError('Seiler two-scale rejection failed')
    if seiler['two_scales']['temperature_holdout']['aggregate']['rmse_mev']<1000: raise RuntimeError('Seiler instability not detected')
    result['laurenti_specimen_holdout_improvement_mev']=laurenti['one_scale']['specimen_holdout']['aggregate']['rmse_mev']-laurenti['two_scales']['specimen_holdout']['aggregate']['rmse_mev']
    result['decision']='Two fixed scales reduce training residuals but are not identified by real specimens; retain a low-rank prediction envelope rather than two oscillator energies.'
    return result


if __name__=='__main__': print(json.dumps(analyze(),indent=2,sort_keys=True))
