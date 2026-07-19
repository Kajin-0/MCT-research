#!/usr/bin/env python3
"""Build deterministic tables and SVG figures for the observation-model manuscript."""
from __future__ import annotations

import argparse
import csv
import html
import json
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from tools.analyze_moazzami2005_manuscript_comparators import analyze as compare_models
from tools.analyze_moazzami2005_real_spectra import analyze as analyze_real_spectra, build_contract
from tools.audit_moazzami2005_digitization_sensitivity import audit as audit_digitization

MODEL_LABELS = {
    "hansen": "Hansen",
    "published_seiler": "Seiler 1990",
    "laurenti": "Laurenti",
    "provisional_hansen_pade": "Provisional Pade",
}
MODEL_ORDER = tuple(MODEL_LABELS)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def svg_document(width: int, height: int, body: Iterable[str], title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">\n'
        '<rect width="100%" height="100%" fill="white"/>\n'
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111}'
        '.axis{stroke:#111;stroke-width:1.4}.grid{stroke:#ddd;stroke-width:1}'
        '.label{font-size:15px}.small{font-size:12px}.title{font-size:20px;font-weight:700}'
        '.panel{font-size:17px;font-weight:700}</style>\n'
        f'<title>{esc(title)}</title>\n' + "\n".join(body) + "\n</svg>\n"
    )


def polyline(points: list[tuple[float, float]], **attrs: Any) -> str:
    coordinates = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
    rendered = " ".join(
        f'{key.replace("_", "-")}="{esc(value)}"' for key, value in attrs.items()
    )
    return f'<polyline points="{coordinates}" fill="none" {rendered}/>'


def candidate_label(identifier: str) -> str:
    replacements = {
        "fractional_power_free": "fractional p free",
        "fractional_power_p_0.5": "fractional p=0.5",
        "fractional_power_p_0.7": "fractional p=0.7",
        "fractional_power_p_0.872": "fractional p=0.872",
        "fractional_power_p_0.849": "fractional p=0.849",
        "fractional_power_p_1": "fractional p=1",
        "chu_1994_kane_region": "Chu 1994 Kane",
    }
    if identifier in replacements:
        return replacements[identifier]
    if identifier.startswith("threshold_"):
        return identifier.removeprefix("threshold_").replace("_cm-1", " cm-1")
    return identifier


def fractional_curve(candidate: dict[str, Any], energy: np.ndarray) -> np.ndarray:
    edge = float(candidate["edge_ev"])
    delta = np.maximum(energy - edge, 0.0)
    return float(candidate["amplitude"]) * np.power(delta, float(candidate["exponent"])) / energy


def chu_curve(candidate: dict[str, Any], energy: np.ndarray) -> np.ndarray:
    delta = np.maximum(energy - float(candidate["edge_ev"]), 0.0)
    return float(candidate["alpha_g_cm1"]) * np.exp(
        np.sqrt(float(candidate["beta_ev_inverse"]) * delta)
    )


