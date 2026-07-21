"""Detector-level cutoff operators for HgCdTe absorption models.

The functions in this module connect a declared absorption coefficient to a
single-pass Beer-Lambert response and then to a response-defined cutoff energy.
The Chang 2006 wrapper is source-bounded and synthetic-analysis oriented. It is
not a production detector model: reflection, interference, collection
efficiency, carrier transport, and multiple passes are excluded.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import exp, isfinite, log

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .chang_2006_absorption import (
    CHANG_2006_RELATIVE_ENERGY_RANGE_EV,
    chang_2006_absorption_shape,
    chang_2006_intrinsic_shape,
)

HC_EV_UM = 1.2398419843320026


@dataclass(frozen=True)
class ResponseCutoff:
    """One source-bounded single-pass response crossing."""

    energy_ev: float
    wavelength_um: float
    branch: str
    target_response: float
    target_absorption_cm_inverse: float
    effective_thickness_um: float
    join_energy_ev: float
    join_absorption_cm_inverse: float


@dataclass(frozen=True)
class CutoffJacobianDiagnostics:
    """Finite-difference identifiability diagnostics for cutoff observations."""

    cutoff_energies_ev: NDArray[np.float64]
    branches: tuple[str, ...]
    jacobian: NDArray[np.float64]
    singular_values: NDArray[np.float64]
    numerical_rank: int
    condition_number: float
    relative_singular_values: NDArray[np.float64]


def _finite_positive(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


def _response(value: float) -> float:
    response = float(value)
    if not isfinite(response) or not 0.0 < response < 1.0:
        raise ValueError("target_response must lie strictly between 0 and 1")
    return response


def absorption_for_target_response_cm_inverse(
    effective_thickness_um: float,
    target_response: float = 0.5,
) -> float:
    """Return the absorption coefficient needed for a single-pass response.

    The model is ``R = 1-exp(-alpha*d)`` with ``d`` converted from micrometres
    to centimetres.
    """

    thickness = _finite_positive(
        effective_thickness_um,
        name="effective_thickness_um",
    )
    response = _response(target_response)
    thickness_cm = thickness * 1.0e-4
    return float(-log(1.0 - response) / thickness_cm)


def single_pass_absorptance(
    absorption_cm_inverse: ArrayLike,
    effective_thickness_um: float,
) -> NDArray[np.float64]:
    """Evaluate ``1-exp(-alpha*d)`` for a declared effective thickness."""

    absorption = np.asarray(absorption_cm_inverse, dtype=float)
    if not np.all(np.isfinite(absorption)) or np.any(absorption < 0.0):
        raise ValueError("absorption_cm_inverse must be finite and non-negative")
    thickness = _finite_positive(
        effective_thickness_um,
        name="effective_thickness_um",
    )
    optical_depth = absorption * thickness * 1.0e-4
    return np.asarray(-np.expm1(-optical_depth), dtype=float)


def cutoff_wavelength_um(energy_ev: float) -> float:
    """Convert a positive photon energy to vacuum wavelength in micrometres."""

    energy = _finite_positive(energy_ev, name="energy_ev")
    return HC_EV_UM / energy


def urbach_tail_cutoff_energy_ev(
    *,
    join_energy_ev: float,
    tail_energy_ev: float,
    join_absorption_cm_inverse: float,
    effective_thickness_um: float,
    target_response: float = 0.5,
) -> float:
    """Return the analytical response crossing on an exponential tail.

    For ``alpha(E)=alpha_join*exp((E-E_join)/W)``, the crossing is

    ``E_cut=E_join+W*ln(alpha_target/alpha_join)``.

    A value above ``join_energy_ev`` is rejected because the assumed tail branch
    would no longer be self-consistent.
    """

    join_energy = _finite_positive(join_energy_ev, name="join_energy_ev")
    width = _finite_positive(tail_energy_ev, name="tail_energy_ev")
    join_absorption = _finite_positive(
        join_absorption_cm_inverse,
        name="join_absorption_cm_inverse",
    )
    target_absorption = absorption_for_target_response_cm_inverse(
        effective_thickness_um,
        target_response,
    )
    cutoff = join_energy + width * log(target_absorption / join_absorption)
    if cutoff > join_energy + 1.0e-14:
        raise ValueError("declared response crossing lies above the Urbach branch")
    return float(cutoff)


def urbach_thickness_shift_ev(
    tail_energy_ev: float,
    thickness_ratio: float,
) -> float:
    """Return ``E_cut(d2)-E_cut(d1)`` for ``d2/d1=thickness_ratio``."""

    width = _finite_positive(tail_energy_ev, name="tail_energy_ev")
    ratio = _finite_positive(thickness_ratio, name="thickness_ratio")
    return float(-width * log(ratio))


def _chang_absorption_cm_inverse(
    energy_ev: float,
    *,
    edge_ev: float,
    urbach_width_ev: float,
    hyperbola_b_ev: float,
    amplitude_cm_inverse: float,
) -> float:
    shape = chang_2006_absorption_shape(
        np.asarray([energy_ev], dtype=float),
        edge_ev=edge_ev,
        urbach_width_ev=urbach_width_ev,
        hyperbola_b_ev=hyperbola_b_ev,
    )
    return float(amplitude_cm_inverse * shape[0])


def chang_2006_response_cutoff(
    *,
    edge_ev: float,
    urbach_width_ev: float,
    hyperbola_b_ev: float,
    amplitude_cm_inverse: float,
    effective_thickness_um: float,
    target_response: float = 0.5,
    enforce_source_domain: bool = True,
    absolute_tolerance_ev: float = 1.0e-12,
) -> ResponseCutoff:
    """Solve one Chang 2006 single-pass response crossing by bisection."""

    edge = _finite_positive(edge_ev, name="edge_ev")
    width = _finite_positive(urbach_width_ev, name="urbach_width_ev")
    b_value = _finite_positive(hyperbola_b_ev, name="hyperbola_b_ev")
    amplitude = _finite_positive(amplitude_cm_inverse, name="amplitude_cm_inverse")
    thickness = _finite_positive(
        effective_thickness_um,
        name="effective_thickness_um",
    )
    response = _response(target_response)
    tolerance = _finite_positive(
        absolute_tolerance_ev,
        name="absolute_tolerance_ev",
    )
    if not isinstance(enforce_source_domain, bool):
        raise ValueError("enforce_source_domain must be boolean")

    relative_lower, relative_upper = CHANG_2006_RELATIVE_ENERGY_RANGE_EV
    lower = edge + relative_lower if enforce_source_domain else max(1.0e-12, edge - 1.0)
    upper = edge + relative_upper if enforce_source_domain else edge + 2.0
    target_absorption = absorption_for_target_response_cm_inverse(thickness, response)

    def residual(energy: float) -> float:
        return _chang_absorption_cm_inverse(
            energy,
            edge_ev=edge,
            urbach_width_ev=width,
            hyperbola_b_ev=b_value,
            amplitude_cm_inverse=amplitude,
        ) - target_absorption

    lower_residual = residual(lower)
    upper_residual = residual(upper)
    if lower_residual > 0.0:
        raise ValueError(
            "response crossing lies below the authorized Chang relative-energy domain"
        )
    if upper_residual < 0.0:
        raise ValueError(
            "response crossing lies above the authorized Chang relative-energy domain"
        )

    left = lower
    right = upper
    while 0.5 * (right - left) > tolerance:
        midpoint = 0.5 * (left + right)
        if residual(midpoint) >= 0.0:
            right = midpoint
        else:
            left = midpoint
    cutoff = 0.5 * (left + right)

    join_energy = edge + 0.5 * width
    join_shape = float(
        chang_2006_intrinsic_shape(
            np.asarray([join_energy], dtype=float),
            edge_ev=edge,
            hyperbola_b_ev=b_value,
        )[0]
    )
    join_absorption = amplitude * join_shape
    branch = "tail" if cutoff < join_energy else "intrinsic"

    return ResponseCutoff(
        energy_ev=float(cutoff),
        wavelength_um=cutoff_wavelength_um(cutoff),
        branch=branch,
        target_response=response,
        target_absorption_cm_inverse=target_absorption,
        effective_thickness_um=thickness,
        join_energy_ev=join_energy,
        join_absorption_cm_inverse=join_absorption,
    )


def chang_2006_cutoff_jacobian(
    *,
    edge_ev: float,
    urbach_width_ev: float,
    hyperbola_b_ev: float,
    amplitude_cm_inverse: float,
    designs: Sequence[tuple[float, float]],
    edge_step_ev: float = 1.0e-6,
    width_step_ev: float = 1.0e-6,
    log_amplitude_step: float = 1.0e-5,
    log_b_step: float = 1.0e-5,
    relative_rank_tolerance: float = 1.0e-8,
) -> CutoffJacobianDiagnostics:
    """Return a cutoff Jacobian for ``(Eg, W, ln A, ln b)``.

    Each design tuple is ``(effective_thickness_um, target_response)``. All
    perturbed responses must remain in the Chang source-relative energy domain.
    """

    if len(designs) == 0:
        raise ValueError("designs must not be empty")
    normalized_designs: list[tuple[float, float]] = []
    for thickness, response in designs:
        normalized_designs.append(
            (
                _finite_positive(thickness, name="design thickness"),
                _response(response),
            )
        )
    rank_tolerance = _finite_positive(
        relative_rank_tolerance,
        name="relative_rank_tolerance",
    )

    base_parameters = np.asarray(
        [
            _finite_positive(edge_ev, name="edge_ev"),
            _finite_positive(urbach_width_ev, name="urbach_width_ev"),
            log(_finite_positive(amplitude_cm_inverse, name="amplitude_cm_inverse")),
            log(_finite_positive(hyperbola_b_ev, name="hyperbola_b_ev")),
        ],
        dtype=float,
    )
    steps = np.asarray(
        [
            _finite_positive(edge_step_ev, name="edge_step_ev"),
            _finite_positive(width_step_ev, name="width_step_ev"),
            _finite_positive(log_amplitude_step, name="log_amplitude_step"),
            _finite_positive(log_b_step, name="log_b_step"),
        ],
        dtype=float,
    )

    def evaluate(parameters: NDArray[np.float64]) -> tuple[NDArray[np.float64], tuple[str, ...]]:
        edge_value, width_value, log_amplitude, log_b = parameters
        energies: list[float] = []
        branches: list[str] = []
        for thickness, response in normalized_designs:
            result = chang_2006_response_cutoff(
                edge_ev=float(edge_value),
                urbach_width_ev=float(width_value),
                hyperbola_b_ev=exp(float(log_b)),
                amplitude_cm_inverse=exp(float(log_amplitude)),
                effective_thickness_um=thickness,
                target_response=response,
            )
            energies.append(result.energy_ev)
            branches.append(result.branch)
        return np.asarray(energies, dtype=float), tuple(branches)

    base_energies, base_branches = evaluate(base_parameters)
    jacobian = np.empty((len(normalized_designs), 4), dtype=float)
    for column, step in enumerate(steps):
        plus = base_parameters.copy()
        minus = base_parameters.copy()
        plus[column] += step
        minus[column] -= step
        plus_values, _ = evaluate(plus)
        minus_values, _ = evaluate(minus)
        jacobian[:, column] = (plus_values - minus_values) / (2.0 * step)

    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    if singular_values.size == 0 or singular_values[0] == 0.0:
        rank = 0
        condition = float("inf")
        relative = np.zeros_like(singular_values)
    else:
        relative = singular_values / singular_values[0]
        rank = int(np.count_nonzero(relative > rank_tolerance))
        condition = (
            float(singular_values[0] / singular_values[-1])
            if singular_values[-1] > 0.0
            else float("inf")
        )

    return CutoffJacobianDiagnostics(
        cutoff_energies_ev=base_energies,
        branches=base_branches,
        jacobian=jacobian,
        singular_values=np.asarray(singular_values, dtype=float),
        numerical_rank=rank,
        condition_number=condition,
        relative_singular_values=np.asarray(relative, dtype=float),
    )
