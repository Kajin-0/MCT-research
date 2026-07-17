"""Acquire and validate the official Browder-Ballard Optica HTML table.

Publisher HTML is used transiently. Only source digests, HTTP metadata, and a
canonical comparison against the committed CdTe Table I transcription are kept.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
from html.parser import HTMLParser
import json
import math
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class TableParser(HTMLParser):
    """Collect plain-text rows from every HTML table."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table_depth = 0
        self._current_table: list[list[str]] | None = None
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        tag = tag.casefold()
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self._current_table = []
        elif self._table_depth == 1 and tag == "tr":
            self._current_row = []
        elif self._table_depth == 1 and tag in {"td", "th"}:
            self._current_cell = []

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if self._table_depth == 1 and tag in {"td", "th"}:
            if self._current_row is not None and self._current_cell is not None:
                value = " ".join("".join(self._current_cell).split())
                self._current_row.append(value)
            self._current_cell = None
        elif self._table_depth == 1 and tag == "tr":
            if self._current_table is not None and self._current_row:
                self._current_table.append(self._current_row)
            self._current_row = None
        elif tag == "table" and self._table_depth:
            if self._table_depth == 1 and self._current_table is not None:
                self.tables.append(self._current_table)
                self._current_table = None
            self._table_depth -= 1


def normalize_text(value: str) -> str:
    value = html.unescape(value)
    value = value.replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", value).strip().casefold()


def parse_number(value: str) -> float:
    normalized = normalize_text(value)
    normalized = normalized.replace("×", "x").replace("−", "-")
    match = re.search(r"[-+]?\d+(?:\.\d+)?", normalized)
    if not match:
        raise ValueError(f"no number found in cell {value!r}")
    return float(match.group(0))


def load_committed_rows(path: Path) -> list[tuple[float, float]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        (float(row["temperature_k"]), float(row["alpha_1e6_per_k"]))
        for row in rows
    ]


def canonical_rows_digest(rows: list[tuple[float, float]]) -> str:
    payload = "".join(f"{temperature:.12g},{alpha:.12g}\n" for temperature, alpha in rows)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def find_cdte_rows(tables: list[list[list[str]]]) -> list[tuple[float, float]]:
    candidates: list[list[tuple[float, float]]] = []
    for table in tables:
        parsed: list[tuple[float, float]] = []
        for row in table:
            if len(row) < 2:
                continue
            try:
                temperature = parse_number(row[0])
                alpha = parse_number(row[1])
            except ValueError:
                continue
            if 0.0 <= temperature <= 500.0 and -20.0 <= alpha <= 30.0:
                parsed.append((temperature, alpha))
        if len(parsed) >= 20:
            candidates.append(parsed)
    if not candidates:
        raise ValueError("no publisher table with at least 20 numeric rows was found")
    return max(candidates, key=len)


