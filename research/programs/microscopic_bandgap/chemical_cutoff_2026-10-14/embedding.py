"""Nested NC plane-wave isometry, never an index-based overlap/truncation."""
import numpy as np


def embed_same_cell(frame, source_G, source_k, source_B, target_G, target_k, target_B):
    c=np.asarray(frame,complex);gs=np.asarray(source_G);gt=np.asarray(target_G)
    ks=np.asarray(source_k,float);kt=np.asarray(target_k,float)
    Bs=np.asarray(source_B,float);Bt=np.asarray(target_B,float)
    if Bs.shape!=(3,3) or Bt.shape!=(3,3) or not np.all(np.isfinite(Bs)) or not np.all(np.isfinite(Bt)):
        raise ValueError('finite physical reciprocal matrices required')
    if np.max(abs(Bs-Bt))>1e-12 or abs(np.linalg.det(Bs))<1e-12:
        raise ValueError('different physical reciprocal cell/axes')
    if ks.shape!=(3,) or kt.shape!=(3,) or np.max(abs(ks-kt))>1e-12:
        raise ValueError('different physical Bloch momentum')
    for g in [gs,gt]:
        if g.ndim!=2 or g.shape[1]!=3 or not np.all(np.isfinite(g)) or not np.all(g==np.rint(g)) or len({tuple(v) for v in g})!=len(g):
            raise ValueError('unique finite integer reciprocal labels required')
    if c.ndim!=3 or c.shape[1:]!=(2,len(gs)) or not np.all(np.isfinite(c)):
        raise ValueError('finite NC spinor coefficients required')
    F=c.reshape(len(c),-1);gram=F.conj()@F.T
    if np.linalg.norm(gram-np.eye(len(c)),2)>1e-8:raise ValueError('source NC Gram gate')
    lookup={tuple(v):i for i,v in enumerate(gt)}
    try:index=np.array([lookup[tuple(v)] for v in gs])
    except KeyError as error:raise ValueError('target omits source physical plane wave') from error
    if np.max(abs((gs+ks)@Bs-(gt[index]+kt)@Bt))>1e-12:
        raise ValueError('physical momentum mapping mismatch')
    out=np.zeros((len(c),2,len(gt)),complex);out[:,:,index]=c
    newgram=out.reshape(len(c),-1).conj()@out.reshape(len(c),-1).T
    if np.max(abs(newgram-gram))>1e-12:raise ValueError('zero-fill Gram changed')
    mask=np.ones(len(gt),bool);mask[index]=False
    return out,index,dict(source_PW=len(gs),target_PW=len(gt),new_only_PW=int(mask.sum()),
        all_source_labels_present=True,max_Gram_change=float(np.max(abs(newgram-gram))),
        source_Gram_defect_op=float(np.linalg.norm(gram-np.eye(len(c)),2)),
        new_only_coefficient_max=float(np.max(abs(out[:,:,mask]))) if np.any(mask) else 0.,
        physical_axes_match=True,source_norm_discarded=0.,renormalization_used=False)
