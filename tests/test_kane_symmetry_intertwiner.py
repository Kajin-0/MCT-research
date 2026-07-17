from tools.analyze_kane_symmetry_intertwiner import analyze


def test_double_group_intertwiner_recovers_canonical_blocks():
    result = analyze()
    assert result["maximum_recovery_error"] < 1.0e-12
    assert result["maximum_symmetry_residual"] < 1.0e-12
    assert result["maximum_time_reversal_residual"] < 1.0e-12
    for block in result["irreps"].values():
        assert block["nullity_C3_only"] > 1
        assert block["nullity_C3_and_S4"] == 1
        assert block["next_singular_value_above_nullspace"] > 0.9
        assert block["character_error_after_random_gauge"] < 1.0e-12
