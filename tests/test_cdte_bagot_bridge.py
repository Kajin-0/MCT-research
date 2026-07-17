import json
from pathlib import Path

import numpy as np

from tools.analyze_cdte_bagot_bridge import alpha_bagot_fit, analyze


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/cdte_lattice/bogucki2022_bagot_cdte_expansion_fit.json"


def test_bagot_formula_has_expected_cdte_shape():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    temperatures = np.asarray([4.0, 10.0, 30.0, 85.0, 200.0, 293.15])
    alpha = alpha_bagot_fit(temperatures, payload["coefficients"])

    assert alpha[0] < 0.0
    assert alpha[2] < alpha[1]
    assert alpha[3] > 0.0
    assert alpha[-1] > alpha[-2] > 0.0
    np.testing.assert_allclose(alpha[2] * 1.0e6, -3.0080, atol=5.0e-4)
    np.testing.assert_allclose(alpha[-1] * 1.0e6, 4.5865, atol=5.0e-4)


def test_secondary_bagot_bridge_is_informative_but_not_executable():
    result = analyze(SOURCE)

    assert result["status"] == (
        "secondary_bagot_bridge_diagnostic_not_execution_authorized"
    )
    assert 6.4762 < result["zero_temperature_diagnostic"]["a0_angstrom"] < 6.4767
    assert result["smith_white_direct_overlap"][
        "rms_alpha_difference_1e6_per_k"
    ] < 0.3
    assert result["two_model_planning_envelope"][
        "fraction_of_half_percent_volume_bracket"
    ] < 0.2
    assert result["decision"]["bridge_plausibility_supported"]
    assert not result["decision"]["execution_bridge_authorized"]
    assert result["underlying_primary_source"]["source_bytes_sha256"] is None
