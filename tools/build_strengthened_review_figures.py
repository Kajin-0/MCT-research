"""Build the strengthened manuscript's generated review figures.

The spectrum/model overlay and three compact robustness figures are copied from
existing frozen repository SVG assets by the workflow. This builder creates the
inference-chain schematic, two energy-resolved residual figures, and two
fit-endpoint heatmaps from the deterministic detailed robustness JSON.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

COLORS = ("#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9")
LABELS = {
    "fractional_power_free": "free p",
    "fractional_power_p_0.5": "p = 0.5",
    "fractional_power_p_0.7": "p = 0.7",
    "fractional_power_p_0.872": "source p = 0.872",
    "fractional_power_p_0.849": "source p = 0.849",
    "fractional_power_p_1": "p = 1",
    "chu_1994_kane_region": "Chu Kane-region",
}


def _save(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def inference_chain(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12.0, 4.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Inference chain and declared downstream sensitivity axes", pad=16, fontsize=15)
    nodes = [
        (0.03, 0.48, 0.16, 0.25, "Specimen state", "composition, carrier state, defects"),
        (0.23, 0.48, 0.16, 0.25, "Source inversion", "ellipsometric layer model and thickness"),
        (0.43, 0.48, 0.16, 0.25, "Published curve", "model-derived alpha(E) bitmap"),
        (0.63, 0.48, 0.16, 0.25, "Reconstruction", "calibration and pixel-to-curve mapping"),
        (0.83, 0.48, 0.14, 0.25, "Fitted intercept", "model, fit domain, weighting"),
    ]
    for x, y, w, h, title, subtitle in nodes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012", linewidth=1.25, facecolor="white"))
        ax.text(x + w / 2, y + 0.16, title, ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(x + w / 2, y + 0.075, subtitle, ha="center", va="center", fontsize=8.7, wrap=True)
    for left, right in zip(nodes[:-1], nodes[1:]):
        ax.add_patch(FancyArrowPatch((left[0] + left[2], 0.605), (right[0], 0.605), arrowstyle="-|>", mutation_scale=13, linewidth=1.2))
    ax.text(0.31, 0.22, "Upstream limitations are inherited, not propagated here", ha="center", fontsize=10)
    ax.text(0.75, 0.22, "This paper audits downstream reconstruction and extraction dependence", ha="center", fontsize=10, fontweight="bold")
    ax.annotate("", xy=(0.83, 0.32), xytext=(0.63, 0.32), arrowprops={"arrowstyle": "-[,widthB=6.2,lengthB=0.8", "lw": 1.4})
    _save(fig, path)


def residual_figure(specimen: dict, title: str, path: Path) -> None:
    energy = np.asarray(specimen["nominal_fit_data"]["energy_ev"], dtype=float)
    halfwidth = np.asarray(specimen["nominal_fit_data"]["log10_vertical_line_halfwidth"], dtype=float)
    fig, ax = plt.subplots(figsize=(9.2, 6.5))
    ax.fill_between(energy, -halfwidth, halfwidth, alpha=0.16, label="local reconstructed line half-width")
    for index, record in enumerate(specimen["nominal_residual_records"]):
        residual = np.asarray(record["residual_log10_absorption"], dtype=float)
        label = LABELS.get(record["candidate_id"], record["candidate_id"])
        if record["boundary_limited"]:
            label += " [boundary]"
        ax.plot(energy, residual, linewidth=1.25, color=COLORS[index % len(COLORS)], label=label)
    ax.axhline(0.0, linewidth=0.9, color="black")
    ax.set_xlabel("Photon energy E (eV)")
    ax.set_ylabel(r"$\log_{10}\alpha_{\mathrm{data}}-\log_{10}\alpha_{\mathrm{fit}}$")
    ax.set_title(title)
    ax.grid(alpha=0.22)
    handles, legend_labels = ax.get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc="lower center", bbox_to_anchor=(0.5, 0.015), ncol=3, frameon=False, fontsize=8.2, handlelength=2.8, columnspacing=1.4)
    fig.subplots_adjust(left=0.12, right=0.97, top=0.90, bottom=0.25)
    _save(fig, path)


def heatmap(specimen: dict, title: str, path: Path) -> None:
    nominal = next(item["edge_ev"] for item in specimen["nominal_candidates"] if item["candidate_id"] == "fractional_power_free")
    lowers = [400.0, 600.0, 800.0, 1000.0]
    uppers = [3000.0, 4000.0, 5000.0]
    values = np.full((len(lowers), len(uppers)), np.nan)
    annotations: dict[tuple[int, int], tuple[float, float]] = {}
    for row, low in enumerate(lowers):
        for col, high in enumerate(uppers):
            records = [item for item in specimen["fit_domain_and_weighting_sensitivity"] if item["fit_absorption_window_cm1"] == [low, high]]
            if not records:
                continue
            shifts = [1000.0 * (item["model_edges_ev"]["fractional_power_free"] - nominal) for item in records]
            values[row, col] = max(abs(value) for value in shifts)
            annotations[(row, col)] = (min(shifts), max(shifts))
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    image = ax.imshow(np.ma.masked_invalid(values), aspect="auto")
    for row in range(len(lowers)):
        for col in range(len(uppers)):
            if (row, col) in annotations:
                minimum, maximum = annotations[(row, col)]
                ax.text(col, row, f"{values[row, col]:.2f}\n[{minimum:+.2f},{maximum:+.2f}]", ha="center", va="center", fontsize=8)
            else:
                ax.text(col, row, "excluded", ha="center", va="center", fontsize=8, fontstyle="italic")
    ax.set_xticks(range(len(uppers)), [f"{int(value)}" for value in uppers])
    ax.set_yticks(range(len(lowers)), [f"{int(value)}" for value in lowers])
    ax.set_xlabel(r"Upper absorption endpoint $\alpha_{\max}$ (cm$^{-1}$)")
    ax.set_ylabel(r"Lower absorption endpoint $\alpha_{\min}$ (cm$^{-1}$)")
    ax.set_title(title + "\ncell: max |shift|; brackets: weighting-rule range (meV)")
    fig.colorbar(image, ax=ax, label="Maximum absolute free-p displacement (meV)")
    fig.tight_layout()
    _save(fig, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.input_json.read_text(encoding="utf-8"))
    specimens = {item["specimen_id"]: item for item in result["specimens"]}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    inference_chain(args.output_dir / "figure1_inference_chain.svg")
    residual_figure(specimens["moazzami2005_x0.226"], "MZ226: residual structure over the nominal fit domain", args.output_dir / "figure6_residuals_mz226.svg")
    residual_figure(specimens["moazzami2005_x0.310"], "MZ310: residual structure over the nominal fit domain", args.output_dir / "figure7_residuals_mz310.svg")
    heatmap(specimens["moazzami2005_x0.226"], "MZ226: free-exponent intercept sensitivity to fit endpoints", args.output_dir / "figure8_fit_grid_mz226.svg")
    heatmap(specimens["moazzami2005_x0.310"], "MZ310: free-exponent intercept sensitivity to fit endpoints", args.output_dir / "figure9_fit_grid_mz310.svg")


if __name__ == "__main__":
    main()
