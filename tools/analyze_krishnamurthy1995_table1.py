#!/usr/bin/env python3
"""Reproduce Krishnamurthy 1995 Table I and close it against Table II."""

from __future__ import annotations

import argparse
import csv
import json
import math
from decimal import Decimal
from pathlib import Path
from typing import Any

BANDS = tuple(f"band_{i}_mev" for i in range(1, 9))
MODES = ("TA", "LA", "LO", "TO")
EDGES = ("valence", "conduction")


def _load_table1(path: str | Path) -> dict[tuple[str, str], tuple[Decimal, ...]]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if len(rows) != 10:
        raise ValueError("Table I must contain 10 rows")
    data: dict[tuple[str, str], tuple[Decimal, ...]] = {}
    for row in rows:
        if row["temperature_k"] != "300" or row["composition_x"] != "0.22":
            raise ValueError("Table I must describe x=0.22 at 300 K")
        key = (row["channel"], row["edge"])
        if key in data:
            raise ValueError(f"duplicate row {key}")
        data[key] = tuple(Decimal(row[name]) for name in BANDS)
    expected = {(c, e) for c in ("total", *MODES) for e in EDGES}
    if set(data) != expected:
        raise ValueError("Table I channel/edge rows are incomplete")
    return data


def _load_table2(path: str | Path) -> tuple[Decimal, Decimal, Decimal]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    by_t = {Decimal(row["temperature_k"]): row for row in rows}
    zero_points = {Decimal(row["zero_point_gap_correction_mev"]) for row in rows}
    if Decimal("1") not in by_t or Decimal("300") not in by_t or len(zero_points) != 1:
        raise ValueError("Table II anchors are incomplete")
    return (
        Decimal(by_t[Decimal("1")]["gap_mev"]),
        Decimal(by_t[Decimal("300")]["gap_mev"]),
        zero_points.pop(),
    )


def _edge_sums(
    data: dict[tuple[str, str], tuple[Decimal, ...]], channel: str
) -> dict[str, Decimal]:
    valence = sum(data[(channel, "valence")], Decimal("0"))
    conduction = sum(data[(channel, "conduction")], Decimal("0"))
    return {"valence": valence, "conduction": conduction, "gap": conduction - valence}


def _combine(
    sums: dict[str, dict[str, Decimal]], channels: tuple[str, ...]
) -> dict[str, Decimal]:
    return {
        key: sum((sums[channel][key] for channel in channels), Decimal("0"))
        for key in ("valence", "conduction", "gap")
    }


def _floats(values: dict[str, Decimal]) -> dict[str, float]:
    return {f"{key}_mev": float(value) for key, value in values.items()}


