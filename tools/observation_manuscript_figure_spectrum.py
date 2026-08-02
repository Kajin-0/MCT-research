"""Generate the real-spectrum observation-model SVG."""
from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

import numpy as np

from tools.analyze_moazzami2005_real_spectra import build_contract


COLORS = (
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # green
    "#CC79A7",  # reddish purple
    "#E69F00",  # orange
    "#7A4EAB",  # purple
)
DASHES = ("", "9 5", "3 4", "12 4 3 4", "2 3", "7 3 2 3")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def curve(candidate: dict[str, Any], energy: np.ndarray) -> np.ndarray:
    delta = np.maximum(energy - float(candidate["edge_ev"]), 0.0)
    if candidate["candidate_id"] == "chu_1994_kane_region":
        return float(candidate["alpha_g_cm1"]) * np.exp(
            np.sqrt(float(candidate["beta_ev_inverse"]) * delta)
        )
    return (
        float(candidate["amplitude"])
        * np.power(delta, float(candidate["exponent"]))
        / energy
    )


def label(identifier: str) -> str:
    labels = {
        "fractional_power_free": "fractional power, free p",
        "fractional_power_p_0.5": "fractional power, p=0.5",
        "fractional_power_p_0.7": "fractional power, p=0.7",
        "fractional_power_p_0.872": "source-panel p=0.872",
        "fractional_power_p_1": "fractional power, p=1",
        "chu_1994_kane_region": "Chu 1994 Kane-region",
    }
    return labels.get(identifier, identifier)


def polyline(points: list[tuple[float, float]], attrs: str) -> str:
    values = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{values}" fill="none" {attrs}/>'