def acquire(contract_path: Path, evidence_dir: Path) -> dict[str, Any]:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    acquisition = contract["acquisition"]
    validation = contract["table_validation"]
    rights = contract["rights_and_storage"]
    expected_rights = {
        "commit_publisher_html": False,
        "upload_publisher_html_as_artifact": False,
        "preserve_only_digest_metadata_and_table_validation": True,
    }
    if rights != expected_rights:
        raise ValueError("contract must enforce digest-only publisher-page preservation")

    evidence_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "schema_version": 1,
        "citation": contract["citation"],
        "source_url": acquisition["source_url"],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "success": False,
        "publisher_html_preserved": False,
    }

    try:
        request = urllib.request.Request(
            acquisition["source_url"],
            headers={
                "User-Agent": "MCT-research-primary-table-audit/1.0",
                "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1",
                "Accept-Encoding": "identity",
            },
        )
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            source_bytes = response.read()
            headers = {key.lower(): value for key, value in response.headers.items()}
            result["http_status"] = getattr(response, "status", None)
            result["response_content_type"] = headers.get("content-type")
            result["response_etag"] = headers.get("etag")
            result["response_last_modified"] = headers.get("last-modified")

        size = len(source_bytes)
        result["size_bytes"] = size
        result["source_sha256"] = hashlib.sha256(source_bytes).hexdigest()
        if not int(acquisition["minimum_size_bytes"]) <= size <= int(
            acquisition["maximum_size_bytes"]
        ):
            raise ValueError(f"publisher page size {size} is outside contract bounds")

        content_type = str(result.get("response_content_type") or "").casefold()
        if not content_type.startswith(acquisition["expected_media_type_prefix"]):
            raise ValueError(f"unexpected content type {content_type!r}")

        encoding_match = re.search(r"charset=([^;\s]+)", content_type)
        encoding = encoding_match.group(1).strip('"') if encoding_match else "utf-8"
        page = source_bytes.decode(encoding, errors="replace")
        plain = normalize_text(re.sub(r"<[^>]+>", " ", page))
        marker_results = {
            marker: normalize_text(marker) in plain
            for marker in acquisition["required_text_markers"]
        }
        result["required_text_markers"] = marker_results
        missing = [marker for marker, present in marker_results.items() if not present]
        if missing:
            raise ValueError(f"required publisher markers missing: {missing}")

        parser = TableParser()
        parser.feed(page)
        publisher_rows = find_cdte_rows(parser.tables)
        committed_path = Path(validation["committed_csv"])
        committed_rows = load_committed_rows(committed_path)

        expected_count = int(validation["expected_row_count"])
        if len(publisher_rows) != expected_count:
            raise ValueError(
                f"publisher CdTe row count {len(publisher_rows)} != {expected_count}"
            )
        if len(committed_rows) != expected_count:
            raise ValueError(
                f"committed CdTe row count {len(committed_rows)} != {expected_count}"
            )

        differences = [
            (abs(left[0] - right[0]), abs(left[1] - right[1]))
            for left, right in zip(publisher_rows, committed_rows, strict=True)
        ]
        maximum_temperature_difference = max(item[0] for item in differences)
        maximum_alpha_difference = max(item[1] for item in differences)
        if maximum_temperature_difference > 1e-12 or maximum_alpha_difference > 1e-12:
            raise ValueError(
                "committed transcription differs from official publisher Table I"
            )

        first_expected = tuple(float(value) for value in validation["expected_first_row"])
        last_expected = tuple(float(value) for value in validation["expected_last_row"])
        if publisher_rows[0] != first_expected or publisher_rows[-1] != last_expected:
            raise ValueError("publisher table endpoints differ from acquisition contract")

        result["table_validation"] = {
            "row_count": len(publisher_rows),
            "publisher_rows_sha256": canonical_rows_digest(publisher_rows),
            "committed_rows_sha256": canonical_rows_digest(committed_rows),
            "maximum_temperature_difference_k": maximum_temperature_difference,
            "maximum_alpha_difference_1e6_per_k": maximum_alpha_difference,
            "first_row": list(publisher_rows[0]),
            "last_row": list(publisher_rows[-1]),
            "exact_match": True,
        }
        result["success"] = True
        (evidence_dir / "source_sha256.txt").write_text(
            f"{result['source_sha256']}  optica-browder-1972-table-page.html\n",
            encoding="utf-8",
        )
        (evidence_dir / "validation.txt").write_text(
            "PASS: official Optica page identity and Table I transcription validated.\n"
            "PASS: publisher HTML was not preserved.\n",
            encoding="utf-8",
        )
        return result
    except Exception as exc:
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
        (evidence_dir / "validation.txt").write_text(
            f"FAIL: {type(exc).__name__}: {exc}\n", encoding="utf-8"
        )
        raise
    finally:
        (evidence_dir / "acquisition.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    acquire(args.contract, args.evidence_dir)


if __name__ == "__main__":
    main()
