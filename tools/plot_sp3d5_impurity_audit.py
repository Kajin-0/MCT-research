#!/usr/bin/env python3
"""Standalone research figure for the frozen binary-derived diagnostic."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


root = Path(__file__).resolve().parents[1]
summary = json.loads((root / "data/calculated/sp3d5_endpoint_reductions.json").read_text())
dataset = next(d for d in summary["datasets"] if d["input"].endswith("mesh30.json"))
record = next(r for r in dataset["endpoint_reductions"] if r["eta_eV"] == .05)
threshold = json.loads((root / "data/calculated/sp3d5_cdte_threshold.json").read_text())
mh = dataset["binary_gap_H_eV"] / 2
delta = (dataset["binary_gap_C_eV"] - dataset["binary_gap_H_eV"]) / 2
x = np.linspace(0, .45, 500)
correct = np.polynomial.polynomial.polyval(x, record["mass_cubic_coefficients_ascending_eV"])
wrong = correct + delta * x * (1 - x) * (1 - 2 * x)

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
a, b = axes
a.axhline(0, color="0.4", lw=.8)
a.plot(x, mh + delta * x, color="0.55", ls=":", label="Binary chord")
a.plot(x, wrong, color="#b76524", ls="--", label="Full T counted twice")
a.plot(x, correct, color="#175b79", lw=2, label="Reference-corrected mass cubic")
for r, color, label, y in [(record["incorrect_double_counted_mass_roots"][0], "#b76524", "0.165", .06),
                            (record["mass_cubic_roots"][0], "#175b79", "0.332", -.09)]:
    a.scatter([r], [0], color=color, zorder=5)
    a.annotate(label, (r, 0), xytext=(r + .007, y), color=color,
               arrowprops={"arrowstyle": "-", "color": color})
a.set(xlabel="Cd fraction x", ylabel="Interpolated common-mode mass (eV)",
      title="A. Reference choice changes the inferred inversion", xlim=(0, .45))
a.legend(fontsize=9, loc="upper left")
for detuning, color in [(0, "#175b79"), (.001, "#a68131"), (.01, "#63775a")]:
    rows = [r for r in threshold["rows"] if r["gap_side_detuning_eV"] == detuning]
    b.plot([r["mesh"] for r in rows], [r["negative_T8_prime"] for r in rows],
           "o-", color=color, label=f"Gap-side detuning {detuning*1000:g} meV")
b.set(xlabel="Mesh points per reciprocal direction", ylabel=r"$-\partial_E T_8$ (dimensionless)",
      title="B. The CdTe band-edge derivative does not settle")
b.legend(fontsize=9)
fig.suptitle("Binary-derived HgCdTe impurity audit — no alloy-gap fitting", fontsize=13)
out = root / "research/programs/microscopic_bandgap/figures"
out.mkdir(parents=True, exist_ok=True)
for extension in ["png", "pdf", "svg"]:
    path = out / f"impurity_reference_and_threshold.{extension}"
    fig.savefig(path, dpi=180)
    if extension == "svg":
        path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