def analyze_tables(table1_path: str | Path, table2_path: str | Path) -> dict[str, Any]:
    data = _load_table1(table1_path)
    gap_1k, gap_300k, zero_point = _load_table2(table2_path)
    sums = {channel: _edge_sums(data, channel) for channel in ("total", *MODES)}
    total = sums["total"]
    acoustic = _combine(sums, ("TA", "LA"))
    optical = _combine(sums, ("LO", "TO"))
    mode_total = _combine(sums, MODES)

    valence_intermediate = {
        edge: sum(data[("total", edge)][:4], Decimal("0")) for edge in EDGES
    }
    valence_intermediate["gap"] = (
        valence_intermediate["conduction"] - valence_intermediate["valence"]
    )
    conduction_intermediate = {
        edge: sum(data[("total", edge)][4:], Decimal("0")) for edge in EDGES
    }
    conduction_intermediate["gap"] = (
        conduction_intermediate["conduction"] - conduction_intermediate["valence"]
    )

    edge_magnitude = abs(total["valence"]) + abs(total["conduction"])
    acoustic_magnitude = abs(acoustic["valence"]) + abs(acoustic["conduction"])
    cancellation_index = (
        abs(valence_intermediate["gap"]) + abs(conduction_intermediate["gap"])
    ) / abs(total["gap"])

    reference_gap = gap_1k - zero_point
    fixed_lattice_gap_300k = reference_gap + total["gap"]
    inferred_non_ep = gap_300k - fixed_lattice_gap_300k
    thermal_ep = total["gap"] - zero_point
    table2_shift = gap_300k - gap_1k

    cell_half_step = Decimal("0.005")
    table1_gap_bound = Decimal("16") * cell_half_step
    non_ep_worst_bound = (
        Decimal("0.005") + Decimal("0.005") + Decimal("0.05") + table1_gap_bound
    )
    non_ep_rss_bound = math.sqrt(
        2 * 0.005**2 + 0.05**2 + float(table1_gap_bound) ** 2
    )

    band_gap = [
        data[("total", "conduction")][i] - data[("total", "valence")][i]
        for i in range(8)
    ]

    return {
        "source_kind": "historical_calculated_data_not_experiment",
        "table1": {
            "total": _floats(total),
            "mode_sums": {mode: _floats(sums[mode]) for mode in MODES},
            "mode_sum_minus_total": {
                f"{key}_mev": float(mode_total[key] - total[key])
                for key in ("valence", "conduction", "gap")
            },
        },
        "phonon_channels": {
            "acoustic": _floats(acoustic),
            "optical": _floats(optical),
            "acoustic_combined_edge_magnitude_fraction": float(
                acoustic_magnitude / edge_magnitude
            ),
            "acoustic_valence_magnitude_fraction": float(
                abs(acoustic["valence"]) / abs(total["valence"])
            ),
            "acoustic_conduction_magnitude_fraction": float(
                abs(acoustic["conduction"]) / abs(total["conduction"])
            ),
            "acoustic_gap_fraction_of_net": float(acoustic["gap"] / total["gap"]),
            "TA_gap_fraction_of_net": float(sums["TA"]["gap"] / total["gap"]),
        },
        "intermediate_bands": {
            "valence_bands_1_to_4": _floats(valence_intermediate),
            "conduction_bands_5_to_8": _floats(conduction_intermediate),
            "gap_cancellation_index": float(cancellation_index),
            "individual_gap_contributions_mev": [float(value) for value in band_gap],
        },
        "table1_table2_closure": {
            "gap_1k_mev": float(gap_1k),
            "zero_point_mev": float(zero_point),
            "unrenormalized_reference_gap_mev": float(reference_gap),
            "electron_phonon_gap_shift_300k_mev": float(total["gap"]),
            "fixed_lattice_gap_300k_mev": float(fixed_lattice_gap_300k),
            "gap_300k_mev": float(gap_300k),
            "inferred_non_electron_phonon_300k_mev": float(inferred_non_ep),
            "thermal_electron_phonon_beyond_zero_point_mev": float(thermal_ep),
            "table2_1_to_300k_shift_mev": float(table2_shift),
            "reconstructed_1_to_300k_shift_mev": float(thermal_ep + inferred_non_ep),
            "closure_residual_mev": float(thermal_ep + inferred_non_ep - table2_shift),
            "inferred_non_ep_fraction_of_thermal_ep": float(abs(inferred_non_ep) / thermal_ep),
        },
        "rounding_bounds": {
            "table1_gap_worst_case_mev": float(table1_gap_bound),
            "inferred_non_ep_worst_case_mev": float(non_ep_worst_bound),
            "inferred_non_ep_rss_mev": non_ep_rss_bound,
        },
        "decision": {
            "result": "300 K gap increase is acoustic dominated and cancellation sensitive",
            "dilation_interpretation": (
                "the -7.90 meV non-electron-phonon remainder is consistent with the "
                "paper's separately described lattice-dilation term"
            ),
            "new_oscillator_family_supported": False,
            "low_temperature_turnover_resolved": False,
            "reason": "Table I contains only one temperature and cannot identify spectral scales",
            "experimental_validation": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--table1", default="data/theory/krishnamurthy1995_hg078cd022_table1.csv"
    )
    parser.add_argument(
        "--table2", default="data/theory/krishnamurthy1995_hg078cd022_table2.csv"
    )
    parser.add_argument("--output")
    args = parser.parse_args()
    summary = analyze_tables(args.table1, args.table2)
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
