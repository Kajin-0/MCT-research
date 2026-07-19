"""Generate the manuscript identifiability diagram as deterministic SVG."""
from __future__ import annotations

import html


def _text(x: float, y: float, value: str, css: str = "label", anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="{css}">'
        f'{html.escape(value)}</text>'
    )


def _box(x: float, y: float, width: float, height: float, css: str = "box") -> str:
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" class="{css}"/>'


def _arrow(x1: float, y1: float, x2: float, y2: float, css: str = "arrow") -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'class="{css}" marker-end="url(#arrowhead)"/>'
    )


def build_identifiability_svg() -> str:
    width, height = 1240, 760
    body: list[str] = [
        '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#444"/></marker></defs>',
        '<style>text{font-family:Arial,sans-serif;fill:#111}.title{font-size:21px;font-weight:700}.panel{font-size:17px;font-weight:700}.label{font-size:15px}.small{font-size:12px}.equation{font-size:16px;font-family:Arial,sans-serif}.box{fill:white;stroke:#222;stroke-width:1.6}.latent{fill:#f2f2f2;stroke:#111;stroke-width:2}.term{fill:#fafafa;stroke:#666;stroke-width:1.4}.result{fill:#ededed;stroke:#111;stroke-width:2}.arrow{stroke:#444;stroke-width:1.6}.dashed{stroke:#777;stroke-width:1.4;stroke-dasharray:6 5}</style>',
        _text(35, 36, "Figure 4. What an absorption-derived HgCdTe edge actually measures", "title", "start"),
    ]

    # State variables and latent material quantity.
    body += [
        _box(45, 110, 190, 92),
        _text(140, 137, "Specimen state", "panel"),
        _text(140, 164, "composition  x ± σx", "label"),
        _text(140, 188, "temperature  T ± σT", "label"),
        _box(315, 112, 245, 88, "latent"),
        _text(437.5, 142, "Latent material gap", "panel"),
        _text(437.5, 178, "Eg = Eg(x,T)", "equation"),
        _arrow(235, 156, 315, 156),
    ]

    # Paired observation classes.
    body += [
        _box(655, 82, 270, 105),
        _text(790, 112, "Magneto-optical observation", "panel"),
        _text(790, 151, "yMO = Eg(x,T) + εMO", "equation"),
        _box(655, 238, 520, 130),
        _text(915, 268, "Intrinsic-absorption observation", "panel"),
        _text(
            915,
            309,
            "yabs = Eg + Δmethod + Δcarrier + Δvacancy + εabs",
            "equation",
        ),
        _arrow(560, 145, 655, 134),
        _arrow(560, 168, 655, 287),
        '<line x1="612" y1="134" x2="612" y2="287" class="dashed"/>',
        _text(600, 216, "same specimen", "small", "end"),
    ]

    # Observation-specific terms and required evidence.
    terms = [
        (
            70,
            435,
            "Δmethod",
            "fit family • window • threshold",
            "tail treatment • calibration",
        ),
        (
            340,
            435,
            "Δcarrier",
            "Hall type • n or p • mobility",
            "Burstein-Moss / filling state",
        ),
        (
            610,
            435,
            "Δvacancy",
            "vacancy-sensitive proxy",
            "anneal and processing history",
        ),
    ]
    for x, title, line1, line2 in terms:
        body += [
            _box(x, 430, 235, 112, "term"),
            _text(x + 117.5, 459, title, "panel"),
            _text(x + 117.5, 490, line1, "small"),
            _text(x + 117.5, 516, line2, "small"),
            _arrow(x + 117.5, 430, 820 if x < 500 else 1005, 368),
        ]

    # Paired difference and claim boundary.
    body += [
        _box(900, 430, 295, 112, "result"),
        _text(1047.5, 458, "Paired same-specimen difference", "panel"),
        _text(1047.5, 490, "yabs − yMO", "equation"),
        _text(
            1047.5,
            518,
            "= Δmethod + Δcarrier + Δvacancy + noise",
            "small",
        ),
        '<line x1="45" y1="600" x2="1195" y2="600" stroke="#bbb"/>',
        _text(
            620,
            640,
            "Without paired modalities, independent composition metrology, Hall state, and a vacancy proxy,",
            "label",
        ),
        _text(
            620,
            670,
            "the latent gap and observation terms are aliased. A precise fit is not the same as identification.",
            "label",
        ),
        _text(
            620,
            716,
            "The diagram defines an observation model; it does not authorize a universal correction.",
            "small",
        ),
    ]

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>HgCdTe gap observation identifiability</title>'
        '<rect width="100%" height="100%" fill="white"/>'
        + "".join(body)
        + "</svg>\n"
    )
