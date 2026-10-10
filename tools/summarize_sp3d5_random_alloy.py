#!/usr/bin/env python3
"""Re-evaluate cached Lanczos spectra at several broadenings without rerunning cells."""

import hashlib
import json
from pathlib import Path

import numpy as np

from mct_research.sp3d5_disorder import LanczosSpectrum


if __name__ == "__main__":
    files = [p for p in sorted(Path("data/calculated").glob("sp3d5_random_alloy_*.json"))
             if not p.name.endswith("summary.json")]
    result = {"claim_status": "CALCULATED finite-cell Gamma spectral-peak diagnostic, not a topological transition",
              "empirical_alloy_gap_inputs": [], "inputs": [], "rows": []}
    for path in files:
        data = json.loads(path.read_text())
        result["inputs"].append({"file": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        energy = np.array(data["energies_eV"])
        for record in data["compositions"]:
            cached = all("lanczos_coefficients" in row for row in record["configurations"])
            etas = [.05, .02, .01, .005] if cached else [data["eta_eV"]]
            for eta in etas:
                peaks, half_peaks = {}, {}
                seed_peaks = {s: [] for s in ["6", "8"]}
                full_mean, half_mean = {}, {}
                for sector in ["6", "8"]:
                    full = np.zeros_like(energy)
                    half = np.zeros_like(energy)
                    for row in record["configurations"]:
                        if cached:
                            spec, trunc = np.zeros_like(energy), np.zeros_like(energy)
                            for coefficients in row["lanczos_coefficients"][sector]:
                                lc = LanczosSpectrum(np.array(coefficients["diagonal"]), np.array(coefficients["off_diagonal"]))
                                count = len(row["lanczos_coefficients"][sector])
                                spec += -lc.green(energy+1j*eta).imag/(np.pi*count)
                                stop = len(lc.diagonal)//2
                                short = LanczosSpectrum(lc.diagonal[:stop], lc.off_diagonal[:stop-1])
                                trunc += -short.green(energy+1j*eta).imag/(np.pi*count)
                            center = row["sector_centers_eV"][sector]
                        else:
                            spec = np.array(row["spectral"][sector]["density"])
                            trunc = spec
                            center = record["peaks"][sector]["energy_eV"]
                        mask = np.flatnonzero(abs(energy-center) < .7)
                        peak = energy[mask[np.argmax(spec[mask])]]
                        seed_peaks[sector].append(float(peak))
                        full += spec/len(record["configurations"])
                        half += trunc/len(record["configurations"])
                    full_mean[sector], half_mean[sector] = full, half
                    peaks[sector] = float(energy[mask[np.argmax(full[mask])]])
                    half_peaks[sector] = float(energy[mask[np.argmax(half[mask])]])
                result["rows"].append({"input": str(path), "side": data["side"],
                    "composition": record["composition"], "eta_eV": eta,
                    "steps": data["steps"], "configurations": len(record["configurations"]),
                    "vca_gap_eV": record["vca_gap_eV"], "peak_energies_eV": peaks,
                    "peak_gap_eV": peaks["6"]-peaks["8"],
                    "seed_peak_gaps_eV": [a-b for a, b in zip(seed_peaks["6"], seed_peaks["8"])],
                    "half_steps_peak_shifts_eV": {s: peaks[s]-half_peaks[s] for s in peaks} if cached else None,
                    "original_max_config_half_steps_peak_shift_eV": max(
                        abs(v) for r in record["configurations"] for v in r["steps_peak_convergence_eV"].values()),
                    "min_density": min(float(full_mean[s].min()) for s in peaks)})
    path = Path("data/calculated/sp3d5_random_alloy_summary.json")
    path.write_text(json.dumps(result, indent=2)+"\n")
    for row in result["rows"]:
        print({key: row[key] for key in ["side", "composition", "eta_eV", "peak_gap_eV", "half_steps_peak_shifts_eV"]})
