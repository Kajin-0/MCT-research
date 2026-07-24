"""Build deterministic grayscale SVG figures for the strict HgCdTe revision."""
from __future__ import annotations

import argparse
import html
import json
import math
from pathlib import Path
from typing import Any


CANDIDATE_ORDER = (
    "fractional_power_free",
    "fractional_power_p_0.5",
    "fractional_power_p_0.7",
    "source_panel",
    "fractional_power_p_1",
    "chu_1994_kane_region",
)
CANDIDATE_LABELS = (
    "free p",
    "p = 0.5",
    "p = 0.7",
    "source-panel p",
    "p = 1",
    "Chu Kane-region",
)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _svg(body: list[str], *, title: str, width: int = 1000, height: int = 600) -> str:
    style = (
        "<style>"
        "text{font-family:Arial,Helvetica,sans-serif;fill:#171717}"
        ".title{font-size:21px;font-weight:700}"
        ".label{font-size:14px}"
        ".small{font-size:12px}"
        ".grid{stroke:#d8d8d8;stroke-width:1}"
        ".axis{stroke:#171717;stroke-width:1.4}"
        "</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>{esc(title)}</title>'
        '<rect width="100%" height="100%" fill="white"/>'
        + style
        + "".join(body)
        + "</svg>\n"
    )


def _source_key(edges: dict[str, float]) -> str:
    return next(
        key
        for key in edges
        if key.startswith("fractional_power_p_")
        and key
        not in {
            "fractional_power_p_0.5",
            "fractional_power_p_0.7",
            "fractional_power_p_1",
        }
    )


def _candidate_lookup(specimen: dict[str, Any]) -> dict[str, dict[str, Any]]:
    edges = specimen["nominal_model_edges_ev"]
    diagnostics = specimen["nominal_model_adequacy_diagnostics"]
    diagnostics_by_id = {item["candidate_id"]: item for item in diagnostics}
    source = _source_key(edges)
    lookup: dict[str, dict[str, Any]] = {}
    for identifier in CANDIDATE_ORDER:
        source_identifier = source if identifier == "source_panel" else identifier
        lookup[identifier] = {
            "edge_ev": float(edges[source_identifier]),
            **diagnostics_by_id[source_identifier],
        }
    return lookup


def relative_intercepts(result: dict[str, Any]) -> str:
    width, height = 1000, 600
    left, right, top, bottom = 205.0, 945.0, 80.0, 515.0
    specimens = result["specimens"]
    lookups = [_candidate_lookup(specimen) for specimen in specimens]
    maxima = []
    baselines = []
    for lookup in lookups:
        baseline = min(
            item["edge_ev"]
            for item in lookup.values()
            if not item["boundary_limited"]
        )
        baselines.append(baseline)
        maxima.extend(1000.0 * (item["edge_ev"] - baseline) for item in lookup.values())
    xmax = max(7.2, math.ceil(max(maxima) * 2.0) / 2.0)
    xmap = lambda value: left + (right - left) * value / xmax
    spacing = (bottom - top) / (len(CANDIDATE_ORDER) - 1)
    ymap = lambda index: bottom - index * spacing

    body = [
        '<text x="500" y="34" text-anchor="middle" class="title">Declared fitted-intercept models are not equally positioned</text>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>',
    ]
    for tick in range(int(math.floor(xmax)) + 1):
        x = xmap(float(tick))
        body += [
            f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{bottom}" class="grid"/>',
            f'<text x="{x:.2f}" y="542" text-anchor="middle" class="label">{tick}</text>',
        ]
    for index, label in enumerate(CANDIDATE_LABELS):
        y = ymap(index)
        body.append(
            f'<text x="195" y="{y+5:.2f}" text-anchor="end" class="label">{esc(label)}</text>'
        )
    offsets = (-9.0, 9.0)
    for specimen_index, (specimen, lookup, baseline) in enumerate(
        zip(specimens, lookups, baselines, strict=True)
    ):
        for index, identifier in enumerate(CANDIDATE_ORDER):
            item = lookup[identifier]
            x = xmap(1000.0 * (item["edge_ev"] - baseline))
            y = ymap(index) + offsets[specimen_index]
            if specimen_index == 0:
                body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.2"/>')
            else:
                body.append(
                    f'<rect x="{x-5.0:.2f}" y="{y-5.0:.2f}" width="10" height="10" fill="white" stroke="black" stroke-width="1.5"/>'
                )
            if item["boundary_limited"]:
                body.append(
                    f'<text x="{x+9:.2f}" y="{y+4:.2f}" class="small">B</text>'
                )
    body += [
        '<circle cx="735" cy="58" r="5.2"/><text x="748" y="62" class="small">x = 0.226</text>',
        '<rect x="826" y="53" width="10" height="10" fill="white" stroke="black" stroke-width="1.5"/><text x="842" y="62" class="small">x = 0.310</text>',
        '<text x="500" y="579" text-anchor="middle" class="label">Fitted intercept relative to the lowest non-boundary model (meV)</text>',
        '<text x="938" y="79" text-anchor="end" class="small">B = boundary-limited</text>',
    ]
    return _svg(body, title="Relative fitted-intercept positions", width=width, height=height)