def build_spectrum_svg(root: Path, base: dict[str, Any]) -> str:
    csv_path = root / "data/manuscript/moazzami2005_figure6a_irse_digitized.csv"
    calibration_path = root / "data/manuscript/moazzami2005_figure6a_irse_calibration.json"
    contract, _ = build_contract(csv_path, calibration_path)
    energy = np.asarray(contract["spectrum"]["energy_ev"], dtype=float)
    absorption = np.asarray(contract["spectrum"]["absorption_cm1"], dtype=float)
    candidates = base["specimens"][0]["contract_result"]["model_candidates"]
    low, high = (
        float(value)
        for value in contract["analysis_assumptions"]["fit_absorption_window_cm1"]
    )
    fit_mask = (absorption >= low) & (absorption <= high)
    fit_indices = np.flatnonzero(fit_mask)
    fit_min = float(energy[fit_indices[0]])
    fit_max = float(energy[fit_indices[-1]])

    width, height = 1220, 700
    left, top, plot_w, plot_h = 105, 95, 760, 490
    legend_x = 910
    xmin, xmax, ymin, ymax = 0.17, 0.30, 1.8, 4.0
    xmap = lambda value: left + plot_w * (value - xmin) / (xmax - xmin)
    ymap = lambda value: top + plot_h * (ymax - math.log10(value)) / (ymax - ymin)

    body = [
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>'
        'text{font-family:Arial,Helvetica,sans-serif;fill:#151515}'
        '.grid{stroke:#e2e2e2;stroke-width:1}'
        '.axis{stroke:#151515;stroke-width:1.5}'
        '.small{font-size:12px}'
        '.note{font-size:12px;fill:#4a4a4a}'
        '.label{font-size:15px}'
        '.title{font-size:21px;font-weight:700}'
        '.subtitle{font-size:14px;fill:#333}'
        '.legend-title{font-size:14px;font-weight:700}'
        '</style>',
        '<text x="35" y="35" class="title">Reconstructed published HgCdTe spectrum and fitted extraction models</text>',
        '<text x="485" y="64" text-anchor="middle" class="subtitle">Moazzami 2005 Figure 6a; x=0.226, T=300 K, thickness=15.40 um</text>',
        f'<rect x="{xmap(fit_min):.2f}" y="{top}" width="{xmap(fit_max)-xmap(fit_min):.2f}" height="{plot_h}" fill="#f4f6f8"/>',
    ]

    for tick in (0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30):
        x = xmap(tick)
        body += [
            f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top+plot_h}" class="grid"/>',
            f'<text x="{x:.2f}" y="612" text-anchor="middle" class="label">{tick:.2f}</text>',
        ]
    for exponent in (2, 3, 4):
        y = top + plot_h * (ymax - exponent) / (ymax - ymin)
        body += [
            f'<line x1="{left}" y1="{y:.2f}" x2="{left+plot_w}" y2="{y:.2f}" class="grid"/>',
            f'<text x="87" y="{y+5:.2f}" text-anchor="end" class="label">10^{exponent}</text>',
        ]

    body += [
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" class="axis"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" class="axis"/>',
        '<text x="485" y="652" text-anchor="middle" class="label">Photon energy E (eV)</text>',
        '<text transform="translate(30 340) rotate(-90)" text-anchor="middle" class="label">Absorption coefficient alpha (cm-1)</text>',
        polyline(
            [(xmap(float(e)), ymap(float(a))) for e, a in zip(energy, absorption, strict=True)],
            'stroke="#9a9a9a" stroke-width="1.2" stroke-linejoin="round" stroke-linecap="round"',
        ),
    ]

    for index in np.flatnonzero(~fit_mask):
        body.append(
            f'<circle cx="{xmap(float(energy[index])):.2f}" cy="{ymap(float(absorption[index])):.2f}" r="2.0" fill="#9a9a9a"/>'
        )
    for index in fit_indices:
        body.append(
            f'<circle cx="{xmap(float(energy[index])):.2f}" cy="{ymap(float(absorption[index])):.2f}" r="2.25" fill="#111111"/>'
        )

    samples = np.linspace(fit_min, fit_max, 160)
    for index, candidate in enumerate(candidates):
        values = curve(candidate, samples)
        valid = (
            (values > 10**ymin)
            & (values < 10**ymax)
            & (samples > float(candidate["edge_ev"]))
        )
        dash = f' stroke-dasharray="{DASHES[index]}"' if DASHES[index] else ""
        body.append(
            polyline(
                [
                    (xmap(float(e)), ymap(float(a)))
                    for e, a in zip(samples[valid], values[valid], strict=True)
                ],
                f'stroke="{COLORS[index]}" stroke-width="2.0"{dash}',
            )
        )

    body += [
        f'<line x1="{xmap(fit_min):.2f}" y1="{top+8}" x2="{xmap(fit_max):.2f}" y2="{top+8}" stroke="#444" stroke-width="1.2"/>',
        f'<line x1="{xmap(fit_min):.2f}" y1="{top+3}" x2="{xmap(fit_min):.2f}" y2="{top+13}" stroke="#444" stroke-width="1.2"/>',
        f'<line x1="{xmap(fit_max):.2f}" y1="{top+3}" x2="{xmap(fit_max):.2f}" y2="{top+13}" stroke="#444" stroke-width="1.2"/>',
        f'<text x="{0.5*(xmap(fit_min)+xmap(fit_max)):.2f}" y="{top+29}" text-anchor="middle" class="small">declared fit population: 600-5000 cm-1</text>',
    ]

    body += [
        f'<rect x="{legend_x-18}" y="92" width="285" height="328" rx="6" fill="#ffffff" stroke="#c8c8c8"/>',
        f'<text x="{legend_x}" y="120" class="legend-title">Reconstructed coordinates</text>',
        f'<line x1="{legend_x}" y1="145" x2="{legend_x+42}" y2="145" stroke="#9a9a9a" stroke-width="1.2"/>',
        f'<circle cx="{legend_x+21}" cy="145" r="2" fill="#9a9a9a"/>',
        f'<text x="{legend_x+53}" y="150" class="small">outside declared fit population</text>',
        f'<line x1="{legend_x}" y1="172" x2="{legend_x+42}" y2="172" stroke="#9a9a9a" stroke-width="1.2"/>',
        f'<circle cx="{legend_x+21}" cy="172" r="2.25" fill="#111"/>',
        f'<text x="{legend_x+53}" y="177" class="small">used in fitted-model analysis</text>',
        f'<text x="{legend_x}" y="216" class="legend-title">Fitted extraction models</text>',
    ]
    for index, candidate in enumerate(candidates):
        y = 244 + index * 28
        dash = f' stroke-dasharray="{DASHES[index]}"' if DASHES[index] else ""
        body += [
            f'<line x1="{legend_x}" y1="{y}" x2="{legend_x+42}" y2="{y}" stroke="{COLORS[index]}" stroke-width="2.0"{dash}/>',
            f'<text x="{legend_x+53}" y="{y+4}" class="small">{esc(label(candidate["candidate_id"]))}</text>',
        ]

    body += [
        f'<text x="{legend_x-18}" y="458" class="note">Coordinates were reconstructed from a published bitmap,</text>',
        f'<text x="{legend_x-18}" y="476" class="note">not obtained from the native ellipsometer export.</text>',
        f'<text x="{legend_x-18}" y="506" class="note">A local two-point reconstruction irregularity was tested</text>',
        f'<text x="{legend_x-18}" y="524" class="note">separately and is not highlighted as a physical feature.</text>',
    ]

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>Reconstructed spectrum and fitted extraction models</title>'
        + "".join(body)
        + "</svg>\n"
    )
