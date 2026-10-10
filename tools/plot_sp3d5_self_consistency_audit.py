#!/usr/bin/env python3
"""Export finite-alloy and scalar-threshold findings as a research figure."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mct_research.sp3d5 import BinaryModel


root = Path(__file__).resolve().parents[1]
alloy = json.loads((root/"data/calculated/sp3d5_random_alloy_refinement.json").read_text())
other = json.loads((root/"data/calculated/sp3d5_random_alloy_side12.json").read_text())
summary = json.loads((root/"data/calculated/sp3d5_random_alloy_summary.json").read_text())
cpa = json.loads((root/"data/calculated/scalar_cpa_threshold.json").read_text())
params = json.loads((root/"data/materials/schindler2012_sp3d5.json").read_text())
raw = {name: BinaryModel(params[name]) for name in ["HgTe", "CdTe"]}
models = [BinaryModel(params[name], -raw[name].gamma_sectors()["E8"]-(.4 if name == "CdTe" else 0)) for name in raw]

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
a, b, c, d = axes.flatten()
colors = {"6": "#175b79", "8": "#b76524"}
record = alloy["compositions"][0]
for sector in ["6", "8"]:
    a.plot(alloy["energies_eV"], record["mean_density"][sector], color=colors[sector], label=rf"$\Gamma_{sector}$ spectrum")
    center = record["configurations"][0]["sector_centers_eV"][sector]
    a.axvline(center, color=colors[sector], ls=":", lw=1.6)
a.text(.04, .91, "Dotted lines: exact VCA centroids", transform=a.transAxes, fontsize=9)
a.set(xlim=(-.22, .02), xlabel="Energy (eV)", ylabel="Projected spectral density (1/eV)",
      title="A. Correct centroid, shifted peaks at x = 0.180")
a.legend(loc="center right", fontsize=9)

x = np.linspace(.15, .35, 100)
gaps = []
for q in x:
    model = BinaryModel({k: (1-q)*models[0].parameters[k]+q*models[1].parameters[k] for k in params["HgTe"]},
                        (1-q)*models[0].shift+q*models[1].shift)
    sectors = model.gamma_sectors()
    gaps.append(sectors["E6"]-sectors["E8"])
b.plot(x, np.array(gaps)*1000, color=".5", ls="--", label="VCA eigenvalue difference")
points = other["compositions"]+[alloy["compositions"][1]]
points.sort(key=lambda r: r["composition"])
b.scatter([r["composition"] for r in points], [1000*r["ensemble_peak_gap_eV"] for r in points], color="#175b79", label="Explicit alloy peak separation", zorder=3)
b.axhline(0, color=".5", lw=.8)
b.annotate("Peak crossing near 0.30", (.30, 0), xytext=(.20, 68),
           arrowprops={"arrowstyle": "->", "color": ".35"}, fontsize=9)
b.set(xlabel="Cd fraction x", ylabel="Signed separation (meV)",
      title="B. Bare vertex fails beyond its endpoint reductions")
b.legend(fontsize=9, loc="lower right")

rows = cpa["rows"]
xx = [r["concentration"] for r in rows]
constant = cpa["constants"]
for field, limit, color, label in [
    ("cpa_edge_x2_coefficient", "cpa_edge_x2", "#175b79", "CPA DOS edge"),
    ("cpa_gamma_peak", "gamma_peak_x2", "#b76524", "Gamma spectral maximum")]:
    yy = [r[field]["x2_coefficient"] if isinstance(r[field], dict) else r[field] for r in rows]
    c.semilogx(xx, yy, "o-", color=color, ms=4, label=label)
    c.axhline(constant[limit], color=color, lw=1, ls=":")
c.set(xlabel="Dilute fraction x", ylabel=r"$(E-x t_0)/x^2$ (eV)",
      title="C. Full scalar CPA confirms two distinct x² limits")
c.legend(fontsize=9)

shape = cpa["inner_shape"]["rows"]
p = [r["scaled_p_over_a2"] for r in shape]
d.plot(p, [r["analytic_normalized_density"] for r in shape], color="#175b79", lw=2, label="Analytical threshold profile")
d.plot(p[::8], [r["numerical_normalized_density"] for r in shape][::8], "o", color="#b76524", ms=3, label="Full numerical CPA")
d.axvline(1/12, color=".4", ls="--", lw=1)
d.axvline(.25, color=".5", ls=":", lw=1)
d.text(.32, .81, "Peak: p/a² = 1/12\nRe denominator zero: 1/4\nPair indicator at peak → √3/2", transform=d.transAxes, fontsize=9)
d.set(xlabel=r"$p/a^2$ above the CPA edge", ylabel="Normalized Gamma spectral density",
      title="D. Threshold regularization does not control clusters")
d.legend(fontsize=9, loc="center right")
fig.suptitle("HgCdTe model audit and scalar threshold benchmark — no alloy-gap fitting", fontsize=13)
out = root/"research/programs/microscopic_bandgap/figures"
for extension in ["png", "pdf", "svg"]:
    path = out/f"self_consistent_threshold_and_alloy.{extension}"
    fig.savefig(path, dpi=180)
    if extension == "svg":
        path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines())+"\n")
