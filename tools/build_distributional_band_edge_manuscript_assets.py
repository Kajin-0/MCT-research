#!/usr/bin/env python3
"""Public deterministic builder with manuscript-scale SVG presentation fixes.

The numerical generation core is preserved in ``tools._distributional_asset_core``.
This wrapper changes only generated SVG presentation: line-weight legends,
spacing, and display of the committed machine-precision residual bound.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

from . import _distributional_asset_core as _core

FIGURE_FILES = _core.FIGURE_FILES
TABLE_FILES = _core.TABLE_FILES
RECORD_PATHS = _core.RECORD_PATHS


def _postprocess_figure2(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        ".line3{fill:none;stroke:#999;stroke-width:2.2;stroke-dasharray:2 4}",
        ".line3{fill:none;stroke:#999;stroke-width:2.2;stroke-dasharray:2 4}"
        ".local{stroke-width:1.15;opacity:.62}",
    )
    text = text.replace('height="920" viewBox="0 0 1480 920"', 'height="950" viewBox="0 0 1480 950"')
    text = text.replace(
        '<text x="836" y="438" class="small">same line style: exact; repeated overlay: local linearization</text>',
        "",
    )

    local_polyline_indices = {1, 3, 5, 7, 9, 11}
    counter = -1

    def mark_local(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        css = match.group(1)
        if counter in local_polyline_indices:
            css += " local"
        return match.group(0).replace(match.group(1), css, 1)

    text = re.sub(
        r'<polyline points="[^"]+" class="(line[123])"/>',
        mark_local,
        text,
    )
    if counter + 1 < 15:
        raise RuntimeError("unexpected Figure 2 polyline structure")

    text = text.replace('y1="875"', 'y1="915"')
    text = text.replace('y2="875"', 'y2="915"')
    text = text.replace('y="879"', 'y="919"')

    legend = (
        '<line x1="1040" y1="143" x2="1085" y2="143" class="line1"/>'
        '<text x="1094" y="147" class="small">exact quadrature</text>'
        '<line x1="1215" y1="143" x2="1260" y2="143" class="line1 local"/>'
        '<text x="1269" y="147" class="small">local linearization</text>'
        '<line x1="305" y1="579" x2="350" y2="579" class="line1"/>'
        '<text x="359" y="583" class="small">single crossing</text>'
        '<line x1="475" y1="579" x2="520" y2="579" class="line1 local"/>'
        '<text x="529" y="583" class="small">always normal</text>'
    )
    text = text.replace("</svg>\n", legend + "</svg>\n")
    path.write_text(text, encoding="utf-8")


def _postprocess_figure3(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'<text x="1375\.0" y="145\.0" text-anchor="end" class="label">(fit-window increase = [^<]+)</text>',
        r'<text x="830.0" y="145.0" class="label">\1</text>',
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")


def _postprocess_figure6(repository_root: Path, path: Path) -> None:
    record_path = repository_root / RECORD_PATHS[4]
    with record_path.open(encoding="utf-8") as handle:
        record = json.load(handle)
    bound = float(
        record["exact_counterexample"]["maximum_absolute_response_difference"]
    )
    text = path.read_text(encoding="utf-8")
    text, replacements = re.subn(
        r'max \|difference\| = [^<]+',
        f'max |difference| &lt;= {bound:.2e}',
        text,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError("Figure 6 residual annotation was not found")
    path.write_text(text, encoding="utf-8")


def build(repository_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    output = Path(output_dir)
    if not output.is_absolute():
        output = (Path.cwd() / output).resolve()

    summary = _core.build(root, output)
    _postprocess_figure2(output / FIGURE_FILES[1])
    _postprocess_figure3(output / FIGURE_FILES[2])
    _postprocess_figure6(root, output / FIGURE_FILES[5])
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
