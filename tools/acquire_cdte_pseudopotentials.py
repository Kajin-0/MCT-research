#!/usr/bin/env python3
"""Acquire and verify the exact pinned CdTe pseudopotential bytes.

Files are downloaded from an immutable GitHub commit, checked against their Git
blob SHA-1 identifiers, inspected structurally, and written with a SHA-256
manifest. The files are not added to the research repository by this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import tempfile
from typing import Any
from urllib.parse import quote
from urllib.request import urlopen

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.inspect_pseudopotential import inspect, validate


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git identity


def _download(url: str, timeout_seconds: float) -> bytes:
    with urlopen(url, timeout=timeout_seconds) as response:  # noqa: S310 - pinned HTTPS
        final_url = response.geturl()
        if not final_url.startswith("https://raw.githubusercontent.com/"):
            raise ValueError(f"unexpected download endpoint: {final_url}")
        return response.read()


def _raw_url(repository: str, commit: str, path: str) -> str:
    safe_path = "/".join(quote(part, safe="") for part in PurePosixPath(path).parts)
    return f"https://raw.githubusercontent.com/{repository}/{commit}/{safe_path}"


def _verify_download(
    *,
    data: bytes,
    expected_blob_sha1: str,
    expected_md5: str | None,
    label: str,
) -> dict[str, Any]:
    actual_blob = git_blob_sha1(data)
    if actual_blob != expected_blob_sha1:
        raise ValueError(
            f"{label} Git blob mismatch: {actual_blob}, expected {expected_blob_sha1}"
        )
    actual_md5 = hashlib.md5(data).hexdigest()  # noqa: S324 - provenance only
    if expected_md5 is not None and actual_md5 != expected_md5:
        raise ValueError(f"{label} MD5 mismatch: {actual_md5}, expected {expected_md5}")
    return {
        "size_bytes": len(data),
        "git_blob_sha1": actual_blob,
        "sha256": hashlib.sha256(data).hexdigest(),
        "md5": actual_md5,
    }


def acquire(
    selection_path: str | Path,
    output_dir: str | Path,
    manifest_path: str | Path,
    *,
    timeout_seconds: float = 60.0,
) -> dict[str, Any]:
    selection_file = Path(selection_path)
    selection = json.loads(selection_file.read_text(encoding="utf-8"))
    upstream = selection["upstream"]
    repository = str(upstream["repository"])
    commit = str(upstream["commit"])
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "source_selection": str(selection_file),
        "upstream_repository": repository,
        "upstream_commit": commit,
        "acquisition_complete": False,
        "calculation_executed": False,
        "files": {},
    }

    with tempfile.TemporaryDirectory() as temporary:
        temporary_dir = Path(temporary)
        for element, metadata in selection["elements"].items():
            for file_format, path_key, blob_key, md5_key in (
                ("upf", "upf_path", "upf_git_blob_sha1", None),
                ("psp8", "psp8_path", "psp8_git_blob_sha1", "psp8_pseudodojo_md5"),
            ):
                relative_path = str(metadata[path_key])
                label = f"{element}_{file_format}"
                url = _raw_url(repository, commit, relative_path)
                data = _download(url, timeout_seconds)
                hashes = _verify_download(
                    data=data,
                    expected_blob_sha1=str(metadata[blob_key]),
                    expected_md5=None if md5_key is None else str(metadata[md5_key]),
                    label=label,
                )

                filename = PurePosixPath(relative_path).name
                destination = output / filename
                destination.write_bytes(data)
                inspection_path = temporary_dir / filename
                inspection_path.write_bytes(data)
                inspected = inspect(inspection_path, file_format)
                validate(
                    inspected,
                    expected_element=element,
                    expected_z_valence=float(metadata["z_valence"]),
                    expected_functional="PBE" if file_format == "upf" else None,
                    expected_pspxc=11 if file_format == "psp8" else None,
                    require_fully_relativistic=True,
                    require_spin_orbit=True,
                    require_nlcc=file_format == "upf",
                )
                if inspected["sha256"] != hashes["sha256"]:
                    raise AssertionError(f"{label} inspection hash mismatch")

                manifest["files"][label] = {
                    "upstream_path": relative_path,
                    "download_url": url,
                    "output_path": str(destination),
                    **hashes,
                    "inspection": {
                        key: value
                        for key, value in inspected.items()
                        if key not in {"path", "sha256", "md5", "size_bytes"}
                    },
                }

    manifest["acquisition_complete"] = True
    manifest_file = Path(manifest_path)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--selection-json",
        default="first_principles/a0/cdte_pseudopotential_selection.json",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--manifest-json", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=60.0)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = acquire(
        args.selection_json,
        args.output_dir,
        args.manifest_json,
        timeout_seconds=args.timeout_seconds,
    )
    for label, metadata in sorted(manifest["files"].items()):
        print(f"{label} sha256={metadata['sha256']}")
    print(f"manifest={args.manifest_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