def figure1(root: Path, base: dict[str, Any]) -> str:
    contract, _ = build_contract(
        root / "data/manuscript/moazzami2005_figure6a_irse_digitized.csv",
        root / "data/manuscript/moazzami2005_figure6a_irse_calibration.json",
    )
    energy = np.asarray(contract["spectrum"]["energy_ev"], dtype=float)
    absorption = np.asarray(contract["spectrum"]["absorption_cm1"], dtype=float)
    candidates = base["specimens"][0]["contract_result"]["model_candidates"]
    width, height = 980, 650
    left, right, top, bottom = 105, 35, 75, 85
    plot_w, plot_h = width - left - right, height - top - bottom
    xmin, xmax, ymin, ymax = 0.17, 0.30, 1.8, 4.0
    xmap = lambda v: left + plot_w * (v - xmin) / (xmax - xmin)
    ymap = lambda v: top + plot_h * (ymax - math.log10(v)) / (ymax - ymin)
    body = [
        '<text x="35" y="34" class="title">Figure 1. Real HgCdTe spectrum and fitted observation models</text>',
        f'<text x="{left + plot_w / 2:.1f}" y="58" text-anchor="middle" class="label">Moazzami 2005 Figure 6a, x=0.226, 300 K, solid IRSE trace</text>',
    ]
    for tick in (0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30):
        x = xmap(tick)
        body += [
            f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_h}" class="grid"/>',
            f'<text x="{x:.2f}" y="{top + plot_h + 27}" text-anchor="middle" class="label">{tick:.2f}</text>',
        ]
    for exponent, label in ((2, "10^2"), (3, "10^3"), (4, "10^4")):
        y = top + plot_h * (ymax - exponent) / (ymax - ymin)
        body += [
            f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" class="grid"/>',
            f'<text x="{left - 18}" y="{y + 5:.2f}" text-anchor="end" class="label">{label}</text>',
        ]
    body += [
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="axis"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="axis"/>',
        f'<text x="{left + plot_w / 2:.1f}" y="{height - 25}" text-anchor="middle" class="label">Photon energy (eV)</text>',
        f'<text transform="translate(30 {top + plot_h / 2:.1f}) rotate(-90)" text-anchor="middle" class="label">Absorption coefficient (cm-1)</text>',
        polyline([(xmap(float(e)), ymap(float(a))) for e, a in zip(energy, absorption, strict=True)], stroke="#111", stroke_width="2.4"),
    ]
    dash_patterns = ("", "9 5", "3 4", "12 4 3 4", "2 3", "7 3 2 3")
    curve_energy = np.linspace(xmin, xmax, 420)
    for index, candidate in enumerate(candidates):
        values = chu_curve(candidate, curve_energy) if candidate["candidate_id"] == "chu_1994_kane_region" else fractional_curve(candidate, curve_energy)
        valid = (values > 10**ymin) & (values < 10**ymax) & (curve_energy > float(candidate["edge_ev"]))
        points = [(xmap(float(e)), ymap(float(a))) for e, a in zip(curve_energy[valid], values[valid], strict=True)]
        attrs: dict[str, Any] = {"stroke": "#666", "stroke_width": "1.5"}
        if dash_patterns[index]:
            attrs["stroke_dasharray"] = dash_patterns[index]
        if points:
            body.append(polyline(points, **attrs))
        ly = 92 + index * 23
        body += [
            f'<line x1="615" y1="{ly}" x2="657" y2="{ly}" stroke="#666" stroke-width="1.5" stroke-dasharray="{dash_patterns[index]}"/>',
            f'<text x="664" y="{ly + 4}" class="small">{esc(candidate_label(candidate["candidate_id"]))}</text>',
        ]
    body += [
        '<line x1="615" y1="230" x2="657" y2="230" stroke="#111" stroke-width="2.4"/>',
        '<text x="664" y="234" class="small">digitized IRSE trace</text>',
        '<text x="108" y="600" class="small">Observation models are compared; none is selected as the material gap.</text>',
    ]
    return svg_document(width, height, body, "Real spectrum and fitted observation models")


def figure2(comparison: dict[str, Any]) -> str:
    width, height = 1180, 690
    left_label, panel_w, gap, top, bottom = 180, 420, 85, 75, 55
    rows = comparison["specimens"][0]["candidates"]
    row_h = (height - top - bottom) / len(rows)
    panels = [
        (comparison["specimens"][0], left_label, 178.0, 275.0),
        (comparison["specimens"][1], left_label + panel_w + gap, 286.0, 356.0),
    ]
    body = ['<text x="35" y="34" class="title">Figure 2. Extracted edge depends on observation definition</text>']
    for index, row in enumerate(rows):
        y = top + (index + 0.5) * row_h
        body.append(f'<text x="{left_label - 12}" y="{y + 4:.2f}" text-anchor="end" class="small">{esc(candidate_label(row["candidate_id"]))}</text>')
        if index == 6:
            body.append(f'<line x1="35" y1="{y - row_h / 2:.2f}" x2="{width - 35}" y2="{y - row_h / 2:.2f}" stroke="#999" stroke-width="1.2"/>')
    for specimen, left, xmin, xmax in panels:
        body.append(f'<text x="{left + panel_w / 2:.1f}" y="58" text-anchor="middle" class="panel">x={specimen["composition_x"]:.3f}, 300 K</text>')
        for tick in np.linspace(xmin, xmax, 5):
            x = left + panel_w * (float(tick) - xmin) / (xmax - xmin)
            body += [
                f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{height - bottom}" class="grid"/>',
                f'<text x="{x:.2f}" y="{height - 24}" text-anchor="middle" class="small">{tick:.0f}</text>',
            ]
        body.append(f'<line x1="{left}" y1="{height - bottom}" x2="{left + panel_w}" y2="{height - bottom}" class="axis"/>')
        for index, row in enumerate(specimen["candidates"]):
            y = top + (index + 0.5) * row_h
            x = left + panel_w * (float(row["edge_mev"]) - xmin) / (xmax - xmin)
            if row["boundary_limited"]:
                body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.2" fill="white" stroke="#111" stroke-width="1.8"/>')
            else:
                body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5" fill="#111"/>')
    body += [
        f'<text x="{left_label + panel_w + gap / 2:.1f}" y="{height - 5}" text-anchor="middle" class="label">Extracted edge (meV)</text>',
        '<circle cx="910" cy="55" r="5.2" fill="white" stroke="#111" stroke-width="1.8"/>',
        '<text x="923" y="59" class="small">boundary-limited fit</text>',
    ]
    return svg_document(width, height, body, "Extracted edge by observation definition")


