#!/usr/bin/env python3
"""Audit the paired 2x2x2 HgCdTe gap-acquisition contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Mapping

import numpy as np

SCHEMA_VERSION = "1.0"
PROTOCOL_ID = "hgcdte_paired_gap_2x2x2_v1"
MODALITIES = ("magneto_optical", "absorption")
PARAMETERS = (
    "latent_intercept",
    "latent_composition_slope",
    "absorption_class_offset",
    "carrier_contribution",
    "vacancy_contribution",
)
PLACEHOLDERS = ("PLANNING", "REQUIRED", "TBD", "PLACEHOLDER")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _req(m: Mapping[str, Any], key: str, where: str) -> Any:
    if key not in m:
        raise ValueError(f"{where} is missing required field {key!r}")
    return m[key]


def _num(value: Any, name: str, *, positive: bool = False) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be finite") from exc
    if not math.isfinite(number) or (positive and number <= 0):
        raise ValueError(f"{name} must be {'positive' if positive else 'finite'}")
    return number


def _text(value: Any, name: str) -> str:
    if value is None:
        raise ValueError(f"{name} must be completed and non-placeholder")
    text = str(value).strip()
    if not text or any(token in text.upper() for token in PLACEHOLDERS):
        raise ValueError(f"{name} must be completed and non-placeholder")
    return text


def _code(value: Any, name: str) -> int:
    code = int(value)
    if code not in (-1, 1):
        raise ValueError(f"{name} must be -1 or +1")
    return code


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _row(x: float, modality: str, carrier: float, vacancy: float) -> list[float]:
    if modality == "magneto_optical":
        return [1.0, x, 0.0, 0.0, 0.0]
    if modality == "absorption":
        return [1.0, x, 1.0, carrier, -vacancy]
    raise ValueError(f"unsupported modality {modality!r}")


def _diagnostics(matrix: np.ndarray) -> dict[str, Any]:
    singular = np.linalg.svd(matrix, compute_uv=False)
    tol = max(matrix.shape) * np.finfo(float).eps * singular[0]
    rank = int(np.sum(singular > tol))
    result: dict[str, Any] = {
        "observation_count": int(matrix.shape[0]),
        "parameter_count": int(matrix.shape[1]),
        "rank": rank,
        "residual_degrees_of_freedom": int(matrix.shape[0] - rank),
        "singular_values": singular.tolist(),
        "condition_number": None,
        "maximum_leverage": None,
    }
    if rank == matrix.shape[1]:
        covariance = np.linalg.inv(matrix.T @ matrix)
        result["condition_number"] = float(singular[0] / singular[-1])
        result["maximum_leverage"] = float(
            np.max(np.diag(matrix @ covariance @ matrix.T))
        )
        result["parameter_standard_error_per_unit_noise"] = {
            key: float(value)
            for key, value in zip(PARAMETERS, np.sqrt(np.diag(covariance)), strict=True)
        }
    return result


def _factorial(specimens: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if len(specimens) != 8:
        raise ValueError("package requires exactly eight physical specimens")
    result: dict[str, dict[str, Any]] = {}
    states = []
    for specimen in specimens:
        specimen_id = str(_req(specimen, "specimen_id", "specimen")).strip()
        if not specimen_id or specimen_id in result:
            raise ValueError("specimen IDs must be unique and non-empty")
        codes = dict(_req(specimen, "nominal_codes", specimen_id))
        state = tuple(_code(codes[key], f"{specimen_id} {key}") for key in (
            "composition", "carrier", "vacancy"
        ))
        states.append(state)
        result[specimen_id] = specimen
    expected = {
        (x, carrier, vacancy)
        for x in (-1, 1)
        for carrier in (-1, 1)
        for vacancy in (-1, 1)
    }
    if set(states) != expected:
        raise ValueError("specimens must contain the complete 2x2x2 factorial")
    return result


def _validate_lineage(specimen: dict[str, Any], *, completed: bool) -> None:
    specimen_id = specimen["specimen_id"]
    lineage = dict(_req(specimen, "lineage", specimen_id))
    fields = (
        "wafer_id", "coupon_id", "growth_method", "growth_run_id",
        "passivation", "contact_state", "storage_history", "processing_history",
    )
    for field in fields:
        _req(lineage, field, f"{specimen_id}.lineage")
    if not isinstance(lineage["processing_history"], list):
        raise ValueError("processing_history must be a list")
    if completed:
        for field in fields[:-1]:
            _text(lineage[field], f"{specimen_id}.lineage.{field}")


def _composition(
    specimens: dict[str, dict[str, Any]], design: dict[str, Any], *, completed: bool
) -> tuple[dict[str, float], dict[str, Any]]:
    reference = _num(design["composition_reference_x"], "composition reference")
    scale = _num(design["composition_scale_x"], "composition scale", positive=True)
    target = _num(design["composition_sigma_target_x"], "composition sigma target", positive=True)
    hard = _num(design["composition_sigma_hard_maximum_x"], "composition sigma hard limit", positive=True)
    codes: dict[str, float] = {}
    groups: dict[int, list[tuple[float, float]]] = {-1: [], 1: []}
    methods_complete = True
    for specimen_id, specimen in specimens.items():
        item = dict(_req(specimen, "composition", specimen_id))
        value = _num(item.get("value_x"), f"{specimen_id} composition")
        sigma = _num(item.get("sigma_x"), f"{specimen_id} composition sigma", positive=True)
        if not 0 <= value <= 1:
            raise ValueError("composition must lie in [0,1]")
        code = int(specimen["nominal_codes"]["composition"])
        groups[code].append((value, sigma))
        codes[specimen_id] = (value - reference) / scale
        try:
            _text(item.get("method"), f"{specimen_id} composition method")
            _text(item.get("calibration_id"), f"{specimen_id} composition calibration")
        except ValueError:
            methods_complete = False
            if completed:
                raise
        thickness = dict(_req(specimen, "thickness", specimen_id))
        if completed:
            _num(thickness.get("value_um"), f"{specimen_id} thickness", positive=True)
            _num(thickness.get("sigma_um"), f"{specimen_id} thickness sigma", positive=True)
            uniformity = _num(thickness.get("lateral_uniformity_fraction"), f"{specimen_id} uniformity")
            if not 0 <= uniformity <= 1:
                raise ValueError("lateral_uniformity_fraction must lie in [0,1]")
            _text(thickness.get("method"), f"{specimen_id} thickness method")
    def mean_sigma(values: list[tuple[float, float]]) -> tuple[float, float]:
        return (
            float(np.mean([value for value, _ in values])),
            math.sqrt(sum(sigma * sigma for _, sigma in values)) / len(values),
        )
    low, low_sigma = mean_sigma(groups[-1])
    high, high_sigma = mean_sigma(groups[1])
    max_sigma = max(sigma for values in groups.values() for _, sigma in values)
    return codes, {
        "reference_x": reference,
        "scale_x": scale,
        "low_mean_x": low,
        "high_mean_x": high,
        "low_mean_sigma_x": low_sigma,
        "high_mean_sigma_x": high_sigma,
        "separation_sigma": abs(high - low) / math.hypot(low_sigma, high_sigma),
        "maximum_sigma_x": max_sigma,
        "target_sigma_x": target,
        "hard_maximum_sigma_x": hard,
        "target_pass": max_sigma <= target,
        "hard_maximum_pass": max_sigma <= hard,
        "completed_methods": methods_complete,
    }


def _group_codes(
    values: dict[str, tuple[int, float, float]], name: str
) -> tuple[dict[str, float], dict[str, float]]:
    groups = {
        code: [(sid, value, sigma) for sid, (label, value, sigma) in values.items() if label == code]
        for code in (-1, 1)
    }
    if any(len(group) != 4 for group in groups.values()):
        raise ValueError(f"{name} requires four low and four high specimens")
    means = {code: float(np.mean([item[1] for item in group])) for code, group in groups.items()}
    if means[1] <= means[-1]:
        raise ValueError(f"{name} high achieved value must exceed low")
    mean_sigmas = {
        code: math.sqrt(sum(item[2] ** 2 for item in group)) / len(group)
        for code, group in groups.items()
    }
    center = 0.5 * (means[1] + means[-1])
    half = 0.5 * (means[1] - means[-1])
    codes = {sid: (value - center) / half for group in groups.values() for sid, value, _ in group}
    return codes, {
        "low_mean": means[-1], "high_mean": means[1],
        "low_mean_sigma": mean_sigmas[-1], "high_mean_sigma": mean_sigmas[1],
        "separation_sigma": (means[1] - means[-1]) / math.hypot(mean_sigmas[-1], mean_sigmas[1]),
        "center": center, "half_span": half,
    }


def materialize_planning_observations(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    plan = dict(_req(payload, "observation_plan", "package"))
    orders = dict(_req(plan, "orders", "observation_plan"))
    result = []
    for block_id, slots in orders.items():
        if len(slots) != 16:
            raise ValueError(f"{block_id} planning order must contain 16 slots")
        for order, token in enumerate(slots, start=1):
            specimen_id, modality = str(token).split(":", 1)
            result.append({
                "observation_id": f"{block_id}_{specimen_id}_{'MO' if modality == 'magneto_optical' else 'ABS'}",
                "specimen_id": specimen_id,
                "temperature_block_id": block_id,
                "modality": modality,
                "measurement_area_id": "PLANNING_REQUIRED",
                "status": "planned",
                "measurement_order": order,
                "technical_replicate_target": int(plan["technical_replicate_target"]),
                "technical_replicate_count": None,
                "raw_data": {"native_uri": None, "sha256": None, "format": None},
                "calibration_ids": ["PLANNING_REQUIRED"],
                "temperature": {"measured_K": None, "sigma_K": None},
                "extraction": {
                    "edge_eV": None, "sigma_edge_eV": None, "method_id": None,
                    "software_commit": None, "covariance_uri": None,
                    "analysis_record_uri": None,
                },
            })
    return result


def _planning_states(
    specimens: dict[str, dict[str, Any]], payload: Mapping[str, Any], block_ids: list[str]
) -> dict[str, dict[str, tuple[str, float, float, float, float]]]:
    plan = dict(_req(payload, "state_plan", "package"))
    carrier = dict(plan["carrier"])
    vacancy = dict(plan["vacancy_proxy"])
    result = {}
    for block_id in block_ids:
        result[block_id] = {}
        for sid, specimen in specimens.items():
            c = int(specimen["nominal_codes"]["carrier"])
            v = int(specimen["nominal_codes"]["vacancy"])
            result[block_id][sid] = (
                str(carrier["polarity"]),
                math.log10(float(carrier["low_density_cm3"] if c < 0 else carrier["high_density_cm3"])),
                float(carrier["sigma_log10_density"]),
                float(vacancy["low_value"] if v < 0 else vacancy["high_value"]),
                float(vacancy["sigma"]),
            )
    return result


def _completed_states(
    specimens: dict[str, dict[str, Any]], block_ids: list[str]
) -> tuple[dict[str, dict[str, tuple[str, float, float, float, float]]], bool, bool]:
    result = {block: {} for block in block_ids}
    processing_ok = True
    drift_ok = True
    for sid, specimen in specimens.items():
        states = dict(_req(specimen, "state_by_temperature", sid))
        if set(states) != set(block_ids):
            raise ValueError(f"{sid} must contain both temperature states")
        for block_id in block_ids:
            state = dict(states[block_id])
            processing_ok &= state.get("processing_between_paired_modalities") is False
            drift = dict(_req(state, "state_drift_check", f"{sid}.{block_id}"))
            drift_ok &= _num(drift.get("pre_post_hall_fractional_change"), "state drift") <= _num(
                drift.get("maximum_allowed_fractional_change"), "drift limit", positive=True
            )
            carrier = dict(_req(state, "carrier", f"{sid}.{block_id}"))
            vacancy = dict(_req(state, "vacancy_proxy", f"{sid}.{block_id}"))
            polarity = str(carrier.get("polarity", "")).lower()
            if polarity not in ("n", "p"):
                raise ValueError("carrier polarity must be n or p")
            density = _num(carrier.get("density_cm3"), "carrier density", positive=True)
            carrier_sigma = _num(carrier.get("sigma_log10_density"), "carrier sigma", positive=True)
            _num(carrier.get("mobility_cm2_Vs"), "mobility", positive=True)
            _num(carrier.get("sigma_mobility_cm2_Vs"), "mobility sigma", positive=True)
            _text(carrier.get("method"), "carrier method")
            _text(carrier.get("calibration_id"), "carrier calibration")
            vacancy_value = _num(vacancy.get("value"), "vacancy proxy")
            vacancy_sigma = _num(vacancy.get("sigma"), "vacancy sigma", positive=True)
            _text(vacancy.get("method"), "vacancy method")
            _text(vacancy.get("calibration_id"), "vacancy calibration")
            _text(vacancy.get("units"), "vacancy units")
            for name, record in (("carrier", carrier), ("vacancy", vacancy)):
                assignment = str(record.get("assignment_basis", ""))
                if assignment not in ("same_specimen", "witness"):
                    raise ValueError(f"{name} assignment_basis must be same_specimen or witness")
                if assignment == "witness":
                    _text(record.get("witness_specimen_id"), f"{name} witness ID")
                    _text(record.get("transfer_uncertainty_record_uri"), f"{name} transfer uncertainty")
            result[block_id][sid] = (
                polarity, math.log10(density), carrier_sigma, vacancy_value, vacancy_sigma
            )
    return result, processing_ok, drift_ok


def _validate_completed_observation(
    observation: dict[str, Any], block: dict[str, Any]
) -> tuple[str, str, str, int, bool, bool]:
    oid = str(_req(observation, "observation_id", "observation"))
    sid = str(_req(observation, "specimen_id", oid))
    modality = str(_req(observation, "modality", oid))
    if modality not in MODALITIES:
        raise ValueError("unsupported modality")
    area = _text(_req(observation, "measurement_area_id", oid), "measurement area")
    if observation.get("status") != "complete":
        raise ValueError(f"{oid} must be complete")
    order = int(_req(observation, "measurement_order", oid))
    target = int(_req(observation, "technical_replicate_target", oid))
    count = int(observation.get("technical_replicate_count", 0))
    if target < 2 or count < 2:
        raise ValueError("at least two technical replicates are required")
    raw = dict(_req(observation, "raw_data", oid))
    _text(raw.get("native_uri"), "raw native URI")
    _text(raw.get("format"), "raw format")
    if not SHA256.fullmatch(str(raw.get("sha256", "")).lower()):
        raise ValueError("raw SHA-256 is invalid")
    calibrations = observation.get("calibration_ids")
    if not isinstance(calibrations, list) or not calibrations:
        raise ValueError("calibration IDs are required")
    for value in calibrations:
        _text(value, "calibration ID")
    temperature = dict(_req(observation, "temperature", oid))
    measured = _num(temperature.get("measured_K"), "measured temperature")
    sigma = _num(temperature.get("sigma_K"), "temperature sigma", positive=True)
    temp_ok = abs(measured - float(block["target_temperature_K"])) <= float(
        block["maximum_absolute_deviation_K"]
    ) and sigma <= float(block["maximum_temperature_sigma_K"])
    extraction = dict(_req(observation, "extraction", oid))
    _num(extraction.get("edge_eV"), "edge")
    _num(extraction.get("sigma_edge_eV"), "edge sigma", positive=True)
    for field in ("method_id", "software_commit", "covariance_uri", "analysis_record_uri"):
        _text(extraction.get(field), field)
    return sid, modality, area, order, temp_ok, count >= 2


def audit(payload: Mapping[str, Any], *, mode: str | None = None) -> dict[str, Any]:
    if str(_req(payload, "schema_version", "package")) != SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if str(_req(payload, "protocol_id", "package")) != PROTOCOL_ID:
        raise ValueError("unsupported protocol_id")
    status = str(_req(payload, "status", "package"))
    audit_mode = mode or ("planning" if status == "planning_template" else "completed")
    completed = audit_mode == "completed"
    if audit_mode not in ("planning", "completed") or status != (
        "completed_package" if completed else "planning_template"
    ):
        raise ValueError("package status and audit mode disagree")
    collaboration = dict(_req(payload, "collaboration", "package"))
    roles = (
        "material_provider", "composition_metrology_lab", "hall_and_defect_lab",
        "absorption_lab", "magneto_optical_lab", "analysis_owner", "data_archive",
    )
    for role in roles:
        value = _req(collaboration, role, "collaboration")
        if completed:
            _text(value, f"collaboration.{role}")
    design = dict(_req(payload, "design", "package"))
    blocks = {str(item["block_id"]): dict(item) for item in design["temperature_blocks"]}
    if len(blocks) != 2:
        raise ValueError("exactly two temperature blocks are required")
    for block_id, block in blocks.items():
        _num(block.get("target_temperature_K"), f"{block_id} target", positive=True)
        _num(block.get("maximum_absolute_deviation_K"), f"{block_id} deviation", positive=True)
        _num(block.get("maximum_temperature_sigma_K"), f"{block_id} sigma", positive=True)
    specimens = _factorial([dict(item) for item in payload["specimens"]])
    for specimen in specimens.values():
        _validate_lineage(specimen, completed=completed)
    x_codes, composition = _composition(specimens, design, completed=completed)
    block_ids = list(blocks)
    if completed:
        states, processing_ok, drift_ok = _completed_states(specimens, block_ids)
        observations = [dict(item) for item in _req(payload, "observations", "package")]
    else:
        states = _planning_states(specimens, payload, block_ids)
        processing_ok = drift_ok = True
        observations = materialize_planning_observations(payload)
    if len(observations) != 32 or len({item["observation_id"] for item in observations}) != 32:
        raise ValueError("package requires exactly 32 unique primary observations")

    all_temp = all_reps = all_polarity = all_separation = all_corr = all_design = True
    per_block: dict[str, Any] = {}
    complete_count = 0
    for block_id, block in blocks.items():
        block_obs = [item for item in observations if item["temperature_block_id"] == block_id]
        if len(block_obs) != 16:
            raise ValueError(f"{block_id} requires exactly 16 observations")
        pairs = {sid: {} for sid in specimens}
        orders = []
        for item in block_obs:
            if completed:
                sid, modality, area, order, temp_ok, reps_ok = _validate_completed_observation(item, block)
                complete_count += 1
                all_temp &= temp_ok
                all_reps &= reps_ok
            else:
                sid, modality, area, order = (
                    str(item["specimen_id"]), str(item["modality"]),
                    str(item["measurement_area_id"]), int(item["measurement_order"]),
                )
            if sid not in pairs or modality in pairs[sid]:
                raise ValueError("unknown specimen or duplicate paired modality")
            pairs[sid][modality] = area
            orders.append(order)
        if sorted(orders) != list(range(1, 17)):
            raise ValueError("measurement order must be a permutation of 1-16")
        if any(set(pair) != set(MODALITIES) for pair in pairs.values()):
            raise ValueError("both modalities are required for every specimen")
        if completed and any(len(set(pair.values())) != 1 for pair in pairs.values()):
            raise ValueError("paired modalities must use one co-registered measurement area")

        polarities = {state[0] for state in states[block_id].values()}
        polarity_ok = len(polarities) == 1
        all_polarity &= polarity_ok
        carrier_values = {
            sid: (int(specimens[sid]["nominal_codes"]["carrier"]), state[1], state[2])
            for sid, state in states[block_id].items()
        }
        vacancy_values = {
            sid: (int(specimens[sid]["nominal_codes"]["vacancy"]), state[3], state[4])
            for sid, state in states[block_id].items()
        }
        carrier_codes, carrier = _group_codes(carrier_values, f"{block_id} carrier")
        vacancy_codes, vacancy = _group_codes(vacancy_values, f"{block_id} vacancy")
        separation_ok = carrier["separation_sigma"] >= float(
            design["minimum_factor_separation_sigma"]
        ) and vacancy["separation_sigma"] >= float(design["minimum_factor_separation_sigma"])
        all_separation &= separation_ok
        ordered = sorted(specimens)
        correlation = float(np.corrcoef(
            [carrier_codes[sid] for sid in ordered], [vacancy_codes[sid] for sid in ordered]
        )[0, 1])
        corr_ok = abs(correlation) <= float(design["carrier_vacancy_max_abs_correlation"])
        all_corr &= corr_ok
        matrix = np.asarray([
            _row(x_codes[item["specimen_id"]], item["modality"],
                 carrier_codes[item["specimen_id"]], vacancy_codes[item["specimen_id"]])
            for item in sorted(block_obs, key=lambda value: int(value["measurement_order"]))
        ])
        diag = _diagnostics(matrix)
        design_ok = bool(
            diag["observation_count"] == 16 and diag["parameter_count"] == 5
            and diag["rank"] == 5 and diag["residual_degrees_of_freedom"] >= 8
            and diag["condition_number"] <= float(design["maximum_condition_number"])
            and diag["maximum_leverage"] <= float(design["maximum_leverage"])
        )
        all_design &= design_ok
        per_block[block_id] = {
            "target_temperature_K": block["target_temperature_K"],
            "specimen_count": 8, "paired_specimen_count": 8,
            "observation_count": 16,
            "carrier_polarity": next(iter(polarities)) if polarity_ok else "mixed",
            "carrier_polarity_pass": polarity_ok,
            "carrier_factor": carrier, "vacancy_factor": vacancy,
            "carrier_vacancy_correlation": correlation,
            "carrier_vacancy_correlation_pass": corr_ok,
            "factor_separation_pass": separation_ok,
            "processing_frozen_pass": processing_ok,
            "state_drift_pass": drift_ok,
            "design_diagnostics": diag, "design_pass": design_ok,
        }

    gates = {
        "composition_hard_maximum": composition["hard_maximum_pass"],
        "all_temperatures": all_temp,
        "technical_replicates": all_reps,
        "processing_frozen": processing_ok,
        "state_drift": drift_ok,
        "single_carrier_polarity": all_polarity,
        "factor_separation": all_separation,
        "carrier_vacancy_correlation": all_corr,
        "design_rank_conditioning_leverage": all_design,
    }
    planning_valid = not completed and all(gates.values())
    completed_valid = completed and complete_count == 32 and all(gates.values())
    return {
        "schema_version": "1.0",
        "analysis": "paired HgCdTe gap-acquisition contract audit",
        "protocol_id": PROTOCOL_ID, "mode": audit_mode, "package_status": status,
        "inventory": {
            "specimen_count": 8, "temperature_block_count": 2,
            "modality_count": 2, "primary_observation_count": 32,
            "completed_observation_count": complete_count,
        },
        "composition": composition,
        "temperature_blocks": per_block,
        "decision": {
            "structural_contract_passed": True,
            "planning_template_valid": planning_valid,
            "completed_package_audit_grade": completed_valid,
            "gates": gates,
            "claim_boundary": (
                "A pass validates the declared local five-parameter acquisition contract. "
                "It does not prove physical completeness, define a universal vacancy "
                "observable, or authorize a universal absorption correction."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--mode", choices=("planning", "completed"))
    parser.add_argument("--output-json")
    args = parser.parse_args()
    path = Path(args.input_json)
    result = audit(json.loads(path.read_text()), mode=args.mode)
    result["input_sha256"] = _sha(path)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text)
    print(text, end="")
    valid = result["decision"][
        "completed_package_audit_grade" if result["mode"] == "completed" else "planning_template_valid"
    ]
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
