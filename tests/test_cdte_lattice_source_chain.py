from tools.analyze_cdte_lattice_source_chain import analyze


def test_cdte_lattice_source_chain_remains_fail_closed():
    result = analyze()
    assert result["status"] == "source_chain_audited_but_execution_gate_remains_closed"
    assert result["williams1969"]["decision_206c"] == "printed_calculated_value_is_a_typographical_error"
    assert 6.474 < result["provisional_zero_k_derivation"]["a0_lower_a"]
    assert result["provisional_zero_k_derivation"]["a0_upper_a"] < 6.480
    assert result["provisional_zero_k_derivation"]["authorization"] == "planning_diagnostic_only"
