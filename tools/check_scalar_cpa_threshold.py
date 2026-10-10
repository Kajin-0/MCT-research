#!/usr/bin/env python3
"""Freeze the exact numerical CPA benchmark; no HgCdTe inputs are used."""

import hashlib
import json
from pathlib import Path

import numpy as np

from mct_research.scalar_cpa_threshold import (
    cpa_gamma_peak, cpa_inner_green, cpa_lower_edge, pair_scattering_indicator,
    threshold_constants,
)
from mct_research.threshold_impurity import dilute_pole_below_edge


if __name__ == "__main__":
    v, bandwidth = -.1, 1.0
    c = threshold_constants(v, bandwidth)
    result = {"claim_status": "CALCULATED numerical check of conditional PROVEN scalar CPA asymptotics",
              "material": None, "empirical_alloy_gap_inputs": [],
              "potential_eV": v, "bandwidth_eV": bandwidth,
              "density_of_states": "3 sqrt(epsilon)/(2 bandwidth**1.5), 0<epsilon<bandwidth",
              "constants": c, "rows": [],
              "pair_indicator_is_rigorous_error_bound": False}
    for x in [.03, .01, .003, .001, .0003, .0001, .00003, .00001]:
        edge = cpa_lower_edge(x, v, bandwidth)
        peak = cpa_gamma_peak(x, v, bandwidth)
        zpeak = (peak["energy"]-x*c["t0"])/(x*x)+1j*peak["external_eta"]/(x*x)
        wpeak = 1/cpa_inner_green(x, zpeak, v, bandwidth)
        ata = dilute_pole_below_edge(x, v, bandwidth)
        result["rows"].append({"concentration": x, "ata_pole_eV": ata,
                               "ata_x_three_halves_coefficient": (ata-x*c["t0"])/x**1.5,
                               "cpa_edge": edge, "cpa_gamma_peak": peak,
                               "cpa_edge_x2_coefficient": (edge["energy"]-x*c["t0"])/(x*x),
                               "edge_pair_indicator": pair_scattering_indicator(edge["w"], x, v),
                               "peak_pair_indicator": pair_scattering_indicator(wpeak, x, v)})
    shape = []
    x = .0001
    for p in np.linspace(.003, 1.8, 200):
        scaled_energy = c["b"]+c["a"]**2*(.25+p)+1j*c["a"]**2*1e-6
        full = cpa_inner_green(x, scaled_energy, v)
        shape.append({"scaled_p_over_a2": float(p),
                      "analytic_normalized_density": float(np.sqrt(p)/(p+.25)**2),
                      "numerical_normalized_density": float(-full.imag*x*x*c["a"]**2)})
    result["inner_shape"] = {"concentration": x, "rows": shape}
    modules = ["src/mct_research/scalar_cpa_threshold.py", "src/mct_research/threshold_impurity.py"]
    result["source_sha256"] = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in modules}
    path = Path("data/calculated/scalar_cpa_threshold.json")
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(path)