def figure3(base: dict[str, Any], comparison: dict[str, Any]) -> str:
    width, height = 1050, 670
    left, right, top, bottom = 90, 35, 90, 100
    plot_w, plot_h = width - left - right, height - top - bottom
    ymin, ymax = -130.0, 30.0
    ymap = lambda value: top + plot_h * (ymax - value) / (ymax - ymin)
    body = ['<text x="35" y="34" class="title">Figure 3. Material-model residual intervals from the observation ensemble</text>']
    for tick in (-120, -90, -60, -30, 0, 30):
        y = ymap(float(tick))
        body += [
            f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" class="grid"/>',
            f'<text x="{left - 14}" y="{y + 5:.2f}" text-anchor="end" class="label">{tick}</text>',
        ]
    body += [
        f'<line x1="{left}" y1="{ymap(0):.2f}" x2="{left + plot_w}" y2="{ymap(0):.2f}" stroke="#111" stroke-width="1.8"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="axis"/>',
        f'<text transform="translate(27 {top + plot_h / 2:.1f}) rotate(-90)" text-anchor="middle" class="label">Observation edge minus model prediction (meV)</text>',
    ]
    group_w = plot_w / len(MODEL_ORDER)
    for model_index, model in enumerate(MODEL_ORDER):
        center = left + (model_index + 0.5) * group_w
        body.append(f'<text x="{center:.2f}" y="{height - 52}" text-anchor="middle" class="label">{esc(MODEL_LABELS[model])}</text>')
        for specimen_index, (base_specimen, comparison_specimen) in enumerate(zip(base["specimens"], comparison["specimens"], strict=True)):
            x = center + (-18.0, 18.0)[specimen_index]
            prediction = float(comparison_specimen["model_predictions_mev"][model])
            model_low = 1000.0 * float(base_specimen["model_family_envelope"]["minimum_edge_ev"]) - prediction
            model_high = 1000.0 * float(base_specimen["model_family_envelope"]["maximum_edge_ev"]) - prediction
            stable = [float(row["edge_mev"]) for row in comparison_specimen["candidates"] if row["observation_class"] == "fixed_absorption_threshold" and row["candidate_id"] != "threshold_5000_cm-1"]
            dash = "" if specimen_index == 0 else "5 4"
            body += [
                f'<line x1="{x:.2f}" y1="{ymap(min(stable) - prediction):.2f}" x2="{x:.2f}" y2="{ymap(max(stable) - prediction):.2f}" stroke="#999" stroke-width="7" stroke-linecap="round" stroke-dasharray="{dash}"/>',
                f'<line x1="{x:.2f}" y1="{ymap(model_low):.2f}" x2="{x:.2f}" y2="{yma@¡µ½‘•±}¡¥ ¤è¸É™ôˆÍÑÉ½­”ôˆŒÄÄÄˆÍÑÉ½­”µÝ¥‘Ñ ôˆÌˆÍÑÉ½­”µ±¥¹•…Àô‰É½Õ¹ˆÍÑÉ½­”µ‘…Í¡…ÉÉ…äô‰í‘…Í¡ôˆ¼øœ°(€€€€€€€€€t(€€€‰½‘ä€¬ôl(€€€€€€€€œñ±¥¹”àÄôˆÔÜÀˆäÄôˆÔÔˆàÈôˆØÄÀˆäÈôˆÔÔˆÍÑÉ½­”ôˆŒÄÄÄˆÍÑÉ½­”µÝ¥‘Ñ ôˆÌˆ¼øœ°(€€€€€€€€œñÑ•áÐàôˆØÄàˆäôˆÔäˆ±…ÍÌô‰Íµ…±°ˆù™¥ÑÑ•µµ½‘•°•¹Ù•±½Á”ð½Ñ•áÐøœ°(€€€€€€€€œñ±¥¹”àÄôˆÜàÀˆäÄôˆÔÔˆàÈôˆàÈÀˆäÈôˆÔÔˆÍÑÉ½­”ôˆŒäääˆÍÑÉ½­”µÝ¥‘Ñ ôˆÜˆ¼øœ°(€€€€€€€€œñÑ•áÐàôˆàÈàˆäôˆÔäˆ±…ÍÌô‰Íµ…±°ˆøÐÀÀ´ÐÀÀÀ´´ÄÑ¡É•Í¡½±‘Ìð½Ñ•áÐøœ°(€€€€€€€˜œñÑ•áÐàô‰í±•™Ð€¬Á±½Ñ}Ü€¼€Èè¸Å™ôˆäô‰í¡•¥¡Ð€´€ÄáôˆÑ•áÐµ…¹¡½Èô‰µ¥‘‘±”ˆ±…ÍÌô‰Íµ…±°ˆù%¹Ñ•ÉÙ…±Ì…É”½‰Í•ÉÙ…Ñ¥½¸µ‘•™¥¹¥Ñ¥½¸Í•¹Í¥Ñ¥Ù¥Ñä°¹½ÐÍÑ…Ñ¥ÍÑ¥…°½¹™¥‘•¹”¥¹Ñ•ÉÙ…±Ì¸ð½Ñ•áÐøœ°(€€€t(€€€É•ÑÕÉ¸ÍÙ}‘½Õµ•¹Ð¡Ý¥‘Ñ °¡•¥¡Ð°‰½‘ä°€‰5…Ñ•É¥…°µµ½‘•°É•Í¥‘Õ…°¥¹Ñ•ÉÙ…±Ìˆ¤(()‘•˜‰Õ¥±¡É½½ÐèÍÑÈðA…Ñ °½ÕÑÁÕÑ}‘¥ÈèÍÑÈðA…Ñ ¤€´ø‘¥ÑmÍÑÈ°¹åtè(€€€É½½Ð°½ÕÑÁÕÐ€ôA…Ñ ¡É½½Ð¤°A…Ñ ¡½ÕÑÁÕÑ}‘¥È¤(€€€½ÕÑÁÕÐ¹µ­‘¥È¡Á…É•¹ÑÌõQÉÕ”°•á¥ÍÑ}½¬õQÉÕ”¤(€€€‰…Í”€ô…¹…±åé•}É•…±}ÍÁ•ÑÉ„¡É½½Ð¤(€€€½µÁ…É¥Í½¸€ô½µÁ…É•}µ½‘•±Ì¡É½½Ð¤(€€€Í•¹Í¥Ñ¥Ù¥Ñä€ô…Õ‘¥Ñ}‘¥¥Ñ¥é…Ñ¥½¸¡É½½Ð¤(€€€Í•¹Í¥Ñ¥Ù¥Ñå}‰å}¥€ôí¥Ñ•µl‰ÍÁ•¥µ•¹}¥‰tè¥Ñ•´™½È¥Ñ•´¥¸Í•¹Í¥Ñ¥Ù¥Ñål‰ÍÁ•¥µ•¹Ì‰uô(€€€ÁÉ½Ù•¹…¹•}É½ÝÌè±¥ÍÑm‘¥ÑmÍÑÈ°¹åut€ômt(€€€•‘•}É½ÝÌè±¥ÍÑm‘¥ÑmÍÑÈ°¹åut€ômt(€€€µ…Ñ•É¥…±}É½ÝÌè±¥ÍÑm‘¥ÑmÍÑÈ°¹åut€ômt(€€€™½È‰…Í•}ÍÁ•¥µ•¸°½µÁ…É…Ñ½È¥¸é¥À¡‰…Í•l‰ÍÁ•¥µ•¹Ì‰t°½µÁ…É¥Í½¹l‰ÍÁ•¥µ•¹Ì‰t°ÍÑÉ¥ÐõQÉÕ”¤è(€€€€€€€µ•Ñ…‘…Ñ„€ô‰…Í•}ÍÁ•¥µ•¹l‰½¹ÑÉ…Ñ}É•ÍÕ±Ð‰ul‰µ•Ñ…‘…Ñ„‰t(€€€€€€€ÁÉ½Ù•¹…¹•}É½ÝÌ¹…ÁÁ•¹¡ì(€€€€€€€€€€€€‰ÍÁ•¥µ•¹}¥ˆè‰…Í•}ÍÁ•¥µ•¹l‰ÍÁ•¥µ•¹}¥‰t°(€€€€€€€€€€€€‰Í½ÕÉ”ˆè‰…Í•}ÍÁ•¥µ•¹l‰½¹ÑÉ…Ñ}É•ÍÕ±Ð‰ul‰Í½ÕÉ”‰ul‰É•™•É•¹”‰t°(€€€€€€€€€€€€‰½µÁ½Í¥Ñ¥½¹}àˆè‰…Í•}ÍÁ•¥µ•¹l‰½µÁ½Í¥Ñ¥½¹}à‰t°(€€€€€€€€€€€€‰½µÁ½Í¥Ñ¥½¹}Í¥µ…}àˆèµ•Ñ…‘…Ñ…l‰½µÁ½Í¥Ñ¥½¹}Í¥µ…}à‰t°(€€€€€€€€€€€€‰Ñ•µÁ•É…ÑÕÉ•}¬ˆè‰…Í•}ÍÁ•¥µ•¹l‰Ñ•µÁ•É…ÑÕÉ•}¬‰t°(€€€€€€€€€€€€‰Ñ¡¥­¹•ÍÍ}Õ´ˆèµ•Ñ…‘…Ñ…l‰Ñ¡¥­¹•ÍÍ}Õ´‰t°(€€€€€€€€€€€€‰…ÉÉ¥•É}ÑåÁ”ˆèµ•Ñ…‘…Ñ…l‰…ÉÉ¥•É}ÑåÁ”‰t°(€€€€€€€€€€€€‰…ÉÉ¥•É}‘•¹Í¥Ñå}ÍÑ…ÑÕÌˆèµ•Ñ…‘…Ñ…l‰…ÉÉ¥•É}‘•¹Í¥Ñå}ÍÑ…ÑÕÌ‰t°(€€€€€€€€€€€€‰‘¥¥Ñ¥é•‘}Á½¥¹Ñ}½Õ¹Ðˆè‰…Í•}ÍÁ•¥µ•¹l‰‘¥¥Ñ¥é•‘}Á½¥¹Ñ}½Õ¹Ð‰t°(€€€€€€€€€€€€‰¥¹ÁÕÑ}Í¡„ÈÔØˆè‰…Í•}ÍÁ•¥µ•¹l‰¥¹ÁÕÑ}Í¡„ÈÔØ‰t°(€€€€€€€ô¤(€€€€€€€Í¡¥™ÑÌ€ôÍ•¹Í¥Ñ¥Ù¥Ñå}‰å}¥‘m‰…Í•}ÍÁ•¥µ•¹l‰ÍÁ•¥µ•¹}¥‰ut(€€€€€€€Í¡¥™Ñ}±½½­ÕÀ€ôì¨©Í¡¥™ÑÍl‰µ½‘•±}…¹‘¥‘…Ñ•}µ…á}Í¡¥™Ñ}µ•Ø‰t°€¨©Í¡¥™ÑÍl‰Ñ¡É•Í¡½±‘}…¹‘¥‘…Ñ•}µ…á}Í¡¥™Ñ}µ•Ø‰uô(€€€€€€€™½ÈÉ½Ü¥¸½µÁ…É…Ñ½Él‰…¹‘¥‘…Ñ•Ì‰tè(€€€€€€€€€€€•‘•}É½ÝÌ¹…ÁÁ•¹¡ì(€€€€€€€€€€€€€€€€‰ÍÁ•¥µ•¹}¥ˆè‰…Í•}ÍÁ•¥µ•¹l‰ÍÁ•¥µ•¹}¥‰t°(€€€€€€€€€€€€€€€€‰…¹‘¥‘…Ñ•}¥ˆèÉ½Ýl‰…¹‘¥‘…Ñ•}¥‰t°(€€€€€€€€€€€€€€€€‰½‰Í•ÉÙ…Ñ¥½¹}±…ÍÌˆèÉ½Ýl‰½‰Í•ÉÙ…Ñ¥½¹}±…ÍÌ‰t°(€€€€€€€€€€€€€€€€‰•‘•}µ•ØˆèÉ½Ýl‰•‘•}µ•Ø‰t°(€€€€€€€€€€€€€€€€‰‰½Õ¹‘…Éå}±¥µ¥Ñ•ˆèÉ½Ýl‰‰½Õ¹‘…Éå}±¥µ¥Ñ•‰t°(€€€€€€€€€€€€€€€€‰‘¥¥Ñ¥é…Ñ¥½¹}½½É‘¥¹…Ñ•}Í¡¥™Ñ}µ•ØˆèÍ¡¥™Ñ}±½½­ÕÁmÉ½Ýl‰…¹‘¥‘…Ñ•}¥‰ut°(€€€€€€€€€€€€€€€€‰¹½µ¥¹…±}Ý¥¹¹•ÈˆèÉ½Ýl‰¹½µ¥¹…±}Ý¥¹¹•È‰t°(€€€€€€€€€€€€€€€€‰¹½µ¥¹…±}ÉÕ¹¹•É}ÕÀˆèÉ½Ýl‰¹½µ¥¹…±}ÉÕ¹¹•É}ÕÀ‰t°(€€€€€€€€€€€€€€€€‰¹½µ¥¹…±}Ý¥¹¹•É}µ…É¥¹}µ•ØˆèÉ½Ýl‰¹½µ¥¹…±}Ý¥¹¹•É}µ…É¥¹}µ•Ø‰t°(€€€€€€€€€€€ô¤(€€€€€€€™½Èµ½‘•°¥¸5=1}=IHè(€€€€€€€€€€€ÁÉ•‘¥Ñ¥½¸€ô½µÁ…É…Ñ½Él‰µ½‘•±}ÁÉ•‘¥Ñ¥½¹Í}µ•Ø‰umµ½‘•±t(€€€€€€€€€€€µ…Ñ•É¥…±}É½ÝÌ¹…ÁÁ•¹¡ì(€€€€€€€€€€€€€€€€‰ÍÁ•¥µ•¹}¥ˆè‰…Í•}ÍÁ•¥µ•¹l‰ÍÁ•¥µ•¹}¥‰t°(€€€€€€€€€€€€€€€€‰µ½‘•±}¥ˆèµ½‘•°°(€€€€€€€€€€€€€€€€‰ÁÉ•‘¥Ñ¥½¹}µ•ØˆèÁÉ•‘¥Ñ¥½¸°(€€€€€€€€€€€€€€€€‰™¥ÑÑ•‘}µ½‘•±}É•Í¥‘Õ…±}µ¥¹}µ•Øˆè€ÄÀÀÀ¸À€¨‰…Í•}ÍÁ•¥µ•¹l‰µ½‘•±}™…µ¥±å}•¹Ù•±½Á”‰ul‰µ¥¹¥µÕµ}•‘•}•Ø‰t€´ÁÉ•‘¥Ñ¥½¸°(€€€€€€€€€€€€€€€€‰™¥ÑÑ•‘}µ½‘•±}É•Í¥‘Õ…±}µ…á}µ•Øˆè€ÄÀÀÀ¸À€¨‰…Í•}ÍÁ•¥µ•¹l‰µ½‘•±}™…µ¥±å}•¹Ù•±½Á”‰ul‰µ…á¥µÕµ}•‘•}•Ø‰t€´ÁÉ•‘¥Ñ¥½¸°(€€€€€€€€€€€€€€€€‰ÍÑÉ¥Ñ}É…¹­¥¹}…ÕÑ¡½É¥é•ˆè…±Í”°(€€€€€€€€€€€ô¤(€€€ÝÉ¥Ñ•}ÍØ¡½ÕÑÁÕÐ€¼€‰Ñ…‰±”Å}ÍÁ•¥µ•¹}ÁÉ½Ù•¹…¹”¹ÍØˆ°ÁÉ½Ù•¹…¹•}É½ÝÌ¤(€€€ÝÉ¥Ñ•}ÍØ¡½ÕÑÁÕÐ€¼€‰Ñ…‰±”É}…¹‘¥‘…Ñ•}‘•™¥¹¥Ñ¥½¹Ì¹ÍØˆ°l(€€€€€€€ì‰…¹‘¥‘…Ñ•}¥ˆè€‰™É…Ñ¥½¹…±}Á½Ý•É}™É•”ˆ°€‰‘•™¥¹¥Ñ¥½¸ˆè€‰…±Á¡„õ¡µœ¥yÀ½ìÀ™¥ÑÑ•ˆ°€‰Í½ÕÉ•}‘½µ…¥¸ˆè€‰‘•±…É•™¥ÐÝ¥¹‘½Ü‰ô°(€€€€€€€ì‰…¹‘¥‘…Ñ•}¥ˆè€‰™É…Ñ¥½¹…±}Á½Ý•É}™¥á•ˆ°€‰‘•™¥¹¥Ñ¥½¸ˆè€‰…±Á¡„õ¡µœ¥yÀ½ìÀ™¥á•ˆ°€‰Í½ÕÉ•}‘½µ…¥¸ˆè€‰ÀôÀ¸Ô°€À¸Ü°Í½ÕÉ”µÁ…¹•°À°€Ä¸À‰ô°(€€€€€€€ì‰…¹‘¥‘…Ñ•}¥ˆè€‰¡Õ|ÄääÑ}­…¹•}É•¥½¸ˆ°€‰‘•™¥¹¥Ñ¥½¸ˆè€‰…±Á¡„õ…±Á¡…}œ•áÀ¡ÍÅÉÐ¡‰•Ñ„¡à±P¤¡µœ¤¤¤ˆ°€‰Í½ÕÉ•}‘½µ…¥¸ˆè€ˆÀ¸ÄÜÀðõàðôÀ¸ÐÐÌì€ÜÜðõPðôÌÀÀ,‰ô°(€€€€€€€ì‰…¹‘¥‘…Ñ•}¥ˆè€‰™¥á•‘}…‰Í½ÉÁÑ¥½¹}Ñ¡É•Í¡½±ˆ°€‰‘•™¥¹¥Ñ¥½¸ˆè€‰™¥ÉÍÐ¥¹Ñ•ÉÁ½±…Ñ•…±Á¡„É½ÍÍ¥¹œˆ°€‰Í½ÕÉ•}‘½µ…¥¸ˆè€ˆÐÀÀ´ÔÀÀÀ´´Äì€ÔÀÀÀ™±…•Ý¡•É”½½É‘¥¹…Ñ”µÍ•¹Í¥Ñ¥Ù”‰ô°(€€€t¤(€€€ÝÉ¥Ñ•}ÍØ¡½ÕÑÁÕÐ€¼€‰Ñ…‰±”Í}•‘•}•¹Í•µ‰±”¹ÍØˆ°•‘•}É½ÝÌ¤(€€€ÝÉ¥Ñ•}ÍØ¡½ÕÑÁÕÐ€¼€‰Ñ…‰±”Ñ}µ…Ñ•É¥…±}µ½‘•±}½µÁ…É¥Í½¸¹ÍØˆ°µ…Ñ•É¥…±}É½ÝÌ¤(€€€ÝÉ¥Ñ•}ÍØ¡½ÕÑÁÕÐ€¼€‰Ñ…‰±”Õ}±…¥µ}‰½Õ¹‘…É¥•Ì¹ÍØˆ°l(€€€€€€€ì‰±…¥´ˆè€‰™É…Ñ¥½¹…°µµ½‘•°•‘”Í•¹Í¥Ñ¥Ù¥Ñä¥Ì…ÁÁÉ½á¥µ…Ñ•±ä€Ø´Üµ•Xˆ°€‰ÍÑ…ÑÕÌˆè€‰…ÕÑ¡½É¥é•ˆ°€‰‰½Õ¹‘…Éäˆè€‰ÑÝ¼‘¥¥Ñ¥é•€ÌÀÀ,%IMÍÁ•ÑÉ„™É½´½¹”Í½ÕÉ”ÍÑÕ‘ä‰ô°(€€€€€€€ì‰±…¥´ˆè€‰ÁÕ‰±¥Í¡•M•¥±•È¥Ì¹½µ¥¹…±±ä±½Í•ÍÐ™½È™¥ÑÑ•µµ½‘•°•‘•Ìˆ°€‰ÍÑ…ÑÕÌˆè€‰‘•ÍÉ¥ÁÑ¥Ù”½¹±äˆ°€‰‰½Õ¹‘…Éäˆè€ˆÀ¸Äà´À¸ÈÔµ•X…‘Ù…¹Ñ…”½Ù•È!…¹Í•¸ì½µÁ½Í¥Ñ¥½¸Õ¹•ÉÑ…¥¹Ñäµ¥ÍÍ¥¹œ‰ô°(€€€€€€€ì‰±…¥´ˆè€‰™¥á•µÑ¡É•Í¡½±‘•™¥¹¥Ñ¥½¸…¸¡…¹”Ñ¡”¹½µ¥¹…°½µÁ…É…Ñ½Èˆ°€‰ÍÑ…ÑÕÌˆè€‰…ÕÑ¡½É¥é•Ñ¡É½Õ €ÐÀÀÀ´´Äˆ°€‰‰½Õ¹‘…Éäˆè€‰Ñ¡É•Í¡½±¥Ì½Á•É…Ñ¥½¹…°…¹¥Ì¹½ÐÑ¡”±…Ñ•¹Ðµ…Ñ•É¥…°…À‰ô°(€€€€€€€ì‰±…¥´ˆè€‰½¹”½ÉÉ•Ñ•½ÈÁÉ½‘ÕÑ¥½¸•‘”•á¥ÍÑÌˆ°€‰ÍÑ…ÑÕÌˆè€‰¹½Ð…ÕÑ¡½É¥é•ˆ°€‰‰½Õ¹‘…Éäˆè€‰½µÁ±•Ñ”…¹‘¥‘…Ñ”•¹Í•µ‰±”µÕÍÐ‰”É•Á½ÉÑ•‰ô°(€€€t¤(€€€€¡½ÕÑÁÕÐ€¼€‰™¥ÕÉ”Å}ÍÁ•ÑÉÕµ}µ½‘•±Ì¹ÍÙœˆ¤¹ÝÉ¥Ñ•}Ñ•áÐ¡™¥ÕÉ”Ä¡É½½Ð°‰…Í”¤°•¹½‘¥¹œô‰ÕÑ˜´àˆ¤(€€€€¡½ÕÑÁÕÐ€¼€‰™¥ÕÉ”É}•‘•}…¹‘¥‘…Ñ•Ì¹ÍÙœˆ¤¹ÝÉ¥Ñ•}Ñ•áÐ¡™¥ÕÉ”È¡½µÁ…É¥Í½¸¤°•¹½‘¥¹œô‰ÕÑ˜´àˆ¤(€€€€¡½ÕÑÁÕÐ€¼€‰™¥ÕÉ”Í}µ…Ñ•É¥…±}É•Í¥‘Õ…±}•¹Ù•±½Á•Ì¹ÍÙœˆ¤¹ÝÉ¥Ñ•}Ñ•áÐ¡™¥ÕÉ”Ì¡‰…Í”°½µÁ…É¥Í½¸¤°•¹½‘¥¹œô‰ÕÑ˜´àˆ¤(€€€ÍÕµµ…Éä€ôì(€€€€€€€€‰Í¡•µ…}Ù•ÉÍ¥½¸ˆè€ˆÄ¸Àˆ°(€€€€€€€€‰…¹…±åÍ¥Ìˆè½µÁ…É¥Í½¹l‰…¹…±åÍ¥Ì‰t°(€€€€€€€€‰‘•¥Í¥½¸ˆè½µÁ…É¥Í½¹l‰‘•¥Í¥½¸‰t°(€€€€€€€€‰‘¥¥Ñ¥é…Ñ¥½¹}‘•¥Í¥½¸ˆèÍ•¹Í¥Ñ¥Ù¥Ñål‰‘•¥Í¥½¸‰t°(€€€€€€€€‰•¹•É…Ñ•‘}™¥±•ÌˆèÍ½ÉÑ•¡Á…Ñ ¹¹…µ”™½ÈÁ…Ñ ¥¸½ÕÑÁÕÐ¹¥Ñ•É‘¥È ¤¤°(€€€€€€€€‰±…¥µ}‰½Õ¹‘…Éäˆè½µÁ…É¥Í½¹l‰±…¥µ}‰½Õ¹‘…Éä‰t°(€€€ô(€€€€¡½ÕÑÁÕÐ€¼€‰µ…¹ÕÍÉ¥ÁÑ}…ÍÍ•Ñ}ÍÕµµ…Éä¹©Í½¸ˆ¤¹ÝÉ¥Ñ•}Ñ•áÐ¡©Í½¸¹‘ÕµÁÌ¡ÍÕµµ…Éä°¥¹‘•¹ÐôÈ°Í½ÉÑ}­•åÌõQÉÕ”¤€¬€‰q¸ˆ°•¹½‘¥¹œô‰ÕÑ˜´àˆ¤(€€€É•ÑÕÉ¸ÍÕµµ…Éä(()‘•˜µ…¥¸ ¤€´ø9½¹”è(€€€Á…ÉÍ•È€ô…ÉÁ…ÉÍ”¹ÉÕµ•¹ÑA…ÉÍ•È ¤(€€€Á…ÉÍ•È¹…‘‘}…ÉÕµ•¹Ð ˆ´µÉ•Á½Í¥Ñ½ÉäµÉ½½Ðˆ°‘•™…Õ±Ðôˆ¸ˆ¤(€€€Á…ÉÍ•È¹…‘‘}…ÉÕµ•¹Ð ˆ´µ½ÕÑÁÕÐµ‘¥Èˆ°É•ÅÕ¥É•õQÉÕ”¤(€€€…ÉÌ€ôÁ…ÉÍ•È¹Á…ÉÍ•}…ÉÌ ¤(€€€É•ÍÕ±Ð€ô‰Õ¥±¡…ÉÌ¹É•Á½Í¥Ñ½Éå}É½½Ð°…ÉÌ¹½ÕÑÁÕÑ}‘¥È¤(€€€ÁÉ¥¹Ð¡©Í½¸¹‘ÕµÁÌ¡É•ÍÕ±Ñl‰‘•¥Í¥½¸‰t°Í½ÉÑ}­•åÌõQÉÕ”¤¤(()¥˜}}¹…µ•}|€ôô€‰}}µ…¥¹}|ˆè(€€€µ…¥¸ ¤