#!/usr/bin/env python3
"""Plot frozen native symmetry control and finer-pair resource estimates."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    data = json.loads((ROOT/'data/calculated/static_hse_binary_gate_20261010.json').read_text())
    control = data['completed_controls']['hgte_finer_quartet']['controls']
    resource = data['fixed_ion_impurity_pair']['finer_native_resource_gate']
    spans = [1000*row['final_quartet_spread_eV'] for row in control]
    memory = [resource[member]['estimated_total_dynamical_RAM_QE_GB'] for member in ['host', 'impurity']]
    physical = resource['host']['physical_memory_bytes']/1024**3
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.3))
    fig.subplots_adjust(top=.83, bottom=.23, wspace=.4)
    fig.suptitle('HgTe numerical reference: finer-grid symmetry and cell resource gate', fontsize=12)
    colors = ['#244b6f', '#c2772a']
    axes[0].bar(['q2 partial SCF', 'q4 partial SCF'], spans, color=colors, width=.55)
    axes[0].set_yscale('log')
    axes[0].set(ylim=(2e-4, 1200), ylabel='Native Gamma8-derived quartet spread (meV)')
    axes[0].set_title('Native quartet restored in the q4 control', fontsize=10)
    axes[0].text(0, spans[0]*1.35, '311.922 meV', ha='center', fontsize=9)
    axes[0].text(1, spans[1]*1.35, '1.053 micro-eV', ha='center', fontsize=9)
    axes[1].bar(['HgTe host', 'Cd-in-HgTe'], memory, color=colors, width=.55)
    axes[1].axhline(physical, color='#666666', linestyle='--', label=f'Physical RAM: {physical:.2f} GiB')
    for i, value in enumerate(memory):
        axes[1].text(i, value+2, f'{value:.2f}', ha='center', fontsize=9)
    axes[1].set(ylim=(0, 100), ylabel='Native QE total RAM estimate (GiB)', title='16-atom k2/q2 pair, default Fock cutoff')
    axes[1].legend(frameon=False, loc='upper center', fontsize=8)
    for axis in axes:
        axis.grid(axis='y', alpha=.2)
        axis.set_axisbelow(True)
        axis.spines[['top', 'right']].set_visible(False)
        axis.tick_params(labelsize=9)
    fig.text(.5, .065, 'Neither partial host passes EXX convergence. No physical impurity coefficient is inferred.\nNative RAM estimates are approximate and are not measured full-SCF peaks.', ha='center', fontsize=9, color='#555555')
    output = ROOT/'research/programs/microscopic_bandgap/figures/hgte_grid_control'
    for suffix in ['png', 'pdf', 'svg']:
        fig.savefig(output.with_suffix('.'+suffix), dpi=180)
    print(str(output.with_suffix('.pdf')))


if __name__ == '__main__':
    main()
