"""Acquire and validate the Greenough-Palmer CdTe primary source.

The source PDF is used transiently. Copyrighted PDF bytes and extracted full text are
never committed or uploaded as workflow artifacts; only digest, metadata, and validation
records are preserved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def normalize_text(value: str) -> str:
    """Normalize scan-extracted text for conservative marker matching."""
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("·", ".").replace("−", "-").replace("–", "-")
    return re.sub(r"\s+", " ", value).strip().casefold()


def parse_pdfinfo_pages(pdfinfo_text: str) -> int:
    """Read the page count from poppler pdfinfo output."""
    match = re.search(r"^Pages:\s*(\d+)\s*$", pdfinfo_text, flags=re.MULTILINE)
    if not match:
        raise ValueError("pdfinfo output does not contain a Pages field")
    return int(match.group(1))


def validate_markers(text: str, markers: list[str]) -> dict[str, bool]:
    """Return normalized containment results for declared source markers."""
    normalized = normalize_text(text)
    return {marker: normalize_text(marker) in normalized for marker in markers}


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def acquire(contract_path: Path, evidence_dir: Path) -> dict[str, Any]:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    acquisition = contract["acquisition"]
    rights = contract["rights_and_storage"]

    if rights != {
        "commit_pdf_to_repository": False,
        "upload_pdf_as_artifact": False,
        "upload_full_text_as_artifact": False,
        "preserve_only_digest_metadata_and_validation": True,
    }:
        raise ValueError("source contract must enforce digest-only preservation")

    evidence_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = evidence_dir / "source.pdf.transient"
    text_path = evidence_dir / "source.txt.transient"
    result: dict[str, Any] = {
        "schema_version": 1,
        "citation": contract["citation"],
        "source_url": acquisition["source_url"],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "success": False,
        "copyrighted_source_preserved": False,
    }

    try:
        request = urllib.request.Request(
            acquisition["source_url"],
            headers={
                "User-Agent": "MCT-research-primary-source-audit/1.0",
                "Accept": "application/pdf,*/*;q=0.1",
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
        digest = hashlib.sha256(source_bytes).hexdigest()
        result["size_bytes"] = size
        result["sha256"] = digest

        minimum = int(acquisition["minimum_size_bytes"])
        maximum = int(acquisition["maximum_size_bytes"])
        if not minimum <= size <= maximum:
            raise ValueError(f"source size {size} outside [{minimum}, {maximum}]")
        if not source_bytes.startswith(b"%PDF-"):
            raise ValueError("source does not begin with a PDF signature")

        pdf_path.write_bytes(source_bytes)
        pdfinfo = _run(["pdfinfo", str(pdf_path)]).stdout
        (evidence_dir / "pdfinfo.txt").write_text(pdfinfo, encoding="utf-8")
        pages = parse_pdfinfo_pages(pdfinfo)
        result["page_count"] = pages
        if pages != int(acquisition["expected_page_count"]):
            raise ValueError(
                f"page count {pages} != {acquisition['expected_page_count']}"
            )

        _run(["pdftotext", "-layout", str(pdf_path), str(text_path)])
        extracted_text = text_path.read_text(encoding="utf-8", errors="replace")
        marker_results = validate_markers(
            extracted_text, list(acquisition["required_text_markers"])
        )
        result["required_text_markers"] = marker_results
        missing = [marker for marker, present in marker_results.items() if not present]
        if missing:
            raise ValueError(f"required text markers missing: {missing}")

        result["success"] = True
        (evidence_dir / "sha256.txt").write_text(
            f"{digest}  greenough_palmer_1973_source.pdf\n", encoding="utf-8"
        )
        (evidence_dir / "validation.txt").write_text(
            "PASS: primary PDF signature, size, page count, and text markers validated.\n"
            "PASS: only digest and metadata evidence are preserved.\n",
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
        for transient in (pdf_path, text_path):
            transient.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    acquire(args.contract, args.evidence_dir)


if __name__ == "__main__":
    main()
