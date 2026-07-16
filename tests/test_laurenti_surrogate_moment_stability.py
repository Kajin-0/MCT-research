from __future__ import annotations

from collections import defaultdict

import numpy as np
import pytest

from tools.run_laurenti_surrogate_moment_stability import (
    EVALUATION_COMPOSITIONS,
    laurenti_high_temperature_slope_ev_per_k,
    run_study,
)


def _by_fold_and_x(
    rows: list[dict[str, float | str]],
) -> dict[tuple[str, float], dict[str, float | str]]:
    return {
        (str(row["fold"]), float(row["x"])): row
        for row in rows
    }


def test_laurenti_high_temperature_slope_formula() -> None:
    temperature_k = 1.0e8
    for x in EVALUATION_COMPOSITIONS:
        amplitude = 6.3 - 15.47 * x + 5.92 * x**2
        scale = 11.0 + 67.7 * x

        # Exact derivative of c*A*T^2/(T+B), evaluated at a temperature
        # far above B. This avoids subtracting nearly equal large values.
        finite_temperature_derivative = (
            1.0e-4
            * amplitude
            * temperature_k
            * (temperature_k + 2.0 * scale)
            / (temperature_k + scale) ** 2
        )
        assert laurenti_high_temperature_slope_ev_per_k(float(x)) == pytest.approx(
            finite_temperature_derivative, rel=0.0, abs=5.0e-13
        )


def test_leading_moment_is_stable_before_discrete_scales() -> None:
    rows = run_study()
    assert len(rows) == 15
    lookup = _by_fold_and_x(rows)

    expected_scales = {
        "low_T_le_40K": (15.0, 320.0),
        "mid_40K_to_200K": (15.0, 160.0),
        "high_T_gt_200K": (20.0, 160.0),
    }
    for fold, scales in expected_scales.items():
        for x in EVALUATION_COMPOSITIONS:
            row = lookup[(fold, float(x))]
            assert (float(row["theta_1_k"]), float(row["theta_2_k"])) == scales

    slopes_by_x: dict[float, list[float]] = defaultdict(list)
    errors_by_x: dict[float, list[float]] = defaultdict(list)
    higher_moment_by_x: dict[float, list[float]] = defaultdict(list)
    for row in rows:
        x = float(row["x"])
        slopes_by_x[x].append(float(row["high_temperature_slope_mev_per_k"]))
        errors_by_x[x].append(float(row["slope_error_mev_per_k"]))
        higher_moment_by_x[x].append(
            float(row["inverse_temperature_coefficient_mev_k"])
        )

    # The leading slope moment remains stable even though the high scale changes
    # from 320 K to 160 K across folds.
    assert np.ptp(slopes_by_x[0.0]) < 0.003
    assert max(abs(value) for value in errors_by_x[0.2]) < 0.0013

    # With the high-temperature range itself held out, the CdTe endpoint slope is
    # less stable but still remains within a declared few-hundredths meV/K screen.
    assert max(abs(value) for value in errors_by_x[1.0]) < 0.023

    # The next moment is not identified at the same level: its magnitude changes
    # by more than a factor of two at the CdTe endpoint.
    magnitudes = np.abs(higher_moment_by_x[1.0])
    assert float(np.max(magnitudes) / np.min(magnitudes)) > 2.0


def test_moment_identity_matches_fitted_amplitudes() -> None:
    rows = run_study()
    for row in rows:
        theta = np.array(
            [float(row["theta_1_k"]), float(row["theta_2_k"])],
            dtype=float,
        )
        amplitude = np.array(
            [float(row["amplitude_1_ev"]), float(row["amplitude_2_ev"])],
            dtype=float,
        )
        expected_slope_mev_per_k = 2000.0 * float(np.sum(amplitude / theta))
        assert float(row["high_temperature_slope_mev_per_k"]) == pytest.approx(
            expected_slope_mev_per_k, rel=0.0, abs=1.0e-12
        )

        expected_inverse_temperature = (
            1000.0 * float(np.sum(amplitude * theta)) / 6.0
        )
        assert float(row["inverse_temperature_coefficient_mev_k"]) == pytest.approx(
            expected_inverse_temperature, rel=0.0, abs=1.0e-10
        )
