#!/usr/bin/env python3
"""Plot frozen coarse-host evidence and the blind exchange-component test."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    data = json.loads((ROOT/'data/calculated/static_hse_binary_gate_20261010.json').read_text())
    record = data['completed_controls']['hgte_coarse_quartet']
    frozen = record['qzero']
    growth = record['feedback_growth']
    history = frozen['printed_gamma_history']
    steps = np.array([row['printed_step'] for row in history])
    energies = np.array([row['quartet_energies_eV'] for row in history])
    centered = (energies-energies.mean(axis=1)[:,None])*1000
    fig,axes = plt.subplots(1,3,figsize=(13.4,3.8),layout='constrained')
    for i,color in enumerate(['#173f6b','#628db6','#c87218','#edaf64']):
        axes[0].plot(steps,centered[:,i],'-o',color=color,markersize=3)
    axes[0].set(xlabel='Printed SCF step (0: PBE)',ylabel='Quartet energy from its mean (meV)',
                title='Unaccepted q2 HgTe host')
    norms = np.array([row['traceless_occupation_norm'] for row in growth['history']])
    axes[1].semilogy(steps[1:],norms[1:],'o-',color='#173f6b',label='Native occupation norm')
    gain = growth['predicted_cold_iteration_gain']
    linear_steps = np.arange(1,4)
    axes[1].semilogy(linear_steps,norms[1]*gain**(linear_steps-1),'--',color='#c87218',
                      label=f'Source gain {gain:.3f}')
    axes[1].set(xlabel='Printed SCF step',ylabel='Traceless occupation norm',
                title='Early gain, without coefficient fitting')
    axes[1].legend(fontsize=8,loc='lower right')
    kernels = frozen['qzero_component_predictions']
    values = [k['qzero_coefficient_eV']*1000 for k in kernels]
    threshold = 1000/frozen['native_cold_half_occupation']['minus_df_dE_eV_inverse']
    axes[2].bar(['q2','q4'],values,color=['#173f6b','#c87218'],width=.55)
    axes[2].set_yscale('log')
    axes[2].axhline(threshold,color='gray',linestyle='--',linewidth=1,
                    label=f'Isolated linear threshold: {threshold:.2f} meV')
    for i,value in enumerate(values):
        axes[2].text(i,value*1.15,f'{value:.3f}',ha='center',fontsize=9)
    axes[2].set(ylabel='J0 (meV)',ylim=(2,650),title='Specified numerical exchange component')
    axes[2].legend(fontsize=8,loc='upper right')
    for ax in axes:
        ax.grid(axis='y',alpha=.2)
        ax.spines[['top','right']].set_visible(False)
    output = ROOT/'research/programs/microscopic_bandgap/figures/hgte_quartet_feedback'
    for suffix in ['png','pdf','svg']:
        fig.savefig(output.with_suffix('.'+suffix),dpi=180)
    print(str(output.with_suffix('.pdf')))


if __name__ == '__main__':
    main()