def robustness_scales(result: dict[str, Any]) -> str:
    width, height = 1000, 600
    left, right, top, bottom = 115.0, 950.0, 82.0, 490.0
    categories = (
        "Calibration corners",
        "Reconstruction, fixed",
        "Reconstruction + membership",
        "Fit domain + weighting",
    )
    specimens = result["specimens"]
    series = []
    for specimen in specimens:
        series.append(
            [
                0.890691 if specimen["specimen_id"].endswith("0.226") else 0.678691,
                specimen["maximum_fixed_membership_reconstruction_shift_mev"],
                specimen["maximum_all_admissible_reconstruction_shift_mev"],
                specimen["maximum_fit_domain_or_weighting_shift_mev"],
            ]
        )
    ymin, ymax = 0.5, 8.0
    xmap = lambda index: left + (right - left) * index / (len(categories) - 1)
    ymap = lambda value: top + (bottom - top) * (
        math.log10(ymax) - math.log10(value)
    ) / (math.log10(ymax) - math.log10(ymin))
    body = [
        '<text x="500" y="34" text-anchor="middle" class="title">Fit-domain convention dominates reconstruction sensitivity</text>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>',
    ]
    for value in (0.5, 1.0, 2.0, 5.0):
        y = ymap(value)
        body += [
            f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" class="grid"/>',
            f'<text x="103" y="{y+5:.2f}" text-anchor="end" class="label">{value:g}</text>',
        ]
    for index, label in enumerate(categories):
        x = xmap(index)
        body.append(
            f'<text x="{x:.2f}" y="525" text-anchor="middle" class="small">{esc(label)}</text>'
        )
    for specimen_index, values in enumerate(series):
        points = " ".join(
            f"{xmap(index):.2f},{ymap(value):.2f}"
            for index, value in enumerate(values)
        )
        dash = ' stroke-dasharray="8 5"' if specimen_index else ""
        body.append(
            f'<polyline points="{points}" fill="none" stroke="black" stroke-width="1.7"{dash}/>'
        )
        for index, value in enumerate(values):
            x, y = xmap(index), ymap(value)
            if specimen_index == 0:
                body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.2"/>')
            else:
                body.append(
                    f'<rect x="{x-5:.2f}" y="{y-5:.2f}" width="10" height="10" fill="white" stroke="black" stroke-width="1.5"/>'
                )
    body += [
        '<circle cx="745" cy="58" r="5.2"/><text x="758" y="62" class="small">x = 0.226</text>',
        '<rect x="841" y="53" width="10" height="10" fill="white" stroke="black" stroke-width="1.5"/><text x="857" y="62" class="small">x = 0.310</text>',
        '<text transform="translate(28 286) rotate(-90)" text-anchor="middle" class="label">Maximum absolute intercept displacement (meV)</text>',
    ]
    return _svg(body, title="Deterministic sensitivity scales", width=width, height=height)


def residual_compatibility(result: dict[str, Any]) -> str:
    width, height = 1000, 600
    left, right, top, bottom = 115.0, 950.0, 82.0, 490.0
    specimens = result["specimens"]
    lookups = [_candidate_lookup(specimen) for specimen in specimens]
    ymin, ymax = 0.5, 10.0
    xmap = lambda index: left + (right - left) * index / (len(CANDIDATE_ORDER) - 1)
    ymap = lambda value: top + (bottom - top) * (
        math.log10(ymax) - math.log10(value)
    ) / (math.log10(ymax) - math.log10(ymin))
    body = [
        '<text x="500" y="34" text-anchor="middle" class="title">Several declared models do not track the reconstructed line at its resolution</text>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>',
    ]
    for value in (0.5, 1.0, 2.0, 5.0, 10.0):
        y = ymap(value)
        body += [
            f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" class="grid"/>',
            f'<text x="103" y="{y+5:.2f}" text-anchor="end" class="label">{value:g}</text>',
        ]
    y_one = ymap(1.0)
    body.append(
        f'<line x1="{left}" y1="{y_one:.2f}" x2="{right}" y2="{y_one:.2f}" stroke="black" stroke-width="1.6" stroke-dasharray="7 5"/>'
    )
    offsets = (-8.0, 8.0)
    for specimen_index, lookup in enumerate(lookups):
        for index, identifier in enumerate(CANDIDATE_ORDER):
            value = lookup[identifier]["normalized_rms_using_vertical_line_halfwidth"]
            x, y = xmap(index) + offsets[specimen_index], ymap(value)
            if specimen_index == 0:
                body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.2"/>')
            else:
                body.append(
                    f'<rect x="{x-5:.2f}" y="{y-5:.2f}" width="10" height="10" fill="white" stroke="black" stroke-width="1.5"/>'
                )
    for index, label in enumerate(CANDIDATE_LABELS):
        x = xmap(index)
        body.append(
            f'<text x="{x:.2f}" y="527" text-anchor="middle" class="small">{esc(label)}</text>'
        )
    body += [
        '<circle cx="724" cy="58" r="5.2"/><text x="737" y="62" class="small">x = 0.226</text>',
        '<rect x="820" y="53" width="10" height="10" fill="white" stroke="black" stroke-width="1.5"/><text x="836" y="62" class="small">x = 0.310</text>',
        '<line x1="724" y1="74" x2="750" y2="74" stroke="black" stroke-width="1.6" stroke-dasharray="7 5"/><text x="758" y="78" class="small">RMS = one line half-width</text>',
        '<text transform="translate(28 286) rotate(-90)" text-anchor="middle" class="label">RMS residual / reconstructed line half-width</text>',
    ]
    return _svg(body, title="Residual compatibility diagnostics", width=width, height=height)


def build(reference_path: Path, output_dir: Path) -> dict[str, str]:
    result = json.loads(reference_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    figures = {
        "figure6_relative_fitted_intercepts.svg": relative_intercepts(result),
        "figure7_robustness_scales.svg": robustness_scales(result),
        "figure8_model_residual_compatibility.svg": residual_compatibility(result),
    }
    for name, text in figures.items():
        (output_dir / name).write_text(text, encoding="utf-8")
    return figures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference-json",
        type=Path,
        default=Path("data/validation/moazzami2005_model_robustness_reference.json"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args()
    build(arguments.reference_json, arguments.output_dir)


if __name__ == "__main__":
    main()
