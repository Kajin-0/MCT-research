#!/usr/bin/env python3
"""Audit primary CdTe lattice/expansion sources and bound a provisional 0 K lattice."""

from __future__ import annotations

import json
import math
import numpy as np

WILLIAMS_T_C = np.asarray([20, 110, 132, 206, 238, 305, 315, 382, 420], float)
WILLIAMS_OBS_A = np.asarray([6.4809, 6.4835, 6.4848, 6.4870, 6.4886, 6.4910, 6.4912, 6.4936, 6.4955], float)
WILLIAMS_PRINTED_CALC_A = np.asarray([6.4808, 6.4838, 6.4846, 6.4827, 6.4884, 6.4909, 6.4913, 6.4940, 6.4956], float)
SMITH_T_K = np.asarray([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,24,25,26,28,30,32,57.5,65,75,85,283], float)
SMITH_ALPHA_1E8 = np.asarray([-0.14,-0.48,-1.42,-4.50,-11.2,-22.2,-38.0,-57.3,-79.0,-101.0,-124.5,-148.1,-170.0,-189.0,-206.5,-223.8,-239.0,-254.0,-265.0,-283.0,-295.0,-300.0,-303.0,-304.0,-300.0,-294.0,-40.0,15.0,92.0,157.0,470.0], float)
PDF_HASHES = {
    "williams1969": "963891204abd0b3c434297eec3a1d337c7bc67a3b937eda4bdfc373746702bab",
    "smith_white1975": "521e58912b46c6fba70f6e7c24135d79e8aa50d8ddc93addbaf97c4d38f74237",
    "horning1986": "c94207304b5967f4d955f0440c19589901f32404ad932368521971c30a2bfef9",
}


def lattice_a(t_c):
    t = np.asarray(t_c, dtype=float)
    return 6.4802 + 31.94e-6*t + 7.55e-9*t**2 + 9.25e-12*t**3


def alpha_williams(t_c):
    t = np.asarray(t_c, dtype=float)
    return 4.932e-6 + 1.165e-9*t + 1.428e-12*t**2


def trapz(x, y):
    return float(np.sum(0.5*(y[1:]+y[:-1])*np.diff(x)))


def analyze():
    calculated = lattice_a(WILLIAMS_T_C)
    residual = WILLIAMS_OBS_A - calculated
    printed_error = WILLIAMS_PRINTED_CALC_A - calculated
    anchor_a = float(lattice_a(20.0))
    anchor_alpha = float(alpha_williams(20.0))
    residual_envelope = float(np.max(np.abs(residual)))
    temperature_bound = anchor_a*anchor_alpha*5.0
    anchor_bound = residual_envelope + temperature_bound

    alpha = SMITH_ALPHA_1E8*1e-8
    mask = SMITH_T_K <= 85.0
    low_integral = -170e-12*2.0**4/4.0 + trapz(SMITH_T_K[mask], alpha[mask])
    alpha85 = float(alpha[SMITH_T_K == 85.0][0])
    alpha283 = float(alpha[SMITH_T_K == 283.0][0])
    final_ten_k = 0.5*(alpha283 + anchor_alpha)*(293.15-283.0)
    width = 283.0-85.0
    i_central = low_integral + 0.5*(alpha85+alpha283)*width + final_ten_k
    i_min = low_integral + alpha85*width + final_ten_k
    i_max = low_integral + alpha283*width + final_ten_k
    a0 = anchor_a*math.exp(-i_central)
    a0_lo = (anchor_a-anchor_bound)*math.exp(-i_max)
    a0_hi = (anchor_a+anchor_bound)*math.exp(-i_min)

    if abs(float(printed_error[3])) < 0.004:
        raise RuntimeError("206 C source-table discrepancy not detected")
    if not (a0_lo < a0 < a0_hi):
        raise RuntimeError("invalid provisional interval")
    if (a0_hi-a0_lo) < 0.004:
        raise RuntimeError("bridge uncertainty understated")

    return {
        "status": "source_chain_audited_but_execution_gate_remains_closed",
        "pdf_sha256": PDF_HASHES,
        "williams1969": {
            "doi": "10.1016/0038-1098(69)90296-8",
            "method": "Unicam 19 cm X-ray powder camera; 99.999 percent CdTe",
            "anchor_temperature_c": 20.0,
            "anchor_lattice_a": anchor_a,
            "observed_anchor_lattice_a": float(WILLIAMS_OBS_A[0]),
            "fit_residual_rms_a": float(np.sqrt(np.mean(residual**2))),
            "fit_residual_maximum_a": residual_envelope,
            "temperature_control_bound_c": 5.0,
            "temperature_component_bound_a": temperature_bound,
            "conservative_anchor_bound_a": anchor_bound,
            "printed_206c_calculated_a": float(WILLIAMS_PRINTED_CALC_A[3]),
            "polynomial_206c_calculated_a": float(calculated[3]),
            "decision_206c": "printed_calculated_value_is_a_typographical_error",
        },
        "smith_white1975": {
            "doi": "10.1088/0022-3719/8/13/012",
            "method": "three-terminal capacitance dilatometer",
            "primary_ranges_k": ["2-33", "55-90", "room_temperature"],
            "cdte2_low_temperature_law": "alpha=-(170+-10)e-12*T^3 below 4 K",
            "literature_reprinted_rows_k": [57.5, 65.0],
            "direct_rows_used_through_k": 85.0,
            "room_temperature_alpha_per_k": alpha283,
            "direct_low_integral_0_to_85": low_integral,
        },
        "horning1986": {
            "doi": "10.1103/PhysRevB.34.3970",
            "room_temperature_statement_a": 6.484,
            "anchor_admissible": False,
            "reason": "rounded contextual statement without traceable uncertainty or lattice extraction",
        },
        "provisional_zero_k_derivation": {
            "assumption": "alpha is monotone between the direct 85 K and 283 K endpoints",
            "central_bridge": "linear alpha between 85 and 283 K",
            "integral_alpha_0_to_293_central": i_central,
            "integral_alpha_0_to_293_min": i_min,
            "integral_alpha_0_to_293_max": i_max,
            "a0_central_a": a0,
            "a0_lower_a": a0_lo,
            "a0_upper_a": a0_hi,
            "half_width_a": 0.5*(a0_hi-a0_lo),
            "authorization": "planning_diagnostic_only",
        },
        "decision": "The 90-293 K integral still dominates uncertainty; keep ready_for_execution false.",
        "next_primary_sources": [
            {"doi": "10.1364/AO.11.000841", "purpose": "10-300 K CdTe bridge; polycrystalline Irtran 6"},
            {"doi": "10.1088/0022-3727/6/5/315", "purpose": "42-300 K single-crystal CdTe expansion"},
        ],
    }


def main():
    print(json.dumps(analyze(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
