"""Generate edge-candidate and material-residual manuscript SVGs."""
from __future__ import annotations

import html
from typing import Any

import numpy as np

from tools.analyze_moazzami2005_manuscript_comparators import MODEL_ORDER

LABELS = {
    "hansen": "Hansen",
    "published_seiler": "Seiler 1990",
    "laurenti": "Laurenti",
    "provisional_hansen_pade": "Provisional Pade",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def candidate_label(identifier: str) -> str:
    labels = {
        "fractional_power_free": "fractional p free",
        "fractional_power_p_0.5": "fractional p=0.5",
        "fractional_power_p_0.7": "fractional p=0.7",
        "fractional_power_p_0.872": "fractional p=0.872",
        "fractional_power_p_0.849": "fractional p=0.849",
        "fractional_power_p_1": "fractional p=1",
        "chu_1994_kane_region": "Chu 1994 Kane",
    }
    if identifier.startswith("threshold_"):
        return identifier.removeprefix("threshold_").replace("_cm-1", " cm-1")
    return labels.get(identifier, identifier)


def wrap(width: int, height: int, title: str, body: list[str]) -> str:
    style = (
        '<style>text{font-family:Arial,sans-serif;fill:#111}'
        '.grid{stroke:#ddd}.axis{stroke:#111;stroke-width:1.4}'
        '.small{font-size:12px}.label{font-size:15px}'
        '.title{font-size:20px;font-weight:700}.panel{font-size:17px;font-weight:700}</style>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>{esc(title)}</title>'
        '<rect width="100%" height="100%" fill="white"/>'
        + style
        + "".join(body)
        + "</svg>\n"
    )


def build_edge_svg(comparison: dict[str, Any]) -> str:
    width, height = 1180, 690
    label_left, panel_w, gap, top, bottom = 180, 420, 85, 75, 55
    template = comparison["specimens"][0]["candidates"]
    row_h = (height - top - bottom) / len(template)
    body = [
        '<text x="35" y="34" class="title">Figure 2. Extracted edge depends on observation definition</text>'
    ]
    for index, row in enumerate(template):
        y = top + (index + 0.5) * row_h
        body.append(
            f'<text x="168" y="{y+4:.2f}" text-anchor="end" class="small">'
            f'{esc(candidate_label(row["candidate_id"]))}</text>'
        )
        if index == 6:
            body.append(
                f'<line x1="35" y1="{y-row_h/2:.2f}" x2="1145" '
                f'y2="{y-row_h/2:.2f}" stroke="#999"/>'
            )
    panels = [
        (comparison["specimens"][0], label_left, 178.0, 275.0),
        (comparison["specimens"][1], label_left + panel_w + gap, 286.0, 356.0),
    ]
    for specimen, left, xmin, xmax in panels:
        body.append(
            f'<text x="{left+panel_w/2:.1f}" y="58" text-anchor="middle" class="panel">'
            f'x={specimen["composition_x"]:.3f}, 300 K</text>'
        )
        for tick in np.linspace(xmin, xmax, 5):
            x = left + panel_w * (float(tick) - xmin) / (xmax - xmin)
            body += [
                f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{height-bottom}" class="grid"/>',
                f'<text x="{x:.2f}" y="666" text-anchor="middle" class="small">{tick:.0f}</text>',
            ]
        body.append(
            f'<line x1="{left}" y1="{height-bottom}" x2="{left+panel_w}" '
            f'y2="{height-bottom}" class="axis"/>'
        )
        for index, row in enumerate(specimen["candidates"]):
            x = left + panel_w * (float(row["edge_mev"]) - xmin) / (xmax - xmin)
            y = top + (index + 0.5) * row_h
            if row["boundary_limited"]:
                body.append(
                    f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.2" fill="white" '
                    'stroke="#111" stroke-width="1.8"/>'
                )
            else:
                body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5" fill="#111"/>')
    body += [
        '<text x="642" y="688" text-anchor="middle" class="label">Extracted edge (meV)</text>',
        '<circle cx="930" cy="55" r="5.2" fill="white" stroke="#111" stroke-width="1.8"/>',
        '<text x="943" y="59" class="small">boundary-limited fit</text>',
    ]
    return wrap(width, height, "Extracted edge by observation definition", body)


def build_residual_svg(base: dict[str, Any], comparison: dict[str, Any]) -> str:
    width, height = 1050, 670
    left, top, plot_w, plot_h = 90, 90, 925, 480
    ymin, ymax = -130.0, 30.0
    ymap = lambda value: top + plot_h * (ymax - value) / (ymax - ymin)
    body = [
        '<text x="35" y="34" class="title">Figure 3. Material-model residual intervals from the observation ensemble</text>'
    ]
    for tick in (-120, -90, -60, -30, 0, 30):
        y = ymap(float(tick))
        body += [
            f'<line x1="{left}" y1="{y:.2f}" x2="1015" y2="{y:.2f}" class="grid"/>',
            f'<text x="76" y="{y+5:.2f}" text-anchor="end" class="label">{tick}</text>',
        ]
    body += [
        f'<line x1="{left}" y1="{ymap(0):.2f}" x2="1015" y2="{ymap(0):.2f}" stroke="#111" stroke-width="1.8"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="570" class="axis"/>',
        '<text transform="translate(27 330) rotate(-90)" text-anchor="middle" class="label">Observation edge minus model prediction (meV)</text>',
    ]
    group_w = plot_w / len(MODEL_ORDER)
    for model_index, model in enumerate(MODEL_ORDER):
        center = left + (model_index + 0.5) * group_w
        body.append(
            f'<text x="{center:.2f}" y="618" text-anchor="middle" class="label">'
            f'{esc(LABELS[model])}</text>'
        )
        for specimen_index, (spectrum, comparator) in enumerate(
            zip(base["specimens"], comparison["specimens"], strict=True)
        ):
            x = center + (-18.0, 18.0)[specimen_index]
            prediction = float(comparator["model_predictions_mev"][model])
            envelope = spectrum["model_family_envelope"]
            low = 1000.0 * float(envelope["minimum_edge_ev"]) - prediction
            high = 1000.0 * float(envelope["maximum_edge_ev"]) - prediction
            stable = [
                float(row["edge_mev"])
                for row in comparator["candidates"]
                if row["observation_class"] == "fixed_absorption_threshold"
                and row["candidate_id"] != "threshold_5000_cm-1"
            ]
            dash = "" if specimen_index == 0 else "5 4"
            body += [
                f'<line x1="{x:.2f}" y1="{ymap(min(stable)-prediction):.2f}" '
                f'x2="{x:.2f}" y2="{ymap(max(stable)-prediction):.2f}" '
                f'stroke="#999" stroke-width="7" stroke-linecap="round" stroke-dasharray="{dash}"/>',
                f'<line x1="{x:.2f}" y1="{ymap(low):.2f}" x2="{x:.2f}" '
                f'y2="{ymap(high):.2f}" stroke="#111" stroke-width="3" '
                f'stroke-linecap="round" stroke-dasharray="{dash}"/>',
            ]
    body += [
        '<line x1="570" y1="55" x2="610" y2="55" stroke="#111" stroke-width="3"/>',
        '<text x="618" y="59" class="small">fitted-model envelope</text>',
        '<line x1="780" y1="55" x2="820" y2="55" stroke="#999" stroke-width="7"/>',
        '<text x="828" y="59" class="small">400-4000 cm-1 thresholds</text>',
        '<text x="552" y="652" text-anchor="middle" class="small">Intervals are observation-definition sensitivity, not statistical confidence intervals.</text>',
    ]
    return wrap(width, height, "Material-model residual intervals", body)
