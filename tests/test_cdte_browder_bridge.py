from tools.analyze_cdte_browder_bridge import analyze


def test_browder_bridge_remains_morphology_limited():
    result = analyze()
    assert result["status"] == "morphology_limited_bridge_sensitivity_only"
    sensitivity = result["zero_k_sensitivity"]
    assert 6.475 < sensitivity["endpoint_adjusted_browder_shape_a0_a"] < 6.477
    assert sensitivity["adjusted_shape_minus_linear_bridge_a"] < -0.0008
    overlap = result["overlap_with_smith_white_single_crystal"]
    assert overlap["maximum_absolute_difference_1e6_per_k"] > 0.8
    assert "Keep ready_for_execution false" in result["decision"]
