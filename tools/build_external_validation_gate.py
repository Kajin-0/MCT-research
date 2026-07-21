#!/usr/bin/env python3
"""Build deterministic DOI acquisition and validation-route reports."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from mct_research.validation_gate import (
    prioritized_source_requests,
    rank_validation_routes,
    select_first_external_validation_route,
)
from mct_research.validation_gate_robustness import selection_robustness

DEFAULT_MANIFEST = (
    "literature/acquisition/distributional_band_edge_sources.json"
)


def _load_manifest(repository_root: Path, manifest_path: str) -> dict[str, Any]:
    with (repository_root / manifest_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _source_lookup(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(source["citation_key"]): source
        for source in manifest["sources"]
    }


def build_report(
    repository_root: str | Path,
    *,
    manifest_path: str = DEFAULT_MANIFEST,
) -> tuple[dict[str, Any], str]:
    """Return machine-readable and Markdown validation-gate reports."""

    root = Path(repository_root).resolve()
    manifest = _load_manifest(root, manifest_path)
    ranked = rank_validation_routes(manifest)
    selected = select_first_external_validation_route(manifest)
    robustness = selection_robustness(manifest)
    sources = _source_lookup(manifest)
    source_order = prioritized_source_requests(manifest)

    route_rows = []
    for rank, route in enumerate(ranked, start=1):
        route_rows.append(
            {
                "rank": rank,
                "route_id": route.route_id,
                "title": route.title,
                "score": route.score,
                "readiness": route.readiness,
                "source_priority": route.source_priority,
                "implementation_cost": route.implementation_cost,
                "source_keys": list(route.source_keys),
                "source_dois": [sources[key]["doi"] for key in route.source_keys],
                "blocking_artifacts": list(route.blocking_artifacts),
            }
        )

    requests = []
    for position, key in enumerate(source_order, start=1):
        source = sources[key]
        requests.append(
            {
                "request_order": position,
                "citation_key": key,
                "doi": source["doi"],
                "priority": source["priority"],
                "title_short": source["title_short"],
                "availability": source["availability"],
                "audit": source["audit"],
                "requested_artifacts": source["requested_artifacts"],
            }
        )

    report = {
        "schema_version": "1.1",
        "manifest_path": manifest_path,
        "selected_route": {
            "route_id": selected.route_id,
            "title": selected.title,
            "score": selected.score,
            "readiness": selected.readiness,
            "source_keys": list(selected.source_keys),
            "source_dois": [sources[key]["doi"] for key in selected.source_keys],
            "blocking_artifacts": list(selected.blocking_artifacts),
        },
        "selection_robustness": asdict(robustness),
        "ranked_routes": route_rows,
        "source_request_order": requests,
        "interpretation": (
            "Scores rank expected decision value under the current acquisition "
            "state. They are not probabilities of truth and must be updated after "
            "each source audit."
        ),
        "external_material_validation_complete": False,
    }

    lines = [
        "# External-validation route gate",
        "",
        "## Selected first route",
        "",
        f"**{selected.title}** (`{selected.route_id}`)",
        "",
        f"- score: `{selected.score}`",
        f"- readiness: `{selected.readiness}`",
        "- required DOIs:",
    ]
    lines.extend(
        f"  - `{sources[key]['doi']}`" for key in selected.source_keys
    )
    lines += ["", "Blocking artifacts:"]
    lines.extend(f"- {item}" for item in selected.blocking_artifacts)
    lines += [
        "",
        "## Local selection robustness",
        "",
        f"- closest actionable competitor: `{robustness.closest_competitor_id}`",
        f"- current score margin: `{robustness.current_margin}`",
        f"- margin after one adverse selected-route step: `{robustness.margin_after_selected_adverse_step}`",
        f"- margin after one favorable competitor step: `{robustness.margin_after_competitor_favorable_step}`",
        f"- margin after simultaneous adverse/favorable steps: `{robustness.margin_after_simultaneous_two_route_steps}`",
        f"- robust to any single one-level change: `{str(robustness.robust_to_any_single_one_level_change).lower()}`",
        f"- robust to simultaneous two-route stress: `{str(robustness.robust_to_simultaneous_adverse_and_favorable_steps).lower()}`",
        "",
        "The route is locally robust to one criterion revision, but not to the declared two-route stress test. Re-score after every source audit.",
        "",
        "## Ranked routes",
        "",
        "| Rank | Route | Score | Readiness | DOI(s) |",
        "|---:|---|---:|---|---|",
    ]
    for row in route_rows:
        dois = "<br>".join(f"`{doi}`" for doi in row["source_dois"])
        lines.append(
            f"| {row['rank']} | {row['title']} | {row['score']} | "
            f"`{row['readiness']}` | {dois} |"
        )
    lines += [
        "",
        "## Paper request order",
        "",
        "| Order | DOI | Source | Current state |",
        "|---:|---|---|---|",
    ]
    for request in requests:
        lines.append(
            f"| {request['request_order']} | `{request['doi']}` | "
            f"{request['title_short']} | `{request['audit']}` |"
        )
    lines += [
        "",
        "## Interpretation boundary",
        "",
        report["interpretation"],
        "",
        "No route currently establishes external material validation.",
    ]
    return report, "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    report, markdown = build_report(
        args.repository_root,
        manifest_path=args.manifest,
    )
    Path(args.output_json).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    Path(args.output_md).write_text(markdown, encoding="utf-8")
    print(json.dumps(report["selected_route"], sort_keys=True))


if __name__ == "__main__":
    main()
