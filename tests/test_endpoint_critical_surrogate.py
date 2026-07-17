import pytest

from tools.analyze_endpoint_critical_surrogate import analyze


def test_endpoint_critical_surrogate_is_rejected():
    result = analyze()
    assert result["critical_composition"] == pytest.approx(0.5047258866)
    assert result["surface_equivalence_to_laurenti"]["maximum_absolute_difference_mev"] < 2.1
    cd_rich = result["direct_cd_rich_marker_scores"]
    assert cd_rich["endpoint_critical_surrogate"]["rmse_mev"] > cd_rich["laurenti_equation7"]["rmse_mev"]
    seiler = result["seiler_profiled_offset_shape_scores"]
    assert seiler["endpoint_critical_surrogate"]["rmse_mev"] > seiler["hansen_linear"]["rmse_mev"]
    assert "Reject the surrogate" in result["decision"]
