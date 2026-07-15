"""Executable analytical models for HgCdTe research."""

from .kane8 import (
    ALPHA_EV_A2,
    ExtendedKaneParameters,
    KaneParameters,
    hamiltonian,
    hamiltonian_two_p,
    time_reversal_residual,
    time_reversal_residual_two_p,
)
from .projection import (
    closure_residual,
    design_diagnostics,
    extended_closure_residual,
    extended_design_diagnostics,
    fit_extended_parameters,
    fit_parameters,
    parameter_templates,
)

__all__ = [
    "ALPHA_EV_A2",
    "ExtendedKaneParameters",
    "KaneParameters",
    "closure_residual",
    "design_diagnostics",
    "extended_closure_residual",
    "extended_design_diagnostics",
    "fit_extended_parameters",
    "fit_parameters",
    "hamiltonian",
    "hamiltonian_two_p",
    "parameter_templates",
    "time_reversal_residual",
    "time_reversal_residual_two_p",
]
