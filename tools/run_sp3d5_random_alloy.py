#!/usr/bin/env python3
"""Nonperturbative finite-cell spectra of the frozen binary-derived alloy model.

Decision: do endpoint mass/reciprocal reductions describe the actual model at
interior compositions? No coefficients are inferred from empirical alloy gaps.
This script extracts calculated spectral maxima; it does not fit a gap law.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from mct_research.sp3d5 import BinaryModel
from mct_research.sp3d5_disorder import (
    lanczos_spectrum, random_occupation, supercell_hamiltonian, uniform_gamma_states,
)


def peak(energy, density, center):
    mask = np.flatnonzero(abs(energy-center) < .7)
    index = mask[np.argmax(density[mask])]
    return {"energy_eV": float(energy[index]), "height": float(density[index]),
            "at_search_boundary": bool(index == mask[0] or index == mask[-1])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", type=int, default=8)
    parser.add_argument("--composition", type=float, nargs="+", default=[.18, .33])
    parser.add_argument("--seeds", type=int, nargs="+", default=[310, 711, 912, 1423])
    parser.add_argument("--steps", type=int, default=800)
    parser.add_argument("--eta", type=float, default=.02)
    parser.add_argument("--output", type=Path, default=Path("data/calculated/sp3d5_random_alloy_side8.json"))
    args = parser.parse_args()
    parameter_path = Path("data/materials/schindler2012_sp3d5.json")
    parameters = json.loads(parameter_path.read_text())
    raw = {name: BinaryModel(parameters[name]) for name in ["HgTe", "CdTe"]}
    models = [BinaryModel(parameters[name], -raw[name].gamma_sectors()["E8"] - (.4 if name == "CdTe" else 0)) for name in raw]
    host, guest = models
    energies = np.linspace(-.8, 1.25, 1026)
    result = {
        "claim_status": "CALCULATED finite-cell spectral diagnostic of a binary-derived Hamiltonian",
        "empirical_alloy_gap_inputs": [], "side": args.side, "cells": args.side**3,
        "parameter_file": str(parameter_path),
        "parameter_sha256": hashlib.sha256(parameter_path.read_bytes()).hexdigest(),
        "valence_offset_eV": .4, "te_share": .25,
        "orbitals": 36 * args.side**3, "steps": args.steps, "eta_eV": args.eta,
        "occupation_statistics": "fixed-count random placement in a periodic primitive-cell box",
        "spectral_observable": "maximum of ensemble-averaged Gamma-sector spectral density, near its VCA edge",
        "energies_eV": energies.tolist(), "compositions": []
    }
    for target in args.composition:
        start = time.monotonic()
        configurations = []
        density = {s: np.zeros_like(energies) for s in [6, 8]}
        for seed in args.seeds:
            occupation = random_occupation(args.side, target, seed)
            x = float(occupation.mean())
            reference = BinaryModel({k: (1-x)*host.parameters[k] + x*guest.parameters[k] for k in host.parameters},
                                    (1-x)*host.shift + x*guest.shift)
            sectors = reference.gamma_sectors()
            h = supercell_hamiltonian(host, guest, args.side, occupation)
            configuration = {"seed": seed, "composition": x, "occupation_sha256": hashlib.sha256(occupation.tobytes()).hexdigest(),
                             "spectral": {}, "centroid_errors_eV": {}, "steps_peak_convergence_eV": {},
                             "lanczos_coefficients": {}, "sector_centers_eV": {}, "sector_variances_eV2": {}}
            for sector in [6, 8]:
                vectors = uniform_gamma_states(sectors[f"states{sector}"], args.side**3)
                spec, truncated = np.zeros_like(energies), np.zeros_like(energies)
                centroid_error = 0.0
                coefficients, variances = [], []
                for a in vectors.T:
                    lanczos = lanczos_spectrum(h, a, args.steps)
                    coefficients.append({"diagonal": lanczos.diagonal.tolist(),
                                         "off_diagonal": lanczos.off_diagonal.tolist()})
                    variances.append(float(lanczos.off_diagonal[0]**2) if len(lanczos.off_diagonal) else 0.0)
                    spec += -lanczos.green(energies + 1j*args.eta).imag / (np.pi * len(vectors.T))
                    stop = min(len(lanczos.diagonal), args.steps//2)
                    half = type(lanczos)(lanczos.diagonal[:stop], lanczos.off_diagonal[:stop-1])
                    truncated += -half.green(energies + 1j*args.eta).imag / (np.pi * len(vectors.T))
                    centroid_error = max(centroid_error, abs(lanczos.diagonal[0]-sectors[f"E{sector}"]))
                center = sectors[f"E{sector}"]
                full_peak, half_peak = peak(energies, spec, center), peak(energies, truncated, center)
                configuration["spectral"][str(sector)] = {"peak": full_peak, "density": spec.tolist()}
                configuration["centroid_errors_eV"][str(sector)] = centroid_error
                configuration["lanczos_coefficients"][str(sector)] = coefficients
                configuration["sector_centers_eV"][str(sector)] = float(center)
                configuration["sector_variances_eV2"][str(sector)] = float(np.mean(variances))
                configuration["steps_peak_convergence_eV"][str(sector)] = full_peak["energy_eV"]-half_peak["energy_eV"]
                density[sector] += spec / len(args.seeds)
            configuration["peak_gap_eV"] = configuration["spectral"]["6"]["peak"]["energy_eV"]-configuration["spectral"]["8"]["peak"]["energy_eV"]
            configurations.append(configuration)
            print(f"side={args.side}, x={x:.6f}, seed={seed}: gap={configuration['peak_gap_eV']:.5f}, "
                  f"Lanczos shift={configuration['steps_peak_convergence_eV']}", flush=True)
        peaks = {str(s): peak(energies, density[s], sectors[f"E{s}"]) for s in [6, 8]}
        result["compositions"].append({"target": target, "composition": x, "vca_gap_eV": sectors["E6"]-sectors["E8"],
                                        "peaks": peaks, "mean_density": {str(s): density[s].tolist() for s in [6, 8]},
                                        "ensemble_peak_gap_eV": peaks["6"]["energy_eV"]-peaks["8"]["energy_eV"],
                                        "configurations": configurations, "elapsed_seconds": time.monotonic()-start})
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+"\n")
