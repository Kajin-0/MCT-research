#!/usr/bin/env python3
"""Build deterministic SVG figures and Markdown tables for the flagship manuscript."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import html
import json
import math
import os
from pathlib import Path
import subprocess
from typing import Any, Iterable, Sequence

import numpy as np

from mct_research import (
    carrier_filled_optical_edge_ev,
    fit_exponential_absorption_tail,
    normalized_gaussian_gap_convolved_power_absorption,
    unified_response_spectrum,
)

FIGURE_FILES = (
    "figure1_forward_hierarchy.svg",
    "figure2_transition_distribution.svg",
    "figure3_herrmann_tail_nonuniqueness.svg",
    "figure4_chang_cutoff_rank.svg",
    "figure5_carrier_filling.svg",
    "figure6_unified_structural_rank.svg",
    "figure7_measurement_design.svg",
)
TABLE_FILES = (
    "table1_theorem_summary.md",
    "table2_quantitative_results.md",
    "table3_claim_provenance.md",
)
RECORD_PATHS = (
    "data/validation/near_critical_transition_model_dependence.json",
    "data/validation/herrmann_gaussian_tail_reproduction.json",
    "data/validation/chang_2006_cutoff_identifiability.json",
    "data/validation/dingrong_1985_carrier_filling_sensitivity.json",
    "data/validation/unified_spectrum_structural_rank.json",
)


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _load_json(root: Path, relative: str) -> dict[str, Any]:
    with (root / relative).open(encoding="utf-8") as handle:
        return json.load(handle)


def _git_commit(root: Path) -> str:
    github_sha = os.environ.get("GITHUB_SHA")
    if github_sha:
        return github_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _metadata(commit: str, sources: Sequence[str], claim_ids: Sequence[str]) -> str:
    payload = {
        "claim_ids": list(claim_ids),
        "generated_from_commit": commit,
        "source_paths": list(sources),
    }
    return _esc(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def _wrap_svg(
    width: int,
    height: int,
    title: str,
    body: Iterable[str],
    *,
    commit: str,
    sources: Sequence[str],
    claim_ids: Sequence[str],
) -> str:
    style = (
        "<style>"
        "text{font-family:Arial,sans-serif;fill:#111}"
        ".title{font-size:24px;font-weight:700}.subtitle{font-size:14px}"
        ".panel-title{font-size:17px;font-weight:700}.label{font-size:13px}"
        ".small{font-size:11px}.tiny{font-size:9px}"
        ".axis{stroke:#111;stroke-width:1.4}.grid{stroke:#ddd;stroke-width:1}"
        ".line1{fill:none;stroke:#111;stroke-width:2.4}"
        ".line2{fill:none;stroke:#555;stroke-width:2.2;stroke-dasharray:8 5}"
        ".line3{fill:none;stroke:#999;stroke-width:2.2;stroke-dasharray:2 4}"
        ".bar1{fill:#222}.bar2{fill:#777}.bar3{fill:#bbb;stroke:#222;stroke-width:1}"
        ".box{fill:#f7f7f7;stroke:#111;stroke-width:1.5}"
        ".synthetic{font-size:11px;font-weight:700;letter-spacing:0.5px}"
        "</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<title>{_esc(title)}</title>'
        f'<desc>Deterministic manuscript figure. Claims: {_esc(", ".join(claim_ids))}.</desc>'
        f'<metadata>{_metadata(commit, sources, claim_ids)}</metadata>'
        '<rect width="100%" height="100%" fill="white"/>'
        + style
        + "".join(body)
        + "</svg>\n"
    )


@dataclass(frozen=True)
class Panel:
    left: float
    top: float
    width: float
    height: float
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    def x(self, value: float) -> float:
        return self.left + self.width * (value - self.xmin) / (self.xmax - self.xmin)

    def y(self, value: float) -> float:
        return self.top + self.height * (self.ymax - value) / (self.ymax - self.ymin)


def _polyline(panel: Panel, xs: Sequence[float], ys: Sequence[float], css: str) -> str:
    points = " ".join(
        f"{panel.x(float(x)):.2f},{panel.y(float(y)):.2f}"
        for x, y in zip(xs, ys, strict=True)
    )
    return f'<polyline points="{points}" class="{css}"/>'


def _axes(
    panel: Panel,
    title: str,
    x_ticks: Sequence[tuple[float, str]],
    y_ticks: Sequence[tuple[float, str]],
    x_label: str,
    y_label: str,
) -> list[str]:
    body = [
        f'<text x="{panel.left:.1f}" y="{panel.top-14:.1f}" class="panel-title">{_esc(title)}</text>',
        f'<line x1="{panel.left:.2f}" y1="{panel.top+panel.height:.2f}" '
        f'x2="{panel.left+panel.width:.2f}" y2="{panel.top+panel.height:.2f}" class="axis"/>',
        f'<line x1="{panel.left:.2f}" y1="{panel.top:.2f}" '
        f'x2="{panel.left:.2f}" y2="{panel.top+panel.height:.2f}" class="axis"/>',
    ]
    for value, label in x_ticks:
        x = panel.x(value)
        body += [
            f'<line x1="{x:.2f}" y1="{panel.top:.2f}" x2="{x:.2f}" '
            f'y2="{panel.top+panel.height:.2f}" class="grid"/>',
            f'<text x="{x:.2f}" y="{panel.top+panel.height+18:.2f}" '
            f'text-anchor="middle" class="small">{_esc(label)}</text>',
        ]
    for value, label in y_ticks:
        y = panel.y(value)
        body += [
            f'<line x1="{panel.left:.2f}" y1="{y:.2f}" '
            f'x2="{panel.left+panel.width:.2f}" y2="{y:.2f}" class="grid"/>',
            f'<text x="{panel.left-8:.2f}" y="{y+4:.2f}" '
            f'text-anchor="end" class="small">{_esc(label)}</text>',
        ]
    body += [
        f'<text x="{panel.left+panel.width/2:.2f}" y="{panel.top+panel.height+40:.2f}" '
        f'text-anchor="middle" class="label">{_esc(x_label)}</text>',
        f'<text transform="translate({panel.left-50:.2f} {panel.top+panel.height/2:.2f}) rotate(-90)" '
        f'text-anchor="middle" class="label">{_esc(y_label)}</text>',
    ]
    return body


def _bar(
    panel: Panel,
    x_center: float,
    width_data: float,
    value: float,
    baseline: float,
    css: str,
) -> str:
    x1 = panel.x(x_center - width_data / 2.0)
    x2 = panel.x(x_center + width_data / 2.0)
    y1 = panel.y(value)
    y2 = panel.y(baseline)
    return (
        f'<rect x="{min(x1,x2):.2f}" y="{min(y1,y2):.2f}" '
        f'width="{abs(x2-x1):.2f}" height="{abs(y2-y1):.2f}" class="{css}"/>'
    )


def _log_relative(values: Sequence[float], floor: float = 1.0e-15) -> list[float]:
    return [math.log10(max(float(value), floor)) for value in values]


def _figure1(commit: str) -> str:
    width, height = 1380, 720
    body = [
        '<text x="35" y="38" class="title">Figure 1. From latent bandgap to reported HgCdTe observable</text>',
        '<text x="35" y="62" class="subtitle">Forward-model layers and manuscript evidence classes</text>',
    ]
    labels = [
        "latent signed gap",
        "composition / gap distribution",
        "carrier and defect state",
        "intrinsic and tail absorption",
        "optical depth / instrument",
        "declared edge or cutoff",
        "reported observable",
    ]
    box_w, box_h, gap, y = 170.0, 88.0, 18.0, 130.0
    for index, label in enumerate(labels):
        x = 32.0 + index * (box_w + gap)
        body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" rx="8" class="box"/>')
        words = label.split(" ")
        midpoint = (len(words) + 1) // 2
        lines = [" ".join(words[:midpoint]), " ".join(words[midpoint:])]
        for line_index, line in enumerate(lines):
            body.append(
                f'<text x="{x+box_w/2:.1f}" y="{y+39+22*line_index:.1f}" '
                f'text-anchor="middle" class="label">{_esc(line)}</text>'
            )
        if index < len(labels) - 1:
            x1 = x + box_w
            x2 = x + box_w + gap - 4
            body += [
                f'<line x1="{x1:.1f}" y1="{y+box_h/2:.1f}" x2="{x2:.1f}" y2="{y+box_h/2:.1f}" class="axis"/>',
                f'<path d="M {x2-7:.1f} {y+box_h/2-5:.1f} L {x2:.1f} {y+box_h/2:.1f} L {x2-7:.1f} {y+box_h/2+5:.1f}" fill="none" stroke="#111"/>',
            ]
    body += [
        '<text x="35" y="300" class="panel-title">Evidence state is part of every claim</text>',
    ]
    states = [
        ("exact theorem", "algebraic result under declared assumptions"),
        ("numerical verification", "deterministic check of theorem or bounded consequence"),
        ("source reproduction", "published convention reproduced under source limits"),
        ("bounded synthetic sensitivity", "illustrative parameters; not a specimen fit"),
        ("external material validation", "calibrated real specimen with sufficient provenance"),
    ]
    for index, (name, definition) in enumerate(states):
        y0 = 340 + index * 66
        body += [
            f'<rect x="70" y="{y0-25}" width="270" height="42" rx="6" class="box"/>',
            f'<text x="205" y="{y0+1}" text-anchor="middle" class="label">{_esc(name)}</text>',
            f'<text x="375" y="{y0+1}" class="label">{_esc(definition)}</text>',
        ]
    body += [
        '<rect x="900" y="330" width="410" height="260" rx="10" class="box"/>',
        '<text x="1105" y="370" text-anchor="middle" class="panel-title">Central inference rule</text>',
        '<text x="1105" y="425" text-anchor="middle" class="label">A reported edge is an output of the chain.</text>',
        '<text x="1105" y="460" text-anchor="middle" class="label">It is not automatically Eg(mean x, T).</text>',
        '<text x="1105" y="515" text-anchor="middle" class="label">Exact null directions require external information,</text>',
        '<text x="1105" y="545" text-anchor="middle" class="label">not merely higher signal-to-noise.</text>',
    ]
    return _wrap_svg(width, height, "Forward hierarchy", body, commit=commit, sources=(), claim_ids=("C01", "C20", "C21"))


def _figure2(record: dict[str, Any], commit: str) -> str:
    width, height = 1480, 920
    body = [
        '<text x="35" y="38" class="title">Figure 2. Near-critical transition broadening and root censoring</text>',
        '<text x="35" y="62" class="synthetic">BOUNDED SYNTHETIC SENSITIVITY - NOT A TOPOLOGICAL PHASE-FRACTION MEASUREMENT</text>',
    ]
    models = record["latent_gap_models"]
    short = ["Laurenti", "Hansen", "Hansen-Pade"]
    classes = ["line1", "line2", "line3"]

    p1 = Panel(85, 120, 560, 300, -0.5, 2.5, 45.0, 85.0)
    body += _axes(p1, "A. Central critical temperature by latent law", [(0, "Laurenti"), (1, "Hansen"), (2, "Pade")], [(50, "50"), (60, "60"), (70, "70"), (80, "80")], "latent law", "critical temperature (K)")
    for index, model in enumerate(models):
        value = float(model["central_critical_temperature_k"])
        body.append(_bar(p1, float(index), 0.55, value, 45.0, ("bar1", "bar2", "bar3")[index]))
        body.append(f'<text x="{p1.x(index):.2f}" y="{p1.y(value)-7:.2f}" text-anchor="middle" class="small">{value:.2f}</text>')
    span = float(record["cross_model_results"]["central_critical_temperature_span_k"])
    body.append(f'<text x="{p1.left+p1.width-8:.1f}" y="{p1.top+24:.1f}" text-anchor="end" class="label">span = {span:.3f} K</text>')

    p2 = Panel(820, 120, 560, 300, 0.001, 0.010, 0.0, 50.0)
    body += _axes(p2, "B. Conditional width and local approximation", [(0.001, "0.001"), (0.003, "0.003"), (0.005, "0.005"), (0.010, "0.010")], [(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40"), (50, "50")], "composition sigma_x", "temperature width (K)")
    for index, model in enumerate(models):
        cases = model["cases"]
        xs = [float(case["composition_sigma"]) for case in cases]
        exact = [float(case["conditional_sigma_temperature_k"]) for case in cases]
        local = [float(case["linearized_sigma_temperature_k"]) for case in cases]
        body += [_polyline(p2, xs, exact, classes[index]), _polyline(p2, xs, local, classes[index])]
    body += [
        '<text x="836" y="438" class="small">same line style: exact; repeated overlay: local linearization</text>',
    ]

    p3 = Panel(85, 555, 560, 270, 0.001, 0.010, 0.0, 1.02)
    body += _axes(p3, "C. Crossing and always-normal probability", [(0.001, "0.001"), (0.003, "0.003"), (0.005, "0.005"), (0.010, "0.010")], [(0, "0"), (0.25, "0.25"), (0.5, "0.50"), (0.75, "0.75"), (1.0, "1.00")], "composition sigma_x", "probability")
    for index, model in enumerate(models):
        cases = model["cases"]
        xs = [float(case["composition_sigma"]) for case in cases]
        crossing = [float(case["single_crossing_probability"]) for case in cases]
        normal = [float(case["always_normal_probability"]) for case in cases]
        body += [_polyline(p3, xs, crossing, classes[index]), _polyline(p3, xs, normal, classes[index])]

    p4 = Panel(820, 555, 560, 270, 0.001, 0.010, 0.0, 10.5)
    body += _axes(p4, "D. Absolute local-width approximation error", [(0.001, "0.001"), (0.003, "0.003"), (0.005, "0.005"), (0.010, "0.010")], [(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8"), (10, "10")], "composition sigma_x", "absolute error (K)")
    for index, model in enumerate(models):
        cases = model["cases"]
        xs = [float(case["composition_sigma"]) for case in cases]
        errors = [abs(float(case["sigma_approximation_error_k"])) for case in cases]
        body.append(_polyline(p4, xs, errors, classes[index]))
    for index, name in enumerate(short):
        y0 = 875
        x0 = 160 + index * 220
        body += [
            f'<line x1="{x0}" y1="{y0}" x2="{x0+42}" y2="{y0}" class="{classes[index]}"/>',
            f'<text x="{x0+50}" y="{y0+4}" class="small">{name}</text>',
        ]
    return _wrap_svg(width, height, "Transition distribution", body, commit=commit, sources=(RECORD_PATHS[0],), claim_ids=("C02", "C03", "C04"))


def _herrmann_regeneration(record: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, list[dict[str, float | str]]]:
    controlled = record["controlled_reproduction"]
    mean_gap = float(controlled["mean_gap_ev"])
    sigma = float(controlled["gap_standard_deviation_ev"])
    energy = mean_gap + sigma * np.linspace(-8.0, 3.0, int(controlled["energy_grid_points"]))
    absorption = normalized_gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma,
        exponent=0.5,
        absorption_at_mean_gap_cm_inverse=float(controlled["absorption_at_mean_gap_cm_inverse"]),
        quadrature_order=int(controlled["quadrature_order"]),
        standard_deviation_limit=float(controlled["standard_deviation_limit"]),
    )
    source_s = float(controlled["source_scale_s_ev"])
    rows: list[dict[str, float | str]] = []
    source_rows = [row for row in record["fit_results"] if float(row["exponent"]) == 0.5]
    source_rows.sort(key=lambda row: (float(row["absorption_window_cm_inverse"][0]), float(row["absorption_window_cm_inverse"][1])))
    for source in source_rows:
        lower, upper = (float(value) for value in source["absorption_window_cm_inverse"])
        fit = fit_exponential_absorption_tail(energy, absorption, absorption_bounds_cm_inverse=(lower, upper))
        ratio = fit.tail_energy_ev / source_s
        if not math.isclose(ratio, float(source["tail_energy_over_source_s"]), rel_tol=2.0e-5, abs_tol=2.0e-7):
            raise RuntimeError("Herrmann regenerated tail ratio does not match immutable record")
        rows.append({
            "label": f"{lower:g}-{upper:g}",
            "lower": lower,
            "upper": upper,
            "ratio": ratio,
            "r_squared": fit.r_squared,
        })
    return energy, absorption, rows


def _figure3(record: dict[str, Any], commit: str) -> str:
    energy, absorption, rows = _herrmann_regeneration(record)
    controlled = record["controlled_reproduction"]
    mean_gap = float(controlled["mean_gap_ev"])
    source_s = float(controlled["source_scale_s_ev"])
    z = (energy - mean_gap) / source_s
    positive = absorption > 0.07
    z_plot = z[positive]
    log_alpha = np.log10(absorption[positive])
    width, height = 1480, 920
    body = [
        '<text x="35" y="38" class="title">Figure 3. One distributed spectrum supports multiple apparent tail energies</text>',
        '<text x="35" y="62" class="synthetic">SOURCE-CONDITIONED REPRODUCTION AND SYNTHETIC OBSERVATION-OPERATOR SENSITIVITY</text>',
    ]
    p1 = Panel(85, 120, 620, 300, -10.0, 5.0, -1.2, 4.0)
    body += _axes(p1, "A. Regenerated square-root Gaussian-gap spectrum", [(-8, "-8"), (-4, "-4"), (0, "0"), (4, "4")], [(-1, "-1"), (0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")], "(E - mean gap) / source s", "log10 absorption (cm^-1)")
    body.append(_polyline(p1, z_plot.tolist(), log_alpha.tolist(), "line1"))
    for level in (0.1, 1.0, 10.0, 100.0, 500.0):
        y = p1.y(math.log10(level))
        body.append(f'<line x1="{p1.left}" y1="{y:.2f}" x2="{p1.left+p1.width}" y2="{y:.2f}" stroke="#aaa" stroke-dasharray="3 4"/>')

    ordered_labels = ["0.1-100", "1-100", "10-100", "10-500", "100-500"]
    row_by_label = {str(row["label"]): row for row in rows}
    plot_rows = [row_by_label[label] for label in ordered_labels]
    p2 = Panel(820, 120, 560, 300, -0.5, 4.5, 0.40, 0.85)
    body += _axes(p2, "B. Apparent W_fit / s by fit window", [(i, label) for i, label in enumerate(ordered_labels)], [(0.4, "0.40"), (0.5, "0.50"), (0.6, "0.60"), (0.7, "0.70"), (0.8, "0.80")], "absorption fit window (cm^-1)", "W_fit / source s")
    for index, row in enumerate(plot_rows):
        css = "bar1" if row["label"] == "1-100" else "bar2"
        body.append(_bar(p2, float(index), 0.58, float(row["ratio"]), 0.40, css))
        body.append(f'<text x="{p2.x(index):.2f}" y="{p2.y(float(row["ratio"]))-7:.2f}" text-anchor="middle" class="small">{float(row["ratio"]):.3f}</text>')

    p3 = Panel(85, 555, 620, 270, 0.43, 0.84, 0.990, 1.000)
    body += _axes(p3, "C. High R-squared does not select a unique tail width", [(0.45, "0.45"), (0.55, "0.55"), (0.65, "0.65"), (0.75, "0.75"), (0.83, "0.83")], [(0.990, "0.990"), (0.994, "0.994"), (0.998, "0.998"), (1.000, "1.000")], "W_fit / source s", "R-squared")
    for row in plot_rows:
        x = p3.x(float(row["ratio"]))
        y = p3.y(float(row["r_squared"]))
        body += [
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#222"/>',
            f'<text x="{x+7:.2f}" y="{y-7:.2f}" class="tiny">{_esc(row["label"])}</text>',
        ]

    p4 = Panel(820, 555, 560, 270, 0.0, 15.0, 0.0, 1.0)
    body += _axes(p4, "D. Width compatible with an observed 4 meV tail", [(0, "0"), (5, "5"), (10, "10"), (15, "15")], [], "gap-distribution sigma_G (meV)", "")
    low, high = (float(value) for value in record["derived_results"]["compatible_sigma_G_range_mev_across_declared_models_and_windows"])
    y = p4.y(0.55)
    body += [
        f'<line x1="{p4.x(low):.2f}" y1="{y:.2f}" x2="{p4.x(high):.2f}" y2="{y:.2f}" stroke="#111" stroke-width="12" stroke-linecap="round"/>',
        f'<text x="{p4.x(low):.2f}" y="{y-20:.2f}" text-anchor="middle" class="label">{low:.3f}</text>',
        f'<text x="{p4.x(high):.2f}" y="{y-20:.2f}" text-anchor="middle" class="label">{high:.3f}</text>',
        f'<text x="{p4.left+p4.width/2:.2f}" y="{p4.top+45:.2f}" text-anchor="middle" class="label">interval, not a posterior distribution</text>',
    ]
    increase = 100.0 * float(record["derived_results"]["fit_window_increase_fraction"])
    body.append(f'<text x="{p2.left+p2.width-5:.1f}" y="{p2.top+25:.1f}" text-anchor="end" class="label">fit-window increase = {increase:.1f}%</text>')
    return _wrap_svg(width, height, "Herrmann tail non-uniqueness", body, commit=commit, sources=(RECORD_PATHS[1], "src/mct_research/spectral_convolution.py"), claim_ids=("C05", "C06", "C07", "C08"))


def _singular_panel(panel: Panel, title: str, values: Sequence[float], rank: int, condition: float | None = None) -> list[str]:
    logs = _log_relative(values)
    body = _axes(panel, title, [(i, str(i + 1)) for i in range(len(values))], [(-15, "1e-15"), (-10, "1e-10"), (-5, "1e-5"), (0, "1")], "singular direction", "log10 relative singular value")
    for index, value in enumerate(logs):
        body.append(_bar(panel, float(index), 0.55, value, -15.0, "bar1" if index < rank else "bar3"))
    annotation = f"rank = {rank}"
    if condition is not None:
        annotation += f"; condition = {condition:.2f}"
    body.append(f'<text x="{panel.left+panel.width-5:.1f}" y="{panel.top+24:.1f}" text-anchor="end" class="label">{_esc(annotation)}</text>')
    return body


def _figure4(record: dict[str, Any], commit: str) -> str:
    width, height = 1480, 920
    body = [
        '<text x="35" y="38" class="title">Figure 4. Effective thickness moves cutoff; tail-only cutoffs remain rank deficient</text>',
        '<text x="35" y="62" class="synthetic">BOUNDED SYNTHETIC CHANG SENSITIVITY - NOT A PRODUCTION DETECTOR CORRECTION</text>',
    ]
    points = record["half_response_cutoffs"]
    xlog = [math.log10(float(row["effective_thickness_um"])) for row in points]
    energies = [1000.0 * float(row["energy_ev"]) for row in points]
    wavelengths = [float(row["wavelength_um"]) for row in points]
    tick_pairs = [(math.log10(value), str(value)) for value in (1, 2, 5, 10, 20)]
    p1 = Panel(85, 120, 620, 300, 0.0, math.log10(20.0), 75.0, 155.0)
    body += _axes(p1, "A. 50% response cutoff energy", tick_pairs, [(80, "80"), (100, "100"), (120, "120"), (140, "140")], "effective thickness (um, log scale)", "cutoff energy (meV)")
    body.append(_polyline(p1, xlog, energies, "line1"))
    for x, y, row in zip(xlog, energies, points, strict=True):
        fill = "#111" if row["branch"] == "tail" else "white"
        body.append(f'<circle cx="{p1.x(x):.2f}" cy="{p1.y(y):.2f}" r="5" fill="{fill}" stroke="#111" stroke-width="1.5"/>')

    p2 = Panel(820, 120, 560, 300, 0.0, math.log10(20.0), 7.5, 15.5)
    body += _axes(p2, "B. Equivalent cutoff wavelength", tick_pairs, [(8, "8"), (10, "10"), (12, "12"), (14, "14")], "effective thickness (um, log scale)", "cutoff wavelength (um)")
    body.append(_polyline(p2, xlog, wavelengths, "line1"))
    for x, y in zip(xlog, wavelengths, strict=True):
        body.append(f'<circle cx="{p2.x(x):.2f}" cy="{p2.y(y):.2f}" r="4.5" fill="#111"/>')

    p3 = Panel(85, 555, 620, 270, -0.5, 3.5, -15.0, 0.0)
    tail = record["all_tail_design"]
    body += _singular_panel(p3, "C. Tail-only cutoff singular values", tail["relative_singular_values"], int(tail["numerical_rank"]))
    p4 = Panel(820, 555, 560, 270, -0.5, 3.5, -15.0, 0.0)
    mixed = record["mixed_branch_design"]
    body += _singular_panel(p4, "D. Mixed intrinsic/tail singular values", mixed["relative_singular_values"], int(mixed["numerical_rank"]), float(mixed["condition_number"]))

    shift = record["thickness_results"]
    body += [
        f'<text x="690" y="470" text-anchor="end" class="label">5 to 20 um: {float(shift["source_valid_5_to_20_um_energy_shift_mev"]):.3f} meV</text>',
        f'<text x="830" y="470" class="label">{float(shift["source_valid_5_to_20_um_wavelength_shift_um"]):+.3f} um</text>',
        '<text x="690" y="495" text-anchor="end" class="small">open markers: intrinsic branch</text>',
        '<text x="830" y="495" class="small">filled markers: tail branch</text>',
    ]
    return _wrap_svg(width, height, "Chang cutoff and rank", body, commit=commit, sources=(RECORD_PATHS[2],), claim_ids=("C09", "C10", "C11", "C12"))


def _carrier_regeneration(record: dict[str, Any]) -> list[dict[str, float]]:
    parameters = record["declared_sensitivity_parameters"]
    regenerated: list[dict[str, float]] = []
    for source in record["density_crossover"]:
        result = carrier_filled_optical_edge_ev(
            zero_density_gap_ev=float(parameters["zero_density_gap_ev"]),
            electron_density_cm3=float(source["density_cm3"]),
            conduction_edge_mass_ratio=float(parameters["conduction_edge_mass_ratio"]),
            nonparabolicity_ev_inverse=float(parameters["nonparabolicity_ev_inverse"]),
            valence_mass_ratio=float(parameters["valence_mass_ratio"]),
            valley_degeneracy=float(parameters["valley_degeneracy"]),
        )
        parabolic = 1000.0 * result.parabolic_conduction_energy_ev
        nonparabolic = 1000.0 * result.nonparabolic_conduction_energy_ev
        overestimate = 1000.0 * result.parabolic_overestimate_ev
        for actual, expected in (
            (parabolic, source["parabolic_conduction_energy_mev"]),
            (nonparabolic, source["nonparabolic_conduction_energy_mev"]),
            (overestimate, source["parabolic_overestimate_mev"]),
        ):
            if not math.isclose(float(actual), float(expected), rel_tol=2.0e-10, abs_tol=2.0e-10):
                raise RuntimeError("carrier-density regeneration does not match immutable record")
        regenerated.append({
            "density": float(source["density_cm3"]),
            "parabolic": parabolic,
            "nonparabolic": nonparabolic,
            "overestimate": overestimate,
        })
    return regenerated


def _figure5(record: dict[str, Any], commit: str) -> str:
    data = _carrier_regeneration(record)
    width, height = 1480, 920
    body = [
        '<text x="35" y="38" class="title">Figure 5. Nonparabolic carrier filling and density-series conditioning</text>',
        '<text x="35" y="62" class="synthetic">BOUNDED SYNTHETIC SENSITIVITY IN THE DINGRONG DENSITY REGIME - NOT A SPECIMEN FIT</text>',
    ]
    xs = [math.log10(row["density"]) for row in data]
    p1 = Panel(85, 120, 620, 300, 14.0, math.log10(7.0e17), 0.0, 320.0)
    body += _axes(p1, "A. Conduction filling energy", [(14, "1e14"), (15, "1e15"), (16, "1e16"), (17, "1e17"), (math.log10(7e17), "7e17")], [(0, "0"), (80, "80"), (160, "160"), (240, "240"), (320, "320")], "electron density (cm^-3, log scale)", "conduction energy (meV)")
    body += [
        _polyline(p1, xs, [row["parabolic"] for row in data], "line2"),
        _polyline(p1, xs, [row["nonparabolic"] for row in data], "line1"),
        '<text x="520" y="145" class="small">solid: nonparabolic</text>',
        '<text x="520" y="165" class="small">dashed: parabolic</text>',
    ]

    p2 = Panel(820, 120, 560, 300, 14.0, math.log10(7.0e17), 0.0, 160.0)
    body += _axes(p2, "B. Parabolic overestimate", [(14, "1e14"), (15, "1e15"), (16, "1e16"), (17, "1e17"), (math.log10(7e17), "7e17")], [(0, "0"), (40, "40"), (80, "80"), (120, "120"), (160, "160")], "electron density (cm^-3, log scale)", "E_par - E_nonparabolic (meV)")
    body.append(_polyline(p2, xs, [row["overestimate"] for row in data], "line1"))
    source_result = record["dingrong_density_result"]
    body.append(f'<text x="{p2.left+p2.width-5:.1f}" y="{p2.top+24:.1f}" text-anchor="end" class="label">7e17 cm^-3: {1000*float(source_result["parabolic_overestimate_ev"]):.3f} meV</text>')

    p3 = Panel(85, 555, 620, 270, -0.5, 3.5, 0.0, 320.0)
    body += _axes(p3, "C. High-density energy decomposition", [(0, "nonpar. Ec"), (1, "valence"), (2, "nonpar. BM"), (3, "parab. BM")], [(0, "0"), (80, "80"), (160, "160"), (240, "240"), (320, "320")], "component", "energy (meV)")
    values = [
        1000.0 * float(source_result["nonparabolic_conduction_energy_ev"]),
        1000.0 * float(source_result["valence_recoil_energy_ev"]),
        1000.0 * float(source_result["nonparabolic_burstein_moss_shift_ev"]),
        1000.0 * float(source_result["parabolic_burstein_moss_shift_ev"]),
    ]
    for index, value in enumerate(values):
        body.append(_bar(p3, float(index), 0.55, value, 0.0, ("bar1", "bar3", "bar1", "bar2")[index]))
        body.append(f'<text x="{p3.x(index):.2f}" y="{p3.y(value)-7:.2f}" text-anchor="middle" class="small">{value:.1f}</text>')

    p4 = Panel(820, 555, 560, 270, -0.5, 4.5, -5.0, 0.0)
    design = record["five_density_identifiability_design"]
    logs = _log_relative(design["relative_singular_values"], floor=1e-6)
    body += _axes(p4, "D. Five-density relative singular values", [(i, str(i + 1)) for i in range(5)], [(-5, "1e-5"), (-4, "1e-4"), (-3, "1e-3"), (-2, "1e-2"), (-1, "1e-1"), (0, "1")], "singular direction", "log10 relative singular value")
    for index, value in enumerate(logs):
        body.append(_bar(p4, float(index), 0.55, value, -5.0, "bar1"))
    body.append(f'<text x="{p4.left+p4.width-5:.1f}" y="{p4.top+24:.1f}" text-anchor="end" class="label">condition = {float(design["condition_number"]):.2f}</text>')
    return _wrap_svg(width, height, "Carrier filling", body, commit=commit, sources=(RECORD_PATHS[3], "src/mct_research/carrier_filling.py"), claim_ids=("C13", "C14", "C15"))


def _unified_regeneration(record: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    design = record["reference_design"]
    energy = np.linspace(float(design["energy_lower_ev"]), float(design["energy_upper_ev"]), int(design["energy_points"]))
    common = {
        "gap_sigma_ev": float(design["gap_sigma_ev"]),
        "intrinsic_exponent": float(record["forward_model"]["fixed_intrinsic_exponent"]),
        "quadrature_order": int(design["quadrature_order"]),
    }
    first = record["exact_counterexample"]["parameter_set_1"]
    second = record["exact_counterexample"]["parameter_set_2"]
    response1 = unified_response_spectrum(
        energy,
        zero_density_gap_ev=float(first["zero_density_gap_ev"]),
        uniform_carrier_shift_ev=float(first["uniform_carrier_shift_ev"]),
        gap_sigma_ev=common["gap_sigma_ev"],
        intrinsic_exponent=common["intrinsic_exponent"],
        absorption_amplitude_cm_inverse_ev_power=float(first["absorption_amplitude_cm_inverse_ev_power"]),
        effective_thickness_um=float(first["effective_thickness_um"]),
        quadrature_order=common["quadrature_order"],
    )
    response2 = unified_response_spectrum(
        energy,
        zero_density_gap_ev=float(second["zero_density_gap_ev"]),
        uniform_carrier_shift_ev=float(second["uniform_carrier_shift_ev"]),
        gap_sigma_ev=common["gap_sigma_ev"],
        intrinsic_exponent=common["intrinsic_exponent"],
        absorption_amplitude_cm_inverse_ev_power=float(second["absorption_amplitude_cm_inverse_ev_power"]),
        effective_thickness_um=float(second["effective_thickness_um"]),
        quadrature_order=common["quadrature_order"],
    )
    maximum = float(np.max(np.abs(response1 - response2)))
    recorded = float(record["exact_counterexample"]["maximum_absolute_response_difference"])
    if maximum > 3.0e-15 or recorded > 3.0e-15:
        raise RuntimeError("unified exact counterexample no longer agrees to machine precision")
    return energy, response1, response2


def _figure6(record: dict[str, Any], commit: str) -> str:
    energy, response1, response2 = _unified_regeneration(record)
    width, height = 1480, 920
    body = [
        '<text x="35" y="38" class="title">Figure 6. Exact spectral equivalence and structural rank</text>',
        '<text x="35" y="62" class="synthetic">EXACT FORWARD-MODEL THEOREM WITH SYNTHETIC COUNTEREXAMPLE - NOT MATERIAL VALIDATION</text>',
    ]
    p1 = Panel(85, 120, 620, 300, 0.08, 0.22, 0.0, 1.0)
    body += _axes(p1, "A. Physically different parameter sets, identical response", [(0.08, "0.08"), (0.12, "0.12"), (0.16, "0.16"), (0.20, "0.20"), (0.22, "0.22")], [(0, "0"), (0.25, "0.25"), (0.5, "0.50"), (0.75, "0.75"), (1, "1.00")], "photon energy (eV)", "single-pass response")
    body += [
        _polyline(p1, energy.tolist(), response1.tolist(), "line1"),
        _polyline(p1, energy.tolist(), response2.tolist(), "line2"),
    ]
    maximum = float(np.max(np.abs(response1 - response2)))
    body.append(f'<text x="{p1.left+p1.width-5:.1f}" y="{p1.top+24:.1f}" text-anchor="end" class="label">max |difference| = {maximum:.2e}</text>')

    p2 = Panel(820, 120, 560, 300, -0.5, 4.5, -15.0, 0.0)
    unmarked = record["unmarked_dense_spectrum"]
    body += _singular_panel(p2, "B. Unmarked dense-spectrum singular values", unmarked["relative_singular_values"], int(unmarked["numerical_rank"]))

    p3 = Panel(85, 555, 620, 270, -0.5, 4.5, -15.0, 0.0)
    marked = record["nontranslational_carrier_marker"]
    body += _singular_panel(p3, "C. Marked-spectrum singular values", marked["relative_singular_values"], int(marked["numerical_rank"]))

    body += [
        '<rect x="820" y="555" width="560" height="270" rx="8" class="box"/>',
        '<text x="840" y="590" class="panel-title">D. Exact invariant combinations</text>',
        '<text x="850" y="635" class="label">Unmarked: Eg0 + Delta, sigma_G, A*d</text>',
        '<text x="850" y="675" class="label">Marked adds: Delta*d</text>',
        '<text x="850" y="725" class="label">remaining null vector:</text>',
        '<text x="850" y="760" class="panel-title">(Delta, -Delta, 0, -1, +1)</text>',
        '<text x="850" y="800" class="small">Known effective thickness removes the marked-model null.</text>',
    ]
    return _wrap_svg(width, height, "Unified structural rank", body, commit=commit, sources=(RECORD_PATHS[4], "src/mct_research/unified_spectrum.py"), claim_ids=("C16", "C17", "C18", "C19", "C20"))


def _figure7(commit: str) -> str:
    width, height = 1380, 760
    body = [
        '<text x="35" y="38" class="title">Figure 7. Measurement design and external-validation boundary</text>',
        '<text x="35" y="62" class="subtitle">Exact identifiability requirements do not depend on recruiting a collaborator</text>',
    ]
    columns = [
        (50, "Base spectrum", ["full calibrated spectrum", "rank 3 of 5", "two exact null directions"]),
        (485, "Required external constraints", ["carrier state + validated shift", "effective thickness or amplitude", "sufficient spectral range"]),
        (920, "Recoverable base parameters", ["latent Eg0", "gap width sigma_G", "absorption amplitude A"]),
    ]
    for x, title, lines in columns:
        body += [
            f'<rect x="{x}" y="120" width="360" height="220" rx="10" class="box"/>',
            f'<text x="{x+180}" y="160" text-anchor="middle" class="panel-title">{_esc(title)}</text>',
        ]
        for index, line in enumerate(lines):
            body.append(f'<text x="{x+25}" y="{205+38*index}" class="label">- {_esc(line)}</text>')
    body += [
        '<line x1="410" y1="230" x2="475" y2="230" class="axis"/>',
        '<line x1="845" y1="230" x2="910" y2="230" class="axis"/>',
        '<text x="35" y="410" class="panel-title">Validation status</text>',
    ]
    rows = [
        ("Transition distribution", "yes", "yes", "n/a", "no"),
        ("Herrmann tail", "yes", "yes", "yes", "no new specimen"),
        ("Chang cutoff", "yes", "yes", "source-bounded", "no"),
        ("Carrier filling", "yes", "yes", "regime anchor", "no"),
        ("Unified theorem", "yes", "yes", "n/a", "no"),
    ]
    headers = ["Component", "Analytical", "Numerical", "Source reproduction", "Real-spectrum validation"]
    x_positions = [45, 505, 680, 845, 1110]
    widths = [440, 155, 145, 245, 225]
    y0 = 445
    for x, w, label in zip(x_positions, widths, headers, strict=True):
        body += [
            f'<rect x="{x}" y="{y0}" width="{w}" height="42" fill="#e8e8e8" stroke="#111"/>',
            f'<text x="{x+w/2}" y="{y0+26}" text-anchor="middle" class="small">{_esc(label)}</text>',
        ]
    for row_index, row in enumerate(rows):
        y = y0 + 42 + 42 * row_index
        for x, w, value in zip(x_positions, widths, row, strict=True):
            body += [
                f'<rect x="{x}" y="{y}" width="{w}" height="42" fill="white" stroke="#999"/>',
                f'<text x="{x+8 if x == x_positions[0] else x+w/2}" y="{y+26}" '
                f'text-anchor="{"start" if x == x_positions[0] else "middle"}" class="small">{_esc(value)}</text>',
            ]
    body += [
        '<text x="690" y="735" text-anchor="middle" class="synthetic">ANALYTICAL CORE COMPLETE; EXTERNAL SPECIMEN VALIDATION REMAINS OPEN</text>',
    ]
    return _wrap_svg(width, height, "Measurement design", body, commit=commit, sources=("manuscript/distributional_band_edge/claim_matrix.md",), claim_ids=("C20", "C21", "C22", "C23"))


def _table1() -> str:
    rows = [
        ("Proposition 1", "narrow composition distribution", "mean curvature bias and local gap width", "exact asymptotic"),
        ("Proposition 2", "simple transition root", "dTc/dx = -Eg_x/Eg_T", "exact local"),
        ("Proposition 3", "Gaussian gaps; power-law local edge", "A sigma_G^p F_p((E-mu)/sigma_G)", "exact scale form"),
        ("Theorem 1", "single-pass exponential tail", "cutoff shift = -W ln(d2/d1)", "exact"),
        ("Theorem 2", "tail-only Chang cutoffs", "rank(J_tail) <= 2", "exact structural"),
        ("Proposition 4", "Kane-type isotropic dispersion", "exact nonparabolic positive root", "exact"),
        ("Proposition 5", "one scalar edge", "rank <= 1", "exact dimensional"),
        ("Theorem 3", "unmarked unified spectrum", "rank(J) <= 3", "exact structural"),
        ("Theorem 4", "absolutely calibrated carrier marker", "rank <= 4 with combined null", "exact structural"),
        ("Corollary", "base unified model", "carrier and optical-scale constraints required", "measurement design"),
    ]
    lines = [
        "# Table 1. Theorem and proposition summary",
        "",
        "| Label | Assumptions | Result | Evidence class |",
        "|---|---|---|---|",
    ]
    lines.extend(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows)
    return "\n".join(lines) + "\n"


def _table2(records: dict[str, dict[str, Any]]) -> str:
    transition = records[RECORD_PATHS[0]]
    herrmann = records[RECORD_PATHS[1]]
    chang = records[RECORD_PATHS[2]]
    carrier = records[RECORD_PATHS[3]]
    unified = records[RECORD_PATHS[4]]
    rows = [
        ("Latent-law central Tc span", f'{transition["cross_model_results"]["central_critical_temperature_span_k"]:.4f} K', "bounded model comparison"),
        ("Herrmann source-window W_fit/s", f'{herrmann["derived_results"]["square_root_source_window_tail_energy_over_s"]:.5f}', "source reproduction"),
        ("Tail-energy fit-window increase", f'{100*herrmann["derived_results"]["fit_window_increase_fraction"]:.1f}% ', "synthetic observation sensitivity"),
        ("5-to-20 um cutoff energy shift", f'{chang["thickness_results"]["source_valid_5_to_20_um_energy_shift_mev"]:.3f} meV', "synthetic Chang sensitivity"),
        ("Parabolic carrier overestimate", f'{1000*carrier["dingrong_density_result"]["parabolic_overestimate_ev"]:.3f} meV', "synthetic Dingrong-regime sensitivity"),
        ("Carrier density-series condition", f'{carrier["five_density_identifiability_design"]["condition_number"]:.2f}', "numerical identifiability"),
        ("Unmarked unified rank", f'{unified["unmarked_dense_spectrum"]["numerical_rank"]} of 5', "exact theorem + numerical verification"),
        ("Exact-counterexample max difference", f'{unified["exact_counterexample"]["maximum_absolute_response_difference"]:.2e}', "numerical verification"),
        ("Marked unified rank", f'{unified["nontranslational_carrier_marker"]["numerical_rank"]} of 5', "exact theorem + numerical verification"),
    ]
    lines = [
        "# Table 2. Quantitative headline results",
        "",
        "| Result | Value | Claim state |",
        "|---|---:|---|",
    ]
    lines.extend(f"| {a} | {b} | {c} |" for a, b, c in rows)
    return "\n".join(lines) + "\n"


def _table3(root: Path) -> str:
    source = (root / "manuscript/distributional_band_edge/claim_matrix.md").read_text(encoding="utf-8")
    rows: list[list[str]] = []
    for line in source.splitlines():
        if not line.startswith("| C"):
            continue
        columns = [column.strip() for column in line.strip().strip("|").split("|")]
        if len(columns) >= 5:
            rows.append([columns[0], columns[2], columns[4]])
    if len(rows) != 23:
        raise RuntimeError("claim matrix must contain exactly 23 claim rows")
    lines = [
        "# Table 3. Claim provenance and validation status",
        "",
        "| Claim ID | Claim class | Current status |",
        "|---|---|---|",
    ]
    lines.extend(f"| {a} | {b} | {c} |" for a, b, c in rows)
    return "\n".join(lines) + "\n"


def build(repository_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    output = Path(output_dir)
    if not output.is_absolute():
        output = (Path.cwd() / output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    commit = _git_commit(root)
    records = {path: _load_json(root, path) for path in RECORD_PATHS}

    figures = {
        FIGURE_FILES[0]: _figure1(commit),
        FIGURE_FILES[1]: _figure2(records[RECORD_PATHS[0]], commit),
        FIGURE_FILES[2]: _figure3(records[RECORD_PATHS[1]], commit),
        FIGURE_FILES[3]: _figure4(records[RECORD_PATHS[2]], commit),
        FIGURE_FILES[4]: _figure5(records[RECORD_PATHS[3]], commit),
        FIGURE_FILES[5]: _figure6(records[RECORD_PATHS[4]], commit),
        FIGURE_FILES[6]: _figure7(commit),
    }
    tables = {
        TABLE_FILES[0]: _table1(),
        TABLE_FILES[1]: _table2(records),
        TABLE_FILES[2]: _table3(root),
    }
    for name, content in {**figures, **tables}.items():
        (output / name).write_text(content, encoding="utf-8")

    summary = {
        "schema_version": "1.0",
        "generated_from_commit": commit,
        "generated_files": sorted([*figures, *tables]),
        "figure_count": len(figures),
        "table_count": len(tables),
        "source_records": list(RECORD_PATHS),
        "external_material_validation": False,
        "claim_boundary": "Rendered assets remain analytical, source-reproduction, or bounded synthetic outputs; they do not establish specimen-level validation.",
    }
    (output / "distributional_band_edge_asset_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = build(args.repository_root, args.output_dir)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
