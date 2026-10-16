"""Exact legacy Reader class; isolated minimal dependencies."""
from pathlib import Path
import numpy as np

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
