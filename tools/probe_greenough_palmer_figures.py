"""Render the Greenough-Palmer graphical-data page for one-day calibration.

This is a temporary diagnostic. It verifies the already-audited source digest, renders
only the page containing Figures 4 and 5, and deletes the source PDF immediately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    source = json.loads(args.source.read_text(encoding="utf-8"))
    url = contract["acquisition"]["source_url"]
    expected_sha = source["source"]["sha256"]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = args.output_dir / "source.pdf.transient"
    prefix = args.output_dir / "page"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "MCT-research-figure-digitization/1.0",
            "Accept": "application/pdf,*/*;q=0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            payload = response.read()
        digest = hashlib.sha256(payload).hexdigest()
        if digest != expected_sha:
            raise RuntimeError(f"source digest changed: {digest} != {expected_sha}")
        pdf_path.write_bytes(payload)

        subprocess.run(
            [
                "pdftoppm",
                "-f",
                "5",
                "-l",
                "5",
                "-r",
                "300",
                "-png",
                "-singlefile",
                str(pdf_path),
                str(prefix),
            ],
            check=True,
        )
        image_path = args.output_dir / "page.png"
        with Image.open(image_path) as image:
            metadata = {
                "source_sha256": digest,
                "pdf_page_number_one_based": 5,
                "render_dpi": 300,
                "width_pixels": image.width,
                "height_pixels": image.height,
                "mode": image.mode,
                "temporary_artifact_retention_days": 1,
                "purpose": "calibrate reproducible digitization of Figures 4 and 5",
            }
        (args.output_dir / "render.json").write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    finally:
        pdf_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
