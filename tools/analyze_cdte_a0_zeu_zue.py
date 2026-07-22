#!/usr/bin/env python3
"""Analyze the bounded CdTe A0 zeu/zue same-state response diagnostic."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

_FATAL_PATTERN = re.compile(r"Error in routine|NaN|SIGSEGV|stopping", re.IGNORECASE)
_FLOAT = r"[-+0-9.Ee]+"


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def _last_dielectric_tensor(text: str) -> list[list[float]]:
    marker = "Dielectric constant in cartesian axis"
    positions = [match.start() for match in re.finditer(marker, text)]
    for start in reversed(positions):
        rows = re.findall(
            rf"\(\s*({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*\)",
            text[start : start + 1000],
        )
        if len(rows) >= 3:
            return [[float(value) for value in row] for row in rows[:3]]
    raise ValueError("missing complete dielectric tensor")


def _tensor_block(
    text: str,
    *,
    marker: str,
    row_initial: str,
) -> list[dict[str, Any]]:
    positions = [match.start() for match in re.finditer(re.escape(marker), text)]
    if not positions:
        raise ValueError(f"missing tensor marker: {marker}")
    atom_pattern = re.compile(r"^\s*atom\s+(\d+)\s+([A-Za-z][A-Za-z0-9]*)[^\n]*$", re.MULTILINE)
    row_pattern = re.compile(
        rf"^\s*{row_initial}[xyz]\s*\(\s*({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*\)\s*$",
        re.MULTILINE,
    )
    for start in reversed(positions):
        segment = text[start : start + 5000]
        stop_candidates = [
            segment.find("Effective charges Sum:", 1),
            segment.find("Effective charges (", len(marker)),
            segment.find("Diagonalizing the dynamical matrix", 1),
        ]
        stop_candidates = [candidate for candidate in stop_candidates if candidate > 0]
        if stop_candidates:
            segment = segment[: min(stop_candidates)]
        atoms = list(atom_pattern.finditer(segment))
        parsed: list[dict[str, Any]] = []
        for index, atom in enumerate(atoms):
            atom_end = atoms[index + 1].start() if index + 1 < len(atoms) else len(segment)
            rows = row_pattern.findall(segment[atom.end() : atom_end])
            if len(rows) != 3:
                parsed = []
                break
            parsed.append(
                {
                    "index": int(atom.group(1)),
                    "symbol": atom.group(2),
                    "tensor": [[float(value) for value in row] for row in rows],
                }
            )
        if parsed:
            parsed.sort(key=lambda item: item["index"])
            expected = list(range(1, len(parsed) + 1))
            if [item["index"] for item in parsed] != expected:
                raise ValueError("non-contiguous atom indices in effective-charge tensor")
            return parsed
    raise ValueError(f"no complete tensor block found for marker: {marker}")


def _sum_tensors(atoms: list[dict[str, Any]]) -> list[list[float]]:
    total = [[0.0, 0.0, 0.0] for _ in range(3)]
    for atom in atoms:
        tensor = atom["tensor"]
        for row in range(3):
            for column in range(3):
                total[row][column] += float(tensor[row][column])
    return total


def _max_abs_matrix(matrix: list[list[float]]) -> float:
    return max(abs(float(value)) for row in matrix for value in row)


def _max_tensor_difference(
    zeu_atoms: list[dict[str, Any]], zue_atoms: list[dict[str, Any]]
) -> float:
    zeu_identity = [(item["index"], item["symbol"]) for item in zeu_atoms]
    zue_identity = [(item["index"], item["symbol"]) for item in zue_atoms]
    if zeu_identity != zue_identity:
        raise ValueError("zeu/zue atom identities differ")
    return max(
        abs(
            float(zeu_atom["tensor"][row][column])
            - float(zue_atom["tensor"][row][column])
        )
        for zeu_atom, zue_atom in zip(zeu_atoms, zue_atoms, strict=True)
        for row in range(3)
        for column in range(3)
    )


def _sampled_band_separations(eigenvalues: dict[str, Any]) -> dict[str, Any]:
    blocks = eigenvalues.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("eigenvalue record has no blocks")
    records: list[dict[str, Any]] = []
    for block in blocks:
        values = block.get("eigenvalues_ev")
        occupations = block.get("occupations")
        if not isinstance(values, list) or not isinstance(occupations, list):
            raise ValueError("incomplete eigenvalue block")
        if len(values) != len(occupations) or not values:
            raise ValueError("eigenvalue/occupation length mismatch")
        occupied = [float(value) for value, occ in zip(values, occupations, strict=True) if float(occ) > 0.5]
        unoccupied = [float(value) for value, occ in zip(values, occupations, strict=True) if float(occ) <= 0.5]
        if not occupied or not unoccupied:
            raise ValueError("sampled block lacks occupied or unoccupied states")
        highest = max(occupied)
        lowest = min(unoccupied)
        records.append(
            {
                "block_index": int(block.get("index", len(records) + 1)),
                "k_point_crystal": block.get("k_point_crystal"),
                "highest_occupied_ev": highest,
                "lowest_unoccupied_ev": lowest,
                "separation_ev": lowest - highest,
            }
        )
    minimum = min(records, key=lambda item: item["separation_ev"])
    return {
        "blocks": records,
        "minimum_separation_ev": minimum["separation_ev"],
        "minimum_block_index": minimum["block_index"],
        "minimum_k_point_crystal": minimum["k_point_crystal"],
    }


def _route_convergence(text: str, *, marker: str, minimum_count: int) -> dict[str, Any]:
    count = len(re.findall(r"Convergence has been achieved", text, flags=re.IGNORECASE))
    checks = {
        "job_done": "JOB DONE" in text,
        "no_fatal_marker": _FATAL_PATTERN.search(text) is None,
        "route_marker_present": marker in text,
        "response_convergence_count": count >= minimum_count,
    }
    return {"count": count, "checks": checks, "passed": all(checks.values())}


def analyze(
    scf_path: str | Path,
    zeu_path: str | Path,
    zue_path: str | Path,
    eigenvalues_path: str | Path,
    state_manifest_path: str | Path,
    contract_path: str | Path,
) -> dict[str, Any]:
    scf_text = Path(scf_path).read_text(encoding="utf-8", errors="replace")
    zeu_text = Path(zeu_path).read_text(encoding="utf-8", errors="replace")
    zue_text = Path(zue_path).read_text(encoding="utf-8", errors="replace")
    eigenvalues = _load_json(eigenvalues_path)
    state_manifest = _load_json(state_manifest_path)
    contract = _load_json(contract_path)
    if contract.get("stage") != "A0_same_state_zeu_zue_response_diagnostic":
        raise ValueError("unexpected zeu/zue contract stage")

    zeu_marker = (
        "Effective charges (d Force / dE) in cartesian axis without acoustic sum rule applied"
    )
    zue_marker = "Effective charges (d P / du) in cartesian axis"
    zeu_atoms = _tensor_block(zeu_text, marker=zeu_marker, row_initial="E")
    zue_atoms = _tensor_block(zue_text, marker=zue_marker, row_initial="P")
    zeu_sum = _sum_tensors(zeu_atoms)
    zue_sum = _sum_tensors(zue_atoms)
    zeu_neutrality = _max_abs_matrix(zeu_sum)
    zue_neutrality = _max_abs_matrix(zue_sum)
    route_difference = _max_tensor_difference(zeu_atoms, zue_atoms)
    sampled = _sampled_band_separations(eigenvalues)

    thresholds = contract["thresholds"]
    minimum_count = int(thresholds["minimum_phonon_response_convergence_count"])
    zeu_convergence = _route_convergence(
        zeu_text, marker=zeu_marker, minimum_count=minimum_count
    )
    zue_convergence = _route_convergence(
        zue_text, marker=zue_marker, minimum_count=minimum_count
    )
    scf_checks = {
        "convergence_achieved": "convergence has been achieved" in scf_text.lower(),
        "job_done": "JOB DONE" in scf_text,
        "no_fatal_marker": _FATAL_PATTERN.search(scf_text) is None,
    }
    same_state_checks = {
        "base_and_zeu_save_match": bool(state_manifest.get("base_and_zeu_save_match")),
        "base_and_zue_save_match": bool(state_manifest.get("base_and_zue_save_match")),
        "one_scf_executed": state_manifest.get("scf_execution_count") == 1,
        "exactly_two_response_routes": state_manifest.get("response_route_count") == 2,
        "route_settings_match_contract": bool(
            state_manifest.get("route_settings_match_contract")
        ),
    }
    checks = {
        "zeu_raw_charge_neutrality": zeu_neutrality
        <= float(thresholds["maximum_raw_charge_neutrality_residual_e"]),
        "zue_raw_charge_neutrality": zue_neutrality
        <= float(thresholds["maximum_raw_charge_neutrality_residual_e"]),
        "zeu_zue_tensor_agreement": route_difference
        <= float(thresholds["maximum_route_tensor_difference_e"]),
        "sampled_insulating_separation": sampled["minimum_separation_ev"]
        > float(thresholds["minimum_sampled_occupied_unoccupied_separation_ev"]),
        "scf_converged": all(scf_checks.values()),
        "zeu_response_converged": zeu_convergence["passed"],
        "zue_response_converged": zue_convergence["passed"],
        "same_state_provenance": all(same_state_checks.values()),
        "complete_zeu_tensor": len(zeu_atoms) == 2,
        "complete_zue_tensor": len(zue_atoms) == 2,
    }
    passed = all(checks.values())
    policy = contract["decision_policy"]
    return {
        "schema_version": "1.0",
        "stage": contract["stage"],
        "status": "same_state_zeu_zue_diagnostic_completed",
        "input_sha256": {
            "scf": _sha256(scf_path),
            "zeu": _sha256(zeu_path),
            "zue": _sha256(zue_path),
            "eigenvalues": _sha256(eigenvalues_path),
            "state_manifest": _sha256(state_manifest_path),
            "contract": _sha256(contract_path),
        },
        "observables": {
            "zeu_atoms": zeu_atoms,
            "zue_atoms": zue_atoms,
            "zeu_raw_charge_sum_tensor_e": zeu_sum,
            "zue_raw_charge_sum_tensor_e": zue_sum,
            "zeu_maximum_raw_charge_neutrality_residual_e": zeu_neutrality,
            "zue_maximum_raw_charge_neutrality_residual_e": zue_neutrality,
            "maximum_zeu_zue_tensor_difference_e": route_difference,
            "zeu_dielectric_tensor": _last_dielectric_tensor(zeu_text),
            "zue_dielectric_tensor": _last_dielectric_tensor(zue_text),
            "sampled_band_separations": sampled,
            "scf_checks": scf_checks,
            "zeu_convergence": zeu_convergence,
            "zue_convergence": zue_convergence,
            "same_state_checks": same_state_checks,
        },
        "checks": checks,
        "decision": {
            "all_mandatory_conditions_pass": passed,
            "a1_electron_phonon_authorized": False,
            "automatic_followup_authorized": False,
            "terminate_current_qe_pbe_pseudopotential_polar_path_for_a1": not passed,
            "authorize_only_separate_k_grid_cutoff_design_review": passed,
            "action": policy["pass_action"] if passed else policy["failure_action"],
            "failed_checks": [name for name, value in checks.items() if not value],
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scf", required=True)
    parser.add_argument("--zeu", required=True)
    parser.add_argument("--zue", required=True)
    parser.add_argument("--eigenvalues", required=True)
    parser.add_argument("--state-manifest", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.scf,
        args.zeu,
        args.zue,
        args.eigenvalues,
        args.state_manifest,
        args.contract,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
