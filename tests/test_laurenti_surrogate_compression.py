from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def _load_tool(name: str) -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "tools" / f"{name}.py"
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_two_scales_reduce_surrogate_error_but_worsen_conditioning() -> None:
    study = _load_tool("run_laurenti_surrogate_compression").run_study()
    models = study["models"]
    one = models["one_fixed_scale_oscillator"]
    two = models["two_fixed_scale_oscillators"]

    one_loco = one["leave_one_composition_out"]
    two_loco = two["leave_one_composition_out"]
    one_temperature = one["held_out_temperature_ranges"]
    two_temperature = two["held_out_temperature_ranges"]

    assert one_loco["aggregate_metrics"]["rmse_mev"] > 1.5
    assert two_loco["aggregate_metrics"]["rmse_mev"] < 0.9
    assert two_loco["aggregate_metrics"]["max_abs_mev"] < 3.2
    assert one_temperature["aggregate_metrics"]["rmse_mev"] > 4.5
    assert one_temperature["aggregate_metrics"]["max_abs_mev"] > 26.0
    assert two_temperature["aggregate_metrics"]["rmse_mev"] < 1.4
    assert two_temperature["aggregate_metrics"]["max_abs_mev"] < 6.0
    assert two_temperature["max_training_condition_number"] > 10.0 * one_temperature["max_training_condition_number"]
    assert one_loco["selection_counts"]["40"] == 20
    assert two_loco["selection_counts"]["20+240"] == 18


def test_real_specimens_reject_two_identified_scales() -> None:
    result = _load_tool("analyze_real_oscillator_gate").analyze()
    seiler = result["classes"]["Seiler"]
    laurenti = result["classes"]["Laurenti"]

    assert seiler["two_scales"]["all_data_rmse_mev"] < seiler["one_scale"]["all_data_rmse_mev"]
    assert seiler["two_scales"]["specimen_holdout"]["aggregate"]["rmse_mev"] > seiler["one_scale"]["specimen_holdout"]["aggregate"]["rmse_mev"]
    assert seiler["two_scales"]["temperature_holdout"]["aggregate"]["rmse_mev"] > 1000.0
    assert laurenti["two_scales"]["temperature_holdout"]["aggregate"]["rmse_mev"] > laurenti["one_scale"]["temperature_holdout"]["aggregate"]["rmse_mev"]
    assert result["laurenti_specimen_holdout_improvement_mev"] < 0.1
    assert result["source_classes_pooled"] is False
