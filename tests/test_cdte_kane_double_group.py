from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest


def _load_tool() -> ModuleType:
    path = Path(__file__).parents[1] / "tools" / "validate_cdte_kane_double_group.py"
    specification = importlib.util.spec_from_file_location(
        "validate_cdte_kane_double_group", path
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _random_unitary(dimension: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    matrix = rng.normal(size=(dimension, dimension)) + 1.0j * rng.normal(
        size=(dimension, dimension)
    )
    q, r = np.linalg.qr(matrix)
    phase = np.diag(r)
    return q * (phase / np.abs(phase)).conj()


def _serialize(matrix: np.ndarray) -> list[list[list[float]]]:
    return [
        [[float(value.real), float(value.imag)] for value in row]
        for row in np.asarray(matrix, dtype=complex)
    ]


def _same_rotation(first: np.ndarray, second: np.ndarray) -> bool:
    return bool(np.linalg.norm(first - second) < 1.0e-10)


def _synthetic_probe(tool: ModuleType) -> tuple[dict[str, object], dict[str, object]]:
    elements = tool.generate_td_double_group()
    spatial_groups: list[list[object]] = []
    for element in elements:
        for group in spatial_groups:
            if _same_rotation(element["rotation"], group[0]["rotation"]):
                group.append(element)
                break
        else:
            spatial_groups.append([element])
    section = [
        min(group, key=lambda item: (len(item["word"]), item["word"]))
        for group in spatial_groups
    ]

    c3 = next(element for element in section if element["word"] == "C")
    s4 = next(element for element in section if element["word"] == "S")
    identity = next(element for element in section if element["word"] == "")
    ordered = [identity, c3, s4] + [
        element for element in section if element not in (identity, c3, s4)
    ]

    gauges = {
        "Gamma7": _random_unitary(2, 201),
        "Gamma8": _random_unitary(4, 202),
        "Gamma6": _random_unitary(2, 203),
    }
    time_reversal = dict(zip(tool.LABELS, tool.time_reversal_blocks(), strict=True))
    block_order = ("Gamma7", "Gamma8", "Gamma6")
    operations: list[dict[str, object]] = []
    unused_unitary = iter(
        index for index in range(3, 100, 2) if index not in (23, 41)
    )
    unused_antiunitary = iter(index for index in range(4, 102, 2))

    for element in ordered:
        if element is identity:
            unitary_index = 1
            antiunitary_index = 2
        elif element is c3:
            unitary_index = 41
            antiunitary_index = next(unused_antiunitary)
        elif element is s4:
            unitary_index = 23
            antiunitary_index = next(unused_antiunitary)
        else:
            unitary_index = next(unused_unitary)
            antiunitary_index = next(unused_antiunitary)

        unitary_blocks = []
        antiunitary_blocks = []
        for label in block_order:
            gauge = gauges[label]
            unitary_blocks.append(
                _serialize(gauge.conj().T @ element["blocks"][label] @ gauge)
            )
            antiunitary_blocks.append(
                _serialize(
                    gauge.conj().T
                    @ (element["blocks"][label] @ time_reversal[label])
                    @ gauge.conj()
                )
            )
        common = {
            "rotation_cartesian": element["rotation"].tolist(),
            "spinor_rotation": _serialize(element["blocks"]["Gamma6"]),
            "matrix_status": "available",
        }
        operations.append(
            {
                **common,
                "index": unitary_index,
                "time_reversal": False,
                "unitary_blocks": unitary_blocks,
            }
        )
        operations.append(
            {
                **common,
                "index": antiunitary_index,
                "time_reversal": True,
                "unitary_blocks": antiunitary_blocks,
            }
        )

    probe: dict[str, object] = {
        "data_file_schema_sha256": "synthetic",
        "space_group_name": "F-43m1'",
        "space_group_number": "216.75",
        "selected_global_bands_one_based": list(range(31, 39)),
        "unitary_operation_count": 24,
        "antiunitary_operation_count": 24,
        "operations": operations,
    }
    contract: dict[str, object] = {
        "stage": "cdte_kane_double_group_gate",
        "generators": [
            {"name": "C3_[111]", "operation_index": 41},
            {"name": "S4_z", "operation_index": 23},
        ],
        "pure_time_reversal_operation_index": 2,
        "energy_blocks": [
            {"irrep": "Gamma7", "bands_one_based": [31, 32], "probe_block_index": 0},
            {
                "irrep": "Gamma8",
                "bands_one_based": [33, 34, 35, 36],
                "probe_block_index": 1,
            },
            {"irrep": "Gamma6", "bands_one_based": [37, 38], "probe_block_index": 2},
        ],
        "thresholds": {
            "operation_rotation_frobenius": 1.0e-8,
            "operation_spinor_frobenius": 1.0e-8,
            "intertwiner_null_singular_value": 1.0e-8,
            "next_singular_value_minimum": 0.5,
            "all_operation_matrix_frobenius": 1.0e-8,
        },
        "authorization": {},
        "claim_boundary": "synthetic test",
    }
    return probe, contract


def test_generators_produce_complete_td_double_group() -> None:
    tool = _load_tool()
    elements = tool.generate_td_double_group()
    assert len(elements) == 48

    spatial_groups: list[list[object]] = []
    for element in elements:
        for group in spatial_groups:
            if _same_rotation(element["rotation"], group[0]["rotation"]):
                group.append(element)
                break
        else:
            spatial_groups.append([element])
    assert len(spatial_groups) == 24
    assert all(len(group) == 2 for group in spatial_groups)
    assert all(
        np.linalg.norm(group[0]["blocks"]["Gamma6"] + group[1]["blocks"]["Gamma6"])
        < 1.0e-12
        for group in spatial_groups
    )


def test_full_unitary_and_antiunitary_canonical_recovery() -> None:
    tool = _load_tool()
    probe, contract = _synthetic_probe(tool)
    result = tool.validate(probe, contract)

    assert result["double_group_element_count"] == 48
    assert result["unitary_operation_count"] == 24
    assert result["antiunitary_operation_count"] == 24
    assert result["maximum_canonical_matrix_residual"] < 1.0e-12
    for irrep in result["irreps"].values():
        assert irrep["generator_intertwiner_nullity"] == 1
        assert irrep["generator_next_singular_value"] > 0.99
        assert irrep["maximum_unitary_residual"] < 1.0e-12
        assert irrep["maximum_antiunitary_residual"] < 1.0e-12


def test_inconsistent_single_operation_sign_fails_closed() -> None:
    tool = _load_tool()
    probe, contract = _synthetic_probe(tool)
    operation = next(
        item
        for item in probe["operations"]
        if not item["time_reversal"] and item["index"] not in (1, 23, 41)
    )
    matrix = tool._complex(operation["unitary_blocks"][1])
    operation["unitary_blocks"][1] = _serialize(-matrix)

    with pytest.raises(RuntimeError, match="residual"):
        tool.validate(probe, contract)
