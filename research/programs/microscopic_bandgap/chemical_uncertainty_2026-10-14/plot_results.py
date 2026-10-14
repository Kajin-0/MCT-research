"""Standalone data curves, no regression or native execution."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
j=json.loads((HERE/'grid_result.json').read_text())
rows=[r for r in j['rows'] if r['reference_kind']=='own_Fermi']
fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
x=[r['W_eV'] for r in rows]
for kind,label in [('original','Gamma only'),('new','2x2x2, native Td reduction')]:
    y=[r[kind]['delta_eV']*1000 for r in rows]
    lo=[r[kind]['conditional_interval_eV'][0]*1000 for r in rows]
    hi=[r[kind]['conditional_interval_eV'][1]*1000 for r in rows]
    line=axes[0].plot(x,y,'o-',label=label)[0]
    axes[0].fill_between(x,lo,hi,color=line.get_color(),alpha=.12)
axes[0].set(xlabel='Gaussian width W (eV)',ylabel='Cd-induced ordering response (meV)',title='Same original physical host projectors')
axes[0].legend(fontsize=9)
y=[r['k_grid_change_eV']*1000 for r in rows]
lo=[r['conditional_grid_difference_interval_eV'][0]*1000 for r in rows];hi=[r['conditional_grid_difference_interval_eV'][1]*1000 for r in rows]
axes[1].plot(x,y,'o-',color='black');axes[1].fill_between(x,lo,hi,color='grey',alpha=.2);axes[1].axhline(0,color='grey',linestyle='--')
axes[1].set(xlabel='Gaussian width W (eV)',ylabel='Refined minus original response (meV)',title='Measured method/grid sensitivity')
for ax in axes:ax.grid(alpha=.2)
fig.text(.5,-.03,'Conditional spectral/projector bounds exclude material and BZ-convergence errors. Lines connect samples; no fit.',ha='center',fontsize=9)
fig.savefig(HERE/'grid_comparison.png',dpi=160,bbox_inches='tight');fig.savefig(HERE/'grid_comparison.pdf',bbox_inches='tight');plt.close(fig)
