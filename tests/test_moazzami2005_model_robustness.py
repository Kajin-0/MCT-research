import math
from pathlib import Path

from tools.audit_moazzami2005_model_robustness import build

ROOT = Path(__file__).resolve().parents[1]


def _by_id(result):
    return {item["specimen_id"]: item for item in result["specimens"]}


def test_model_robustness_audit_is_deterministic_and_separates_estimands() -> None:
    result = build(ROOT)
    assert result["schema_version"] == "1.0"
    assert "not experimental uncertainty" in result["claim_boundary"]
    assert result["methods"]["model_class"].startswith("fitted intercept models only")
    assert len(result["specimens"]) == 2
    for specimen in result["specimens"]:
        candidates = specimen["nominal_candidates"]
        assert len(candidates) == 6
        assert all("threshold" not in item["candidate_id"] for item in candidates)
        assert specimen["decision"]["fixed_absorption_thresholds_excluded_from_model_span"]
        assert specimen["decision"]["adequacy_metrics_are_descriptive_not_probabilistic"]
        assert len(specimen["fit_domain_and_weighting_sensitivity"]) >= 12
        rules = {
            item["weighting_rule"]
            for item in specimen["fit_domain_and_weighting_sensitivity"]
        }
        assert rules == {
            "uniform_points",
            "energy_interval",
            "log_absorption_interval",
        }
        reconstructions = {
            item["reconstruction"] for item in specimen["reconstruction_sensitivity"]
        }
        assert "raw_pixel_centerline" in reconstructions
        assert "inverse_variance_weighted_isotonic" in reconstructions
        assert "isotonic_lower_line_envelope" in reconstructions
        assert "isotonic_upper_line_envelope" in reconstructions
        for value in specimen["maximum_reconstruction_shift_mev_by_candidate"].values():
            assert math.isfinite(value) and value >= 0.0
        for value in specimen["maximum_fit_domain_or_weighting_shift_mev_by_candidate"].values():
            assert math.isfinite(value) and value >= 0.0


def test_vectorized_nominal_grid_reproduces_controlling_edges() -> None:
    result = build(ROOT)
    specimens = _by_id(result)
    expected = {
        "moazzami2005_x0.226": {
            "fractional_power_free": 0.18171125,
            "fractional_power_p_0.5": 0.1875,
            "fractional_power_p_0.7": 0.18618,
            "fractional_power_p_0.872": 0.18369125,
            "fractional_power_p_1": 0.181085625,
            "chu_1994_kane_region": 0.1875,
        },
        "moazzami2005_x0.310": {
            "fractional_power_free": 0.289669625,
            "fractional_power_p_0.5": 0.296347625,
            "fractional_power_p_0.7": 0.295247875,
            "fractional_power_p_0.849": 0.29378375,
            "fractional_power_p_1": 0.291763125,
            "chu_1994_kane_region": 0.2965,
        },
    }
    for specimen_id, candidate_expectations in expected.items():
        actual = {
            item["candidate_id"]: item["edge_ev"]
            for item in specimens[specimen_id]["nominal_candidates"]
        }
        assert actual.keys() == candidate_expectations.keys()
        for candidate_id, expected_edge in candidate_expectations.items():
            assert abs(actual[candidate_id] - expected_edge) <= 1e-12
