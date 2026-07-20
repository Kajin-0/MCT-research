from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/evidence/guldner_weiler_1977_magneto_core.json"
TOOL_PATH = ROOT / "tools/audit_guldner_weiler_1977_magneto_core.py"

spec = importlib.util.spec_from_file_location("guldner_weiler_audit", TOOL_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _payload() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_audit_passes_and_counts_sources() -> None:
    result = module.audit(DATA_PATH)
    assert result["primary_source_count"] == 3
    assert result["independent_laboratory_lineage_count"] == 2
    assert result["guldner_exact_anchor_count"] == 7


def test_exact_guldner_anchor_inventory() -> None:
    payload = _payload()
    observed = [
        (row["composition_x"], row["interaction_gap_meV"])
        for row in payload["guldner"]["exact_primary_anchors"]
    ]
    assert observed == module.EXPECTED_ANCHORS


def test_weiler_uncertainty_scales_are_exact() -> None:
    assert module.composition_energy_scale_meV(24.0, 0.005) == pytest.approx(9.28)
    assert module.composition_energy_scale_meV(24.0, 0.006) == pytest.approx(11.136)
    assert module.composition_energy_scale_meV(24.0, 0.015) == pytest.approx(27.84)
    assert module.composition_energy_scale_meV(91.0, 0.005) == pytest.approx(8.945)
    assert module.composition_energy_scale_meV(91.0, 0.006) == pytest.approx(10.734)
    assert module.composition_energy_scale_meV(91.0, 0.015) == pytest.approx(26.835)


def test_composition_uncertainty_dominates_fit_precision() -> None:
    result = module.audit(DATA_PATH)
    assert result["minimum_composition_energy_scale_meV"] > 3.0
    assert result["minimum_ratio_to_gap_fit_sigma"] > 2.9
    assert result["maximum_ratio_to_gap_fit_sigma"] > 9.0


def test_guldner_figure_series_is_fail_closed(tmp_path: Path) -> None:
    payload = _payload()
    payload["guldner"]["full_figure_11_series"]["numeric_ingestion_authorized"] = True
    with pytest.raises(ValueError, match="Figure 11"):
        module.audit(_write(tmp_path, payload))


def test_weiler_figure_points_are_fail_closed(tmp_path: Path) -> None:
    payload = _payload()
    payload["weiler"]["per_specimen_gap_series"]["numeric_ingestion_authorized"] = True
    with pytest.raises(ValueError, match="per-specimen"):
        module.audit(_write(tmp_path, payload))


def test_unreported_guldner_sigma_cannot_be_invented(tmp_path: Path) -> None:
    payload = _payload()
    payload["guldner"]["specimen_level_composition_uncertainty_reported"] = True
    with pytest.raises(ValueError, match="sigma_x"):
        module.audit(_write(tmp_path, payload))


def test_transmission_composition_cannot_become_independent(tmp_path: Path) -> None:
    payload = _payload()
    payload["weiler"]["composition_provenance"]["room_temperature_transmission_cut_on"][
        "independent_material_gap_validation"
    ] = True
    with pytest.raises(ValueError, match="independent gap validation"):
        module.audit(_write(tmp_path, payload))


def test_cross_lab_ranking_cannot_be_authorized(tmp_path: Path) -> None:
    payload = _payload()
    payload["decision"]["few_meV_quantitative_cross_lab_ranking_authorized"] = True
    with pytest.raises(ValueError, match="decision"):
        module.audit(_write(tmp_path, payload))


def test_domain_rejects_unreported_temperature_and_sigma() -> None:
    with pytest.raises(ValueError, match="24 K and 91 K"):
        module.weiler_dEg_dx_eV_per_x(50.0)
    with pytest.raises(ValueError, match="source-declared"):
        module.composition_energy_scale_meV(24.0, 0.010)
