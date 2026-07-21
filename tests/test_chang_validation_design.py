from __future__ import annotations

import math

import pytest

from mct_research.chang_validation_design import (
    cutoff_difference_variance_ev2,
    estimate_tail_width_from_cutoff_pair,
    log_thickness_ratio_variance,
    maximum_source_valid_thickness_ratio,
    required_equal_cutoff_sigma_ev,
)

E1_EV = 0.0996292713225439
E2_EV = 0.0829937389891052
W_EV = 0.012


def test_pair_recovers_declared_tail_width_exactly() -> None:
    result = estimate_tail_width_from_cutoff_pair(
        E1_EV,
        E2_EV,
        5.0,
        20.0,
    )
    assert result.width_ev == pytest.approx(W_EV, abs=2.0e-15)
    assert result.cutoff_difference_ev == pytest.approx(
        -0.01663553233343869,
        abs=2.0e-15,
    )
    assert result.log_thickness_ratio == pytest.approx(math.log(4.0))
    assert result.standard_uncertainty_ev == 0.0


def test_correlated_cutoff_uncertainty_propagation() -> None:
    independent = estimate_tail_width_from_cutoff_pair(
        E1_EV,
        E2_EV,
        5.0,
        20.0,
        cutoff_sigma_1_ev=0.001,
        cutoff_sigma_2_ev=0.001,
    )
    correlated = estimate_tail_width_from_cutoff_pair(
        E1_EV,
        E2_EV,
        5.0,
        20.0,
        cutoff_sigma_1_ev=0.001,
        cutoff_sigma_2_ev=0.001,
        cutoff_correlation=0.8,
    )
    assert independent.standard_uncertainty_ev == pytest.approx(
        0.0010201394465967897
    )
    assert independent.relative_standard_uncertainty == pytest.approx(
        0.08501162054973248
    )
    assert correlated.standard_uncertainty_ev == pytest.approx(
        0.0004562202298238875
    )
    assert correlated.relative_standard_uncertainty == pytest.approx(
        0.03801835248532395
    )


def test_effective_thickness_uncertainty_is_retained() -> None:
    result = estimate_tail_width_from_cutoff_pair(
        E1_EV,
        E2_EV,
        5.0,
        20.0,
        cutoff_sigma_1_ev=0.001,
        cutoff_sigma_2_ev=0.001,
        thickness_sigma_1=0.1,
        thickness_sigma_2=0.4,
    )
    assert result.log_thickness_ratio_variance == pytest.approx(0.0008)
    assert result.standard_uncertainty_ev == pytest.approx(
        0.0010491081532214709
    )
    assert result.relative_standard_uncertainty == pytest.approx(
        0.08742567943512257
    )


def test_source_domain_maximum_ratio_and_margin() -> None:
    absolute = maximum_source_valid_thickness_ratio(
        E1_EV,
        W_EV,
        0.080,
    )
    two_mev_margin = maximum_source_valid_thickness_ratio(
        E1_EV,
        W_EV,
        0.080,
        energy_margin_ev=0.002,
    )
    three_mev_margin = maximum_source_valid_thickness_ratio(
        E1_EV,
        W_EV,
        0.080,
        energy_margin_ev=0.003,
    )
    assert absolute == pytest.approx(5.133422600006805)
    assert two_mev_margin == pytest.approx(4.34534841704622)
    assert three_mev_margin == pytest.approx(3.9979135407217457)
    assert 4.0 / absolute == pytest.approx(0.7792072291096194)
    assert 4.0 / two_mev_margin == pytest.approx(0.920524573888836)


def test_required_equal_cutoff_precision() -> None:
    assert required_equal_cutoff_sigma_ev(
        W_EV,
        4.0,
        0.05,
    ) == pytest.approx(0.0005881548860811283)
    assert required_equal_cutoff_sigma_ev(
        W_EV,
        4.0,
        0.10,
    ) == pytest.approx(0.0011763097721622566)
    assert required_equal_cutoff_sigma_ev(
        W_EV,
        4.0,
        0.20,
    ) == pytest.approx(0.0023526195443245133)

    assert required_equal_cutoff_sigma_ev(
        W_EV,
        4.0,
        0.05,
        relative_thickness_sigma_1=0.02,
        relative_thickness_sigma_2=0.02,
    ) == pytest.approx(0.0005369601195816175)


def test_covariance_components() -> None:
    assert cutoff_difference_variance_ev2(
        0.001,
        0.001,
        correlation=0.8,
    ) == pytest.approx(4.0e-7)
    assert log_thickness_ratio_variance(
        5.0,
        20.0,
        0.1,
        0.4,
    ) == pytest.approx(0.0008)
    assert log_thickness_ratio_variance(
        5.0,
        20.0,
        0.1,
        0.4,
        correlation=1.0,
    ) == pytest.approx(0.0)


def test_validation_design_rejects_inconsistent_inputs() -> None:
    with pytest.raises(ValueError, match="non-unit ratio"):
        estimate_tail_width_from_cutoff_pair(0.1, 0.09, 5.0, 5.0)
    with pytest.raises(ValueError, match="positive exponential-tail width"):
        estimate_tail_width_from_cutoff_pair(0.1, 0.11, 5.0, 20.0)
    with pytest.raises(ValueError, match="between -1 and 1"):
        cutoff_difference_variance_ev2(0.001, 0.001, correlation=1.1)
    with pytest.raises(ValueError, match="above the minimum"):
        maximum_source_valid_thickness_ratio(0.081, 0.012, 0.080, energy_margin_ev=0.002)
    with pytest.raises(ValueError, match="thickness uncertainty alone"):
        required_equal_cutoff_sigma_ev(
            0.012,
            1.1,
            0.05,
            relative_thickness_sigma_1=0.02,
            relative_thickness_sigma_2=0.02,
        )
