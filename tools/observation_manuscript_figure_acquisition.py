"""Generate the paired 2x2x2 HgCdTe acquisition-design SVG."""
from __future__ import annotations

import html
from typing import Any

from tools.design_minimum_gap_identifiability_dataset import analyze


def _text(x: float, y: float, value: Any, css: str = "label", anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="{css}">'
        f'{html.escape(str(value))}</text>'
    )


def _box(x: float, y: float, width: float, height: float, css: str = "cell") -> str:
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" class="{css}"/>'


def _scenario() -> tuple[dict[str, Any], dict[str, float]]:
    result = analyze()
    scenario = next(
        item
        for item in result["scenarios"]
        if item["name"] == "audit_grade_eight_specimen_factorial"
    )
    return scenario, result["composition_coding"]


def _specimen_map(scenario: dict[str, Any]) -> dict[tuple[int, int, int], str]:
    records: dict[tuple[int, int, int], str] = {}
    for row in scenario["observation_ledger"]:
        key = (
            int(row["composition_code"]),
            int(row["carrier_proxy_code"]),
            int(row["vacancy_proxy_code"]),
        )
        records.setdefault(key, row["specimen_id"])
    return records


def _temperature_panel(
    body: list[str],
    *,
    panel_x: float,
    title: str,
    specimens: dict[tuple[int, int, int], str],
    x_low: float,
    x_high: float,
) -> None:
    panel_width = 500
    grid_left = panel_x + 105
    grid_top = 150
    column_width = 180
    row_height = 150
    body += [
        _box(panel_x, 78, panel_width, 500, "panelbox"),
        _text(panel_x + panel_width / 2, 111, title, "panel"),
        _text(grid_left + column_width / 2, 139, f"composition low  x={x_low:.2f}", "small"),
        _text(grid_left + 1.5 * column_width, 139, f"composition high  x={x_high:.2f}", "small"),
        _text(panel_x + 55, grid_top + 0.5 * row_height, "carrier low", "small"),
        _text(panel_x + 55, grid_top + 1.5 * row_height, "carrier high", "small"),
    ]
    for carrier_index, carrier in enumerate((-1, 1)):
        for composition_index, composition in enumerate((-1, 1)):
            x = grid_left + composition_index * column_width
            y = grid_top + carrier_index * row_height
            body.append(_box(x, y, 165, 135, "cell"))
            for vacancy_index, vacancy in enumerate((-1, 1)):
                specimen = specimens[(composition, carrier, vacancy)]
                band_y = y + 10 + vacancy_index * 58
                body += [
                    _box(x + 10, band_y, 145, 50, "subcell"),
                    _text(x + 23, band_y + 20, "V-" if vacancy < 0 else "V+", "tiny", "start"),
                    _text(x + 82.5, band_y + 20, specimen.replace("factorial_", "S"), "small"),
                    _text(x + 82.5, band_y + 40, "MO  <->  ABS", "tiny"),
                ]


def build_acquisition_svg() -> str:
    scenario, coding = _scenario()
    specimens = _specimen_map(scenario)
    diagnostics = scenario["diagnostics"]
    width, height = 1240, 760
    body: list[str] = [
        '<style>text{font-family:Arial,sans-serif;fill:#111}.title{font-size:21px;font-weight:700}.panel{font-size:17px;font-weight:700}.label{font-size:15px}.small{font-size:12px}.tiny{font-size:11px}.panelbox{fill:white;stroke:#111;stroke-width:2}.cell{fill:#f7f7f7;stroke:#555;stroke-width:1.3}.subcell{fill:white;stroke:#999;stroke-width:1}.metric{fill:#efefef;stroke:#222;stroke-width:1.6}.arrow{stroke:#555;stroke-width:1.8;stroke-dasharray:7 5}</style>',
        _text(35, 36, "Figure 5. Audit-grade paired 2x2x2 acquisition design", "title", "start"),
        _text(
            620,
            62,
            "Eight specimen states x two modalities x two temperature blocks = 32 gap observations",
            "label",
        ),
    ]
    _temperature_panel(
        body,
        panel_x=45,
        title="Low-temperature block  (target 6 K)",
        specimens=specimens,
        x_low=float(coding["coded_minus_one_x"]),
        x_high=float(coding["coded_plus_one_x"]),
    )
    _temperature_panel(
        body,
        panel_x=695,
        title="Room-temperature block  (300 K)",
        specimens=specimens,
        x_low=float(coding["coded_minus_one_x"]),
        x_high=float(coding["coded_plus_one_x"]),
    )
    body += [
        '<line x1="570" y1="325" x2="670" y2="325" class="arrow"/>',
        _text(620, 307, "repeat same design", "small"),
        _text(620, 348, "new T block", "small"),
        _box(45, 615, 1150, 95, "metric"),
        _text(125, 644, f'rank  {diagnostics["rank"]}/5', "panel"),
        _text(310, 644, f'observations/block  {diagnostics["observation_count"]}', "panel"),
        _text(540, 644, f'residual DOF  {diagnostics["residual_degrees_of_freedom"]}', "panel"),
        _text(755, 644, f'condition number  {diagnostics["condition_number"]:.3f}', "panel"),
        _text(1030, 644, f'max leverage  {diagnostics["maximum_leverage"]:.4f}', "panel"),
        _text(
            620,
            681,
            "Each specimen requires independent composition metrology, Hall state, vacancy proxy, raw absorption, and paired magneto-optical gap.",
            "small",
        ),
        _text(
            620,
            735,
            "Unique audit-grade subset within the declared two-level 2^3 candidate family; not a universal optimal-design proof.",
            "small",
        ),
    ]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>Paired HgCdTe acquisition design</title>'
        '<rect width="100%" height="100%" fill="white"/>'
        + "".join(body)
        + "</svg>\n"
    )
