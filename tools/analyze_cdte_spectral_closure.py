#!/usr/bin/env python3
"""Evaluate gauge-invariant conventional-Kane spectral closure for static CdTe."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cdte_finite_k_projection import _read_nnkp, _sha256, _validate_kpoint_contract
from cdte_spectral_closure import analyze_conventional_spectral_closure


def analyze(
    eigenvalues_path: str | Path,
    nnkp_path: str | Path,
    contract_path: str | Path,
    finite_result_path: str | Path,
) -> dict[str, Any]:
    eigenvalues = json.loads(Path(eigenvalues_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    finite_result = json.loads(Path(finite_result_path).read_text(encoding="utf-8"))
    _, cartesian = _read_nnkp(nnkp_path)
    _validate_kpoint_contract(cartesian, contract)
    if finite_result.get("reconstruction_mode") != "selected_band_polar":
        raise ValueError("spectral closure requires the selected-band polar result")
    closure = analyze_conventional_spectral_closure(
        eigenvalues,
        cartesian,
        contract,
        finite_result["two_p"]["parameters"],
    )
    return {
        "schema_version": "1.0",
        "status": "gauge_invariant_conventional_quadratic_spectral_closure_tested",
        "input_sha256": {
            "exact_qe_eigenvalues": _sha256(eigenvalues_path),
            "nnkp": _sha256(nnkp_path),
            "finite_k_contract": _sha256(contract_path),
            "finite_k_result": _sha256(finite_result_path),
        },
        "reconstruction_mode": finite_result["reconstruction_mode"],
        "spectral_closure": closure,
        "claim_boundary": (
            "This is a gauge-invariant selected-band dispersion diagnostic at the "
            "unconverged static PBE smoke point. It does not establish reference "
            "CdTe parameters or authorize additional first-principles depth."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eigenvalues", required=True)
    parser.add_argument("--nnkp", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--finite-result", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.eigenvalues,
        args.nnkp,
        args.contract,
        args.finite_result,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
