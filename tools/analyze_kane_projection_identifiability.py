#!/usr/bin/env python3
"""Rank certificate for finite-temperature 8-band Kane parameter extraction."""

from __future__ import annotations

import json
import math

import numpy as np

PARAMETERS = ("Eg", "Delta", "P8", "P7", "F", "gamma1", "gamma2", "gamma3")

ROWS = {
    "Eg": (1, 0, 0, 0, 0, 0, 0, 0),
    "Delta": (0, 1, 0, 0, 0, 0, 0, 0),
    "P8": (0, 0, 1, 0, 0, 0, 0, 0),
    "P7": (0, 0, 0, 1, 0, 0, 0, 0),
    "c6_over_C_minus_1": (0, 0, 0, 0, 2, 0, 0, 0),
    "cHH_001_over_C": (0, 0, 0, 0, 0, -1, 2, 0),
    "cLH_001_over_C": (0, 0, 0, 0, 0, -1, -2, 0),
    "cHH_111_over_C": (0, 0, 0, 0, 0, -1, 0, 2),
    "cLH_111_over_C": (0, 0, 0, 0, 0, -1, 0, -2),
}

STAGES = {
    "gamma_only": ("Eg", "Delta"),
    "gamma_plus_linear": ("Eg", "Delta", "P8", "P7"),
    "plus_001_quadratic": (
        "Eg", "Delta", "P8", "P7", "c6_over_C_minus_1",
        "cHH_001_over_C", "cLH_001_over_C",
    ),
    "plus_111_quadratic": tuple(ROWS),
}

EXPECTED_RANKS = (2, 4, 7, 8)


def stage_result(row_names: tuple[str, ...]) -> dict[str, object]:
    matrix = np.asarray([ROWS[name] for name in row_names], dtype=float)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    rank = int(np.linalg.matrix_rank(matrix))
    return {
        "rows": list(row_names),
        "rank": rank,
        "null_dimension": len(PARAMETERS) - rank,
        "singular_values": singular_values.tolist(),
    }


def residue_example(z6: float = 0.8, z8: float = 0.9, z7: float = 0.7,
                    p: float = 8.0) -> dict[str, float]:
    p8 = math.sqrt(z6 * z8) * p
    p7 = math.sqrt(z6 * z7) * p
    eta = 2.0 * abs(p8 - p7) / (abs(p8) + abs(p7))
    return {"Z6": z6, "Z8": z8, "Z7": z7, "P": p,
            "P8_QP": p8, "P7_QP": p7, "eta_P": eta}


def analyze() -> dict[str, object]:
    stages = {name: stage_result(rows) for name, rows in STAGES.items()}
    ranks = tuple(int(stage["rank"]) for stage in stages.values())
    if ranks != EXPECTED_RANKS:
        raise RuntimeError(f"unexpected identifiability ranks: {ranks}")
    residue = residue_example()
    if not math.isclose(residue["eta_P"], 0.12549213361245665,
                        rel_tol=0.0, abs_tol=1.0e-14):
        raise RuntimeError("residue example changed")
    return {
        "parameters": list(PARAMETERS),
        "stages": stages,
        "minimal_training_directions": ["[001]", "[111]"],
        "recommended_holdout_direction": "[110]",
        "zone_center_decision": "only_Eg_and_Delta_identifiable",
        "full_rank_decision": "finite_k_linear_and_two_inequivalent_quadratic_directions_required",
        "residue_induced_one_P_failure": residue,
        "claim_boundary": (
            "A Gamma-only self-energy cannot determine P8, P7, F, or gamma1-3. "
            "A differentiating result requires fixed-basis finite-k matrix data "
            "and a held-out closure test."
        ),
    }


def main() -> int:
    print(json.dumps(analyze(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
