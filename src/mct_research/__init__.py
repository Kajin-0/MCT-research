"""Executable analytical models for HgCdTe research."""

from .kane8 import ALPHA_EV_A2, KaneParameters, hamiltonian, time_reversal_residual
from .projection import closure_residual, design_diagnostics, fit_parameters, parameter_templates

__all__ = [
    "ALPHA_EV_A2",
    "KaneParameters",
    "closure_residual",
    "design_diagnostics",
    "fit_parameters",
    "hamiltonian",
    "parameter_templates",
    "time_reversal_residual",
]
