"""Generate the real-spectrum observation-model SVG."""
from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

import numpy as np

from tools.analyze_moazzami2005_real_spectra import build_contract


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
        "fractional_power_free": "fractional p free",
        "fractional_power_p_0.5": "fractional p=0.5",
        "fractional_power_p_0.7": "fractional p=0.7",
        "fractional_power_p_0.872": "fractional p=0.872",
        "fractional_power_p_1": "fractional p=1",
        "chu_1994_kane_region": "Chu 1994 Kane",
    }
    return labels.get(identifier, identifier)


def polyline(points: list[tuple[float, float]], attrs: str) -> str:
    values = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{values}" fill="none" {attrs}/>'


def build_spectrum_svg(root: Path, base: dict[str, Any]) -> str:
    contract, _ = build_contract(
        root / "data/manuscript/moazzami2005_figure6a_irse_digitized.csv",
        root / "data/manuscript/moazzami2005_figure6a_irse_calibration.json",
    )
    energy = np.asarray(contract["spectrum"]["energy_ev"], dtype=float)
    absorption = np.asarray(contract["spectrum"]["absorption_cm1"], dtype=float)
    candidates = base["specimens"][0]["contract_result"]["model_candidates"]
    width, height = 980, 650
    left, top, plot_w, plot_h = 105, 75, 840, 490
    xmin, xmax, ymin, ymax = 0.17, 0.30, 1.8, 4.0
    xmap = lambda value: left + plot_w * (value - xmin) / (xmax - xmin)
    ymap = lambda value: top + plot_h * (ymax - math.log10(value)) / (ymax - ymin)
    body = [
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#111}.grid{stroke:#ddd}.axis{stroke:#111;stroke-width:1.4}.small{font-size:12px}.label{font-size:15px}.title{font-size:20px;font-weight:700}</style>',
        '<text x="35" y="34" class="title">Figure 1. Real HgCdTe spectrum and fitted observation models</text>',
        '<text x="525" y="58" text-anchor="middle" class="label">Moazzami 2005 Figure 6a, x=0.226, 300 K, solid IRSE trace</text>',
    ]
    for tick in (0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30):
        x = xmap(tick)
        body += [
            f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top+plot_h}" class="grid"/>',
            f'<text x="{x:.2f}" y="592" text-anchor="middle" class="label">{tick:.2f}</text>',
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
        '<text x="525" y="628" text-anchor="middle" class="label">Photon energy (eV)</text>',
        '<text transform="translate(28 320) rotate(-90)" text-anchor="middle" class="label">Absorption coefficient (cm-1)</text>',
        polyline(
            [(xmap(float(e)), ymap(float(a))) for e, a in zip(energy, absorption, strict=True)],
            'stroke="#111" stroke-width="2.4"',
        ),
    ]
    patterns = ("", "9 5", "3 4", "12 4 3 4", "2 3", "7 3 2 3")
    samples = np.linspace(xmin, xmax, 160)
    for index, candidate in enumerate(candidates):
        values = curve(candidate, samples)
        valid = (
            (values > 10**ymin)
            & (values < 10**ymax)
            & (samples > float(candidate["edge_ev"]))
        )
        dash = f' stroke-dasharray="{patterns[index]}"' if patterns[index] else ""
        body.append(
            polyline(
                [(xmap(float(e)), ymap(float(a))) for e, a in zip(samples[valid], values[valid], strict=True)],
                f'stroke="#666" stroke-width="1.5"{dash}',
            )
        )
        y = 92 + index * 23
        body += [
            f'<line x1="615" y1="{y}" x2="657" y2="{y}" stroke="#666" stroke-width="1.5"{dash}/>',
            f'<text x="664" y="{y+4}" class="small">{esc(label(candidate["candidate_id"]))}</text>',
        ]
    body += [
        '<line x1="615" y1="230" x2="657" y2="230" stroke="#111" stroke-width="2.4"/>',
        '<text x="664" y="234" class="small">digitized IRSE trace</text>',
        '<text x="108" y="610" class="small">Observation models are compared; none is selected as the material gap.</text>',
    ]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>Real spectrum and fitted observation models</title>'
        + "".join(body)
        + "</svg>\n"
    )
