#!/usr/bin/env python3
"""Test whether the insulating endpoint T' has a finite band-edge limit.

At delta=0 the even mesh excludes Gamma: this is an infrared cutoff, not a
claim that the continuum threshold lies outside the host spectrum.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from mct_research.impurity_tmatrix import branch_trace, t_derivative, t_matrix
from mct_research.sp3d5 import BinaryModel, host_embedding, star_embedding, star_potential


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh", type=int, nargs="+", default=[6, 10, 14, 18, 22, 30])
    parser.add_argument("--output", type=Path, default=Path("data/calculated/sp3d5_cdte_threshold.json"))
    args = parser.parse_args()
    parameters = json.loads(Path("data/materials/schindler2012_sp3d5.json").read_text())
    raw = {name: BinaryModel(parameters[name]) for name in ["HgTe", "CdTe"]}
    models = {name: BinaryModel(parameters[name], -raw[name].gamma_sectors()["E8"] - (0.4 if name == "CdTe" else 0)) for name in raw}
    host, guest = models["CdTe"], models["HgTe"]
    sec = host.gamma_sectors()
    v = star_potential(host, guest)
    a = star_embedding(np.zeros(3)) @ sec["states8"]
    result = {"claim_status": "CALCULATED threshold convergence diagnostic, not physical composition law",
              "empirical_alloy_gap_inputs": [], "rows": []}
    for mesh in args.mesh:
        if mesh % 2 or mesh < 2:
            raise ValueError("Even positive meshes required")
        embedding = host_embedding(host, mesh)
        for delta in [0.0, 0.001, 0.01]:
            energy = sec["E8"] + delta
            g, gp = embedding.resolvent(energy), embedding.resolvent(energy, 1)
            t = t_matrix(v, g)
            row = {"mesh": mesh, "gap_side_detuning_eV": delta,
                   "T8_eV": branch_trace(t, a).real,
                   "negative_T8_prime": branch_trace(-t_derivative(t, gp), a).real}
            result["rows"].append(row)
            print(row, flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
